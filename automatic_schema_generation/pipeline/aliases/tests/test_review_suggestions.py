"""Tests for the LLM review layer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from pipeline.config import PipelineConfig, load_config
from pipeline.aliases.review import (
    ReviewedSuggestion,
    format_approved_aliases_yaml,
    review_suggestions,
)
from pipeline.aliases.suggest import Suggestion


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


def _make_suggestion(name: str, resource: str, count: int = 10) -> Suggestion:
    return Suggestion(
        schema_name=name,
        normalized=name.replace("-", "_"),
        matched_token="repository",
        target_resource=resource,
        ref_count=count,
    )


def test_calls_llm_per_resource_and_parses_verdicts(tmp_path: Path) -> None:
    config = _config(tmp_path, {"repos": {"aliases": ["repository"]}})
    spec = {
        "components": {
            "schemas": {
                "full-repository": {"type": "object"},
                "repository-ruleset": {"type": "object"},
            },
        },
    }
    suggestions = {
        "repos": [
            _make_suggestion("full-repository", "repos", 19),
            _make_suggestion("repository-ruleset", "repos", 5),
        ],
    }

    calls: list[str] = []

    def fake_llm(prompt: str) -> str:
        calls.append(prompt)
        return json.dumps([
            {"schema_name": "full-repository", "verdict": "variant", "reason": "alternate view of repository"},
            {"schema_name": "repository-ruleset", "verdict": "distinct", "reason": "separate concept"},
        ])

    result = review_suggestions(suggestions, spec, config, fake_llm)
    assert len(calls) == 1
    assert "repos" in result
    verdicts = {entry.suggestion.schema_name: entry.verdict for entry in result["repos"]}
    assert verdicts["full-repository"] == "variant"
    assert verdicts["repository-ruleset"] == "distinct"


def test_missing_verdict_defaults_to_uncertain(tmp_path: Path) -> None:
    """If the LLM doesn't return a verdict for a schema, we fall back to uncertain."""
    config = _config(tmp_path, {"repos": {"aliases": ["repository"]}})
    spec = {"components": {"schemas": {"full-repository": {"type": "object"}}}}
    suggestions = {"repos": [_make_suggestion("full-repository", "repos")]}

    def fake_llm(prompt: str) -> str:
        return "[]"  # LLM returned nothing

    result = review_suggestions(suggestions, spec, config, fake_llm)
    assert result["repos"][0].verdict == "uncertain"


def test_cache_skips_llm_on_rerun(tmp_path: Path) -> None:
    """A second run with the same inputs should not call the LLM at all."""
    config = _config(tmp_path, {"repos": {"aliases": ["repository"]}})
    spec = {"components": {"schemas": {"full-repository": {"type": "object"}}}}
    suggestions = {"repos": [_make_suggestion("full-repository", "repos")]}
    cache_path = tmp_path / "cache.json"

    call_count = 0

    def fake_llm(prompt: str) -> str:
        nonlocal call_count
        call_count += 1
        return json.dumps([
            {"schema_name": "full-repository", "verdict": "variant", "reason": "alt view"},
        ])

    review_suggestions(suggestions, spec, config, fake_llm, cache_path=cache_path)
    assert call_count == 1
    assert cache_path.exists()

    # Second run — cache hit, no LLM call.
    review_suggestions(suggestions, spec, config, fake_llm, cache_path=cache_path)
    assert call_count == 1


def test_response_with_extra_prose_still_parses(tmp_path: Path) -> None:
    """Claude sometimes wraps JSON in prose. We extract the first [...] block."""
    config = _config(tmp_path, {"repos": {"aliases": ["repository"]}})
    spec = {"components": {"schemas": {"full-repository": {"type": "object"}}}}
    suggestions = {"repos": [_make_suggestion("full-repository", "repos")]}

    def fake_llm(prompt: str) -> str:
        return 'Sure, here are the verdicts:\n\n[{"schema_name": "full-repository", "verdict": "variant", "reason": "alt view"}]\n\nHope this helps!'

    result = review_suggestions(suggestions, spec, config, fake_llm)
    assert result["repos"][0].verdict == "variant"


def test_malformed_response_yields_uncertain(tmp_path: Path) -> None:
    config = _config(tmp_path, {"repos": {"aliases": ["repository"]}})
    spec = {"components": {"schemas": {"full-repository": {"type": "object"}}}}
    suggestions = {"repos": [_make_suggestion("full-repository", "repos")]}

    def fake_llm(prompt: str) -> str:
        return "not json at all"

    result = review_suggestions(suggestions, spec, config, fake_llm)
    assert result["repos"][0].verdict == "uncertain"


def test_format_approved_aliases_yaml_only_variants(tmp_path: Path) -> None:
    reviewed = {
        "repos": [
            ReviewedSuggestion(
                suggestion=_make_suggestion("full-repository", "repos", 19),
                verdict="variant",
                reason="alternate view",
            ),
            ReviewedSuggestion(
                suggestion=_make_suggestion("repository-ruleset", "repos", 5),
                verdict="distinct",
                reason="separate concept",
            ),
            ReviewedSuggestion(
                suggestion=_make_suggestion("weird-thing", "repos", 2),
                verdict="uncertain",
                reason="unclear",
            ),
        ],
    }
    output = format_approved_aliases_yaml(reviewed)
    assert "- full_repository" in output
    assert "repository_ruleset" not in output
    assert "weird_thing" not in output


def test_format_approved_aliases_yaml_with_uncertain_included(tmp_path: Path) -> None:
    reviewed = {
        "repos": [
            ReviewedSuggestion(
                suggestion=_make_suggestion("weird-thing", "repos", 2),
                verdict="uncertain",
                reason="unclear",
            ),
        ],
    }
    output = format_approved_aliases_yaml(reviewed, include_uncertain=True)
    assert "# - weird_thing" in output
    assert "uncertain" in output
