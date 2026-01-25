"""slack messages blocks column

Revision ID: c8f3a2b1d9e4
Revises: b49e93fd90ec
Create Date: 2025-12-27 14:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


revision: str = "c8f3a2b1d9e4"
down_revision: Union[str, None] = "b49e93fd90ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _fetch_slack_schemas(conn) -> list[str]:
    """Fetch all Slack-related schemas (templates and runtime environments)."""
    result = conn.execute(
        text(
            """
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name LIKE 'slack_%'
               OR schema_name LIKE 'state_pool_%'
            """
        )
    )
    return [row[0] for row in result]


def _table_exists(conn, schema: str, table: str) -> bool:
    result = conn.execute(
        text(
            """
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = :schema
              AND table_name = :table
            """
        ),
        {"schema": schema, "table": table},
    )
    return result.scalar() is not None


def _column_exists(conn, schema: str, table: str, column: str) -> bool:
    result = conn.execute(
        text(
            """
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = :schema
              AND table_name = :table
              AND column_name = :column
            """
        ),
        {"schema": schema, "table": table, "column": column},
    )
    return result.scalar() is not None


def _quote_ident(ident: str) -> str:
    return f'"{ident.replace('"', '""')}"'


def upgrade() -> None:
    """Add blocks JSONB column to messages table in all Slack schemas."""
    conn = op.get_bind()
    schemas = _fetch_slack_schemas(conn)

    for schema in schemas:
        if not _table_exists(conn, schema, "messages"):
            continue
        if _column_exists(conn, schema, "messages", "blocks"):
            continue
        # Ensure this is a Slack schema by checking for message_id column
        if not _column_exists(conn, schema, "messages", "message_id"):
            continue

        schema_q = _quote_ident(schema)
        conn.execute(text(f'ALTER TABLE {schema_q}."messages" ADD COLUMN blocks JSONB'))


def downgrade() -> None:
    """Remove blocks column from messages table in all Slack schemas."""
    conn = op.get_bind()
    schemas = _fetch_slack_schemas(conn)

    for schema in schemas:
        if not _table_exists(conn, schema, "messages"):
            continue
        if not _column_exists(conn, schema, "messages", "blocks"):
            continue

        schema_q = _quote_ident(schema)
        conn.execute(text(f'ALTER TABLE {schema_q}."messages" DROP COLUMN blocks'))
