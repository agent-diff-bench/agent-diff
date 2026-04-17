"""Tests for the path-level alias gap identification step.

Each test builds a minimal yaml config + inline spec dict and asserts
on the ``ReviewBucket`` returned by ``find_unresolved_path_tokens``.
The helper ``_build_config`` writes a throwaway yaml + stub spec file
into ``tmp_path`` so ``load_config`` has something valid to parse —
the actual spec the walker sees is passed as a dict literal separate
from the file.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from pipeline.alias_gaps_identification import (
    ReviewBucket,
    UnresolvedCandidate,
    find_unresolved_path_tokens,
    write_review_bucket,
)
from pipeline.config import PipelineConfig, load_config


def _build_config(
    tmp_path: Path,
    *,
    resources: dict[str, Any],
    vocabulary: dict[str, Any] | None = None,
    naming: dict[str, Any] | None = None,
) -> PipelineConfig:
    """Write a minimal yaml config + stub spec to tmp_path and load it."""
    cfg_path = tmp_path / "app.yaml"
    spec_path = tmp_path / "spec.json"
    spec_path.write_text('{"paths": {}, "components": {"schemas": {}}}')
    cfg_data: dict[str, Any] = {
        "app_slug": "test",
        "app_name": "Test",
        "openapi_path": "spec.json",
        "target_dir": "out",
        "resources": resources,
    }
    if vocabulary is not None:
        cfg_data["vocabulary"] = vocabulary
    if naming is not None:
        cfg_data["naming"] = naming
    cfg_path.write_text(yaml.safe_dump(cfg_data))
    return load_config(cfg_path)


# ---------------------------------------------------------------------------
# Empty / fully resolved cases — no gaps
# ---------------------------------------------------------------------------


def test_empty_spec_produces_empty_bucket(tmp_path: Path) -> None:
    """No paths → zero candidates."""
    config = _build_config(tmp_path, resources={"users": {"aliases": []}})
    spec = {"paths": {}, "components": {"schemas": {}}}
    bucket = find_unresolved_path_tokens(spec, config)
    assert bucket.candidates == []


def test_fully_resolved_path_emits_nothing(tmp_path: Path) -> None:
    """Every URL segment and every parameter hits an alias → empty bucket."""
    config = _build_config(
        tmp_path,
        resources={
            "users": {"aliases": ["user", "owner"]},
            "repos": {"aliases": ["repo"]},
        },
    )
    # Every token here resolves after config-load-time expansion:
    #   'repos'   → canonical
    #   'owner'   → users alias
    #   'repo_id' → repos alias via _id expansion
    spec = {
        "paths": {
            "/repos/{owner}/{repo_id}": {
                "parameters": [
                    {"name": "owner", "in": "path", "required": True},
                    {"name": "repo_id", "in": "path", "required": True},
                ],
                "get": {"responses": {"200": {"description": "ok"}}},
            }
        },
        "components": {"schemas": {}},
    }
    bucket = find_unresolved_path_tokens(spec, config)
    assert bucket.candidates == []


# ---------------------------------------------------------------------------
# URL-segment and parameter misses
# ---------------------------------------------------------------------------


def test_url_segment_miss_produces_candidate(tmp_path: Path) -> None:
    """A URL segment with no matching alias lands in the bucket."""
    config = _build_config(
        tmp_path,
        resources={
            "users": {"aliases": ["user", "owner"]},
            "repos": {"aliases": ["repo"]},
        },
    )
    spec = {
        "paths": {
            "/repos/{owner}/{repo}/labels": {
                "get": {"responses": {"200": {"description": "ok"}}},
            }
        },
        "components": {"schemas": {}},
    }
    bucket = find_unresolved_path_tokens(spec, config)
    assert len(bucket.candidates) == 1
    candidate = bucket.candidates[0]
    assert candidate.token == "labels"
    assert candidate.judgement is None
    assert len(candidate.excerpts) == 1
    assert candidate.excerpts[0]["path"] == "/repos/{owner}/{repo}/labels"
    # Path-level excerpt shape (no method, has path_item).
    assert "path_item" in candidate.excerpts[0]
    assert "method" not in candidate.excerpts[0]


# ---------------------------------------------------------------------------
# Compound-hit short-circuit vs. partial-compound split fallback
# ---------------------------------------------------------------------------


def test_compound_hit_short_circuits_split_fallback(tmp_path: Path) -> None:
    """A compound token that resolves via alias expansion must not be split.

    If the walker naively split ``pull_request_id`` into ``pull``,
    ``request``, ``id`` and tried to resolve each, ``request`` would
    wrongly land in the bucket even though the config-time alias
    expansion already put ``pull_request_id`` in ``aliases_lookup``.
    """
    config = _build_config(
        tmp_path,
        resources={
            "pulls": {"aliases": ["pull", "pull_request"]},
        },
    )
    spec = {
        "paths": {
            "/pulls/{pull_request_id}": {
                "get": {
                    "parameters": [
                        {"name": "pull_request_id", "in": "path", "required": True},
                    ],
                    "responses": {"200": {"description": "ok"}},
                },
            }
        },
        "components": {"schemas": {}},
    }
    bucket = find_unresolved_path_tokens(spec, config)
    assert bucket.candidates == []


def test_partial_compound_miss_emits_only_missing_part(tmp_path: Path) -> None:
    """If only one piece of a compound token misses, only that piece is emitted.

    ``pull_number`` splits into ``pull`` + ``number``. ``pull`` is a
    configured alias and resolves; ``number`` doesn't resolve (GitHub
    uses numeric identifiers on PRs but the config doesn't know that).
    Only ``number`` should land in the bucket.
    """
    config = _build_config(
        tmp_path,
        resources={"pulls": {"aliases": ["pull"]}},
    )
    spec = {
        "paths": {
            "/pulls/{pull_number}": {
                "get": {
                    "parameters": [
                        {"name": "pull_number", "in": "path", "required": True},
                    ],
                    "responses": {"200": {"description": "ok"}},
                },
            }
        },
        "components": {"schemas": {}},
    }
    bucket = find_unresolved_path_tokens(spec, config)
    tokens = {c.token for c in bucket.candidates}
    assert "number" in tokens
    assert "pull" not in tokens  # resolves, must not appear as a gap
    assert "pulls" not in tokens  # canonical, must not appear as a gap


# ---------------------------------------------------------------------------
# Parameter $ref handling (deferred)
# ---------------------------------------------------------------------------


def test_parameter_ref_is_silently_skipped(tmp_path: Path) -> None:
    """A ``$ref`` parameter has no local ``name`` — walker skips without crashing."""
    config = _build_config(
        tmp_path,
        resources={"users": {"aliases": ["user", "owner"]}},
    )
    spec = {
        "paths": {
            "/users/{owner}": {
                "parameters": [
                    {"$ref": "#/components/parameters/Owner"},
                ],
                "get": {"responses": {"200": {"description": "ok"}}},
            }
        },
        "components": {
            "schemas": {},
            "parameters": {
                "Owner": {"name": "owner", "in": "path", "required": True},
            },
        },
    }
    bucket = find_unresolved_path_tokens(spec, config)
    # The path string itself contains ``{owner}`` which is tokenized
    # to ``owner`` and hits the users alias — so the path is fully
    # resolved despite the $ref parameter being skipped.
    assert bucket.candidates == []


# ---------------------------------------------------------------------------
# Vocabulary filters
# ---------------------------------------------------------------------------


def test_vocabulary_ignore_tokens_suppresses_bucket_entry(tmp_path: Path) -> None:
    """A token matching ``ignore_tokens`` never enters the bucket."""
    config = _build_config(
        tmp_path,
        resources={"repos": {"aliases": ["repo"]}},
        vocabulary={"ignore_tokens": [r"^archive$"]},
    )
    spec = {
        "paths": {
            "/repos/{repo}/archive": {
                "post": {"responses": {"200": {"description": "ok"}}},
            }
        },
        "components": {"schemas": {}},
    }
    bucket = find_unresolved_path_tokens(spec, config)
    assert bucket.candidates == []


def test_vocabulary_ignore_values_applies_to_raw_case(tmp_path: Path) -> None:
    """``ignore_values`` matches the raw string before normalization.

    Pattern ``^[A-Z][A-Z0-9_]*$`` targets ALL_CAPS strings. This is
    only possible BEFORE ``normalize_identifier`` lowercases the
    input — which is exactly what the walker does.
    """
    config = _build_config(
        tmp_path,
        resources={"users": {"aliases": ["user"]}},
        vocabulary={"ignore_values": [r"^[A-Z][A-Z0-9_]*$"]},
    )
    spec = {
        "paths": {
            "/users/{HTTP_PROXY}": {
                "parameters": [
                    {"name": "HTTP_PROXY", "in": "path", "required": True},
                ],
                "get": {"responses": {"200": {"description": "ok"}}},
            }
        },
        "components": {"schemas": {}},
    }
    bucket = find_unresolved_path_tokens(spec, config)
    # ``HTTP_PROXY`` raw-matches the ALL_CAPS pattern and is dropped
    # before normalization. The path string walk also sees it inside
    # ``{HTTP_PROXY}`` after brace strip, and the filter catches it
    # there too. No gaps.
    assert bucket.candidates == []


# ---------------------------------------------------------------------------
# Excerpt accumulation and deduplication
# ---------------------------------------------------------------------------


def test_same_token_on_multiple_paths_keeps_excerpts_together(tmp_path: Path) -> None:
    """One unresolved token seen on two different paths → one candidate, two excerpts."""
    config = _build_config(
        tmp_path,
        resources={
            "users": {"aliases": ["user"]},
            "teams": {"aliases": ["team"]},
        },
    )
    spec = {
        "paths": {
            "/users/{user_id}/notifications": {
                "get": {"responses": {"200": {"description": "ok"}}},
            },
            "/teams/{team_id}/notifications": {
                "get": {"responses": {"200": {"description": "ok"}}},
            },
        },
        "components": {"schemas": {}},
    }
    bucket = find_unresolved_path_tokens(spec, config)
    notifications = next(
        c for c in bucket.candidates if c.token == "notifications"
    )
    assert len(notifications.excerpts) == 2
    paths = {excerpt["path"] for excerpt in notifications.excerpts}
    assert paths == {
        "/users/{user_id}/notifications",
        "/teams/{team_id}/notifications",
    }


def test_within_path_dedup_collapses_identical_excerpts(tmp_path: Path) -> None:
    """Same token emitted by two path-level sources dedupes to one excerpt.

    Both the path string segment tokenizer and the path-level
    parameter walker emit with the SAME path-level excerpt. The
    hash-based dedup collapses them to one stored copy.
    """
    config = _build_config(
        tmp_path,
        resources={"users": {"aliases": ["user"]}},
    )
    spec = {
        "paths": {
            "/notifications": {
                "parameters": [
                    {"name": "notifications", "in": "query"},
                ],
                "get": {"responses": {"200": {"description": "ok"}}},
            },
        },
        "components": {"schemas": {}},
    }
    bucket = find_unresolved_path_tokens(spec, config)
    notifications = next(
        c for c in bucket.candidates if c.token == "notifications"
    )
    assert len(notifications.excerpts) == 1


# ---------------------------------------------------------------------------
# Operation-level excerpt shape
# ---------------------------------------------------------------------------


def test_operation_level_parameter_uses_merged_excerpt(tmp_path: Path) -> None:
    """An operation-level parameter's excerpt merges path_level and the specific operation."""
    config = _build_config(
        tmp_path,
        resources={"repos": {"aliases": ["repo"]}},
    )
    spec = {
        "paths": {
            "/repos/{repo}": {
                "summary": "shared summary",
                "parameters": [
                    {"name": "repo", "in": "path", "required": True},
                ],
                "get": {
                    "parameters": [
                        {"name": "milestone", "in": "query"},
                    ],
                    "responses": {"200": {"description": "ok"}},
                },
                "post": {
                    "responses": {"200": {"description": "created"}},
                },
            }
        },
        "components": {"schemas": {}},
    }
    bucket = find_unresolved_path_tokens(spec, config)
    milestone = next(c for c in bucket.candidates if c.token == "milestone")
    assert len(milestone.excerpts) == 1
    excerpt = milestone.excerpts[0]
    # Merged-excerpt shape.
    assert excerpt["path"] == "/repos/{repo}"
    assert excerpt["method"] == "GET"
    assert "path_level" in excerpt
    assert "operation" in excerpt
    # path_level carries shared stuff but NOT the HTTP verb blocks.
    assert "summary" in excerpt["path_level"]
    assert "parameters" in excerpt["path_level"]
    assert "get" not in excerpt["path_level"]
    assert "post" not in excerpt["path_level"]
    # operation is the specific GET block.
    assert excerpt["operation"]["parameters"][0]["name"] == "milestone"


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


