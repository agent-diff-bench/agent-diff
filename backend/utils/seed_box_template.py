#!/usr/bin/env python3
"""
Seed script for creating Box template schemas.

Creates two templates:
- box_base: Empty schema with tables only
- box_default: Pre-populated with default test data (if seed file exists)

Usage:
    python backend/utils/seed_box_template.py
"""

import os
import re
import sys
import json
from pathlib import Path
from uuid import uuid4

# Pattern for safe SQL identifiers (letters, digits, underscores, starting with letter/underscore)
SAFE_IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from src.services.box.database.base import Base
from src.services.box.database import schema as box_schema

# Tables in foreign key dependency order
TABLE_ORDER = [
    "box_users",
    "box_folders",
    "box_files",
    "box_file_versions",
    "box_file_contents",
    "box_comments",
    "box_tasks",
    "box_task_assignments",
    "box_hubs",
    "box_hub_items",
]


def create_schema(conn, schema_name: str):
    """Create a PostgreSQL schema.

    Validates schema name is a safe SQL identifier to ensure consistency
    with unquoted usage elsewhere (e.g., schema.table in INSERT statements).
    """
    if not SAFE_IDENTIFIER_PATTERN.match(schema_name):
        raise ValueError(
            f"Invalid schema name '{schema_name}': must start with letter/underscore "
            "and contain only letters, digits, underscores"
        )
    conn.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))
    conn.execute(text(f"CREATE SCHEMA {schema_name}"))


def create_tables(conn, schema_name: str):
    """Create all tables in the schema using SQLAlchemy metadata."""
    conn_with_schema = conn.execution_options(schema_translate_map={None: schema_name})
    _ = box_schema  # Ensure all models are loaded
    Base.metadata.create_all(conn_with_schema, checkfirst=True)


def _validate_identifier(identifier: str, allowed_set: set[str], label: str) -> str:
    """Validate that an identifier is in the allowed set to prevent SQL injection."""
    if identifier not in allowed_set:
        raise ValueError(
            f"Invalid {label}: {identifier}. Must be one of: {allowed_set}"
        )
    return identifier


def insert_seed_data(conn, schema_name: str, seed_data: dict):
    """Insert seed data into tables using parameterized SQL.

    Validates table names and column names against SQLAlchemy metadata
    to prevent SQL injection through externally controlled values.

    Args:
        conn: Database connection
        schema_name: Target schema name (must match a known pattern)
        seed_data: Dict mapping table names to lists of records
    """
    # Validate schema name matches expected pattern (box_* prefixed)
    if not schema_name.startswith("box_") and schema_name not in ("public",):
        raise ValueError(f"Invalid schema_name pattern: {schema_name}")

    # Get valid table and column names from SQLAlchemy metadata
    valid_tables = set(TABLE_ORDER)
    valid_columns_per_table = {
        table.name: set(col.name for col in table.columns)
        for table in Base.metadata.tables.values()
    }

    if "box_file_versions" in seed_data:
        content_records = []
        for version_record in seed_data["box_file_versions"]:
            if "local_path" in version_record:
                local_path = version_record.pop("local_path")
                repo_root = Path(__file__).parent.parent.parent
                file_path = repo_root / local_path

                if file_path.exists():
                    try:
                        content = file_path.read_bytes()
                        # box_file_contents has 'id' (PK, same as version id) and 'version_id' (FK)
                        content_records.append(
                            {
                                "id": version_record[
                                    "id"
                                ],  # Use version_id as primary key
                                "version_id": version_record["id"],
                                "content": content,
                            }
                        )
                    except Exception as e:
                        print(f"Warning: Failed to read file {file_path}: {e}")
                else:
                    print(f"Warning: Seed file not found: {file_path}")

        # Add generated content records to seed_data
        if content_records:
            if "box_file_contents" not in seed_data:
                seed_data["box_file_contents"] = []
            seed_data["box_file_contents"].extend(content_records)
            print(f"  Prepared {len(content_records)} file content records")

    for table_name in TABLE_ORDER:
        if table_name not in seed_data:
            continue

        # Validate table name
        _validate_identifier(table_name, valid_tables, "table_name")

        records = seed_data[table_name]
        if not records:
            continue

        print(f"  Inserting {len(records)} {table_name}...")

        # Get valid columns for this table
        valid_columns = valid_columns_per_table.get(table_name, set())

        for record in records:
            # Validate all column names in the record
            for col_name in record.keys():
                _validate_identifier(col_name, valid_columns, f"column in {table_name}")

            # Build SQL with validated identifiers
            columns = ", ".join(record.keys())
            placeholders = ", ".join([f":{k}" for k in record.keys()])
            sql = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({placeholders})"
            conn.execute(text(sql), record)


def register_public_template(
    conn, *, service: str, name: str, location: str, description: str | None = None
):
    """Register a template in platform meta DB as public (owner_scope='public')."""
    # Check if template already exists
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
        "table_order": json.dumps(TABLE_ORDER),
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
            service="box",
            name=template_name,
            location=template_name,
            description=(
                "Box base template without seed data"
                if template_name == "box_base"
                else "Box default template with seed data"
            ),
        )
        print(f"Registered public template: {template_name}")


def main():
    """Discover and create all Box templates from examples/box/seeds/."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)

    engine = create_engine(db_url)
    seeds_dir = Path(__file__).parent.parent.parent / "examples" / "box" / "seeds"

    # Create empty base template
    create_template(engine, "box_base")

    # Discover and create templates for all seed JSON files (if any)
    if seeds_dir.exists():
        seed_files = list(seeds_dir.glob("*.json"))

        for seed_file in seed_files:
            template_name = seed_file.stem  # e.g. "box_default" from "box_default.json"
            create_template(engine, template_name, seed_file)

        print(f"\n All {1 + len(seed_files)} Box template(s) created successfully\n")
    else:
        print("\n Box base template created successfully (no seed files found)\n")


if __name__ == "__main__":
    main()
