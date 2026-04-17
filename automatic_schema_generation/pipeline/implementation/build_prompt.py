"""Prompt constructor for entity implementation.

Two-pass architecture: Pass 1 builds the base model, operations,
serializers, and routes. Pass 2 adds FK relationships.

Usage::

    pass1 = build_pass1_prompt("repos", resources_doc, endpoints_doc, config, spec)
    pass2 = build_pass2_prompt("repos", resources_doc, endpoints_doc, config, spec)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pipeline.config import PipelineConfig

_PASS1_TEMPLATE = Path(__file__).parent / "implementation_prompt_pass1.md"
_PASS2_TEMPLATE = Path(__file__).parent / "implementation_prompt_pass2.md"
_MOCKS_DIR = Path(__file__).parent / "mocks"


def _common_placeholders(
    resource_name: str,
    resources_doc: dict[str, Any],
    config: PipelineConfig,
) -> tuple[dict[str, Any], dict[str, str]]:
    """Return (resource_entry, shared_placeholders)."""
    resource = resources_doc["resources"][resource_name]
    entity_slug = _singularize(resource_name)
    placeholders = {
        "APP_NAME": config.app_name,
        "RESOURCE_NAME": resource_name,
        "TABLE_NAME": f"{config.app_slug}_{resource_name}",
        "MODEL_CLASS_NAME": _model_class_name(config.app_name, entity_slug),
        "ENTITY_SLUG": entity_slug,
        "PRIMARY_KEY": resource.get("primary_key") or "id",
        "OPENAPI_PATH": str(config.openapi_path),
        "TARGET_DIR": str(config.target_dir),
    }
    return resource, placeholders


def build_pass1_prompt(
    resource_name: str,
    resources_doc: dict[str, Any],
    endpoints_doc: dict[str, Any],
    config: PipelineConfig,
    spec: dict[str, Any] | None = None,
    implemented_constructors: list[str] | None = None,
) -> str:
    """Pass 1: base model, operations, serializers, routes — no FKs."""
    resource, placeholders = _common_placeholders(resource_name, resources_doc, config)
    if implemented_constructors:
        error_note = (
            "Already implemented in `core/errors.py`: "
            + ", ".join(f"`{name}()`" for name in implemented_constructors)
            + "\n\nFor error codes not covered above, implement the response "
            "inline or add a new constructor to `core/errors.py`."
        )
    else:
        error_note = (
            "Check `core/errors.py` for any existing error constructors before "
            "writing your own."
        )
    placeholders.update({
        "BOUND_SCHEMAS": json.dumps(resource.get("bound_schemas") or {}, indent=2),
        "ENDPOINTS": _format_endpoints(resource, endpoints_doc, spec),
        "REFERENCED_SCHEMAS": _format_referenced_schemas(resource, endpoints_doc),
        "IMPLEMENTED_ERRORS": error_note,
    })
    return _fill_template(_PASS1_TEMPLATE, placeholders)


def build_pass2_prompt(
    resource_name: str,
    resources_doc: dict[str, Any],
    endpoints_doc: dict[str, Any],
    config: PipelineConfig,
    spec: dict[str, Any] | None = None,
) -> str:
    """Pass 2: FK columns, relationships, association tables."""
    resource, placeholders = _common_placeholders(resource_name, resources_doc, config)
    placeholders.update({
        "RELATIONSHIP_PATTERNS": _load_mock_patterns(),
        "RELATED_RESOURCES": _format_related(resource, resources_doc, config),
        "EXTERNAL_SCHEMAS": _format_external(resource_name, spec, config),
    })
    return _fill_template(_PASS2_TEMPLATE, placeholders)


def _fill_template(template_path: Path, placeholders: dict[str, str]) -> str:
    template = template_path.read_text()
    for key, value in placeholders.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


def _load_mock_patterns() -> str:
    lines: list[str] = []
    for path in sorted(_MOCKS_DIR.glob("*.py")):
        lines.append(f"### {path.stem.replace('_', ' ').title()}")
        lines.append(f"```python\n{path.read_text().rstrip()}\n```")
        lines.append("")
    return "\n".join(lines)


def _format_endpoints(
    resource: dict[str, Any],
    endpoints_doc: dict[str, Any],
    spec: dict[str, Any] | None,
) -> str:
    endpoints_block = endpoints_doc.get("endpoints") or {}
    spec_paths = (spec or {}).get("paths") or {}
    lines: list[str] = []
    for key in resource.get("endpoint_keys") or []:
        entry = endpoints_block.get(key)
        if entry is None:
            continue
        method = entry["method"]
        path = entry["path"]
        lines.append(f"#### {method} {path}")

        # Summary from the original spec
        spec_operation = (spec_paths.get(path) or {}).get(method.lower()) or {}
        summary = (spec_operation.get("summary") or "").strip()
        if summary:
            lines.append(f"_{summary}_")

        # Parameters
        parameters = entry.get("parameters") or []
        if parameters:
            lines.append("Parameters:")
            for parameter in parameters:
                resolved = _resolve_param(parameter, spec) if "$ref" in parameter else parameter
                name = resolved.get("name", "?")
                location = resolved.get("in", "?")
                required = "required" if resolved.get("required") else "optional"
                schema_type = (resolved.get("schema") or {}).get("type", "string")
                lines.append(f"  - {name} ({location}, {required}): {schema_type}")

        # Request body for mutation endpoints
        request_body = entry.get("request_body")
        if isinstance(request_body, dict):
            rb_content = request_body.get("content") or {}
            for media_type, media in rb_content.items():
                schema = media.get("schema") or {}
                ref = schema.get("$ref")
                if ref:
                    lines.append(f"Request body: {ref}")
                elif schema.get("properties"):
                    rb_required = schema.get("required") or []
                    field_summaries = []
                    for field_name, field_schema in schema["properties"].items():
                        field_type = _normalize_type(field_schema)
                        tag = " (required)" if field_name in rb_required else ""
                        field_summaries.append(f"  - {field_name}: {field_type}{tag}")
                    lines.append(f"Request body ({media_type}):")
                    lines.extend(field_summaries)
                break

        # Responses — 2xx with schema detail, errors as status codes only
        responses = entry.get("responses") or {}
        error_codes: list[str] = []
        for status_code, response in responses.items():
            code_str = str(status_code)
            if not code_str.startswith("2"):
                error_codes.append(code_str)
                continue
            content = response.get("content") or {}
            if not content:
                lines.append(f"Response {status_code}: no content")
                continue
            for media_type, media in content.items():
                schema = media.get("schema") or {}
                ref = schema.get("$ref")
                if ref:
                    lines.append(f"Response {status_code}: {ref}")
                elif schema.get("type") == "array":
                    items_ref = (schema.get("items") or {}).get("$ref")
                    if items_ref:
                        lines.append(f"Response {status_code}: array of {items_ref}")
                break
        if error_codes:
            lines.append(f"Errors: {', '.join(sorted(error_codes))}")
        lines.append("")
    return "\n".join(lines)


def _normalize_type(field_schema: dict[str, Any]) -> str:
    """Turn JSON schema type into a readable string, handling ['type', 'null']."""
    raw = field_schema.get("type", "object")
    if isinstance(raw, list):
        non_null = [t for t in raw if t != "null"]
        base = non_null[0] if non_null else "object"
        return f"{base} (nullable)" if "null" in raw else base
    if field_schema.get("oneOf") or field_schema.get("anyOf"):
        return "object (nullable)" if any(
            b.get("type") == "null"
            for b in (field_schema.get("oneOf") or field_schema.get("anyOf") or [])
        ) else "object"
    return raw


def _resolve_param(parameter: dict[str, Any], spec: dict[str, Any] | None) -> dict[str, Any]:
    """Follow a single $ref hop for a parameter object."""
    if spec is None:
        return parameter
    ref = parameter.get("$ref", "")
    if not ref.startswith("#/"):
        return parameter
    parts = ref.lstrip("#/").split("/")
    node: Any = spec
    for part in parts:
        if isinstance(node, dict):
            node = node.get(part)
        else:
            return parameter
    return node if isinstance(node, dict) else parameter


def _format_referenced_schemas(
    resource: dict[str, Any],
    endpoints_doc: dict[str, Any],
) -> str:
    """Collect schemas referenced by this resource's endpoints but not in bound_schemas."""
    bound_names = set((resource.get("bound_schemas") or {}).keys())
    all_schemas = endpoints_doc.get("schemas") or {}
    endpoints_block = endpoints_doc.get("endpoints") or {}
    ref_prefix = "#/schemas/"

    referenced_names: set[str] = set()
    for key in resource.get("endpoint_keys") or []:
        entry = endpoints_block.get(key)
        if entry is None:
            continue
        _collect_refs(entry.get("responses"), ref_prefix, referenced_names)
        _collect_refs(entry.get("request_body"), ref_prefix, referenced_names)

    # Follow $ref chains transitively — if JobResponse refs JobBase
    # which refs AsanaResource, include all three
    frontier = referenced_names - bound_names
    all_referenced: set[str] = set()
    while frontier:
        name = frontier.pop()
        if name in all_referenced or name in bound_names:
            continue
        all_referenced.add(name)
        schema = all_schemas.get(name)
        if isinstance(schema, dict):
            nested: set[str] = set()
            _collect_refs(schema, ref_prefix, nested)
            frontier.update(nested - all_referenced - bound_names)

    if not all_referenced:
        return "{}"
    extra_schemas = {
        name: all_schemas[name]
        for name in sorted(all_referenced)
        if name in all_schemas
    }
    return json.dumps(extra_schemas, indent=2)


