"""Tests for the property-level reference extractor (Group C)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pipeline.config import PipelineConfig, load_config
from pipeline.extraction.property_references import (
    PropertyReference,
    find_property_references,
)


def _config(
    tmp_path: Path,
    resources: dict[str, Any],
    *,
    naming: dict[str, Any] | None = None,
) -> PipelineConfig:
    spec_path = tmp_path / "spec.json"
    spec_path.write_text('{"paths": {}, "components": {"schemas": {}}}')
    cfg_path = tmp_path / "app.yaml"
    cfg_data: dict[str, Any] = {
        "app_slug": "test",
        "app_name": "Test",
        "openapi_path": "spec.json",
        "target_dir": "out",
        "resources": resources,
    }
    if naming is not None:
        cfg_data["naming"] = naming
    cfg_path.write_text(yaml.safe_dump(cfg_data))
    return load_config(cfg_path)


def test_empty_schema_returns_nothing(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    assert find_property_references({}, config, {}) == []


def test_property_name_compound_form_hits(tmp_path: Path) -> None:
    """``owner_id`` hits via the config-time alias expansion."""
    config = _config(tmp_path, {"users": {"aliases": ["user", "owner"]}})
    schema = {
        "type": "object",
        "properties": {
            "owner_id": {"type": "integer"},
            "title": {"type": "string"},
        },
    }
    references = find_property_references(schema, config, {})
    assert references == [
        PropertyReference(token="owner_id", resource="users", path=("owner_id",)),
    ]


def test_qualifier_prefix_strip(tmp_path: Path) -> None:
    """``parent_repo_id`` strips the ``parent_`` prefix and then hits."""
    config = _config(
        tmp_path,
        {"repos": {"aliases": ["repo"]}},
        naming={"qualifier_prefixes": ["parent_"]},
    )
    schema = {
        "type": "object",
        "properties": {
            "parent_repo_id": {"type": "integer"},
        },
    }
    references = find_property_references(schema, config, {})
    assert len(references) == 1
    assert references[0].resource == "repos"
    assert references[0].token == "parent_repo_id"


def test_property_ref_to_bound_schema_hits(tmp_path: Path) -> None:
    """``assignee: {$ref: SimpleUser}`` emits via the bindings table."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    schema = {
        "type": "object",
        "properties": {
            "assignee": {"$ref": "#/components/schemas/SimpleUser"},
        },
    }
    bindings = {"SimpleUser": "users"}
    references = find_property_references(schema, config, bindings)
    assert len(references) == 1
    assert references[0].resource == "users"
    assert references[0].token == "assignee"
    assert references[0].path == ("assignee",)


def test_name_and_ref_hit_same_resource_dedupes(tmp_path: Path) -> None:
    """If both the name and the $ref at the same path bind to the same resource, emit once."""
    config = _config(tmp_path, {"users": {"aliases": ["user", "assignee"]}})
    schema = {
        "type": "object",
        "properties": {
            "assignee": {"$ref": "#/components/schemas/User"},
        },
    }
    references = find_property_references(schema, config, {"User": "users"})
    assert len(references) == 1


def test_nested_inline_object_walked(tmp_path: Path) -> None:
    """An inline nested object under a non-aliased property is still walked."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    schema = {
        "type": "object",
        "properties": {
            "meta": {
                "type": "object",
                "properties": {
                    "actor": {"$ref": "#/components/schemas/User"},
                },
            },
        },
    }
    references = find_property_references(schema, config, {"User": "users"})
    assert len(references) == 1
    assert references[0].resource == "users"
    assert references[0].path == ("meta", "actor")


def test_array_items_walked(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    schema = {
        "type": "object",
        "properties": {
            "reviewers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer"},
                    },
                },
            },
        },
    }
    references = find_property_references(schema, config, {})
    resources = {reference.resource for reference in references}
    assert "users" in resources


def test_additional_properties_walked(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    schema = {
        "type": "object",
        "additionalProperties": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
            },
        },
    }
    references = find_property_references(schema, config, {})
    assert len(references) == 1
    assert references[0].resource == "users"


def test_composition_branches_walked(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    schema = {
        "allOf": [
            {"type": "object", "properties": {"user_id": {"type": "integer"}}},
            {"type": "object", "properties": {"title": {"type": "string"}}},
        ],
    }
    references = find_property_references(schema, config, {})
    assert len(references) == 1
    assert references[0].resource == "users"


def test_top_level_ref_is_not_followed(tmp_path: Path) -> None:
    """A top-level ``$ref`` short-circuits the walk — we never chase refs."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    schema = {"$ref": "#/components/schemas/User"}
    # Even though User is in bindings, we don't follow the top-level ref.
    references = find_property_references(schema, config, {"User": "users"})
    assert references == []


def test_ref_following_descends_into_component_schema(tmp_path: Path) -> None:
    """With ``component_schemas`` provided, a top-level ``$ref`` is followed."""
    config = _config(tmp_path, {
        "users": {"aliases": ["user", "assignee"]},
        "repos": {"aliases": ["repo"]},
    })
    component_schemas = {
        "Issue": {
            "type": "object",
            "properties": {
                "assignee": {"$ref": "#/components/schemas/User"},
                "repo_id": {"type": "integer"},
            },
        },
        "User": {"type": "object", "properties": {"id": {"type": "integer"}}},
    }
    # Walk a body that is just {$ref: Issue} — without component_schemas we
    # emit nothing; with it, we follow into Issue and find its field-level refs.
    references = find_property_references(
        {"$ref": "#/components/schemas/Issue"},
        config,
        {"Issue": "issues", "User": "users"},
        component_schemas=component_schemas,
    )
    resources_by_path = {reference.path: reference.resource for reference in references}
    assert resources_by_path[("assignee",)] == "users"
    assert resources_by_path[("repo_id",)] == "repos"


def test_ref_following_cycle_safety(tmp_path: Path) -> None:
    """Mutually-referencing schemas don't recurse forever."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    component_schemas = {
        "A": {
            "type": "object",
            "properties": {"b": {"$ref": "#/components/schemas/B"}},
        },
        "B": {
            "type": "object",
            "properties": {"a": {"$ref": "#/components/schemas/A"}},
        },
    }
    # Should terminate without recursion errors.
    references = find_property_references(
        {"$ref": "#/components/schemas/A"},
        config,
        {},
        component_schemas=component_schemas,
    )
    assert isinstance(references, list)


def test_non_matching_properties_ignored(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "created_at": {"type": "string"},
        },
    }
    assert find_property_references(schema, config, {}) == []
