"""Serialization helpers for the GitHub API replica.

Each serialize function converts an ORM model into a dict matching the
source API's response shape. Functions are added one at a time during the
resource implementation loop.

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its serializer functions to this file incrementally.
"""

from __future__ import annotations

from typing import Any, Optional

from ..database.schema import (
    GitHubGist, GitHubGistComment, GitHubUser,
    GitHubIssue, GitHubIssueComment, GitHubIssueEvent, GitHubIssueReaction,
)


# ---------------------------------------------------------------------------
# User serialization helper
# ---------------------------------------------------------------------------

def _serialize_user(user: Optional[GitHubUser]) -> Optional[dict[str, Any]]:
    """Build a simple-user shaped dict from a GitHubUser, or None."""
    if user is None:
        return None
    login = user.login or str(user.id)
    return {
        "login": login,
        "id": user.id,
        "node_id": f"U_{user.id}",
        "avatar_url": f"https://avatars.githubusercontent.com/u/{user.id}?v=4",
        "gravatar_id": "",
        "url": f"https://api.github.com/users/{login}",
        "html_url": f"https://github.com/{login}",
        "followers_url": f"https://api.github.com/users/{login}/followers",
        "following_url": f"https://api.github.com/users/{login}/following{{/other_user}}",
        "gists_url": f"https://api.github.com/users/{login}/gists{{/gist_id}}",
        "starred_url": f"https://api.github.com/users/{login}/starred{{/owner}}{{/repo}}",
        "subscriptions_url": f"https://api.github.com/users/{login}/subscriptions",
        "organizations_url": f"https://api.github.com/users/{login}/orgs",
        "repos_url": f"https://api.github.com/users/{login}/repos",
        "events_url": f"https://api.github.com/users/{login}/events{{/privacy}}",
        "received_events_url": f"https://api.github.com/users/{login}/received_events",
        "type": "User",
        "site_admin": False,
    }


def _serialize_fork_of(gist: Optional[GitHubGist]) -> Optional[dict[str, Any]]:
    """Serialize the fork_of relationship as a nested gist object."""
    if gist is None:
        return None
    return {
        "url": gist.url,
        "forks_url": gist.forks_url,
        "commits_url": gist.commits_url,
        "id": gist.id,
        "node_id": gist.node_id,
        "git_pull_url": gist.git_pull_url,
        "git_push_url": gist.git_push_url,
        "html_url": gist.html_url,
        "public": gist.public,
        "created_at": gist.created_at,
        "updated_at": gist.updated_at,
        "description": gist.description,
        "comments": gist.comments or 0,
        "comments_url": gist.comments_url,
        "owner": _serialize_user(gist.owner_rel),
        "user": _serialize_user(gist.user_rel),
        "truncated": gist.truncated or False,
    }


# ---------------------------------------------------------------------------
# Gists — base-gist shape (used in list endpoints)
# ---------------------------------------------------------------------------

def serialize_gist_base(gist: GitHubGist) -> dict[str, Any]:
    """base-gist schema shape for collection endpoints."""
    # Strip content from files for list responses
    files_without_content = {}
    if gist.files:
        for filename, file_data in gist.files.items():
            entry = dict(file_data) if isinstance(file_data, dict) else {}
            entry.pop("content", None)
            entry.pop("truncated", None)
            files_without_content[filename] = entry

    return {
        "url": gist.url,
        "forks_url": gist.forks_url,
        "commits_url": gist.commits_url,
        "id": gist.id,
        "node_id": gist.node_id,
        "git_pull_url": gist.git_pull_url,
        "git_push_url": gist.git_push_url,
        "html_url": gist.html_url,
        "files": files_without_content,
        "public": gist.public,
        "created_at": gist.created_at,
        "updated_at": gist.updated_at,
        "description": gist.description,
        "comments": gist.comments or 0,
        "comments_enabled": gist.comments_enabled,
        "comments_url": gist.comments_url,
        "owner": _serialize_user(gist.owner_rel),
        "truncated": gist.truncated or False,
    }


def serialize_gist_list(gists: list[GitHubGist]) -> list[dict[str, Any]]:
    """Array of base-gist objects."""
    return [serialize_gist_base(gist) for gist in gists]


# ---------------------------------------------------------------------------
# Gists — gist-simple shape (used in single-gist endpoints)
# ---------------------------------------------------------------------------

def serialize_gist(gist: GitHubGist) -> dict[str, Any]:
    """gist-simple schema shape for detail endpoints."""
    return {
        "url": gist.url,
        "forks_url": gist.forks_url,
        "commits_url": gist.commits_url,
        "id": gist.id,
        "node_id": gist.node_id,
        "git_pull_url": gist.git_pull_url,
        "git_push_url": gist.git_push_url,
        "html_url": gist.html_url,
        "files": gist.files or {},
        "public": gist.public,
        "created_at": gist.created_at,
        "updated_at": gist.updated_at,
        "description": gist.description,
        "comments": gist.comments or 0,
        "comments_enabled": gist.comments_enabled,
        "comments_url": gist.comments_url,
        "user": _serialize_user(gist.user_rel),
        "owner": _serialize_user(gist.owner_rel),
        "truncated": gist.truncated or False,
        "forks": gist.forks or [],
        "history": gist.history or [],
        "fork_of": _serialize_fork_of(gist.fork_of_rel),
    }


