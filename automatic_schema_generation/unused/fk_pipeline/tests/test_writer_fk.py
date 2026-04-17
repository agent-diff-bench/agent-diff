"""Writer tests for the fk_candidates section.

These complement test_writer.py — they only assert the new surface
(the ``fk_candidates`` block and the new meta counts). The existing
resources/endpoints/unbucketed assertions live in test_writer.py and
should continue to hold when fk_candidates is absent.
"""

from __future__ import annotations

import json
from pathlib import Path

from fk_pipeline.bucketing import build_map
from fk_pipeline.candidates import (
    Cardinality,
    CandidateType,
    Confidence,
    FkCandidate,
    ResolutionReason,
)
from fk_pipeline.extractor import extract_candidates
from fk_pipeline.shapes import resolve_shapes
from fk_pipeline.writer import ARTIFACT_FILENAME, ArtifactMeta, write_artifact

from .conftest import make_alias_map, make_op, make_spec


def _write_and_read(tmp_path: Path, naming, spec, resource_aliases,
                    with_candidates: bool):
    alias_map = make_alias_map(resource_aliases)
    rem = build_map(spec, alias_map, naming)
    candidates = None
    if with_candidates:
        shapes = resolve_shapes(rem, spec, alias_map)
        candidates = extract_candidates(
            rem=rem, shapes=shapes, alias_map=alias_map,
            naming=naming, spec=spec,
        )
    out_path = tmp_path / ARTIFACT_FILENAME
    meta = ArtifactMeta(
        app_slug="test",
        source_spec="/nowhere",
        model="claude-haiku-4-5",
        prompt_version="v1",
        user_resource_count=len(resource_aliases),
        endpoint_count=len(rem.endpoints),
        edge_count=len(rem.edges),
        unbucketed_count=len(rem.unbucketed_endpoints),
        vocabulary_cache_hit=False,
        fk_candidate_count=len(candidates) if candidates is not None else 0,
        fk_linked_count=(
            sum(1 for c in candidates if not c.needs_llm)
            if candidates is not None else 0
        ),
        fk_unresolved_count=(
            sum(1 for c in candidates if c.needs_llm)
            if candidates is not None else 0
        ),
    )
    write_artifact(
        rem=rem,
        output_path=out_path,
        meta=meta,
        resource_order=list(resource_aliases.keys()),
        fk_candidates=candidates,
    )
    return json.loads(out_path.read_text())


def test_artifact_without_candidates_omits_section(tmp_path: Path, default_naming):
    """When ``fk_candidates=None`` the section is absent from the JSON."""
    spec = make_spec({"/projects": {"get": make_op()}})
    data = _write_and_read(
        tmp_path, default_naming, spec, {"projects": []}, with_candidates=False
    )
    assert "fk_candidates" not in data
    # And the step-2 meta counts are absent too.
    meta = data["_meta"]
    assert "fk_candidate_count" not in meta


def test_artifact_with_candidates_has_linked_and_unresolved(
    tmp_path: Path, default_naming
):
    """Linked vs unresolved split renders correctly and meta counts match."""
    spec = make_spec(
        {
            "/projects/{id}": {
                "get": make_op(
                    operation_id="get_project",
                    path_params=["id"],
                    response_schema_ref="#/components/schemas/Project",
                )
            }
        },
        schemas={
            "Project": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "owner_id": {"type": "integer"},       # linked → users
                    "reviewer_id": {"type": "integer"},    # unresolved
                },
            }
        },
    )
    data = _write_and_read(
        tmp_path, default_naming, spec,
        {"projects": [], "users": ["owner"]}, with_candidates=True,
    )
    assert "fk_candidates" in data
    projects = data["fk_candidates"]["projects"]
    assert "linked" in projects
    assert "unresolved" in projects
    linked_targets = {c["raw_target"] for c in projects["linked"]}
    unresolved_targets = {c["raw_target"] for c in projects["unresolved"]}
    assert "owner" in linked_targets
    assert "reviewer" in unresolved_targets
    # Meta counts add up.
    meta = data["_meta"]
    assert meta["fk_candidate_count"] == meta["fk_linked_count"] + meta["fk_unresolved_count"]
    assert meta["fk_linked_count"] >= 1
    assert meta["fk_unresolved_count"] >= 1


def test_fk_candidates_sorted_deterministically(tmp_path: Path, default_naming):
    """Within each bucket, candidates come out in stable order."""
    # Hand-craft a candidate list with intentionally scrambled order
    # so the writer's own sort is the thing being tested.
    candidates = [
        FkCandidate(
            source_resource="projects",
            source_path=("Project", "z_last_id"),
            raw_target="z_last",
            candidate_type=CandidateType.SCALAR_ID,
            resolution_reason=ResolutionReason.UNRESOLVED,
            target_resource=None,
            inferred_cardinality=None,
            confidence=Confidence.WEAK,
            needs_llm=True,
            evidence="",
        ),
        FkCandidate(
            source_resource="projects",
            source_path=("Project", "a_first_id"),
            raw_target="a_first",
            candidate_type=CandidateType.SCALAR_ID,
            resolution_reason=ResolutionReason.UNRESOLVED,
            target_resource=None,
            inferred_cardinality=None,
            confidence=Confidence.WEAK,
            needs_llm=True,
            evidence="",
        ),
    ]
    spec = make_spec({"/projects": {"get": make_op()}})
    alias_map = make_alias_map({"projects": []})
    rem = build_map(spec, alias_map, default_naming)
    out_path = tmp_path / ARTIFACT_FILENAME
    meta = ArtifactMeta(
        app_slug="t", source_spec="/n", model="m", prompt_version="v1",
        user_resource_count=1, endpoint_count=len(rem.endpoints),
        edge_count=len(rem.edges), unbucketed_count=len(rem.unbucketed_endpoints),
        vocabulary_cache_hit=False,
        fk_candidate_count=2, fk_linked_count=0, fk_unresolved_count=2,
    )
    write_artifact(
        rem=rem, output_path=out_path, meta=meta,
        resource_order=["projects"], fk_candidates=candidates,
    )
    data = json.loads(out_path.read_text())
    unresolved = data["fk_candidates"]["projects"]["unresolved"]
    # Sorted by source_path → a_first before z_last.
    assert unresolved[0]["raw_target"] == "a_first"
    assert unresolved[1]["raw_target"] == "z_last"
