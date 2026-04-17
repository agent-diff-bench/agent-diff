"""LLM review layer for alias suggestions.

Takes the output of ``suggest_aliases`` and sends each resource's
candidates through an LLM for ``variant`` / ``distinct`` / ``uncertain``
classification. The LLM is a pluggable callable — the caller wires
in whichever client they want (Claude CLI, Anthropic SDK, mock for
tests). Verdicts are cached by input hash so re-runs are free.

One call per resource (batched), not one per candidate — lets the
LLM compare candidates for the same resource in one context.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pipeline.config import PipelineConfig
from pipeline.aliases.suggest import Suggestion

_VALID_VERDICTS = frozenset({"variant", "distinct", "uncertain"})


@dataclass(frozen=True)
class ReviewedSuggestion:
    suggestion: Suggestion
    verdict: str   # "variant" | "distinct" | "uncertain"
    reason: str    # LLM's one-line explanation


def review_suggestions(
    suggestions: dict[str, list[Suggestion]],
    spec: dict[str, Any],
    config: PipelineConfig,
    llm_call: Callable[[str], str],
    cache_path: Path | None = None,
) -> dict[str, list[ReviewedSuggestion]]:
    """Send each resource's candidates through the LLM, return verdicts."""
    raw_component_schemas = (spec.get("components") or {}).get("schemas") or {}
    component_schemas: dict[str, Any] = (
        raw_component_schemas if isinstance(raw_component_schemas, dict) else {}
    )
    cache = _load_cache(cache_path)
    reviewed: dict[str, list[ReviewedSuggestion]] = {}

    for resource, resource_suggestions in suggestions.items():
        cached: dict[str, tuple[str, str]] = {}
        uncached: list[Suggestion] = []
        for suggestion in resource_suggestions:
            key = _cache_key(resource, suggestion, component_schemas.get(suggestion.schema_name))
            if key in cache:
                cached[suggestion.schema_name] = cache[key]
            else:
                uncached.append(suggestion)

        new_verdicts: dict[str, tuple[str, str]] = {}
        if uncached:
            prompt = _build_prompt(resource, config, uncached, component_schemas)
            response = llm_call(prompt)
            new_verdicts = _parse_response(response)
            for suggestion in uncached:
                verdict_reason = new_verdicts.get(
                    suggestion.schema_name, ("uncertain", "no verdict from LLM")
                )
                key = _cache_key(resource, suggestion, component_schemas.get(suggestion.schema_name))
                cache[key] = verdict_reason
                new_verdicts[suggestion.schema_name] = verdict_reason

        reviewed[resource] = [
            ReviewedSuggestion(
                suggestion=suggestion,
                verdict=(cached.get(suggestion.schema_name) or new_verdicts.get(suggestion.schema_name) or ("uncertain", "missing"))[0],
                reason=(cached.get(suggestion.schema_name) or new_verdicts.get(suggestion.schema_name) or ("uncertain", "missing"))[1],
            )
            for suggestion in resource_suggestions
        ]

    _save_cache(cache_path, cache)
    return reviewed


def _cache_key(resource: str, suggestion: Suggestion, schema_body: Any) -> str:
    """Stable hash of everything that could affect the LLM verdict."""
    payload = {
        "resource": resource,
        "schema_name": suggestion.schema_name,
        "normalized": suggestion.normalized,
        "matched_token": suggestion.matched_token,
        "schema_body": schema_body,
    }
    serialized = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def _load_cache(cache_path: Path | None) -> dict[str, tuple[str, str]]:
    if cache_path is None or not cache_path.exists():
        return {}
    try:
        data = json.loads(cache_path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    entries = data.get("entries") or {}
    return {
        key: (value["verdict"], value["reason"])
        for key, value in entries.items()
        if isinstance(value, dict) and "verdict" in value and "reason" in value
    }


def _save_cache(cache_path: Path | None, cache: dict[str, tuple[str, str]]) -> None:
    if cache_path is None:
        return
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "version": "1",
        "entries": {
            key: {"verdict": verdict, "reason": reason}
            for key, (verdict, reason) in cache.items()
        },
    }
    cache_path.write_text(json.dumps(data, indent=2, sort_keys=True))


