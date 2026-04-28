"""ORM schema for the GitHub API replica.

Entities are added to this file one at a time during the resource
implementation loop. Each entity implementation may also add stub models
for FK dependencies marked with: # STUB — expand when implementing this resource

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its model class to this file incrementally.
"""

from typing import Any, Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# ---------------------------------------------------------------------------
# Users (stub)
# ---------------------------------------------------------------------------

class GitHubUser(Base):
    """# STUB — expand when implementing this resource"""
    __tablename__ = "github_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    login: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Reverse relationships to gists
    owned_gists: Mapped[list["GitHubGist"]] = relationship(
        back_populates="owner_rel", foreign_keys="GitHubGist.owner_id"
    )
    user_gists: Mapped[list["GitHubGist"]] = relationship(
        back_populates="user_rel", foreign_keys="GitHubGist.user_id"
    )

    # Reverse relationships to issues
    created_issues: Mapped[list["GitHubIssue"]] = relationship(
        back_populates="user_rel", foreign_keys="GitHubIssue.user_id"
    )
    closed_issues: Mapped[list["GitHubIssue"]] = relationship(
        back_populates="closed_by_rel", foreign_keys="GitHubIssue.closed_by_id"
    )


# ---------------------------------------------------------------------------
# Gists
# ---------------------------------------------------------------------------

class GitHubGist(Base):
    __tablename__ = "github_gists"
    __table_args__ = (
        Index("ix_github_gists_owner_id", "owner_id"),
        Index("ix_github_gists_user_id", "user_id"),
        Index("ix_github_gists_fork_of_id", "fork_of_id"),
    )

    # Identity
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    node_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # URLs
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    forks_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    commits_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    git_pull_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    git_push_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    html_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    comments_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Content
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    files: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    public: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    truncated: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # Counters
    comments: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    comments_enabled: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # FK to users — owner is the gist creator, user is typically the same
    owner_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("github_users.id"), nullable=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("github_users.id"), nullable=True
    )

    # Self-referential FK for fork_of
    fork_of_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("github_gists.id"), nullable=True
    )

    # History/forks arrays stored as JSONB
    forks: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    history: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Timestamps
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships — multiple FKs to same target need foreign_keys=
    owner_rel: Mapped[Optional["GitHubUser"]] = relationship(
        back_populates="owned_gists", foreign_keys=[owner_id]
    )
    user_rel: Mapped[Optional["GitHubUser"]] = relationship(
        back_populates="user_gists", foreign_keys=[user_id]
    )

    # Self-referential: fork_of
    fork_of_rel: Mapped[Optional["GitHubGist"]] = relationship(
        remote_side=[id], back_populates="forked_gists"
    )
    forked_gists: Mapped[list["GitHubGist"]] = relationship(
        back_populates="fork_of_rel"
    )


class GitHubGistComment(Base):
    __tablename__ = "github_gist_comments"
    __table_args__ = (
        Index("ix_github_gist_comments_gist_id", "gist_id"),
        Index("ix_github_gist_comments_user_id", "user_id"),
    )

    # Identity — gist comment IDs are integers
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    node_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Parent gist FK
    gist_id: Mapped[str] = mapped_column(
        ForeignKey("github_gists.id"), nullable=False
    )

    # Content
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author_association: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="NONE")

    # User FK
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("github_users.id"), nullable=True
    )

    # Timestamps
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    gist: Mapped["GitHubGist"] = relationship()
    user_rel: Mapped[Optional["GitHubUser"]] = relationship()


