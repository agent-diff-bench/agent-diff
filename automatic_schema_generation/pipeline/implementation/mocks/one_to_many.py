"""Pattern: One-to-Many (1:N) — REFERENCE MOCK, not real code.

These models are fictional examples showing how to implement a 1:N
FK relationship. Do not reuse these names — build your own models
based on the actual resource schemas provided in the prompt.

Use this pattern when one entity "belongs to" another and the child
carries the FK column.
"""

from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ExampleParent(Base):
    __tablename__ = "mock_parents"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Parent side: list relationship, no FK column on this table.
    # cascade="all,delete-orphan" ensures children are removed when
    # the parent is deleted.
    children: Mapped[list["ExampleChild"]] = relationship(
        back_populates="parent", cascade="all,delete-orphan"
    )


class ExampleChild(Base):
    __tablename__ = "mock_children"
    __table_args__ = (
        Index("ix_mock_children_parent", "parent_id"),
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Child side: FK column + scalar relationship.
    # nullable=False means every child must belong to a parent.
    # Use nullable=True when the parent is optional.
    parent_id: Mapped[str] = mapped_column(
        ForeignKey("mock_parents.id"), nullable=False
    )
    parent: Mapped["ExampleParent"] = relationship(back_populates="children")


# --- Operations (key patterns) ---
#
# def create_child(session, *, parent_id, title):
#     child = ExampleChild(
#         id=generate_id("child"),
#         parent_id=parent_id,             # FK set at creation
#         title=title,
#     )
#     session.add(child)
#     session.flush()
#     return child
#
# def list_children_by_parent(session, parent_id):
#     return session.execute(
#         select(ExampleChild)
#         .where(ExampleChild.parent_id == parent_id,
#                ExampleChild.is_deleted.is_(False))
#     ).scalars().all()
