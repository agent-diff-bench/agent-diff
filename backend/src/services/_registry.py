"""Replica registry loader.

Reads ``replicas.yaml`` (colocated in this package) and exposes typed lists
of the REST and GraphQL replicas known to the platform.

The YAML file is the source of truth — the generation pipeline edits it
when scaffolding a new replica app. This module parses it once at import
time so runtime consumers (``src.platform.api.main``, ``utils/seed_all.py``)
get type-checked dataclass instances instead of raw dicts. A typo in a
field name therefore fails at process startup rather than at request time.

See ``replicas.yaml`` for the documented field contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class RestReplica:
    """A REST replica with a shared mount pattern.

    These are wired into Starlette generically: import ``routes_module``,
    read ``routes_attr``, wrap in a ``Router``, and ``app.mount`` under
    ``mount_path``. Any app that fits this shape belongs here.
    """

    slug: str
    mount_path: str
    routes_module: str
    routes_attr: str
    seed_command: str


@dataclass(frozen=True)
class GraphQLReplica:
    """A GraphQL replica.

    Mounting is still bespoke per app (schema loading, resolver binding,
    executor construction), so only ``seed_command`` is used today. Once
    GraphQL wiring stabilizes, this dataclass can grow to drive mounting
    the same way ``RestReplica`` does.
    """

    slug: str
    seed_command: str


_REGISTRY_PATH = Path(__file__).parent / "replicas.yaml"


def _load() -> tuple[list[RestReplica], list[GraphQLReplica]]:
    """Parse ``replicas.yaml`` into typed dataclass lists.

    Called exactly once at module import. Unknown or missing fields raise
    ``TypeError`` from the dataclass constructors, which surfaces as an
    import error — loud and early.
    """
    data = yaml.safe_load(_REGISTRY_PATH.read_text()) or {}
    rest = [RestReplica(**entry) for entry in data.get("rest", [])]
    graphql = [GraphQLReplica(**entry) for entry in data.get("graphql", [])]
    return rest, graphql


REST_REPLICAS, GRAPHQL_REPLICAS = _load()
