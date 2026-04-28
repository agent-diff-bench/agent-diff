"""Session-first CRUD operations for GitHub.

Functions are added to this file one at a time during the resource
implementation loop. Every function takes a SQLAlchemy Session as the first
argument. No function accesses request state directly.

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its operation functions to this file incrementally.
"""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session, contains_eager, joinedload

from ..core.utils import generate_id, now_iso
from .schema import (
    GitHubGist, GitHubGistComment, GitHubGistStar, GitHubUser,
    GitHubIssue, GitHubIssueComment, GitHubIssueEvent, GitHubIssueReaction,
)


# ---------------------------------------------------------------------------
# Stub helpers — ensure FK targets exist before flushing
# ---------------------------------------------------------------------------

def _ensure_user_stub(session: Session, user_id: int | str) -> GitHubUser:
    """Create a minimal GitHubUser stub if one doesn't already exist."""
    numeric_id = int(user_id)
    existing = session.get(GitHubUser, numeric_id)
    if existing is not None:
        return existing
    stub = GitHubUser(
        id=numeric_id,
        login=str(user_id),
        is_deleted=False,
    )
    session.add(stub)
    session.flush()
    return stub


def _serialize_user_stub(user: GitHubUser) -> dict[str, Any]:
    """Build a simple-user shaped dict from a GitHubUser row."""
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


# ---------------------------------------------------------------------------
# Gists
# ---------------------------------------------------------------------------

def _build_gist_urls(gist_id: str) -> dict[str, str]:
    """Build the standard URL set for a gist."""
    base = f"https://api.github.com/gists/{gist_id}"
    return {
        "url": base,
        "forks_url": f"{base}/forks",
        "commits_url": f"{base}/commits",
        "comments_url": f"{base}/comments",
        "git_pull_url": f"https://gist.github.com/{gist_id}.git",
        "git_push_url": f"https://gist.github.com/{gist_id}.git",
        "html_url": f"https://gist.github.com/{gist_id}",
    }


def _normalize_files(raw_files: dict) -> dict:
    """Normalize incoming file objects — ensure each entry has required metadata."""
    normalized = {}
    for filename, file_data in raw_files.items():
        if file_data is None:
            continue
        content = file_data.get("content", "")
        normalized[filename] = {
            "filename": file_data.get("filename", filename),
            "type": "text/plain",
            "language": file_data.get("language"),
            "raw_url": f"https://gist.githubusercontent.com/raw/{filename}",
            "size": len(content) if content else 0,
            "truncated": False,
            "content": content,
            "encoding": "utf-8",
        }
    return normalized


def create_gist(
    session: Session,
    data: dict,
    owner_id: str,
) -> GitHubGist:
    gist_id = generate_id("gist")
    timestamp = now_iso()
    urls = _build_gist_urls(gist_id)

    raw_files = data.get("files", {})
    files = _normalize_files(raw_files)

    # public can be bool or string "true"/"false"
    public_value = data.get("public", False)
    if isinstance(public_value, str):
        public_value = public_value.lower() == "true"

    # Ensure user stub exists before setting FK
    user_stub = _ensure_user_stub(session, owner_id)

    gist = GitHubGist(
        id=gist_id,
        node_id=f"G_{gist_id}",
        description=data.get("description"),
        files=files,
        public=bool(public_value),
        comments=0,
        comments_enabled=True,
        truncated=False,
        owner_id=user_stub.id,
        user_id=user_stub.id,
        created_at=timestamp,
        updated_at=timestamp,
        is_deleted=False,
        **urls,
    )
    session.add(gist)
    session.flush()
    return gist


def get_gist(session: Session, gist_id: str) -> Optional[GitHubGist]:
    statement = (
        select(GitHubGist)
        .options(
            joinedload(GitHubGist.owner_rel),
            joinedload(GitHubGist.user_rel),
            joinedload(GitHubGist.fork_of_rel),
        )
        .where(
            GitHubGist.id == gist_id,
            GitHubGist.is_deleted == False,
        )
    )
    return session.execute(statement).scalar_one_or_none()


def update_gist(session: Session, gist_id: str, data: dict) -> Optional[GitHubGist]:
    gist = get_gist(session, gist_id)
    if gist is None:
        return None

    if "description" in data:
        gist.description = data["description"]

    if "files" in data:
        current_files = dict(gist.files) if gist.files else {}
        for filename, file_data in data["files"].items():
            if file_data is None:
                # Delete file
                current_files.pop(filename, None)
            elif "filename" in file_data and file_data["filename"] != filename:
                # Rename file
                old_entry = current_files.pop(filename, {})
                new_name = file_data["filename"]
                old_entry["filename"] = new_name
                if "content" in file_data:
                    old_entry["content"] = file_data["content"]
                    old_entry["size"] = len(file_data["content"])
                current_files[new_name] = old_entry
            else:
                # Update or add file
                existing = current_files.get(filename, {})
                content = file_data.get("content", existing.get("content", ""))
                current_files[filename] = {
                    "filename": filename,
                    "type": existing.get("type", "text/plain"),
                    "language": file_data.get("language", existing.get("language")),
                    "raw_url": existing.get("raw_url", f"https://gist.githubusercontent.com/raw/{filename}"),
                    "size": len(content) if content else 0,
                    "truncated": False,
                    "content": content,
                    "encoding": "utf-8",
                }
        gist.files = current_files

    gist.updated_at = now_iso()
    session.flush()
    return gist


def delete_gist(session: Session, gist_id: str) -> bool:
    gist = get_gist(session, gist_id)
    if gist is None:
        return False
    gist.is_deleted = True
    session.flush()
    return True


