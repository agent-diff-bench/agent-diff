"""CRUD helpers for the GitHub replica.

Each function takes a SQLAlchemy session and returns ORM objects. Route
handlers are responsible for formatting responses.
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Iterable, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from .schema import (
    Issue,
    IssueAssignee,
    IssueComment,
    IssueLabel,
    Label,
    PullRequestReviewer,
    Repository,
    User,
)


_ID_RANGE = (10_000_000, 99_999_999)


def _new_id() -> str:
    return str(random.randint(*_ID_RANGE))


def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    return session.query(User).filter(User.id == user_id).one_or_none()


def get_user_by_login(session: Session, login: str) -> Optional[User]:
    return session.query(User).filter(User.login == login).one_or_none()


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.query(User).filter(User.email == email).one_or_none()


def get_repo(session: Session, owner: str, repo: str) -> Optional[Repository]:
    full_name = f"{owner}/{repo}"
    return (
        session.query(Repository).filter(Repository.full_name == full_name).one_or_none()
    )


def list_labels(session: Session, repo: Repository) -> List[Label]:
    return (
        session.query(Label)
        .filter(Label.repository_id == repo.id)
        .order_by(Label.name)
        .all()
    )


def get_label(session: Session, repo: Repository, name: str) -> Optional[Label]:
    return (
        session.query(Label)
        .filter(Label.repository_id == repo.id, Label.name == name)
        .one_or_none()
    )


def create_label(
    session: Session,
    repo: Repository,
    *,
    name: str,
    color: str = "ededed",
    description: Optional[str] = None,
) -> Label:
    label = Label(
        id=_new_id(),
        repository_id=repo.id,
        name=name,
        color=color,
        description=description,
    )
    session.add(label)
    session.flush()
    return label


def update_label(
    session: Session,
    label: Label,
    *,
    new_name: Optional[str] = None,
    color: Optional[str] = None,
    description: Optional[str] = None,
) -> Label:
    if new_name is not None:
        label.name = new_name
    if color is not None:
        label.color = color
    if description is not None:
        label.description = description
    session.flush()
    return label


def delete_label(session: Session, label: Label) -> None:
    session.query(IssueLabel).filter(IssueLabel.label_id == label.id).delete()
    session.delete(label)
    session.flush()


def _next_number(session: Session, repo: Repository) -> int:
    current = (
        session.query(func.max(Issue.number))
        .filter(Issue.repository_id == repo.id)
        .scalar()
    )
    return (current or 0) + 1


def list_issues(
    session: Session,
    repo: Repository,
    *,
    state: str = "open",
    include_pulls: bool = True,
) -> List[Issue]:
    q = session.query(Issue).filter(Issue.repository_id == repo.id)
    if state != "all":
        q = q.filter(Issue.state == state)
    if not include_pulls:
        q = q.filter(Issue.is_pull_request.is_(False))
    return q.order_by(Issue.number.desc()).all()


def get_issue(session: Session, repo: Repository, number: int) -> Optional[Issue]:
    return (
        session.query(Issue)
        .filter(Issue.repository_id == repo.id, Issue.number == number)
        .one_or_none()
    )


def create_issue(
    session: Session,
    repo: Repository,
    *,
    title: str,
    body: Optional[str],
    user: User,
    assignees: Iterable[User] = (),
    labels: Iterable[Label] = (),
    is_pull_request: bool = False,
    head_ref: Optional[str] = None,
    base_ref: Optional[str] = None,
    head_sha: Optional[str] = None,
    base_sha: Optional[str] = None,
    draft: bool = False,
) -> Issue:
    issue = Issue(
        id=_new_id(),
        repository_id=repo.id,
        number=_next_number(session, repo),
        title=title,
        body=body,
        state="open",
        user_id=user.id,
        is_pull_request=is_pull_request,
        draft=draft if is_pull_request else None,
        merged=False if is_pull_request else None,
        head_ref=head_ref,
        base_ref=base_ref,
        head_sha=head_sha,
        base_sha=base_sha,
    )
    session.add(issue)
    session.flush()
    for u in assignees:
        session.add(IssueAssignee(issue_id=issue.id, user_id=u.id))
    for lbl in labels:
        session.add(IssueLabel(issue_id=issue.id, label_id=lbl.id))
    session.flush()
    return issue


def update_issue(
    session: Session,
    issue: Issue,
    *,
    title: Optional[str] = None,
    body: Optional[str] = None,
    state: Optional[str] = None,
    state_reason: Optional[str] = None,
    locked: Optional[bool] = None,
) -> Issue:
    if title is not None:
        issue.title = title
    if body is not None:
        issue.body = body
    if locked is not None:
        issue.locked = locked
    if state is not None and state != issue.state:
        issue.state = state
        if state == "closed":
            issue.closed_at = datetime.utcnow()
            if state_reason:
                issue.state_reason = state_reason
            elif issue.state_reason is None:
                issue.state_reason = "completed"
        else:
            issue.closed_at = None
            issue.state_reason = None
    elif state_reason is not None and issue.state == "closed":
        issue.state_reason = state_reason
    session.flush()
    return issue


def set_issue_assignees(
    session: Session, issue: Issue, users: Iterable[User]
) -> List[User]:
    existing = {ia.user_id for ia in issue.assignees}
    added: List[User] = []
    for u in users:
        if u.id in existing:
            continue
        session.add(IssueAssignee(issue_id=issue.id, user_id=u.id))
        added.append(u)
        existing.add(u.id)
    session.flush()
    session.refresh(issue)
    return added


def remove_issue_assignees(
    session: Session, issue: Issue, users: Iterable[User]
) -> List[User]:
    ids = {u.id for u in users}
    to_remove = [ia for ia in issue.assignees if ia.user_id in ids]
    removed_users = [ia.user for ia in to_remove if ia.user]
    for ia in to_remove:
        session.delete(ia)
    session.flush()
    session.refresh(issue)
    return removed_users


def set_issue_labels(
    session: Session, issue: Issue, labels: Iterable[Label]
) -> List[Label]:
    session.query(IssueLabel).filter(IssueLabel.issue_id == issue.id).delete()
    label_list = list(labels)
    for lbl in label_list:
        session.add(IssueLabel(issue_id=issue.id, label_id=lbl.id))
    session.flush()
    session.refresh(issue)
    return label_list


def add_issue_labels(
    session: Session, issue: Issue, labels: Iterable[Label]
) -> List[Label]:
    existing = {il.label_id for il in issue.labels}
    for lbl in labels:
        if lbl.id in existing:
            continue
        session.add(IssueLabel(issue_id=issue.id, label_id=lbl.id))
        existing.add(lbl.id)
    session.flush()
    session.refresh(issue)
    return [il.label for il in issue.labels if il.label]


def remove_issue_label(session: Session, issue: Issue, label: Label) -> None:
    session.query(IssueLabel).filter(
        IssueLabel.issue_id == issue.id, IssueLabel.label_id == label.id
    ).delete()
    session.flush()
    session.refresh(issue)


def clear_issue_labels(session: Session, issue: Issue) -> None:
    session.query(IssueLabel).filter(IssueLabel.issue_id == issue.id).delete()
    session.flush()
    session.refresh(issue)


def list_issue_comments(session: Session, issue: Issue) -> List[IssueComment]:
    return (
        session.query(IssueComment)
        .filter(IssueComment.issue_id == issue.id)
        .order_by(IssueComment.created_at)
        .all()
    )


def get_comment(session: Session, comment_id: str) -> Optional[IssueComment]:
    return (
        session.query(IssueComment).filter(IssueComment.id == comment_id).one_or_none()
    )


def create_comment(
    session: Session, issue: Issue, *, user: User, body: str
) -> IssueComment:
    comment = IssueComment(
        id=_new_id(),
        issue_id=issue.id,
        user_id=user.id,
        body=body,
    )
    session.add(comment)
    issue.comments_count = (issue.comments_count or 0) + 1
    session.flush()
    return comment


def update_comment(
    session: Session, comment: IssueComment, *, body: str
) -> IssueComment:
    comment.body = body
    session.flush()
    return comment


def delete_comment(session: Session, comment: IssueComment) -> None:
    if comment.issue and comment.issue.comments_count:
        comment.issue.comments_count = max(comment.issue.comments_count - 1, 0)
    session.delete(comment)
    session.flush()


def set_requested_reviewers(
    session: Session, pr: Issue, users: Iterable[User]
) -> List[User]:
    existing = {prr.user_id for prr in pr.requested_reviewers}
    added: List[User] = []
    for u in users:
        if u.id in existing:
            continue
        session.add(PullRequestReviewer(issue_id=pr.id, user_id=u.id))
        added.append(u)
        existing.add(u.id)
    session.flush()
    session.refresh(pr)
    return added


def remove_requested_reviewers(
    session: Session, pr: Issue, users: Iterable[User]
) -> None:
    ids = {u.id for u in users}
    session.query(PullRequestReviewer).filter(
        PullRequestReviewer.issue_id == pr.id,
        PullRequestReviewer.user_id.in_(ids),
    ).delete(synchronize_session=False)
    session.flush()
    session.refresh(pr)


def merge_pull(
    session: Session,
    pr: Issue,
    *,
    merger: User,
    commit_sha: Optional[str] = None,
) -> Issue:
    pr.merged = True
    pr.state = "closed"
    pr.state_reason = "completed"
    pr.merged_at = datetime.utcnow()
    pr.closed_at = pr.merged_at
    pr.merged_by_id = merger.id
    pr.merge_commit_sha = commit_sha or _new_id() * 2
    session.flush()
    return pr
