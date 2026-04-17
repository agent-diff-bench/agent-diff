"""Body-level reference extractor (Group E).

Walks an operation's request body + response bodies, finds schema
``$ref``s, and resolves them via the Group D bindings table. Top-
level ``$ref``s into ``components.requestBodies`` / ``components.
responses`` are dereferenced first. Descends into ``items`` and
``allOf`` / ``oneOf`` / ``anyOf`` branches, not properties.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import Any

_SCHEMA_PREFIX = "#/components/schemas/"
_REQUEST_BODY_PREFIX = "#/components/requestBodies/"
_RESPONSE_PREFIX = "#/components/responses/"


@dataclass(frozen=True)
class BodyReference:
    resource: str
    role: str            # "request" | "response"
    status_code: str | None
    media_type: str
    schema_name: str


def find_body_references(
    operation: dict[str, Any],
    spec: dict[str, Any],
    bindings: Mapping[str, str],
) -> list[BodyReference]:
    raw_components = spec.get("components")
    components: dict[str, Any] = raw_components if isinstance(raw_components, dict) else {}
    holders: list[tuple[str, str | None, dict[str, Any]]] = []

    request_body = _deref(operation.get("requestBody"), _REQUEST_BODY_PREFIX, components.get("requestBodies") or {})
    if isinstance(request_body, dict):
        content = request_body.get("content")
        if isinstance(content, dict):
            holders.append(("request", None, content))

    responses = operation.get("responses")
    if isinstance(responses, dict):
        response_components = components.get("responses") or {}
        for status_code, response in responses.items():
            response = _deref(response, _RESPONSE_PREFIX, response_components)
            if not isinstance(response, dict):
                continue
            content = response.get("content")
            if isinstance(content, dict):
                holders.append(("response", str(status_code), content))

    seen: set[tuple[str, str, str | None, str, str]] = set()
    references: list[BodyReference] = []
    for role, status_code, content in holders:
        for media_type, media in content.items():
            if not isinstance(media, dict):
                continue
            for resource, schema_name in _walk(media.get("schema"), bindings):
                key = (resource, role, status_code, media_type, schema_name)
                if key in seen:
                    continue
                seen.add(key)
                references.append(BodyReference(resource, role, status_code, media_type, schema_name))
    return references


def _deref(node: Any, prefix: str, targets: Mapping[str, Any]) -> dict[str, Any] | None:
    if not isinstance(node, dict):
        return None
    ref = node.get("$ref")
    if not isinstance(ref, str):
        return node
    if not ref.startswith(prefix):
        return None
    target = targets.get(ref[len(prefix):])
    return target if isinstance(target, dict) else None


def _walk(schema: Any, bindings: Mapping[str, str]) -> Iterator[tuple[str, str]]:
    if not isinstance(schema, dict):
        return
    ref = schema.get("$ref")
    if isinstance(ref, str) and ref.startswith(_SCHEMA_PREFIX):
        name = ref[len(_SCHEMA_PREFIX):]
        target = bindings.get(name)
        if target is not None:
            yield target, name
        return
    items = schema.get("items")
    if isinstance(items, dict):
        yield from _walk(items, bindings)
    for key in ("allOf", "oneOf", "anyOf"):
        for branch in schema.get(key) or []:
            yield from _walk(branch, bindings)
