"""Add composite indexes for calendar event queries

Adds composite indexes on calendar_events to optimize the most common
query patterns: time-range filtering, status filtering, and sync-token
incremental queries.

Revision ID: a1b2c3d4e5f6
Revises: merge_heads_20260130
Create Date: 2026-02-11 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "merge_heads_20260130"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Composite index for the most common list_events query pattern:
    #   WHERE calendar_id = X AND status != 'cancelled' AND start_datetime < Y
    op.create_index(
        "ix_event_cal_status_start",
        "calendar_events",
        ["calendar_id", "status", "start_datetime"],
        unique=False,
    )

    # Composite index for time-range queries (list_events with timeMin/timeMax, freebusy):
    #   WHERE calendar_id = X AND start_datetime >= Y AND end_datetime <= Z
    op.create_index(
        "ix_event_cal_start_end",
        "calendar_events",
        ["calendar_id", "start_datetime", "end_datetime"],
        unique=False,
    )

    # Composite index for sync-token incremental queries:
    #   WHERE calendar_id = X AND updated_at > Y
    op.create_index(
        "ix_event_cal_updated",
        "calendar_events",
        ["calendar_id", "updated_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_event_cal_updated", table_name="calendar_events")
    op.drop_index("ix_event_cal_start_end", table_name="calendar_events")
    op.drop_index("ix_event_cal_status_start", table_name="calendar_events")
