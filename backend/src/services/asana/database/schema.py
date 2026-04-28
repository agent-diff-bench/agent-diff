"""ORM schema for the Asana API replica.

Entities are added to this file one at a time during the resource
implementation loop. Each entity implementation may also add stub models
for FK dependencies marked with: # STUB — expand when implementing this resource

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its model class to this file incrementally.
"""

from typing import Any, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, String, Table, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# ---------------------------------------------------------------------------
# Association tables
# ---------------------------------------------------------------------------

# Users can belong to multiple workspaces, and workspaces have multiple users.
asana_user_workspace_association = Table(
    "asana_user_workspace_association",
    Base.metadata,
    Column("user_gid", ForeignKey("asana_users.gid"), primary_key=True),
    Column("workspace_gid", ForeignKey("asana_workspaces.gid"), primary_key=True),
)

# Users can belong to multiple teams, and teams have multiple users.
asana_user_team_association = Table(
    "asana_user_team_association",
    Base.metadata,
    Column("user_gid", ForeignKey("asana_users.gid"), primary_key=True),
    Column("team_gid", ForeignKey("asana_teams.gid"), primary_key=True),
)

# Tasks can belong to multiple projects, and projects contain multiple tasks.
asana_task_project_association = Table(
    "asana_task_project_association",
    Base.metadata,
    Column("task_gid", ForeignKey("asana_tasks.gid"), primary_key=True),
    Column("project_gid", ForeignKey("asana_projects.gid"), primary_key=True),
)

# Tasks can have multiple tags, and tags can be on multiple tasks.
asana_task_tag_association = Table(
    "asana_task_tag_association",
    Base.metadata,
    Column("task_gid", ForeignKey("asana_tasks.gid"), primary_key=True),
    Column("tag_gid", ForeignKey("asana_tags.gid"), primary_key=True),
)


# ---------------------------------------------------------------------------
# Stub models — expanded when each resource is implemented
# ---------------------------------------------------------------------------

class AsanaTag(Base):
    __tablename__ = "asana_tags"
    __table_args__ = (
        Index("ix_asana_tags_workspace", "workspace_gid"),
    )

    # Identity
    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="tag")
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # TagBase fields
    color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # TagResponse fields
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    permalink_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Stored as JSONB — array of user compact objects
    followers: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # FK: workspace → asana_workspaces
    workspace_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_workspaces.gid"), nullable=True
    )
    workspace_ref: Mapped[Optional["AsanaWorkspace"]] = relationship(
        back_populates="tags"
    )

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # M:N: tasks ↔ tags
    tasks: Mapped[list["AsanaTask"]] = relationship(
        secondary=asana_task_tag_association, back_populates="tags"
    )

    stories: Mapped[list["AsanaStory"]] = relationship(
        back_populates="tag_ref"
    )


class AsanaTeam(Base):
    __tablename__ = "asana_teams"
    __table_args__ = (
        Index("ix_asana_teams_organization", "organization_gid"),
    )

    # Identity
    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="team")
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # TeamRequest / TeamResponse fields
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    html_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    permalink_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    visibility: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    edit_team_name_or_description_access_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    edit_team_visibility_or_trash_team_access_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    member_invite_management_access_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    guest_invite_management_access_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    join_request_management_access_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    team_member_removal_access_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    team_content_management_access_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    endorsed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # FK: organization → asana_workspaces
    organization_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_workspaces.gid"), nullable=True
    )
    organization_ref: Mapped[Optional["AsanaWorkspace"]] = relationship(
        back_populates="teams"
    )

    # Custom field settings stored as JSONB array
    custom_field_settings: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Team members stored as JSONB array of user compact objects
    members: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    projects: Mapped[list["AsanaProject"]] = relationship(
        back_populates="team_ref"
    )

    # M:N: users ↔ teams
    users: Mapped[list["AsanaUser"]] = relationship(
        secondary=asana_user_team_association, back_populates="teams"
    )


