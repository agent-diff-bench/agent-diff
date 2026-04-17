"""GitHub API replica schema.

Follows GitHub's real data model: issues and pull requests live in the same
number space per repo. A single ``github_issues`` table stores both, with
``is_pull_request`` distinguishing them. PR-only fields are nullable.

Only the surface needed for the bench is modeled: issues, pulls, labels,
assignees, requested reviewers, and issue/PR comments (GitHub calls them
"issue comments" even when attached to a PR).
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "github_users"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    login: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(128))
    email: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    type: Mapped[str] = mapped_column(String(16), default="User")
    site_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def to_mini_dict(self) -> dict:
        return {
            "login": self.login,
            "id": int(self.id) if self.id.isdigit() else self.id,
            "node_id": f"U_{self.id}",
            "type": self.type,
            "site_admin": self.site_admin,
            "url": f"https://api.github.com/users/{self.login}",
            "html_url": f"https://github.com/{self.login}",
            "avatar_url": f"https://github.com/{self.login}.png",
        }


class Repository(Base):
    __tablename__ = "github_repositories"
    __table_args__ = (
        UniqueConstraint("owner_id", "name", name="uq_github_repo_owner_name"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    owner_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_users.id"), index=True
    )
    name: Mapped[str] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    private: Mapped[bool] = mapped_column(Boolean, default=False)
    default_branch: Mapped[str] = mapped_column(String(128), default="main")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner: Mapped["User"] = relationship("User")
    issues: Mapped[List["Issue"]] = relationship("Issue", back_populates="repository")
    labels: Mapped[List["Label"]] = relationship("Label", back_populates="repository")

    def to_dict(self) -> dict:
        return {
            "id": int(self.id) if self.id.isdigit() else self.id,
            "node_id": f"R_{self.id}",
            "name": self.name,
            "full_name": self.full_name,
            "owner": self.owner.to_mini_dict() if self.owner else None,
            "private": self.private,
            "description": self.description,
            "default_branch": self.default_branch,
            "url": f"https://api.github.com/repos/{self.full_name}",
            "html_url": f"https://github.com/{self.full_name}",
        }


class Label(Base):
    __tablename__ = "github_labels"
    __table_args__ = (
        UniqueConstraint("repository_id", "name", name="uq_github_label_repo_name"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    repository_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_repositories.id"), index=True
    )
    name: Mapped[str] = mapped_column(String(128))
    color: Mapped[str] = mapped_column(String(8), default="ededed")
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    repository: Mapped["Repository"] = relationship(
        "Repository", back_populates="labels"
    )

    def to_dict(self) -> dict:
        return {
            "id": int(self.id) if self.id.isdigit() else self.id,
            "node_id": f"L_{self.id}",
            "name": self.name,
            "color": self.color,
            "description": self.description,
            "default": self.is_default,
            "url": (
                f"https://api.github.com/repos/{self.repository.full_name}/labels/{self.name}"
                if self.repository
                else None
            ),
        }


class Issue(Base):
    """Unified issue + pull request row.

    When ``is_pull_request`` is true, the PR-specific fields (head_ref,
    base_ref, merged, etc.) are populated and the row represents a PR.
    GitHub's ``/issues`` list endpoint also returns PRs (with a
    ``pull_request`` field); this mirrors that shape.
    """

    __tablename__ = "github_issues"
    __table_args__ = (
        UniqueConstraint("repository_id", "number", name="uq_github_issue_repo_number"),
        Index("ix_github_issues_state", "repository_id", "state"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    repository_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_repositories.id"), index=True
    )
    number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    body: Mapped[Optional[str]] = mapped_column(Text)
    state: Mapped[str] = mapped_column(String(16), default="open")
    state_reason: Mapped[Optional[str]] = mapped_column(String(32))
    user_id: Mapped[Optional[str]] = mapped_column(
        String(32), ForeignKey("github_users.id"), index=True
    )
    locked: Mapped[bool] = mapped_column(Boolean, default=False)
    comments_count: Mapped[int] = mapped_column(Integer, default=0)

    is_pull_request: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", index=True
    )
    draft: Mapped[Optional[bool]] = mapped_column(Boolean)
    merged: Mapped[Optional[bool]] = mapped_column(Boolean)
    merged_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    merged_by_id: Mapped[Optional[str]] = mapped_column(
        String(32), ForeignKey("github_users.id")
    )
    merge_commit_sha: Mapped[Optional[str]] = mapped_column(String(64))
    head_ref: Mapped[Optional[str]] = mapped_column(String(255))
    base_ref: Mapped[Optional[str]] = mapped_column(String(255))
    head_sha: Mapped[Optional[str]] = mapped_column(String(64))
    base_sha: Mapped[Optional[str]] = mapped_column(String(64))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    repository: Mapped["Repository"] = relationship(
        "Repository", back_populates="issues"
    )
    user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[user_id])
    merged_by: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[merged_by_id]
    )
    labels: Mapped[List["IssueLabel"]] = relationship(
        "IssueLabel", back_populates="issue", cascade="all, delete-orphan"
    )
    assignees: Mapped[List["IssueAssignee"]] = relationship(
        "IssueAssignee", back_populates="issue", cascade="all, delete-orphan"
    )
    requested_reviewers: Mapped[List["PullRequestReviewer"]] = relationship(
        "PullRequestReviewer", back_populates="issue", cascade="all, delete-orphan"
    )
    comments: Mapped[List["IssueComment"]] = relationship(
        "IssueComment",
        back_populates="issue",
        cascade="all, delete-orphan",
        order_by="IssueComment.created_at",
    )

    def _base_dict(self) -> dict:
        full_name = self.repository.full_name if self.repository else ""
        labels = [il.label.to_dict() for il in self.labels if il.label]
        assignees = [ia.user.to_mini_dict() for ia in self.assignees if ia.user]
        url_base = f"https://api.github.com/repos/{full_name}"
        return {
            "id": int(self.id) if self.id.isdigit() else self.id,
            "node_id": f"I_{self.id}",
            "number": self.number,
            "title": self.title,
            "body": self.body,
            "state": self.state,
            "state_reason": self.state_reason,
            "locked": self.locked,
            "comments": self.comments_count,
            "user": self.user.to_mini_dict() if self.user else None,
            "labels": labels,
            "assignee": assignees[0] if assignees else None,
            "assignees": assignees,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "url": f"{url_base}/issues/{self.number}",
            "html_url": f"https://github.com/{full_name}/issues/{self.number}",
            "repository_url": url_base,
        }

    def to_issue_dict(self) -> dict:
        data = self._base_dict()
        if self.is_pull_request:
            full_name = self.repository.full_name if self.repository else ""
            data["pull_request"] = {
                "url": f"https://api.github.com/repos/{full_name}/pulls/{self.number}",
                "html_url": f"https://github.com/{full_name}/pull/{self.number}",
                "merged_at": self.merged_at.isoformat() if self.merged_at else None,
            }
        return data

    def to_pull_dict(self) -> dict:
        data = self._base_dict()
        full_name = self.repository.full_name if self.repository else ""
        data["url"] = f"https://api.github.com/repos/{full_name}/pulls/{self.number}"
        data["html_url"] = f"https://github.com/{full_name}/pull/{self.number}"
        reviewers = [
            prr.user.to_mini_dict() for prr in self.requested_reviewers if prr.user
        ]
        data.update(
            {
                "draft": bool(self.draft),
                "merged": bool(self.merged),
                "merged_at": self.merged_at.isoformat() if self.merged_at else None,
                "merged_by": self.merged_by.to_mini_dict() if self.merged_by else None,
                "merge_commit_sha": self.merge_commit_sha,
                "head": {
                    "ref": self.head_ref,
                    "sha": self.head_sha,
                    "label": f"{self.repository.owner.login}:{self.head_ref}"
                    if self.repository and self.repository.owner and self.head_ref
                    else self.head_ref,
                },
                "base": {
                    "ref": self.base_ref,
                    "sha": self.base_sha,
                    "label": f"{self.repository.owner.login}:{self.base_ref}"
                    if self.repository and self.repository.owner and self.base_ref
                    else self.base_ref,
                },
                "requested_reviewers": reviewers,
                "requested_teams": [],
            }
        )
        return data


class IssueLabel(Base):
    __tablename__ = "github_issue_labels"

    issue_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_issues.id"), primary_key=True
    )
    label_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_labels.id"), primary_key=True
    )

    issue: Mapped["Issue"] = relationship("Issue", back_populates="labels")
    label: Mapped["Label"] = relationship("Label")


class IssueAssignee(Base):
    __tablename__ = "github_issue_assignees"

    issue_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_issues.id"), primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_users.id"), primary_key=True
    )

    issue: Mapped["Issue"] = relationship("Issue", back_populates="assignees")
    user: Mapped["User"] = relationship("User")


class PullRequestReviewer(Base):
    __tablename__ = "github_pull_request_reviewers"

    issue_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_issues.id"), primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_users.id"), primary_key=True
    )

    issue: Mapped["Issue"] = relationship("Issue", back_populates="requested_reviewers")
    user: Mapped["User"] = relationship("User")


class IssueComment(Base):
    """Comments on an issue or pull request.

    GitHub unifies these — both surface through
    ``/repos/{owner}/{repo}/issues/{number}/comments`` and PR review-thread
    comments are a separate system.
    """

    __tablename__ = "github_issue_comments"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    issue_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("github_issues.id"), index=True
    )
    user_id: Mapped[Optional[str]] = mapped_column(
        String(32), ForeignKey("github_users.id")
    )
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    issue: Mapped["Issue"] = relationship("Issue", back_populates="comments")
    user: Mapped[Optional["User"]] = relationship("User")

    def to_dict(self) -> dict:
        full_name = (
            self.issue.repository.full_name
            if self.issue and self.issue.repository
            else ""
        )
        number = self.issue.number if self.issue else None
        return {
            "id": int(self.id) if self.id.isdigit() else self.id,
            "node_id": f"IC_{self.id}",
            "user": self.user.to_mini_dict() if self.user else None,
            "body": self.body,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "issue_url": f"https://api.github.com/repos/{full_name}/issues/{number}",
            "url": f"https://api.github.com/repos/{full_name}/issues/comments/{self.id}",
            "html_url": f"https://github.com/{full_name}/issues/{number}#issuecomment-{self.id}",
        }
