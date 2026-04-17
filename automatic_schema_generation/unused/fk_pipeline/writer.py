"""Serializer — turns a ``ResourceEndpointMap`` into the JSON artifact.

The on-disk shape is the contract downstream steps depend on, so this
module is deliberately boring: no logic, just deterministic
serialization with stable ordering.

Artifact layout:

    {
      "_meta": { ... },
      "resource_aliases": { canonical: [alias, ...] },
      "resources": { canonical: [ {edge}, ... ] },
      "endpoints": { "METHOD /path": { ...EndpointRecord } },
      "unbucketed_endpoints": [ { ...EndpointRecord } ]
    }

``resources`` and ``endpoints`` are two views of the same edge set
(see ``models.py``) — downstream code can read whichever shape is
more convenient and they'll always agree.

Stable ordering rules:
  * Resources listed in the order the user declared them in config,
    then anything else alphabetically. This keeps diffs stable across
    runs when a spec's schema set churns but the user's resource list
    is the same.
  * Edges within a resource sorted by (role_strength, endpoint_key) —
    the strongest relationships surface first, which is what an
    operator reading the file wants to see.
  * Endpoints sorted by key ("METHOD /path"); parameters within each
    operation preserved verbatim since they come from the spec.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .candidates import FkCandidate, LlmDecision
from .models import Edge, EndpointRecord, ResourceEndpointMap, _ROLE_STRENGTH


ARTIFACT_FILENAME: str = "resource_endpoint_map.json"


@dataclass
class ArtifactMeta:
    """Metadata block written to the top of the artifact.

    Captures the inputs that produced this map so a stale artifact
    can be detected and re-run without guesswork.
    """

    app_slug: str
    source_spec: str
    model: str
    prompt_version: str
    user_resource_count: int
    endpoint_count: int
    edge_count: int
    unbucketed_count: int
    vocabulary_cache_hit: bool
    # Step-2 counts (zero when the extractor hasn't run yet).
    fk_candidate_count: int = 0
    fk_linked_count: int = 0
    fk_unresolved_count: int = 0
    # Step-3 counts (zero when the resolution step hasn't run).
    # ``fk_rejected_count`` is candidates the LLM reviewed and decided
    # are not actually FKs; they survive in the artifact in a separate
    # bucket for audit. ``fk_llm_linked_count`` is how many originally
    # unresolved candidates the LLM upgraded to linked.
    fk_rejected_count: int = 0
    fk_llm_linked_count: int = 0


def write_artifact(
    rem: ResourceEndpointMap,
    output_path: Path,
    meta: ArtifactMeta,
    resource_order: list[str],
    fk_candidates: list[FkCandidate] | None = None,
) -> None:
    """Serialize a ResourceEndpointMap (+ FK candidates) to disk.

    ``resource_order`` is the user-declared resource list; resources
    appear in that order in the output. Any canonicals present in
    ``rem`` but not in ``resource_order`` are appended alphabetically
    at the end (defensive — this shouldn't happen in practice since
    the alias map is built from the user's list).

    ``fk_candidates`` is the flat list produced by ``extractor``. When
    ``None`` (step-1-only runs), the ``fk_candidates`` section is
    omitted entirely — downstream code treats absence and empty list
    as distinct signals ("extractor wasn't run" vs "extractor found
    nothing to record").
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build the resources view with stable ordering.
    resources_view = rem.resources_view()
    ordered_resources: dict[str, list[dict[str, Any]]] = {}
    for canonical in resource_order:
        if canonical in resources_view:
            ordered_resources[canonical] = [
                _edge_to_view_dict(e)
                for e in _sort_edges(resources_view[canonical])
            ]
    # Any strays (shouldn't happen, but we preserve them rather than drop)
    for canonical in sorted(resources_view):
        if canonical not in ordered_resources:
            ordered_resources[canonical] = [
                _edge_to_view_dict(e)
                for e in _sort_edges(resources_view[canonical])
            ]

    # Endpoints view — sort by key, attach edges in strength order.
    endpoints_view: dict[str, dict[str, Any]] = {}
    for key in sorted(rem.endpoints):
        record = rem.endpoints[key]
        endpoints_view[key] = _endpoint_to_dict(record, sort_edges=True)

    unbucketed_view = [
        _endpoint_to_dict(r, sort_edges=False)
        for r in sorted(rem.unbucketed_endpoints, key=lambda r: r.key)
    ]

    # Resource aliases view — preserve declared order, canonical lists sorted.
    aliases_view: dict[str, list[str]] = {}
    for canonical in resource_order:
        if canonical in rem.resource_aliases:
            aliases_view[canonical] = sorted(set(rem.resource_aliases[canonical]))
    for canonical in sorted(rem.resource_aliases):
        if canonical not in aliases_view:
            aliases_view[canonical] = sorted(set(rem.resource_aliases[canonical]))

    meta_block: dict[str, Any] = {
        "app_slug": meta.app_slug,
        "source_spec": meta.source_spec,
        "model": meta.model,
        "prompt_version": meta.prompt_version,
        "user_resource_count": meta.user_resource_count,
        "endpoint_count": meta.endpoint_count,
        "edge_count": meta.edge_count,
        "unbucketed_count": meta.unbucketed_count,
        "vocabulary_cache_hit": meta.vocabulary_cache_hit,
    }
    if fk_candidates is not None:
        meta_block["fk_candidate_count"] = meta.fk_candidate_count
        meta_block["fk_linked_count"] = meta.fk_linked_count
        meta_block["fk_unresolved_count"] = meta.fk_unresolved_count
        # Step-3 counts are only meaningful when the resolution step
        # actually ran. We still write them unconditionally here
        # (they default to 0) so downstream consumers don't have to
        # special-case "resolution didn't run yet" vs "resolution ran
        # and found nothing".
        meta_block["fk_rejected_count"] = meta.fk_rejected_count
        meta_block["fk_llm_linked_count"] = meta.fk_llm_linked_count

    payload: dict[str, Any] = {
        "_meta": meta_block,
        "resource_aliases": aliases_view,
        "resources": ordered_resources,
        "endpoints": endpoints_view,
        "unbucketed_endpoints": unbucketed_view,
    }
    if fk_candidates is not None:
        payload["fk_candidates"] = _fk_candidates_view(
            fk_candidates, resource_order
        )

    output_path.write_text(json.dumps(payload, indent=2) + "\n")


def _sort_edges(edges: list[Edge]) -> list[Edge]:
    """Sort edges by (role_strength, endpoint_key).

    Strongest first within a resource is the natural reading order —
    owner edges before parents before query/body references. Ties
    broken by endpoint key for determinism.
    """
    return sorted(
        edges,
        key=lambda e: (_ROLE_STRENGTH[e.role], e.endpoint_key),
    )


def _fk_candidates_view(
    candidates: list[FkCandidate],
    resource_order: list[str],
) -> dict[str, Any]:
    """Group FK candidates by source resource with a three-way bucket split.

    Output layout:

        {
          "<resource>": {
            "linked":     [ {candidate}, ... ],
            "unresolved": [ {candidate}, ... ],
            "rejected":   [ {candidate}, ... ],
          },
          ...
        }

    Routing rules:
      * ``rejected`` — candidates the LLM (step 3) examined and
        decided are not actually FKs. Kept for audit. Empty when
        step 3 hasn't run.
      * ``linked`` — everything else with ``needs_llm=False``.
        Includes both walker-linked candidates (``llm_inferred=False``)
        and LLM-upgraded candidates (``llm_inferred=True``,
        ``llm_decision=LINKED``). The ``llm_inferred`` field on each
        entry lets consumers distinguish the two provenance classes.
      * ``unresolved`` — everything the walker couldn't resolve AND
        the LLM either hasn't seen yet or couldn't decide on.

    Resources appear in ``resource_order``; any candidates whose
    source resource is outside that list (shouldn't happen, but we
    don't drop data silently) appear after, sorted alphabetically.
    """
    by_resource: dict[str, dict[str, list[dict[str, Any]]]] = {}

    for cand in candidates:
        bucket = by_resource.setdefault(
            cand.source_resource,
            {"linked": [], "unresolved": [], "rejected": []},
        )
        if cand.llm_inferred and cand.llm_decision == LlmDecision.REJECTED:
            key = "rejected"
        elif cand.needs_llm:
            key = "unresolved"
        else:
            key = "linked"
        bucket[key].append(cand.to_dict())

    # Stable ordering within each bucket: already ordered by the
    # extractor's sort, so just re-sort defensively on the view key
    # so the output is self-consistent even if callers pass an
    # unsorted list.
    def _sort_key(entry: dict[str, Any]) -> tuple[Any, ...]:
        return (
            tuple(entry.get("source_path") or []),
            entry.get("raw_target") or "",
            entry.get("candidate_type") or "",
        )

    def _materialize(bucket: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
        return {
            "linked": sorted(bucket["linked"], key=_sort_key),
            "unresolved": sorted(bucket["unresolved"], key=_sort_key),
            "rejected": sorted(bucket["rejected"], key=_sort_key),
        }

    ordered: dict[str, Any] = {}
    for resource in resource_order:
        if resource not in by_resource:
            continue
        ordered[resource] = _materialize(by_resource[resource])
    for resource in sorted(by_resource):
        if resource in ordered:
            continue
        ordered[resource] = _materialize(by_resource[resource])
    return ordered


def _edge_to_view_dict(edge: Edge) -> dict[str, Any]:
    """Resources-view shape — no resource field (it's the outer key)."""
    return {
        "endpoint": edge.endpoint_key,
        "role": edge.role.value,
        "evidence": edge.evidence,
    }


def _endpoint_to_dict(
    record: EndpointRecord,
    *,
    sort_edges: bool,
) -> dict[str, Any]:
    """Endpoints-view shape — full operation + attached edges.

    ``raw_operation`` is preserved verbatim so downstream steps can
    walk schemas without re-parsing the spec. For unbucketed endpoints
    this is load-bearing: triage tooling reads the operation summary
    and parameters to decide whether to add a resource or extend the
    naming config.
    """
    edges = record.resource_edges
    if sort_edges:
        edges = _sort_edges(edges)
    return {
        "method": record.method,
        "path": record.path,
        "operation_id": record.operation_id,
        "resource_edges": [
            {
                "resource": e.resource,
                "role": e.role.value,
                "evidence": e.evidence,
            }
            for e in edges
        ],
        "raw_operation": record.raw_operation,
    }