class AsanaUser(Base):
    __tablename__ = "asana_users"

    # Identity
    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="user")
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # UserBaseResponse fields
    email: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    photo: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # UserResponse fields (arrays of compact refs, stored as JSONB)
    workspaces: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    custom_fields: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    owned_projects: Mapped[list["AsanaProject"]] = relationship(
        back_populates="owner_ref", foreign_keys="AsanaProject.owner_gid"
    )
    completed_projects: Mapped[list["AsanaProject"]] = relationship(
        back_populates="completed_by_ref", foreign_keys="AsanaProject.completed_by_gid"
    )

    # Incoming: tasks reference users via assignee, completed_by, assigned_by
    assigned_tasks: Mapped[list["AsanaTask"]] = relationship(
        back_populates="assignee_ref", foreign_keys="AsanaTask.assignee_gid"
    )
    completed_tasks: Mapped[list["AsanaTask"]] = relationship(
        back_populates="completed_by_ref", foreign_keys="AsanaTask.completed_by_gid"
    )
    assigned_by_tasks: Mapped[list["AsanaTask"]] = relationship(
        back_populates="assigned_by_ref", foreign_keys="AsanaTask.assigned_by_gid"
    )

    # M:N: users ↔ teams
    teams: Mapped[list["AsanaTeam"]] = relationship(
        secondary=asana_user_team_association, back_populates="users"
    )

    # M:N: users ↔ workspaces
    workspace_refs: Mapped[list["AsanaWorkspace"]] = relationship(
        secondary=asana_user_workspace_association, back_populates="users"
    )

    # Incoming: stories reference users via created_by, assignee, follower
    created_stories: Mapped[list["AsanaStory"]] = relationship(
        back_populates="created_by_ref", foreign_keys="AsanaStory.created_by_gid"
    )
    assigned_stories: Mapped[list["AsanaStory"]] = relationship(
        back_populates="assignee_ref", foreign_keys="AsanaStory.assignee_gid"
    )
    followed_stories: Mapped[list["AsanaStory"]] = relationship(
        back_populates="follower_ref", foreign_keys="AsanaStory.follower_gid"
    )


class AsanaWorkspace(Base):
    __tablename__ = "asana_workspaces"

    # Identity
    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="workspace")
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # WorkspaceResponse fields
    email_domains: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    is_organization: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    projects: Mapped[list["AsanaProject"]] = relationship(
        back_populates="workspace_ref"
    )
    tags: Mapped[list["AsanaTag"]] = relationship(
        back_populates="workspace_ref"
    )
    tasks: Mapped[list["AsanaTask"]] = relationship(
        back_populates="workspace_ref"
    )
    teams: Mapped[list["AsanaTeam"]] = relationship(
        back_populates="organization_ref"
    )

    # M:N: users ↔ workspaces
    users: Mapped[list["AsanaUser"]] = relationship(
        secondary=asana_user_workspace_association, back_populates="workspace_refs"
    )


