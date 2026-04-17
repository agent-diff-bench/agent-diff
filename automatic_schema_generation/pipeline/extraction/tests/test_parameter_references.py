"""Tests for the non-path parameter reference extractor (Group B)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pipeline.config import PipelineConfig, load_config
from pipeline.extraction.parameter_references import (
    ParameterReference,
    find_parameter_references,
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


def test_empty_path_item_returns_nothing(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    assert find_parameter_references({}, config) == []


def test_query_parameter_hit(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    path_item = {
        "get": {
            "parameters": [
                {"name": "user_id", "in": "query"},
            ],
            "responses": {"200": {"description": "ok"}},
        },
    }
    references = find_parameter_references(path_item, config)
    assert references == [
        ParameterReference(token="user_id", resource="users", location="query"),
    ]


def test_path_parameter_is_ignored(tmp_path: Path) -> None:
    """``in: path`` is Group A's job; Group B must not emit path params."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    path_item = {
        "get": {
            "parameters": [
                {"name": "user_id", "in": "path", "required": True},
            ],
            "responses": {"200": {"description": "ok"}},
        },
    }
    assert find_parameter_references(path_item, config) == []


def test_header_and_cookie_parameters_hit(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    path_item = {
        "get": {
            "parameters": [
                {"name": "user_id", "in": "header"},
                {"name": "user", "in": "cookie"},
            ],
            "responses": {"200": {"description": "ok"}},
        },
    }
    references = find_parameter_references(path_item, config)
    locations = {reference.location for reference in references}
    assert locations == {"header", "cookie"}


def test_path_level_shared_parameters_are_walked(tmp_path: Path) -> None:
    """Parameters declared at the path item level apply to every operation."""
    config = _config(tmp_path, {"repos": {"aliases": ["repo"]}})
    path_item = {
        "parameters": [
            {"name": "repo", "in": "query"},
        ],
        "get": {"responses": {"200": {"description": "ok"}}},
    }
    references = find_parameter_references(path_item, config)
    assert len(references) == 1
    assert references[0].resource == "repos"
    assert references[0].location == "query"


def test_ref_parameter_is_silently_skipped(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    path_item = {
        "get": {
            "parameters": [
                {"$ref": "#/components/parameters/UserId"},
            ],
            "responses": {"200": {"description": "ok"}},
        },
    }
    assert find_parameter_references(path_item, config) == []


def test_non_matching_token_is_ignored(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    path_item = {
        "get": {
            "parameters": [
                {"name": "widget", "in": "query"},
            ],
            "responses": {"200": {"description": "ok"}},
        },
    }
    assert find_parameter_references(path_item, config) == []


def test_duplicate_declarations_dedup(tmp_path: Path) -> None:
    """Same (token, resource, location) declared at path + op dedupes to one."""
    config = _config(tmp_path, {"repos": {"aliases": ["repo"]}})
    path_item = {
        "parameters": [{"name": "repo", "in": "query"}],
        "get": {
            "parameters": [{"name": "repo", "in": "query"}],
            "responses": {"200": {"description": "ok"}},
        },
    }
    references = find_parameter_references(path_item, config)
    assert len(references) == 1
    assert references[0].token == "repo"
    assert references[0].location == "query"


def test_same_token_across_locations_keeps_each_entry(tmp_path: Path) -> None:
    """A token appearing in both ``query`` and ``header`` produces two entries."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    path_item = {
        "get": {
            "parameters": [
                {"name": "user_id", "in": "query"},
                {"name": "user_id", "in": "header"},
            ],
            "responses": {"200": {"description": "ok"}},
        },
    }
    references = find_parameter_references(path_item, config)
    locations = {reference.location for reference in references}
    assert locations == {"query", "header"}