def test_write_review_bucket_roundtrip(tmp_path: Path) -> None:
    """JSON serialization produces the expected shape and re-reads cleanly."""
    bucket = ReviewBucket(candidates=[
        UnresolvedCandidate(
            token="labels",
            excerpts=[
                {"path": "/repos/{owner}/{repo}/labels", "path_item": {}},
            ],
            judgement=None,
        ),
    ])
    output_path = tmp_path / "pipeline_out" / "gap_paths.json"
    write_review_bucket(
        bucket,
        output_path,
        config_path=tmp_path / "app.yaml",
        spec_path=tmp_path / "spec.json",
    )
    assert output_path.exists()
    data = json.loads(output_path.read_text())
    # _meta shape
    assert data["_meta"]["candidate_count"] == 1
    assert data["_meta"]["config_path"] is not None
    assert data["_meta"]["spec_path"] is not None
    assert "generated_at" in data["_meta"]
    # candidates shape
    assert len(data["candidates"]) == 1
    entry = data["candidates"][0]
    assert entry["token"] == "labels"
    assert entry["judgement"] is None  # always emitted, never omitted
    assert entry["excerpts"][0]["path"] == "/repos/{owner}/{repo}/labels"


def test_write_review_bucket_preserves_populated_judgement(tmp_path: Path) -> None:
    """If a bucket carries a non-null judgement, the writer emits it verbatim.

    Future milestones will populate ``judgement`` with LLM output.
    This test pins down that the writer doesn't blindly overwrite it.
    """
    bucket = ReviewBucket(candidates=[
        UnresolvedCandidate(
            token="archive",
            excerpts=[{"path": "/projects/{id}/archive", "path_item": {}}],
            judgement={"status": "reject", "reason": "action verb, not a resource"},
        ),
    ])
    output_path = tmp_path / "pipeline_out" / "gap_paths.json"
    write_review_bucket(bucket, output_path)
    data = json.loads(output_path.read_text())
    entry = data["candidates"][0]
    assert entry["judgement"] == {
        "status": "reject",
        "reason": "action verb, not a resource",
    }
