"""Config loader for the fk_pipeline step.

Reads the same ``app_config.yaml`` the old pipeline uses, but only
extracts the subset this pipeline needs plus a few new fields. Unknown
keys are ignored — users can add fk_pipeline-specific config to an
existing app_config without confusing the old loader (which itself
uses ``.get()`` with defaults).

Defaults are *minimal*, not aspirational: the safest universal set,
and every app that needs more declares it explicitly. This is a
deliberate break from ``pipeline/config.py``'s grab-bag defaults —
the fk_pipeline classifier is supposed to be loose and let the LLM
disambiguate, and over-eager defaults would just bake in false
positives at match time.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from pipeline.naming import singularize


# Minimal defaults. Anything an app needs beyond these it declares
# explicitly. See the module docstring for why.
DEFAULT_FK_SUFFIXES: tuple[str, ...] = ("_id",)
DEFAULT_QUALIFIER_PREFIXES: tuple[str, ...] = ("parent_",)
DEFAULT_PK_FIELD_NAMES: tuple[str, ...] = ("id",)
DEFAULT_SELF_ID_FIELDS: tuple[str, ...] = ("id",)

# Haiku 4.5 — the cheapest model that reliably handles the closed-world
# alias classification task. Overridable per-app via ``fk_pipeline.model``.
DEFAULT_MODEL: str = "claude-haiku-4-5"

# Sonnet for the FK-resolution step. This call is harder than the
# vocabulary pass: it inspects per-candidate schema fragments and has
# to make role-word judgements (``assignee`` → ``users``) that Haiku
# is noticeably flakier on. Bumping to Sonnet is a small cost for a
# meaningful quality gain on the step that drives schema correctness.
# Overridable per-app via ``fk_pipeline.resolution_model``.
DEFAULT_RESOLUTION_MODEL: str = "claude-sonnet-4-5"

# Whether to reuse on-disk LLM caches by default. ``True`` (the safe
# default) matches historical behavior — if an ``fk_pipeline_out/``
# file exists with a matching cache key, we skip the LLM call. Set
# ``fk_pipeline.use_cache: false`` in the yaml to force regeneration
# from scratch, which is useful when iterating on prompt versions or
# deliberately re-running to get fresh LLM output.
DEFAULT_USE_CACHE: bool = True


@dataclass
class FkNamingConfig:
    """Naming vocabulary for the fk_pipeline role classifier.

    Intentionally separate from ``pipeline/config.py``'s ``NamingConfig``.
    That one has historically-motivated defaults that match the old
    walker's assumptions; this one is the minimal safe set.

    Fields:
        fk_suffixes: Token suffixes that mark a path/query/body field
            as a potential FK. Minimal default ``("_id",)`` — apps
            using ``_gid``, ``_uid``, ``_ref`` etc. add them here.

        qualifier_prefixes: Prefixes that qualify a resource reference
            without changing its target. ``parent_task_id`` strips
            ``parent_`` and ``_id`` to yield ``task`` → matches the
            ``tasks`` resource. Default ``("parent_",)``; apps that
            use ``source_``, ``root_``, ``origin_``, ``target_``,
            ``linked_`` add them here.

        pk_field_names: Field names that, when appearing inside an
            object, mark the object as carrying a primary-key reference.
            Used by the walker's nested-object case. Default ``("id",)``.

        self_id_fields: Field names that represent the entity's own
            primary key (not a FK). The walker filters these out when
            matching nested-object FKs. Default ``("id",)``.

        resource_aliases: Pinned user-declared aliases. The dict is
            keyed by the *alias* and valued by the *canonical plural*.
            Example: ``{"repository": "repos", "organization": "orgs"}``.
            These always win over LLM-produced aliases — if the user
            pinned it, we use it.
    """

    fk_suffixes: tuple[str, ...] = field(
        default_factory=lambda: tuple(DEFAULT_FK_SUFFIXES)
    )
    qualifier_prefixes: tuple[str, ...] = field(
        default_factory=lambda: tuple(DEFAULT_QUALIFIER_PREFIXES)
    )
    pk_field_names: tuple[str, ...] = field(
        default_factory=lambda: tuple(DEFAULT_PK_FIELD_NAMES)
    )
    self_id_fields: tuple[str, ...] = field(
        default_factory=lambda: tuple(DEFAULT_SELF_ID_FIELDS)
    )
    resource_aliases: dict[str, str] = field(default_factory=dict)


@dataclass
class FkPipelineConfig:
    """Top-level config for a single fk_pipeline run."""

    app_slug: str
    openapi_path: Path
    resources: list[str]
    naming: FkNamingConfig
    model: str
    # Separate model for the step-3 FK resolution pass. Defaults to
    # Sonnet (see ``DEFAULT_RESOLUTION_MODEL``) because the judgement
    # it makes per candidate is harder than the closed-world alias
    # classification Haiku runs in step 1.
    resolution_model: str
    # When True (default), reuse existing LLM cache files if the
    # cache key matches. When False, always call the LLM and rewrite
    # the cache. Applies to both the vocabulary and resolution caches.
    use_cache: bool
    # Regex patterns (as raw strings) matched with ``re.fullmatch``
    # against dict keys during vocabulary extraction. Keys that match
    # any pattern are skipped entirely — we neither tokenize the key
    # nor walk its value. Lets users exclude noisy sections like
    # ``description`` / ``summary`` / ``example`` / ``$ref`` from
    # contributing to the candidate vocabulary. Empty by default.
    vocabulary_ignore_keys: list[str]
    # Regex patterns (as raw strings) matched with ``re.fullmatch``
    # against each raw string value BEFORE tokenization. Matching
    # values are skipped — the raw case is preserved during matching,
    # so patterns like ``^[A-Z][A-Z0-9_]*$`` can target ALL_CAPS enum
    # values before they get lowercased. Also useful for hash-shaped
    # opaque identifiers (``^[a-zA-Z0-9]{31,}$``). Empty by default.
    vocabulary_ignore_values: list[str]
    # Regex patterns (as raw strings) matched with ``re.fullmatch``
    # against each token AFTER tokenization. This is the post-tokenize
    # filter layer, used to drop tokens that only become visible once
    # ``tokenize`` has split a longer string — most commonly hashes
    # embedded inside URLs (``https://.../blobs/3a0f86...`` → token
    # ``3a0f86...``, which the pre-tokenize filter can't see because
    # the whole URL doesn't match). Empty by default.
    vocabulary_ignore_tokens: list[str]
    output_dir: Path
    # The app_config.yaml file itself — kept for relative path resolution
    # and diagnostic messages.
    config_path: Path


def load_config(config_path: Path) -> FkPipelineConfig:
    """Load an fk_pipeline config from an app_config.yaml file.

    Reads the same file the old pipeline does. Only the keys below are
    consumed; everything else is ignored so this loader coexists with
    the old one on the same file.

    Accepted top-level keys:
        app_slug: str (required)
        openapi_path: path (required, relative to config file's dir)
        scoped_resources: list[str] (required)
        naming: mapping (optional; see FkNamingConfig)
        fk_pipeline: mapping (optional; step-specific overrides)

    The ``fk_pipeline`` sub-block supports:
        model: str — LLM model for alias expansion, default Haiku 4.5
        resolution_model: str — LLM model for FK resolution (step 3),
            default Sonnet (see ``DEFAULT_RESOLUTION_MODEL``). Separate
            from ``model`` because step 3 makes harder judgements and
            benefits from a stronger model.
        output_dir: path — where artifacts go, default ``<config_dir>/fk_pipeline_out/``
    """
    config_path = config_path.resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"app_config not found: {config_path}")

    with open(config_path) as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise ValueError(
            f"app_config must be a YAML mapping at top level, "
            f"got {type(data).__name__}"
        )

    config_dir = config_path.parent

    # Required fields
    try:
        app_slug = data["app_slug"]
        openapi_rel = data["openapi_path"]
        resources = data["scoped_resources"]
    except KeyError as e:
        raise ValueError(
            f"app_config is missing required key {e!s} "
            f"(need: app_slug, openapi_path, scoped_resources)"
        )

    if not isinstance(app_slug, str) or not app_slug:
        raise ValueError("app_config 'app_slug' must be a non-empty string")
    if not isinstance(resources, list) or not all(isinstance(r, str) for r in resources):
        raise ValueError("app_config 'scoped_resources' must be a list of strings")
    if not resources:
        raise ValueError("app_config 'scoped_resources' must be non-empty")

    openapi_path = (config_dir / openapi_rel).resolve()
    if not openapi_path.exists():
        raise FileNotFoundError(f"OpenAPI spec not found: {openapi_path}")

    naming = _load_naming(data.get("naming"), scoped_resources=list(resources))

    fk_block = data.get("fk_pipeline") or {}
    if not isinstance(fk_block, dict):
        raise ValueError(
            f"app_config 'fk_pipeline' must be a mapping, got {type(fk_block).__name__}"
        )
    model = fk_block.get("model", DEFAULT_MODEL)
    if not isinstance(model, str) or not model:
        raise ValueError("app_config 'fk_pipeline.model' must be a non-empty string")

    resolution_model = fk_block.get("resolution_model", DEFAULT_RESOLUTION_MODEL)
    if not isinstance(resolution_model, str) or not resolution_model:
        raise ValueError(
            "app_config 'fk_pipeline.resolution_model' must be a non-empty string"
        )

    use_cache = fk_block.get("use_cache", DEFAULT_USE_CACHE)
    if not isinstance(use_cache, bool):
        raise ValueError(
            f"app_config 'fk_pipeline.use_cache' must be a bool, "
            f"got {type(use_cache).__name__}"
        )

    # Parse + validate both regex-pattern lists with the same rules:
    # must be a list of strings, and every string must compile as a
    # regex. Compiled results are discarded — callers re-compile from
    # the raw strings so the cache key (which hashes strings) stays
    # stable across processes.
    def _load_pattern_list(field_name: str) -> list[str]:
        raw = fk_block.get(field_name, []) or []
        if not isinstance(raw, list) or not all(
            isinstance(pattern, str) for pattern in raw
        ):
            raise ValueError(
                f"app_config 'fk_pipeline.{field_name}' must be a "
                f"list of regex pattern strings"
            )
        for pattern in raw:
            try:
                re.compile(pattern)
            except re.error as err:
                raise ValueError(
                    f"app_config 'fk_pipeline.{field_name}' contains "
                    f"invalid regex {pattern!r}: {err}"
                )
        return list(raw)

    vocabulary_ignore_keys = _load_pattern_list("vocabulary_ignore_keys")
    vocabulary_ignore_values = _load_pattern_list("vocabulary_ignore_values")
    vocabulary_ignore_tokens = _load_pattern_list("vocabulary_ignore_tokens")

    output_dir_raw = fk_block.get("output_dir", "fk_pipeline_out")
    output_dir = (config_dir / output_dir_raw).resolve()

    return FkPipelineConfig(
        app_slug=app_slug,
        openapi_path=openapi_path,
        resources=list(resources),
        naming=naming,
        model=model,
        resolution_model=resolution_model,
        use_cache=use_cache,
        vocabulary_ignore_keys=vocabulary_ignore_keys,
        vocabulary_ignore_values=vocabulary_ignore_values,
        vocabulary_ignore_tokens=vocabulary_ignore_tokens,
        output_dir=output_dir,
        config_path=config_path,
    )


def _load_naming(
    raw: Any,
    *,
    scoped_resources: list[str],
) -> FkNamingConfig:
    """Build an FkNamingConfig from a raw YAML mapping.

    Missing fields fall back to the minimal defaults above. Shared with
    the old pipeline's ``naming:`` block — fields the old pipeline uses
    but this one doesn't are silently ignored, and vice versa.

    ``scoped_resources`` is passed so the ``resource_aliases`` canonical
    side can be normalized: the old pipeline's yaml uses singular
    canonicals (``repository: repo``) while this pipeline's canonicals
    are plurals (from ``scoped_resources``). We detect the singular
    form and normalize it to the matching plural so the same yaml file
    can drive both pipelines.
    """
    if raw is None:
        return FkNamingConfig()
    if not isinstance(raw, dict):
        raise ValueError(
            f"app_config 'naming' must be a mapping, got {type(raw).__name__}"
        )

    # Build a singular → plural lookup so we can normalize resource_aliases
    # values that were written in singular form for the old pipeline.
    singular_to_plural: dict[str, str] = {}
    for plural in scoped_resources:
        singular_to_plural.setdefault(singularize(plural), plural)

    def _as_tuple(key: str, default: tuple[str, ...]) -> tuple[str, ...]:
        value = raw.get(key)
        if value is None:
            return default
        if not isinstance(value, (list, tuple)):
            raise ValueError(
                f"app_config 'naming.{key}' must be a list, "
                f"got {type(value).__name__}"
            )
        return tuple(str(v) for v in value)

    aliases_raw = raw.get("resource_aliases") or {}
    if not isinstance(aliases_raw, dict):
        raise ValueError(
            f"app_config 'naming.resource_aliases' must be a mapping, "
            f"got {type(aliases_raw).__name__}"
        )
    # Coerce to str→str; surface bad types as config errors rather than
    # mysterious walker crashes later. If the canonical side is written
    # in singular form (as the old pipeline's yaml does), normalize it
    # to the matching plural from ``scoped_resources``. After
    # normalization the canonical side MUST be in ``scoped_resources``
    # — a pinned alias pointing at something that isn't a scoped
    # resource is a config mistake, and we want to surface it at load
    # time rather than deep inside the LLM phase.
    aliases: dict[str, str] = {}
    for k, v in aliases_raw.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise ValueError(
                f"app_config 'naming.resource_aliases' entries must be str→str, "
                f"got {type(k).__name__}→{type(v).__name__} for {k!r}"
            )
        canonical = v
        if canonical not in scoped_resources and canonical in singular_to_plural:
            canonical = singular_to_plural[canonical]
        if canonical not in scoped_resources:
            raise ValueError(
                f"app_config 'naming.resource_aliases' maps {k!r} → {v!r}, "
                f"but {v!r} is not in scoped_resources. "
                f"Either fix the alias or add {v!r} to scoped_resources."
            )
        aliases[k] = canonical

    return FkNamingConfig(
        fk_suffixes=_as_tuple("fk_suffixes", tuple(DEFAULT_FK_SUFFIXES)),
        qualifier_prefixes=_as_tuple(
            "qualifier_prefixes", tuple(DEFAULT_QUALIFIER_PREFIXES)
        ),
        pk_field_names=_as_tuple("pk_field_names", tuple(DEFAULT_PK_FIELD_NAMES)),
        self_id_fields=_as_tuple("self_id_fields", tuple(DEFAULT_SELF_ID_FIELDS)),
        resource_aliases=aliases,
    )
