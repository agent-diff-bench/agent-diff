"""
Extract a scoped subset of the Todoist OpenAPI spec.

Keeps only paths related to: projects, tasks, sections, comments, labels,
plus the user identity endpoint (needed for auth/principal resolution).
Walks all kept operations and collects only the $ref schemas they actually
reference (transitively), producing a minimal self-contained spec.
"""

import json
import sys
from pathlib import Path
from copy import deepcopy

SCRIPT_DIR = Path(__file__).parent
SOURCE = SCRIPT_DIR / "openapi.source.json"
OUTPUT = SCRIPT_DIR / "openapi.scoped.json"

# ---------------------------------------------------------------------------
# 1. Define which path prefixes to keep
# ---------------------------------------------------------------------------
KEEP_PREFIXES = [
    "/api/v1/projects",
    "/api/v1/tasks",
    "/api/v1/sections",
    "/api/v1/comments",
    "/api/v1/labels",
    "/api/v1/user",  # identity / principal endpoint
]


def path_in_scope(path: str) -> bool:
    return any(path.startswith(p) for p in KEEP_PREFIXES)


# ---------------------------------------------------------------------------
# 2. Collect all $ref pointers reachable from a JSON subtree
# ---------------------------------------------------------------------------
def collect_refs(node, refs: set):
    """Recursively find all $ref strings in a JSON-like structure."""
    if isinstance(node, dict):
        if "$ref" in node:
            refs.add(node["$ref"])
        for v in node.values():
            collect_refs(v, refs)
    elif isinstance(node, list):
        for item in node:
            collect_refs(item, refs)


def ref_to_key(ref: str) -> tuple:
    """Convert '#/components/schemas/Foo' -> ('schemas', 'Foo')."""
    parts = ref.lstrip("#/").split("/")
    if len(parts) >= 3 and parts[0] == "components":
        return (parts[1], parts[2])
    return None


# ---------------------------------------------------------------------------
# 3. Transitively resolve all referenced component entries
# ---------------------------------------------------------------------------
def resolve_all_refs(components: dict, seed_refs: set) -> dict:
    """
    Starting from seed_refs, walk components transitively and return
    only the entries that are actually needed.
    """
    needed = {}  # (section, name) -> definition
    queue = list(seed_refs)
    visited = set()

    while queue:
        ref = queue.pop()
        if ref in visited:
            continue
        visited.add(ref)

        key = ref_to_key(ref)
        if key is None:
            continue
        section, name = key
        section_dict = components.get(section, {})
        if name not in section_dict:
            continue

        needed.setdefault(section, {})[name] = deepcopy(section_dict[name])

        # find nested refs
        child_refs = set()
        collect_refs(section_dict[name], child_refs)
        for cr in child_refs:
            if cr not in visited:
                queue.append(cr)

    return needed


# ---------------------------------------------------------------------------
# 4. Main
# ---------------------------------------------------------------------------
def main():
    with open(SOURCE) as f:
        spec = json.load(f)

    # Filter paths
    scoped_paths = {}
    for path, path_item in spec.get("paths", {}).items():
        if path_in_scope(path):
            scoped_paths[path] = deepcopy(path_item)

    # Collect all refs from kept paths
    seed_refs = set()
    collect_refs(scoped_paths, seed_refs)

    # Also collect refs from securitySchemes (needed for auth)
    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    collect_refs(security_schemes, seed_refs)

    # Transitively resolve
    components = spec.get("components", {})
    needed_components = resolve_all_refs(components, seed_refs)

    # Always keep securitySchemes if present
    if security_schemes:
        needed_components["securitySchemes"] = deepcopy(security_schemes)

    # Build output spec
    output = {
        "openapi": spec["openapi"],
        "info": {
            **spec["info"],
            "description": (
                "Scoped subset of the Todoist API covering: "
                "projects, tasks, sections, comments, labels, user. "
                "Extracted from the full spec for the agent-diff learning run."
            ),
        },
        "servers": spec.get("servers", []),
        "paths": scoped_paths,
        "components": needed_components,
    }

    # Preserve top-level security if present
    if "security" in spec:
        output["security"] = spec["security"]

    # Keep only tags that match kept paths
    if "tags" in spec:
        used_tags = set()
        for path_item in scoped_paths.values():
            for method_obj in path_item.values():
                if isinstance(method_obj, dict):
                    for tag in method_obj.get("tags", []):
                        used_tags.add(tag)
        output["tags"] = [t for t in spec["tags"] if t.get("name") in used_tags]

    with open(OUTPUT, "w") as f:
        json.dump(output, f, indent=2)

    # Report
    total_paths = len(scoped_paths)
    total_ops = sum(
        1
        for pi in scoped_paths.values()
        for m in pi
        if m in ("get", "post", "put", "patch", "delete")
    )
    total_schemas = len(needed_components.get("schemas", {}))

    print(f"Source paths:  {len(spec.get('paths', {}))}")
    print(f"Scoped paths:  {total_paths}")
    print(f"Scoped ops:    {total_ops}")
    print(f"Schemas kept:  {total_schemas}")
    print(f"Output:        {OUTPUT}")
    print()
    for path in sorted(scoped_paths):
        methods = [m.upper() for m in scoped_paths[path] if m in ("get", "post", "put", "patch", "delete")]
        joined = ", ".join(methods)
        print(f"  {path}  [{joined}]")


if __name__ == "__main__":
    main()
