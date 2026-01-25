"""
Box Database Base - SQLAlchemy declarative base and common utilities.

Following patterns from Slack and Linear replicas.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for Box models."""

    pass
