"""FK candidate extractor tests.

Each test builds a minimum spec that isolates one walker decision
(scalar _id, nested $ref, array of $ref, inline object, unresolved,
self-reference, path/query param lift). We assert on the candidate
list directly so a regression report pinpoints a named scenario.
"""

from __future__ import annotations

from fk_pipeline.bucketing import build_map
from fk_pipeline.candidates import (
    Cardinality,
    CandidateType,
    Confidence,
    ResolutionReason,
)
from fk_pipeline.extractor import extract_candidates
from fk_pipeline.shapes import resolve_shapes

from .conftest import make_alias_map, make_op, make_spec


def _run(spec, resource_aliases, naming):
    alias_map = make_alias_map(resource_aliases)
    rem = build_map(spec, alias_map, naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    return extract_candidates(
        rem=rem, shapes=shapes, alias_map=alias_map, naming=naming, spec=spec,
    )


def _find(cands, *, source, raw_target, ctype=None):
    hits = [
        c for c in cands
        if c.source_resource == source and c.raw_target == raw_target
        and (ctype is None or c.candidate_type == ctype)
    ]
    assert hits, (
        f"no candidate found for source={source!r} raw_target={raw_target!r} "
        f"(candidates: {[(c.source_resource, c.raw_target, c.candidate_type.value) for c in cands]})"
    )
    return hits[0]


# ---------------------------------------------------------------------------
# Pass 1: schema walk
# ---------------------------------------------------------------------------


def test_scalar_id_resolves_to_known_resource(default_naming):
    """``owner_id`` on Project with ``users`` scoped → linked ONE_TO_MANY."""
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
    cands = _run(spec, {"projects": [], "users": ["owner"]}, default_naming)
    hit = _find(
        cands, source="projects", raw_target="owner",
        ctype=CandidateType.SCALAR_ID,
    )
    assert hit.target_resource == "users"
    assert hit.resolution_reason == ResolutionReason.SUFFIX_STRIP
    assert hit.inferred_cardinality == Cardinality.ONE_TO_MANY
    assert hit.confidence == Confidence.STRONG
    assert hit.needs_llm is False


def test_scalar_id_unresolved_goes_to_llm_bucket(default_naming):
    """``assignee_id`` when ``assignee`` isn't in any alias → UNRESOLVED."""
    spec = make_spec(
        {
            "/issues/{id}": {
                "get": make_op(
                    operation_id="get_issue",
                    path_params=["id"],
                    response_schema_ref="#/components/schemas/Issue",
                )
            }
        },
        schemas={
            "Issue": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "assignee_id": {"type": "integer"},
                },
            }
        },
    )
    cands = _run(spec, {"issues": [], "users": []}, default_naming)
    hit = _find(cands, source="issues", raw_target="assignee")
    assert hit.target_resource is None
    assert hit.resolution_reason == ResolutionReason.UNRESOLVED
    assert hit.inferred_cardinality is None
    assert hit.confidence == Confidence.WEAK
    assert hit.needs_llm is True


def test_nested_ref_to_known_schema(default_naming):
    """``reviewer: {$ref: User}`` → linked NESTED_REF, target=users."""
    spec = make_spec(
        {
            "/pulls/{id}": {
                "get": make_op(
                    operation_id="get_pull",
                    path_params=["id"],
                    response_schema_ref="#/components/schemas/Pull",
                )
            }
        },
        schemas={
            "Pull": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "reviewer": {"$ref": "#/components/schemas/User"},
                },
            },
            "User": {
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
        },
    )
    cands = _run(spec, {"pulls": [], "users": []}, default_naming)
    hit = _find(
        cands, source="pulls", raw_target="User",
        ctype=CandidateType.NESTED_REF,
    )
    assert hit.target_resource == "users"
    assert hit.resolution_reason == ResolutionReason.SCHEMA_REF
    assert hit.inferred_cardinality == Cardinality.ONE_TO_MANY
    assert hit.needs_llm is False


def test_array_of_refs_emits_many_to_many(default_naming):
    """``labels: [{$ref: Label}]`` → linked ARRAY_OF_REFS, M:N."""
    spec = make_spec(
        {
            "/issues/{id}": {
                "get": make_op(
                    operation_id="get_issue",
                    path_params=["id"],
                    response_schema_ref="#/components/schemas/Issue",
                )
            }
        },
        schemas={
            "Issue": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "labels": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Label"},
                    },
                },
            },
            "Label": {
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
        },
    )
    cands = _run(spec, {"issues": [], "labels": []}, default_naming)
    hit = _find(
        cands, source="issues", raw_target="Label",
        ctype=CandidateType.ARRAY_OF_REFS,
    )
    assert hit.target_resource == "labels"
    assert hit.inferred_cardinality == Cardinality.MANY_TO_MANY
    assert hit.needs_llm is False


def test_inline_object_with_pk_field(default_naming):
    """Inline object with an ``id`` property → INLINE_OBJECT candidate."""
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
                    "owner": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                        },
                    },
                },
            }
        },
    )
    cands = _run(spec, {"projects": [], "users": ["owner"]}, default_naming)
    hit = _find(
        cands, source="projects", raw_target="owner",
        ctype=CandidateType.INLINE_OBJECT,
    )
    assert hit.target_resource == "users"
    assert hit.resolution_reason == ResolutionReason.DIRECT
    assert hit.inferred_cardinality == Cardinality.ONE_TO_MANY


