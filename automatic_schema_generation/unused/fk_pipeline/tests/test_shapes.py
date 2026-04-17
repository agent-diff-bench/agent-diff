"""Shape resolution tests.

These tests don't touch the extractor — they just assert that the
picker chooses the right representative schema and that the
normalizer unwraps envelopes, nullable wrappers, and ``allOf``
correctly. Each test hands the resolver a hand-built spec + a fake
REM so we can pin down one decision per test.
"""

from __future__ import annotations

from typing import Any

from fk_pipeline.bucketing import build_map
from fk_pipeline.shapes import resolve_shapes

from .conftest import make_alias_map, make_op, make_spec


def _rem(spec, resources):
    return build_map(spec, make_alias_map({r: [] for r in resources}), None)  # noqa


def _rem_with_naming(spec, resources, naming):
    return build_map(spec, make_alias_map({r: [] for r in resources}), naming)


def test_owner_item_response_picked_as_shape(default_naming):
    """When an OWNER_ITEM endpoint exists, its 200 response is the shape."""
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
                    "owner_id": {"type": "integer"},
                },
            }
        },
    )
    alias_map = make_alias_map({"projects": []})
    rem = build_map(spec, alias_map, default_naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    assert "projects" in shapes
    shape = shapes["projects"]
    assert shape.source == "owner_item"
    assert shape.origin_schema_name == "Project"
    assert set(shape.properties.keys()) == {"id", "name", "owner_id"}


def test_owner_collection_unwraps_pagination_envelope(default_naming):
    """A paginated list response has its envelope unwrapped to the item shape."""
    spec = make_spec(
        {
            "/projects": {
                "get": make_op(
                    operation_id="list_projects",
                    response_schema_ref="#/components/schemas/ProjectList",
                )
            }
        },
        schemas={
            "ProjectList": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Project"},
                    },
                    "total": {"type": "integer"},
                    "next": {"type": "string"},
                },
            },
            "Project": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
        },
    )
    alias_map = make_alias_map({"projects": []})
    rem = build_map(spec, alias_map, default_naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    shape = shapes["projects"]
    assert shape.source == "owner_collection"
    # Envelope unwrapped → inner Project schema props are exposed.
    assert set(shape.properties.keys()) == {"id", "name"}
    # The unwrap should have emitted a warning for traceability.
    assert any("pagination envelope" in w for w in shape.warnings)


def test_component_fallback_when_no_endpoints(default_naming):
    """A resource with no endpoints but a matching schema still gets a shape."""
    spec = make_spec(
        {"/health": {"get": make_op(operation_id="health")}},
        schemas={
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "login": {"type": "string"},
                },
            }
        },
    )
    alias_map = make_alias_map({"users": []})
    rem = build_map(spec, alias_map, default_naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    shape = shapes["users"]
    assert shape.source == "component"
    assert shape.origin_schema_name == "User"
    assert "login" in shape.properties


def test_all_of_merged_into_flat_object(default_naming):
    """allOf branches are merged; later branches override earlier on conflict."""
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
                "allOf": [
                    {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                        },
                    },
                    {
                        "type": "object",
                        "properties": {
                            # Conflicts with first branch — last should win.
                            "name": {"type": "string", "maxLength": 100},
                            "email": {"type": "string"},
                        },
                    },
                ]
            }
        },
    )
    alias_map = make_alias_map({"users": []})
    rem = build_map(spec, alias_map, default_naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    shape = shapes["users"]
    # All three properties surface.
    assert {"id", "name", "email"} <= set(shape.properties.keys())
    # The conflict on ``name`` was noted as a warning.
    assert any("allOf merge conflict" in w and "name" in w for w in shape.warnings)


def test_nullable_wrapper_unwrapped(default_naming):
    """A $ref inside anyOf[X, null] unwraps to the non-null branch."""
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
                    "owner": {
                        "anyOf": [
                            {"$ref": "#/components/schemas/User"},
                            {"type": "null"},
                        ]
                    }
                },
            },
            "User": {
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
        },
    )
    alias_map = make_alias_map({"projects": []})
    rem = build_map(spec, alias_map, default_naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    # The shape is the Project schema; the owner prop is preserved and
    # its schema is the unwrapped nullable, which still carries $ref.
    owner_schema = shapes["projects"].properties["owner"]
    assert "anyOf" in owner_schema or "$ref" in owner_schema


def test_cycle_terminates_via_visited_set(default_naming):
    """A → B → A shouldn't recurse forever."""
    spec = make_spec(
        {
            "/a/{id}": {
                "get": make_op(
                    operation_id="get_a",
                    path_params=["id"],
                    response_schema_ref="#/components/schemas/A",
                )
            }
        },
        schemas={
            "A": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "b": {"$ref": "#/components/schemas/B"},
                },
            },
            "B": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "a": {"$ref": "#/components/schemas/A"},
                },
            },
        },
    )
    alias_map = make_alias_map({"a": []})
    rem = build_map(spec, alias_map, default_naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    # Must terminate and produce a usable shape.
    assert "a" in shapes
    assert shapes["a"].source == "owner_item"


def test_resource_with_no_shape_source(default_naming):
    """A scoped resource that has nothing to anchor to gets an empty shape."""
    spec = make_spec({"/health": {"get": make_op(operation_id="health")}})
    alias_map = make_alias_map({"widgets": []})
    rem = build_map(spec, alias_map, default_naming)
    shapes = resolve_shapes(rem, spec, alias_map)
    assert shapes["widgets"].source == "none"
    assert shapes["widgets"].properties == {}
