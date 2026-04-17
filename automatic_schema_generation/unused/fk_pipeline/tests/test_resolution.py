"""LLM resolution (step 3) tests.

No real LLM calls — the ``_call_resolution_llm`` transport is
stubbed via monkeypatching. These tests cover the pure pieces:

  * Cache key determinism / sensitivity.
  * ``_needs_resolution`` selection rules.
  * Merge validation (closed-world target check, missing cardinality
    defaulting, invalid decisions).
  * In-place mutation of candidates after apply.
  * Cache roundtrip (write → load with matching key).
  * Integration with a fake LLM: a full run end-to-end with a stubbed
    response, verifying the writer's rejected/linked/unresolved split.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fk_pipeline.bucketing import build_map
from fk_pipeline.candidates import (
    Cardinality,
    CandidateType,
    Confidence,
    FkCandidate,
    LlmDecision,
    ResolutionReason,
)
from fk_pipeline.extractor import extract_candidates
from fk_pipeline.resolution import (
    FkResolution,
    PROMPT_VERSION,
    RESOLUTIONS_CACHE_FILENAME,
    _apply_resolutions,
    _merge_resolutions,
    _needs_resolution,
    compute_cache_key,
    load_cached_resolutions,
    resolve_candidates,
    write_resolutions_cache,
)
from fk_pipeline.shapes import resolve_shapes
from fk_pipeline.writer import ARTIFACT_FILENAME, ArtifactMeta, write_artifact

from .conftest import make_alias_map, make_op, make_spec


# ---------------------------------------------------------------------------
# Small builders shared by most tests
# ---------------------------------------------------------------------------


def _make_unresolved(
    source: str,
    raw_target: str,
    *,
    path: tuple[str, ...] | None = None,
    ctype: CandidateType = CandidateType.SCALAR_ID,
) -> FkCandidate:
    """Build a walker-unresolved candidate for merge/apply tests."""
    return FkCandidate(
        source_resource=source,
        source_path=path or (source.capitalize(), f"{raw_target}_id"),
        raw_target=raw_target,
        candidate_type=ctype,
        resolution_reason=ResolutionReason.UNRESOLVED,
        target_resource=None,
        inferred_cardinality=None,
        confidence=Confidence.WEAK,
        needs_llm=True,
        evidence=f"field '{raw_target}_id' unresolved",
    )


def _make_linked(source: str, target: str, raw_target: str) -> FkCandidate:
    """Walker-linked candidate (no LLM needed)."""
    return FkCandidate(
        source_resource=source,
        source_path=(source.capitalize(), f"{raw_target}_id"),
        raw_target=raw_target,
        candidate_type=CandidateType.SCALAR_ID,
        resolution_reason=ResolutionReason.SUFFIX_STRIP,
        target_resource=target,
        inferred_cardinality=Cardinality.ONE_TO_MANY,
        confidence=Confidence.STRONG,
        needs_llm=False,
        evidence=f"field '{raw_target}_id' → {target}",
    )


# ---------------------------------------------------------------------------
# Selection rules
# ---------------------------------------------------------------------------


def test_needs_resolution_only_for_unresolved_or_cardinality_hole():
    """Walker-linked candidates are skipped; unresolved are picked up."""
    linked = _make_linked("projects", "users", "owner")
    unresolved = _make_unresolved("projects", "assignee")
    cardinality_hole = FkCandidate(
        source_resource="projects",
        source_path=("Project", "owner_id"),
        raw_target="owner",
        candidate_type=CandidateType.SCALAR_ID,
        resolution_reason=ResolutionReason.SUFFIX_STRIP,
        target_resource="users",
        inferred_cardinality=None,  # the hole
        confidence=Confidence.STRONG,
        needs_llm=False,
        evidence="...",
    )
    assert _needs_resolution(linked) is False
    assert _needs_resolution(unresolved) is True
    assert _needs_resolution(cardinality_hole) is True


# ---------------------------------------------------------------------------
# Cache key
# ---------------------------------------------------------------------------


def test_cache_key_is_order_independent():
    a = _make_unresolved("projects", "assignee")
    b = _make_unresolved("projects", "reviewer")
    key_ab = compute_cache_key([a, b], ["projects", "users"], "alias-k1",
                               "claude-sonnet-4-5", PROMPT_VERSION)
    key_ba = compute_cache_key([b, a], ["users", "projects"], "alias-k1",
                               "claude-sonnet-4-5", PROMPT_VERSION)
    assert key_ab == key_ba


def test_cache_key_changes_on_any_input():
    a = _make_unresolved("projects", "assignee")
    base = compute_cache_key([a], ["projects", "users"], "alias-k1",
                             "claude-sonnet-4-5", "v1")
    # Different candidate
    assert base != compute_cache_key(
        [_make_unresolved("projects", "reviewer")],
        ["projects", "users"], "alias-k1", "claude-sonnet-4-5", "v1",
    )
    # Different resources
    assert base != compute_cache_key(
        [a], ["projects"], "alias-k1", "claude-sonnet-4-5", "v1",
    )
    # Different alias map key (upstream invalidation)
    assert base != compute_cache_key(
        [a], ["projects", "users"], "alias-k2", "claude-sonnet-4-5", "v1",
    )
    # Different model
    assert base != compute_cache_key(
        [a], ["projects", "users"], "alias-k1", "claude-opus-4-6", "v1",
    )
    # Different prompt version
    assert base != compute_cache_key(
        [a], ["projects", "users"], "alias-k1", "claude-sonnet-4-5", "v2",
    )


# ---------------------------------------------------------------------------
# Merge validation
# ---------------------------------------------------------------------------


def test_merge_linked_target_out_of_scope_becomes_rejected():
    """LLM invents a target → we downgrade to rejected with audit trail."""
    cand = _make_unresolved("projects", "widget")
    llm_raw = [{
        "id": 0, "decision": "linked", "target_resource": "widgets",
        "cardinality": "ONE_TO_MANY", "reason": "widget points at a widget",
    }]
    resolutions = _merge_resolutions(
        to_resolve=[cand], llm_raw=llm_raw, resources=["projects", "users"]
    )
    assert len(resolutions) == 1
    r = resolutions[0]
    assert r.decision == LlmDecision.REJECTED
    assert r.target_resource is None
    assert "out-of-scope" in r.reason.lower()


def test_merge_linked_without_cardinality_defaults_to_one_to_many():
    """LLM picks a target but forgets cardinality → default O2M."""
    cand = _make_unresolved("projects", "assignee")
    llm_raw = [{
        "id": 0, "decision": "linked", "target_resource": "users",
        "reason": "role word",
    }]
    resolutions = _merge_resolutions(
        to_resolve=[cand], llm_raw=llm_raw, resources=["projects", "users"]
    )
    assert resolutions[0].decision == LlmDecision.LINKED
    assert resolutions[0].cardinality == Cardinality.ONE_TO_MANY


def test_merge_invalid_decision_is_silently_dropped():
    """LLM returns a decision string we don't know → drop entry."""
    cand = _make_unresolved("projects", "assignee")
    llm_raw = [{
        "id": 0, "decision": "MAYBE", "target_resource": "users",
        "reason": "unsure",
    }]
    resolutions = _merge_resolutions(
        to_resolve=[cand], llm_raw=llm_raw, resources=["projects", "users"]
    )
    assert resolutions == []


