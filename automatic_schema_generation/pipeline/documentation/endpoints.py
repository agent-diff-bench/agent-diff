"""Documentation generation — endpoints.json.

Assembles a per-endpoint catalog from the spec, attaches the
reference evidence produced by Groups A/B/C/E, and includes the
transitive closure of every component schema reachable from any
endpoint. The output is self-contained: ``$ref``s are rewritten
from ``#/components/schemas/*`` to ``#/schemas/*`` so the top-level
``schemas`` block replaces ``spec.components.schemas`` for
downstream consumption.

Deterministic: no LLM calls, no prompt templating. Re-running
produces identical output (except ``_meta.generated_at``).
"""

from __future__ import annotations

import copy
import json
from collections.abc import Mapping
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipeline.config import PipelineConfig
from pipeline.extraction.endpoint_references import find_endpoint_references
from pipeline.extraction.schema_bindings import build_schema_bindings

_HTTP_METHODS = frozenset({
    "get", "post", "put", "patch", "delete", "head", "options", "trace",
})
_OLD_REF_PREFIX = "#/components/schemas/"
_NEW_REF_PREFIX = "#/schemas/"


def generate_endpoints_document(
    spec: dict[str, Any],
    config: PipelineConfig,
    bindings: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build the endpoints.json document structure."""
    if bindings is None:
        bindings = build_schema_bindings(spec, config)

    endpoints: dict[str, dict[str, Any]] = {}
    paths = spec.get("paths") or {}
    if isinstance(paths, dict):
        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method in _HTTP_METHODS:
                operation = path_item.get(method)
                if not isinstance(operation, dict):
                    continue
                entry = _build_entry(method, path, operation, spec, config, bindings)
                endpoints[f"{method.upper()} {path}"] = entry

    schemas = _collect_transitive_schemas(endpoints, spec)
    endpoints = _rewrite_refs(endpoints)
    schemas = _rewrite_refs(schemas)

    return {
        "_meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "config_path": str(config.config_path) if config.config_path else None,
            "endpoint_count": len(endpoints),
            "schema_count": len(schemas),
        },
        "endpoints": endpoints,
        "schemas": schemas,
    }


def _build_entry(
    method: str,
    path: str,
    operation: dict[str, Any],
    spec: dict[str, Any],
    config: PipelineConfig,
    bindings: Mapping[str, str],
) -> dict[str, Any]:
    result = find_endpoint_references(method, path, spec, config, bindings)
    responses = _deref_responses(operation.get("responses") or {}, spec)
    return {
        "method": method.upper(),
        "path": path,
        "subject": result.subject,
        "subject_source": result.subject_source,
        "parameters": copy.deepcopy(operation.get("parameters") or []),
        "request_body": copy.deepcopy(operation.get("requestBody")),
        "responses": responses,
        "references": {
            "path": [asdict(reference) for reference in result.path_references],
            "parameters": [asdict(reference) for reference in result.parameter_references],
            "body": [asdict(reference) for reference in result.body_references],
            "property": [asdict(reference) for reference in result.property_references],
        },
    }


def _deref_responses(
    responses: dict[str, Any],
    spec: dict[str, Any],
) -> dict[str, Any]:
    """Resolve $ref pointers in response objects (components/responses)."""
    component_responses = (spec.get("components") or {}).get("responses") or {}
    result: dict[str, Any] = {}
    for status_code, response in responses.items():
        if isinstance(response, dict) and "$ref" in response:
            ref = response["$ref"]
            prefix = "#/components/responses/"
            if ref.startswith(prefix):
                name = ref[len(prefix):]
                resolved = component_responses.get(name)
                if isinstance(resolved, dict):
                    result[status_code] = copy.deepcopy(resolved)
                    continue
        result[status_code] = copy.deepcopy(response)
    return result


def _collect_transitive_schemas(
    endpoints: dict[str, Any],
    spec: dict[str, Any],
) -> dict[str, Any]:
    """Collect every component schema transitively reachable from ``endpoints``."""
    raw_components = (spec.get("components") or {}).get("schemas") or {}
    component_schemas: dict[str, Any] = raw_components if isinstance(raw_components, dict) else {}

    reachable: set[str] = set()
    frontier: set[str] = set()
    _find_refs(endpoints, frontier)
    while frontier:
        name = frontier.pop()
        if name in reachable:
            continue
        reachable.add(name)
        target = component_schemas.get(name)
        if isinstance(target, dict):
            nested: set[str] = set()
            _find_refs(target, nested)
            frontier.update(nested - reachable)

    return {
        name: copy.deepcopy(component_schemas[name])
        for name in sorted(reachable)
        if name in component_schemas
    }


def _find_refs(node: Any, out: set[str]) -> None:
    """Walk a nested structure and collect schema ``$ref`` target names."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and value.startswith(_OLD_REF_PREFIX):
                out.add(value[len(_OLD_REF_PREFIX):])
            else:
                _find_refs(value, out)
    elif isinstance(node, list):
        for item in node:
            _find_refs(item, out)


def _rewrite_refs(node: Any) -> Any:
    """Return a copy of ``node`` with every schema ``$ref`` prefix rewritten."""
    if isinstance(node, dict):
        result: dict[str, Any] = {}
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and value.startswith(_OLD_REF_PREFIX):
                result[key] = _NEW_REF_PREFIX + value[len(_OLD_REF_PREFIX):]
            else:
                result[key] = _rewrite_refs(value)
        return result
    if isinstance(node, list):
        return [_rewrite_refs(item) for item in node]
    return node


def classify_responses(spec: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Split components/responses into generic (shared error schema) vs resource-specific.

    Returns (generic_responses, resource_responses). Generic responses use
    a schema referenced by 3+ responses — these are app-wide error patterns.
    Resource-specific responses use a unique schema or have domain-specific content.
    Status-only responses (no body) are included in generic.
    """
    component_responses = (spec.get("components") or {}).get("responses") or {}
    if not component_responses:
        return {}, {}

    # Count how many responses reference each schema
    from collections import Counter
    schema_usage: Counter[str] = Counter()
    for name, body in component_responses.items():
        ref = _response_schema_ref(body)
        if ref:
            schema_usage[ref] += 1

    # A schema is shared if 3+ responses use it, OR if its name indicates
    # an error/validation pattern (these are generic even if only one
    # response definition references them, since endpoints reuse them widely)
    error_keywords = {"error", "validation"}
    shared_schemas = set()
    for schema, count in schema_usage.items():
        schema_name = schema.rsplit("/", 1)[-1].lower().replace("-", "_")
        if count >= 3 or any(keyword in schema_name for keyword in error_keywords):
            shared_schemas.add(schema)

    component_schemas = (spec.get("components") or {}).get("schemas") or {}
    generic: dict[str, Any] = {}
    resource_specific: dict[str, Any] = {}

    for name, body in component_responses.items():
        content = body.get("content") or {}
        has_body = bool(content)
        ref = _response_schema_ref(body)

        entry = copy.deepcopy(body)
        # Inline the referenced schema body for completeness
        if ref and ref in component_schemas:
            entry["_resolved_schema"] = copy.deepcopy(component_schemas[ref])

        if not has_body or ref in shared_schemas:
            generic[name] = entry
        else:
            resource_specific[name] = entry

    return generic, resource_specific


def _response_schema_ref(response_body: dict[str, Any]) -> str | None:
    """Extract the schema $ref from a response body, if any."""
    content = response_body.get("content") or {}
    for media_type, media in content.items():
        schema = media.get("schema") or {}
        ref = schema.get("$ref")
        if isinstance(ref, str):
            return ref
    return None


def write_endpoints_document(document: dict[str, Any], output_path: Path) -> None:
    """Serialize ``document`` to ``output_path`` as indented JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(document, indent=2))