class AsanaTask(Base):
    __tablename__ = "asana_tasks"
    __table_args__ = (
        Index("ix_asana_tasks_workspace", "workspace_gid"),
        Index("ix_asana_tasks_assignee", "assignee_gid"),
        Index("ix_asana_tasks_completed_by", "completed_by_gid"),
        Index("ix_asana_tasks_assigned_by", "assigned_by_gid"),
        Index("ix_asana_tasks_parent", "parent_gid"),
        Index("ix_asana_tasks_assignee_section", "assignee_section_gid"),
    )

    # Identity
    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="task")
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resource_subtype: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # TaskCompact: created_by stored as JSONB (compact user object)
    created_by: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # TaskBase fields
    approval_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    assignee_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    completed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    completed_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    due_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    due_on: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    external: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    html_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hearted: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    hearts: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    is_rendered_as_separator: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    liked: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    likes: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    memberships: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    modified_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    num_hearts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    num_likes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    num_subtasks: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    start_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    start_on: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    actual_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # FK: assignee → asana_users (multiple FKs to same table)
    assignee_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )
    # FK: assignee_section → asana_sections
    assignee_section_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_sections.gid"), nullable=True
    )
    # FK: completed_by → asana_users
    completed_by_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )
    # FK: assigned_by → asana_users
    assigned_by_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )
    # Self-referential FK: parent → asana_tasks
    parent_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_tasks.gid"), nullable=True
    )
    # FK: workspace → asana_workspaces
    workspace_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_workspaces.gid"), nullable=True
    )
    # Non-FK reference fields (custom_type is not a modeled resource)
    custom_type_gid: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    custom_type_status_option_gid: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # JSONB arrays/objects for nested data
    custom_fields: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    followers: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    dependencies: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    dependents: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # TaskResponse fields
    permalink_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # M:N relationships (already existed on stub)
    projects: Mapped[list["AsanaProject"]] = relationship(
        secondary=asana_task_project_association, back_populates="tasks"
    )
    tags: Mapped[list["AsanaTag"]] = relationship(
        secondary=asana_task_tag_association, back_populates="tasks"
    )

    # Incoming: stories reference tasks via task, duplicate_of, duplicated_from, dependency, target
    stories_as_task: Mapped[list["AsanaStory"]] = relationship(
        back_populates="task_ref", foreign_keys="AsanaStory.task_gid"
    )
    stories_as_duplicate_of: Mapped[list["AsanaStory"]] = relationship(
        back_populates="duplicate_of_ref", foreign_keys="AsanaStory.duplicate_of_gid"
    )
    stories_as_duplicated_from: Mapped[list["AsanaStory"]] = relationship(
        back_populates="duplicated_from_ref", foreign_keys="AsanaStory.duplicated_from_gid"
    )
    stories_as_dependency: Mapped[list["AsanaStory"]] = relationship(
        back_populates="dependency_ref", foreign_keys="AsanaStory.dependency_gid"
    )

    # FK relationships: users (multiple FKs to same table, need foreign_keys=)
    assignee_ref: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="assigned_tasks", foreign_keys=[assignee_gid]
    )
    completed_by_ref: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="completed_tasks", foreign_keys=[completed_by_gid]
    )
    assigned_by_ref: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="assigned_by_tasks", foreign_keys=[assigned_by_gid]
    )

    # FK relationship: workspace
    workspace_ref: Mapped[Optional["AsanaWorkspace"]] = relationship(
        back_populates="tasks"
    )

    # FK relationship: assignee_section
    assignee_section_ref: Mapped[Optional["AsanaSection"]] = relationship(
        back_populates="tasks_as_assignee_section"
    )

    # Self-referential: parent/children
    parent: Mapped[Optional["AsanaTask"]] = relationship(
        remote_side=[gid], back_populates="subtasks"
    )
    subtasks: Mapped[list["AsanaTask"]] = relationship(
        back_populates="parent"
    )

class AsanaSection(Base):
    __tablename__ = "asana_sections"
    __table_args__ = (
        Index("ix_asana_sections_project", "project_gid"),
        Index("ix_asana_sections_parent", "parent_gid"),
    )

    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="section")
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # FK: project → asana_projects
    project_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_projects.gid"), nullable=True
    )
    project: Mapped[Optional["AsanaProject"]] = relationship(
        back_populates="sections"
    )

    # Self-referential FK: parent section
    parent_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_sections.gid"), nullable=True
    )
    parent: Mapped[Optional["AsanaSection"]] = relationship(
        remote_side=[gid], back_populates="children"
    )
    children: Mapped[list["AsanaSection"]] = relationship(
        back_populates="parent"
    )

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Incoming: tasks reference sections via assignee_section
    tasks_as_assignee_section: Mapped[list["AsanaTask"]] = relationship(
        back_populates="assignee_section_ref"
    )

    # Incoming: stories reference sections via old_section / new_section
    stories_as_old_section: Mapped[list["AsanaStory"]] = relationship(
        back_populates="old_section_ref", foreign_keys="AsanaStory.old_section_gid"
    )
    stories_as_new_section: Mapped[list["AsanaStory"]] = relationship(
        back_populates="new_section_ref", foreign_keys="AsanaStory.new_section_gid"
    )


