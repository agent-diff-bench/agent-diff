"""Vocabulary extraction + cache-key tests.

These tests don't touch the LLM — ``_call_alias_llm`` is the only
piece that needs network/CLI access, and it's isolated from the
pure functions exercised here. The merge/cache/lookup code is all
deterministic and unit-testable.
"""

from __future__ import annotations

import json
from pathlib import Path

from fk_pipeline.vocabulary import (
    PROMPT_VERSION,
    _build_lookup,
    _merge_aliases,
    compute_cache_key,
    extract_candidate_vocabulary,
    load_cached_vocabulary,
    write_vocabulary_artifact,
)

from .conftest import make_spec


def test_extract_vocabulary_from_url_segments():
    spec = make_spec(
        {
            "/projects": {"get": {"responses": {}}},
            "/projects/{id}/tasks": {"get": {"responses": {}}},
        }
    )
    vocab = extract_candidate_vocabulary(spec)
    assert "projects" in vocab
    assert "tasks" in vocab


def test_vocabulary_ignore_tokens_filters_post_tokenization():
    """Token patterns catch tokens that the pre-tokenize filter misses.

    The motivating case: example values in OpenAPI often contain
    hashes embedded in URLs like
    ``https://api.github.com/repos/octocat/example/git/blobs/a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15``.
    The ``ignore_value_patterns`` filter can't catch the hash because
    the URL as a whole doesn't match a hash pattern. But once
    ``tokenize`` splits the URL on ``/`` and ``.``, the hash pops
    out as a single long token that a post-tokenize filter can drop.
    """
    url_with_hash = (
        "https://api.github.com/repos/octocat/example/git/blobs/"
        "a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15"
    )
    spec = make_spec(
        {
            "/projects/{id}": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "url": {
                                                "type": "string",
                                                "examples": [url_with_hash],
                                            },
                                            "assignee": {"type": "string"},
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    )

    # Pre-tokenize filter alone can't catch the hash — the URL
    # doesn't fullmatch the hash pattern.
    value_only = extract_candidate_vocabulary(
        spec,
        ignore_value_patterns=[
            r"^[a-zA-Z0-9]{31,}$",       # standalone hashes / opaque IDs
        ],
    )
    assert "a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15" in value_only, (
        "sanity: pre-tokenize filter shouldn't catch URL-embedded hashes"
    )

    # Post-tokenize filter catches it.
    filtered = extract_candidate_vocabulary(
        spec,
        ignore_token_patterns=[
            r"^[a-zA-Z0-9]{31,}$",       # hashes that pop out of URLs
        ],
    )
    assert "a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15" not in filtered
    # Real signals still present.
    assert "projects" in filtered
    assert "assignee" in filtered
    assert "repos" in filtered  # tokenized out of the URL


def test_vocabulary_ignore_values_filters_raw_strings_pre_lowercase():
    """Value patterns match against raw (not lowercased) strings.

    Three cases pinned down here:

      * ``ALL_CAPS`` enum values (``OPEN``, ``CLOSED``) are skipped
        via ``^[A-Z][A-Z0-9_]*$``. Because the match happens BEFORE
        ``tokenize`` lowercases, the pattern can see the original
        case.
      * Hash-shaped opaque IDs (40-char hex) are skipped via
        ``^[a-zA-Z0-9]{31,}$``.
      * Legitimate schema property names (``assignee``) and URL
        tokens (``projects``) survive both filters.
    """
    spec = make_spec(
        {
            "/projects/{project_id}": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "assignee": {"type": "string"},
                                            "state": {
                                                "type": "string",
                                                "enum": ["OPEN", "CLOSED"],
                                            },
                                            "commit_sha": {
                                                "type": "string",
                                                "example": "a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15",
                                            },
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    )

    unfiltered = extract_candidate_vocabulary(spec)
    # Without the filter, lowercased enum values and the hash both
    # leak into the vocabulary.
    assert "open" in unfiltered
    assert "closed" in unfiltered
    assert "a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15" in unfiltered

    filtered = extract_candidate_vocabulary(
        spec,
        ignore_value_patterns=[
            r"^[A-Z][A-Z0-9_]*$",       # ALL_CAPS enums / constants
            r"^[a-zA-Z0-9]{31,}$",       # hashes / long opaque IDs
        ],
    )
    assert "open" not in filtered
    assert "closed" not in filtered
    assert "a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15" not in filtered
    # Real signal survives.
    assert "projects" in filtered
    assert "assignee" in filtered


def test_vocabulary_ignore_keys_skips_matching_subtrees():
    """Keys matching ``ignore_key_patterns`` contribute nothing.

    Not only is the key itself not tokenized, the walker skips its
    entire value subtree — which is the whole point: we want to be
    able to tell the extractor "don't even look at descriptions"
    so we never pay the cost of tokenizing prose.
    """
    spec = make_spec(
        {
            "/projects/{project_id}": {
                "get": {
                    "description": "List all projects and their assignees",
                    "summary": "Get project details",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "description": "A project object",
                                        "properties": {
                                            "owner": {"type": "string"},
                                        },
                                    }
                                }
                            }
                        }
                    },
                }
            }
        }
    )

    # Without the filter, the description prose contributes tokens
    # like ``list``, ``assignees``, ``details`` (some stoplisted,
    # some not).
    unfiltered = extract_candidate_vocabulary(spec)
    assert "assignees" in unfiltered  # from the description string
    assert "projects" in unfiltered
    assert "owner" in unfiltered

    # With ``^description$`` / ``^summary$`` ignored, the prose
    # tokens disappear but real signals remain.
    filtered = extract_candidate_vocabulary(
        spec, ignore_key_patterns=[r"^description$", r"^summary$"]
    )
    assert "assignees" not in filtered
    assert "projects" in filtered  # still caught via URL segments
    assert "owner" in filtered  # still caught via the properties walk