def list_gists(
    session: Session,
    *,
    owner_id: Optional[str] = None,
    public_only: bool = False,
    since: Optional[str] = None,
    per_page: int = 30,
    page: int = 1,
) -> list[GitHubGist]:
    statement = select(GitHubGist).where(GitHubGist.is_deleted == False)
    if owner_id is not None:
        # owner_id from the caller is a string login; join to user stub for lookup
        statement = (
            statement
            .join(GitHubGist.owner_rel)
            .options(contains_eager(GitHubGist.owner_rel))
            .where(GitHubUser.login == str(owner_id))
        )
    else:
        statement = statement.options(joinedload(GitHubGist.owner_rel))
    if public_only:
        statement = statement.where(GitHubGist.public == True)
    if since is not None:
        statement = statement.where(GitHubGist.updated_at >= since)
    statement = statement.order_by(GitHubGist.updated_at.desc())
    statement = statement.offset((page - 1) * per_page).limit(per_page)
    return list(session.execute(statement).scalars().unique().all())


def list_starred_gists(
    session: Session,
    user_id: str,
    *,
    since: Optional[str] = None,
    per_page: int = 30,
    page: int = 1,
) -> list[GitHubGist]:
    starred_ids = select(GitHubGistStar.gist_id).where(
        GitHubGistStar.user_id == user_id,
    )
    statement = (
        select(GitHubGist)
        .options(joinedload(GitHubGist.owner_rel))
        .where(
            GitHubGist.id.in_(starred_ids),
            GitHubGist.is_deleted == False,
        )
        .order_by(GitHubGist.updated_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    if since is not None:
        statement = statement.where(GitHubGist.updated_at >= since)
    return list(session.execute(statement).scalars().unique().all())


def fork_gist(session: Session, gist_id: str, owner_id: str) -> Optional[GitHubGist]:
    original = get_gist(session, gist_id)
    if original is None:
        return None

    new_id = generate_id("gist")
    timestamp = now_iso()
    urls = _build_gist_urls(new_id)

    # Ensure user stub exists before setting FK
    user_stub = _ensure_user_stub(session, owner_id)

    forked = GitHubGist(
        id=new_id,
        node_id=f"G_{new_id}",
        description=original.description,
        files=dict(original.files) if original.files else {},
        public=original.public,
        comments=0,
        comments_enabled=True,
        truncated=False,
        owner_id=user_stub.id,
        user_id=user_stub.id,
        fork_of_id=original.id,
        created_at=timestamp,
        updated_at=timestamp,
        is_deleted=False,
        **urls,
    )
    session.add(forked)
    session.flush()
    return forked


# ---------------------------------------------------------------------------
# Gist stars
# ---------------------------------------------------------------------------

def star_gist(session: Session, gist_id: str, user_id: str) -> bool:
    gist = get_gist(session, gist_id)
    if gist is None:
        return False
    existing = session.execute(
        select(GitHubGistStar).where(
            GitHubGistStar.gist_id == gist_id,
            GitHubGistStar.user_id == user_id,
        )
    ).scalar_one_or_none()
    if existing is None:
        session.add(GitHubGistStar(gist_id=gist_id, user_id=user_id))
        session.flush()
    return True


def unstar_gist(session: Session, gist_id: str, user_id: str) -> bool:
    gist = get_gist(session, gist_id)
    if gist is None:
        return False
    existing = session.execute(
        select(GitHubGistStar).where(
            GitHubGistStar.gist_id == gist_id,
            GitHubGistStar.user_id == user_id,
        )
    ).scalar_one_or_none()
    if existing is not None:
        session.delete(existing)
        session.flush()
    return True


def is_gist_starred(session: Session, gist_id: str, user_id: str) -> Optional[bool]:
    """Returns True if starred, False if not starred, None if gist not found."""
    gist = get_gist(session, gist_id)
    if gist is None:
        return None
    existing = session.execute(
        select(GitHubGistStar).where(
            GitHubGistStar.gist_id == gist_id,
            GitHubGistStar.user_id == user_id,
        )
    ).scalar_one_or_none()
    return existing is not None


# ---------------------------------------------------------------------------
# Gist comments
# ---------------------------------------------------------------------------

def create_gist_comment(
    session: Session,
    gist_id: str,
    body: str,
    user_id: str,
) -> Optional[GitHubGistComment]:
    gist = get_gist(session, gist_id)
    if gist is None:
        return None

    # Ensure user stub exists before setting FK
    user_stub = _ensure_user_stub(session, user_id)

    timestamp = now_iso()
    comment = GitHubGistComment(
        node_id=f"GC_{gist_id}",
        gist_id=gist_id,
        body=body,
        user_id=user_stub.id,
        author_association="NONE",
        created_at=timestamp,
        updated_at=timestamp,
        is_deleted=False,
    )
    session.add(comment)
    session.flush()

    # Set URL after we have the auto-generated ID
    comment.url = f"https://api.github.com/gists/{gist_id}/comments/{comment.id}"
    comment.node_id = f"GC_{comment.id}"

    # Increment comment count on the gist
    gist.comments = (gist.comments or 0) + 1
    session.flush()
    return comment


def get_gist_comment(
    session: Session,
    gist_id: str,
    comment_id: int,
) -> Optional[GitHubGistComment]:
    statement = (
        select(GitHubGistComment)
        .options(joinedload(GitHubGistComment.user_rel))
        .where(
            GitHubGistComment.id == comment_id,
            GitHubGistComment.gist_id == gist_id,
            GitHubGistComment.is_deleted == False,
        )
    )
    return session.execute(statement).scalar_one_or_none()


def update_gist_comment(
    session: Session,
    gist_id: str,
    comment_id: int,
    body: str,
) -> Optional[GitHubGistComment]:
    comment = get_gist_comment(session, gist_id, comment_id)
    if comment is None:
        return None
    comment.body = body
    comment.updated_at = now_iso()
    session.flush()
    return comment


def delete_gist_comment(
    session: Session,
    gist_id: str,
    comment_id: int,
) -> bool:
    comment = get_gist_comment(session, gist_id, comment_id)
    if comment is None:
        return False
    comment.is_deleted = True
    # Decrement comment count
    gist = get_gist(session, gist_id)
    if gist is not None:
        gist.comments = max((gist.comments or 0) - 1, 0)
    session.flush()
    return True


def list_gist_comments(
    session: Session,
    gist_id: str,
    *,
    per_page: int = 30,
    page: int = 1,
) -> list[GitHubGistComment]:
    statement = (
        select(GitHubGistComment)
        .options(joinedload(GitHubGistComment.user_rel))
        .where(
            GitHubGistComment.gist_id == gist_id,
            GitHubGistComment.is_deleted == False,
        )
        .order_by(GitHubGistComment.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    return list(session.execute(statement).scalars().unique().all())


# ---------------------------------------------------------------------------
# Gist commits (synthesized — we store version snapshots as JSONB on create/update)
# ---------------------------------------------------------------------------

def list_gist_commits(
    session: Session,
    gist_id: str,
    *,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list[dict]]:
    """Return synthetic commit history for the gist."""
    gist = get_gist(session, gist_id)
    if gist is None:
        return None
    history = gist.history or []
    start = (page - 1) * per_page
    return history[start:start + per_page]


def _add_gist_commit(gist: GitHubGist, user_id: str, session: Optional[Session] = None, change_status: Optional[dict] = None) -> None:
    """Append a commit entry to the gist's history."""
    import hashlib
    version = hashlib.sha1(f"{gist.id}-{gist.updated_at}".encode()).hexdigest()

    # Build user object for the commit if we can resolve it
    user_data: Any = user_id
    if session is not None:
        try:
            user_stub = _ensure_user_stub(session, user_id)
            user_data = _serialize_user_stub(user_stub)
        except (ValueError, TypeError):
            pass

    commit_entry = {
        "url": f"https://api.github.com/gists/{gist.id}/{version}",
        "version": version,
        "user": user_data,
        "change_status": change_status or {"total": 0, "additions": 0, "deletions": 0},
        "committed_at": gist.updated_at,
    }
    if gist.history is None:
        gist.history = []
    # Prepend so newest is first
    gist.history = [commit_entry] + list(gist.history)


# ---------------------------------------------------------------------------
# Gist forks
# ---------------------------------------------------------------------------

def list_gist_forks(
    session: Session,
    gist_id: str,
    *,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list[GitHubGist]]:
    """List forks of a gist. Returns None if the parent gist doesn't exist."""
    parent = get_gist(session, gist_id)
    if parent is None:
        return None
    statement = (
        select(GitHubGist)
        .options(joinedload(GitHubGist.owner_rel))
        .where(
            GitHubGist.is_deleted == False,
            GitHubGist.fork_of_id == gist_id,
        )
        .order_by(GitHubGist.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    return list(session.execute(statement).scalars().unique().all())


# ---------------------------------------------------------------------------
# Gist revisions
# ---------------------------------------------------------------------------

def get_gist_revision(
    session: Session,
    gist_id: str,
    sha: str,
) -> Optional[GitHubGist]:
    """Get a gist at a specific revision. We return the current gist if the sha matches any commit."""
    gist = get_gist(session, gist_id)
    if gist is None:
        return None
    # Check if the sha matches any commit in history
    history = gist.history or []
    for commit in history:
        if commit.get("version") == sha:
            return gist
    # If no history or no match, return None
    if not history:
        return gist
    return None


# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------

def _build_issue_urls(owner: str, repo: str, number: int) -> dict[str, str]:
    """Build the standard URL set for an issue."""
    base = f"https://api.github.com/repos/{owner}/{repo}"
    return {
        "url": f"{base}/issues/{number}",
        "repository_url": base,
        "labels_url": f"{base}/issues/{number}/labels{{/name}}",
        "comments_url": f"{base}/issues/{number}/comments",
        "events_url": f"{base}/issues/{number}/events",
        "html_url": f"https://github.com/{owner}/{repo}/issues/{number}",
        "timeline_url": f"{base}/issues/{number}/timeline",
    }


def _next_issue_number(session: Session, owner: str, repo: str) -> int:
    """Get the next issue number for a repo (max existing + 1)."""
    result = session.execute(
        select(func.max(GitHubIssue.number)).where(
            GitHubIssue.repo_owner == owner,
            GitHubIssue.repo_name == repo,
        )
    ).scalar()
    return (result or 0) + 1


def _default_reactions() -> dict:
    return {
        "url": "",
        "total_count": 0,
        "+1": 0,
        "-1": 0,
        "laugh": 0,
        "confused": 0,
        "heart": 0,
        "hooray": 0,
        "eyes": 0,
        "rocket": 0,
    }


def create_issue(
    session: Session,
    owner: str,
    repo: str,
    data: dict,
    user_id: str,
) -> GitHubIssue:
    issue_id = int(generate_id("issue"))
    number = _next_issue_number(session, owner, repo)
    timestamp = now_iso()
    urls = _build_issue_urls(owner, repo, number)

    _ensure_user_stub(session, user_id)

    title = data.get("title", "")
    if isinstance(title, dict):
        title = str(title)

    reactions = _default_reactions()
    reactions["url"] = f"https://api.github.com/repos/{owner}/{repo}/issues/{number}/reactions"

    issue = GitHubIssue(
        id=issue_id,
        node_id=f"I_{issue_id}",
        repo_owner=owner,
        repo_name=repo,
        number=number,
        title=title,
        body=data.get("body"),
        state="open",
        state_reason=None,
        locked=False,
        comments=0,
        user_id=int(user_id),
        labels=data.get("labels") or [],
        assignees=data.get("assignees") or [],
        milestone=data.get("milestone"),
        issue_type=data.get("type"),
        author_association="OWNER",
        reactions=reactions,
        draft=False,
        created_at=timestamp,
        updated_at=timestamp,
        is_deleted=False,
        **urls,
    )
    session.add(issue)
    session.flush()
    return issue


def get_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
) -> Optional[GitHubIssue]:
    statement = (
        select(GitHubIssue)
        .options(
            joinedload(GitHubIssue.user_rel),
            joinedload(GitHubIssue.closed_by_rel),
            joinedload(GitHubIssue.parent_rel),
        )
        .where(
            GitHubIssue.repo_owner == owner,
            GitHubIssue.repo_name == repo,
            GitHubIssue.number == issue_number,
            GitHubIssue.is_deleted == False,
        )
    )
    return session.execute(statement).unique().scalar_one_or_none()


def get_issue_by_id(session: Session, issue_id: int) -> Optional[GitHubIssue]:
    statement = (
        select(GitHubIssue)
        .options(
            joinedload(GitHubIssue.user_rel),
            joinedload(GitHubIssue.closed_by_rel),
            joinedload(GitHubIssue.parent_rel),
        )
        .where(
            GitHubIssue.id == issue_id,
            GitHubIssue.is_deleted == False,
        )
    )
    return session.execute(statement).unique().scalar_one_or_none()


def update_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    data: dict,
) -> Optional[GitHubIssue]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None

    if "title" in data and data["title"] is not None:
        title = data["title"]
        if isinstance(title, dict):
            title = str(title)
        issue.title = title
    if "body" in data:
        issue.body = data["body"]
    if "state" in data:
        issue.state = data["state"]
    if "state_reason" in data:
        issue.state_reason = data["state_reason"]
    if "milestone" in data:
        issue.milestone = data["milestone"]
    if "labels" in data:
        issue.labels = data["labels"]
    if "assignees" in data:
        issue.assignees = data["assignees"]
    if "type" in data:
        issue.issue_type = data["type"]
    if "issue_field_values" in data:
        issue.issue_field_values = data["issue_field_values"]

    if data.get("state") == "closed" and issue.closed_at is None:
        issue.closed_at = now_iso()
    elif data.get("state") == "open":
        issue.closed_at = None

    issue.updated_at = now_iso()
    session.flush()
    return issue


def list_issues(
    session: Session,
    *,
    owner: Optional[str] = None,
    repo: Optional[str] = None,
    state: str = "open",
    labels: Optional[str] = None,
    sort: str = "created",
    direction: str = "desc",
    since: Optional[str] = None,
    assignee: Optional[str] = None,
    creator: Optional[str] = None,
    milestone: Optional[str] = None,
    per_page: int = 30,
    page: int = 1,
) -> list[GitHubIssue]:
    statement = (
        select(GitHubIssue)
        .options(
            joinedload(GitHubIssue.user_rel),
            joinedload(GitHubIssue.closed_by_rel),
        )
        .where(GitHubIssue.is_deleted == False)
    )

    if owner is not None and repo is not None:
        statement = statement.where(
            GitHubIssue.repo_owner == owner,
            GitHubIssue.repo_name == repo,
        )

    if state != "all":
        statement = statement.where(GitHubIssue.state == state)

    if since is not None:
        statement = statement.where(GitHubIssue.updated_at >= since)

    # Sort
    sort_column = GitHubIssue.created_at
    if sort == "updated":
        sort_column = GitHubIssue.updated_at
    if direction == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    statement = statement.offset((page - 1) * per_page).limit(per_page)
    return list(session.execute(statement).scalars().unique().all())


def list_issues_for_user(
    session: Session,
    user_id: str,
    *,
    state: str = "open",
    sort: str = "created",
    direction: str = "desc",
    since: Optional[str] = None,
    labels: Optional[str] = None,
    per_page: int = 30,
    page: int = 1,
) -> list[GitHubIssue]:
    """List issues assigned to a user across all repos."""
    statement = (
        select(GitHubIssue)
        .options(
            joinedload(GitHubIssue.user_rel),
            joinedload(GitHubIssue.closed_by_rel),
        )
        .where(
            GitHubIssue.is_deleted == False,
            GitHubIssue.user_id == int(user_id),
        )
    )
    if state != "all":
        statement = statement.where(GitHubIssue.state == state)
    if since is not None:
        statement = statement.where(GitHubIssue.updated_at >= since)

    sort_column = GitHubIssue.created_at
    if sort == "updated":
        sort_column = GitHubIssue.updated_at
    if direction == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    statement = statement.offset((page - 1) * per_page).limit(per_page)
    return list(session.execute(statement).scalars().unique().all())


# ---------------------------------------------------------------------------
# Issue comments
# ---------------------------------------------------------------------------

def _build_issue_comment_urls(owner: str, repo: str, comment_id: int, issue_number: int) -> dict[str, str]:
    base = f"https://api.github.com/repos/{owner}/{repo}"
    return {
        "url": f"{base}/issues/comments/{comment_id}",
        "html_url": f"https://github.com/{owner}/{repo}/issues/{issue_number}#issuecomment-{comment_id}",
        "issue_url": f"{base}/issues/{issue_number}",
    }


def create_issue_comment(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    body: str,
    user_id: str,
) -> Optional[GitHubIssueComment]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None

    comment_id = int(generate_id("issue_comment"))
    timestamp = now_iso()
    _ensure_user_stub(session, user_id)
    urls = _build_issue_comment_urls(owner, repo, comment_id, issue_number)

    comment = GitHubIssueComment(
        id=comment_id,
        node_id=f"IC_{comment_id}",
        issue_id=issue.id,
        repo_owner=owner,
        repo_name=repo,
        body=body,
        user_id=int(user_id),
        author_association="NONE",
        reactions=_default_reactions(),
        created_at=timestamp,
        updated_at=timestamp,
        is_deleted=False,
        **urls,
    )
    session.add(comment)

    issue.comments = (issue.comments or 0) + 1
    issue.updated_at = timestamp
    session.flush()
    return comment


def get_issue_comment(
    session: Session,
    owner: str,
    repo: str,
    comment_id: int,
) -> Optional[GitHubIssueComment]:
    statement = (
        select(GitHubIssueComment)
        .where(
            GitHubIssueComment.id == comment_id,
            GitHubIssueComment.repo_owner == owner,
            GitHubIssueComment.repo_name == repo,
            GitHubIssueComment.is_deleted == False,
        )
    )
    return session.execute(statement).scalar_one_or_none()


def update_issue_comment(
    session: Session,
    owner: str,
    repo: str,
    comment_id: int,
    body: str,
) -> Optional[GitHubIssueComment]:
    comment = get_issue_comment(session, owner, repo, comment_id)
    if comment is None:
        return None
    comment.body = body
    comment.updated_at = now_iso()
    session.flush()
    return comment


def delete_issue_comment(
    session: Session,
    owner: str,
    repo: str,
    comment_id: int,
) -> bool:
    comment = get_issue_comment(session, owner, repo, comment_id)
    if comment is None:
        return False
    comment.is_deleted = True

    # Decrement comment count on parent issue
    issue = get_issue_by_id(session, comment.issue_id)
    if issue is not None:
        issue.comments = max((issue.comments or 0) - 1, 0)
    session.flush()
    return True


def list_issue_comments_for_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    *,
    since: Optional[str] = None,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list[GitHubIssueComment]]:
    """List comments for a specific issue. Returns None if issue not found."""
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None

    statement = (
        select(GitHubIssueComment)
        .where(
            GitHubIssueComment.issue_id == issue.id,
            GitHubIssueComment.is_deleted == False,
        )
    )
    if since is not None:
        statement = statement.where(GitHubIssueComment.updated_at >= since)
    statement = statement.order_by(GitHubIssueComment.id.asc())
    statement = statement.offset((page - 1) * per_page).limit(per_page)
    return list(session.execute(statement).scalars().all())


def list_issue_comments_for_repo(
    session: Session,
    owner: str,
    repo: str,
    *,
    sort: str = "created",
    direction: str = "desc",
    since: Optional[str] = None,
    per_page: int = 30,
    page: int = 1,
) -> list[GitHubIssueComment]:
    statement = (
        select(GitHubIssueComment)
        .where(
            GitHubIssueComment.repo_owner == owner,
            GitHubIssueComment.repo_name == repo,
            GitHubIssueComment.is_deleted == False,
        )
    )
    if since is not None:
        statement = statement.where(GitHubIssueComment.updated_at >= since)

    sort_column = GitHubIssueComment.created_at
    if sort == "updated":
        sort_column = GitHubIssueComment.updated_at
    if direction == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    statement = statement.offset((page - 1) * per_page).limit(per_page)
    return list(session.execute(statement).scalars().all())


def pin_issue_comment(
    session: Session,
    owner: str,
    repo: str,
    comment_id: int,
    user_id: str,
) -> Optional[GitHubIssueComment]:
    comment = get_issue_comment(session, owner, repo, comment_id)
    if comment is None:
        return None
    _ensure_user_stub(session, user_id)
    comment.pin = {
        "pinned_at": now_iso(),
        "pinned_by": _serialize_user_stub(session.get(GitHubUser, int(user_id))),
    }
    comment.updated_at = now_iso()
    session.flush()
    return comment


def unpin_issue_comment(
    session: Session,
    owner: str,
    repo: str,
    comment_id: int,
) -> bool:
    comment = get_issue_comment(session, owner, repo, comment_id)
    if comment is None:
        return False
    comment.pin = None
    comment.updated_at = now_iso()
    session.flush()
    return True


# ---------------------------------------------------------------------------
# Issue events
# ---------------------------------------------------------------------------

def create_issue_event(
    session: Session,
    owner: str,
    repo: str,
    issue_id: int,
    event: str,
    actor_id: str,
    **kwargs: Any,
) -> GitHubIssueEvent:
    event_id = int(generate_id("issue_event"))
    timestamp = now_iso()
    base_url = f"https://api.github.com/repos/{owner}/{repo}"

    issue_event = GitHubIssueEvent(
        id=event_id,
        node_id=f"IE_{event_id}",
        issue_id=issue_id,
        repo_owner=owner,
        repo_name=repo,
        url=f"{base_url}/issues/events/{event_id}",
        event=event,
        actor_id=int(actor_id),
        commit_id=kwargs.get("commit_id"),
        commit_url=kwargs.get("commit_url"),
        created_at=timestamp,
        is_deleted=False,
        **{key: value for key, value in kwargs.items() if key not in ("commit_id", "commit_url")},
    )
    session.add(issue_event)
    session.flush()
    return issue_event


def get_issue_event(
    session: Session,
    owner: str,
    repo: str,
    event_id: int,
) -> Optional[GitHubIssueEvent]:
    statement = (
        select(GitHubIssueEvent)
        .where(
            GitHubIssueEvent.id == event_id,
            GitHubIssueEvent.repo_owner == owner,
            GitHubIssueEvent.repo_name == repo,
            GitHubIssueEvent.is_deleted == False,
        )
    )
    return session.execute(statement).scalar_one_or_none()


def list_issue_events_for_repo(
    session: Session,
    owner: str,
    repo: str,
    *,
    per_page: int = 30,
    page: int = 1,
) -> list[GitHubIssueEvent]:
    statement = (
        select(GitHubIssueEvent)
        .where(
            GitHubIssueEvent.repo_owner == owner,
            GitHubIssueEvent.repo_name == repo,
            GitHubIssueEvent.is_deleted == False,
        )
        .order_by(GitHubIssueEvent.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    return list(session.execute(statement).scalars().all())


def list_issue_events_for_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    *,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list[GitHubIssueEvent]]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None

    statement = (
        select(GitHubIssueEvent)
        .where(
            GitHubIssueEvent.issue_id == issue.id,
            GitHubIssueEvent.is_deleted == False,
        )
        .order_by(GitHubIssueEvent.created_at.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    return list(session.execute(statement).scalars().all())


# ---------------------------------------------------------------------------
# Issue reactions
# ---------------------------------------------------------------------------

VALID_REACTIONS = {"+1", "-1", "laugh", "confused", "heart", "hooray", "rocket", "eyes"}


def create_issue_reaction(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    content: str,
    user_id: str,
) -> tuple[Optional[GitHubIssueReaction], bool]:
    """Create a reaction on an issue. Returns (reaction, created) — created=False if it already existed."""
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None, False

    # Check for existing reaction by same user with same content
    existing = session.execute(
        select(GitHubIssueReaction).where(
            GitHubIssueReaction.issue_id == issue.id,
            GitHubIssueReaction.comment_id == None,
            GitHubIssueReaction.user_id == int(user_id),
            GitHubIssueReaction.content == content,
        )
    ).scalar_one_or_none()
    if existing is not None:
        return existing, False

    _ensure_user_stub(session, user_id)
    reaction_id = int(generate_id("issue_reaction"))
    reaction = GitHubIssueReaction(
        id=reaction_id,
        node_id=f"REA_{reaction_id}",
        issue_id=issue.id,
        user_id=int(user_id),
        content=content,
        repo_owner=owner,
        repo_name=repo,
        created_at=now_iso(),
    )
    session.add(reaction)

    # Update rollup on issue
    reactions = dict(issue.reactions) if issue.reactions else _default_reactions()
    reactions[content] = reactions.get(content, 0) + 1
    reactions["total_count"] = reactions.get("total_count", 0) + 1
    issue.reactions = reactions
    session.flush()
    return reaction, True


def delete_issue_reaction(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    reaction_id: int,
) -> bool:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return False

    reaction = session.execute(
        select(GitHubIssueReaction).where(
            GitHubIssueReaction.id == reaction_id,
            GitHubIssueReaction.issue_id == issue.id,
        )
    ).scalar_one_or_none()
    if reaction is None:
        return False

    # Update rollup
    reactions = dict(issue.reactions) if issue.reactions else _default_reactions()
    reactions[reaction.content] = max(reactions.get(reaction.content, 0) - 1, 0)
    reactions["total_count"] = max(reactions.get("total_count", 0) - 1, 0)
    issue.reactions = reactions

    session.delete(reaction)
    session.flush()
    return True


def list_issue_reactions(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    *,
    content: Optional[str] = None,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list[GitHubIssueReaction]]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None

    statement = (
        select(GitHubIssueReaction)
        .where(
            GitHubIssueReaction.issue_id == issue.id,
            GitHubIssueReaction.comment_id == None,
        )
    )
    if content is not None:
        statement = statement.where(GitHubIssueReaction.content == content)
    statement = statement.order_by(GitHubIssueReaction.id.asc())
    statement = statement.offset((page - 1) * per_page).limit(per_page)
    return list(session.execute(statement).scalars().all())


# ---------------------------------------------------------------------------
# Issue comment reactions
# ---------------------------------------------------------------------------

def create_issue_comment_reaction(
    session: Session,
    owner: str,
    repo: str,
    comment_id: int,
    content: str,
    user_id: str,
) -> tuple[Optional[GitHubIssueReaction], bool]:
    comment = get_issue_comment(session, owner, repo, comment_id)
    if comment is None:
        return None, False

    existing = session.execute(
        select(GitHubIssueReaction).where(
            GitHubIssueReaction.comment_id == comment_id,
            GitHubIssueReaction.user_id == int(user_id),
            GitHubIssueReaction.content == content,
        )
    ).scalar_one_or_none()
    if existing is not None:
        return existing, False

    _ensure_user_stub(session, user_id)
    reaction_id = int(generate_id("issue_reaction"))
    reaction = GitHubIssueReaction(
        id=reaction_id,
        node_id=f"REA_{reaction_id}",
        comment_id=comment_id,
        user_id=int(user_id),
        content=content,
        repo_owner=owner,
        repo_name=repo,
        created_at=now_iso(),
    )
    session.add(reaction)

    # Update rollup on comment
    reactions = dict(comment.reactions) if comment.reactions else _default_reactions()
    reactions[content] = reactions.get(content, 0) + 1
    reactions["total_count"] = reactions.get("total_count", 0) + 1
    comment.reactions = reactions
    session.flush()
    return reaction, True


def delete_issue_comment_reaction(
    session: Session,
    owner: str,
    repo: str,
    comment_id: int,
    reaction_id: int,
) -> bool:
    comment = get_issue_comment(session, owner, repo, comment_id)
    if comment is None:
        return False

    reaction = session.execute(
        select(GitHubIssueReaction).where(
            GitHubIssueReaction.id == reaction_id,
            GitHubIssueReaction.comment_id == comment_id,
        )
    ).scalar_one_or_none()
    if reaction is None:
        return False

    reactions = dict(comment.reactions) if comment.reactions else _default_reactions()
    reactions[reaction.content] = max(reactions.get(reaction.content, 0) - 1, 0)
    reactions["total_count"] = max(reactions.get("total_count", 0) - 1, 0)
    comment.reactions = reactions

    session.delete(reaction)
    session.flush()
    return True


def list_issue_comment_reactions(
    session: Session,
    owner: str,
    repo: str,
    comment_id: int,
    *,
    content: Optional[str] = None,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list[GitHubIssueReaction]]:
    comment = get_issue_comment(session, owner, repo, comment_id)
    if comment is None:
        return None

    statement = (
        select(GitHubIssueReaction)
        .where(GitHubIssueReaction.comment_id == comment_id)
    )
    if content is not None:
        statement = statement.where(GitHubIssueReaction.content == content)
    statement = statement.order_by(GitHubIssueReaction.id.asc())
    statement = statement.offset((page - 1) * per_page).limit(per_page)
    return list(session.execute(statement).scalars().all())


# ---------------------------------------------------------------------------
# Issue locking
# ---------------------------------------------------------------------------

def lock_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    lock_reason: Optional[str] = None,
) -> Optional[GitHubIssue]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    issue.locked = True
    issue.active_lock_reason = lock_reason
    issue.updated_at = now_iso()
    session.flush()
    return issue


def unlock_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
) -> Optional[GitHubIssue]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    issue.locked = False
    issue.active_lock_reason = None
    issue.updated_at = now_iso()
    session.flush()
    return issue


# ---------------------------------------------------------------------------
# Issue labels (managed on the JSONB labels column)
# ---------------------------------------------------------------------------

def add_labels_to_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    label_data: Any,
) -> Optional[list]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None

    current_labels = list(issue.labels) if issue.labels else []

    # label_data can be {"labels": [...]} or a list of strings/objects
    new_labels = label_data
    if isinstance(label_data, dict):
        new_labels = label_data.get("labels", [])

    for label in (new_labels or []):
        if isinstance(label, str):
            if not any((l.get("name") if isinstance(l, dict) else l) == label for l in current_labels):
                current_labels.append({"id": int(generate_id("issue")), "node_id": "LA_stub", "url": "", "name": label, "description": None, "color": "ededed", "default": False})
        elif isinstance(label, dict):
            name = label.get("name", "")
            if not any((l.get("name") if isinstance(l, dict) else l) == name for l in current_labels):
                current_labels.append(label)

    issue.labels = current_labels
    issue.updated_at = now_iso()
    session.flush()
    return current_labels


def set_labels_on_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    label_data: Any,
) -> Optional[list]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None

    new_labels = label_data
    if isinstance(label_data, dict):
        new_labels = label_data.get("labels", [])

    resolved = []
    for label in (new_labels or []):
        if isinstance(label, str):
            resolved.append({"id": int(generate_id("issue")), "node_id": "LA_stub", "url": "", "name": label, "description": None, "color": "ededed", "default": False})
        elif isinstance(label, dict):
            resolved.append(label)

    issue.labels = resolved
    issue.updated_at = now_iso()
    session.flush()
    return resolved


def remove_label_from_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    label_name: str,
) -> Optional[list]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None

    current_labels = list(issue.labels) if issue.labels else []
    updated = [l for l in current_labels if (l.get("name") if isinstance(l, dict) else l) != label_name]

    if len(updated) == len(current_labels):
        # Label was not found
        return None

    issue.labels = updated
    issue.updated_at = now_iso()
    session.flush()
    return updated


def remove_all_labels_from_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
) -> Optional[bool]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    issue.labels = []
    issue.updated_at = now_iso()
    session.flush()
    return True


