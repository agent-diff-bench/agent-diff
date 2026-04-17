"""ORM schema for the Asana API replica.

Entities are added to this file one at a time during the resource
implementation loop. Each entity implementation may also add stub models
for FK dependencies marked with: # STUB — expand when implementing this resource

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its model class to this file incrementally.
"""

from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, String, Table, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# ---------------------------------------------------------------------------
# Stub models for FK targets not yet fully implemented
# ---------------------------------------------------------------------------


class AsanaProject(Base):
    __tablename__ = "asana_projects"
    __table_args__ = (
        Index("ix_asana_projects_owner", "owner"),
        Index("ix_asana_projects_completed_by", "completed_by"),
        Index("ix_asana_projects_team", "team"),
        Index("ix_asana_projects_workspace", "workspace"),
    )

    # Identity
    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="project")
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # ProjectBase fields
    archived: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    modified_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    default_view: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    due_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    due_on: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    start_on: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    html_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    public: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    privacy_setting: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    default_access_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    minimum_access_level_for_customization: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    minimum_access_level_for_sharing: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # ProjectResponse fields
    completed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    completed_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    permalink_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Nested objects stored as JSONB
    current_status: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    current_status_update: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    custom_field_settings: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    custom_fields: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    members: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    followers: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    project_brief: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_from_template: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # FK columns — multiple FKs to asana_users (owner, completed_by)
    owner: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )
    completed_by: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )

    # FK columns — many-to-one to teams and workspaces
    team: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_teams.gid"), nullable=True
    )
    workspace: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_workspaces.gid"), nullable=True
    )

    # Soft-delete support
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # --- Relationships ---

    # Many-to-one: project -> user (owner), disambiguated with foreign_keys
    owner_object: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="owned_projects", foreign_keys=[owner]
    )
    completed_by_object: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="completed_projects", foreign_keys=[completed_by]
    )

    # Many-to-one: project -> team
    team_object: Mapped[Optional["AsanaTeam"]] = relationship(
        back_populates="projects", foreign_keys=[team]
    )

    # Many-to-one: project -> workspace
    workspace_object: Mapped[Optional["AsanaWorkspace"]] = relationship(
        back_populates="projects", foreign_keys=[workspace]
    )

    # Many-to-many: projects <-> tasks (existing from Pass 1)
    tasks: Mapped[list["AsanaTask"]] = relationship(
        secondary="asana_task_project_association", back_populates="project_objects"
    )

    # Incoming: sections that belong to this project
    sections: Mapped[list["AsanaSection"]] = relationship(
        back_populates="project_object", foreign_keys="AsanaSection.project_gid"
    )

    # Incoming: stories that reference this project
    stories: Mapped[list["AsanaStory"]] = relationship(
        back_populates="project_object", foreign_keys="AsanaStory.project_gid"
    )


class AsanaSection(Base):
    # STUB — expand when implementing this resource
    __tablename__ = "asana_sections"
    __table_args__ = (
        Index("ix_asana_sections_project", "project_gid"),
    )

    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="section")
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # FK: section belongs to a project
    project_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_projects.gid"), nullable=True
    )

    project_object: Mapped[Optional["AsanaProject"]] = relationship(
        back_populates="sections", foreign_keys=[project_gid]
    )

    tasks: Mapped[list["AsanaTask"]] = relationship(
        back_populates="assignee_section_object",
        foreign_keys="AsanaTask.assignee_section",
    )


class AsanaStory(Base):
    # STUB — expand when implementing this resource
    __tablename__ = "asana_stories"
    __table_args__ = (
        Index("ix_asana_stories_project", "project_gid"),
    )

    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="story")
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # FK lives on stories side, pointing at the task it belongs to
    task_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_tasks.gid"), nullable=True
    )
    task: Mapped[Optional["AsanaTask"]] = relationship(
        back_populates="stories", foreign_keys=[task_gid]
    )

    # FK: story can reference a project
    project_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_projects.gid"), nullable=True
    )
    project_object: Mapped[Optional["AsanaProject"]] = relationship(
        back_populates="stories", foreign_keys=[project_gid]
    )


class AsanaTag(Base):
    # STUB — expand when implementing this resource
    __tablename__ = "asana_tags"

    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="tag")
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    tasks: Mapped[list["AsanaTask"]] = relationship(
        secondary="asana_task_tag_association", back_populates="tag_objects"
    )


class AsanaTeam(Base):
    # STUB — expand when implementing this resource
    __tablename__ = "asana_teams"

    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="team")

    projects: Mapped[list["AsanaProject"]] = relationship(
        back_populates="team_object", foreign_keys="AsanaProject.team"
    )


