"""Scan implemented routes and build endpoint documentation + test registry.

Imports the app's routes module, reads the Route objects, matches them
against endpoints.json for metadata, and writes:
  - implemented_endpoints.json — full metadata for implemented endpoints
  - test_registry.json — test manifest with status tracking
"""

from __future__ import annotations

import json
import re
from importlib import import_module
from pathlib import Path
from typing import Any


def scan_implemented_routes(routes_module: str) -> list[dict[str, Any]]:
    """Import the routes module and extract all registered Route entries."""
    module = import_module(routes_module)
    routes = getattr(module, "routes", [])

    implemented = []
    for route in routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if not path or "unknown_path" in path:
            continue
        for method in methods:
            if method.upper() in ("HEAD", "OPTIONS"):
                continue
            implemented.append({"method": method.upper(), "path": path})
    return implemented


def build_test_registry(
    implemented: list[dict[str, Any]],
    endpoints_doc: dict[str, Any],
    app_slug: str,
) -> dict[str, Any]:
    """Build documentation + test registry from implemented routes."""
    endpoints_block = endpoints_doc.get("endpoints") or {}
    schemas_block = endpoints_doc.get("schemas") or {}

    matched_endpoints: dict[str, Any] = {}
    test_entries: list[dict[str, Any]] = []

    for route in implemented:
        method = route["method"]
        path = route["path"]
        key = f"{method} {path}"

        endpoint_meta = endpoints_block.get(key)
        if endpoint_meta:
            matched_endpoints[key] = endpoint_meta

        test_entry: dict[str, Any] = {
            "method": method,
            "path": path,
            "has_spec_metadata": endpoint_meta is not None,
            "tested": False,
            "test_result": None,
        }

        if endpoint_meta:
            test_entry["subject"] = endpoint_meta.get("subject")
            test_entry["summary"] = _extract_summary(endpoint_meta, endpoints_doc)

            path_params = re.findall(r"\{(\w+)\}", path)
            test_entry["path_params"] = path_params
            test_entry["needs_seed"] = method in ("GET", "PUT", "DELETE") and bool(path_params)

        test_entries.append(test_entry)

    unimplemented = []
    for key in endpoints_block:
        if key not in matched_endpoints:
            parts = key.split(" ", 1)
            if len(parts) == 2:
                unimplemented.append({"method": parts[0], "path": parts[1]})

    return {
        "app_slug": app_slug,
        "total_spec_endpoints": len(endpoints_block),
        "implemented_count": len(matched_endpoints),
        "unimplemented_count": len(unimplemented),
        "endpoints": test_entries,
        "unimplemented": unimplemented,
    }


def _extract_summary(
    endpoint_meta: dict[str, Any],
    endpoints_doc: dict[str, Any],
) -> str | None:
    """Try to get a summary for the endpoint."""
    return endpoint_meta.get("summary") or endpoint_meta.get("subject")


def write_registry(
    output_dir: Path,
    implemented_endpoints: dict[str, Any],
    test_registry: dict[str, Any],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "implemented_endpoints.json").write_text(
        json.dumps(implemented_endpoints, indent=2)
    )
    (output_dir / "test_registry.json").write_text(
        json.dumps(test_registry, indent=2)
    )
