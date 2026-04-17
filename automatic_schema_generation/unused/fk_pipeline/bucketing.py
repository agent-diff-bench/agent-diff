"""Role classifier — the core of step 1.

Takes a loaded spec + an AliasMap + naming config and produces a
``ResourceEndpointMap``. Pure function over its inputs — no I/O, no
side effects, easy to unit test.

The classifier runs per-operation and emits one ownership edge plus
zero-or-more reference edges. Edges are deduplicated by (resource,
endpoint) with stronger roles suppressing weaker ones (see
``models.py`` for the strength ordering).

Two passes total:

  1. Per-operation walk: URL segments + path params + query params.
     Emits OWNER_* / SUB_COLLECTION / PARENT / QUERY_REFERENCED.

  2. Schema-ref pass: walks response/request body schemas for ``$ref``
     pointers whose target component schema name matches a resource.
     Emits BODY_REFERENCED only if no stronger role already exists for
     the (resource, endpoint) pair.

Why two passes: the first pass is cheap (path+params only) and
sufficient for most ownership and parent relationships. The schema-
ref pass is more expensive (walks full operation bodies) and
deliberately runs second so its edges are always the weakest — body
references don't override stronger URL-level relationships.
"""

from __future__ import annotations

from typing import Any

from pipeline.naming import singularize
from pipeline.schema_walk import resolve_ref

from ._text import snake_case
from .config import FkNamingConfig
from .models import (
    Edge,
    EdgeRole,
    EndpointRecord,
    ResourceEndpointMap,
    role_is_stronger,
)
from .vocabulary import AliasMap


# ---------------------------------------------------------------------------
# Spec-walking primitives
#
# These used to live in a separate ``intake.py`` module, but their only
# callers are in this file (``iter_operations`` / ``merge_parameters``)
# and ``cli.py`` (``load_openapi``, which now lives there). Keeping them
# here removes a weak package boundary and puts the spec-shape
# assumptions next to the code that depends on them.
# ---------------------------------------------------------------------------


# Keys that appear on a ``paths[<path>]`` item but are NOT operations.
# Skipped when iterating so we never treat a summary/description/parameters
# block as an HTTP verb.
_NON_OPERATION_KEYS: frozenset[str] = frozenset({
    "summary", "description", "servers", "parameters", "$ref",
})

# Standard HTTP methods OpenAPI 3.x uses on path items.
_HTTP_METHODS: frozenset[str] = frozenset({
    "get", "post", "put", "patch", "delete", "head", "options", "trace",
})


def iter_operations(
    spec: dict[str, Any],
) -> list[tuple[str, str, dict[str, Any], dict[str, Any]]]:
    """Enumerate every operation in the spec.

    Yields tuples of (path, METHOD_UPPER, operation_dict, path_item_dict).
    The path item is returned so callers can reach path-level parameters
    without re-indexing.

    Non-operation keys (summary/description/parameters/servers/$ref) and
    vendor extensions that aren't recognized HTTP methods are skipped.
    """
    results = []
    for path, path_item in (spec.get("paths") or {}).items():
        if not isinstance(path_item, dict):
            continue
        for method, op in path_item.items():
            if method in _NON_OPERATION_KEYS:
                continue
            if method.lower() not in _HTTP_METHODS:
                continue
            if not isinstance(op, dict):
                continue
            results.append((path, method.upper(), op, path_item))
    return results


