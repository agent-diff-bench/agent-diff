"""Documentation generation — resources.json.

Resource-first pivot built on top of an ``endpoints.json`` document.
For each configured resource, assembles:

- ``bound_schemas`` — every component schema the Group D bindings
  table maps to this resource, inlined verbatim from the
  ``endpoints.json`` top-level schemas block (already ref-rewritten
  to ``#/schemas/*``).
- ``outgoing_references`` — grouped by target resource, with the
  evidence produced by Groups A/B/C/E for operations whose subject
  is this resource.
- ``incoming_references`` — grouped by source resource, same
  evidence shape, from operations whose subject is something else
  but which reference this resource.
- ``endpoint_keys`` — ``"METHOD /path"`` pointers into
  ``endpoints.json`` for every operation whose subject is this
  resource (cross-link, no duplication).

``_meta.source_endpoints_hash`` is a SHA256 of the (sorted)
``endpoints.json`` payload so re-runs can detect drift.

Deterministic: no LLM calls.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipeline.config import PipelineConfig
from pipeline.extraction.reference_groups import group_references_by_pair
from pipeline.extraction.schema_bindings import build_schema_bindings


def generate_resources_document(
    spec: dict[str, Any],
    config: PipelineConfig,
    endpoints_document: dict[str, Any],
    bindings: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build the resources.json document structure."""
    if bindings is None:
        bindings = build_schema_bindings(spec, config)

    groups = group_references_by_pair(spec, config, bindings)
    schemas_block = endpoints_document.get("schemas") or {}
    endpoints_block = endpoints_document.get("endpoints") or {}

    # Invert the bindings map: resource → list of schema names.
    schemas_by_resource: dict[str, list[str]] = {}
    for schema_name, resource in bindings.items():
        schemas_by_resource.setdefault(resource, []).append(schema_name)

    # Partition endpoint keys by subject.
    endpoint_keys_by_subject: dict[str, list[str]] = {}
    for key, entry in endpoints_block.items():
        subject = entry.get("subject")
        if isinstance(subject, str):
            endpoint_keys_by_subject.setdefault(subject, []).append(key)

    resources: dict[str, dict[str, Any]] = {}
    for resource_name in sorted(config.resources.aliases_by_resource.keys()):
        outgoing: dict[str, list[dict[str, Any]]] = {}
        incoming: dict[str, list[dict[str, Any]]] = {}
        for (source, target), evidence_list in groups.items():
            serialized = [asdict(evidence) for evidence in evidence_list]
            if source == resource_name:
                outgoing.setdefault(target, []).extend(serialized)
            if target == resource_name and source != resource_name:
                incoming.setdefault(source, []).extend(serialized)

        bound_names = sorted(schemas_by_resource.get(resource_name, []))
        bound_schemas = {
            name: schemas_block[name]
            for name in bound_names
            if name in schemas_block
        }

        resources[resource_name] = {
            "resource": resource_name,
            "primary_key": config.resources.primary_keys_lookup.get(resource_name),
            "bound_schemas": bound_schemas,
            "endpoint_keys": sorted(endpoint_keys_by_subject.get(resource_name, [])),
            "outgoing_references": outgoing,
            "incoming_references": incoming,
        }

    return {
        "_meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "config_path": str(config.config_path) if config.config_path else None,
            "resource_count": len(resources),
            "source_endpoints_hash": _hash_document(endpoints_document),
        },
        "resources": resources,
    }


def _hash_document(document: dict[str, Any]) -> str:
    """Stable SHA256 of the document, excluding ``_meta.generated_at``."""
    scrubbed = dict(document)
    meta = dict(document.get("_meta") or {})
    meta.pop("generated_at", None)
    scrubbed["_meta"] = meta
    payload = json.dumps(scrubbed, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def write_resources_document(document: dict[str, Any], output_path: Path) -> None:
    """Serialize ``document`` to ``output_path`` as indented JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(document, indent=2))
