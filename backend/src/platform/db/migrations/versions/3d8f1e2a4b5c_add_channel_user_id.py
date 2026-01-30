"""Add user_id to calendar_channels

Revision ID: 3d8f1e2a4b5c
Revises: 2ac6c433442a
Create Date: 2026-01-20 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d8f1e2a4b5c'
down_revision: Union[str, None] = '2ac6c433442a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add user_id column to calendar_channels for ownership tracking
    op.add_column(
        'calendar_channels',
        sa.Column('user_id', sa.String(length=255), nullable=True)
    )
    # Add index for efficient user-based queries
    op.create_index(
        'ix_channel_user_id',
        'calendar_channels',
        ['user_id'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index('ix_channel_user_id', table_name='calendar_channels')
    op.drop_column('calendar_channels', 'user_id')
