"""Tests for the deterministic alias suggester."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pipeline.config import PipelineConfig, load_config
from pipeline.aliases.suggest import (
    Suggestion,
    format_suggestions_yaml,
    suggest_aliases,
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


def test_empty_spec_returns_nothing(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    assert suggest_aliases({}, config) == {}


def test_already_bound_schema_is_not_suggested(tmp_path: Path) -> None:
    """``simple-user`` binds directly via Group D, so it should not appear as a suggestion."""
    config = _config(tmp_path, {"users": {"aliases": ["user", "simple_user"]}})
    spec = {
        "paths": {
            "/users/{user_id}": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/simple-user"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {"simple-user": {"type": "object"}},
        },
    }
    assert suggest_aliases(spec, config) == {}


def test_unreferenced_schema_is_not_suggested(tmp_path: Path) -> None:
    """A schema that nobody ``$ref``s is dropped even if it would match."""
    config = _config(tmp_path, {"repos": {"aliases": ["repo", "repository"]}})
    spec = {
        "paths": {},
        "components": {
            "schemas": {"full-repository": {"type": "object"}},
        },
    }
    assert suggest_aliases(spec, config) == {}


def test_token_hit_surfaces_suggestion(tmp_path: Path) -> None:
    config = _config(tmp_path, {"repos": {"aliases": ["repo", "repository"]}})
    spec = {
        "paths": {
            "/repos/{repo}": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/full-repository"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {"full-repository": {"type": "object"}},
        },
    }
    result = suggest_aliases(spec, config)
    assert "repos" in result
    assert len(result["repos"]) == 1
    suggestion = result["repos"][0]
    assert suggestion.schema_name == "full-repository"
    assert suggestion.normalized == "full_repository"
    assert suggestion.matched_token == "repository"
    assert suggestion.target_resource == "repos"
    assert suggestion.ref_count >= 1


def test_ranking_by_ref_count(tmp_path: Path) -> None:
    """Higher ref_count comes first within a resource bucket."""
    config = _config(tmp_path, {"repos": {"aliases": ["repo", "repository"]}})
    spec = {
        "paths": {
            "/repos": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/full-repository"},
                                },
                            },
                        },
                    },
                },
            },
            "/repos/{repo}": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/full-repository"},
                                },
                            },
                        },
                    },
                },
            },
            "/repos/other": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/simple-repository"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "full-repository": {"type": "object"},
                "simple-repository": {"type": "object"},
            },
        },
    }
    result = suggest_aliases(spec, config)
    assert [s.schema_name for s in result["repos"]] == [
        "full-repository",
        "simple-repository",
    ]


def test_multi_token_hit_emits_under_multiple_resources(tmp_path: Path) -> None:
    """A schema name with tokens hitting two different resources is emitted under both."""
    config = _config(tmp_path, {
        "pulls": {"aliases": ["pull"]},
        "comments": {"aliases": ["comment"]},
    })
    spec = {
        "paths": {
            "/pulls/{pull_id}/comments": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/pull-request-review-comment"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {"pull-request-review-comment": {"type": "object"}},
        },
    }
    result = suggest_aliases(spec, config)
    assert "pulls" in result
    assert "comments" in result
    assert result["pulls"][0].matched_token == "pull"
    assert result["comments"][0].matched_token == "comment"


def test_non_matching_schema_is_ignored(tmp_path: Path) -> None:
    """A schema whose tokens don't hit any alias produces no suggestion."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "paths": {
            "/rate_limit": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/rate-limit"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {"rate-limit": {"type": "object"}},
        },
    }
    assert suggest_aliases(spec, config) == {}


def test_yaml_formatter_shape(tmp_path: Path) -> None:
    config = _config(tmp_path, {"repos": {"aliases": ["repository"]}})
    suggestions = {
        "repos": [
            Suggestion(
                schema_name="full-repository",
                normalized="full_repository",
                matched_token="repository",
                target_resource="repos",
                ref_count=19,
            ),
        ],
    }
    output = format_suggestions_yaml(suggestions)
    assert "repos:" in output
    assert "- full_repository" in output
    assert "19 refs" in output
    assert "token=repository" in output
