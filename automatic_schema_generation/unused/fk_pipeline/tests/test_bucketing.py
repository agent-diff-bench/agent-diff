"""Classifier edge-case tests.

Each test exercises one decision the role classifier has to make.
They're deliberately small — one path, one expected edge set — so a
regression report points at a named scenario instead of a diff of
counts.
"""

from __future__ import annotations

from fk_pipeline.bucketing import build_map
from fk_pipeline.models import EdgeRole

from .conftest import make_alias_map, make_op, make_spec


def _edges_by_resource(rem, endpoint_key: str) -> dict[str, EdgeRole]:
    """Return {resource: role} for edges attached to one endpoint."""
    rec = rem.endpoints[endpoint_key]
    return {e.resource: e.role for e in rec.resource_edges}


def test_owner_collection_top_level(default_naming):
    """GET /projects — top-level collection, no parent, no self-id."""
    alias_map = make_alias_map({"projects": []})
    spec = make_spec(
        {"/projects": {"get": make_op(operation_id="list_projects")}}
    )
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /projects")
    assert edges == {"projects": EdgeRole.OWNER_COLLECTION}


def test_owner_item_with_id_suffix(default_naming):
    """GET /projects/{project_id} — strict REST self-id form."""
    alias_map = make_alias_map({"projects": []})
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
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /projects/{project_id}")
    assert edges == {"projects": EdgeRole.OWNER_ITEM}


def test_owner_item_with_bare_singular_param(default_naming):
    """GET /repos/{repo} — bare owner-singular path param (GitHub style)."""
    alias_map = make_alias_map({"repos": ["repo"]})
    spec = make_spec(
        {
            "/repos/{repo}": {
                "get": make_op(
                    operation_id="get_repo",
                    path_params=["repo"],
                )
            }
        }
    )
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /repos/{repo}")
    assert edges == {"repos": EdgeRole.OWNER_ITEM}


def test_owner_action_verb_suffix(default_naming):
    """POST /projects/{project_id}/archive — action verb after item."""
    alias_map = make_alias_map({"projects": []})
    spec = make_spec(
        {
            "/projects/{project_id}/archive": {
                "post": make_op(
                    operation_id="archive_project",
                    path_params=["project_id"],
                )
            }
        }
    )
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "POST /projects/{project_id}/archive")
    # The project resource is owner-action, and the action verb does
    # not itself become another edge.
    assert edges == {"projects": EdgeRole.OWNER_ACTION}


def test_sub_collection_nested(default_naming):
    """GET /projects/{project_id}/tasks — nested collection."""
    alias_map = make_alias_map({"projects": [], "tasks": []})
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
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /projects/{project_id}/tasks")
    # tasks is sub-collection; projects is referenced via path_param.
    assert edges == {
        "tasks": EdgeRole.SUB_COLLECTION,
        "projects": EdgeRole.PARENT,
    }


def test_parent_chain_with_sub_item(default_naming):
    """GET /projects/{project_id}/tasks/{task_id} — nested item."""
    alias_map = make_alias_map({"projects": [], "tasks": []})
    spec = make_spec(
        {
            "/projects/{project_id}/tasks/{task_id}": {
                "get": make_op(
                    operation_id="get_task",
                    path_params=["project_id", "task_id"],
                )
            }
        }
    )
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /projects/{project_id}/tasks/{task_id}")
    assert edges == {
        "tasks": EdgeRole.OWNER_ITEM,
        "projects": EdgeRole.PARENT,
    }


def test_query_referenced(default_naming):
    """GET /tasks?project_id=... — project surfaces as query reference."""
    alias_map = make_alias_map({"projects": [], "tasks": []})
    spec = make_spec(
        {
            "/tasks": {
                "get": make_op(
                    operation_id="list_tasks",
                    query_params=["project_id"],
                )
            }
        }
    )
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /tasks")
    assert edges == {
        "tasks": EdgeRole.OWNER_COLLECTION,
        "projects": EdgeRole.QUERY_REFERENCED,
    }


