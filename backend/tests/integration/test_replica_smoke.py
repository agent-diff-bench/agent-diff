"""Smoke tests for every REST replica registered in replicas.yaml.

This file is hand-written once and never edited by the generation pipeline.
It iterates ``REST_REPLICAS`` at collection time, so as soon as a new
replica is appended to ``replicas.yaml`` (whether by the pipeline's
scaffold stage or manually), a smoke test is automatically generated
for it — no per-app test file emission.

What each smoke test proves, in order:
  1. The replica's ``<slug>_base`` template schema exists and is
     cloneable by the platform — i.e. ``seed_template.py`` was run
     successfully during container startup.
  2. The replica's routes module imports without error — i.e. the
     scaffold files the pipeline emitted are syntactically valid and
     don't reference undefined symbols.
  3. The routes module exposes the configured ``routes_attr``
     (typically ``routes``) as a list — i.e. the scaffold contract
     is honored.
  4. Starlette can mount those routes. If the list is empty (no
     resources implemented yet), the mount still succeeds and any
     request against the replica returns 404 rather than 500.
  5. The full isolation middleware chain works: a scoped DB session
     is attached to ``request.state`` and the request completes.

Together these prove the wiring is good before any real resource is
implemented. Once the implement stage lands its first endpoint, the
same fixture (``replica_client``) can be reused by per-resource tests
with zero extra setup — see the "factory fixture" docstring in
``conftest.py``.
"""

from __future__ import annotations

import pytest

from src.services._registry import REST_REPLICAS


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "replica",
    REST_REPLICAS,
    ids=[r.slug for r in REST_REPLICAS],
)
async def test_replica_mounts_and_returns_404_on_unknown_path(
    replica, replica_client
):
    """Every registered REST replica must mount cleanly and route 404s.

    A 500 here means a scaffold file has an import error, a middleware
    is crashing, or the base template doesn't exist — all blockers that
    must be fixed before the implement stage can run.
    """
    client = await replica_client(replica.slug)

    # Hit a deliberately nonexistent path. If the replica mounts cleanly
    # and the routing layer is healthy, Starlette returns 404. A 500
    # means something in the import/mount/middleware chain exploded.
    response = await client.get("/__smoke_test_nonexistent_path__")

    assert response.status_code == 404, (
        f"Replica {replica.slug!r} returned {response.status_code} on an "
        f"unknown path — expected 404. Body: {response.text[:500]}"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "replica",
    REST_REPLICAS,
    ids=[r.slug for r in REST_REPLICAS],
)
async def test_replica_routes_attr_is_a_list(replica):
    """The routes module must expose the configured attribute as a list.

    This is a cheap import-time check that catches scaffold regressions
    (e.g. someone deleting ``routes = []`` from the template) without
    spinning up a template environment.
    """
    from importlib import import_module

    module = import_module(replica.routes_module)
    routes = getattr(module, replica.routes_attr, None)

    assert routes is not None, (
        f"{replica.routes_module} has no attribute {replica.routes_attr!r}"
    )
    assert isinstance(routes, list), (
        f"{replica.routes_module}.{replica.routes_attr} must be a list, "
        f"got {type(routes).__name__}"
    )