def _collect_refs(obj: Any, prefix: str, out: set[str]) -> None:
    """Recursively find all $ref values starting with prefix."""
    if isinstance(obj, dict):
        ref = obj.get("$ref")
        if isinstance(ref, str) and ref.startswith(prefix):
            out.add(ref[len(prefix):])
        for value in obj.values():
            _collect_refs(value, prefix, out)
    elif isinstance(obj, list):
        for item in obj:
            _collect_refs(item, prefix, out)


def _format_related(
    resource: dict[str, Any],
    resources_doc: dict[str, Any],
    config: PipelineConfig,
) -> str:
    resource_name = resource.get("resource", "")
    resource_aliases = config.resources.aliases_by_resource.get(resource_name, frozenset())
    outgoing = resource.get("outgoing_references") or {}
    incoming = resource.get("incoming_references") or {}
    all_related = sorted(
        (set(outgoing.keys()) | set(incoming.keys())) - {"_unresolved_"}
    )
    if not all_related:
        return "_No related resources detected._"

    all_resources = resources_doc.get("resources") or {}
    lines: list[str] = []
    for related_name in all_related:
        directions: list[str] = []
        if related_name in outgoing:
            directions.append("outgoing")
        if related_name in incoming:
            directions.append("incoming")

        related_resource = all_resources.get(related_name) or {}
        related_pk = related_resource.get("primary_key") or "id"
        table_name = f"{config.app_slug}_{related_name}"

        is_self_ref = related_name == resource_name

        lines.append(f"### {related_name}")
        if is_self_ref:
            lines.append(f"- **SELF-REFERENTIAL** — this resource references itself")
            lines.append(f"- Use the Self Referential pattern: nullable FK to own table,")
            lines.append(f"  `remote_side=[id]` on the parent relationship")
        lines.append(f"- Table: `{table_name}`")
        lines.append(f"- Primary key: `{related_pk}`")
        lines.append(f"- Direction: {', '.join(directions)}")

        # Summarize which fields in the current resource reference this related resource
        referencing_fields = _extract_referencing_fields(
            outgoing.get(related_name, []),
            incoming.get(related_name, []),
        )
        if referencing_fields:
            lines.append(
                f"- **Fields referencing {related_name}**: "
                f"`{'`, `'.join(referencing_fields)}`"
            )
            lines.append("")
            if is_self_ref:
                lines.append(
                    f"These fields create a self-referential hierarchy. "
                    f"Add a nullable FK column (e.g. `parent_id`) pointing "
                    f"at `{table_name}.{related_pk}` with `remote_side=[{related_pk}]`."
                )
            else:
                lines.append(
                    f"These fields all point at the `{table_name}` table. "
                    f"Infer the correct FK relationship type and apply using "
                    f"the reference patterns above."
                )

        lines.append("")
        lines.append("Evidence:")
        for evidence in outgoing.get(related_name, []):
            lines.append(
                f"  - {evidence['method']} {evidence['path']}"
                f" — {evidence['kind']}: {evidence['location']}"
            )
        for evidence in incoming.get(related_name, []):
            lines.append(
                f"  - {evidence['method']} {evidence['path']}"
                f" — {evidence['kind']}: {evidence['location']} (incoming)"
            )

        bound_schemas = related_resource.get("bound_schemas") or {}
        if bound_schemas:
            slim = _slim_schemas(bound_schemas, related_pk, resource_aliases)
            lines.append(f"\nKey fields (PK + fields referencing {resource_name}):")
            lines.append(f"```json\n{json.dumps(slim, indent=2)}\n```")
        lines.append("")
    return "\n".join(lines)


