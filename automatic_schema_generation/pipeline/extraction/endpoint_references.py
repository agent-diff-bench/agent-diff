"""Per-endpoint reference aggregator.

Combines every walker (Groups A/B/C/E) into a single per-operation
record and infers the operation's subject via the "rightmost URL
alias" rule: walking URL segments right-to-left, the first token
whose normalized form hits ``aliases_lookup`` is the subject. If no
segment hits, ``subject`` is ``None``.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import Any

from pipeline._text import normalize_identifier
from pipeline.extraction.body_references import BodyReference, _deref, find_body_references
from pipeline.config import PipelineConfig
from pipeline.extraction.parameter_references import ParameterReference, find_parameter_references
from pipeline.extraction.path_references import PathReference, find_path_references
from pipeline.extraction.property_references import PropertyReference, find_property_references

_REQUEST_BODY_PREFIX = "#/components/requestBodies/"
_RESPONSE_PREFIX = "#/components/responses/"


@dataclass(frozen=True)
class EndpointReferences:
    method: str
    path: str
    subject: str | None
    subject_source: str   # "url_rightmost_alias" | "no_alias_in_url"
    path_references: list[PathReference]
    parameter_references: list[ParameterReference]
    body_references: list[BodyReference]
    property_references: list[PropertyReference]


def find_endpoint_references(
    method: str,
    path: str,
    spec: dict[str, Any],
    config: PipelineConfig,
    bindings: Mapping[str, str],
) -> EndpointReferences:
    path_item: dict[str, Any] = (spec.get("paths") or {}).get(path) or {}
    operation: dict[str, Any] = path_item.get(method.lower()) or {}

    path_refs = find_path_references(path, path_item, config)
    parameter_refs = find_parameter_references(path_item, config)
    body_refs = find_body_references(operation, spec, bindings)
    component_schemas = (spec.get("components") or {}).get("schemas") or {}
    property_refs: list[PropertyReference] = []
    for schema in _iter_body_schemas(operation, spec):
        property_refs.extend(find_property_references(schema, config, bindings, component_schemas))

    subject: str | None = None
    subject_source = "no_alias_in_url"
    aliases_lookup = config.resources.aliases_lookup
    for segment in reversed(path.split("/")):
        stripped = segment.strip("{}")
        if not stripped:
            continue
        resource = aliases_lookup.get(normalize_identifier(stripped))
        if resource is not None:
            subject, subject_source = resource, "url_rightmost_alias"
            break

    return EndpointReferences(
        method=method.upper(),
        path=path,
        subject=subject,
        subject_source=subject_source,
        path_references=path_refs,
        parameter_references=parameter_refs,
        body_references=body_refs,
        property_references=property_refs,
    )


def _iter_body_schemas(operation: dict[str, Any], spec: dict[str, Any]) -> Iterator[dict[str, Any]]:
    raw_components = spec.get("components")
    components: dict[str, Any] = raw_components if isinstance(raw_components, dict) else {}
    contents: list[Any] = []
    request_body = _deref(operation.get("requestBody"), _REQUEST_BODY_PREFIX, components.get("requestBodies") or {})
    if isinstance(request_body, dict):
        contents.append(request_body.get("content"))
    responses = operation.get("responses") or {}
    if isinstance(responses, dict):
        response_components = components.get("responses") or {}
        for response in responses.values():
            response = _deref(response, _RESPONSE_PREFIX, response_components)
            if isinstance(response, dict):
                contents.append(response.get("content"))
    for content in contents:
        if not isinstance(content, dict):
            continue
        for media in content.values():
            if isinstance(media, dict) and isinstance(media.get("schema"), dict):
                yield media["schema"]