def test_merge_out_of_range_id_dropped():
    """LLM returns an id that doesn't map to any candidate → drop."""
    cand = _make_unresolved("projects", "assignee")
    llm_raw = [
        {"id": 999, "decision": "linked", "target_resource": "users",
         "cardinality": "ONE_TO_MANY", "reason": ""},
        {"id": 0, "decision": "rejected", "reason": "free text"},
    ]
    resolutions = _merge_resolutions(
        to_resolve=[cand], llm_raw=llm_raw, resources=["projects", "users"]
    )
    assert len(resolutions) == 1
    assert resolutions[0].decision == LlmDecision.REJECTED


def test_merge_rejected_emits_rejected():
    cand = _make_unresolved("projects", "label")
    llm_raw = [{"id": 0, "decision": "rejected", "reason": "free text label"}]
    resolutions = _merge_resolutions(
        to_resolve=[cand], llm_raw=llm_raw, resources=["projects", "users"]
    )
    assert resolutions[0].decision == LlmDecision.REJECTED
    assert resolutions[0].reason == "free text label"


# ---------------------------------------------------------------------------
# Apply — in-place mutation of FkCandidate objects
# ---------------------------------------------------------------------------


def test_apply_linked_upgrades_candidate():
    cand = _make_unresolved("projects", "assignee")
    resolution = FkResolution(
        source_resource="projects",
        source_path=cand.source_path,
        raw_target="assignee",
        candidate_type=CandidateType.SCALAR_ID,
        decision=LlmDecision.LINKED,
        target_resource="users",
        cardinality=Cardinality.ONE_TO_MANY,
        reason="role word",
    )
    outcome = _apply_resolutions(
        [cand], [resolution], model="sonnet-x",
        cache_hit=False, cache_key="k",
    )
    assert cand.llm_inferred is True
    assert cand.llm_decision == LlmDecision.LINKED
    assert cand.target_resource == "users"
    assert cand.inferred_cardinality == Cardinality.ONE_TO_MANY
    assert cand.needs_llm is False
    assert cand.llm_model == "sonnet-x"
    assert outcome.linked_count == 1
    assert outcome.rejected_count == 0


