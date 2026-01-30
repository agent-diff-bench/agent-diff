#!/usr/bin/env python3
"""
Seed script for creating Google Calendar API replica template schemas.

Creates templates:
- calendar_base: Empty schema with tables only
- calendar_default: Pre-populated with default test data

Usage:
    python backend/utils/seed_calendar_template.py
"""

import os
import sys
import json
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from psycopg2.extras import Json
from src.services.calendar.database.base import Base
from src.services.calendar.database import schema as calendar_schema

# Tables in foreign key dependency order
TABLE_ORDER = [
    "calendar_users",
    "calendars",
    "calendar_list_entries",
    "calendar_events",
    "calendar_event_attendees",
    "calendar_event_reminders",
    "calendar_acl_rules",
    "calendar_settings",
    "calendar_channels",
    "calendar_sync_tokens",
]


def quote_identifier(name: str) -> str:
    """Quote a column name for PostgreSQL to preserve case sensitivity."""
    return f'"{name}"'


def create_schema(conn, schema_name: str):
    """Create a PostgreSQL schema."""
    conn.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))
    conn.execute(text(f"CREATE SCHEMA {schema_name}"))


def create_tables(conn, schema_name: str):
    """Create all tables in the schema using SQLAlchemy metadata."""
    conn_with_schema = conn.execution_options(schema_translate_map={None: schema_name})
    _ = calendar_schema  # Ensure all models are loaded
    Base.metadata.create_all(conn_with_schema, checkfirst=True)


def insert_seed_data(conn, schema_name: str, seed_data: dict):
    """Insert seed data into tables using dynamic SQL.

    Args:
        conn: Database connection
        schema_name: Target schema name
        seed_data: Dict mapping table names to lists of records
    """
    for table_name in TABLE_ORDER:
        if table_name not in seed_data:
            continue

        records = seed_data[table_name]
        if not records:
            continue

        print(f"  Inserting {len(records)} {table_name}...")

        for record in records:
            # Convert dict/list values to JSON strings for PostgreSQL
            processed_record = {}
            for k, v in record.items():
                if isinstance(v, (dict, list)):
                    processed_record[k] = json.dumps(v)
                else:
                    processed_record[k] = v

            # Quote column names to preserve case sensitivity in PostgreSQL
            columns = ", ".join([quote_identifier(k) for k in processed_record.keys()])
            placeholders = ", ".join([f":{k}" for k in processed_record.keys()])
            sql = (
                f'INSERT INTO "{schema_name}"."{table_name}" '
                f"({columns}) VALUES ({placeholders})"
            )
            conn.execute(text(sql), processed_record)


def register_public_template(
    conn,
    *,
    service: str,
    name: str,
    location: str,
    description: str | None = None,
    table_order: list[str] | None = None,
):
    """Register a template in platform meta DB as public."""

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
        print(f"Template {name} already exists, skipping")
        return

    sql = text(
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
    params = {
        "id": str(uuid4()),
        "service": service,
        "name": name,
        "version": "v1",
        "description": description,
        "location": location,
        "table_order": Json(table_order) if table_order is not None else None,
    }
    conn.execute(sql, params)


def create_template(engine, template_name: str, seed_file: Path | None = None):
    """Create a template schema with optional seed data.

    Args:
        engine: SQLAlchemy engine
        template_name: Name of the schema to create
        seed_file: Optional path to JSON seed file
    """
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

        # Register as a public template in platform DB
        register_public_template(
            conn,
            service="calendar",
            name=template_name,
            location=template_name,
            description=(
                "Google Calendar API base template"
                if template_name == "calendar_base"
                else "Google Calendar API default template with seed data"
            ),
            table_order=TABLE_ORDER,
        )
        print(f"Registered public template: {template_name}")


def main():
    """Create both calendar_base and calendar_default templates."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)

    engine = create_engine(db_url)
    seeds_dir = Path(__file__).parent.parent.parent / "examples" / "calendar" / "seeds"

    # Create empty base template
    create_template(engine, "calendar_base")

    # Discover and create templates for all seed JSON files
    if seeds_dir.exists():
        seed_files = list(seeds_dir.glob("*.json"))
        for seed_file in seed_files:
            template_name = seed_file.stem
            create_template(engine, template_name, seed_file)
        print(f"\nAll {1 + len(seed_files)} Calendar template(s) created successfully\n")
    else:
        print(f"\nSeeds directory not found: {seeds_dir}")
        print("Only calendar_base template created.\n")


if __name__ == "__main__":
    main()