def list_labels_for_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    *,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    labels = issue.labels or []
    start = (page - 1) * per_page
    return labels[start:start + per_page]


# ---------------------------------------------------------------------------
# Issue dependencies (stored as JSONB — lightweight tracking)
# ---------------------------------------------------------------------------

def add_issue_dependency(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    blocked_by_issue_id: int,
) -> Optional[GitHubIssue]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    deps = dict(issue.issue_dependencies_summary) if issue.issue_dependencies_summary else {"blocked_by": [], "blocking": []}
    blocked_by = deps.get("blocked_by", [])
    if blocked_by_issue_id not in blocked_by:
        blocked_by.append(blocked_by_issue_id)
    deps["blocked_by"] = blocked_by
    issue.issue_dependencies_summary = deps
    issue.updated_at = now_iso()
    session.flush()
    return issue


def remove_issue_dependency(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    blocked_by_issue_id: int,
) -> Optional[GitHubIssue]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    deps = dict(issue.issue_dependencies_summary) if issue.issue_dependencies_summary else {"blocked_by": [], "blocking": []}
    blocked_by = deps.get("blocked_by", [])
    if blocked_by_issue_id in blocked_by:
        blocked_by.remove(blocked_by_issue_id)
    deps["blocked_by"] = blocked_by
    issue.issue_dependencies_summary = deps
    issue.updated_at = now_iso()
    session.flush()
    return issue


