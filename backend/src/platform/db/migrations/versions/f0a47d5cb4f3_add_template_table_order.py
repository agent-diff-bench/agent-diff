"""Add table_order metadata to templates."""

from typing import Sequence, Union
import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

LINEAR_TABLE_ORDER = [
    "organizations",
    "users",
    "external_users",
    "teams",
    "workflow_states",
    "team_memberships",
    "user_settings",
    "user_flags",
    "templates",
    "projects",
    "project_labels",
    "project_milestones",
    "project_statuses",
    "cycles",
    "issue_labels",
    "issues",
    "comments",
    "attachments",
    "reactions",
    "favorites",
    "issue_histories",
    "issue_suggestions",
    "issue_relations",
    "customer_needs",
    "documents",
    "document_contents",
    "drafts",
    "issue_drafts",
    "initiatives",
    "initiative_updates",
    "initiative_histories",
    "initiative_relations",
    "initiative_to_projects",
    "project_updates",
    "project_histories",
    "project_relations",
    "posts",
    "notifications",
    "webhooks",
    "integrations",
    "integrations_settings",
    "git_automation_states",
    "facets",
    "triage_responsibilities",
    "agent_sessions",
    "organization_invites",
    "organization_domains",
    "paid_subscriptions",
    "entity_external_links",
    "issue_imports",
]

# revision identifiers, used by Alembic.
revision: str = "f0a47d5cb4f3"
down_revision: Union[str, None] = "9b3ea480abcb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "environments",
        sa.Column(
            "table_order", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        schema="public",
    )

    op.execute(
        sa.text(
            """
            UPDATE public.environments
            SET table_order = :table_order::jsonb
            WHERE service = 'linear' AND table_order IS NULL
            """
        ).bindparams(table_order=json.dumps(LINEAR_TABLE_ORDER))
    )


def downgrade() -> None:
    op.drop_column("environments", "table_order", schema="public")
