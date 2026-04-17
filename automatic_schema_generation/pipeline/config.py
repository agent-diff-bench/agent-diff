"""Config loader — reads app.yaml into a validated PipelineConfig.

Also provides ``auto_configure_resources`` which calls an LLM to
populate aliases and primary keys from the OpenAPI spec.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

from ._text import IDENTIFIER_PATTERN, normalize_identifier


# ---------------------------------------------------------------------------
# Constants + defaults
# ---------------------------------------------------------------------------


_DEFAULT_PRIMARY_KEY: str = "id"

_DEFAULT_QUALIFIER_PREFIXES: tuple[str, ...] = ("parent_",)
_DEFAULT_SELF_ID_FIELDS: tuple[str, ...] = ("id",)
_DEFAULT_PK_FIELD_NAMES: tuple[str, ...] = ("id",)


# ---------------------------------------------------------------------------
# Dataclass hierarchy
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ResourcesConfig:
    """Closed-world resource definitions.

    ``aliases_lookup``: alias → canonical (reverse map for O(1) token resolution).
    ``aliases_by_resource``: canonical → frozenset of expanded aliases.
    ``primary_keys_lookup``: canonical → PK column name.

    Each alias is expanded with PK field names at load time so ``user``
    yields ``user``, ``user_id``, ``user_node_id`` in the lookup.
    """

    aliases_lookup: Mapping[str, str]
    aliases_by_resource: Mapping[str, frozenset[str]]
    primary_keys_lookup: Mapping[str, str]


@dataclass(frozen=True)
class NamingConfig:
    """Global naming rules applied uniformly across all resources."""

    qualifier_prefixes: tuple[str, ...] = field(
        default_factory=lambda: tuple(_DEFAULT_QUALIFIER_PREFIXES)
    )
    self_id_fields: tuple[str, ...] = field(
        default_factory=lambda: tuple(_DEFAULT_SELF_ID_FIELDS)
    )
    pk_field_names: tuple[str, ...] = field(
        default_factory=lambda: tuple(_DEFAULT_PK_FIELD_NAMES)
    )


@dataclass(frozen=True)
class PipelineConfig:
    """Top-level config for a single pipeline run."""

    app_slug: str
    app_name: str
    openapi_path: Path
    target_dir: Path
    resources: ResourcesConfig
    naming: NamingConfig
    config_path: Path


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------


def load_config(config_path: Path) -> PipelineConfig:
    """Parse a per-app yaml into a ``PipelineConfig``.
    """
    config_path = config_path.resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"app_config not found: {config_path}")

    with open(config_path) as handle:
        raw = yaml.safe_load(handle) or {}
    if not isinstance(raw, dict):
        raise ValueError(
            f"app_config must be a YAML mapping at top level, "
            f"got {type(raw).__name__}"
        )

    config_dir = config_path.parent

    # Required top-level fields.
    app_slug = _require_string(raw, "app_slug")
    app_name = _require_string(raw, "app_name")
    openapi_relative = _require_string(raw, "openapi_path")
    target_relative = _require_string(raw, "target_dir")

    openapi_path = (config_dir / openapi_relative).resolve()
    if not openapi_path.exists():
        raise FileNotFoundError(f"OpenAPI spec not found: {openapi_path}")
    target_dir = (config_dir / target_relative).resolve()

    # Naming — parsed before resources so alias expansion can use pk_field_names.
    naming_raw = raw.get("naming") or {}
    if not isinstance(naming_raw, dict):
        raise ValueError(
            f"app_config 'naming' must be a mapping, "
            f"got {type(naming_raw).__name__}"
        )
    naming = NamingConfig(
        qualifier_prefixes=_as_string_tuple(
            naming_raw, "naming.qualifier_prefixes", _DEFAULT_QUALIFIER_PREFIXES
        ),
        self_id_fields=_as_string_tuple(
            naming_raw, "naming.self_id_fields", _DEFAULT_SELF_ID_FIELDS
        ),
        pk_field_names=_as_string_tuple(
            naming_raw, "naming.pk_field_names", _DEFAULT_PK_FIELD_NAMES
        )
    )

    resources_raw = raw.get("resources")
    if not isinstance(resources_raw, dict) or not resources_raw:
        raise ValueError(
            "app_config 'resources' must be a non-empty mapping of "
            "canonical_name → {aliases, ...}"
        )

    aliases_lookup: dict[str, str] = {}
    aliases_by_resource: dict[str, frozenset[str]] = {}
    primary_keys_lookup: dict[str, str] = {}

    for canonical, resource_raw in resources_raw.items():
        if not isinstance(canonical, str) or not canonical:
            raise ValueError(
                f"app_config 'resources' key must be a non-empty string, "
                f"got {canonical!r}"
            )
        # Resource keys become table names — must be strict snake_case.
        if not IDENTIFIER_PATTERN.fullmatch(canonical):
            raise ValueError(
                f"app_config 'resources' key {canonical!r} must be a "
                f"snake_case identifier (lowercase letters, digits, and "
                f"underscores only, starting with a letter) — e.g. "
                f"``pull_request`` instead of ``PullRequest`` / "
                f"``pull-request`` / ``pullRequest``"
            )
        if not isinstance(resource_raw, dict):
            raise ValueError(
                f"app_config 'resources.{canonical}' must be a mapping, "
                f"got {type(resource_raw).__name__}"
            )

        aliases_raw = resource_raw.get("aliases") or []
        if not isinstance(aliases_raw, list) or not all(
            isinstance(alias, str) for alias in aliases_raw
        ):
            raise ValueError(
                f"app_config 'resources.{canonical}.aliases' must be a "
                f"list of strings"
            )

        default_primary_key = (
            naming.pk_field_names[0]
            if naming.pk_field_names
            else _DEFAULT_PRIMARY_KEY
        )
        primary_key = resource_raw.get("primary_key", default_primary_key)
        if not isinstance(primary_key, str) or not primary_key:
            raise ValueError(
                f"app_config 'resources.{canonical}.primary_key' must be a "
                f"non-empty string, got {primary_key!r}"
            )

        base_aliases: set[str] = {canonical}
        for alias in aliases_raw:
            normalized = normalize_identifier(alias)
            if not normalized:
                raise ValueError(
                    f"app_config 'resources.{canonical}.aliases' "
                    f"contains {alias!r}, which normalizes to an empty "
                    f"string — aliases must contain at least one letter"
                )
            base_aliases.add(normalized)

        # Expand aliases with PK suffixes: user → user, user_id, user_node_id
        pk_names: set[str] = set(naming.pk_field_names)
        pk_names.update(naming.self_id_fields)
        pk_names.add(primary_key)
        aliases = set(base_aliases)
        for alias in base_aliases:
            if any(alias.endswith(f"_{pk_name}") for pk_name in pk_names):
                continue
            for pk_name in pk_names:
                aliases.add(f"{alias}_{pk_name}")

        for alias in aliases:
            previous = aliases_lookup.get(alias)
            if previous is not None and previous != canonical:
                raise ValueError(
                    f"alias {alias!r} appears in both 'resources.{previous}' "
                    f"and 'resources.{canonical}' — each alias must map to "
                    f"exactly one canonical resource"
                )
            aliases_lookup[alias] = canonical

        aliases_by_resource[canonical] = frozenset(aliases)
        primary_keys_lookup[canonical] = primary_key

    resources = ResourcesConfig(
        aliases_lookup=MappingProxyType(aliases_lookup),
        aliases_by_resource=MappingProxyType(aliases_by_resource),
        primary_keys_lookup=MappingProxyType(primary_keys_lookup),
    )

    return PipelineConfig(
        app_slug=app_slug,
        app_name=app_name,
        openapi_path=openapi_path,
        target_dir=target_dir,
        resources=resources,
        naming=naming,
        config_path=config_path,
    )


# ---------------------------------------------------------------------------
# Small validation helpers — shared between fields
# ---------------------------------------------------------------------------


def _require_string(raw: dict[str, Any], key: str) -> str:
    """Read a required top-level string field or raise with the field name."""
    value = raw.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(
            f"app_config '{key}' must be a non-empty string, got {value!r}"
        )
    return value


def _as_string_tuple(
    raw: dict[str, Any],
    field_path: str,
    default: tuple[str, ...],
) -> tuple[str, ...]:
    """Read an optional ``list[str]`` field into a tuple, fallback to default."""
    # ``field_path`` is the dotted path used in error messages; the
    # raw dict is the parent scope (``naming``/``vocabulary``/...).
    key = field_path.split(".")[-1]
    value = raw.get(key)
    if value is None:
        return default
    if not isinstance(value, (list, tuple)) or not all(
        isinstance(entry, str) for entry in value
    ):
        raise ValueError(
            f"app_config '{field_path}' must be a list of strings, "
            f"got {type(value).__name__}"
        )
    return tuple(value)


# ---------------------------------------------------------------------------
# Auto-configure — LLM populates aliases and PKs from the spec
# ---------------------------------------------------------------------------

_AUTO_CONFIGURE_PROMPT = """\
Read the OpenAPI spec at: {spec_path}