def merge_parameters(
    path_item: dict[str, Any],
    operation: dict[str, Any],
    spec: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Merge path-item level parameters with operation-level parameters.

    OpenAPI 3.x lets path items carry a ``parameters`` list that applies
    to every operation under that path; each operation can add more or
    override by (name, in). Operation-level entries override path-level
    with the same (name, in).

    When ``spec`` is passed, parameter ``$ref`` entries are resolved
    against ``components.parameters`` so the classifier sees concrete
    ``name``/``in`` fields. GitHub et al. make heavy use of shared
    parameter definitions — without resolution the classifier would see
    empty dicts and miss every ownership edge.
    """
    def _resolve(raw: Any) -> dict[str, Any] | None:
        if not isinstance(raw, dict):
            return None
        if spec is None or "$ref" not in raw:
            return raw
        ref = raw["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/components/parameters/"):
            return None
        name = ref.split("/")[-1]
        target = ((spec.get("components") or {}).get("parameters") or {}).get(name)
        return target if isinstance(target, dict) else None

    op_params = operation.get("parameters") or []
    path_params = path_item.get("parameters") or []
    if not isinstance(op_params, list):
        op_params = []
    if not isinstance(path_params, list):
        path_params = []

    seen: set[tuple[str, str]] = set()
    merged: list[dict[str, Any]] = []
    for raw in op_params:
        p = _resolve(raw)
        if p is None:
            continue
        seen.add((p.get("name", ""), p.get("in", "")))
        merged.append(p)
    for raw in path_params:
        p = _resolve(raw)
        if p is None:
            continue
        if (p.get("name", ""), p.get("in", "")) in seen:
            continue
        merged.append(p)
    return merged


def build_map(
    spec: dict[str, Any],
    alias_map: AliasMap,
    naming: FkNamingConfig,
) -> ResourceEndpointMap:
    """Run the full bucketing pass.

    Returns a ResourceEndpointMap with edges, endpoints, unbucketed
    endpoints, and the alias view.
    """
    # Canonical edge list. We key by (resource, endpoint_key) for dedup.
    edges_by_key: dict[tuple[str, str], Edge] = {}
    endpoints: dict[str, EndpointRecord] = {}
    unbucketed: list[EndpointRecord] = []

    def _maybe_add_edge(edge: Edge) -> None:
        """Dedupe: stronger role wins for the same (resource, endpoint)."""
        key = (edge.resource, edge.endpoint_key)
        existing = edges_by_key.get(key)
        if existing is None:
            edges_by_key[key] = edge
            return
        if role_is_stronger(edge.role, existing.role):
            edges_by_key[key] = edge

    # Pass 1: URL + path params + query params
    for path, method, op, path_item in iter_operations(spec):
        params = merge_parameters(path_item, op, spec)
        endpoint_key = f"{method} {path}"
        operation_id = op.get("operationId", "") or ""
        record = EndpointRecord(
            method=method,
            path=path,
            operation_id=operation_id,
            raw_operation=op,
            resource_edges=[],
        )
        endpoints[endpoint_key] = record

        classified = _classify_operation(
            path=path,
            method=method,
            params=params,
            alias_map=alias_map,
            naming=naming,
            endpoint_key=endpoint_key,
        )
        for edge in classified:
            _maybe_add_edge(edge)

    # Pass 2: schema $ref references in response + request body
    for endpoint_key, record in endpoints.items():
        for ref_resource, evidence in _walk_operation_for_schema_refs(
            record.raw_operation, spec, alias_map
        ):
            edge = Edge(
                resource=ref_resource,
                endpoint_key=endpoint_key,
                role=EdgeRole.BODY_REFERENCED,
                evidence=evidence,
            )
            _maybe_add_edge(edge)

    # Final edge list, attached to endpoints.
    final_edges = list(edges_by_key.values())
    for edge in final_edges:
        record = endpoints.get(edge.endpoint_key)
        if record is not None:
            record.resource_edges.append(edge)

    # Unbucketed = endpoints with no edges.
    for record in endpoints.values():
        if not record.resource_edges:
            unbucketed.append(record)

    # Alias view for the artifact header.
    alias_view: dict[str, list[str]] = {}
    for canonical, entry in alias_map.entries.items():
        full = [canonical]
        if entry.singular != canonical:
            full.append(entry.singular)
        full.extend(entry.syntactic_aliases)
        alias_view[canonical] = sorted(set(full))

    return ResourceEndpointMap(
        edges=final_edges,
        endpoints=endpoints,
        unbucketed_endpoints=unbucketed,
        resource_aliases=alias_view,
    )


# ---------------------------------------------------------------------------
# Per-operation classifier — the one non-trivial function
# ---------------------------------------------------------------------------


def _classify_operation(
    path: str,
    method: str,
    params: list[dict[str, Any]],
    alias_map: AliasMap,
    naming: FkNamingConfig,
    endpoint_key: str,
) -> list[Edge]:
    """Produce ownership + reference edges for one operation.

    Walks the URL path left-to-right finding matched segments (a
    segment whose value or singular is in the alias lookup). The
    deepest match is the owner; earlier matches become PARENT.
    Path and query params then add further reference edges.

    Edge evidence strings are written to be human-readable for
    debugging — they're the first thing an operator sees when the
    classifier does something surprising.
    """
    edges: list[Edge] = []

    segments = [s for s in path.split("/") if s]
    segment_infos = _segment_infos(segments, alias_map)
    matched = [(idx, seg, r) for idx, seg, r in segment_infos if r is not None]

    path_params = [p for p in params if p.get("in") == "path"]
    query_params = [p for p in params if p.get("in") == "query"]

    if matched:
        owner_idx, owner_seg, owner_resource = matched[-1]
        owner_singular = alias_map.entries[owner_resource].singular
        tail = segments[owner_idx + 1 :]

        owner_role, owner_evidence = _classify_ownership(
            owner_seg=owner_seg,
            owner_resource=owner_resource,
            owner_singular=owner_singular,
            tail_segments=tail,
            path_params=path_params,
            naming=naming,
            alias_map=alias_map,
            is_nested=owner_idx > 0,
        )
        edges.append(
            Edge(
                resource=owner_resource,
                endpoint_key=endpoint_key,
                role=owner_role,
                evidence=owner_evidence,
            )
        )

        # Every other matched segment becomes PARENT.
        for idx, seg, r in matched[:-1]:
            evidence = f"url_segment '{seg}' at position {idx}"
            # If the next segment is a path param, prefer naming it in
            # the evidence string — it's what the test generator will
            # actually need to seed.
            if idx + 1 < len(segments) and segments[idx + 1].startswith("{"):
                param_name = segments[idx + 1].strip("{}")
                evidence = f"path_param '{param_name}' after segment '{seg}'"
            edges.append(
                Edge(
                    resource=r,
                    endpoint_key=endpoint_key,
                    role=EdgeRole.PARENT,
                    evidence=evidence,
                )
            )

    # Path params that resolve to a resource not already in the
    # matched segments list. Covers bare-name path params like
    # {owner}, {repo}, {username} — as long as their name (or stripped
    # form) is in the alias map. Names that don't resolve are left
    # alone; step 3 (FK candidate extraction) will emit them with a
    # 'needs_semantic_review' flag, and step 6 will classify them.
    owner_resource = matched[-1][2] if matched else None
    owner_singular = (
        alias_map.entries[owner_resource].singular if owner_resource else None
    )
    for p in path_params:
        name = p.get("name", "")
        if not isinstance(name, str) or not name:
            continue
        resolved = _resolve_param_to_resource(
            name, alias_map, naming, owner_singular=owner_singular
        )
        if resolved is None:
            continue
        resource, reason = resolved
        # Skip if this is the owner's self-id param — already encoded
        # by the OWNER_ITEM role.
        if reason == "self_id":
            continue
        # Dedup will handle the case where a matched non-param segment
        # already emitted a PARENT edge.
        edges.append(
            Edge(
                resource=resource,
                endpoint_key=endpoint_key,
                role=EdgeRole.PARENT,
                evidence=f"path_param '{name}' ({reason})",
            )
        )

    # Query params → QUERY_REFERENCED.
    for p in query_params:
        name = p.get("name", "")
        if not isinstance(name, str) or not name:
            continue
        resolved = _resolve_param_to_resource(
            name, alias_map, naming, owner_singular=owner_singular
        )
        if resolved is None:
            continue
        resource, reason = resolved
        if reason == "self_id":
            continue
        edges.append(
            Edge(
                resource=resource,
                endpoint_key=endpoint_key,
                role=EdgeRole.QUERY_REFERENCED,
                evidence=f"query_param '{name}' ({reason})",
            )
        )

    return edges


def _segment_infos(
    segments: list[str],
    alias_map: AliasMap,
) -> list[tuple[int, str, str | None]]:
    """For each non-parameter segment, try to resolve it to a resource.

    Returns a list of (index, segment, canonical_resource_or_None)
    with one entry per segment (parameters included, with None).
    The index is the segment's position within the full segments list.
    """
    out: list[tuple[int, str, str | None]] = []
    for i, seg in enumerate(segments):
        if seg.startswith("{"):
            out.append((i, seg, None))
            continue
        token = seg.lower().replace("-", "_")
        resolved = alias_map.lookup.get(token) or alias_map.lookup.get(
            singularize(token)
        )
        out.append((i, seg, resolved))
    return out


def _classify_ownership(
    owner_seg: str,
    owner_resource: str,
    owner_singular: str,
    tail_segments: list[str],
    path_params: list[dict[str, Any]],
    naming: FkNamingConfig,
    alias_map: AliasMap,
    is_nested: bool,
) -> tuple[EdgeRole, str]:
    """Decide the ownership role for a matched owner segment.

    Rules:
      * If the tail is empty or only a self-id param, it's ``OWNER_ITEM``
        (when the param is present) or ``OWNER_COLLECTION`` (no param).
      * If the tail contains a non-param word that isn't a known
        resource alias, it's ``OWNER_ACTION`` (verb-style sub-path).
      * If the owner's segment is nested under a parent that itself
        matched a resource, the owner role is ``SUB_COLLECTION`` rather
        than ``OWNER_COLLECTION`` when no self-id param is present on
        the owner.

    The ``is_nested`` flag indicates whether any matched segment comes
    before the owner — that's the signal for SUB_COLLECTION.
    """
    has_self_id = _has_owner_self_id_param(
        owner_singular, path_params, naming
    )

    # Filter tail to exclude self-id params we've already accounted for.
    tail_non_params = [s for s in tail_segments if not s.startswith("{")]
    tail_params = [s for s in tail_segments if s.startswith("{")]

    if not tail_non_params:
        # Tail is empty or only parameters.
        if has_self_id:
            return EdgeRole.OWNER_ITEM, f"url_segment '{owner_seg}' + self-id path param"
        # No tail, no self-id — this is a collection operation.
        if is_nested:
            return (
                EdgeRole.SUB_COLLECTION,
                f"url_segment '{owner_seg}' as sub-collection under parent",
            )
        return EdgeRole.OWNER_COLLECTION, f"url_segment '{owner_seg}'"

    # Tail has at least one non-param word. It's either an action or
    # (rare, handled outside this function) a deeper resource segment.
    # A deeper resource wouldn't make this segment the owner in the
    # first place — the left-to-right walk picks the deepest match.
    # So any tail non-param is either an action word or a segment the
    # alias map didn't recognize.
    tail_word = tail_non_params[-1]
    return (
        EdgeRole.OWNER_ACTION,
        f"url_segment '{owner_seg}' + action '{tail_word}'",
    )


def _has_owner_self_id_param(
    owner_singular: str,
    path_params: list[dict[str, Any]],
    naming: FkNamingConfig,
) -> bool:
    """True if any path param is exactly the owner's self-id.

    A "self-id" is one of:

      * The bare owner singular name — GitHub uses ``{repo}`` directly
        as a path param to identify a repository, not ``{repo_id}``.
        This is a common pattern (``{username}``, ``{repo}``, ``{gist_id}``
        all coexist in the same spec).
      * ``<owner_singular><suffix>`` for some suffix in
        ``naming.fk_suffixes`` — the canonical REST form.
      * One of ``naming.self_id_fields`` — the bare-id fallback for
        APIs that put ``id``/``node_id`` directly in the path.

    Qualifier prefixes are NOT stripped here: ``parent_task_id`` is
    deliberately NOT treated as the self-id of ``tasks``, because
    semantically it's a parent reference, not the item being addressed.
    """
    for p in path_params:
        name = p.get("name", "")
        if not isinstance(name, str):
            continue
        if name == owner_singular:
            return True
        if name in naming.self_id_fields:
            return True
        for suffix in naming.fk_suffixes:
            if name == f"{owner_singular}{suffix}":
                return True
    return False


def _resolve_param_to_resource(
    param_name: str,
    alias_map: AliasMap,
    naming: FkNamingConfig,
    *,
    owner_singular: str | None,
) -> tuple[str, str] | None:
    """Map a parameter name to a resource via suffix/qualifier stripping.

    Returns (canonical_resource, reason) or None if the name doesn't
    resolve. ``reason`` is one of:

      * ``"self_id"`` — the name is exactly the owner's self-id. The
        caller should skip this (already encoded by OWNER_ITEM).
      * ``"direct"`` — the name (or its singular) is in alias lookup
        as-is. Covers bare-name params like ``{owner}``, ``{repo}``.
      * ``"suffix_strip"`` — name stripped of an fk_suffix matches.
        Covers ``{project_id}``, ``{repo_gid}``.
      * ``"qualifier_strip"`` — name stripped of an fk_suffix AND a
        qualifier_prefix matches. Covers ``{parent_task_id}``,
        ``{source_project_id}``.

    Lookup chain is tried in order; first match wins.
    """
    # 1. Owner self-id shortcut — skip without further work. The three
    # forms we recognize mirror ``_has_owner_self_id_param``: bare
    # singular, ``self_id_fields``, and ``<singular><fk_suffix>``.
    if owner_singular is not None:
        if param_name == owner_singular and owner_singular in alias_map.lookup:
            return alias_map.lookup[owner_singular], "self_id"
        if param_name in naming.self_id_fields and owner_singular in alias_map.lookup:
            return alias_map.lookup[owner_singular], "self_id"
        for suffix in naming.fk_suffixes:
            if param_name == f"{owner_singular}{suffix}":
                return alias_map.lookup.get(owner_singular, ""), "self_id"

    # 2. Direct match on the bare name (covers {owner}, {repo}, {username}).
    direct = alias_map.lookup.get(param_name) or alias_map.lookup.get(
        singularize(param_name)
    )
    if direct is not None:
        return direct, "direct"

    # 3. Strip an fk_suffix, then try lookup.
    for suffix in naming.fk_suffixes:
        if param_name.endswith(suffix):
            stem = param_name[: -len(suffix)]
            stripped = alias_map.lookup.get(stem) or alias_map.lookup.get(
                singularize(stem)
            )
            if stripped is not None:
                return stripped, "suffix_strip"
            # 4. Also try stripping a qualifier prefix (parent_, source_, ...)
            for prefix in naming.qualifier_prefixes:
                if stem.startswith(prefix):
                    inner = stem[len(prefix) :]
                    qualified = alias_map.lookup.get(inner) or alias_map.lookup.get(
                        singularize(inner)
                    )
                    if qualified is not None:
                        return qualified, "qualifier_strip"
            break  # only one fk_suffix can match; no point retrying

    # 5. Qualifier-prefix-only strip (no fk_suffix present, rare).
    for prefix in naming.qualifier_prefixes:
        if param_name.startswith(prefix):
            inner = param_name[len(prefix) :]
            qualified = alias_map.lookup.get(inner) or alias_map.lookup.get(
                singularize(inner)
            )
            if qualified is not None:
                return qualified, "qualifier_strip"

    return None


# ---------------------------------------------------------------------------
# Schema-ref pass — emits BODY_REFERENCED edges
# ---------------------------------------------------------------------------


def _walk_operation_for_schema_refs(
    operation: dict[str, Any],
    spec: dict[str, Any],
    alias_map: AliasMap,
) -> list[tuple[str, str]]:
    """Find $ref targets in response/request body schemas that match a resource.

    Returns a list of (canonical_resource, evidence) tuples. The
    evidence string names the schema and where it was found so
    debugging a misclassification is one grep away.

    Walk is depth-bounded (8 hops) to avoid pathological recursion on
    mutually-recursive schemas. Only ``application/json`` content is
    inspected — other media types are rare for FK references.
    """
    results: list[tuple[str, str]] = []
    seen_refs: set[str] = set()  # dedupe same $ref within the same operation

    def _record_ref(ref: str, source: str) -> None:
        if ref in seen_refs:
            return
        seen_refs.add(ref)
        if not ref.startswith("#/components/schemas/"):
            return
        schema_name = ref.split("/")[-1]
        resource = _resource_for_schema_name(schema_name, alias_map)
        if resource is None:
            return
        results.append(
            (resource, f"{source} references schema '{schema_name}'")
        )

    # Response schemas
    for code, resp in (operation.get("responses") or {}).items():
        if not isinstance(resp, dict):
            continue
        content = (resp.get("content") or {}).get("application/json") or {}
        schema = content.get("schema")
        if not isinstance(schema, dict):
            continue
        _collect_refs_from_schema(
            schema, spec, f"response[{code}]", _record_ref, depth=0
        )

    # Request body schema
    req = operation.get("requestBody") or {}
    if isinstance(req, dict):
        content = (req.get("content") or {}).get("application/json") or {}
        schema = content.get("schema")
        if isinstance(schema, dict):
            _collect_refs_from_schema(
                schema, spec, "request_body", _record_ref, depth=0
            )

    return results


_MAX_SCHEMA_WALK_DEPTH: int = 8


def _collect_refs_from_schema(
    schema: dict[str, Any],
    spec: dict[str, Any],
    source_label: str,
    record: Any,  # callable(ref: str, source: str) -> None
    *,
    depth: int,
) -> None:
    """Walk a schema collecting every ``#/components/schemas/X`` $ref it finds.

    Depth-bounded to protect against pathological recursion. Visits
    ``properties``, ``items``, ``allOf``/``oneOf``/``anyOf`` branches,
    and one hop through ``$ref``.
    """
    if depth >= _MAX_SCHEMA_WALK_DEPTH or not isinstance(schema, dict):
        return

    if "$ref" in schema:
        ref = schema["$ref"]
        if isinstance(ref, str):
            record(ref, source_label)
            resolved = resolve_ref(schema, spec)
            if isinstance(resolved, dict) and resolved is not schema:
                _collect_refs_from_schema(
                    resolved, spec, source_label, record, depth=depth + 1
                )
        return

    # Properties
    props = schema.get("properties") or {}
    if isinstance(props, dict):
        for prop in props.values():
            if isinstance(prop, dict):
                _collect_refs_from_schema(
                    prop, spec, source_label, record, depth=depth + 1
                )

    # Array items
    items = schema.get("items")
    if isinstance(items, dict):
        _collect_refs_from_schema(
            items, spec, source_label, record, depth=depth + 1
        )

    # Compositions
    for combinator in ("allOf", "oneOf", "anyOf"):
        branches = schema.get(combinator)
        if isinstance(branches, list):
            for sub in branches:
                if isinstance(sub, dict):
                    _collect_refs_from_schema(
                        sub, spec, source_label, record, depth=depth + 1
                    )


def _resource_for_schema_name(
    schema_name: str,
    alias_map: AliasMap,
) -> str | None:
    """Resolve a component schema name to a canonical resource.

    Tries the lowercased name, the snake-cased name, and the
    singularized form of each. Only returns a hit when the *whole*
    (snake-cased) name is in the alias map — sub-token matches would
    inflate the false-positive rate (``CustomFieldSetting`` contains
    ``custom``, ``field``, ``setting`` but is not itself a settings
    resource).
    """
    lowered = schema_name.lower()
    snake = snake_case(schema_name).strip("_").replace("__", "_")
    for candidate in (lowered, snake):
        hit = alias_map.lookup.get(candidate) or alias_map.lookup.get(
            singularize(candidate)
        )
        if hit is not None:
            return hit
    return None