def test_vocabulary_includes_path_parameter_names():
    """Path parameter names contribute to the candidate vocabulary.

    ``{owner}`` contributes ``owner``, ``{gist_id}`` contributes both
    ``gist_id`` and ``gist`` (the ``id`` part is dropped by the
    stoplist). Without this the LLM can't classify ``owner`` as an
    alias for ``users`` — path params are sometimes the only place
    an alias word appears.
    """
    spec = make_spec(
        {
            "/repos/{owner}/{repo}": {"get": {"responses": {}}},
            "/gists/{gist_id}": {"get": {"responses": {}}},
        }
    )
    vocab = extract_candidate_vocabulary(spec)
    assert "owner" in vocab
    assert "repo" in vocab
    assert "gist" in vocab
    # The composite ``gist_id`` also comes through — the stoplist
    # drops ``id`` but not compound forms.
    assert "gist_id" in vocab
    assert "id" not in vocab  # stoplisted part of ``gist_id``


def test_vocabulary_stoplist_drops_verbs():
    """Action verbs like 'archive' never end up in candidate vocabulary."""
    spec = make_spec(
        {
            "/projects/{id}/archive": {"post": {"responses": {}}},
        }
    )
    vocab = extract_candidate_vocabulary(spec)
    assert "projects" in vocab
    assert "archive" not in vocab  # filtered by stoplist


def test_vocabulary_from_schema_names_snake_case():
    """Component schema names are snake-cased before tokenizing.

    The tokenizer emits both the compound form and its underscore
    parts, so ``UserProfile`` yields ``user_profile`` (the compound
    form the LLM uses for alias matching) alongside ``user`` and
    ``profile`` (the decomposed stems that help path-param names
    like ``{gist_id}`` contribute ``gist`` to the vocabulary).
    Only the compound form is load-bearing for this test.
    """
    spec = make_spec(
        {"/x": {"get": {"responses": {}}}},
        schemas={
            "UserProfile": {"type": "object"},
            "Organization": {"type": "object"},
        },
    )
    vocab = extract_candidate_vocabulary(spec)
    assert "user_profile" in vocab
    assert "organization" in vocab


def test_vocabulary_from_response_top_level_props():
    """Response body top-level property names feed the candidate pool."""
    spec = make_spec(
        {
            "/issues/{id}": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Issue"}
                                }
                            }
                        }
                    }
                }
            }
        },
        schemas={
            "Issue": {
                "type": "object",
                "properties": {
                    "assignee": {"type": "string"},
                    "labels": {"type": "array"},
                },
            }
        },
    )
    vocab = extract_candidate_vocabulary(spec)
    assert "issues" in vocab
    assert "assignee" in vocab
    assert "labels" in vocab


def test_cache_key_stable_and_order_independent():
    """Changing input order must not change the cache key."""
    a = compute_cache_key(
        resources=["a", "b", "c"],
        vocabulary=["x", "y", "z"],
        pinned_aliases={"alpha": "a"},
        model="claude-haiku-4-5",
        prompt_version="v1",
    )
    b = compute_cache_key(
        resources=["c", "b", "a"],
        vocabulary=["z", "x", "y"],
        pinned_aliases={"alpha": "a"},
        model="claude-haiku-4-5",
        prompt_version="v1",
    )
    assert a == b


def test_cache_key_changes_with_any_input():
    base = compute_cache_key(
        resources=["a", "b"],
        vocabulary=["x"],
        pinned_aliases={},
        model="claude-haiku-4-5",
        prompt_version="v1",
    )
    assert base != compute_cache_key(
        resources=["a", "b", "c"], vocabulary=["x"], pinned_aliases={},
        model="claude-haiku-4-5", prompt_version="v1",
    )
    assert base != compute_cache_key(
        resources=["a", "b"], vocabulary=["x", "y"], pinned_aliases={},
        model="claude-haiku-4-5", prompt_version="v1",
    )
    assert base != compute_cache_key(
        resources=["a", "b"], vocabulary=["x"], pinned_aliases={"al": "a"},
        model="claude-haiku-4-5", prompt_version="v1",
    )
    assert base != compute_cache_key(
        resources=["a", "b"], vocabulary=["x"], pinned_aliases={},
        model="other-model", prompt_version="v1",
    )
    assert base != compute_cache_key(
        resources=["a", "b"], vocabulary=["x"], pinned_aliases={},
        model="claude-haiku-4-5", prompt_version="v2",
    )


