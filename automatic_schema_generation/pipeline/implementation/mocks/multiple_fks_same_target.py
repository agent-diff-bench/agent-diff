"""Pattern: Multiple FKs to the Same Target — REFERENCE MOCK, not real code.

These models are fictional examples showing how to disambiguate
when two or more FK columns reference the same table. Do not reuse
these names — build your own models based on the actual resource
schemas provided in the prompt.

When multiple FK columns point at the same target, SQLAlchemy
cannot infer which relationship uses which column. Disambiguate
with the foreign_keys= argument. Each relationship on the target
side also needs its own back_populates name.
"""

from typing import Optional

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ExamplePerson(Base):
    __tablename__ = "mock_persons"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # One back_populates list per FK role on the referencing side.
    created_tickets: Mapped[list["ExampleTicket"]] = relationship(
        back_populates="creator", foreign_keys="ExampleTicket.creator_id"
    )
    assigned_tickets: Mapped[list["ExampleTicket"]] = relationship(
        back_populates="assignee", foreign_keys="ExampleTicket.assignee_id"
    )


class ExampleTicket(Base):
    __tablename__ = "mock_tickets"
    __table_args__ = (
        Index("ix_mock_tickets_creator", "creator_id"),
        Index("ix_mock_tickets_assignee", "assignee_id"),
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)

    # Two FK columns to the same table.
    creator_id: Mapped[str] = mapped_column(
        ForeignKey("mock_persons.id"), nullable=False
    )
    assignee_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("mock_persons.id"), nullable=True
    )

    # foreign_keys= resolves the ambiguity. Without it, SQLAlchemy
    # raises AmbiguousForeignKeysError at mapper configuration time.
    creator: Mapped["ExamplePerson"] = relationship(
        back_populates="created_tickets", foreign_keys=[creator_id]
    )
    assignee: Mapped[Optional["ExamplePerson"]] = relationship(
        back_populates="assigned_tickets", foreign_keys=[assignee_id]
    )


# --- Serializer hint ---
#
# def serialize_ticket(ticket: ExampleTicket) -> dict:
#     return {
#         "id": ticket.id,
#         "title": ticket.title,
#         "creator_id": ticket.creator_id,
#         "assignee_id": ticket.assignee_id,
#     }
