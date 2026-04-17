"""Pattern: Many-to-Many (M:N) — REFERENCE MOCK, not real code.

These models are fictional examples showing how to implement an M:N
relationship via an association table. Do not reuse these names —
build your own models based on the actual resource schemas provided
in the prompt.

Use an association Table when both sides carry a list and no extra
metadata is needed on the link itself. If the link needs extra
columns (e.g. joined_at, role), use an explicit mapped class with
a composite primary key instead of a bare Table.
"""

from sqlalchemy import Boolean, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# Association table — bare Table, not a mapped class.
# Composite primary key prevents duplicate links.
example_item_tag_association = Table(
    "mock_item_tag_association",
    Base.metadata,
    Column("item_id", ForeignKey("mock_items.id"), primary_key=True),
    Column("tag_id", ForeignKey("mock_tags.id"), primary_key=True),
)


class ExampleItem(Base):
    __tablename__ = "mock_items"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # secondary= points at the association table.
    # Both sides use back_populates to keep the ORM in sync.
    tags: Mapped[list["ExampleTag"]] = relationship(
        secondary=example_item_tag_association, back_populates="items"
    )


class ExampleTag(Base):
    __tablename__ = "mock_tags"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    items: Mapped[list["ExampleItem"]] = relationship(
        secondary=example_item_tag_association, back_populates="tags"
    )


# --- Operations (key patterns) ---
#
# Adding / removing links operates on the relationship list directly.
# SQLAlchemy handles the association table inserts and deletes.
#
# def add_tag_to_item(session, item_id, tag_id):
#     item = session.get(ExampleItem, item_id)
#     tag = session.get(ExampleTag, tag_id)
#     if tag not in item.tags:
#         item.tags.append(tag)
#     session.flush()
#
# def remove_tag_from_item(session, item_id, tag_id):
#     item = session.get(ExampleItem, item_id)
#     tag = session.get(ExampleTag, tag_id)
#     if tag in item.tags:
#         item.tags.remove(tag)
#     session.flush()
#
# Querying items by tag:
#
# def list_items_by_tag(session, tag_id):
#     return session.execute(
#         select(ExampleItem)
#         .join(ExampleItem.tags)
#         .where(ExampleTag.id == tag_id,
#                ExampleItem.is_deleted.is_(False))
#     ).scalars().all()
