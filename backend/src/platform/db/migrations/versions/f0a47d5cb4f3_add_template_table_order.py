"""Add table_order metadata to templates."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

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


def downgrade() -> None:
    op.drop_column("environments", "table_order", schema="public")