For each resource listed below, examine the spec's component schemas, endpoint
paths, parameters, and response bodies. Then output a YAML block with:

1. **aliases**: every name/variant the spec uses to refer to this resource.
   You MUST include both singular AND plural forms (e.g. user AND users,
   project AND projects). Also include:
   - Role words that resolve to this resource (e.g. owner, assignee, creator,
     author, committer, collaborator all map to users)
   - Schema name variants (e.g. simple_user, full_repository, task_compact)
   - Abbreviated forms (e.g. repo for repository, pr for pull_request)
   Normalize everything to snake_case.

   Do NOT include as aliases:
   - Field or column names that describe a property of the entity, not a
     name for the entity itself
   - Generic positional or structural words that describe where an entity
     sits in a relationship, not what the entity is
   - Abbreviations you invented that do not appear anywhere in the spec

2. **primary_key**: the field name used as the unique identifier. Default is
   "id" — only override if the spec uses something else (e.g. "sha" for
   commits, "name" for branches, "gid" for Asana-style APIs).

3. **self_id_fields**: fields that represent the entity's own identity (not a
   FK to another resource). Usually just the primary key, but some APIs have
   multiple identity fields (e.g. "id" and "node_id" for GitHub, "gid" for
   Asana). Only include if different from the default ["id"].