def list_issue_dependencies_blocked_by(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    *,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list[GitHubIssue]]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    deps = issue.issue_dependencies_summary or {}
    blocked_by_ids = deps.get("blocked_by", [])
    if not blocked_by_ids:
        return []
    statement = (
        select(GitHubIssue)
        .options(
            joinedload(GitHubIssue.user_rel),
            joinedload(GitHubIssue.closed_by_rel),
        )
        .where(
            GitHubIssue.id.in_(blocked_by_ids),
            GitHubIssue.is_deleted == False,
        )
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    return list(session.execute(statement).scalars().unique().all())


def list_issue_dependencies_blocking(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    *,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list[GitHubIssue]]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    # Find issues that list this issue in their blocked_by
    # For simplicity, scan all issues in the same repo
    all_issues = session.execute(
        select(GitHubIssue).where(
            GitHubIssue.is_deleted == False,
        )
    ).scalars().all()
    blocking = []
    for other in all_issues:
        deps = other.issue_dependencies_summary or {}
        if issue.id in deps.get("blocked_by", []):
            blocking.append(other)
    start = (page - 1) * per_page
    return blocking[start:start + per_page]


# ---------------------------------------------------------------------------
# Sub-issues (tracked on JSONB sub_issues_summary)
# ---------------------------------------------------------------------------

def add_sub_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    sub_issue_id: int,
    replace_parent: bool = False,
) -> Optional[GitHubIssue]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    summary = dict(issue.sub_issues_summary) if issue.sub_issues_summary else {"sub_issues": []}
    sub_issues = summary.get("sub_issues", [])
    if sub_issue_id not in sub_issues:
        sub_issues.append(sub_issue_id)
    summary["sub_issues"] = sub_issues
    issue.sub_issues_summary = summary
    issue.updated_at = now_iso()
    session.flush()
    return issue


