"""Tests for the cross-endpoint reference grouper."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pipeline.config import PipelineConfig, load_config
from pipeline.extraction.reference_groups import (
    ReferenceEvidence,
    group_references_by_pair,
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


def test_empty_spec_returns_empty_groups(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    assert group_references_by_pair({}, config, {}) == {}


def test_url_references_grouped_by_subject_and_target(tmp_path: Path) -> None:
    """``GET /repos/{owner}/{repo}`` → subject=repos, targets={users, repos}."""
    config = _config(tmp_path, {
        "users": {"aliases": ["user", "owner"]},
        "repos": {"aliases": ["repo"]},
    })
    spec = {
        "paths": {
            "/repos/{owner}/{repo}": {
                "get": {"responses": {"200": {"description": "ok"}}},
            },
        },
    }
    groups = group_references_by_pair(spec, config, {})
    assert ("repos", "users") in groups
    assert ("repos", "repos") in groups  # self-reference via {repo} is valid evidence
    users_evidence = groups[("repos", "users")]
    assert any(entry.location == "owner" for entry in users_evidence)


def test_unresolved_subject_bucketed_under_sentinel(tmp_path: Path) -> None:
    """``GET /rate_limit`` has no alias hits — source is ``_unresolved_``."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "paths": {
            "/rate_limit": {
                "get": {
                    "parameters": [{"name": "user_id", "in": "query"}],
                    "responses": {"200": {"description": "ok"}},
                },
            },
        },
    }
    groups = group_references_by_pair(spec, config, {})
    assert ("_unresolved_", "users") in groups


def test_multiple_operations_merge_into_same_pair(tmp_path: Path) -> None:
    """Two endpoints with the same (subject, target) pair accumulate evidence."""
    config = _config(tmp_path, {
        "issues": {"aliases": ["issue"]},
        "users": {"aliases": ["user"]},
    })
    spec = {
        "paths": {
            "/issues/{issue_id}": {
                "get": {
                    "parameters": [{"name": "user_id", "in": "query"}],
                    "responses": {"200": {"description": "ok"}},
                },
            },
            "/issues/{issue_id}/comments": {
                "get": {
                    "parameters": [{"name": "user_id", "in": "query"}],
                    "responses": {"200": {"description": "ok"}},
                },
            },
        },
    }
    groups = group_references_by_pair(spec, config, {})
    # Both paths resolve to subject=issues (``comments`` isn't configured so
    # right-to-left walk falls through to ``{issue_id}`` → issues).
    issues_users = groups.get(("issues", "users"))
    assert issues_users is not None
    paths_seen = {entry.path for entry in issues_users}
    assert paths_seen == {"/issues/{issue_id}", "/issues/{issue_id}/comments"}


def test_body_and_property_references_flow_into_groups(tmp_path: Path) -> None:
    config = _config(tmp_path, {
        "issues": {"aliases": ["issue"]},
        "users": {"aliases": ["user"]},
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
                    "responses": {
                        "201": {
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
        "components": {"schemas": {}},
    }
    groups = group_references_by_pair(spec, config, {"Issue": "issues"})
    # Inline request body → property reference (issues → users)
    assert ("issues", "users") in groups
    property_hits = [
        entry for entry in groups[("issues", "users")] if entry.kind == "property"
    ]
    assert any(entry.location == "user_id" for entry in property_hits)
    # Response body → body_response reference (issues → issues, self-reference)
    assert ("issues", "issues") in groups
    body_hits = [
        entry for entry in groups[("issues", "issues")]
        if entry.kind == "body_response"
    ]
    assert len(body_hits) >= 1


def test_multiple_methods_on_same_path_walked_separately(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "paths": {
            "/users/{user_id}": {
                "get": {"responses": {"200": {"description": "ok"}}},
                "delete": {"responses": {"204": {"description": "ok"}}},
            },
        },
    }
    groups = group_references_by_pair(spec, config, {})
    entries = groups.get(("users", "users"), [])
    methods_seen = {entry.method for entry in entries}
    assert methods_seen == {"GET", "DELETE"}