def _extract_referencing_fields(
    outgoing_evidence: list[dict[str, Any]],
    incoming_evidence: list[dict[str, Any]],
) -> list[str]:
    """Extract unique field paths from property evidence, deduplicating prefixes."""
    raw_paths: set[str] = set()
    for evidence in (*outgoing_evidence, *incoming_evidence):
        if evidence["kind"] == "property":
            raw_paths.add(evidence["location"])
    # Remove paths that are extensions of a shorter path (e.g. drop
    # "owner.login" when "owner" already exists)
    minimal: set[str] = set()
    for path in sorted(raw_paths, key=len):
        if not any(path.startswith(existing + ".") for existing in minimal):
            minimal.add(path)
    return sorted(minimal)


def _slim_schemas(
    bound_schemas: dict[str, Any],
    primary_key: str,
    target_aliases: frozenset[str],
) -> dict[str, Any]:
    """Extract only PK fields and properties whose name matches target aliases."""
    result: dict[str, Any] = {}
    for schema_name, schema in bound_schemas.items():
        properties = schema.get("properties") or {}
        kept: dict[str, Any] = {}
        for field_name, field_schema in properties.items():
            if field_name == primary_key:
                kept[field_name] = field_schema
                continue
            normalized = field_name.lower().replace("-", "_")
            for alias in target_aliases:
                if alias in normalized:
                    kept[field_name] = field_schema
                    break
        if kept:
            entry: dict[str, Any] = {"properties": kept}
            required = schema.get("required")
            if isinstance(required, list):
                kept_required = [r for r in required if r in kept]
                if kept_required:
                    entry["required"] = kept_required
            result[schema_name] = entry
    return result


