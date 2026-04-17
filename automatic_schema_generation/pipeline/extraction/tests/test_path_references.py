"""Tests for the path-level reference extractor (Group A)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pipeline.config import PipelineConfig, load_config
from pipeline.extraction.path_references import PathReference, find_path_references


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


def test_empty_path_returns_nothing(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    assert find_path_references("/", {}, config) == []


def test_url_segments_emit_resources(tmp_path: Path) -> None:
    config = _config(tmp_path, {
        "users": {"aliases": ["user", "owner"]},
        "repos": {"aliases": ["repo"]},
    })
    references = find_path_references(
        "/repos/{owner}/{repo}/labels",
        {"get": {"responses": {"200": {"description": "ok"}}}},
        config,
    )
    resources = {reference.resource for reference in references}
    assert resources == {"repos", "users"}


def test_path_parameter_compound_form_hits(tmp_path: Path) -> None:
    config = _config(tmp_path, {"repos": {"aliases": ["repo"]}})
    references = find_path_references(
        "/repos/{repo_id}",
        {
            "parameters": [
                {"name": "repo_id", "in": "path", "required": True},
            ],
            "get": {"responses": {"200": {"description": "ok"}}},
        },
        config,
    )
    sources = {(reference.resource, reference.source) for reference in references}
    assert ("repos", "url_segment") in sources
    assert ("repos", "path_parameter") in sources


def test_operation_level_parameter_walks(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    references = find_path_references(
        "/search",
        {
            "get": {
                "parameters": [
                    {"name": "user_id", "in": "path"},
                ],
                "responses": {"200": {"description": "ok"}},
            },
        },
        config,
    )
    assert any(
        reference.resource == "users" and reference.source == "path_parameter"
        for reference in references
    )


def test_ref_parameter_is_silently_skipped(tmp_path: Path) -> None:
    """A ``$ref`` parameter has no local ``name`` — walker skips without crashing.

    The URL string walk still picks up ``{owner}`` from the path, so
    ``users`` is emitted via ``url_segment`` even though the parameter
    itself was skipped.
    """
    config = _config(tmp_path, {"users": {"aliases": ["user", "owner"]}})
    references = find_path_references(
        "/users/{owner}",
        {
            "parameters": [{"$ref": "#/components/parameters/Owner"}],
            "get": {"responses": {"200": {"description": "ok"}}},
        },
        config,
    )
    resources = {reference.resource for reference in references}
    assert resources == {"users"}


def test_non_matching_token_is_ignored(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    references = find_path_references(
        "/widgets/{widget_id}",
        {"get": {"responses": {"200": {"description": "ok"}}}},
        config,
    )
    assert references == []


def test_duplicate_parameter_declarations_dedup(tmp_path: Path) -> None:
    """Same param declared at path level and operation level collapses to one."""
    config = _config(tmp_path, {"repos": {"aliases": ["repo"]}})
    references = find_path_references(
        "/repos/{repo}",
        {
            "parameters": [{"name": "repo", "in": "path"}],
            "get": {
                "parameters": [{"name": "repo", "in": "path"}],
                "responses": {"200": {"description": "ok"}},
            },
        },
        config,
    )
    entries = [
        (reference.token, reference.resource, reference.source)
        for reference in references
    ]
    assert ("repo", "repos", "url_segment") in entries
    assert ("repo", "repos", "path_parameter") in entries
    assert entries.count(("repo", "repos", "path_parameter")) == 1
