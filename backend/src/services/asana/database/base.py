"""SQLAlchemy declarative base for Asana models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Service-local declarative base for Asana."""

    pass
