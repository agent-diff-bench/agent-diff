"""Non-path parameter reference extractor (Group B).

For a path item, walks every declared parameter with ``in`` equal to
``query``, ``header``, or ``cookie`` — the ones ``path_references``
deliberately skips — and emits hits against ``config.resources.
aliases_lookup``. Path-level parameters are merged with each HTTP
method's operation-level parameters, same walk pattern as Group A.

``$ref`` parameters (without a local ``name``) are silently skipped;
resolving them into ``components.parameters`` is a later milestone.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pipeline._text import normalize_identifier
from pipeline.config import PipelineConfig

_HTTP_METHODS = frozenset({
    "get", "post", "put", "patch", "delete", "head", "options", "trace",
})
_LOCATIONS = frozenset({"query", "header", "cookie"})


@dataclass(frozen=True)
class ParameterReference:
    token: str
    resource: str
    location: str  # "query" | "header" | "cookie"


def find_parameter_references(
    path_item: dict[str, Any],
    config: PipelineConfig,
) -> list[ParameterReference]:
    aliases_lookup = config.resources.aliases_lookup
    candidates: list[tuple[str, str]] = []

    parameter_blocks: list[dict[str, Any]] = [path_item]
    for method, operation in path_item.items():
        if method in _HTTP_METHODS and isinstance(operation, dict):
            parameter_blocks.append(operation)

    for block in parameter_blocks:
        for parameter in block.get("parameters") or []:
            if not isinstance(parameter, dict):
                continue
            location = parameter.get("in")
            if location not in _LOCATIONS:
                continue
            name = parameter.get("name")
            if isinstance(name, str) and name:
                candidates.append((name, location))

    seen: set[tuple[str, str, str]] = set()
    references: list[ParameterReference] = []
    for token, location in candidates:
        resource = aliases_lookup.get(normalize_identifier(token))
        if resource is None:
            continue
        key = (token, resource, location)
        if key in seen:
            continue
        seen.add(key)
        references.append(
            ParameterReference(token=token, resource=resource, location=location)
        )
    return references
