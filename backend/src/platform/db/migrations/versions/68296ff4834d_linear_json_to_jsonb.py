"""linear json to jsonb

Revision ID: 68296ff4834d
Revises: f0a47d5cb4f3
Create Date: 2025-11-12 21:56:06.822951

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


TABLE_COLUMN_MAP = {
    "issues": [
        "activitySummary",
        "descriptionData",
        "labelIds",
        "previousIdentifiers",
        "reactionData",
    ],
    "attachments": [
        "metadata",
        "source",
    ],
    "comments": [
        "reactionData",
        "threadSummary",
    ],
    "cycles": [
        "completedIssueCountHistory",
        "completedScopeHistory",
        "currentProgress",
        "inProgressScopeHistory",
        "issueCountHistory",
        "progressHistory",
        "scopeHistory",
    ],
    "projects": [
        "completedIssueCountHistory",
        "completedScopeHistory",
        "currentProgress",
        "inProgressScopeHistory",
        "issueCountHistory",
        "labelIds",
        "progressHistory",
        "scopeHistory",
    ],
    "project_milestones": [
        "currentProgress",
        "descriptionData",
        "progressHistory",
    ],
    "teams": [
        "currentProgress",
        "progressHistory",
    ],
    "organizations": [
        "allowedAuthServices",
        "allowedFileUploadContentTypes",
        "customersConfiguration",
        "previousUrlKeys",
        "samlSettings",
        "scimSettings",
        "themeSettings",
        "workingDays",
    ],
    "posts": [
        "reactionData",
        "writtenSummaryData",
    ],
    "organization_invites": [
        "metadata",
    ],
    "issue_imports": [
        "errorMetadata",
        "mapping",
        "serviceMetadata",
    ],
    "user_settings": [
        "notificationCategoryPreferences",
        "notificationChannelPreferences",
        "notificationDeliveryPreferences",
        "unsubscribedFrom",
        "settings",
        "usageWarningHistory",
    ],
}


def _fetch_linear_schemas(conn) -> list[str]:
    result = conn.execute(
        text(
            """
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name LIKE 'linear_%'
               OR schema_name LIKE 'state_%'
            """
        )
    )
    return [row[0] for row in result]


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


def _alter_columns(conn, schemas: list[str], *, to_jsonb: bool) -> None:
    target_type = "JSONB" if to_jsonb else "JSON"
    cast = "::jsonb" if to_jsonb else "::json"
    for schema in schemas:
        for table, columns in TABLE_COLUMN_MAP.items():
            for column in columns:
                if not _column_exists(conn, schema, table, column):
                    continue
                conn.execute(
                    text(
                        f'ALTER TABLE "{schema}"."{table}" '
                        f'ALTER COLUMN "{column}" TYPE {target_type} '
                        f'USING "{column}"{cast}'
                    )
                )


# revision identifiers, used by Alembic.
revision: str = "68296ff4834d"
down_revision: Union[str, None] = "f0a47d5cb4f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    schemas = _fetch_linear_schemas(conn)
    if not schemas:
        return
    _alter_columns(conn, schemas, to_jsonb=True)


def downgrade() -> None:
    conn = op.get_bind()
    schemas = _fetch_linear_schemas(conn)
    if not schemas:
        return
    _alter_columns(conn, schemas, to_jsonb=False)