def test_self_reference_is_weak_and_needs_llm(default_naming):
    """A field that points back at the same resource is kept but weak."""
    spec = make_spec(
        {
            "/users/{id}": {
                "get": make_op(
                    operation_id="get_user",
                    path_params=["id"],
                    response_schema_ref="#/components/schemas/User",
                )
            }
        },
        schemas={
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "manager": {"$ref": "#/components/schemas/User"},
                },
            }
        },
    )
    cands = _run(spec, {"users": []}, default_naming)
    hit = _find(
        cands, source="users", raw_target="User",
        ctype=CandidateType.NESTED_REF,
    )
    assert hit.target_resource == "users"
    assert hit.confidence == Confidence.WEAK
    assert hit.needs_llm is True


def test_unknown_schema_ref_is_unresolved(default_naming):
    """``owner: {$ref: Widget}`` when ``Widget`` isn't a resource."""
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
                    "owner": {"$ref": "#/components/schemas/Widget"},
                },
            },
            "Widget": {
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
        },
    )
    cands = _run(spec, {"projects": []}, default_naming)
    hit = _find(cands, source="projects", raw_target="Widget")
    assert hit.target_resource is None
    assert hit.resolution_reason == ResolutionReason.UNRESOLVED
    assert hit.needs_llm is True


def test_qualifier_prefix_resolves(default_naming):
    """``parent_project_id`` resolves via suffix + qualifier_prefix strip."""
    spec = make_spec(
        {
            "/tasks/{id}": {
                "get": make_op(
                    operation_id="get_task",
                    path_params=["id"],
                    response_schema_ref="#/components/schemas/Task",
                )
            }
        },
        schemas={
            "Task": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "parent_project_id": {"type": "integer"},
                },
            }
        },
    )
    cands = _run(spec, {"tasks": [], "projects": []}, default_naming)
    hit = _find(cands, source="tasks", raw_target="project")
    assert hit.target_resource == "projects"
    assert hit.resolution_reason == ResolutionReason.QUALIFIER_STRIP


def test_plain_scalar_without_fk_shape_is_ignored(default_naming):
    """``name: string`` generates no candidate — nothing FK-shaped about it."""
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
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                },
            }
        },
    )
    cands = _run(spec, {"projects": []}, default_naming)
    # None of the plain string fields become candidates.
    assert not any(
        c.source_resource == "projects"
        and c.raw_target in {"name", "description"}
        for c in cands
    )


# ---------------------------------------------------------------------------
# Pass 2: endpoint param lift
# ---------------------------------------------------------------------------


def test_query_param_fk_resolved(default_naming):
    """``?assignee_id=`` with ``users`` scoped + alias → QUERY_PARAM_FK."""
    spec = make_spec(
        {
            "/issues": {
                "get": make_op(
                    operation_id="list_issues",
                    query_params=["assignee_id"],
                )
            }
        }
    )
    cands = _run(spec, {"issues": [], "users": ["assignee"]}, default_naming)
    hit = _find(
        cands, source="issues", raw_target="assignee",
        ctype=CandidateType.QUERY_PARAM_FK,
    )
    assert hit.target_resource == "users"
    assert hit.inferred_cardinality == Cardinality.ONE_TO_MANY


def test_query_param_fk_unresolved(default_naming):
    """``?reviewer_id=`` with ``reviewer`` not in any alias → UNRESOLVED."""
    spec = make_spec(
        {
            "/pulls": {
                "get": make_op(
                    operation_id="list_pulls",
                    query_params=["reviewer_id"],
                )
            }
        }
    )
    cands = _run(spec, {"pulls": [], "users": []}, default_naming)
    hit = _find(
        cands, source="pulls", raw_target="reviewer",
        ctype=CandidateType.QUERY_PARAM_FK,
    )
    assert hit.target_resource is None
    assert hit.needs_llm is True


def test_owner_self_id_param_not_emitted(default_naming):
    """The owner's own self-id param must not become a FK candidate."""
    spec = make_spec(
        {
            "/projects/{project_id}": {
                "get": make_op(
                    operation_id="get_project",
                    path_params=["project_id"],
                )
            }
        }
    )
    cands = _run(spec, {"projects": []}, default_naming)
    # project_id is the owner's self-id → suppressed.
    assert not any(
        c.source_resource == "projects" and c.raw_target == "project"
        and c.candidate_type == CandidateType.PATH_PARAM_FK
        for c in cands
    )


def test_endpoint_params_lift_even_when_bucketing_has_parent_edge(default_naming):
    """Candidate list is complete: a PARENT-edge param is still lifted.

    Design note: bucketing edges and FK candidates are two different
    views of the same underlying relationship graph. The candidate
    list carries richer per-field detail (cardinality, source path,
    stem) that the edge view doesn't, so we deliberately do not
    suppress duplicates.
    """
    spec = make_spec(
        {
            "/projects/{project_id}/tasks": {
                "get": make_op(
                    operation_id="list_project_tasks",
                    path_params=["project_id"],
                )
            }
        }
    )
    cands = _run(spec, {"projects": [], "tasks": []}, default_naming)
    lifted = [
        c for c in cands
        if c.source_resource == "tasks"
        and c.target_resource == "projects"
        and c.candidate_type == CandidateType.PATH_PARAM_FK
    ]
    assert len(lifted) == 1
    assert lifted[0].inferred_cardinality == Cardinality.ONE_TO_MANY


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


def test_candidate_list_is_deterministic(default_naming):
    """Same inputs → same output order."""
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
                    "parent_id": {"type": "integer"},
                },
            }
        },
    )
    a = _run(spec, {"projects": [], "users": ["owner"]}, default_naming)
    b = _run(spec, {"projects": [], "users": ["owner"]}, default_naming)
    assert [(c.source_resource, c.raw_target, c.candidate_type) for c in a] == [
        (c.source_resource, c.raw_target, c.candidate_type) for c in b
    ]
