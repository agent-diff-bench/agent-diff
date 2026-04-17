#!/usr/bin/env python3
"""Generic seed script for creating per-app template schemas.

Usage:
    python backend/utils/seed_template.py --app slack
    python backend/utils/seed_template.py --app calendar
    python backend/utils/seed_template.py --app todoist

================================================================================
Overview
================================================================================

This script is intentionally app-agnostic. It takes an ``--app <slug>``
argument, imports that app's SQLAlchemy models, and builds one or more
PostgreSQL *template schemas* in the database pointed at by
``DATABASE_URL``:

  - A ``<app>_base`` schema containing every table the app defines, with
    zero rows. Always produced.
  - One ``<stem>`` schema for every ``*.json`` file found under
    ``backend/seeds/<app>/`` (or the fallback ``examples/<app>/seeds/``),
    seeded with that file's contents.

Each template is registered as a public template in the platform meta DB
(``public.environments``) so the rest of agent-diff can clone it for
per-test environments.

Steps performed per template, inside a single transaction:
  1. ``DROP SCHEMA IF EXISTS <template> CASCADE`` then ``CREATE SCHEMA``.
  2. ``Base.metadata.create_all`` with ``schema_translate_map={None: <template>}``
     so the same ORM models populate any schema name at runtime.
  3. If a seed file is provided, insert rows table-by-table in
     ``Base.metadata.sorted_tables`` order (FK-safe topological order).
  4. Insert a row into ``public.environments`` — skipped if a row with the
     same ``(service, name, version, visibility)`` already exists, to
     preserve that row's stable identity across reseedings.

Cross-template isolation is by design: each template is a separate
PostgreSQL schema (a namespace inside the same database), so inconsistent
data across two seed files describes two parallel worlds, not a conflict.

================================================================================
Per-app contract — what each app's schema must honor
================================================================================

For this script to work on an app without any per-app customization,
that app must satisfy the following contract:

  1. Layout. The package exists at ``backend/src/services/<app>/database/``
     and contains:
       - ``base.py`` exporting a top-level ``Base`` (the SQLAlchemy
         declarative base).
       - ``schema.py`` importing ``Base`` from ``base`` and defining every
         ORM model against it.
     Importing ``schema.py`` is what populates ``Base.metadata.tables``,
     so models must be declared eagerly at module-import time — not in
     conditional branches or lazy-import helpers.

  2. No explicit schema on models. No model may set
     ``__table_args__ = {"schema": "..."}``. The template-building trick
     depends on ``schema_translate_map={None: <template>}``, which only
     rewrites tables whose schema is ``None``. An explicit schema on a
     model would break per-template isolation and cause rows to land in
     the wrong namespace.

  3. No cross-schema foreign keys. A ``ForeignKey("other_schema.t.col")``
     is stored as literal text and does not get rewritten by the
     translate map. Keep all FK targets within the app's own models.

  4. No circular FK cycles between different tables. SQLAlchemy's
     ``sorted_tables`` raises ``CircularDependencyError`` on cycles.
     Self-referential FKs on a single table are fine (SQLAlchemy
     special-cases them); see the seed-authoring note below.

  5. Column types that survive a JSON round-trip. The seed format is
     JSON, and this script's type handling is deliberately minimal:

     Supported (works today):
       - Primitives: ``INTEGER``, ``BIGINT``, ``TEXT``, ``VARCHAR``,
         ``BOOLEAN``, ``FLOAT``, ``NUMERIC`` (as a string in JSON to
         preserve precision).
       - ``TIMESTAMP``, ``DATE``, ``TIME`` — seed as ISO-8601 strings;
         PostgreSQL implicitly casts them.
       - ``UUID`` — seed as string; PostgreSQL implicitly casts.
       - ``JSONB`` / ``JSON`` — seed as a nested dict/list; the script
         detects these and runs ``json.dumps`` before binding.

     NOT supported (the script will silently misbehave or raise):
       - ``ARRAY(...)`` columns. A Python list in the seed JSON gets
         ``json.dumps``'d and sent as JSON text, which PostgreSQL rejects
         when the column type is ``text[]`` / ``integer[]`` / etc. If a
         future app needs arrays, ``_encode_value`` must grow a branch
         that looks up the target column's type and leaves lists intact
         for ``ARRAY`` columns (psycopg2 binds Python lists to arrays
         natively). Until then, prefer ``JSONB`` for list-shaped fields.
       - ``LargeBinary`` / ``BYTEA`` columns seeded from JSON. JSON has
         no bytes type, so seed authors would have to base64-encode, and
         this script does not decode. Apps needing binary content (e.g.
         Box's file contents) must compile those rows via an upstream
         build step that emits pre-decoded rows, or keep a bespoke
         seed script.

  6. Schema-level concerns live in ``schema.py``, not here. Anything
     that shapes the DDL — PostgreSQL extensions, custom indexes,
     triggers for derived columns, views, materialized views — belongs
     in the app's ``schema.py`` via SQLAlchemy DDL constructs and event
     listeners, e.g.::

         from sqlalchemy import DDL, event, Index
         event.listen(
             Base.metadata,
             "before_create",
             DDL("CREATE EXTENSION IF NOT EXISTS pg_trgm"),
         )

         class BoxFile(Base):
             __tablename__ = "box_files"
             name = mapped_column(String(255))
             __table_args__ = (
                 Index(
                     "ix_box_files_name_trgm", "name",
                     postgresql_using="gin",
                     postgresql_ops={"name": "gin_trgm_ops"},
                 ),
             )

     Declaring these in ``schema.py`` means ``Base.metadata.create_all``
     emits them for every template automatically, and this seeder needs
     no knowledge of them.

================================================================================
Seed-authoring notes
================================================================================

Seed JSONs are dict-of-table-to-list-of-records:

    {
      "teams":  [{"id": "T001", "name": "Acme"}, ...],
      "users":  [{"id": "U001", "team_id": "T001", ...}, ...]
    }

Column keys must match the model's column names exactly (the seeder
validates this against ``Base.metadata`` and raises on unknown columns
before any insert runs).

Inter-table FK ordering is handled by ``Base.metadata.sorted_tables`` —
parents are inserted before children automatically.

Intra-table ordering is the seed author's responsibility. If a table has
a self-referential FK (e.g. ``todoist_projects.parent_id -> .id``),
records in that table's JSON array must list parents before children.
Records are inserted in the order they appear in the array; a child
listed before its parent will trigger an FK violation and abort the
template.

Duplicate primary keys or FK violations within a seed file propagate as
PostgreSQL errors, rolling back the entire template's transaction. The
schema is dropped, and because ``main`` does not catch these exceptions,
any later templates in the same run are skipped. Fix the bad seed file
and re-run.

Naming caveat: avoid a seed file named ``<app>_base.json``. The empty
base template is always created first under that exact name, and a
``<app>_base.json`` in the seed directory would overwrite its contents
in a second pass while the registry row still carries the original
"without seed data" description.

================================================================================
Platform coupling
================================================================================

Two pieces of this script are platform-specific rather than app-specific
and would need attention if the platform changes:

  - psycopg2 driver. The script imports ``psycopg2.extras.Json`` to bind
    the ``table_order`` list to a JSONB column. Switching to psycopg
    (psycopg3) requires replacing this import with the equivalent
    adapter.
  - ``public.environments`` table shape. ``register_public_template``
    assumes columns ``id, service, name, version, visibility,
    description, owner_id, kind, location, table_order, created_at,
    updated_at``, with ``id`` accepting string UUIDs and ``table_order``
    being JSONB. This is the agent-diff platform meta schema; if that
    table is reshaped, this function needs to follow.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine
from psycopg2.extras import Json


# ---------------------------------------------------------------------------
# App loading
# ---------------------------------------------------------------------------


def _load_base_and_schema(app_slug: str):
    """Import the app's ``Base`` and register all ORM models.

    Expects the standard layout: ``Base`` declared in
    ``src.services.<app>.database.base`` and models in
    ``src.services.<app>.database.schema``.
    """
    schema_mod = importlib.import_module(f"src.services.{app_slug}.database.schema")
    base_mod = importlib.import_module(f"src.services.{app_slug}.database.base")
    return base_mod.Base, schema_mod


# ---------------------------------------------------------------------------
# Schema / table creation
# ---------------------------------------------------------------------------


def quote_identifier(name: str) -> str:
    """Quote a SQL identifier for PostgreSQL to preserve case sensitivity."""
    return '"' + name.replace('"', '""') + '"'


def create_schema(conn: Connection, schema_name: str) -> None:
    """Drop-and-recreate a PostgreSQL schema."""
    q = quote_identifier(schema_name)
    conn.execute(text(f"DROP SCHEMA IF EXISTS {q} CASCADE"))
    conn.execute(text(f"CREATE SCHEMA {q}"))


def create_tables(conn: Connection, schema_name: str, Base) -> None:
    """Create all tables registered on ``Base`` inside the given schema."""
    conn_with_schema = conn.execution_options(
        schema_translate_map={None: schema_name}
    )
    Base.metadata.create_all(conn_with_schema, checkfirst=True)


# ---------------------------------------------------------------------------
# Seed insertion
# ---------------------------------------------------------------------------


def _encode_value(value: Any) -> Any:
    """Prepare a Python value for PostgreSQL insertion.

    dict/list become JSON strings so PG's JSONB column can accept them via
    a plain bound parameter. Other values pass through untouched.
    """
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return value


def insert_seed_data(
    conn: Connection,
    schema_name: str,
    seed_data: dict[str, list[dict[str, Any]]],
    Base,
) -> None:
    """Insert seed data in ``Base.metadata.sorted_tables`` (FK) order.

    Table and column names are validated against the model metadata to
    prevent injection through externally controlled keys.
    """
    valid_columns_per_table = {
        t.name: {c.name for c in t.columns} for t in Base.metadata.tables.values()
    }

    for table in Base.metadata.sorted_tables:
        table_name = table.name
        records = seed_data.get(table_name)
        if not records:
            continue

        valid_columns = valid_columns_per_table[table_name]
        print(f"  Inserting {len(records)} {table_name}...")

        for record in records:
            unknown = set(record.keys()) - valid_columns
            if unknown:
                raise ValueError(
                    f"Seed record for {table_name} contains unknown columns: "
                    f"{sorted(unknown)}. Valid columns: {sorted(valid_columns)}"
                )

            processed = {k: _encode_value(v) for k, v in record.items()}
            columns = ", ".join(quote_identifier(k) for k in processed.keys())
            placeholders = ", ".join(f":{k}" for k in processed.keys())
            sql = (
                f"INSERT INTO {quote_identifier(schema_name)}."
                f"{quote_identifier(table_name)} ({columns}) VALUES ({placeholders})"
            )
            conn.execute(text(sql), processed)


# ---------------------------------------------------------------------------
# Public template registration
# ---------------------------------------------------------------------------


def register_public_template(
    conn: Connection,
    *,
    service: str,
    name: str,
    location: str,
    description: str | None,
    table_order: list[str],
) -> None:
    """Register a template in ``public.environments`` as a public template."""
    check_sql = text(
        """
        SELECT id FROM public.environments
        WHERE service = :service
          AND name = :name
          AND version = :version
          AND visibility = 'public'
          AND owner_id IS NULL
        LIMIT 1
        """
    )
    existing = conn.execute(
        check_sql, {"service": service, "name": name, "version": "v1"}
    ).fetchone()

    if existing:
        print(f"Template {name} already exists, skipping registration")
        return

    insert_sql = text(
        """
        INSERT INTO public.environments (
            id, service, name, version, visibility, description,
            owner_id, kind, location, table_order, created_at, updated_at
        ) VALUES (
            :id, :service, :name, :version, 'public', :description,
            NULL, 'schema', :location, :table_order, NOW(), NOW()
        )
        """
    )
    conn.execute(
        insert_sql,
        {
            "id": str(uuid4()),
            "service": service,
            "name": name,
            "version": "v1",
            "description": description,
            "location": location,
            "table_order": Json(table_order),
        },
    )


# ---------------------------------------------------------------------------
# Template creation
# ---------------------------------------------------------------------------


def create_template(
    engine: Engine,
    *,
    app_slug: str,
    template_name: str,
    Base,
    seed_file: Path | None,
    description: str | None,
) -> None:
    """Create a template schema, optionally seeding it from a JSON file.

    If ``seed_file`` is None, the schema is created with all tables but
    no rows — useful as a structural baseline (``<app>_base``) that tests
    can clone and populate themselves.
    """
    print(f"\n=== Creating {template_name} ===")

    sorted_table_names = [t.name for t in Base.metadata.sorted_tables]

    with engine.begin() as conn:
        create_schema(conn, template_name)
        print(f"Created schema: {template_name}")

        create_tables(conn, template_name, Base)
        print(f"Created {len(Base.metadata.tables)} tables")

        if seed_file is not None:
            if not seed_file.exists():
                print(f"Seed file not found: {seed_file} — skipping data load")
            else:
                with open(seed_file) as f:
                    seed_data = json.load(f)

                insert_seed_data(conn, template_name, seed_data, Base)
                print(f"Loaded seed data from {seed_file.name}")
        else:
            print(f"Empty template {template_name} ready")

        register_public_template(
            conn,
            service=app_slug,
            name=template_name,
            location=template_name,
            description=description,
            table_order=sorted_table_names,
        )
        print(f"Registered public template: {template_name}")


# ---------------------------------------------------------------------------
# Seed directory resolution
# ---------------------------------------------------------------------------


def _resolve_seeds_dir(app_slug: str) -> Path:
    """Resolve the seed directory, preferring ``backend/seeds/<app>/``.

    Falls back to ``examples/<app>/seeds/`` for local development layouts
    where seed fixtures live at the repo root.
    """
    backend_root = Path(__file__).parent.parent
    primary = backend_root / "seeds" / app_slug
    if primary.exists():
        return primary

    repo_root = backend_root.parent
    fallback = repo_root / "examples" / app_slug / "seeds"
    return fallback


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create per-app template schemas (empty + seeded)."
    )
    parser.add_argument(
        "--app",
        required=True,
        help="App slug (e.g. slack, calendar, todoist). Must match a directory "
             "under backend/src/services/.",
    )
    args = parser.parse_args()
    app_slug: str = args.app

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)

    Base, _schema_mod = _load_base_and_schema(app_slug)

    engine = create_engine(db_url)
    seeds_dir = _resolve_seeds_dir(app_slug)

    base_name = f"{app_slug}_base"
    create_template(
        engine,
        app_slug=app_slug,
        template_name=base_name,
        Base=Base,
        seed_file=None,
        description=f"{app_slug} base template without seed data",
    )

    seed_files: list[Path] = []
    if seeds_dir.exists():
        seed_files = sorted(seeds_dir.glob("*.json"))
    else:
        print(f"\nSeeds directory not found: {seeds_dir}")
        print(f"Only {base_name} template created.\n")

    for seed_file in seed_files:
        template_name = seed_file.stem
        create_template(
            engine,
            app_slug=app_slug,
            template_name=template_name,
            Base=Base,
            seed_file=seed_file,
            description=f"{app_slug} template seeded from {seed_file.name}",
        )

    total = 1 + len(seed_files)
    print(f"\nAll {total} {app_slug} template(s) created successfully\n")


if __name__ == "__main__":
    main()