# ---------------------------------------------------------------------------
# Gist comments — gist-comment shape
# ---------------------------------------------------------------------------

def serialize_gist_comment(comment: GitHubGistComment) -> dict[str, Any]:
    """gist-comment schema shape."""
    return {
        "id": comment.id,
        "node_id": comment.node_id,
        "url": comment.url,
        "body": comment.body,
        "user": _serialize_user(comment.user_rel),
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
        "author_association": comment.author_association or "NONE",
    }


def serialize_gist_comment_list(
    comments: list[GitHubGistComment],
) -> list[dict[str, Any]]:
    """Array of gist-comment objects."""
    return [serialize_gist_comment(comment) for comment in comments]


# ---------------------------------------------------------------------------
# Gist commits — gist-commit shape
# ---------------------------------------------------------------------------

def serialize_gist_commit(commit: dict[str, Any]) -> dict[str, Any]:
    """gist-commit schema shape."""
    return {
        "url": commit.get("url"),
        "version": commit.get("version"),
        "user": commit.get("user"),
        "change_status": commit.get("change_status", {}),
        "committed_at": commit.get("committed_at"),
    }


def serialize_gist_commit_list(
    commits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Array of gist-commit objects."""
    return [serialize_gist_commit(commit) for commit in commits]


# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------

def _serialize_user_by_id(user_id: Optional[int]) -> Optional[dict[str, Any]]:
    """Build a simple-user dict from a raw user ID (no DB lookup)."""
    if user_id is None:
        return None
    login = str(user_id)
    return {
        "login": login,
        "id": user_id,
        "node_id": f"U_{user_id}",
        "avatar_url": f"https://avatars.githubusercontent.com/u/{user_id}?v=4",
        "gravatar_id": "",
        "url": f"https://api.github.com/users/{login}",
        "html_url": f"https://github.com/{login}",
        "followers_url": f"https://api.github.com/users/{login}/followers",
        "following_url": f"https://api.github.com/users/{login}/following{{/other_user}}",
        "gists_url": f"https://api.github.com/users/{login}/gists{{/gist_id}}",
        "starred_url": f"https://api.github.com/users/{login}/starred{{/owner}}{{/repo}}",
        "subscriptions_url": f"https://api.github.com/users/{login}/subscriptions",
        "organizations_url": f"https://api.github.com/users/{login}/orgs",
        "repos_url": f"https://api.github.com/users/{login}/repos",
        "events_url": f"https://api.github.com/users/{login}/events{{/privacy}}",
        "received_events_url": f"https://api.github.com/users/{login}/received_events",
        "type": "User",
        "site_admin": False,
    }


def _serialize_issue_user(issue: GitHubIssue, rel_attr: str, id_attr: str) -> Optional[dict[str, Any]]:
    """Serialize a user from a relationship if loaded, falling back to ID-based."""
    from sqlalchemy import inspect as sa_inspect
    state = sa_inspect(issue, raiseerr=False)
    # Use relationship if it was eager-loaded; otherwise fall back to raw ID
    if state is not None and rel_attr in state.dict:
        return _serialize_user(state.dict[rel_attr])
    return _serialize_user_by_id(getattr(issue, id_attr, None))


def serialize_issue(issue: GitHubIssue) -> dict[str, Any]:
    """issue schema shape."""
    result: dict[str, Any] = {
        "id": issue.id,
        "node_id": issue.node_id,
        "url": issue.url,
        "repository_url": issue.repository_url,
        "labels_url": issue.labels_url,
        "comments_url": issue.comments_url,
        "events_url": issue.events_url,
        "html_url": issue.html_url,
        "number": issue.number,
        "state": issue.state,
        "state_reason": issue.state_reason,
        "title": issue.title,
        "body": issue.body,
        "user": _serialize_issue_user(issue, "user_rel", "user_id"),
        "labels": issue.labels or [],
        "assignees": issue.assignees or [],
        "milestone": issue.milestone,
        "locked": issue.locked,
        "active_lock_reason": issue.active_lock_reason,
        "comments": issue.comments or 0,
        "pull_request": issue.pull_request,
        "closed_at": issue.closed_at,
        "created_at": issue.created_at,
        "updated_at": issue.updated_at,
        "author_association": issue.author_association or "NONE",
        "draft": issue.draft,
        "closed_by": _serialize_issue_user(issue, "closed_by_rel", "closed_by_id"),
        "body_html": issue.body_html,
        "body_text": issue.body_text,
        "timeline_url": issue.timeline_url,
        "reactions": issue.reactions,
        "performed_via_github_app": issue.performed_via_github_app,
        "sub_issues_summary": issue.sub_issues_summary,
        "issue_dependencies_summary": issue.issue_dependencies_summary,
        "parent_issue_url": issue.parent_issue_url,
    }
    if issue.issue_type is not None:
        result["type"] = issue.issue_type
    if issue.issue_field_values is not None:
        result["issue_field_values"] = issue.issue_field_values
    return result


def serialize_issue_list(issues: list[GitHubIssue]) -> list[dict[str, Any]]:
    """Array of issue objects."""
    return [serialize_issue(issue) for issue in issues]


def serialize_issue_search_result(issue: GitHubIssue, score: float = 1.0) -> dict[str, Any]:
    """issue-search-result-item schema shape."""
    result = serialize_issue(issue)
    result["score"] = score
    return result


# ---------------------------------------------------------------------------
# Issue comments
# ---------------------------------------------------------------------------

def serialize_issue_comment(comment: GitHubIssueComment) -> dict[str, Any]:
    """issue-comment schema shape."""
    return {
        "id": comment.id,
        "node_id": comment.node_id,
        "url": comment.url,
        "html_url": comment.html_url,
        "issue_url": comment.issue_url,
        "body": comment.body,
        "body_text": comment.body_text,
        "body_html": comment.body_html,
        "user": _serialize_user_by_id(comment.user_id),
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
        "author_association": comment.author_association or "NONE",
        "performed_via_github_app": comment.performed_via_github_app,
        "reactions": comment.reactions,
        "pin": comment.pin,
    }


def serialize_issue_comment_list(
    comments: list[GitHubIssueComment],
) -> list[dict[str, Any]]:
    """Array of issue-comment objects."""
    return [serialize_issue_comment(comment) for comment in comments]


# ---------------------------------------------------------------------------
# Issue events
# ---------------------------------------------------------------------------

def serialize_issue_event(event: GitHubIssueEvent) -> dict[str, Any]:
    """issue-event schema shape."""
    result: dict[str, Any] = {
        "id": event.id,
        "node_id": event.node_id,
        "url": event.url,
        "actor": _serialize_user_by_id(event.actor_id),
        "event": event.event,
        "commit_id": event.commit_id,
        "commit_url": event.commit_url,
        "created_at": event.created_at,
        "performed_via_github_app": event.performed_via_github_app,
    }
    if event.label is not None:
        result["label"] = event.label
    if event.assignee_id is not None:
        result["assignee"] = _serialize_user_by_id(event.assignee_id)
    if event.assigner_id is not None:
        result["assigner"] = _serialize_user_by_id(event.assigner_id)
    if event.milestone is not None:
        result["milestone"] = event.milestone
    if event.rename is not None:
        result["rename"] = event.rename
    if event.dismissed_review is not None:
        result["dismissed_review"] = event.dismissed_review
    if event.project_card is not None:
        result["project_card"] = event.project_card
    if event.lock_reason is not None:
        result["lock_reason"] = event.lock_reason
    if event.author_association is not None:
        result["author_association"] = event.author_association
    return result


def serialize_issue_event_list(
    events: list[GitHubIssueEvent],
) -> list[dict[str, Any]]:
    """Array of issue-event objects."""
    return [serialize_issue_event(event) for event in events]


# ---------------------------------------------------------------------------
# Reactions
# ---------------------------------------------------------------------------

def serialize_reaction(reaction: GitHubIssueReaction) -> dict[str, Any]:
    """reaction schema shape."""
    return {
        "id": reaction.id,
        "node_id": reaction.node_id,
        "user": _serialize_user_by_id(reaction.user_id),
        "content": reaction.content,
        "created_at": reaction.created_at,
    }


def serialize_reaction_list(
    reactions: list[GitHubIssueReaction],
) -> list[dict[str, Any]]:
    """Array of reaction objects."""
    return [serialize_reaction(reaction) for reaction in reactions]


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

def serialize_label(label: dict[str, Any]) -> dict[str, Any]:
    """label schema shape from a JSONB label dict."""
    return {
        "id": label.get("id"),
        "node_id": label.get("node_id", ""),
        "url": label.get("url", ""),
        "name": label.get("name", ""),
        "description": label.get("description"),
        "color": label.get("color", "ededed"),
        "default": label.get("default", False),
    }


def serialize_label_list(labels: list) -> list[dict[str, Any]]:
    """Array of label objects."""
    result = []
    for label in labels:
        if isinstance(label, dict):
            result.append(serialize_label(label))
        else:
            result.append({"id": None, "node_id": "", "url": "", "name": str(label), "description": None, "color": "ededed", "default": False})
    return result