Resources to configure: {resource_names}

Respond ONLY with a YAML block (no markdown fences, no prose), like:

users:
  aliases:
    - user
    - users
    - owner
    - author
  primary_key: id
projects:
  aliases:
    - project
    - projects
  primary_key: gid
  self_id_fields:
    - gid
"""


def auto_configure_resources(
    config_path: Path,
    spec_path: Path,
    resource_names: list[str],
    llm_call: Callable[[str], str],
) -> None:
    """Call an LLM to populate aliases and PKs, then write to config YAML."""
    prompt = _AUTO_CONFIGURE_PROMPT.format(
        spec_path=spec_path,
        resource_names=", ".join(resource_names),
    )
    response = llm_call(prompt)
    parsed = _parse_auto_configure_response(response, resource_names)

    raw = yaml.safe_load(config_path.read_text()) or {}
    resources_raw = raw.get("resources") or {}
    for resource_name, resource_config in parsed.items():
        existing = resources_raw.get(resource_name) or {}
        existing_aliases = existing.get("aliases") or []
        merged_aliases = sorted(set(existing_aliases) | set(resource_config.get("aliases", [])))
        resources_raw[resource_name] = {"aliases": merged_aliases}
        primary_key = resource_config.get("primary_key")
        if primary_key and primary_key != "id":
            resources_raw[resource_name]["primary_key"] = primary_key
        self_id_fields = resource_config.get("self_id_fields")
        if self_id_fields:
            resources_raw[resource_name]["self_id_fields"] = self_id_fields

    # Merge self_id_fields into naming if any resource specified them
    all_self_ids: set[str] = set()
    for resource_entry in resources_raw.values():
        if isinstance(resource_entry, dict):
            for field in resource_entry.get("self_id_fields") or []:
                all_self_ids.add(field)
    if all_self_ids:
        naming = raw.get("naming") or {}
        existing_self_ids = set(naming.get("self_id_fields") or [])
        naming["self_id_fields"] = sorted(existing_self_ids | all_self_ids)
        raw["naming"] = naming

    raw["resources"] = resources_raw
    config_path.write_text(yaml.safe_dump(raw, default_flow_style=False, sort_keys=False))


def _parse_auto_configure_response(
    response: str,
    resource_names: list[str],
) -> dict:
    """Parse the LLM's YAML response into {resource: {aliases, primary_key}}."""
    # Strip markdown fences if present
    text = response.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]

    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError:
        return {}
    if not isinstance(parsed, dict):
        return {}

    result = {}
    for resource_name in resource_names:
        entry = parsed.get(resource_name)
        if not isinstance(entry, dict):
            continue
        aliases = entry.get("aliases") or []
        if not isinstance(aliases, list):
            continue
        config_entry: dict[str, Any] = {"aliases": [str(alias) for alias in aliases]}
        primary_key = entry.get("primary_key")
        if isinstance(primary_key, str) and primary_key:
            config_entry["primary_key"] = primary_key
        self_id_fields = entry.get("self_id_fields")
        if isinstance(self_id_fields, list) and all(isinstance(field, str) for field in self_id_fields):
            config_entry["self_id_fields"] = self_id_fields
        result[resource_name] = config_entry
    return result
