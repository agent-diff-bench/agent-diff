#!/usr/bin/env python3
"""Run every replica's seed command, in registry order.

Replaces the hardcoded chain of ``python utils/seed_<app>_template.py``
invocations that used to live in ``ops/docker-compose.yml``. The chain
is now derived from ``backend/src/services/replicas.yaml`` via the
registry loader, so adding a new replica is a single YAML append — no
compose edit needed.

Behavior:
  - Iterates REST replicas first, then GraphQL replicas. Order within
    each list matches the YAML file (no topological sorting — each app's
    templates are independent PostgreSQL schemas).
  - Runs each ``seed_command`` as a shell command with the current
    working directory set to ``backend/`` (where the seeders live).
  - Streams child stdout/stderr directly to this process's streams so
    the compose logs look identical to the old chained form.
  - Exits non-zero on the first failure. The compose ``&&`` chain
    already had this behavior; preserving it keeps startup semantics
    the same.

Usage:
    python utils/seed_all.py
"""

from __future__ import annotations

import shlex
import subprocess
import sys
from itertools import chain
from pathlib import Path

# Make ``src.services._registry`` importable when run as a script.
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services._registry import (  # noqa: E402
    GRAPHQL_REPLICAS,
    REST_REPLICAS,
    GraphQLReplica,
    RestReplica,
)


def _run(label: str, command: str) -> None:
    """Run one seed command, failing the whole script on non-zero exit."""
    print(f"\n=== Seeding {label} ===", flush=True)
    print(f"$ {command}", flush=True)

    # shell=False + shlex.split keeps argv explicit and avoids an extra
    # shell layer. Seed commands in the registry are plain argv.
    result = subprocess.run(shlex.split(command), cwd=Path(__file__).parent.parent)
    if result.returncode != 0:
        print(
            f"\nERROR: seed command for {label} failed with exit code "
            f"{result.returncode}",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(result.returncode)


def main() -> None:
    all_replicas: list[RestReplica | GraphQLReplica] = list(
        chain(REST_REPLICAS, GRAPHQL_REPLICAS)
    )

    if not all_replicas:
        print("No replicas registered in replicas.yaml — nothing to seed.")
        return

    print(
        f"Seeding {len(REST_REPLICAS)} REST + {len(GRAPHQL_REPLICAS)} "
        f"GraphQL replica(s) from replicas.yaml",
        flush=True,
    )

    for replica in all_replicas:
        _run(replica.slug, replica.seed_command)

    print(f"\nAll {len(all_replicas)} replica seed command(s) completed.", flush=True)


if __name__ == "__main__":
    main()
