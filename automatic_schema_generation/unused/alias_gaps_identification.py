"""Path-level alias gap identification — first heuristic of the alias
completeness check.

Walks every path in the spec, tokenizes the URL path string plus the
parameter ``name`` fields at both path-item level and operation level,
and produces a ``ReviewBucket`` of tokens that didn't resolve against
the config's pre-expanded ``aliases_lookup``. The output is a JSON file
that a future LLM-judgement step will consume, annotate with
accept/reject decisions, and feed back into the walker so subsequent
runs skip already-judged tokens.

Scope — intentionally minimal:

  * Sources walked: URL path segments (brace-stripped for
    ``{param}`` placeholders), ``path_item.parameters`` entries,
    and each ``operation.parameters`` entry. Nothing else.
  * Lookup policy: try the whole normalized string first (the
    alias expansion at config-load time means compound forms like
    ``pull_request_id`` are already in the lookup directly), then
    fall back to splitting on underscores and checking each part.
  * Filtering: ``config.vocabulary.ignore_values`` is matched against
    the raw pre-normalization string; ``ignore_tokens`` is matched
    against each post-split token.
  * Parameter ``$ref``s are skipped. Resolving them is a deferred
    future step; any parameter entry that's a bare ``$ref`` without
    a local ``name`` field contributes nothing to this pass.
  * LLM judgement: the dataclass carries a ``judgement`` field that
    defaults to ``None`` and is never populated by the walker. A
    later milestone will read prior output, skip tokens with a
    recorded ``{"status": "reject", ...}``, and populate the field
    from an LLM call.

Output schema::

    {
      "_meta": {
        "generated_at":    "<iso-timestamp>",
        "config_path":     "<absolute path or null>",
        "spec_path":       "<absolute path or null>",
        "candidate_count": <int>
      },
      "candidates": [
        {
          "token":     "<normalized snake_case string>",
          "judgement": null,
          "excerpts":  [<excerpt dict>, ...]
        },
        ...
      ]
    }

Excerpts come in two shapes depending on where the token was found:

  * Path-level excerpt (URL string segments and shared ``parameters``
    at the path-item level)::

        {"path": "<url>", "path_item": <verbatim path_item dict>}

  * Operation-level excerpt (``parameters`` at an individual HTTP
    verb block). Merges the path-level context with the specific
    operation so the LLM sees both layers in one object without
    sibling operations cluttering the view::

        {"path":       "<url>",
         "method":     "<VERB>",
         "path_level": <path_item with HTTP verb blocks stripped>,
         "operation":  <verbatim operation dict>}
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ._text import normalize_identifier
from .config import PipelineConfig


# OpenAPI 3.x HTTP methods. Keys on a path item that aren't one of
# these are metadata (``summary``, ``description``, shared
# ``parameters``, ``servers``, ``$ref``), not operation blocks.
_HTTP_METHODS: frozenset[str] = frozenset({
    "get", "post", "put", "patch", "delete", "head", "options", "trace",
})


@dataclass
class UnresolvedCandidate:
    """One token that didn't resolve to any known resource alias.

    ``token`` is the normalized snake_case form. It's the primary
    deduplication key for the bucket.

    ``excerpts`` is a list of spec fragments — one per distinct
    occurrence — that together give an LLM enough context to decide
    whether the token refers to an as-yet-unmapped resource or to
    something that should be ignored (action verb, metadata, external
    reference, etc.). Excerpts within one candidate are deduped by
    their JSON-canonical hash, so two walker sources emitting the
    same fragment for the same token collapse to one entry.

    ``judgement`` is a placeholder for a future LLM-review step. It
    defaults to ``None`` in this milestone and is never populated by
    the walker. A later milestone will read prior output, examine
    each candidate's ``judgement``, and skip tokens that previous
    runs marked as ``"status": "reject"``.
    """

    token: str
    excerpts: list[dict[str, Any]] = field(default_factory=list)
    judgement: dict[str, Any] | None = None


@dataclass
class ReviewBucket:
    """Container for the unresolved tokens found in one walker pass."""

    candidates: list[UnresolvedCandidate] = field(default_factory=list)


def find_unresolved_path_tokens(
    spec: dict[str, Any],
    config: PipelineConfig,
) -> ReviewBucket:
    """Walk every path in the spec and collect tokens that don't resolve.

    Three signal sources per path, walked in sequence:

      1. The path string itself. Split on ``/``, drop empty segments,
         strip braces from ``{param}`` placeholders so the parameter
         name flows through the same lookup logic as a plain URL
         segment.
      2. Path-level ``parameters`` — shared across all operations
         under this path item.
      3. Operation-level ``parameters`` — per HTTP verb block. The
         excerpt for these tokens merges the path-level context with
         the specific operation so the LLM sees both layers.

    Each source's raw string goes through ``_check_raw`` which
    applies vocabulary filters, normalizes, tries the compound form
    in ``aliases_lookup`` first, and falls back to splitting on
    underscores. Unresolved parts are accumulated in a dict keyed by
    token, deduping excerpts within each candidate by their JSON
    hash.

    The accumulator is materialized into a ``ReviewBucket`` with
    candidates sorted alphabetically by token and excerpts within
    each candidate sorted by ``(path, method)``, giving byte-stable
    diffs across runs even if the spec's dict iteration order
    changes.
    """
    ignore_values_patterns: list[re.Pattern[str]] = [
        re.compile(pattern) for pattern in config.vocabulary.ignore_values
    ]
    ignore_tokens_patterns: list[re.Pattern[str]] = [
        re.compile(pattern) for pattern in config.vocabulary.ignore_tokens
    ]
    aliases_lookup = config.resources.aliases_lookup

    # Accumulator: token → {excerpt_hash → excerpt_dict}. The inner
    # dict gives us O(1) "have I already stored this excerpt for
    # this token" dedup and stable materialization order.
    by_token: dict[str, dict[str, dict[str, Any]]] = {}

    for path, path_item in (spec.get("paths") or {}).items():
        if not isinstance(path, str) or not isinstance(path_item, dict):
            continue

        # Build the path-level excerpt once per path — reused by
        # both the URL-segment walk and the shared parameter walk
        # below. Deep-copied so downstream mutations of the output
        # JSON can't corrupt the spec dict we were handed.
        path_level_excerpt: dict[str, Any] = {
            "path": path,
            "path_item": copy.deepcopy(path_item),
        }

        # 1. Tokenize the path string itself.
        for segment in path.split("/"):
            if not segment:
                continue
            # Unwrap parameter placeholders so ``{pull_number}``
            # contributes ``pull_number`` — the name flows through
            # the same lookup logic as a plain segment like ``pulls``.
            if segment.startswith("{") and segment.endswith("}"):
                segment = segment[1:-1]
            _check_raw(
                raw=segment,
                excerpt=path_level_excerpt,
                by_token=by_token,
                aliases_lookup=aliases_lookup,
                ignore_values_patterns=ignore_values_patterns,
                ignore_tokens_patterns=ignore_tokens_patterns,
            )

        # 2. Path-level ``parameters`` (shared across all operations).
        for parameter in path_item.get("parameters") or []:
            name = _parameter_name_or_none(parameter)
            if name is None:
                continue
            _check_raw(
                raw=name,
                excerpt=path_level_excerpt,
                by_token=by_token,
                aliases_lookup=aliases_lookup,
                ignore_values_patterns=ignore_values_patterns,
                ignore_tokens_patterns=ignore_tokens_patterns,
            )

        # 3. Operation-level ``parameters`` — per HTTP verb block.
        for method, operation in path_item.items():
            if (
                not isinstance(method, str)
                or method.lower() not in _HTTP_METHODS
                or not isinstance(operation, dict)
            ):
                continue

            # Merge the path-level context with the specific
            # operation block so the LLM sees both layers in one
            # excerpt. ``path_level_block`` is the path_item with
            # HTTP-verb blocks stripped — shared parameters, the
            # summary, description, and servers remain visible.
            path_level_block = {
                key: copy.deepcopy(value)
                for key, value in path_item.items()
                if not isinstance(key, str) or key.lower() not in _HTTP_METHODS
            }
            operation_excerpt: dict[str, Any] = {
                "path": path,
                "method": method.upper(),
                "path_level": path_level_block,
                "operation": copy.deepcopy(operation),
            }

            for parameter in operation.get("parameters") or []:
                name = _parameter_name_or_none(parameter)
                if name is None:
                    continue
                _check_raw(
                    raw=name,
                    excerpt=operation_excerpt,
                    by_token=by_token,
                    aliases_lookup=aliases_lookup,
                    ignore_values_patterns=ignore_values_patterns,
                    ignore_tokens_patterns=ignore_tokens_patterns,
                )

    # Materialize into the final sorted ReviewBucket. Candidates
    # alphabetically; excerpts within each candidate by
    # (path, method) so reruns produce byte-stable diffs.
    candidates: list[UnresolvedCandidate] = []
    for token in sorted(by_token):
        excerpts = sorted(
            by_token[token].values(),
            key=lambda excerpt: (
                str(excerpt.get("path", "")),
                str(excerpt.get("method", "")),
            ),
        )
        candidates.append(UnresolvedCandidate(
            token=token,
            excerpts=excerpts,
            judgement=None,
        ))

    return ReviewBucket(candidates=candidates)


def _check_raw(
    *,
    raw: str,
    excerpt: dict[str, Any],
    by_token: dict[str, dict[str, dict[str, Any]]],
    aliases_lookup: Any,
    ignore_values_patterns: list[re.Pattern[str]],
    ignore_tokens_patterns: list[re.Pattern[str]],
) -> None:
    """Check one raw string against the alias set, record any gaps.

    Called from three places (URL segment walk, path-level parameter
    walk, operation-level parameter walk) — the three-call-site rule
    for helpers.

    Flow:

      1. Apply ``ignore_values`` against the RAW string so patterns
         that depend on the original case (``^[A-Z][A-Z0-9_]*$``)
         have something to match against before normalization
         lowercases everything.
      2. Normalize via ``normalize_identifier``. An empty result is
         silently dropped — nothing useful to look up.
      3. Try the fully normalized compound in ``aliases_lookup``.
         The config-load-time alias expansion means compound forms
         like ``pull_request_id`` are in the lookup directly, so a
         hit here means "resolved, no gap" and we short-circuit.
      4. On miss, split on underscores and check each part. Parts
         that match ``ignore_tokens`` or are themselves in
         ``aliases_lookup`` are skipped; the rest are recorded as
         unresolved in ``by_token``.

    Excerpt deduplication happens inside step 4: the excerpt is
    hashed with sha256 over its JSON-canonical form, and the hash
    is the inner-dict key under ``by_token[part]``. Two different
    walker sources emitting the same excerpt for the same token
    collapse to one stored copy.
    """
    for pattern in ignore_values_patterns:
        if pattern.fullmatch(raw):
            return

    normalized = normalize_identifier(raw)
    if not normalized:
        return

    if normalized in aliases_lookup:
        return

    for part in normalized.split("_"):
        if not part:
            continue
        if any(pattern.fullmatch(part) for pattern in ignore_tokens_patterns):
            continue
        if part in aliases_lookup:
            continue
        # Dedup the excerpt within this candidate by hashing its
        # canonical JSON form. The ``default=str`` is a safety net
        # for any non-JSON-native value that might sneak in from
        # the spec (unlikely at this depth, but free insurance).
        excerpt_hash = hashlib.sha256(
            json.dumps(excerpt, sort_keys=True, default=str).encode()
        ).hexdigest()
        inner = by_token.setdefault(part, {})
        if excerpt_hash not in inner:
            inner[excerpt_hash] = excerpt


def _parameter_name_or_none(parameter: Any) -> str | None:
    """Return a parameter's ``name`` field, or None if we can't reach it.

    A parameter that's a bare ``$ref`` (no local ``name``) is
    skipped. Resolving ``$ref`` references into
    ``components.parameters`` is deferred to a later milestone —
    GitHub uses shared parameter definitions heavily, and the
    follow-up step will walk them properly. For now, silently skip.
    """
    if not isinstance(parameter, dict):
        return None
    if "$ref" in parameter:
        return None
    name = parameter.get("name")
    if not isinstance(name, str) or not name:
        return None
    return name


def write_review_bucket(
    bucket: ReviewBucket,
    output_path: Path,
    *,
    config_path: Path | None = None,
    spec_path: Path | None = None,
) -> None:
    """Serialize a ``ReviewBucket`` to JSON at the given output path.

    ``judgement`` is always emitted (as ``null`` in this milestone)
    so the schema is stable across future milestones that populate
    it. Callers that want a non-null value can pass a bucket whose
    candidates already have ``judgement`` filled in — the writer
    makes no distinction.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "_meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "config_path": str(config_path) if config_path else None,
            "spec_path": str(spec_path) if spec_path else None,
            "candidate_count": len(bucket.candidates),
        },
        "candidates": [
            {
                "token": candidate.token,
                "judgement": candidate.judgement,
                "excerpts": candidate.excerpts,
            }
            for candidate in bucket.candidates
        ],
    }
    output_path.write_text(json.dumps(payload, indent=2) + "\n")
