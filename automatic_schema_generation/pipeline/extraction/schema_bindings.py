"""Schema bindings (Group D).

Binds each component schema to a canonical resource. A schema binds
if (D1) its normalized name hits ``aliases_lookup``, or (D3) it is a
pass-through to another schema via a top-level ``$ref`` or composes
via ``allOf`` / ``oneOf`` / ``anyOf`` over already-bound schemas.
``allOf`` propagates when branches that bind agree on one target
(conflict aborts); ``oneOf`` / ``anyOf`` propagate only when every
branch agrees. Chains resolve via a fixed-point loop.

The output ``{schema_name: canonical_resource}`` map is consumed by
the property walker (Group C) and the body-level walker (Group E).
"""

from __future__ import annotations

from typing import Any

from pipeline._text import normalize_identifier
from pipeline.config import PipelineConfig

_REF_PREFIX = "#/components/schemas/"


def build_schema_bindings(
    spec: dict[str, Any],
    config: PipelineConfig,
) -> dict[str, str]:
    aliases_lookup = config.resources.aliases_lookup
    schemas = (spec.get("components") or {}).get("schemas") or {}
    if not isinstance(schemas, dict):
        return {}

    bindings: dict[str, str] = {}

    # D1. Direct name hit on component schemas.
    for name in schemas:
        resource = aliases_lookup.get(normalize_identifier(name))
        if resource is not None:
            bindings[name] = resource

    # D3. Fixed-point propagation through allOf / oneOf / anyOf. Each
    # pass only looks at already-bound ``$ref`` targets, so chained
    # compositions (A → B → User) resolve in as many passes as their
    # depth. The loop terminates when a full pass adds nothing.
    changed = True
    while changed:
        changed = False
        for name, schema in schemas.items():
            if name in bindings or not isinstance(schema, dict):
                continue
            inferred = _infer_from_composition(schema, bindings)
            if inferred is not None:
                bindings[name] = inferred
                changed = True

    return bindings


def _infer_from_composition(
    schema: dict[str, Any],
    bindings: dict[str, str],
) -> str | None:
    # Bare top-level $ref: schema is a pass-through alias for its target.
    bare_ref = _ref_binding(schema, bindings)
    if bare_ref is not None:
        return bare_ref

    # allOf: branches that bind must agree; one hit wins, conflicts abort.
    all_of_hits: set[str] = set()
    for branch in schema.get("allOf") or []:
        target = _ref_binding(branch, bindings)
        if target is not None:
            all_of_hits.add(target)
    if len(all_of_hits) == 1:
        return next(iter(all_of_hits))
    if len(all_of_hits) > 1:
        return None

    # oneOf / anyOf: every branch must resolve to the same bound target.
    for key in ("oneOf", "anyOf"):
        branches = schema.get(key) or []
        if not branches:
            continue
        targets = {_ref_binding(branch, bindings) for branch in branches}
        if None not in targets and len(targets) == 1:
            return next(iter(targets))
    return None


def _ref_binding(node: Any, bindings: dict[str, str]) -> str | None:
    if not isinstance(node, dict):
        return None
    ref = node.get("$ref")
    if not isinstance(ref, str) or not ref.startswith(_REF_PREFIX):
        return None
    return bindings.get(ref[len(_REF_PREFIX):])
