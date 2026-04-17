"""Path-level reference extractor (Group A).

Walks an operation's URL path and declared path parameters, and
returns every token that hits ``config.resources.aliases_lookup``.
Assumes config aliases are fully expanded at load time — the loader
produces every ``<alias>_<pk>`` form so a single whole-token lookup
is enough (no split fallback, no suffix stripping at walk time).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pipeline._text import normalize_identifier
from pipeline.config import PipelineConfig

_HTTP_METHODS = frozenset({
    "get", "post", "put", "patch", "delete", "head", "options", "trace",
})


@dataclass(frozen=True)
class PathReference:
    token: str
    resource: str
    source: str  # "url_segment" | "path_parameter"


def find_path_references(
    path: str,
    path_item: dict[str, Any],
    config: PipelineConfig,
) -> list[PathReference]:
    aliases_lookup = config.resources.aliases_lookup
    candidates: list[tuple[str, str]] = []

    # URL segments — strip braces on path-parameter placeholders.
    for segment in path.split("/"):
        stripped = segment.strip("{}")
        if stripped:
            candidates.append((stripped, "url_segment"))

    # Path-level + operation-level parameter blocks share the same walk.
    parameter_blocks: list[dict[str, Any]] = [path_item]
    for method, operation in path_item.items():
        if method in _HTTP_METHODS and isinstance(operation, dict):
            parameter_blocks.append(operation)

    for block in parameter_blocks:
        for parameter in block.get("parameters") or []:
            if not isinstance(parameter, dict) or parameter.get("in") != "path":
                continue
            name = parameter.get("name")
            if isinstance(name, str) and name:
                candidates.append((name, "path_parameter"))

    # Normalize, look up, dedup, emit.
    seen: set[tuple[str, str, str]] = set()
    references: list[PathReference] = []
    for token, source in candidates:
        resource = aliases_lookup.get(normalize_identifier(token))
        if resource is None:
            continue
        key = (token, resource, source)
        if key in seen:
            continue
        seen.add(key)
        references.append(
            PathReference(token=token, resource=resource, source=source)
        )
    return references