def remove_sub_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    sub_issue_id: int,
) -> Optional[GitHubIssue]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    summary = dict(issue.sub_issues_summary) if issue.sub_issues_summary else {"sub_issues": []}
    sub_issues = summary.get("sub_issues", [])
    if sub_issue_id in sub_issues:
        sub_issues.remove(sub_issue_id)
    summary["sub_issues"] = sub_issues
    issue.sub_issues_summary = summary
    issue.updated_at = now_iso()
    session.flush()
    return issue


def list_sub_issues(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    *,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list[GitHubIssue]]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    summary = issue.sub_issues_summary or {}
    sub_issue_ids = summary.get("sub_issues", [])
    if not sub_issue_ids:
        return []
    statement = (
        select(GitHubIssue)
        .options(
            joinedload(GitHubIssue.user_rel),
            joinedload(GitHubIssue.closed_by_rel),
        )
        .where(
            GitHubIssue.id.in_(sub_issue_ids),
            GitHubIssue.is_deleted == False,
        )
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    return list(session.execute(statement).scalars().unique().all())


def reprioritize_sub_issue(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    sub_issue_id: int,
    after_id: Optional[int] = None,
    before_id: Optional[int] = None,
) -> Optional[GitHubIssue]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    summary = dict(issue.sub_issues_summary) if issue.sub_issues_summary else {"sub_issues": []}
    sub_issues = list(summary.get("sub_issues", []))
    if sub_issue_id not in sub_issues:
        return None
    sub_issues.remove(sub_issue_id)
    if after_id is not None and after_id in sub_issues:
        index = sub_issues.index(after_id) + 1
        sub_issues.insert(index, sub_issue_id)
    elif before_id is not None and before_id in sub_issues:
        index = sub_issues.index(before_id)
        sub_issues.insert(index, sub_issue_id)
    else:
        sub_issues.append(sub_issue_id)
    summary["sub_issues"] = sub_issues
    issue.sub_issues_summary = summary
    issue.updated_at = now_iso()
    session.flush()
    return issue


# ---------------------------------------------------------------------------
# Issue field values
# ---------------------------------------------------------------------------

def set_issue_field_values(
    session: Session,
    repository_id: int,
    issue_number: int,
    field_values: list,
) -> Optional[list]:
    """Set (replace) field values for an issue found by repository_id and number."""
    statement = (
        select(GitHubIssue)
        .where(
            GitHubIssue.number == issue_number,
            GitHubIssue.is_deleted == False,
        )
    )
    issue = session.execute(statement).scalar_one_or_none()
    if issue is None:
        return None
    issue.issue_field_values = field_values
    issue.updated_at = now_iso()
    session.flush()
    return field_values


def add_issue_field_values(
    session: Session,
    repository_id: int,
    issue_number: int,
    field_values: list,
) -> Optional[list]:
    statement = (
        select(GitHubIssue)
        .where(
            GitHubIssue.number == issue_number,
            GitHubIssue.is_deleted == False,
        )
    )
    issue = session.execute(statement).scalar_one_or_none()
    if issue is None:
        return None
    current = list(issue.issue_field_values) if issue.issue_field_values else []
    current.extend(field_values)
    issue.issue_field_values = current
    issue.updated_at = now_iso()
    session.flush()
    return current


def delete_issue_field_value(
    session: Session,
    repository_id: int,
    issue_number: int,
    issue_field_id: int,
) -> bool:
    statement = (
        select(GitHubIssue)
        .where(
            GitHubIssue.number == issue_number,
            GitHubIssue.is_deleted == False,
        )
    )
    issue = session.execute(statement).scalar_one_or_none()
    if issue is None:
        return False
    current = list(issue.issue_field_values) if issue.issue_field_values else []
    updated = [fv for fv in current if fv.get("issue_field_id") != issue_field_id]
    issue.issue_field_values = updated
    issue.updated_at = now_iso()
    session.flush()
    return True


def list_issue_field_values(
    session: Session,
    owner: str,
    repo: str,
    issue_number: int,
    *,
    per_page: int = 30,
    page: int = 1,
) -> Optional[list]:
    issue = get_issue(session, owner, repo, issue_number)
    if issue is None:
        return None
    field_values = issue.issue_field_values or []
    start = (page - 1) * per_page
    return field_values[start:start + per_page]


# ---------------------------------------------------------------------------
# Search issues
# ---------------------------------------------------------------------------

def search_issues(
    session: Session,
    query: str,
    *,
    sort: Optional[str] = None,
    order: str = "desc",
    per_page: int = 30,
    page: int = 1,
) -> tuple[list[GitHubIssue], int]:
    """Simple keyword search across issue titles and bodies. Returns (items, total_count)."""
    statement = (
        select(GitHubIssue)
        .options(
            joinedload(GitHubIssue.user_rel),
            joinedload(GitHubIssue.closed_by_rel),
        )
        .where(GitHubIssue.is_deleted == False)
    )

    # Simple keyword matching
    if query:
        pattern = f"%{query}%"
        statement = statement.where(
            (GitHubIssue.title.ilike(pattern)) | (GitHubIssue.body.ilike(pattern))
        )

    # Count total
    count_statement = select(func.count()).select_from(statement.subquery())
    total_count = session.execute(count_statement).scalar() or 0

    # Sort
    if sort == "updated":
        sort_column = GitHubIssue.updated_at
    elif sort == "comments":
        sort_column = GitHubIssue.comments
    elif sort == "created":
        sort_column = GitHubIssue.created_at
    else:
        sort_column = GitHubIssue.created_at

    if order == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    statement = statement.offset((page - 1) * per_page).limit(per_page)
    items = list(session.execute(statement).scalars().unique().all())
    return items, total_count
