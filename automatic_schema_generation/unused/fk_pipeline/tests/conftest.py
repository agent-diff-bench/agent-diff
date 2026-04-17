"""Shared test helpers.

A few small factories that build the throwaway ``AliasMap`` / spec
fragments most classifier tests need. Keeping them here so each test
file focuses on the case under test, not on boilerplate.
"""

from __future__ import annotations

from typing import Any

import pytest

from fk_pipeline.config import FkNamingConfig
from fk_pipeline.vocabulary import (
    AliasMap,
    ResourceAliasEntry,
    _build_lookup,
)

# Reuse the existing pipeline's singularize (same cross-package dep as
# the production code).
from pipeline.naming import singularize


def make_alias_map(aliases: dict[str, list[str]]) -> AliasMap:
    """Build an AliasMap directly from a canonical→aliases dict.

    Skips the LLM path entirely; every word becomes a pinned
    user-config entry. This is what we'd get if the LLM returned an
    exact, clean answer.
    """
    entries: dict[str, ResourceAliasEntry] = {}
    for canonical, extras in aliases.items():
        entries[canonical] = ResourceAliasEntry(
            canonical=canonical,
            singular=singularize(canonical),
            syntactic_aliases=list(extras),
            pinned_by_user=True,
            source="user_config",
        )
    return AliasMap(
        entries=entries,
        lookup=_build_lookup(entries),
        unmatched_vocabulary=[],
        cache_key="test",
        cache_hit=False,
    )


def make_spec(paths: dict[str, dict[str, Any]], *, schemas: dict[str, Any] | None = None) -> dict[str, Any]:
    """Wrap a paths dict in the minimum OpenAPI envelope the loader needs."""
    return {
        "openapi": "3.0.0",
        "info": {"title": "test", "version": "0"},
        "paths": paths,
        "components": {"schemas": schemas or {}},
    }


def make_op(
    *,
    operation_id: str = "op",
    path_params: list[str] | None = None,
    query_params: list[str] | None = None,
    response_schema_ref: str | None = None,
    request_schema_ref: str | None = None,
) -> dict[str, Any]:
    """Build a minimal operation dict for classifier tests.

    Callers pass param names directly; we fill in ``in`` automatically.
    """
    params: list[dict[str, Any]] = []
    for name in path_params or []:
        params.append({"name": name, "in": "path", "required": True})
    for name in query_params or []:
        params.append({"name": name, "in": "query"})

    op: dict[str, Any] = {
        "operationId": operation_id,
        "parameters": params,
        "responses": {"200": {"description": "ok"}},
    }

    if response_schema_ref:
        op["responses"]["200"]["content"] = {
            "application/json": {
                "schema": {"$ref": response_schema_ref},
            }
        }
    if request_schema_ref:
        op["requestBody"] = {
            "content": {
                "application/json": {
                    "schema": {"$ref": request_schema_ref},
                }
            }
        }
    return op


@pytest.fixture
def default_naming() -> FkNamingConfig:
    return FkNamingConfig()