class GitHubGistStar(Base):
    """Tracks which users have starred which gists."""
    __tablename__ = "github_gist_stars"
    __table_args__ = (
        Index("ix_github_gist_stars_gist_id", "gist_id"),
        Index("ix_github_gist_stars_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    gist_id: Mapped[str] = mapped_column(
        ForeignKey("github_gists.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(String(50), nullable=False)


# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------

class GitHubIssue(Base):
    __tablename__ = "github_issues"
    __table_args__ = (
        Index("ix_github_issues_repo_number", "repo_owner", "repo_name", "number", unique=True),
        Index("ix_github_issues_state", "state"),
        Index("ix_github_issues_user_id", "user_id"),
        Index("ix_github_issues_closed_by_id", "closed_by_id"),
        Index("ix_github_issues_parent_id", "parent_id"),
    )

    # Identity
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    node_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Repository context (denormalized — no FK in pass 1)
    repo_owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    repo_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # URLs
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    repository_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    labels_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    comments_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    events_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    html_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    timeline_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Core fields
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(1000), nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    body_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    body_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    state: Mapped[str] = mapped_column(String(20), nullable=False, default="open")
    state_reason: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    locked: Mapped[bool] = mapped_column(Boolean, default=False)
    active_lock_reason: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Counters
    comments: Mapped[int] = mapped_column(Integer, default=0)

    # User references — FK to github_users
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("github_users.id"), nullable=True
    )
    closed_by_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("github_users.id"), nullable=True
    )

    # Self-referential FK for parent issue hierarchy
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("github_issues.id"), nullable=True
    )

    # JSONB fields for nested/array data
    labels: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    assignees: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    milestone: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    pull_request: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    reactions: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    sub_issues_summary: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    issue_dependencies_summary: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    issue_field_values: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    performed_via_github_app: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Misc optional fields
    draft: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    author_association: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="NONE")
    issue_type: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    parent_issue_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Timestamps
    closed_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships — multiple FKs to same target need foreign_keys=
    user_rel: Mapped[Optional["GitHubUser"]] = relationship(
        foreign_keys=[user_id], back_populates="created_issues"
    )
    closed_by_rel: Mapped[Optional["GitHubUser"]] = relationship(
        foreign_keys=[closed_by_id], back_populates="closed_issues"
    )

    # Self-referential: parent/child issue hierarchy
    parent_rel: Mapped[Optional["GitHubIssue"]] = relationship(
        remote_side="GitHubIssue.id", back_populates="child_issues",
        foreign_keys=[parent_id],
    )
    child_issues: Mapped[list["GitHubIssue"]] = relationship(
        back_populates="parent_rel", foreign_keys=[parent_id],
    )


class GitHubIssueComment(Base):
    __tablename__ = "github_issue_comments"
    __table_args__ = (
        Index("ix_github_issue_comments_issue_id", "issue_id"),
        Index("ix_github_issue_comments_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    node_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Parent context
    issue_id: Mapped[int] = mapped_column(Integer, nullable=False)
    repo_owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    repo_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # URLs
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    html_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    issue_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Content
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    body_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    body_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # User reference
    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Metadata
    author_association: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="NONE")
    performed_via_github_app: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    reactions: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    pin: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Timestamps
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class GitHubIssueEvent(Base):
    __tablename__ = "github_issue_events"
    __table_args__ = (
        Index("ix_github_issue_events_issue_id", "issue_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    node_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Parent context
    issue_id: Mapped[int] = mapped_column(Integer, nullable=False)
    repo_owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    repo_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # URLs
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Event data
    event: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    commit_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    commit_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    actor_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    author_association: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    lock_reason: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    performed_via_github_app: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Event-specific payload stored as JSONB
    label: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    assignee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    assigner_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    review_requester_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    requested_reviewer_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    requested_team: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    dismissed_review: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    milestone: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    project_card: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    rename: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Timestamp
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Soft-delete
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class GitHubIssueReaction(Base):
    """Tracks reactions on issues and issue comments."""
    __tablename__ = "github_issue_reactions"
    __table_args__ = (
        Index("ix_github_issue_reactions_issue_id", "issue_id"),
        Index("ix_github_issue_reactions_comment_id", "comment_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    node_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Which entity this reaction belongs to (one of these will be set)
    issue_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comment_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Context
    repo_owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    repo_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Reaction data
    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
