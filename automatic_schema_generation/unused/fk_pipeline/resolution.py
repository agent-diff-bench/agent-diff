"""FK candidate resolution via LLM — the semantic disambiguation step.

Runs after ``extractor.py`` on the subset of candidates that the
walker couldn't fully resolve mechanically. The walker is deliberately
a proposal engine (zero false negatives); this module is where
semantic judgement happens.

Two kinds of candidates land here:

  1. **Unresolved** (``needs_llm=True``, ``target_resource is None``)
     — the walker saw something FK-shaped but the field name / schema
     name wasn't in any alias set. The LLM picks a canonical target
     or rejects the candidate.

  2. **Linked without cardinality** (``target_resource`` set,
     ``inferred_cardinality is None``) — the walker knew WHICH
     resource but couldn't decide the relationship type. The LLM
     fills in the cardinality. Not currently produced by step 2
     (every linked candidate ships with a cardinality today) but
     kept in the taxonomy so future proposal types don't need to
     grow their own LLM plumbing.

Self-references the walker recorded as weak (``needs_llm=True`` with
``target_resource == source_resource``) are also re-examined — the
LLM can either confirm the self-reference or reject it.

Closed-world contract: the LLM can only return ``target_resource``
values from the scoped resource list. Anything else is a hallucination
and we replace the decision with a rejection in ``_merge_resolutions``.

Cache contract mirrors ``vocabulary.py``:

    Outputs persist to ``<output_dir>/fk_resolutions.json`` with a
    SHA-256 cache key over the LLM-call inputs. On re-run, if the
    cache file's key matches, we skip the LLM call entirely and just
    apply the cached decisions to the current candidate list.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import load_prompt_template
from .candidates import (
    CandidateSignature,
    Cardinality,
    CandidateType,
    FkCandidate,
    LlmDecision,
)
from .claude_cli import call_claude_json, ClaudeCliJsonParseError
from .models import ResourceEndpointMap
from .shapes import ResolvedShape
from .vocabulary import AliasMap


logger = logging.getLogger(__name__)


# Bump this whenever ``prompts/fk_resolution.md`` changes in a way
# that could change outputs, so stale caches get invalidated.
PROMPT_VERSION: str = "v1"

RESOLUTIONS_CACHE_FILENAME: str = "fk_resolutions.json"


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------


@dataclass
class FkResolution:
    """One LLM decision on one candidate.

    Cached and re-applied on subsequent runs. The ``signature`` tuple
    matches ``FkCandidate.signature`` so a cached resolution can be
    applied to a freshly-extracted candidate list by dict lookup.
    """

    source_resource: str
    source_path: tuple[str, ...]
    raw_target: str
    candidate_type: CandidateType
    decision: LlmDecision
    target_resource: str | None
    cardinality: Cardinality | None
    reason: str

    @property
    def signature(self) -> CandidateSignature:
        return (
            self.source_resource,
            tuple(self.source_path),
            self.raw_target,
            self.candidate_type.value,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_resource": self.source_resource,
            "source_path": list(self.source_path),
            "raw_target": self.raw_target,
            "candidate_type": self.candidate_type.value,
            "decision": self.decision.value,
            "target_resource": self.target_resource,
            "cardinality": (
                self.cardinality.value if self.cardinality is not None else None
            ),
            "reason": self.reason,
        }


@dataclass
class ResolutionOutcome:
    """Aggregate result of a resolution run.

    ``resolutions`` is the flat list the cache serializes. ``linked``,
    ``rejected``, and ``cardinality_only`` counts drive the CLI log
    line and the artifact meta block. ``cache_hit`` mirrors the same
    flag on ``AliasMap`` — useful for downstream tooling.
    """

    resolutions: list[FkResolution]
    linked_count: int
    rejected_count: int
    cardinality_only_count: int
    cache_hit: bool
    cache_key: str
    model: str


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def resolve_candidates(
    candidates: list[FkCandidate],
    rem: ResourceEndpointMap,
    shapes: dict[str, ResolvedShape],
    alias_map: AliasMap,
    spec: dict[str, Any],
    resources: list[str],
    model: str,
    output_dir: Path,
    *,
    use_cache: bool = True,
) -> ResolutionOutcome:
    """Run step-3 LLM disambiguation on a candidate list.

    **Mutates** ``candidates`` in place: for each candidate the LLM
    decided on, the candidate's ``llm_inferred`` / ``llm_decision`` /
    ``llm_reason`` / ``llm_model`` fields get populated, and
    (when the decision upgrades the candidate) ``target_resource``
    and ``inferred_cardinality`` get rewritten.

    The return value is a ``ResolutionOutcome`` describing what the
    LLM did — useful for logging and artifact meta. Callers that only
    care about the mutated candidate list can ignore it.

    When there's nothing to resolve (every candidate is already
    mechanically linked), this is a no-op and returns an empty
    outcome without calling the LLM or touching the cache.

    ``use_cache=False`` forces regeneration even when a matching cache
    file exists. The regenerated decisions are still written to disk.
    """
    to_resolve = [c for c in candidates if _needs_resolution(c)]
    if not to_resolve:
        return ResolutionOutcome(
            resolutions=[],
            linked_count=0,
            rejected_count=0,
            cardinality_only_count=0,
            cache_hit=False,
            cache_key="",
            model=model,
        )

    cache_key = compute_cache_key(
        to_resolve, resources, alias_map.cache_key, model, PROMPT_VERSION
    )
    cache_path = output_dir / RESOLUTIONS_CACHE_FILENAME

    if use_cache:
        cached = load_cached_resolutions(cache_path, cache_key)
        if cached is not None:
            logger.info("  [cache hit] %s", cache_path)
            return _apply_resolutions(
                candidates, cached, model=model, cache_hit=True, cache_key=cache_key
            )
    else:
        logger.info("  [cache disabled] regenerating resolutions via LLM")

    logger.info(
        "  [llm] calling %s to resolve %d candidate(s) across %d resources",
        model, len(to_resolve), len(resources),
    )

    # Build the per-candidate context the LLM will see. The list order
    # is stable (``to_resolve`` is sorted by the extractor) so the
    # ``id`` integers we hand out below match between runs.
    contexts = [
        _extract_candidate_context(c, rem, shapes, spec)
        for c in to_resolve
    ]

    llm_raw = _call_resolution_llm(
        candidates=to_resolve,
        contexts=contexts,
        resources=resources,
        alias_map=alias_map,
        model=model,
    )

    resolutions = _merge_resolutions(
        to_resolve=to_resolve, llm_raw=llm_raw, resources=resources
    )

    write_resolutions_cache(
        resolutions=resolutions,
        cache_path=cache_path,
        cache_key=cache_key,
        model=model,
        resources=resources,
    )
    logger.info("  [write] %s", cache_path)

    return _apply_resolutions(
        candidates, resolutions, model=model, cache_hit=False, cache_key=cache_key
    )


# ---------------------------------------------------------------------------
# Cache key + I/O
# ---------------------------------------------------------------------------


def compute_cache_key(
    candidates: list[FkCandidate],
    resources: list[str],
    alias_cache_key: str,
    model: str,
    prompt_version: str,
) -> str:
    """Deterministic cache key over everything the LLM call depends on.

    Every relevant input is canonicalized (sorted, typed) before
    hashing so semantically identical runs produce the same key.
    Changing ANY input — candidate list, resources, upstream alias
    map, model, prompt version — invalidates the cache.
    """
    cand_sigs = sorted(
        (
            {
                "source_resource": c.source_resource,
                "source_path": list(c.source_path),
                "raw_target": c.raw_target,
                "candidate_type": c.candidate_type.value,
                "resolution_reason": c.resolution_reason.value,
                "target_resource": c.target_resource,
                "inferred_cardinality": (
                    c.inferred_cardinality.value
                    if c.inferred_cardinality is not None
                    else None
                ),
            }
            for c in candidates
        ),
        key=lambda d: (
            d["source_resource"],
            tuple(d["source_path"]),
            d["raw_target"],
            d["candidate_type"],
        ),
    )
    payload = {
        "candidates": cand_sigs,
        "resources": sorted(resources),
        "alias_cache_key": alias_cache_key,
        "model": model,
        "prompt_version": prompt_version,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_cached_resolutions(
    cache_path: Path,
    expected_key: str,
) -> list[FkResolution] | None:
    """Load a cached resolution list if its key matches.

    Returns None on any kind of mismatch (missing file, corrupted
    JSON, key mismatch, unknown decision value). Callers re-run the
    LLM on None.
    """
    if not cache_path.exists():
        return None
    try:
        data = json.loads(cache_path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict):
        return None
    meta = data.get("_meta") or {}
    if meta.get("cache_key") != expected_key:
        return None

    raw = data.get("resolutions")
    if not isinstance(raw, list):
        return None

    out: list[FkResolution] = []
    for entry in raw:
        if not isinstance(entry, dict):
            return None
        try:
            decision = LlmDecision(entry["decision"])
            candidate_type = CandidateType(entry["candidate_type"])
        except (KeyError, ValueError):
            return None
        card_raw = entry.get("cardinality")
        cardinality: Cardinality | None = None
        if card_raw is not None:
            try:
                cardinality = Cardinality(card_raw)
            except ValueError:
                return None
        out.append(
            FkResolution(
                source_resource=str(entry.get("source_resource", "")),
                source_path=tuple(entry.get("source_path") or []),
                raw_target=str(entry.get("raw_target", "")),
                candidate_type=candidate_type,
                decision=decision,
                target_resource=entry.get("target_resource"),
                cardinality=cardinality,
                reason=str(entry.get("reason", "")),
            )
        )
    return out


def write_resolutions_cache(
    resolutions: list[FkResolution],
    cache_path: Path,
    cache_key: str,
    model: str,
    resources: list[str],
) -> None:
    """Serialize the resolution list to the cache file."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    linked = sum(1 for r in resolutions if r.decision == LlmDecision.LINKED)
    rejected = sum(1 for r in resolutions if r.decision == LlmDecision.REJECTED)
    card_only = sum(
        1 for r in resolutions if r.decision == LlmDecision.CARDINALITY_ONLY
    )
    payload: dict[str, Any] = {
        "_meta": {
            "cache_key": cache_key,
            "model": model,
            "prompt_version": PROMPT_VERSION,
            "resource_count": len(resources),
            "resolution_count": len(resolutions),
            "linked_count": linked,
            "rejected_count": rejected,
            "cardinality_only_count": card_only,
        },
        "resolutions": [
            r.to_dict()
            for r in sorted(
                resolutions,
                key=lambda r: (
                    r.source_resource,
                    tuple(r.source_path),
                    r.raw_target,
                    r.candidate_type.value,
                ),
            )
        ],
    }
    cache_path.write_text(json.dumps(payload, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Candidate selection + context extraction
# ---------------------------------------------------------------------------


def _needs_resolution(candidate: FkCandidate) -> bool:
    """True iff step 3 should touch this candidate.

    Two cases:

      * ``needs_llm=True`` — the walker flagged it as ambiguous. This
        covers unresolved candidates AND self-references the walker
        downgraded to weak.
      * ``target_resource`` set but ``inferred_cardinality`` is None —
        we know where it points, we just don't know the relationship
        type. Forward-compatible with proposal types that don't carry
        shape information.
    """
    return candidate.needs_llm or (
        candidate.target_resource is not None
        and candidate.inferred_cardinality is None
    )


def _extract_candidate_context(
    candidate: FkCandidate,
    rem: ResourceEndpointMap,
    shapes: dict[str, ResolvedShape],
    spec: dict[str, Any],
) -> dict[str, Any]:
    """Build the per-candidate JSON context shown to the LLM.

    Per the design: each candidate gets enough raw schema text to let
    the LLM make an informed decision, but not the whole OpenAPI spec
    (which would blow the context window and dilute the signal).

    For schema-walk candidates we pull the owning schema's property
    definition and — if the candidate is a NESTED_REF / ARRAY_OF_REFS
    — also the target component schema's top-level property list.

    For endpoint-param candidates we pull the matching parameter
    object from the endpoint's raw operation.

    Missing context is tolerated: if we can't locate the schema
    fragment the LLM still sees the evidence string and the walker's
    classification, which is often enough.
    """
    ctx: dict[str, Any] = {
        "source_resource": candidate.source_resource,
        "source_path": list(candidate.source_path),
        "raw_target": candidate.raw_target,
        "candidate_type": candidate.candidate_type.value,
        "resolution_reason": candidate.resolution_reason.value,
        "current_target_resource": candidate.target_resource,
        "current_cardinality": (
            candidate.inferred_cardinality.value
            if candidate.inferred_cardinality is not None
            else None
        ),
        "evidence": candidate.evidence,
    }

    fragment = _find_schema_fragment(candidate, rem, shapes, spec)
    if fragment is not None:
        ctx["schema_fragment"] = fragment

    return ctx


def _find_schema_fragment(
    candidate: FkCandidate,
    rem: ResourceEndpointMap,
    shapes: dict[str, ResolvedShape],
    spec: dict[str, Any],
) -> dict[str, Any] | None:
    """Locate the minimal OpenAPI fragment describing this candidate.

    Dispatches on how the candidate was extracted: parameter lifts
    carry the endpoint key in ``source_path[0]`` (recognizable by the
    " " in "METHOD /path"); everything else came from the schema walk.
    Returns a small dict or None when no fragment was found.
    """
    if _looks_like_endpoint_param(candidate, rem):
        return _fragment_for_endpoint_param(candidate, rem)
    return _fragment_for_schema_property(candidate, shapes, spec)


def _looks_like_endpoint_param(
    candidate: FkCandidate,
    rem: ResourceEndpointMap,
) -> bool:
    """True when source_path is ``(endpoint_key, "path.NAME")``."""
    return (
        len(candidate.source_path) >= 2
        and " " in candidate.source_path[0]
        and candidate.source_path[0] in rem.endpoints
    )


def _fragment_for_endpoint_param(
    candidate: FkCandidate,
    rem: ResourceEndpointMap,
) -> dict[str, Any] | None:
    endpoint_key = candidate.source_path[0]
    loc, _, name = candidate.source_path[1].partition(".")
    params = rem.endpoints[endpoint_key].raw_operation.get("parameters") or []
    if not isinstance(params, list):
        return None
    for param in params:
        if (
            isinstance(param, dict)
            and param.get("name") == name
            and param.get("in") == loc
        ):
            return {
                "kind": "endpoint_parameter",
                "endpoint": endpoint_key,
                "parameter": _compact_param(param),
            }
    return None


def _fragment_for_schema_property(
    candidate: FkCandidate,
    shapes: dict[str, ResolvedShape],
    spec: dict[str, Any],
) -> dict[str, Any] | None:
    """Build the schema-walk fragment: owning property + (optional) target schema."""
    fragment: dict[str, Any] = {"kind": "schema_property"}

    shape = shapes.get(candidate.source_resource)
    prop_name = candidate.source_path[-1] if candidate.source_path else None
    if shape is not None and prop_name and prop_name in shape.properties:
        fragment["owning_schema"] = (
            shape.origin_schema_name or candidate.source_resource
        )
        fragment["property_name"] = prop_name
        fragment["property_schema"] = _compact_schema(shape.properties[prop_name])

    if candidate.candidate_type in (
        CandidateType.NESTED_REF,
        CandidateType.ARRAY_OF_REFS,
    ):
        target = _lookup_component_schema(candidate.raw_target, spec)
        if target is not None:
            name, target_schema = target
            props = target_schema.get("properties")
            fragment["target_schema_name"] = name
            fragment["target_schema_property_names"] = (
                sorted(props.keys()) if isinstance(props, dict) else []
            )

    if "property_schema" not in fragment and "target_schema_name" not in fragment:
        return None
    return fragment


def _compact_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Squeeze a schema dict down to the keys the LLM cares about.

    We deliberately drop large / noisy OpenAPI keys (``example``,
    ``examples``, ``x-*`` extensions, long ``description`` text) to
    keep the prompt lean. Everything structurally meaningful is kept.
    """
    if not isinstance(schema, dict):
        return {}
    keep_keys = (
        "$ref", "type", "format", "enum", "nullable",
        "items", "properties", "anyOf", "oneOf", "allOf",
        "additionalProperties",
    )
    out: dict[str, Any] = {}
    for key in keep_keys:
        if key in schema:
            out[key] = schema[key]
    # Keep description only if it's short — role hints are useful,
    # novels are not.
    desc = schema.get("description")
    if isinstance(desc, str) and 0 < len(desc) <= 200:
        out["description"] = desc
    return out


def _compact_param(param: dict[str, Any]) -> dict[str, Any]:
    """Param-object projection for the prompt context."""
    out: dict[str, Any] = {
        "name": param.get("name"),
        "in": param.get("in"),
    }
    if "required" in param:
        out["required"] = param["required"]
    schema = param.get("schema")
    if isinstance(schema, dict):
        out["schema"] = _compact_schema(schema)
    desc = param.get("description")
    if isinstance(desc, str) and 0 < len(desc) <= 200:
        out["description"] = desc
    return out


def _lookup_component_schema(
    schema_name: str,
    spec: dict[str, Any],
) -> tuple[str, dict[str, Any]] | None:
    """Return (name, schema) for a component schema by case-insensitive name."""
    schemas = (spec.get("components") or {}).get("schemas") or {}
    if not isinstance(schemas, dict):
        return None
    if schema_name in schemas and isinstance(schemas[schema_name], dict):
        return schema_name, schemas[schema_name]
    # Case-insensitive fallback.
    lowered = schema_name.lower()
    for name, schema in schemas.items():
        if isinstance(name, str) and name.lower() == lowered and isinstance(schema, dict):
            return name, schema
    return None


# ---------------------------------------------------------------------------
# LLM call + merge
# ---------------------------------------------------------------------------


def _call_resolution_llm(
    candidates: list[FkCandidate],
    contexts: list[dict[str, Any]],
    resources: list[str],
    alias_map: AliasMap,
    model: str,
) -> list[dict[str, Any]]:
    """Render the prompt, call the CLI, and return the raw resolution list.

    Each candidate context gets an integer ``id`` that the LLM must
    echo back. We then map the returned id → candidate in the merge
    step. Candidates the LLM fails to return are treated as
    unresolved (they stay in the candidate list with ``llm_inferred``
    unset).
    """
    prompt_template = _load_prompt_template()

    numbered = [
        {"id": idx, **ctx}
        for idx, ctx in enumerate(contexts)
    ]

    aliases_view: dict[str, list[str]] = {}
    for canonical in resources:
        entry = alias_map.entries.get(canonical)
        if entry is None:
            aliases_view[canonical] = []
            continue
        aliases_view[canonical] = sorted(set(
            [entry.singular] + list(entry.syntactic_aliases)
        ))

    prompt = (
        prompt_template
        .replace(
            "{CANONICAL_RESOURCES_JSON}",
            json.dumps(resources, indent=2),
        )
        .replace(
            "{RESOURCE_ALIASES_JSON}",
            json.dumps(aliases_view, indent=2),
        )
        .replace(
            "{CANDIDATES_JSON}",
            json.dumps(numbered, indent=2),
        )
    )

    try:
        response = call_claude_json(prompt, model=model, max_retries=1)
    except ClaudeCliJsonParseError as e:
        raise RuntimeError(
            "LLM FK resolution failed: claude returned unparseable JSON "
            f"after retry.\nRaw response head:\n{(e.stdout or '')[:800]}"
        ) from e

    if not isinstance(response, dict):
        raise RuntimeError(
            f"LLM FK resolution response is not a JSON object: "
            f"{type(response).__name__}"
        )

    raw = response.get("resolutions")
    if not isinstance(raw, list):
        raise RuntimeError(
            f"LLM FK resolution response.resolutions is not a list: "
            f"{type(raw).__name__}"
        )
    return raw


def _merge_resolutions(
    to_resolve: list[FkCandidate],
    llm_raw: list[dict[str, Any]],
    resources: list[str],
) -> list[FkResolution]:
    """Validate the LLM output and turn it into ``FkResolution`` objects.

    Each LLM entry is parsed inline (id / decision / cardinality /
    reason) and then dispatched to a per-decision validator. Malformed
    entries are silently dropped; candidates the LLM omits remain
    mechanically unresolved in the final artifact.
    """
    resource_set = set(resources)
    out: list[FkResolution] = []
    seen_ids: set[int] = set()

    for entry in llm_raw:
        if not isinstance(entry, dict):
            continue

        raw_id = entry.get("id")
        if not isinstance(raw_id, int) or not (0 <= raw_id < len(to_resolve)):
            continue
        if raw_id in seen_ids:
            continue
        seen_ids.add(raw_id)
        candidate = to_resolve[raw_id]

        decision_raw = entry.get("decision")
        if not isinstance(decision_raw, str):
            continue
        try:
            decision = LlmDecision(decision_raw.upper())
        except ValueError:
            continue

        cardinality: Cardinality | None = None
        card_raw = entry.get("cardinality")
        if isinstance(card_raw, str):
            try:
                cardinality = Cardinality(card_raw.upper())
            except ValueError:
                cardinality = None

        reason = entry.get("reason")
        if not isinstance(reason, str):
            reason = ""

        if decision == LlmDecision.LINKED:
            out.append(_validate_linked(
                candidate, entry.get("target_resource"),
                cardinality, reason, resource_set,
            ))
        elif decision == LlmDecision.CARDINALITY_ONLY:
            resolution = _validate_cardinality_only(candidate, cardinality, reason)
            if resolution is not None:
                out.append(resolution)
        else:
            out.append(_build_resolution(
                candidate, LlmDecision.REJECTED,
                target=None, cardinality=None, reason=reason,
            ))

    return out


def _build_resolution(
    candidate: FkCandidate,
    decision: LlmDecision,
    *,
    target: str | None,
    cardinality: Cardinality | None,
    reason: str,
) -> FkResolution:
    """Construct an ``FkResolution`` that carries the candidate's signature."""
    return FkResolution(
        source_resource=candidate.source_resource,
        source_path=tuple(candidate.source_path),
        raw_target=candidate.raw_target,
        candidate_type=candidate.candidate_type,
        decision=decision,
        target_resource=target,
        cardinality=cardinality,
        reason=reason,
    )


def _validate_linked(
    candidate: FkCandidate,
    target: Any,
    cardinality: Cardinality | None,
    reason: str,
    resource_set: set[str],
) -> FkResolution:
    """Enforce the closed-world rule on a ``linked`` decision.

    Out-of-scope targets are downgraded to rejected with an audit
    trail. Missing cardinality defaults to ONE_TO_MANY since we know
    the target is valid.
    """
    if not isinstance(target, str) or target not in resource_set:
        return _build_resolution(
            candidate, LlmDecision.REJECTED,
            target=None, cardinality=None,
            reason=(
                f"LLM proposed out-of-scope target {target!r}; "
                f"downgraded to rejected. Original reason: {reason}"
            ),
        )
    return _build_resolution(
        candidate, LlmDecision.LINKED,
        target=target,
        cardinality=cardinality or Cardinality.ONE_TO_MANY,
        reason=reason,
    )


def _validate_cardinality_only(
    candidate: FkCandidate,
    cardinality: Cardinality | None,
    reason: str,
) -> FkResolution | None:
    """``cardinality_only`` requires a cardinality; without one we drop it.

    The target is taken from the candidate (the walker set it); the
    LLM only fills in the relationship type.
    """
    if cardinality is None:
        return None
    return _build_resolution(
        candidate, LlmDecision.CARDINALITY_ONLY,
        target=candidate.target_resource,
        cardinality=cardinality,
        reason=reason,
    )


def _apply_resolutions(
    candidates: list[FkCandidate],
    resolutions: list[FkResolution],
    *,
    model: str,
    cache_hit: bool,
    cache_key: str,
) -> ResolutionOutcome:
    """Mutate ``candidates`` in place, applying each resolution by signature.

    Unmatched candidates are left untouched; unmatched resolutions
    (stale cache entries) are silently discarded — the cache will be
    rewritten on the next run that produces new decisions.
    """
    by_sig: dict[CandidateSignature, FkResolution] = {
        r.signature: r for r in resolutions
    }
    linked = 0
    rejected = 0
    card_only = 0

    for candidate in candidates:
        resolution = by_sig.get(candidate.signature)
        if resolution is None:
            continue

        candidate.llm_inferred = True
        candidate.llm_decision = resolution.decision
        candidate.llm_reason = resolution.reason
        candidate.llm_model = model
        candidate.needs_llm = False

        if resolution.decision == LlmDecision.LINKED:
            candidate.target_resource = resolution.target_resource
            candidate.inferred_cardinality = resolution.cardinality
            linked += 1
        elif resolution.decision == LlmDecision.CARDINALITY_ONLY:
            candidate.inferred_cardinality = resolution.cardinality
            card_only += 1
        else:
            # REJECTED: clear target and cardinality so downstream
            # treats it as "don't use", but keep needs_llm=False so
            # the writer routes it into the rejected bucket.
            candidate.target_resource = None
            candidate.inferred_cardinality = None
            rejected += 1

    return ResolutionOutcome(
        resolutions=resolutions,
        linked_count=linked,
        rejected_count=rejected,
        cardinality_only_count=card_only,
        cache_hit=cache_hit,
        cache_key=cache_key,
        model=model,
    )


def _load_prompt_template() -> str:
    """Read the versioned prompt template from disk."""
    return load_prompt_template("fk_resolution.md")