def test_apply_rejected_clears_target_and_marks_rejected():
    cand = _make_unresolved("projects", "label")
    resolution = FkResolution(
        source_resource="projects",
        source_path=cand.source_path,
        raw_target="label",
        candidate_type=CandidateType.SCALAR_ID,
        decision=LlmDecision.REJECTED,
        target_resource=None,
        cardinality=None,
        reason="free text",
    )
    outcome = _apply_resolutions(
        [cand], [resolution], model="sonnet-x",
        cache_hit=False, cache_key="k",
    )
    assert cand.llm_inferred is True
    assert cand.llm_decision == LlmDecision.REJECTED
    assert cand.target_resource is None
    assert cand.needs_llm is False  # so the writer routes to rejected bucket
    assert outcome.rejected_count == 1


def test_apply_leaves_unmatched_candidate_alone():
    """A resolution for a candidate not in the current list is a no-op."""
    cand = _make_unresolved("projects", "assignee")
    stale = FkResolution(
        source_resource="projects",
        source_path=("Stale", "stale_id"),
        raw_target="stale",
        candidate_type=CandidateType.SCALAR_ID,
        decision=LlmDecision.LINKED,
        target_resource="users",
        cardinality=Cardinality.ONE_TO_MANY,
        reason="",
    )
    _apply_resolutions(
        [cand], [stale], model="m", cache_hit=False, cache_key="k",
    )
    assert cand.llm_inferred is False
    assert cand.target_resource is None


# ---------------------------------------------------------------------------
# Cache roundtrip
# ---------------------------------------------------------------------------


def test_cache_roundtrip(tmp_path: Path):
    resolutions = [
        FkResolution(
            source_resource="projects",
            source_path=("Project", "assignee_id"),
            raw_target="assignee",
            candidate_type=CandidateType.SCALAR_ID,
            decision=LlmDecision.LINKED,
            target_resource="users",
            cardinality=Cardinality.ONE_TO_MANY,
            reason="role word",
        ),
        FkResolution(
            source_resource="projects",
            source_path=("Project", "tag_name"),
            raw_target="tag",
            candidate_type=CandidateType.SCALAR_ID,
            decision=LlmDecision.REJECTED,
            target_resource=None,
            cardinality=None,
            reason="free text",
        ),
    ]
    cache_path = tmp_path / RESOLUTIONS_CACHE_FILENAME
    write_resolutions_cache(
        resolutions=resolutions, cache_path=cache_path,
        cache_key="k1", model="sonnet-x", resources=["projects", "users"],
    )
    assert cache_path.exists()
    loaded = load_cached_resolutions(cache_path, expected_key="k1")
    assert loaded is not None
    assert len(loaded) == 2
    linked = [r for r in loaded if r.decision == LlmDecision.LINKED][0]
    assert linked.target_resource == "users"
    assert linked.cardinality == Cardinality.ONE_TO_MANY
    rejected = [r for r in loaded if r.decision == LlmDecision.REJECTED][0]
    assert rejected.target_resource is None