def _format_external(
    resource_name: str,
    spec: dict[str, Any] | None,
    config: PipelineConfig,
) -> str:
    """Find unbound schemas related to this resource: by $ref or by name tokens."""
    if spec is None:
        return "_No spec provided — cannot scan for external schemas._"

    from pipeline._text import normalize_identifier
    from pipeline.extraction.schema_bindings import build_schema_bindings
    full_bindings = build_schema_bindings(spec, config)

    this_resource_schemas = {
        name for name, resource in full_bindings.items()
        if resource == resource_name
    }
    all_bound = set(full_bindings.keys())
    resource_aliases = config.resources.aliases_by_resource.get(resource_name, frozenset())

    component_schemas = (spec.get("components") or {}).get("schemas") or {}
    external: dict[str, str] = {}
    for schema_name, schema_body in component_schemas.items():
        if schema_name in all_bound:
            continue
        # Match 1: schema $refs into this resource's bound schemas
        refs_found: set[str] = set()
        _collect_refs(schema_body, "#/components/schemas/", refs_found)
        matching = refs_found & this_resource_schemas
        if matching:
            external[schema_name] = f"refs: {', '.join(sorted(matching))}"
            continue
        # Match 2: schema name contains a token matching this resource's aliases
        normalized = normalize_identifier(schema_name)
        tokens = set(normalized.split("_"))
        if tokens & resource_aliases:
            external[schema_name] = "name match"

    if not external:
        return "_No external schemas reference this resource._"

    # Split: name-matched schemas get full bodies (small, operationally
    # relevant), ref-matched schemas get just a one-liner (large webhook
    # payloads are context-only).
    name_matched = {n: r for n, r in external.items() if r == "name match"}
    ref_matched = {n: r for n, r in external.items() if r != "name match"}

    lines: list[str] = []
    for schema_name in sorted(name_matched):
        body = component_schemas.get(schema_name)
        if body:
            lines.append(f"### {schema_name}")
            lines.append(f"```json\n{json.dumps(body, indent=2)}\n```")
            lines.append("")

    if ref_matched:
        lines.append("Other schemas that reference this resource (context only):")
        for schema_name in sorted(ref_matched)[:20]:
            reason = ref_matched[schema_name]
            lines.append(f"- `{schema_name}` ({reason})")
        if len(ref_matched) > 20:
            lines.append(f"- ... and {len(ref_matched) - 20} more")
    return "\n".join(lines)



def _singularize(name: str) -> str:
    if name.endswith("ies"):
        return name[:-3] + "y"
    if name.endswith("sses") or name.endswith(("xes", "ches", "shes", "zes")):
        return name[:-2]
    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


def _model_class_name(app_name: str, entity_slug: str) -> str:
    app_part = re.sub(r"[^A-Za-z0-9]", "", app_name)
    if app_part:
        app_part = app_part[:1].upper() + app_part[1:]
    parts = [segment for segment in re.split(r"[-_ ]", entity_slug) if segment]
    entity_part = "".join(segment[:1].upper() + segment[1:] for segment in parts)
    return f"{app_part}{entity_part}"