def test_qualifier_prefix_stripped(default_naming):
    """GET /tasks/{parent_task_id} — parent_ prefix strips to task."""
    alias_map = make_alias_map({"tasks": []})
    spec = make_spec(
        {
            "/tasks/{parent_task_id}": {
                "get": make_op(
                    operation_id="get_parent",
                    path_params=["parent_task_id"],
                )
            }
        }
    )
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /tasks/{parent_task_id}")
    # parent_task_id is deliberately NOT the self-id of tasks — it's a
    # self-referential parent reference, so the endpoint is an
    # OWNER_COLLECTION-like operation with a PARENT edge (dedup: the
    # stronger role for 'tasks' is OWNER_COLLECTION, overriding PARENT).
    assert edges == {"tasks": EdgeRole.OWNER_COLLECTION}


def test_body_referenced_via_schema_ref(default_naming):
    """GET /issues/{id} returning a User component → users body reference."""
    alias_map = make_alias_map({"issues": [], "users": []})
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
                    "user": {"$ref": "#/components/schemas/User"},
                },
            },
            "User": {
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
        },
    )
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /issues/{id}")
    assert edges["issues"] == EdgeRole.OWNER_ITEM
    assert edges["users"] == EdgeRole.BODY_REFERENCED


def test_body_ref_does_not_override_stronger(default_naming):
    """A schema ref to Task cannot demote tasks from OWNER_ITEM."""
    alias_map = make_alias_map({"tasks": []})
    spec = make_spec(
        {
            "/tasks/{task_id}": {
                "get": make_op(
                    operation_id="get_task",
                    path_params=["task_id"],
                    response_schema_ref="#/components/schemas/Task",
                )
            }
        },
        schemas={
            "Task": {"type": "object", "properties": {"id": {"type": "integer"}}},
        },
    )
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /tasks/{task_id}")
    assert edges == {"tasks": EdgeRole.OWNER_ITEM}


def test_parameter_ref_resolution(default_naming):
    """$ref parameters resolve to concrete name/in fields (GitHub style)."""
    alias_map = make_alias_map({"repos": ["repo"]})
    spec = make_spec(
        {
            "/repos/{repo}": {
                "get": {
                    "operationId": "get_repo",
                    "parameters": [{"$ref": "#/components/parameters/repo"}],
                    "responses": {"200": {"description": "ok"}},
                }
            }
        }
    )
    # Drop the resolved parameter definition into components.parameters.
    spec["components"]["parameters"] = {
        "repo": {"name": "repo", "in": "path", "required": True},
    }
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /repos/{repo}")
    assert edges == {"repos": EdgeRole.OWNER_ITEM}


def test_unresolvable_param_is_ignored(default_naming):
    """An unrecognized path param name shouldn't fabricate edges."""
    alias_map = make_alias_map({"projects": []})
    spec = make_spec(
        {
            "/projects/{weird_thing}": {
                "get": make_op(
                    operation_id="get_weird",
                    path_params=["weird_thing"],
                )
            }
        }
    )
    rem = build_map(spec, alias_map, default_naming)
    edges = _edges_by_resource(rem, "GET /projects/{weird_thing}")
    # The unrecognized param does NOT become an edge. The owner is
    # still projects, and because there's no matched self-id it stays
    # at OWNER_COLLECTION (a collection operation on a single path
    # param the classifier can't resolve).
    assert edges == {"projects": EdgeRole.OWNER_COLLECTION}


def test_unbucketed_endpoint_preserved(default_naming):
    """An endpoint with no resource matches lands in unbucketed with metadata."""
    alias_map = make_alias_map({"projects": []})
    spec = make_spec(
        {
            "/health": {"get": make_op(operation_id="health_check")},
        }
    )
    rem = build_map(spec, alias_map, default_naming)
    assert "GET /health" in rem.endpoints
    assert len(rem.unbucketed_endpoints) == 1
    unb = rem.unbucketed_endpoints[0]
    assert unb.key == "GET /health"
    assert unb.operation_id == "health_check"
    # Full operation dict is preserved for triage.
    assert unb.raw_operation.get("operationId") == "health_check"
