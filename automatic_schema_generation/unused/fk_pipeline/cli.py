"""Entry point — ``python -m fk_pipeline.cli <app_config.yaml>``.

Wires the pieces together:

  1. Verify the ``claude`` CLI is available (fail fast, not deep in a
     subprocess).
  2. Load the app config.
  3. Load the OpenAPI spec.
  4. Expand syntactic aliases via LLM (cached).
  5. Run the role classifier.
  6. Resolve per-resource shapes + extract FK candidates.
  7. Run LLM disambiguation on unresolved FK candidates (cached).
  8. Write the ``resource_endpoint_map.json`` artifact.

Deliberately thin: all the interesting decisions live in the modules
this script calls. Its job is only to stitch them together and report
progress to the user.

Progress reporting uses the stdlib ``logging`` module. Every module in
the package logs to a child of the ``fk_pipeline`` logger, which is
configured once in ``main()``. Tests don't call ``main`` so their
runs are silent by default (no handler attached).
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

from .bucketing import build_map
from .candidates import LlmDecision
from .claude_cli import ClaudeCliError, check_claude_cli_available
from .config import FkPipelineConfig, load_config
from .extractor import extract_candidates
from .models import ResourceEndpointMap
from .resolution import resolve_candidates
from .shapes import SHAPES_ARTIFACT_FILENAME, resolve_shapes, write_shapes_artifact
from .vocabulary import (
    PROMPT_VERSION,
    AliasMap,
    expand_aliases,
)
from .writer import ARTIFACT_FILENAME, ArtifactMeta, write_artifact


logger = logging.getLogger("fk_pipeline")


def _configure_logging(*, quiet: bool) -> None:
    """Attach one stderr handler to the ``fk_pipeline`` logger.

    The messages in this package are self-labeling (``[config] ...``,
    ``[aliases] ...``) so the formatter is deliberately minimal —
    just the message, no level prefix, no timestamp. Level is INFO by
    default or WARNING under ``--quiet``; that's where the WARNING
    vs INFO split matters (e.g. the unmatched-vocabulary notice is
    suppressed by normal progress but shown in quiet mode).
    """
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING if quiet else logging.INFO)
    # Don't double-print through root if anyone up the tree has a handler.
    logger.propagate = False


def _load_openapi(path: Path) -> dict[str, Any]:
    """Load an OpenAPI JSON spec and validate minimally.

    Raises if the file doesn't exist, isn't valid JSON, isn't a
    top-level mapping, or lacks ``paths`` / ``components.schemas`` —
    both are load-bearing for every downstream stage.
    """
    if not path.exists():
        raise FileNotFoundError(f"OpenAPI spec not found: {path}")
    try:
        spec = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise ValueError(f"OpenAPI spec at {path} is not valid JSON: {e}")
    if not isinstance(spec, dict):
        raise ValueError(
            f"OpenAPI spec at {path} must be a JSON object at top level, "
            f"got {type(spec).__name__}"
        )
    if "paths" not in spec or not isinstance(spec["paths"], dict):
        raise ValueError(f"OpenAPI spec at {path} has no 'paths' mapping")
    components = spec.get("components")
    if not isinstance(components, dict) or "schemas" not in components:
        raise ValueError(
            f"OpenAPI spec at {path} has no 'components.schemas' mapping"
        )
    return spec


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="fk_pipeline",
        description=(
            "Step 1 of the FK pipeline: build a bidirectional "
            "resource\u2194endpoint map from an OpenAPI spec, with "
            "LLM-assisted syntactic alias expansion."
        ),
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to the app_config.yaml for the target app.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output (warnings and errors still shown).",
    )
    return parser.parse_args(argv)


def _report_llm_error(phase_name: str, err: Exception) -> int:
    """Log a failed LLM phase and return the CLI exit code.

    ``ClaudeCliError`` surfaces the transport-level detail (stderr);
    other exceptions get a traceback via ``logger.exception`` so
    unexpected failures don't disappear into the void.
    """
    if isinstance(err, ClaudeCliError):
        logger.error("claude CLI call failed during %s: %s", phase_name, err)
        if err.stderr:
            logger.error("stderr: %s", err.stderr.strip())
    else:
        logger.exception("error during %s: %s", phase_name, err)
    return 3


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    _configure_logging(quiet=args.quiet)

    # Phases 1–3: setup (preflight + config + spec).
    phase = "startup"
    try:
        phase = "claude CLI preflight"
        check_claude_cli_available()
        phase = "config load"
        cfg: FkPipelineConfig = load_config(args.config)
        phase = "OpenAPI spec load"
        spec = _load_openapi(cfg.openapi_path)
    except (ClaudeCliError, FileNotFoundError, ValueError) as e:
        logger.error("error during %s: %s", phase, e)
        return 2

    logger.info("[config] app_slug=%s", cfg.app_slug)
    logger.info("[config] openapi=%s", cfg.openapi_path)
    resources_preview = ", ".join(cfg.resources[:6])
    if len(cfg.resources) > 6:
        resources_preview += "..."
    logger.info(
        "[config] resources=%d (%s)", len(cfg.resources), resources_preview,
    )
    logger.info("[config] model=%s", cfg.model)
    logger.info("[config] resolution_model=%s", cfg.resolution_model)
    logger.info("[config] use_cache=%s", cfg.use_cache)
    if cfg.vocabulary_ignore_keys:
        logger.info(
            "[config] vocabulary_ignore_keys=%s",
            ", ".join(cfg.vocabulary_ignore_keys),
        )
    if cfg.vocabulary_ignore_values:
        logger.info(
            "[config] vocabulary_ignore_values=%s",
            ", ".join(cfg.vocabulary_ignore_values),
        )
    if cfg.vocabulary_ignore_tokens:
        logger.info(
            "[config] vocabulary_ignore_tokens=%s",
            ", ".join(cfg.vocabulary_ignore_tokens),
        )
    logger.info("[config] output_dir=%s", cfg.output_dir)

    path_count = len(spec.get("paths") or {})
    schema_count = len((spec.get("components") or {}).get("schemas") or {})
    logger.info(
        "[spec] loaded: %d paths, %d component schemas",
        path_count, schema_count,
    )

    # 4. Expand aliases (cached).
    try:
        alias_map: AliasMap = expand_aliases(
            resources=cfg.resources,
            spec=spec,
            naming=cfg.naming,
            model=cfg.model,
            output_dir=cfg.output_dir,
            source_spec_path=str(cfg.openapi_path),
            use_cache=cfg.use_cache,
            vocabulary_ignore_keys=cfg.vocabulary_ignore_keys,
            vocabulary_ignore_values=cfg.vocabulary_ignore_values,
            vocabulary_ignore_tokens=cfg.vocabulary_ignore_tokens,
        )
    except (ClaudeCliError, RuntimeError) as e:
        return _report_llm_error("alias expansion", e)

    total_aliases = sum(
        len(e.syntactic_aliases) for e in alias_map.entries.values()
    )
    logger.info(
        "[aliases] %d syntactic aliases across %d resources (cache_hit=%s)",
        total_aliases, len(alias_map.entries), alias_map.cache_hit,
    )
    if alias_map.unmatched_vocabulary:
        sample = ", ".join(alias_map.unmatched_vocabulary[:8])
        more = len(alias_map.unmatched_vocabulary) - 8
        suffix = f" (+{more} more)" if more > 0 else ""
        # Soft warning: the pipeline kept going but something in the
        # spec didn't map onto any canonical resource, which usually
        # means the scoped_resources list is incomplete.
        logger.warning("[aliases] unmatched vocabulary: %s%s", sample, suffix)

    # 5. Build the resource\u2194endpoint map.
    t1 = time.time()
    rem: ResourceEndpointMap = build_map(
        spec=spec,
        alias_map=alias_map,
        naming=cfg.naming,
    )
    logger.info(
        "[bucket] %d endpoints, %d edges, %d unbucketed (%.2fs)",
        len(rem.endpoints), len(rem.edges), len(rem.unbucketed_endpoints),
        time.time() - t1,
    )

    # 6. Resolve per-resource shapes + extract FK candidates.
    t2 = time.time()
    shapes = resolve_shapes(rem, spec, alias_map)
    shapes_path = cfg.output_dir / SHAPES_ARTIFACT_FILENAME
    write_shapes_artifact(shapes, shapes_path)
    logger.info("[shapes] %s", shapes_path)

    fk_candidates = extract_candidates(
        rem=rem,
        shapes=shapes,
        alias_map=alias_map,
        naming=cfg.naming,
        spec=spec,
    )
    linked_count = sum(1 for c in fk_candidates if not c.needs_llm)
    unresolved_count = len(fk_candidates) - linked_count
    logger.info(
        "[extract] %d FK candidates (linked=%d, unresolved=%d, %.2fs)",
        len(fk_candidates), linked_count, unresolved_count,
        time.time() - t2,
    )

    # 7. LLM disambiguation of unresolved FK candidates (cached).
    # Mutates ``fk_candidates`` in place.
    t3 = time.time()
    try:
        resolution_outcome = resolve_candidates(
            candidates=fk_candidates,
            rem=rem,
            shapes=shapes,
            alias_map=alias_map,
            spec=spec,
            resources=cfg.resources,
            model=cfg.resolution_model,
            output_dir=cfg.output_dir,
            use_cache=cfg.use_cache,
        )
    except (ClaudeCliError, RuntimeError) as e:
        return _report_llm_error("FK resolution", e)

    # Recompute bucket counts post-resolution so the meta reflects
    # the mutated state of ``fk_candidates``.
    final_linked = sum(
        1 for c in fk_candidates
        if not c.needs_llm and c.target_resource is not None
    )
    final_rejected = sum(
        1 for c in fk_candidates
        if c.llm_decision == LlmDecision.REJECTED
    )
    final_unresolved = len(fk_candidates) - final_linked - final_rejected
    logger.info(
        "[resolve] %d linked, %d rejected, %d cardinality-only "
        "(cache_hit=%s, %.2fs)",
        resolution_outcome.linked_count,
        resolution_outcome.rejected_count,
        resolution_outcome.cardinality_only_count,
        resolution_outcome.cache_hit,
        time.time() - t3,
    )

    # 8. Write artifact.
    output_path = cfg.output_dir / ARTIFACT_FILENAME
    meta = ArtifactMeta(
        app_slug=cfg.app_slug,
        source_spec=str(cfg.openapi_path),
        model=cfg.model,
        prompt_version=PROMPT_VERSION,
        user_resource_count=len(cfg.resources),
        endpoint_count=len(rem.endpoints),
        edge_count=len(rem.edges),
        unbucketed_count=len(rem.unbucketed_endpoints),
        vocabulary_cache_hit=alias_map.cache_hit,
        fk_candidate_count=len(fk_candidates),
        fk_linked_count=final_linked,
        fk_unresolved_count=final_unresolved,
        fk_rejected_count=final_rejected,
        fk_llm_linked_count=resolution_outcome.linked_count,
    )
    write_artifact(
        rem=rem,
        output_path=output_path,
        meta=meta,
        resource_order=cfg.resources,
        fk_candidates=fk_candidates,
    )
    logger.info("[write] %s", output_path)

    # Per-resource edge summary so the operator can eyeball the result
    # without opening the artifact. Logged as a single multi-line message
    # to keep lines tied together under a single log record.
    summary_lines = ["", "Per-resource edge counts:"]
    resources_view = rem.resources_view()
    for canonical in cfg.resources:
        edges = resources_view.get(canonical, [])
        role_counts: dict[str, int] = {}
        for e in edges:
            role_counts[e.role.value] = role_counts.get(e.role.value, 0) + 1
        parts = ", ".join(
            f"{role}={count}" for role, count in sorted(role_counts.items())
        )
        line = f"  {canonical}: {len(edges)} edges"
        if parts:
            line += f" ({parts})"
        summary_lines.append(line)
    logger.info("\n".join(summary_lines))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
