"""SQLAlchemy declarative base for GitHub models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Service-local declarative base for GitHub."""

    pass
