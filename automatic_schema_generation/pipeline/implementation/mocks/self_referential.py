"""Pattern: Self-Referential FK — REFERENCE MOCK, not real code.

These models are fictional examples showing how to implement a
self-referential tree hierarchy. Do not reuse these names — build
your own models based on the actual resource schemas provided in
the prompt.

Use this pattern for any entity that nests within itself: folders,
comments, org units, task subtasks, etc. The FK is nullable because
root nodes have parent_id = NULL.
"""

from typing import Optional

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ExampleNode(Base):
    __tablename__ = "mock_nodes"
    __table_args__ = (
        Index("ix_mock_nodes_parent", "parent_id"),
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)

    # FK to own table. Nullable because root nodes have no parent.
    parent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("mock_nodes.id"), nullable=True
    )

    # remote_side=[id] tells SQLAlchemy which column is the "one"
    # side. Without it, SQLAlchemy can't distinguish parent from
    # children since both reference the same table.
    parent: Mapped[Optional["ExampleNode"]] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list["ExampleNode"]] = relationship(
        back_populates="parent"
    )


# --- Operations (key patterns) ---
#
# def get_root_nodes(session):
#     return session.execute(
#         select(ExampleNode).where(ExampleNode.parent_id.is_(None))
#     ).scalars().all()
#
# def get_children(session, node_id):
#     return session.execute(
#         select(ExampleNode)
#         .where(ExampleNode.parent_id == node_id)
#     ).scalars().all()
#
# def move_node(session, node_id, new_parent_id):
#     node = session.get(ExampleNode, node_id)
#     node.parent_id = new_parent_id
#     session.flush()
