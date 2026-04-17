"""Tests for resources.json resource-first pivot."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from pipeline.config import PipelineConfig, load_config
from pipeline.documentation.endpoints import generate_endpoints_document
from pipeline.documentation.resources import (
    generate_resources_document,
    write_resources_document,
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


def test_empty_spec_produces_all_configured_resources(tmp_path: Path) -> None:
    """Every configured resource appears even when there's no endpoint data."""
    config = _config(tmp_path, {
        "users": {"aliases": ["user"]},
        "repos": {"aliases": ["repo"]},
    })
    endpoints_document = generate_endpoints_document({}, config)
    resources_document = generate_resources_document({}, config, endpoints_document)
    assert set(resources_document["resources"].keys()) == {"users", "repos"}
    for record in resources_document["resources"].values():
        assert record["bound_schemas"] == {}
        assert record["endpoint_keys"] == []
        assert record["outgoing_references"] == {}
        assert record["incoming_references"] == {}


def test_bound_schemas_attached_per_resource(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user", "simple_user"]}})
    spec = {
        "paths": {
            "/users/{user_id}": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/SimpleUser"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "SimpleUser": {"type": "object", "properties": {"id": {"type": "integer"}}},
            },
        },
    }
    endpoints_document = generate_endpoints_document(spec, config)
    resources_document = generate_resources_document(spec, config, endpoints_document)
    users_record = resources_document["resources"]["users"]
    assert "SimpleUser" in users_record["bound_schemas"]


def test_endpoint_keys_populated_for_subject(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "paths": {
            "/users/{user_id}": {
                "get": {"responses": {"200": {"description": "ok"}}},
                "delete": {"responses": {"204": {"description": "ok"}}},
            },
        },
    }
    endpoints_document = generate_endpoints_document(spec, config)
    resources_document = generate_resources_document(spec, config, endpoints_document)
    users_endpoints = resources_document["resources"]["users"]["endpoint_keys"]
    assert "GET /users/{user_id}" in users_endpoints
    assert "DELETE /users/{user_id}" in users_endpoints


def test_outgoing_and_incoming_references_split(tmp_path: Path) -> None:
    """``issues → users`` evidence shows up as outgoing on issues and incoming on users."""
    config = _config(tmp_path, {
        "users": {"aliases": ["user", "owner"]},
        "issues": {"aliases": ["issue"]},
    })
    spec = {
        "paths": {
            "/issues/{issue_id}": {
                "get": {
                    "parameters": [{"name": "owner_id", "in": "query"}],
                    "responses": {"200": {"description": "ok"}},
                },
            },
        },
    }
    endpoints_document = generate_endpoints_document(spec, config)
    resources_document = generate_resources_document(spec, config, endpoints_document)
    issues_outgoing = resources_document["resources"]["issues"]["outgoing_references"]
    users_incoming = resources_document["resources"]["users"]["incoming_references"]
    assert "users" in issues_outgoing
    assert "issues" in users_incoming
    assert len(issues_outgoing["users"]) >= 1


def test_self_references_appear_in_outgoing_only(tmp_path: Path) -> None:
    """``issues → issues`` evidence goes in outgoing, not incoming (incoming excludes self)."""
    config = _config(tmp_path, {"issues": {"aliases": ["issue"]}})
    spec = {
        "paths": {
            "/issues/{issue_id}": {
                "get": {"responses": {"200": {"description": "ok"}}},
            },
        },
    }
    endpoints_document = generate_endpoints_document(spec, config)
    resources_document = generate_resources_document(spec, config, endpoints_document)
    issues_record = resources_document["resources"]["issues"]
    assert "issues" in issues_record["outgoing_references"]
    assert "issues" not in issues_record["incoming_references"]


def test_meta_hash_stable_across_reruns(tmp_path: Path) -> None:
    """Re-running produces the same source_endpoints_hash (modulo generated_at)."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "paths": {
            "/users/{user_id}": {
                "get": {"responses": {"200": {"description": "ok"}}},
            },
        },
    }
    first = generate_resources_document(spec, config, generate_endpoints_document(spec, config))
    second = generate_resources_document(spec, config, generate_endpoints_document(spec, config))
    assert first["_meta"]["source_endpoints_hash"] == second["_meta"]["source_endpoints_hash"]


def test_write_resources_document_roundtrip(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "paths": {
            "/users/{user_id}": {
                "get": {"responses": {"200": {"description": "ok"}}},
            },
        },
    }
    endpoints_document = generate_endpoints_document(spec, config)
    resources_document = generate_resources_document(spec, config, endpoints_document)
    output_path = tmp_path / "pipeline_docs" / "resources.json"
    write_resources_document(resources_document, output_path)
    assert output_path.exists()
    reloaded = json.loads(output_path.read_text())
    assert "users" in reloaded["resources"]