def test_cache_miss_on_wrong_key(tmp_path: Path):
    cache_path = tmp_path / RESOLUTIONS_CACHE_FILENAME
    write_resolutions_cache(
        resolutions=[], cache_path=cache_path,
        cache_key="old", model="m", resources=["projects"],
    )
    assert load_cached_resolutions(cache_path, expected_key="new") is None


def test_cache_miss_on_missing_file(tmp_path: Path):
    assert load_cached_resolutions(tmp_path / "nope.json", "k") is None


# ---------------------------------------------------------------------------
# End-to-end: resolve_candidates() with a stubbed LLM
# ---------------------------------------------------------------------------


def _build_e2e_fixture(default_naming):
    """Spec with a walker-unresolved ``assignee_id`` + walker-linked ``owner_id``."""
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
                    "owner_id": {"type": "integer"},      # walker-linked
                    "assignee_id": {"type": "integer"},   # walker-unresolved
                    "tag_name": {"type": "string"},       # not a candidate at all
                },
            }
        },
    )
    alias_map = make_alias_map({"projects": [], "users": ["owner"]})
    rem = build_map(spec, alias_map, default_naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    candidates = extract_candidates(
        rem=rem, shapes=shapes, alias_map=alias_map,
        naming=default_naming, spec=spec,
    )
    return spec, alias_map, rem, shapes, candidates


def test_resolve_candidates_end_to_end_with_stubbed_llm(
    tmp_path: Path, default_naming, monkeypatch
):
    """A full run: extractor → resolution → writer, stubbing the LLM.

    Asserts that:
      * Walker-linked ``owner`` stays in the ``linked`` bucket with
        ``llm_inferred`` absent.
      * Walker-unresolved ``assignee`` moves into the ``linked`` bucket
        with ``llm_inferred=True``.
      * The cache file is written with the outcome counts.
    """
    spec, alias_map, rem, shapes, candidates = _build_e2e_fixture(default_naming)

    # Sanity: there should be at least one unresolved candidate (``assignee``).
    unresolved = [c for c in candidates if c.needs_llm]
    assert any(c.raw_target == "assignee" for c in unresolved), (
        f"fixture changed: {[c.raw_target for c in candidates]}"
    )

    def fake_call_claude_json(prompt, model, max_retries=1):
        # Inspect the prompt only loosely — we care that the
        # module rendered something containing the candidate.
        assert "assignee" in prompt
        # Return a linked decision for every id in the prompt. We
        # can't easily know the ids without parsing, but the test
        # fixture only has one unresolved candidate so id 0 is it.
        return {
            "resolutions": [
                {
                    "id": 0,
                    "decision": "linked",
                    "target_resource": "users",
                    "cardinality": "ONE_TO_MANY",
                    "reason": "assignee is a role word for users",
                }
            ]
        }

    monkeypatch.setattr(
        "fk_pipeline.resolution.call_claude_json",
        fake_call_claude_json,
    )

    outcome = resolve_candidates(
        candidates=candidates,
        rem=rem,
        shapes=shapes,
        alias_map=alias_map,
        spec=spec,
        resources=["projects", "users"],
        model="claude-sonnet-4-5",
        output_dir=tmp_path,
    )
    assert outcome.linked_count == 1
    assert outcome.rejected_count == 0
    assert outcome.cache_hit is False

    # Walker-linked ``owner`` is untouched.
    owner = next(c for c in candidates if c.raw_target == "owner")
    assert owner.llm_inferred is False
    assert owner.target_resource == "users"

    # Walker-unresolved ``assignee`` is now linked and marked LLM-inferred.
    assignee = next(c for c in candidates if c.raw_target == "assignee")
    assert assignee.llm_inferred is True
    assert assignee.llm_decision == LlmDecision.LINKED
    assert assignee.target_resource == "users"
    assert assignee.inferred_cardinality == Cardinality.ONE_TO_MANY
    assert assignee.needs_llm is False

    # Cache file written.
    cache_path = tmp_path / RESOLUTIONS_CACHE_FILENAME
    assert cache_path.exists()
    data = json.loads(cache_path.read_text())
    assert data["_meta"]["linked_count"] == 1


def test_resolve_candidates_cache_hit_second_run(
    tmp_path: Path, default_naming, monkeypatch
):
    """Running twice with the same inputs hits the cache and doesn't call LLM."""
    spec, alias_map, rem, shapes, candidates1 = _build_e2e_fixture(default_naming)

    call_count = {"n": 0}

    def fake_call(prompt, model, max_retries=1):
        call_count["n"] += 1
        return {
            "resolutions": [
                {
                    "id": 0, "decision": "linked",
                    "target_resource": "users",
                    "cardinality": "ONE_TO_MANY", "reason": "",
                }
            ]
        }

    monkeypatch.setattr("fk_pipeline.resolution.call_claude_json", fake_call)

    resolve_candidates(
        candidates=candidates1, rem=rem, shapes=shapes, alias_map=alias_map,
        spec=spec, resources=["projects", "users"],
        model="claude-sonnet-4-5", output_dir=tmp_path,
    )
    assert call_count["n"] == 1

    # Re-run with a freshly-extracted candidate list (same fixture).
    _, _, _, _, candidates2 = _build_e2e_fixture(default_naming)
    outcome = resolve_candidates(
        candidates=candidates2, rem=rem, shapes=shapes, alias_map=alias_map,
        spec=spec, resources=["projects", "users"],
        model="claude-sonnet-4-5", output_dir=tmp_path,
    )
    assert call_count["n"] == 1, "second run must not call the LLM"
    assert outcome.cache_hit is True
    # The cached resolution should have been applied.
    assignee2 = next(c for c in candidates2 if c.raw_target == "assignee")
    assert assignee2.llm_inferred is True
    assert assignee2.target_resource == "users"


def test_resolve_candidates_noop_when_nothing_needs_llm(
    tmp_path: Path, default_naming, monkeypatch
):
    """When every candidate is already mechanically linked, no LLM call."""
    # A spec with only ``owner_id`` (walker-linked via alias).
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
                    "owner_id": {"type": "integer"},
                },
            }
        },
    )
    alias_map = make_alias_map({"projects": [], "users": ["owner"]})
    rem = build_map(spec, alias_map, default_naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    candidates = extract_candidates(
        rem=rem, shapes=shapes, alias_map=alias_map,
        naming=default_naming, spec=spec,
    )
    assert all(not c.needs_llm for c in candidates)

    def boom(*_a, **_kw):  # pragma: no cover
        raise AssertionError("LLM should not have been called")

    monkeypatch.setattr("fk_pipeline.resolution.call_claude_json", boom)

    outcome = resolve_candidates(
        candidates=candidates, rem=rem, shapes=shapes, alias_map=alias_map,
        spec=spec, resources=["projects", "users"],
        model="claude-sonnet-4-5", output_dir=tmp_path,
    )
    assert outcome.linked_count == 0
    assert outcome.rejected_count == 0
    assert outcome.cache_hit is False
    # No cache file either — we don't write one when there was no work.
    assert not (tmp_path / RESOLUTIONS_CACHE_FILENAME).exists()


# ---------------------------------------------------------------------------
# Writer integration — rejected bucket rendering
# ---------------------------------------------------------------------------


def test_writer_splits_linked_unresolved_rejected(tmp_path: Path, default_naming):
    """After resolution, the three buckets show up in the artifact."""
    spec = make_spec({"/projects": {"get": make_op()}})
    alias_map = make_alias_map({"projects": [], "users": []})
    rem = build_map(spec, alias_map, default_naming)

    walker_linked = FkCandidate(
        source_resource="projects",
        source_path=("Project", "owner_id"),
        raw_target="owner",
        candidate_type=CandidateType.SCALAR_ID,
        resolution_reason=ResolutionReason.SUFFIX_STRIP,
        target_resource="users",
        inferred_cardinality=Cardinality.ONE_TO_MANY,
        confidence=Confidence.STRONG,
        needs_llm=False,
        evidence="walker-linked",
    )
    llm_linked = FkCandidate(
        source_resource="projects",
        source_path=("Project", "assignee_id"),
        raw_target="assignee",
        candidate_type=CandidateType.SCALAR_ID,
        resolution_reason=ResolutionReason.UNRESOLVED,
        target_resource="users",
        inferred_cardinality=Cardinality.ONE_TO_MANY,
        confidence=Confidence.WEAK,
        needs_llm=False,
        evidence="llm-linked",
        llm_inferred=True,
        llm_decision=LlmDecision.LINKED,
        llm_reason="assignee is a user",
        llm_model="sonnet-x",
    )
    llm_rejected = FkCandidate(
        source_resource="projects",
        source_path=("Project", "tag_name"),
        raw_target="tag",
        candidate_type=CandidateType.SCALAR_ID,
        resolution_reason=ResolutionReason.UNRESOLVED,
        target_resource=None,
        inferred_cardinality=None,
        confidence=Confidence.WEAK,
        needs_llm=False,
        evidence="llm-rejected",
        llm_inferred=True,
        llm_decision=LlmDecision.REJECTED,
        llm_reason="free text label",
        llm_model="sonnet-x",
    )
    still_unresolved = FkCandidate(
        source_resource="projects",
        source_path=("Project", "mystery_id"),
        raw_target="mystery",
        candidate_type=CandidateType.SCALAR_ID,
        resolution_reason=ResolutionReason.UNRESOLVED,
        target_resource=None,
        inferred_cardinality=None,
        confidence=Confidence.WEAK,
        needs_llm=True,
        evidence="still unresolved",
    )

    out_path = tmp_path / ARTIFACT_FILENAME
    meta = ArtifactMeta(
        app_slug="t", source_spec="/n", model="m", prompt_version="v1",
        user_resource_count=2, endpoint_count=len(rem.endpoints),
        edge_count=len(rem.edges), unbucketed_count=len(rem.unbucketed_endpoints),
        vocabulary_cache_hit=False,
        fk_candidate_count=4, fk_linked_count=2, fk_unresolved_count=1,
        fk_rejected_count=1, fk_llm_linked_count=1,
    )
    write_artifact(
        rem=rem, output_path=out_path, meta=meta,
        resource_order=["projects", "users"],
        fk_candidates=[walker_linked, llm_linked, llm_rejected, still_unresolved],
    )
    data = json.loads(out_path.read_text())
    projects_view = data["fk_candidates"]["projects"]
    assert {"linked", "unresolved", "rejected"} == set(projects_view.keys())

    linked_targets = {c["raw_target"] for c in projects_view["linked"]}
    unresolved_targets = {c["raw_target"] for c in projects_view["unresolved"]}
    rejected_targets = {c["raw_target"] for c in projects_view["rejected"]}
    assert linked_targets == {"owner", "assignee"}
    assert unresolved_targets == {"mystery"}
    assert rejected_targets == {"tag"}

    # The LLM-linked entry must carry its provenance.
    assignee_view = next(
        c for c in projects_view["linked"] if c["raw_target"] == "assignee"
    )
    assert assignee_view["llm_inferred"] is True
    assert assignee_view["llm_decision"] == "LINKED"
    assert assignee_view["llm_reason"] == "assignee is a user"

    # The walker-linked entry must NOT carry LLM fields.
    owner_view = next(
        c for c in projects_view["linked"] if c["raw_target"] == "owner"
    )
    assert "llm_inferred" not in owner_view

    # Meta counts are serialized.
    assert data["_meta"]["fk_rejected_count"] == 1
    assert data["_meta"]["fk_llm_linked_count"] == 1
