"""SQLAlchemy declarative base for __APP_NAME__."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Service-local declarative base."""


# BEGIN RESOURCE DECLARATIONS
class TimestampMixin:
    """Shared created/updated timestamp columns."""

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
# END RESOURCE DECLARATIONS

