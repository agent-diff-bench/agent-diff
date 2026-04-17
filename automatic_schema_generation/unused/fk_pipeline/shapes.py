"""Resource shape resolution.

For each scoped resource we pick ONE representative schema and
normalize it, so the FK candidate extractor walks a single canonical
shape per resource rather than every response/request body the
resource appears in. Without this, candidate counts scale with
endpoint surface area (O(endpoints × fields)) instead of with the
graph (O(resources × fields)).

Picking priority — strongest first:
    1. ``OWNER_ITEM`` response schema. This is the "single row" view
       of the resource, and it's what most FK fields live on.
    2. ``OWNER_COLLECTION`` response, unwrapped from a pagination
       envelope (``data`` / ``items`` / ``results`` / ``value`` /
       ``_embedded``).
    3. ``BODY_REFERENCED`` schema — weakest, used when a resource has
       no owned endpoints but appears as a nested field elsewhere.
    4. A component schema whose snake-cased name matches the resource
       or its singular. Absolute fallback.

Normalization, applied in order:
    * Resolve one ``$ref`` hop (bounded by a visited-set).
    * Unwrap the OpenAPI 3.1 nullable wrapper
      (``anyOf: [<schema>, {type: "null"}]``).
    * Unwrap common pagination envelopes when the envelope's only
      data-carrying property is a single known wrapper key.
    * Merge ``allOf`` branches into one flat object. On key conflict,
      warn and prefer the LAST branch (OpenAPI convention: branches
      later in the list are more specific).

The output is a ``dict[resource, ResolvedShape]`` the extractor can
walk without re-implementing any of the above.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pipeline.naming import singularize
from pipeline.schema_walk import resolve_ref, unwrap_nullable

from ._text import name_tokens
from .models import EdgeRole, ResourceEndpointMap
from .vocabulary import AliasMap


SHAPES_ARTIFACT_FILENAME: str = "resource_shapes.json"

# Keys that commonly wrap a page of items inside a collection response.
# We unwrap these when the wrapper schema has no other data-carrying
# properties (just pagination metadata). Ordered by rough frequency.
_PAGINATION_WRAPPER_KEYS: tuple[str, ...] = (
    "data",
    "items",
    "results",
    "_embedded",
    "value",
    "records",
    "nodes",
    "edges",
    "entries",
)

# Properties that appear alongside the data wrapper on paginated
# envelopes — used to detect "this is a pagination envelope, unwrap".
_PAGINATION_METADATA_KEYS: frozenset[str] = frozenset({
    "total", "total_count", "count", "page", "per_page", "size",
    "limit", "offset", "cursor", "next", "prev", "previous",
    "has_more", "has_next", "page_info", "_links", "links",
    "pagination", "meta", "_meta",
})


@dataclass
class ResolvedShape:
    """One resource's canonical, normalized schema.

    ``properties`` is a flat dict of top-level field name → resolved
    schema dict. ``source`` records how the shape was picked so
    debugging is one grep away.

    ``origin_schema_name`` is the component schema name (if any) the
    shape originally came from. The extractor uses this when reporting
    candidate source paths — if the shape came from a ``User`` schema
    the source path looks like ``("User", "assignee")`` rather than
    ``("users", "assignee")``, which matches how OpenAPI authors think
    about their data.
    """

    resource: str
    properties: dict[str, dict[str, Any]]
    source: str  # "owner_item" | "owner_collection" | "body_referenced" | "component" | "none"
    origin_endpoint: str | None = None
    origin_schema_name: str | None = None
    # Warnings raised during allOf merge / pagination unwrap. Surfaced
    # into the shapes artifact for operator review.
    warnings: list[str] = field(default_factory=list)


def resolve_shapes(
    rem: ResourceEndpointMap,
    spec: dict[str, Any],
    alias_map: AliasMap,
) -> dict[str, ResolvedShape]:
    """Pick + normalize one representative schema per resource.

    Iterates the scoped resource list (preserved via ``rem.resource_aliases``)
    and runs the priority chain for each. Resources that fail every
    source land in the output with ``source="none"`` and an empty
    property dict — downstream code treats those as "no observable
    shape, nothing to walk" rather than a hard error.
    """
    out: dict[str, ResolvedShape] = {}
    for resource in rem.resource_aliases:
        shape = _pick_shape_for_resource(resource, rem, spec, alias_map)
        out[resource] = shape
    return out


def write_shapes_artifact(
    shapes: dict[str, ResolvedShape],
    output_path: Path,
) -> None:
    """Serialize the resolved shapes for debugging / cache inspection.

    Not load-bearing for the rest of the pipeline — the extractor
    consumes shapes in memory. But a persisted artifact is useful
    when an operator wants to see *which* schema the extractor picked
    for a given resource (a common source of "why didn't it find my
    FK?" confusion).
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {}
    for resource in sorted(shapes):
        shape = shapes[resource]
        payload[resource] = {
            "source": shape.source,
            "origin_endpoint": shape.origin_endpoint,
            "origin_schema_name": shape.origin_schema_name,
            "property_names": sorted(shape.properties.keys()),
            "warnings": list(shape.warnings),
        }
    output_path.write_text(json.dumps(payload, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Picking — walk the REM to find a representative schema
# ---------------------------------------------------------------------------


def _pick_shape_for_resource(
    resource: str,
    rem: ResourceEndpointMap,
    spec: dict[str, Any],
    alias_map: AliasMap,
) -> ResolvedShape:
    """Run the picking priority chain for one resource."""
    # 1. OWNER_ITEM — the canonical single-row view.
    picked = _find_first_edge_schema(
        resource, rem, spec, role=EdgeRole.OWNER_ITEM
    )
    if picked is not None:
        endpoint_key, schema, name = picked
        shape = _build_shape(
            resource, schema, spec, source="owner_item",
            endpoint_key=endpoint_key, origin_schema_name=name,
        )
        if shape.properties:
            return shape

    # 2. OWNER_COLLECTION — unwrapped from pagination envelope.
    picked = _find_first_edge_schema(
        resource, rem, spec, role=EdgeRole.OWNER_COLLECTION
    )
    if picked is not None:
        endpoint_key, schema, name = picked
        unwrapped, unwrap_note = _unwrap_pagination(schema, spec)
        warnings: list[str] = []
        if unwrap_note:
            warnings.append(unwrap_note)
        shape = _build_shape(
            resource, unwrapped, spec, source="owner_collection",
            endpoint_key=endpoint_key, origin_schema_name=name,
            extra_warnings=warnings,
        )
        if shape.properties:
            return shape

    # 3. BODY_REFERENCED — weakest edge-derived source.
    picked = _find_first_edge_schema(
        resource, rem, spec, role=EdgeRole.BODY_REFERENCED
    )
    if picked is not None:
        endpoint_key, schema, name = picked
        shape = _build_shape(
            resource, schema, spec, source="body_referenced",
            endpoint_key=endpoint_key, origin_schema_name=name,
        )
        if shape.properties:
            return shape

    # 4. Component schema name fallback.
    component = _find_component_schema_for_resource(resource, spec, alias_map)
    if component is not None:
        name, schema = component
        shape = _build_shape(
            resource, schema, spec, source="component",
            endpoint_key=None, origin_schema_name=name,
        )
        if shape.properties:
            return shape

    # Nothing worked. Return an empty shape — the walker treats this
    # as "no observable fields, skip".
    return ResolvedShape(
        resource=resource,
        properties={},
        source="none",
    )


def _find_first_edge_schema(
    resource: str,
    rem: ResourceEndpointMap,
    spec: dict[str, Any],
    *,
    role: EdgeRole,
) -> tuple[str, dict[str, Any], str | None] | None:
    """Find the best endpoint where ``resource`` has the given role.

    Returns (endpoint_key, response_schema_dict, schema_name_or_None)
    or None. Ranks candidate endpoints by the "quality" of their
    response schema so we don't pick a narrow stats/admin endpoint
    over the canonical single-row view.

    Scoring (higher wins, ties broken by endpoint key):

      * +100 if the response schema name (snake-cased) directly
        contains the resource's canonical plural or singular as a
        whole token. This is the strongest signal that the schema
        represents the resource (e.g. ``repository`` → ``repos``,
        ``pull-request`` → ``pulls``, ``simple-user`` → ``users``).
      * +  N where N is the number of top-level properties on the
        resolved schema. A single-row schema has more properties
        than a narrow stats/summary endpoint, so this nudges the
        picker toward rich shapes when no name match is available.
      * +  5 bonus for the ``200`` response specifically — some
        endpoints bury the "real" schema in a 201/204 code.

    No alias lookup here: picking by schema name alone is more
    conservative and less brittle than reaching into alias state
    that was itself built from the same spec.
    """
    singular = (
        singularize(resource)
        if resource not in ("users",)  # common plural-only sentinel
        else "user"
    )
    best: tuple[int, str, str, dict[str, Any], str | None] | None = None
    for endpoint_key in sorted(rem.endpoints):
        record = rem.endpoints[endpoint_key]
        match = any(
            e.resource == resource and e.role == role
            for e in record.resource_edges
        )
        if not match:
            continue
        schema, name = _pick_response_schema(record.raw_operation, spec)
        if schema is None:
            continue
        score = _score_schema_for_resource(
            schema, name, spec, resource, singular
        )
        if best is None or score > best[0]:
            best = (score, endpoint_key, endpoint_key, schema, name)
    if best is None:
        return None
    _, endpoint_key, _, schema, name = best
    return endpoint_key, schema, name


def _score_schema_for_resource(
    schema: dict[str, Any],
    name: str | None,
    spec: dict[str, Any],
    resource: str,
    singular: str,
) -> int:
    """Score how well a schema represents a given resource.

    Higher is better. See ``_find_first_edge_schema`` for the scheme.
    """
    score = 0
    if name:
        tokens = name_tokens(name)
        if resource in tokens or singular in tokens:
            score += 100
    # Property count — deeper shapes beat narrow ones.
    resolved, _ = _normalize_schema(schema, spec, visited=set())
    props = resolved.get("properties") if isinstance(resolved, dict) else None
    if isinstance(props, dict):
        score += len(props)
    return score


def _pick_response_schema(
    operation: dict[str, Any],
    spec: dict[str, Any],
) -> tuple[dict[str, Any] | None, str | None]:
    """Pick a JSON response schema for an operation.

    Preference order: ``200`` → first 2xx → first response present.
    Returns (schema_dict, schema_name_if_ref) or (None, None) when no
    JSON schema is attached.
    """
    responses = operation.get("responses") or {}
    if not isinstance(responses, dict):
        return None, None
    # Ordering: 200 first, then other 2xx sorted, then anything.
    sorted_codes: list[str] = []
    if "200" in responses:
        sorted_codes.append("200")
    for code in sorted(responses):
        if code == "200":
            continue
        if code.startswith("2"):
            sorted_codes.append(code)
    for code in sorted(responses):
        if code not in sorted_codes:
            sorted_codes.append(code)

    for code in sorted_codes:
        resp = responses.get(code) or {}
        if not isinstance(resp, dict):
            continue
        content = (resp.get("content") or {}).get("application/json") or {}
        schema = content.get("schema")
        if not isinstance(schema, dict):
            continue
        name = None
        if "$ref" in schema:
            ref = schema["$ref"]
            if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
                name = ref.split("/")[-1]
        return schema, name
    return None, None


def _find_component_schema_for_resource(
    resource: str,
    spec: dict[str, Any],
    alias_map: AliasMap,
) -> tuple[str, dict[str, Any]] | None:
    """Fall back to picking a component schema by name match.

    Scoring:
      * 4 — exact match on the canonical plural.
      * 3 — exact match on the singular (so ``pull`` → ``pulls``).
      * 3 — snake-case tokenized name contains the singular as a
            whole token AND the name has no explicit qualifier like
            ``simple``/``minimal``/``public`` (keeps ``repository`` +
            ``pull-request`` but lets ``simple-user`` fall back to
            the lower-scored variant).
      * 2 — tokenized name contains the singular as a whole token
            with a qualifier — still usable, just slightly worse.
      * 1 — alias lookup maps the name back to this resource.

    On ties, the schema with the most top-level properties wins —
    that almost always picks the canonical "full" schema over a
    narrow summary/stats variant.
    """
    schemas = (spec.get("components") or {}).get("schemas") or {}
    if not isinstance(schemas, dict):
        return None
    singular = (
        alias_map.entries[resource].singular
        if resource in alias_map.entries
        else singularize(resource)
    )
    qualifier_words: frozenset[str] = frozenset({
        "simple", "minimal", "public", "private", "nested", "mini",
        "small", "summary", "slim", "basic", "compact",
    })

    best: tuple[int, int, str, dict[str, Any]] | None = None
    for name, schema in schemas.items():
        if not isinstance(name, str) or not isinstance(schema, dict):
            continue
        lowered = name.lower()
        score = 0
        if lowered == resource:
            score = 4
        elif lowered == singular:
            score = 3
        else:
            tokens = name_tokens(name)
            if singular in tokens or resource in tokens:
                if tokens & qualifier_words:
                    score = 2
                else:
                    score = 3
            elif alias_map.lookup.get(lowered) == resource or \
                    alias_map.lookup.get(singularize(lowered)) == resource:
                score = 1
            else:
                continue
        # Secondary: property count as tie-breaker.
        props = schema.get("properties") or {}
        prop_count = len(props) if isinstance(props, dict) else 0
        candidate = (score, prop_count, name, schema)
        if best is None or candidate > best:
            best = candidate
    if best is None:
        return None
    return best[2], best[3]


# ---------------------------------------------------------------------------
# Building — normalize + extract top-level properties
# ---------------------------------------------------------------------------


def _build_shape(
    resource: str,
    schema: dict[str, Any],
    spec: dict[str, Any],
    *,
    source: str,
    endpoint_key: str | None,
    origin_schema_name: str | None,
    extra_warnings: list[str] | None = None,
) -> ResolvedShape:
    """Normalize a schema and extract its top-level property dict."""
    warnings: list[str] = list(extra_warnings or [])
    resolved, merge_warnings = _normalize_schema(schema, spec, visited=set())
    warnings.extend(merge_warnings)
    props = resolved.get("properties") or {}
    if not isinstance(props, dict):
        props = {}
    # Keep each property's schema as-is (the extractor does its own
    # per-field normalization). This is where we could pre-resolve $ref
    # hops, but that would lose the provenance the extractor wants.
    clean: dict[str, dict[str, Any]] = {}
    for name, prop in props.items():
        if isinstance(name, str) and isinstance(prop, dict):
            clean[name] = prop
    return ResolvedShape(
        resource=resource,
        properties=clean,
        source=source,
        origin_endpoint=endpoint_key,
        origin_schema_name=origin_schema_name,
        warnings=warnings,
    )


def _normalize_schema(
    schema: dict[str, Any],
    spec: dict[str, Any],
    visited: set[str],
) -> tuple[dict[str, Any], list[str]]:
    """Apply $ref → nullable → allOf merge, return a flat object schema.

    ``visited`` is keyed by ``$ref`` strings, so a cycle (``A → B → A``)
    terminates by returning the partially-resolved schema rather than
    recursing forever. Per project decision: no explicit depth limit
    — the spec is finite and the visited set handles cycles.
    """
    warnings: list[str] = []

    # One level of $ref resolution with visited-set cycle protection.
    if "$ref" in schema:
        ref = schema["$ref"]
        if isinstance(ref, str):
            if ref in visited:
                return {}, warnings
            visited = visited | {ref}
            resolved = resolve_ref(schema, spec)
            if isinstance(resolved, dict):
                schema = resolved

    # Unwrap OpenAPI 3.1 nullable (anyOf wrapper).
    schema = unwrap_nullable(schema)
    if isinstance(schema, dict) and "$ref" in schema:
        ref = schema["$ref"]
        if isinstance(ref, str) and ref not in visited:
            visited = visited | {ref}
            resolved = resolve_ref(schema, spec)
            if isinstance(resolved, dict):
                schema = resolved

    if not isinstance(schema, dict):
        return {}, warnings

    # Merge allOf into a single flat object, normalizing each branch.
    all_of = schema.get("allOf")
    if isinstance(all_of, list) and all_of:
        merged_props: dict[str, Any] = {}
        conflict_keys: set[str] = set()
        for branch in all_of:
            if not isinstance(branch, dict):
                continue
            normalized_branch, branch_warnings = _normalize_schema(
                branch, spec, visited
            )
            warnings.extend(branch_warnings)
            branch_props = normalized_branch.get("properties") or {}
            if not isinstance(branch_props, dict):
                continue
            for k, v in branch_props.items():
                if k in merged_props and merged_props[k] is not v:
                    conflict_keys.add(k)
                merged_props[k] = v  # last wins
        if conflict_keys:
            warnings.append(
                "allOf merge conflict on keys "
                + ", ".join(sorted(conflict_keys))
                + " — preferring last branch"
            )
        # Also merge the schema's own direct properties (some specs
        # mix ``allOf`` + sibling ``properties``, which is legal).
        own_props = schema.get("properties") or {}
        if isinstance(own_props, dict):
            for k, v in own_props.items():
                if k in merged_props and merged_props[k] is not v:
                    conflict_keys.add(k)
                merged_props[k] = v
        return {"type": "object", "properties": merged_props}, warnings

    return schema, warnings


# ---------------------------------------------------------------------------
# Pagination envelope unwrap
# ---------------------------------------------------------------------------


def _unwrap_pagination(
    schema: dict[str, Any],
    spec: dict[str, Any],
) -> tuple[dict[str, Any], str | None]:
    """Peel a pagination envelope off a collection response.

    Returns (inner_schema, warning_or_none). The inner schema is the
    item-level shape — a single resource object — even though the
    outer schema represents a list. If nothing looks like a paginated
    envelope, the input is returned unchanged.
    """
    resolved, _ = _normalize_schema(schema, spec, visited=set())
    if not isinstance(resolved, dict):
        return schema, None

    # Direct array: just unwrap items.
    if resolved.get("type") == "array":
        items = resolved.get("items")
        if isinstance(items, dict):
            return items, None
        return schema, None

    props = resolved.get("properties") or {}
    if not isinstance(props, dict):
        return schema, None

    # Envelope heuristic: the schema is an object, it has exactly one
    # wrapper key whose value is an array, and every other top-level
    # key is a known pagination metadata name. If so, unwrap the array.
    wrapper_key: str | None = None
    for candidate in _PAGINATION_WRAPPER_KEYS:
        if candidate in props:
            wrapper_key = candidate
            break
    if wrapper_key is None:
        return schema, None

    non_wrapper_keys = set(props) - {wrapper_key}
    if non_wrapper_keys and not non_wrapper_keys.issubset(_PAGINATION_METADATA_KEYS):
        # Something on the envelope isn't a pagination meta field —
        # treat the whole thing as the shape rather than unwrap. This
        # is the safe call: if we unwrap aggressively we can lose real
        # data. Returning the envelope means the walker sees the
        # wrapper's own fields, which is at worst noisy.
        return resolved, None

    inner = props[wrapper_key]
    if not isinstance(inner, dict):
        return resolved, None
    if inner.get("type") == "array":
        items = inner.get("items")
        if isinstance(items, dict):
            return items, f"unwrapped pagination envelope via '{wrapper_key}'"
    if "$ref" in inner:
        return inner, f"unwrapped pagination envelope via '{wrapper_key}'"
    return resolved, None
