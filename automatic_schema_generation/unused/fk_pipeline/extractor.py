"""FK candidate extractor — the proposal engine.

Consumes a ``ResourceEndpointMap`` + ``dict[resource, ResolvedShape]``
and emits a flat list of ``FkCandidate`` records. The extractor is
deliberately simple: it walks each resource's representative schema,
classifies each field into a ``CandidateType``, then tries to resolve
the target resource through ``alias_map.lookup`` using the same
lookup chain that ``bucketing`` uses for path/query parameters.

  * Resolved → strong candidate with inferred cardinality.
  * Not resolved → unresolved candidate marked ``needs_llm=True``.

Two passes:

  1. **Schema walk** — for each resource, walk its canonical shape.
     Top-level fields and one level of nested objects. Array items
     that are ``$ref`` objects are treated as arrays-of-refs (M:N);
     array items that are inline objects with a PK field are treated
     as inline-object M:N candidates.

  2. **Endpoint param lift** — walk path + query params of every
     endpoint that owns a resource (``OWNER_ITEM`` / ``OWNER_COLLECTION``
     / ``OWNER_ACTION`` / ``SUB_COLLECTION``). Any param name that
     looks FK-shaped and is NOT the owner's own self-id gets
     recorded. This is the only way we catch things like GitHub's
     ``pull_number`` or Jira's ``issueIdOrKey`` that live only in
     URLs, never in response bodies.

Zero role-word logic. Zero hardcoded target guesses. Everything the
alias lookup can't resolve lands in the unresolved bucket for the
next LLM step to sort out.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pipeline.naming import singularize
from pipeline.schema_walk import unwrap_nullable

from ._text import snake_case
from .candidates import (
    Cardinality,
    CandidateType,
    Confidence,
    FkCandidate,
    ResolutionReason,
)
from .config import FkNamingConfig
from .models import EdgeRole, ResourceEndpointMap
from .shapes import ResolvedShape
from .vocabulary import AliasMap


# How many hops deep into nested inline objects to recurse. Inline
# objects with a PK field short-circuit (they ARE a candidate and we
# stop walking into them). Plain nested objects are walked so we can
# find FK fields on embedded structures like ``metadata.owner_id``.
_MAX_OBJECT_RECURSION: int = 4


def extract_candidates(
    rem: ResourceEndpointMap,
    shapes: dict[str, ResolvedShape],
    alias_map: AliasMap,
    naming: FkNamingConfig,
    spec: dict[str, Any],
) -> list[FkCandidate]:
    """Run both passes and return the flat candidate list.

    The output is sorted by (source_resource, source_path, raw_target)
    so the writer can produce deterministic artifacts.
    """
    out: list[FkCandidate] = []

    # Pass 1: walk each resource shape.
    for resource, shape in shapes.items():
        if not shape.properties:
            continue
        ctx = _WalkContext(
            source_resource=resource,
            alias_map=alias_map,
            naming=naming,
            spec=spec,
            out=out,
            visited_refs=set(),
        )
        root_label = shape.origin_schema_name or resource
        for prop_name, prop_schema in shape.properties.items():
            _walk_property(
                ctx,
                (root_label, prop_name),
                prop_name,
                prop_schema,
                depth=0,
            )

    # Pass 2: endpoint path/query params.
    _walk_endpoint_params(rem, alias_map, naming, out)

    # Stable ordering for deterministic artifacts.
    out.sort(key=lambda c: (
        c.source_resource,
        tuple(c.source_path),
        c.raw_target,
        c.candidate_type.value,
    ))
    return out


# ---------------------------------------------------------------------------
# Schema walk
# ---------------------------------------------------------------------------


@dataclass
class _WalkContext:
    """Arguments that are constant across one schema walk.

    Bundling them reduces every helper's signature from 8+ arguments
    to (ctx, source_path, prop_name, schema) — the shape of data that
    actually varies between recursive calls.
    """

    source_resource: str
    alias_map: AliasMap
    naming: FkNamingConfig
    spec: dict[str, Any]
    out: list[FkCandidate]
    visited_refs: set[str]


def _walk_property(
    ctx: _WalkContext,
    source_path: tuple[str, ...],
    prop_name: str,
    prop_schema: dict[str, Any],
    depth: int,
) -> None:
    """Classify a single property as a FK candidate (or recurse).

    Dispatches on the property's schema shape, checking the strongest
    signal first so a nested object with both a PK field and a ``$ref``
    is still treated as NESTED_REF rather than INLINE_OBJECT. Each
    branch delegates to a small case handler below.
    """
    if not isinstance(prop_schema, dict):
        return

    schema = unwrap_nullable(prop_schema)
    if not isinstance(schema, dict):
        schema = prop_schema

    if _get_ref(schema) is not None:
        _classify_ref(ctx, source_path, prop_name, schema)
        return
    if schema.get("type") == "array":
        _classify_array(ctx, source_path, prop_name, schema)
        return
    if schema.get("type") == "object" or "properties" in schema:
        _classify_object(ctx, source_path, prop_name, schema, depth)
        return
    if _is_scalar_schema(schema) and _looks_fk_shaped(prop_name, ctx.naming):
        _classify_scalar(ctx, source_path, prop_name)


def _classify_ref(
    ctx: _WalkContext,
    source_path: tuple[str, ...],
    prop_name: str,
    schema: dict[str, Any],
) -> None:
    """Direct ``$ref`` → NESTED_REF candidate."""
    _emit_schema_ref_candidate(
        source_resource=ctx.source_resource,
        source_path=source_path,
        prop_name=prop_name,
        ref=_get_ref(schema),  # type: ignore[arg-type]
        candidate_type=CandidateType.NESTED_REF,
        cardinality=Cardinality.ONE_TO_MANY,
        alias_map=ctx.alias_map,
        out=ctx.out,
    )


def _classify_array(
    ctx: _WalkContext,
    source_path: tuple[str, ...],
    prop_name: str,
    schema: dict[str, Any],
) -> None:
    """Array property — three sub-cases, all emit ARRAY_OF_REFS / M:N.

    1. ``items: {$ref: X}``            → schema-ref candidate
    2. ``items: {inline obj with pk}`` → field-name candidate
    3. ``items: {scalar}, name fk-ish`` → field-name candidate

    Anything else (array of free-form objects, array of unkeyed inline
    objects) emits nothing.
    """
    items = schema.get("items")
    if not isinstance(items, dict):
        return
    items = unwrap_nullable(items) or items
    if not isinstance(items, dict):
        return

    item_ref = _get_ref(items)
    if item_ref is not None:
        _emit_schema_ref_candidate(
            source_resource=ctx.source_resource,
            source_path=source_path,
            prop_name=prop_name,
            ref=item_ref,
            candidate_type=CandidateType.ARRAY_OF_REFS,
            cardinality=Cardinality.MANY_TO_MANY,
            alias_map=ctx.alias_map,
            out=ctx.out,
        )
        return

    if _object_has_pk_field(items, ctx.naming) or (
        _is_scalar_schema(items) and _looks_fk_shaped(prop_name, ctx.naming)
    ):
        _emit_field_name_candidate(
            source_resource=ctx.source_resource,
            source_path=source_path,
            prop_name=prop_name,
            candidate_type=CandidateType.ARRAY_OF_REFS,
            cardinality=Cardinality.MANY_TO_MANY,
            alias_map=ctx.alias_map,
            naming=ctx.naming,
            out=ctx.out,
        )


def _classify_object(
    ctx: _WalkContext,
    source_path: tuple[str, ...],
    prop_name: str,
    schema: dict[str, Any],
    depth: int,
) -> None:
    """Inline object — either emit INLINE_OBJECT or recurse one level.

    If the object has a PK field (``id``/``node_id``/...) it's an
    entity reference in-disguise and emits an INLINE_OBJECT candidate.
    Otherwise we treat it as a plain wrapper (``metadata``,
    ``attributes``, ...) and walk its properties so fields like
    ``metadata.owner_id`` still surface.

    ``additionalProperties: {$ref: X}`` — a map-of-refs — is emitted as
    a separate ARRAY_OF_REFS candidate regardless.
    """
    if _object_has_pk_field(schema, ctx.naming):
        _emit_field_name_candidate(
            source_resource=ctx.source_resource,
            source_path=source_path,
            prop_name=prop_name,
            candidate_type=CandidateType.INLINE_OBJECT,
            cardinality=Cardinality.ONE_TO_MANY,
            alias_map=ctx.alias_map,
            naming=ctx.naming,
            out=ctx.out,
        )
        return

    if depth >= _MAX_OBJECT_RECURSION:
        return

    sub_props = schema.get("properties") or {}
    if isinstance(sub_props, dict):
        for sub_name, sub_schema in sub_props.items():
            if isinstance(sub_name, str) and isinstance(sub_schema, dict):
                _walk_property(
                    ctx,
                    source_path + (sub_name,),
                    sub_name,
                    sub_schema,
                    depth + 1,
                )

    # additionalProperties: a map-of-refs (``dict[str, $ref]``).
    ap = schema.get("additionalProperties")
    if isinstance(ap, dict):
        ap_ref = _get_ref(unwrap_nullable(ap) or ap)
        if ap_ref is not None:
            _emit_schema_ref_candidate(
                source_resource=ctx.source_resource,
                source_path=source_path + ("<map>",),
                prop_name=prop_name,
                ref=ap_ref,
                candidate_type=CandidateType.ARRAY_OF_REFS,
                cardinality=Cardinality.MANY_TO_MANY,
                alias_map=ctx.alias_map,
                out=ctx.out,
            )


def _classify_scalar(
    ctx: _WalkContext,
    source_path: tuple[str, ...],
    prop_name: str,
) -> None:
    """Scalar field whose name is FK-shaped (``owner_id``, ``project_gid``)."""
    _emit_field_name_candidate(
        source_resource=ctx.source_resource,
        source_path=source_path,
        prop_name=prop_name,
        candidate_type=CandidateType.SCALAR_ID,
        cardinality=Cardinality.ONE_TO_MANY,
        alias_map=ctx.alias_map,
        naming=ctx.naming,
        out=ctx.out,
    )


def _emit_schema_ref_candidate(
    source_resource: str,
    source_path: tuple[str, ...],
    prop_name: str,
    ref: str,
    candidate_type: CandidateType,
    cardinality: Cardinality,
    alias_map: AliasMap,
    out: list[FkCandidate],
) -> None:
    """Emit a candidate whose target is a component schema $ref.

    Tries alias lookup on the schema name (and its snake/singular
    variants) first. Three outcomes: linked (strong), self-referential
    (weak, LLM re-examines), or unresolved (LLM picks a target).
    """
    schema_name = ref.split("/")[-1] if "/" in ref else ref
    target = _resolve_schema_name(schema_name, alias_map)

    if target is None:
        resolved = ResolutionReason.UNRESOLVED
        target_resource = None
        confidence = Confidence.WEAK
        needs_llm = True
        evidence = f"field '{prop_name}' → unknown schema '{schema_name}'"
    elif target == source_resource:
        # Self-reference — weak, LLM decides if it's meaningful.
        resolved = ResolutionReason.SCHEMA_REF
        target_resource = target
        confidence = Confidence.WEAK
        needs_llm = True
        evidence = (
            f"field '{prop_name}' self-references schema '{schema_name}'"
        )
    else:
        resolved = ResolutionReason.SCHEMA_REF
        target_resource = target
        confidence = Confidence.STRONG
        needs_llm = False
        evidence = f"field '{prop_name}' → schema '{schema_name}'"

    out.append(
        FkCandidate(
            source_resource=source_resource,
            source_path=source_path,
            raw_target=schema_name,
            candidate_type=candidate_type,
            resolution_reason=resolved,
            target_resource=target_resource,
            inferred_cardinality=cardinality if target_resource else None,
            confidence=confidence,
            needs_llm=needs_llm,
            evidence=evidence,
        )
    )


def _emit_field_name_candidate(
    source_resource: str,
    source_path: tuple[str, ...],
    prop_name: str,
    candidate_type: CandidateType,
    cardinality: Cardinality,
    alias_map: AliasMap,
    naming: FkNamingConfig,
    out: list[FkCandidate],
) -> None:
    """Emit a candidate whose target is derived from the field name.

    Runs the same resolution chain as path/query params: direct match,
    strip fk_suffix, strip qualifier prefix, etc. Unresolved when none
    of the variants are in ``alias_map.lookup``.
    """
    resolved = _resolve_field_name(prop_name, alias_map, naming)
    if resolved is None:
        # Unresolved — LLM picks a target. raw_target is the most
        # informative variant we can compute (stem after suffix strip).
        raw_target = _strip_fk_suffix(prop_name, naming) or prop_name
        target_resource: str | None = None
        reason = ResolutionReason.UNRESOLVED
        confidence = Confidence.WEAK
        needs_llm = True
        evidence = f"field '{prop_name}' unresolved"
        card: Cardinality | None = None
    else:
        target_resource, reason, raw_target = resolved
        is_self = target_resource == source_resource
        confidence = Confidence.WEAK if is_self else Confidence.STRONG
        needs_llm = is_self
        card = cardinality
        evidence = (
            f"field '{prop_name}' self-resolves to '{target_resource}'"
            if is_self
            else f"field '{prop_name}' → resource '{target_resource}' ({reason.value})"
        )

    out.append(
        FkCandidate(
            source_resource=source_resource,
            source_path=source_path,
            raw_target=raw_target,
            candidate_type=candidate_type,
            resolution_reason=reason,
            target_resource=target_resource,
            inferred_cardinality=card,
            confidence=confidence,
            needs_llm=needs_llm,
            evidence=evidence,
        )
    )


# ---------------------------------------------------------------------------
# Endpoint param lift
# ---------------------------------------------------------------------------


# Roles that mark an endpoint as "owning" a resource for the purposes
# of the param-lift pass. SUB_COLLECTION is included so nested
# endpoints like ``/projects/{project_id}/tasks`` attach their query
# params to ``tasks`` too.
_OWNER_ROLES: frozenset[EdgeRole] = frozenset({
    EdgeRole.OWNER_ITEM,
    EdgeRole.OWNER_COLLECTION,
    EdgeRole.OWNER_ACTION,
    EdgeRole.SUB_COLLECTION,
})


def _walk_endpoint_params(
    rem: ResourceEndpointMap,
    alias_map: AliasMap,
    naming: FkNamingConfig,
    out: list[FkCandidate],
) -> None:
    """Lift FK-shaped path + query params into candidates.

    For every endpoint that owns a resource, walk the endpoint's raw
    parameters and emit a candidate for each one whose stem resolves
    (or doesn't) via the alias map. We intentionally do NOT inspect
    the OpenAPI ``schema`` field of the param — a param named
    ``project_id`` with schema ``integer`` is enough signal on its
    own, and anything fancier is duplicate work of pass 1.

    The owner's self-id param is skipped (already encoded by the
    OWNER_ITEM edge in bucketing). We deliberately do NOT filter out
    params whose target is already a PARENT / QUERY_REFERENCED /
    BODY_REFERENCED edge on the same endpoint — bucketing's output
    and the candidate list are two different views of the same
    underlying relationships, and the candidate list is supposed to
    be complete (cardinality, source field path, stem info) even
    when the bucketing edge already expresses the link.
    """
    for endpoint_key in sorted(rem.endpoints):
        record = rem.endpoints[endpoint_key]
        owner_resources = [
            e.resource for e in record.resource_edges if e.role in _OWNER_ROLES
        ]
        if not owner_resources:
            continue

        params = record.raw_operation.get("parameters") or []
        if not isinstance(params, list):
            continue

        for owner in owner_resources:
            owner_singular = (
                alias_map.entries[owner].singular
                if owner in alias_map.entries
                else singularize(owner)
            )

            for param in params:
                if not isinstance(param, dict):
                    continue
                name = param.get("name", "")
                loc = param.get("in", "")
                if not isinstance(name, str) or not name:
                    continue
                if loc not in ("path", "query"):
                    continue

                # Skip the owner's own self-id forms.
                if _is_owner_self_id(name, owner_singular, naming):
                    continue

                # Classify shape for the candidate record.
                candidate_type = (
                    CandidateType.PATH_PARAM_FK
                    if loc == "path"
                    else CandidateType.QUERY_PARAM_FK
                )

                resolved = _resolve_field_name(name, alias_map, naming)
                if resolved is not None:
                    target, reason, raw_target = resolved
                    if target == owner:
                        # Same-resource reference (a second copy of
                        # the owner's id under a different param
                        # name). Skip silently.
                        continue
                    out.append(
                        FkCandidate(
                            source_resource=owner,
                            source_path=(endpoint_key, f"{loc}.{name}"),
                            raw_target=raw_target,
                            candidate_type=candidate_type,
                            resolution_reason=reason,
                            target_resource=target,
                            inferred_cardinality=Cardinality.ONE_TO_MANY,
                            confidence=Confidence.STRONG,
                            needs_llm=False,
                            evidence=(
                                f"{loc}_param '{name}' → resource "
                                f"'{target}' ({reason.value})"
                            ),
                        )
                    )
                    continue

                # Only record unresolved params that LOOK fk-shaped.
                # A plain ``q`` or ``limit`` param is not a FK signal
                # and pass-1 body walking won't pick it up either.
                if not _looks_fk_shaped(name, naming):
                    continue
                raw_target = _strip_fk_suffix(name, naming) or name
                out.append(
                    FkCandidate(
                        source_resource=owner,
                        source_path=(endpoint_key, f"{loc}.{name}"),
                        raw_target=raw_target,
                        candidate_type=candidate_type,
                        resolution_reason=ResolutionReason.UNRESOLVED,
                        target_resource=None,
                        inferred_cardinality=None,
                        confidence=Confidence.WEAK,
                        needs_llm=True,
                        evidence=f"{loc}_param '{name}' unresolved",
                    )
                )


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


_SCALAR_TYPES: frozenset[str] = frozenset({
    "string", "integer", "number", "boolean",
})


def _is_scalar_schema(schema: dict[str, Any]) -> bool:
    """True if the schema is a plain scalar (no $ref, no object/array)."""
    if "$ref" in schema:
        return False
    t = schema.get("type")
    if isinstance(t, str):
        return t in _SCALAR_TYPES
    # No explicit type + no $ref + no object/array markers → treat as
    # scalar. Some specs omit ``type`` for scalar fields.
    if "properties" in schema or "items" in schema:
        return False
    return True


def _get_ref(schema: dict[str, Any]) -> str | None:
    """Return the ``$ref`` string on the schema, if any."""
    ref = schema.get("$ref")
    if isinstance(ref, str) and ref:
        return ref
    return None


def _object_has_pk_field(
    schema: dict[str, Any],
    naming: FkNamingConfig,
) -> bool:
    """True if a schema object has one of the configured PK field names.

    Used to detect "this nested object IS an entity with an id" — the
    walker treats those as INLINE_OBJECT candidates rather than
    recursing into them.
    """
    if not isinstance(schema, dict):
        return False
    props = schema.get("properties")
    if not isinstance(props, dict):
        return False
    for pk in naming.pk_field_names:
        if pk in props:
            return True
    return False


def _looks_fk_shaped(name: str, naming: FkNamingConfig) -> bool:
    """True if the field name ends with any configured fk_suffix."""
    for suffix in naming.fk_suffixes:
        if name.endswith(suffix) and len(name) > len(suffix):
            return True
    return False


def _strip_fk_suffix(name: str, naming: FkNamingConfig) -> str | None:
    """Return the field-name stem after stripping the first matching fk_suffix.

    Returns None if no suffix matches. Callers use this to build
    ``raw_target`` for unresolved candidates.
    """
    for suffix in naming.fk_suffixes:
        if name.endswith(suffix) and len(name) > len(suffix):
            return name[: -len(suffix)]
    return None


def _is_owner_self_id(
    name: str,
    owner_singular: str,
    naming: FkNamingConfig,
) -> bool:
    """Mirror of bucketing._has_owner_self_id_param for a single name.

    Used during endpoint param lift so we don't emit a candidate for
    the owner's own self-id parameter (already encoded by the
    OWNER_ITEM edge on the endpoint).
    """
    if name == owner_singular:
        return True
    if name in naming.self_id_fields:
        return True
    for suffix in naming.fk_suffixes:
        if name == f"{owner_singular}{suffix}":
            return True
    return False


def _resolve_field_name(
    name: str,
    alias_map: AliasMap,
    naming: FkNamingConfig,
) -> tuple[str, ResolutionReason, str] | None:
    """Resolve a field/param name to a canonical resource.

    Returns (canonical, reason, raw_target) or None. ``raw_target``
    is the stem the walker resolved on — useful for evidence strings
    and for matching back to the LLM output later.

    Lookup chain (mirrors bucketing._resolve_param_to_resource minus
    the owner-self-id short-circuit):

      1. Direct: the name (or its singular) is in ``alias_map.lookup``.
      2. Suffix strip: name without the fk_suffix is in lookup.
      3. Qualifier + suffix strip: name without qualifier_prefix and
         fk_suffix is in lookup.
      4. Qualifier prefix alone: name without qualifier_prefix is in
         lookup.
    """
    # 1. Direct
    direct = alias_map.lookup.get(name) or alias_map.lookup.get(singularize(name))
    if direct is not None:
        return direct, ResolutionReason.DIRECT, name

    # 2. Suffix strip, then optional qualifier strip.
    for suffix in naming.fk_suffixes:
        if name.endswith(suffix) and len(name) > len(suffix):
            stem = name[: -len(suffix)]
            stripped = alias_map.lookup.get(stem) or alias_map.lookup.get(
                singularize(stem)
            )
            if stripped is not None:
                return stripped, ResolutionReason.SUFFIX_STRIP, stem
            for prefix in naming.qualifier_prefixes:
                if stem.startswith(prefix):
                    inner = stem[len(prefix):]
                    qualified = alias_map.lookup.get(inner) or alias_map.lookup.get(
                        singularize(inner)
                    )
                    if qualified is not None:
                        return (
                            qualified,
                            ResolutionReason.QUALIFIER_STRIP,
                            inner,
                        )
            break

    # 3. Qualifier strip without a suffix.
    for prefix in naming.qualifier_prefixes:
        if name.startswith(prefix):
            inner = name[len(prefix):]
            qualified = alias_map.lookup.get(inner) or alias_map.lookup.get(
                singularize(inner)
            )
            if qualified is not None:
                return qualified, ResolutionReason.QUALIFIER_STRIP, inner

    return None


def _resolve_schema_name(
    schema_name: str,
    alias_map: AliasMap,
) -> str | None:
    """Map a component schema name to a canonical resource via alias lookup.

    Tries lowercased, snake-cased, and singularized variants. Returns
    None if nothing matches — those become UNRESOLVED candidates.
    """
    lowered = schema_name.lower()
    snake = snake_case(schema_name)
    for candidate in (lowered, snake):
        hit = alias_map.lookup.get(candidate) or alias_map.lookup.get(
            singularize(candidate)
        )
        if hit is not None:
            return hit
    return None