def _build_prompt(
    resource: str,
    config: PipelineConfig,
    suggestions: list[Suggestion],
    component_schemas: Mapping[str, Any],
) -> str:
    existing = sorted(config.resources.aliases_by_resource.get(resource, frozenset()))
    lines = [
        f'You are reviewing proposed schema aliases for the "{resource}" resource.',
        "",
        f"The full OpenAPI spec is available at: `{config.openapi_path}`",
        "If any schema body below is truncated or unclear, read the spec directly.",
        "",
        f"Existing aliases for {resource}:",
    ]
    for alias in existing:
        lines.append(f"  - {alias}")
    lines.append("")
    lines.append("Candidate aliases to review:")
    lines.append("")
    for index, suggestion in enumerate(suggestions, start=1):
        body = component_schemas.get(suggestion.schema_name)
        body_json = json.dumps(body, indent=2) if body is not None else "<missing>"
        if len(body_json) > 2000:
            body_json = body_json[:2000] + "\n... (truncated)"
        lines.append(f"{index}. schema_name: {suggestion.schema_name}")
        lines.append(f"   ref_count: {suggestion.ref_count}")
        lines.append(f"   matched_token: {suggestion.matched_token}")
        lines.append(f"   schema_body: {body_json}")
        lines.append("")
    lines.append(
        f'For each candidate, decide: is this schema a VARIANT of "{resource}" '
        "(same underlying entity, possibly with more or fewer fields, or a "
        "partial view), or a DISTINCT concept that happens to share a word?"
    )
    lines.append("")
    lines.append("Mark as DISTINCT (not variant):")
    lines.append("- Webhook event payloads (e.g. webhook-team-created, webhook-pull-request-assigned)")
    lines.append("  — these wrap the entity in an event envelope, they are not the entity itself")
    lines.append("- Primitive type schemas that hold a single value like a SHA, ID, or OID")
    lines.append("  — these are field types, not entity variants")
    lines.append("- Configuration, policy, or settings schemas that apply to the entity")
    lines.append("  — these describe rules about the entity, not the entity itself")
    lines.append("- Enum or status value schemas (e.g. ProjectStatus, ProjectVisibility)")
    lines.append("")
    lines.append("Mark as VARIANT only if the schema represents the same underlying entity")
    lines.append("with a different set of fields (compact view, full view, search result, etc.)")
    lines.append("")
    lines.append("Respond in JSON (no markdown fences):")
    lines.append(
        '[{"schema_name": "...", "verdict": "variant" | "distinct" | "uncertain", "reason": "brief one-line explanation"}, ...]'
    )
    return "\n".join(lines)


def _parse_response(response: str) -> dict[str, tuple[str, str]]:
    """Parse the LLM JSON response into ``{schema_name: (verdict, reason)}``."""
    start = response.find("[")
    end = response.rfind("]")
    if start == -1 or end == -1 or end <= start:
        return {}
    try:
        entries = json.loads(response[start : end + 1])
    except json.JSONDecodeError:
        return {}
    result: dict[str, tuple[str, str]] = {}
    if not isinstance(entries, list):
        return {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = entry.get("schema_name")
        verdict = entry.get("verdict")
        reason = entry.get("reason", "")
        if isinstance(name, str) and verdict in _VALID_VERDICTS:
            result[name] = (verdict, str(reason))
    return result


def format_approved_aliases_yaml(
    reviewed: dict[str, list[ReviewedSuggestion]],
    *,
    include_uncertain: bool = False,
) -> str:
    """Emit a yaml snippet with variant (and optionally uncertain) approved."""
    lines = [
        "# LLM-reviewed alias suggestions.",
        "# 'variant' verdicts are active aliases; 'uncertain' are commented",
        "# out for manual review; 'distinct' are dropped.",
        "",
        "resources:",
    ]
    for resource in sorted(reviewed.keys()):
        variants = [reviewed_entry for reviewed_entry in reviewed[resource] if reviewed_entry.verdict == "variant"]
        uncertains = [reviewed_entry for reviewed_entry in reviewed[resource] if reviewed_entry.verdict == "uncertain"]
        if not variants and not (include_uncertain and uncertains):
            continue
        lines.append(f"  {resource}:")
        lines.append("    aliases:")
        for entry in variants:
            suggestion = entry.suggestion
            lines.append(
                f"      - {suggestion.normalized}"
                f"  # variant, {suggestion.ref_count} refs — {entry.reason}"
            )
        if include_uncertain:
            for entry in uncertains:
                suggestion = entry.suggestion
                lines.append(
                    f"      # - {suggestion.normalized}"
                    f"  # uncertain, {suggestion.ref_count} refs — {entry.reason}"
                )
    return "\n".join(lines) + "\n"
