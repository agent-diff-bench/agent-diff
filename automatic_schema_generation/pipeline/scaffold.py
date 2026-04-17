"""Scaffold generator — creates the target service directory structure.

Copies template files from mockfiles/app_scaffold/ with token
replacement. Registers the replica in replicas.yaml so docker-compose
can mount and seed it immediately. Does NOT overwrite existing files.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

_TEMPLATE_DIR = Path(__file__).parent.parent / "mockfiles" / "app_scaffold"
_REPLICAS_YAML = Path(__file__).parent.parent.parent / "backend" / "src" / "services" / "replicas.yaml"

_TEMPLATE_FILES = [
    "database/base.py",
    "database/schema.py",
    "database/operations.py",
    "core/errors.py",
    "core/serializers.py",
    "core/utils.py",
    "api/routes.py",
]


def generate_scaffold(
    app_name: str,
    app_slug: str,
    target_dir: Path,
    mount_suffix: str = "",
) -> None:
    """Create directory structure, scaffold files, and register in replicas.yaml."""
    for subdir in ["api", "core", "database"]:
        (target_dir / subdir).mkdir(parents=True, exist_ok=True)

    for init_path in [
        target_dir / "__init__.py",
        target_dir / "api" / "__init__.py",
        target_dir / "core" / "__init__.py",
        target_dir / "database" / "__init__.py",
    ]:
        if not init_path.exists():
            init_path.write_text("")

    replacements = {
        "__APP_NAME__": app_name,
        "__APP_SLUG__": app_slug,
    }

    for relative_path in _TEMPLATE_FILES:
        template_path = _TEMPLATE_DIR / relative_path
        output_path = target_dir / relative_path

        if output_path.exists():
            print(f"  [skip] {relative_path}")
            continue
        if not template_path.exists():
            print(f"  [warn] template {relative_path} not found")
            continue

        content = template_path.read_text()
        for token, value in replacements.items():
            content = content.replace(token, value)
        output_path.write_text(content)
        print(f"  [create] {relative_path}")

    _register_replica(app_slug, mount_suffix)
    _register_service_enum(app_slug)


def _register_replica(app_slug: str, mount_suffix: str) -> None:
    """Append a REST entry to replicas.yaml if not already present."""
    if not _REPLICAS_YAML.exists():
        print(f"  [warn] replicas.yaml not found at {_REPLICAS_YAML}")
        return

    raw = yaml.safe_load(_REPLICAS_YAML.read_text()) or {}
    rest_entries = raw.get("rest") or []

    if any(entry.get("slug") == app_slug for entry in rest_entries):
        print(f"  [skip] {app_slug} already registered in replicas.yaml")
        return

    mount_path = f"/api/env/{{env_id}}/services/{app_slug}"
    if mount_suffix:
        mount_path += f"/{mount_suffix.strip('/')}"

    rest_entries.append({
        "slug": app_slug,
        "mount_path": mount_path,
        "routes_module": f"src.services.{app_slug}.api.routes",
        "routes_attr": "routes",
        "seed_command": f"python utils/seed_template.py --app {app_slug}",
    })
    raw["rest"] = rest_entries
    _REPLICAS_YAML.write_text(yaml.safe_dump(raw, default_flow_style=False, sort_keys=False))
    print(f"  [register] {app_slug} at {mount_path}")


_SERVICE_ENUM_PATH = Path(__file__).parent.parent.parent / "backend" / "src" / "platform" / "api" / "models.py"


def _register_service_enum(app_slug: str) -> None:
    """Add the app to the Service enum if not already present."""
    if not _SERVICE_ENUM_PATH.exists():
        print(f"  [warn] models.py not found at {_SERVICE_ENUM_PATH}")
        return

    content = _SERVICE_ENUM_PATH.read_text()
    entry = f'    {app_slug} = "{app_slug}"'
    if entry in content:
        print(f"  [skip] {app_slug} already in Service enum")
        return

    import re
    # Find the last enum member line (pattern: `    name = "name"`)
    lines = content.split("\n")
    last_member_index = -1
    in_enum = False
    for index, line in enumerate(lines):
        if "class Service" in line:
            in_enum = True
            continue
        if in_enum and re.match(r'^    \w+ = "', line):
            last_member_index = index
        if in_enum and last_member_index > 0 and line.strip() and not line.startswith(" "):
            break

    if last_member_index > 0:
        lines.insert(last_member_index + 1, entry)
        _SERVICE_ENUM_PATH.write_text("\n".join(lines))
        print(f"  [register] {app_slug} added to Service enum")
    else:
        print(f"  [warn] could not find insertion point in Service enum")


def detect_mount_suffix(spec: dict) -> str:
    """Extract API path prefix from the spec to use as mount suffix.

    If all paths share a common prefix (e.g. /api/v1), return it.
    Otherwise return empty string.
    """
    paths = list((spec.get("paths") or {}).keys())
    if not paths:
        return ""
    # Find common prefix of all paths
    parts_list = [p.strip("/").split("/") for p in paths]
    prefix_parts: list[str] = []
    for segments in zip(*parts_list):
        if len(set(segments)) == 1 and not segments[0].startswith("{"):
            prefix_parts.append(segments[0])
        else:
            break
    return "/".join(prefix_parts)