class AsanaStory(Base):
    __tablename__ = "asana_stories"
    __table_args__ = (
        Index("ix_asana_stories_project", "project_gid"),
        Index("ix_asana_stories_old_section", "old_section_gid"),
        Index("ix_asana_stories_new_section", "new_section_gid"),
        Index("ix_asana_stories_target_gid", "target_gid"),
        Index("ix_asana_stories_task_gid", "task_gid"),
        Index("ix_asana_stories_tag", "tag_gid"),
        Index("ix_asana_stories_story", "story_gid"),
        Index("ix_asana_stories_duplicate_of", "duplicate_of_gid"),
        Index("ix_asana_stories_duplicated_from", "duplicated_from_gid"),
        Index("ix_asana_stories_dependency", "dependency_gid"),
        Index("ix_asana_stories_created_by", "created_by_gid"),
        Index("ix_asana_stories_assignee", "assignee_gid"),
        Index("ix_asana_stories_follower", "follower_gid"),
    )

    # Identity
    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="story")
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # StoryBase fields
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    resource_subtype: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    html_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_pinned: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    sticker_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # FK: created_by → asana_users
    created_by_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )

    # StoryResponse fields
    type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_editable: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_edited: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    hearted: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    hearts: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    num_hearts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    liked: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    likes: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    num_likes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reaction_summary: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    previews: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Conditional name-change fields
    old_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    new_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Conditional subtype-change fields
    old_resource_subtype: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    new_resource_subtype: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Conditional text custom field change
    old_text_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_text_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Conditional number custom field change
    old_number_value: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    new_number_value: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Conditional approval status change
    old_approval_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    new_approval_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Conditional date fields stored as JSONB (StoryResponseDates shape)
    old_dates: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    new_dates: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    old_date_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    new_date_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Conditional enum fields stored as JSONB
    old_enum_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    new_enum_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    old_multi_enum_values: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    new_multi_enum_values: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Conditional people fields stored as JSONB
    old_people_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    new_people_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # FK: self-referential story → asana_stories
    story_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_stories.gid"), nullable=True
    )

    # FK: assignee → asana_users
    assignee_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )

    # FK: follower → asana_users
    follower_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )

    # FK: task → asana_tasks
    task_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_tasks.gid"), nullable=True
    )

    # FK: tag → asana_tags
    tag_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_tags.gid"), nullable=True
    )

    # No FK — custom fields are not a modeled resource
    custom_field_gid: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # FK: duplicate_of → asana_tasks
    duplicate_of_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_tasks.gid"), nullable=True
    )

    # FK: duplicated_from → asana_tasks
    duplicated_from_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_tasks.gid"), nullable=True
    )

    # FK: dependency → asana_tasks
    dependency_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_tasks.gid"), nullable=True
    )

    # Target can reference tasks or goals — no FK constraint since it's polymorphic
    target_gid: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # --- FK relationships ---

    # project → asana_projects (set up by sections Pass 2)
    project_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_projects.gid"), nullable=True
    )
    project: Mapped[Optional["AsanaProject"]] = relationship(
        back_populates="stories"
    )

    # old_section / new_section → asana_sections (set up by sections Pass 2)
    old_section_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_sections.gid"), nullable=True
    )
    old_section_ref: Mapped[Optional["AsanaSection"]] = relationship(
        back_populates="stories_as_old_section", foreign_keys=[old_section_gid]
    )

    new_section_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_sections.gid"), nullable=True
    )
    new_section_ref: Mapped[Optional["AsanaSection"]] = relationship(
        back_populates="stories_as_new_section", foreign_keys=[new_section_gid]
    )

    # tag → asana_tags
    tag_ref: Mapped[Optional["AsanaTag"]] = relationship(
        back_populates="stories"
    )

    # Self-referential: story → asana_stories
    parent_story: Mapped[Optional["AsanaStory"]] = relationship(
        remote_side=[gid], back_populates="child_stories", foreign_keys=[story_gid]
    )
    child_stories: Mapped[list["AsanaStory"]] = relationship(
        back_populates="parent_story", foreign_keys=[story_gid]
    )

    # task → asana_tasks (multiple FKs to same table, need foreign_keys=)
    task_ref: Mapped[Optional["AsanaTask"]] = relationship(
        back_populates="stories_as_task", foreign_keys=[task_gid]
    )
    duplicate_of_ref: Mapped[Optional["AsanaTask"]] = relationship(
        back_populates="stories_as_duplicate_of", foreign_keys=[duplicate_of_gid]
    )
    duplicated_from_ref: Mapped[Optional["AsanaTask"]] = relationship(
        back_populates="stories_as_duplicated_from", foreign_keys=[duplicated_from_gid]
    )
    dependency_ref: Mapped[Optional["AsanaTask"]] = relationship(
        back_populates="stories_as_dependency", foreign_keys=[dependency_gid]
    )
    # users → asana_users (multiple FKs to same table, need foreign_keys=)
    created_by_ref: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="created_stories", foreign_keys=[created_by_gid]
    )
    assignee_ref: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="assigned_stories", foreign_keys=[assignee_gid]
    )
    follower_ref: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="followed_stories", foreign_keys=[follower_gid]
    )


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