def test_merge_aliases_pinned_wins_and_llm_cannot_override():
    """A pinned alias cannot be stolen by the LLM."""
    merged = _merge_aliases(
        resources=["repos", "orgs"],
        vocabulary=["repository", "organization", "widget"],
        pinned={"repository": "repos"},
        llm_aliases={
            "repos": [],
            "orgs": ["organization", "repository"],  # LLM tries to steal 'repository'
        },
        cache_key="k",
    )
    repos = merged.entries["repos"]
    orgs = merged.entries["orgs"]
    assert "repository" in repos.syntactic_aliases
    assert "repository" not in orgs.syntactic_aliases
    assert "organization" in orgs.syntactic_aliases
    # Widget is unmatched — no canonical claimed it.
    assert "widget" in merged.unmatched_vocabulary


def test_merge_aliases_canonical_implicit():
    """A resource's canonical/singular form is implicitly claimed."""
    merged = _merge_aliases(
        resources=["projects"],
        vocabulary=["projects", "project", "something"],
        pinned={},
        llm_aliases={"projects": ["project", "something"]},
        cache_key="k",
    )
    # The canonical plural and its singular are NOT listed in the
    # alias set (they're implicit), but both DO end up in the lookup.
    assert merged.lookup.get("projects") == "projects"
    assert merged.lookup.get("project") == "projects"
    assert merged.lookup.get("something") == "projects"


def test_cache_roundtrip(tmp_path: Path):
    """Write then load reconstructs the same AliasMap."""
    from fk_pipeline.vocabulary import ResourceAliasEntry, AliasMap

    entries = {
        "projects": ResourceAliasEntry(
            canonical="projects", singular="project",
            syntactic_aliases=["project"], pinned_by_user=False, source="llm",
        ),
    }
    alias_map = AliasMap(
        entries=entries,
        lookup=_build_lookup(entries),
        unmatched_vocabulary=["widget"],
        cache_key="k1",
        cache_hit=False,
    )
    cache_path = tmp_path / "resource_vocabulary.json"
    write_vocabulary_artifact(
        alias_map,
        cache_path,
        source_spec="/nowhere",
        model="claude-haiku-4-5",
        vocabulary_size=42,
    )
    assert cache_path.exists()
    loaded = load_cached_vocabulary(cache_path, expected_key="k1")
    assert loaded is not None
    assert loaded.cache_hit is True
    assert "project" in loaded.entries["projects"].syntactic_aliases
    assert loaded.unmatched_vocabulary == ["widget"]


def test_cache_miss_on_key_mismatch(tmp_path: Path):
    """Loading with the wrong key returns None (cache invalidation)."""
    from fk_pipeline.vocabulary import ResourceAliasEntry, AliasMap

    entries = {
        "projects": ResourceAliasEntry(
            canonical="projects", singular="project",
            syntactic_aliases=[], pinned_by_user=False, source="llm",
        ),
    }
    alias_map = AliasMap(
        entries=entries,
        lookup=_build_lookup(entries),
        unmatched_vocabulary=[],
        cache_key="old-key",
        cache_hit=False,
    )
    cache_path = tmp_path / "resource_vocabulary.json"
    write_vocabulary_artifact(
        alias_map, cache_path,
        source_spec="/nowhere", model="claude-haiku-4-5", vocabulary_size=0,
    )
    # Different key → cache miss.
    assert load_cached_vocabulary(cache_path, expected_key="new-key") is None


def test_cache_miss_on_missing_file(tmp_path: Path):
    assert load_cached_vocabulary(tmp_path / "nope.json", expected_key="k") is None


def test_build_lookup_includes_singular_and_aliases():
    from fk_pipeline.vocabulary import ResourceAliasEntry
    entries = {
        "repos": ResourceAliasEntry(
            canonical="repos", singular="repo",
            syntactic_aliases=["repository", "repositories"],
            pinned_by_user=True, source="user_config",
        ),
    }
    lookup = _build_lookup(entries)
    assert lookup["repos"] == "repos"
    assert lookup["repo"] == "repos"
    assert lookup["repository"] == "repos"
    assert lookup["repositories"] == "repos"


def test_prompt_version_constant():
    """Sanity check — the prompt version is a non-empty string."""
    assert isinstance(PROMPT_VERSION, str) and PROMPT_VERSION
