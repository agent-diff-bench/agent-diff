#!/usr/bin/env python3
"""Seed script for GitHub template schemas.

Creates:
- ``github_base``: empty schema (tables only), handy as a clean-slate template.
- ``github_default``: pre-populated with a small ACME widgets repo containing
  issues, pull requests, labels, assignees, and comments.

Usage:
    python backend/utils/seed_github_template.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text

from src.services.github.database import schema as github_schema
from src.services.github.database.base import Base


TABLE_ORDER = [
    "github_users",
    "github_repositories",
    "github_labels",
    "github_issues",
    "github_issue_labels",
    "github_issue_assignees",
    "github_pull_request_reviewers",
    "github_issue_comments",
]


def create_schema(conn, schema_name: str) -> None:
    conn.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))
    conn.execute(text(f"CREATE SCHEMA {schema_name}"))


def create_tables(conn, schema_name: str) -> None:
    conn_with_schema = conn.execution_options(schema_translate_map={None: schema_name})
    _ = github_schema
    Base.metadata.create_all(conn_with_schema, checkfirst=True)


def insert_seed_data(conn, schema_name: str, seed_data: dict) -> None:
    for table_name in TABLE_ORDER:
        records = seed_data.get(table_name) or []
        if not records:
            continue
        print(f"  Inserting {len(records)} {table_name}...")
        for record in records:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(f":{k}" for k in record.keys())
            sql = (
                f"INSERT INTO {schema_name}.{table_name} ({columns}) "
                f"VALUES ({placeholders})"
            )
            conn.execute(text(sql), record)


def register_public_template(
    conn,
    *,
    service: str,
    name: str,
    location: str,
    description: str | None = None,
    table_order: list[str] | None = None,
) -> None:
    existing = conn.execute(
        text(
            """
            SELECT id FROM public.environments
            WHERE service = :service
              AND name = :name
              AND version = :version
              AND visibility = 'public'
              AND owner_id IS NULL
            LIMIT 1
            """
        ),
        {"service": service, "name": name, "version": "v1"},
    ).fetchone()

    if existing:
        print(f"Template {name} already exists, skipping registration")
        return

    conn.execute(
        text(
            """
            INSERT INTO public.environments (
                id, service, name, version, visibility, description,
                owner_id, kind, location, table_order, created_at, updated_at
            ) VALUES (
                :id, :service, :name, :version, 'public', :description,
                NULL, 'schema', :location, :table_order, NOW(), NOW()
            )
            """
        ),
        {
            "id": str(uuid4()),
            "service": service,
            "name": name,
            "version": "v1",
            "description": description,
            "location": location,
            "table_order": json.dumps(table_order) if table_order else None,
        },
    )


def create_template(engine, template_name: str, seed_file: Path | None = None) -> None:
    print(f"\n=== Creating {template_name} ===")

    with engine.begin() as conn:
        create_schema(conn, template_name)
        print(f"Created schema: {template_name}")

        create_tables(conn, template_name)
        print(f"Created {len(Base.metadata.tables)} tables")

        if seed_file:
            if not seed_file.exists():
                print(f"Seed file not found: {seed_file}")
                return
            with open(seed_file) as f:
                seed_data = json.load(f)
            insert_seed_data(conn, template_name, seed_data)
            print(f"Loaded seed data from {seed_file.name}")
        else:
            print(f"Empty template {template_name} ready")

        description = (
            "GitHub base template without seed data"
            if template_name == "github_base"
            else "GitHub default template with a small widgets repo"
        )
        register_public_template(
            conn,
            service="github",
            name=template_name,
            location=template_name,
            description=description,
            table_order=TABLE_ORDER,
        )
        print(f"Registered public template: {template_name}")


def main() -> None:
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)

    engine = create_engine(db_url)

    seeds_dir = Path(__file__).parent.parent / "seeds" / "github"
    if not seeds_dir.exists():
        seeds_dir = (
            Path(__file__).parent.parent.parent / "examples" / "github" / "seeds"
        )

    create_template(engine, "github_base")

    seed_files = sorted(seeds_dir.glob("*.json"))
    for seed_file in seed_files:
        create_template(engine, seed_file.stem, seed_file)

    print(f"\n All {1 + len(seed_files)} GitHub template(s) created successfully\n")


if __name__ == "__main__":
    main()
