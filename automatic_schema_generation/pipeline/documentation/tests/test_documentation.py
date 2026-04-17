"""Tests for endpoints.json documentation generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from pipeline.config import PipelineConfig, load_config
from pipeline.documentation.endpoints import (
    generate_endpoints_document,
    write_endpoints_document,
)


def _config(tmp_path: Path, resources: dict[str, Any]) -> PipelineConfig:
    spec_path = tmp_path / "spec.json"
    spec_path.write_text('{"paths": {}, "components": {"schemas": {}}}')
    cfg_path = tmp_path / "app.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "app_slug": "test",
        "app_name": "Test",
        "openapi_path": "spec.json",
        "target_dir": "out",
        "resources": resources,
    }))
    return load_config(cfg_path)


def test_empty_spec_produces_minimal_document(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    document = generate_endpoints_document({}, config)
    assert document["endpoints"] == {}
    assert document["schemas"] == {}
    assert document["_meta"]["endpoint_count"] == 0
    assert document["_meta"]["schema_count"] == 0
    assert "generated_at" in document["_meta"]


def test_single_endpoint_entry_shape(tmp_path: Path) -> None:
    config = _config(tmp_path, {
        "users": {"aliases": ["user", "owner"]},
        "repos": {"aliases": ["repo"]},
        "issues": {"aliases": ["issue"]},
    })
    spec = {
        "paths": {
            "/repos/{owner}/{repo}/issues": {
                "get": {
                    "parameters": [{"name": "assignee", "in": "query"}],
                    "responses": {"200": {"description": "ok"}},
                },
            },
        },
    }
    document = generate_endpoints_document(spec, config)
    assert "GET /repos/{owner}/{repo}/issues" in document["endpoints"]
    entry = document["endpoints"]["GET /repos/{owner}/{repo}/issues"]
    assert entry["method"] == "GET"
    assert entry["path"] == "/repos/{owner}/{repo}/issues"
    assert entry["subject"] == "issues"
    assert entry["subject_source"] == "url_rightmost_alias"
    assert entry["parameters"] == [{"name": "assignee", "in": "query"}]
    assert entry["request_body"] is None
    assert entry["responses"] == {"200": {"description": "ok"}}
    assert "references" in entry
    references = entry["references"]
    assert "path" in references
    assert "parameters" in references
    assert "body" in references
    assert "property" in references


def test_transitive_schema_closure(tmp_path: Path) -> None:
    """A → B → C where Issue refs A: all of A, B, C land in the schemas block."""
    config = _config(tmp_path, {"issues": {"aliases": ["issue"]}})
    spec = {
        "paths": {
            "/issues": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/A"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "A": {
                    "type": "object",
                    "properties": {
                        "b": {"$ref": "#/components/schemas/B"},
                    },
                },
                "B": {
                    "type": "object",
                    "properties": {
                        "c": {"$ref": "#/components/schemas/C"},
                    },
                },
                "C": {"type": "object"},
                "Unused": {"type": "object"},
            },
        },
    }
    document = generate_endpoints_document(spec, config)
    assert set(document["schemas"].keys()) == {"A", "B", "C"}
    assert "Unused" not in document["schemas"]


def test_refs_are_rewritten_to_self_contained_form(tmp_path: Path) -> None:
    """Every ``$ref`` in both endpoints and schemas gets the new prefix."""
    config = _config(tmp_path, {"issues": {"aliases": ["issue"]}})
    spec = {
        "paths": {
            "/issues": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Issue"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "Issue": {
                    "type": "object",
                    "properties": {
                        "related": {"$ref": "#/components/schemas/Issue"},
                    },
                },
            },
        },
    }
    document = generate_endpoints_document(spec, config)
    # Endpoint ref is rewritten.
    entry = document["endpoints"]["GET /issues"]
    response_schema = entry["responses"]["200"]["content"]["application/json"]["schema"]
    assert response_schema == {"$ref": "#/schemas/Issue"}
    # Self-reference inside the schemas block is rewritten too.
    issue_related = document["schemas"]["Issue"]["properties"]["related"]
    assert issue_related == {"$ref": "#/schemas/Issue"}


def test_cycle_in_component_schemas_terminates(tmp_path: Path) -> None:
    config = _config(tmp_path, {"issues": {"aliases": ["issue"]}})
    spec = {
        "paths": {
            "/issues": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/A"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "A": {"properties": {"b": {"$ref": "#/components/schemas/B"}}},
                "B": {"properties": {"a": {"$ref": "#/components/schemas/A"}}},
            },
        },
    }
    document = generate_endpoints_document(spec, config)
    assert set(document["schemas"].keys()) == {"A", "B"}


def test_references_populated_from_walkers(tmp_path: Path) -> None:
    config = _config(tmp_path, {
        "users": {"aliases": ["user"]},
        "issues": {"aliases": ["issue"]},
    })
    spec = {
        "paths": {
            "/issues": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "user_id": {"type": "integer"},
                                    },
                                },
                            },
                        },
                    },
                    "responses": {"201": {"description": "created"}},
                },
            },
        },
    }
    document = generate_endpoints_document(spec, config)
    entry = document["endpoints"]["POST /issues"]
    property_refs = entry["references"]["property"]
    resources = {reference["resource"] for reference in property_refs}
    assert "users" in resources


def test_write_endpoints_document_roundtrip(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "paths": {
            "/users/{user_id}": {
                "get": {"responses": {"200": {"description": "ok"}}},
            },
        },
    }
    document = generate_endpoints_document(spec, config)
    output_path = tmp_path / "pipeline_docs" / "endpoints.json"
    write_endpoints_document(document, output_path)
    assert output_path.exists()
    reloaded = json.loads(output_path.read_text())
    assert "GET /users/{user_id}" in reloaded["endpoints"]
    assert reloaded["_meta"]["endpoint_count"] == 1