class AsanaUser(Base):
    # STUB — expand when implementing this resource
    __tablename__ = "asana_users"

    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="user")

    assigned_tasks: Mapped[list["AsanaTask"]] = relationship(
        back_populates="assignee_object", foreign_keys="AsanaTask.assignee"
    )
    owned_projects: Mapped[list["AsanaProject"]] = relationship(
        back_populates="owner_object", foreign_keys="AsanaProject.owner"
    )
    completed_projects: Mapped[list["AsanaProject"]] = relationship(
        back_populates="completed_by_object", foreign_keys="AsanaProject.completed_by"
    )


class AsanaWorkspace(Base):
    # STUB — expand when implementing this resource
    __tablename__ = "asana_workspaces"

    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="workspace")

    tasks: Mapped[list["AsanaTask"]] = relationship(
        back_populates="workspace_object", foreign_keys="AsanaTask.workspace"
    )
    projects: Mapped[list["AsanaProject"]] = relationship(
        back_populates="workspace_object", foreign_keys="AsanaProject.workspace"
    )


# ---------------------------------------------------------------------------
# Many-to-many association tables
# ---------------------------------------------------------------------------

asana_task_project_association = Table(
    "asana_task_project_association",
    Base.metadata,
    Column("task_gid", ForeignKey("asana_tasks.gid"), primary_key=True),
    Column("project_gid", ForeignKey("asana_projects.gid"), primary_key=True),
)

asana_task_tag_association = Table(
    "asana_task_tag_association",
    Base.metadata,
    Column("task_gid", ForeignKey("asana_tasks.gid"), primary_key=True),
    Column("tag_gid", ForeignKey("asana_tags.gid"), primary_key=True),
)


# ---------------------------------------------------------------------------
# Main task model
# ---------------------------------------------------------------------------


class AsanaTask(Base):
    __tablename__ = "asana_tasks"

    # Identity
    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="task")

    # TaskCompact fields
    name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resource_subtype: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_by: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # TaskBase fields
    approval_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    assignee_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    completed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    completed_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    completed_by: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    due_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    due_on: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    external: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    html_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hearted: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    hearts: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    is_rendered_as_separator: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    liked: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    likes: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    memberships: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    modified_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    num_hearts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    num_likes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    num_subtasks: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    start_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    start_on: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    actual_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # FK columns — one-to-many relationships where the task carries the FK
    assignee: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )
    assignee_section: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_sections.gid"), nullable=True
    )
    workspace: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_workspaces.gid"), nullable=True
    )

    # Self-referential FK for parent/subtask hierarchy
    parent: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_tasks.gid"), nullable=True
    )

    # Non-FK reference fields (JSONB or plain values without FK constraints)
    assigned_by: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    custom_fields: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    custom_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    custom_type_status_option: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    dependencies: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    dependents: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    followers: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    permalink_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Soft-delete support
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # --- Relationships ---

    # Self-referential: parent/children
    parent_task: Mapped[Optional["AsanaTask"]] = relationship(
        remote_side=[gid], back_populates="subtasks"
    )
    subtasks: Mapped[list["AsanaTask"]] = relationship(
        back_populates="parent_task"
    )

    # Many-to-one: task -> user (assignee)
    assignee_object: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="assigned_tasks", foreign_keys=[assignee]
    )

    # Many-to-one: task -> section (assignee_section)
    assignee_section_object: Mapped[Optional["AsanaSection"]] = relationship(
        back_populates="tasks", foreign_keys=[assignee_section]
    )

    # Many-to-one: task -> workspace
    workspace_object: Mapped[Optional["AsanaWorkspace"]] = relationship(
        back_populates="tasks", foreign_keys=[workspace]
    )

    # Many-to-many: tasks <-> projects
    project_objects: Mapped[list["AsanaProject"]] = relationship(
        secondary=asana_task_project_association, back_populates="tasks"
    )

    # Many-to-many: tasks <-> tags
    tag_objects: Mapped[list["AsanaTag"]] = relationship(
        secondary=asana_task_tag_association, back_populates="tasks"
    )

    # Incoming: stories that reference this task
    stories: Mapped[list["AsanaStory"]] = relationship(
        back_populates="task", foreign_keys="AsanaStory.task_gid"
    )

    __table_args__ = (
        Index("ix_asana_tasks_assignee", "assignee"),
        Index("ix_asana_tasks_workspace", "workspace"),
        Index("ix_asana_tasks_parent", "parent"),
        Index("ix_asana_tasks_assignee_section", "assignee_section"),
    )
