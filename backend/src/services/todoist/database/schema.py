"""ORM schema for the Todoist API replica.

Models mirror the Todoist REST API response shapes. Field names use snake_case
to match the API's JSON keys (Todoist uses snake_case natively).

Personal and workspace projects are unified into a single table. Workspace-only
fields are nullable.
"""

from typing import Any, Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# STUB — expand when implementing this resource
class Folder(Base):
    """Todoist folder (workspace-level project grouping).

    Stub model — only enough for FK integrity. Expand when implementing
    the folders resource.
    """

    __tablename__ = "todoist_folders"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationships
    projects: Mapped[list["Project"]] = relationship(back_populates="folder")


# STUB — expand when implementing this resource
class Section(Base):
    """Todoist section within a project.

    Stub model — only enough for FK integrity. Expand when implementing
    the sections resource.
    """

    __tablename__ = "todoist_sections"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("todoist_projects.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationships
    project: Mapped["Project"] = relationship()
    tasks: Mapped[list["Task"]] = relationship(back_populates="section")


class User(Base):
    """Todoist user — maps to UserJSON / UserSyncView in the API.

    This is a minimal version covering fields needed for FK integrity and the
    GET /user endpoint. The full UserJSON schema has 50+ fields; most are stored
    in the settings JSONB column rather than as individual columns.
    """

    __tablename__ = "todoist_users"

    # Identity
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Account state
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Timestamps
    joined_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    deleted_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # All remaining UserJSON fields — preferences, onboarding, karma, avatars,
    # feature flags, etc. Stored as JSONB to avoid 40+ rarely-queried columns.
    settings: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Relationships
    created_projects: Mapped[list["Project"]] = relationship(back_populates="creator")
    owned_tasks: Mapped[list["Task"]] = relationship(
        back_populates="user", foreign_keys="Task.user_id"
    )


class Project(Base):
    """Todoist project — personal or workspace.

    Maps to PersonalProjectSyncView / WorkspaceProjectSyncView in the API.
    """

    __tablename__ = "todoist_projects"
    __table_args__ = (
        Index("ix_todoist_projects_creator", "creator_uid"),
        Index("ix_todoist_projects_workspace", "workspace_id"),
        Index("ix_todoist_projects_parent", "parent_id"),
    )

    # Identity
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # Hierarchy
    parent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_projects.id"), nullable=True
    )
    child_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    default_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Display
    color: Mapped[str] = mapped_column(String(50), nullable=False, default="charcoal")
    view_style: Mapped[str] = mapped_column(String(20), nullable=False, default="list")
    is_collapsed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_favorite: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # State flags
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_frozen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    inbox_project: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Permissions / sharing
    is_shared: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_assign_tasks: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    can_comment: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    public_key: Mapped[str] = mapped_column(String(255), nullable=False, default="")

    # Nested access object — stored as JSONB since we don't query on it.
    # Shape: {"visibility": "...", "configuration": {...}}
    access: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Ownership
    creator_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )

    # Timestamps — stored as strings to match Todoist API format
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # --- Workspace-only fields (nullable for personal projects) ---
    workspace_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    folder_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_folders.id"), nullable=True
    )
    status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    collaborator_role_default: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    is_invite_only: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_link_sharing_enabled: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True
    )
    is_pending_default_collaborator_invites: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True
    )
    is_project_insights_enabled: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True
    )

    # Relationships
    creator: Mapped[Optional["User"]] = relationship(back_populates="created_projects")
    folder: Mapped[Optional["Folder"]] = relationship(back_populates="projects")
    parent: Mapped[Optional["Project"]] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Project"]] = relationship(back_populates="parent")
    tasks: Mapped[list["Task"]] = relationship(back_populates="project")


class Task(Base):
    """Todoist task — maps to ItemSyncView in the API."""

    __tablename__ = "todoist_tasks"
    __table_args__ = (
        Index("ix_todoist_tasks_project", "project_id"),
        Index("ix_todoist_tasks_section", "section_id"),
        Index("ix_todoist_tasks_parent", "parent_id"),
        Index("ix_todoist_tasks_user", "user_id"),
    )

    # Identity
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # Hierarchy and placement
    project_id: Mapped[str] = mapped_column(
        ForeignKey("todoist_projects.id"), nullable=False
    )
    section_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_sections.id"), nullable=True
    )
    parent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_tasks.id"), nullable=True
    )
    child_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    day_order: Mapped[int] = mapped_column(Integer, nullable=False, default=-1)

    # Ownership and assignment
    user_id: Mapped[str] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=False
    )
    added_by_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )
    assigned_by_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )
    responsible_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )
    completed_by_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )

    # State
    checked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_collapsed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Labels — stored as JSON array of strings
    labels: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Due date — nested object, stored as JSONB
    # Shape: {"date": "...", "string": "...", "lang": "...", "is_recurring": bool, "datetime": "..."}
    due: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Deadline — nested object, stored as JSONB
    # Shape: {"date": "...", "lang": "...", "is_recurring": bool}
    deadline: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Duration — nested object, stored as JSONB
    # Shape: {"amount": int, "unit": "minute"|"day"}
    duration: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Metadata
    note_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goal_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Timestamps
    added_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    completed_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="tasks")
    section: Mapped[Optional["Section"]] = relationship(back_populates="tasks")
    user: Mapped["User"] = relationship(
        back_populates="owned_tasks", foreign_keys=[user_id]
    )
    parent: Mapped[Optional["Task"]] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Task"]] = relationship(back_populates="parent")


class Label(Base):
    """Todoist label — maps to LabelRestView in the API."""

    __tablename__ = "todoist_labels"
    __table_args__ = (
        Index("ix_todoist_labels_order", "order"),
    )

    # Identity
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False, default="charcoal")
    
    # Organization
    order: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # State
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Timestamps
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
