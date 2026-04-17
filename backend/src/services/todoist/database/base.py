"""SQLAlchemy declarative base for Todoist models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Service-local declarative base for Todoist."""

    pass