class AsanaProject(Base):
    __tablename__ = "asana_projects"
    __table_args__ = (
        Index("ix_asana_projects_team", "team_gid"),
        Index("ix_asana_projects_owner", "owner_gid"),
        Index("ix_asana_projects_completed_by", "completed_by_gid"),
        Index("ix_asana_projects_workspace", "workspace_gid"),
        Index("ix_asana_projects_parent", "parent_gid"),
    )

    # Identity
    gid: Mapped[str] = mapped_column(String(50), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="project")
    name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # ProjectBase fields
    archived: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    default_view: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    due_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    due_on: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    html_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    modified_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    public: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    privacy_setting: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    start_on: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    default_access_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    minimum_access_level_for_customization: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    minimum_access_level_for_sharing: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # ProjectResponse fields
    completed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    completed_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    permalink_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # FK: completed_by → asana_users
    completed_by_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )
    completed_by_ref: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="completed_projects", foreign_keys=[completed_by_gid]
    )

    # FK: owner → asana_users
    owner_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_users.gid"), nullable=True
    )
    owner_ref: Mapped[Optional["AsanaUser"]] = relationship(
        back_populates="owned_projects", foreign_keys=[owner_gid]
    )

    # FK: team → asana_teams
    team_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_teams.gid"), nullable=True
    )
    team_ref: Mapped[Optional["AsanaTeam"]] = relationship(
        back_populates="projects"
    )

    # FK: workspace → asana_workspaces
    workspace_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_workspaces.gid"), nullable=True
    )
    workspace_ref: Mapped[Optional["AsanaWorkspace"]] = relationship(
        back_populates="projects"
    )

    # Self-referential FK: parent project
    parent_gid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("asana_projects.gid"), nullable=True
    )
    parent: Mapped[Optional["AsanaProject"]] = relationship(
        remote_side=[gid], back_populates="children"
    )
    children: Mapped[list["AsanaProject"]] = relationship(
        back_populates="parent"
    )

    # Non-FK reference fields stored as plain strings
    created_from_template: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    project_brief: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Nested objects stored as JSONB
    current_status: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    current_status_update: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    custom_field_settings: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    custom_fields: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    members: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    followers: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Incoming relationships
    sections: Mapped[list["AsanaSection"]] = relationship(
        back_populates="project"
    )
    stories: Mapped[list["AsanaStory"]] = relationship(
        back_populates="project"
    )
    tasks: Mapped[list["AsanaTask"]] = relationship(
        secondary=asana_task_project_association, back_populates="projects"
    )
