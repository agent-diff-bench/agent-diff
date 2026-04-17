"""Property-level reference extractor (Group C).

Walks a schema tree and emits hits at object property nodes via
two signals: the property name (normalized, optional qualifier
prefix strip, then looked up in ``aliases_lookup``) and the
property value when it is a ``$ref`` to a Group D bound schema.
Descends through inline ``properties``, ``items``,
``additionalProperties``, and composition branches. If
``component_schemas`` is given, ``$ref``s are also followed into
their target schemas with a visited-set cycle guard; pass
``start_schema_name`` to pre-seed visited so self-refs don't loop.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from pipeline._text import normalize_identifier
from pipeline.config import PipelineConfig

_SCHEMA_PREFIX = "#/components/schemas/"


@dataclass(frozen=True)
class PropertyReference:
    token: str
    resource: str
    path: tuple[str, ...]


def find_property_references(
    schema: dict[str, Any],
    config: PipelineConfig,
    bindings: Mapping[str, str],
    component_schemas: Mapping[str, Any] | None = None,
    start_schema_name: str | None = None,
) -> list[PropertyReference]:
    aliases_lookup = config.resources.aliases_lookup
    qualifier_prefixes = config.naming.qualifier_prefixes
    schemas = component_schemas or {}
    visited: set[str] = {start_schema_name} if start_schema_name else set()
    seen: set[tuple[str, str, tuple[str, ...]]] = set()
    references: list[PropertyReference] = []

    def record(token: str, resource: str, path: tuple[str, ...]) -> None:
        key = (token, resource, path)
        if key in seen:
            return
        seen.add(key)
        references.append(PropertyReference(token, resource, path))

    def resolve_name(name: str) -> str | None:
        hit = aliases_lookup.get(normalize_identifier(name))
        if hit is not None:
            return hit
        for prefix in qualifier_prefixes:
            if name.startswith(prefix):
                hit = aliases_lookup.get(normalize_identifier(name[len(prefix):]))
                if hit is not None:
                    return hit
        return None

    def walk(node: Any, path: tuple[str, ...]) -> None:
        if not isinstance(node, dict):
            return
        ref_at_top = node.get("$ref")
        if isinstance(ref_at_top, str) and ref_at_top.startswith(_SCHEMA_PREFIX):
            target_name = ref_at_top[len(_SCHEMA_PREFIX):]
            target_resource = bindings.get(target_name)
            if target_resource is not None and path:
                record(path[-1], target_resource, path)
            if target_name not in visited:
                target_schema = schemas.get(target_name)
                if isinstance(target_schema, dict):
                    visited.add(target_name)
                    walk(target_schema, path)
            return
        for name, child in (node.get("properties") or {}).items():
            if not isinstance(name, str):
                continue
            child_path = path + (name,)
            hit = resolve_name(name)
            if hit is not None:
                record(name, hit, child_path)
            if isinstance(child, dict):
                walk(child, child_path)
        items = node.get("items")
        if isinstance(items, dict):
            walk(items, path)
        additional = node.get("additionalProperties")
        if isinstance(additional, dict):
            walk(additional, path)
        for key in ("allOf", "oneOf", "anyOf"):
            for branch in node.get(key) or []:
                walk(branch, path)

    walk(schema, ())
    return references
