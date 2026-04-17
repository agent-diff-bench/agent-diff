"""Session-first CRUD operations for Todoist resources.

Every function takes a SQLAlchemy Session as the first argument. No function
accesses request state directly — that translation happens in the route layer.
"""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .schema import Label, Project, Task
from ..core.utils import generate_id, now_iso


# ============================================================================
# PROJECT QUERIES
# ============================================================================


def get_project(session: Session, project_id: str) -> Project | None:
    """Get a single project by ID. Returns None if not found or deleted."""
    return session.execute(
        select(Project).where(Project.id == project_id, Project.is_deleted.is_(False))
    ).scalar_one_or_none()


def list_projects(
    session: Session,
    *,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Project], str | None]:
    """List active (non-archived, non-deleted) projects with cursor pagination.

    Returns (projects, next_cursor). next_cursor is None when there are no more
    results.

    Cursor is the last project ID from the previous page — we order by
    default_order then id for stable pagination.
    """
    query = (
        select(Project)
        .where(Project.is_deleted.is_(False), Project.is_archived.is_(False))
        .order_by(Project.default_order.asc(), Project.id.asc())
    )

    if cursor is not None:
        # Fetch the cursor row to get its ordering position
        cursor_project = session.execute(
            select(Project.default_order, Project.id).where(Project.id == cursor)
        ).one_or_none()
        if cursor_project is not None:
            query = query.where(
                (Project.default_order > cursor_project.default_order)
                | (
                    (Project.default_order == cursor_project.default_order)
                    & (Project.id > cursor_project.id)
                )
            )

    # Fetch one extra to detect if there's a next page
    results = session.execute(query.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    else:
        return list(results), None


def list_archived_projects(
    session: Session,
    *,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Project], str | None]:
    """List archived projects with cursor pagination."""
    query = (
        select(Project)
        .where(Project.is_deleted.is_(False), Project.is_archived.is_(True))
        .order_by(Project.default_order.asc(), Project.id.asc())
    )

    if cursor is not None:
        cursor_project = session.execute(
            select(Project.default_order, Project.id).where(Project.id == cursor)
        ).one_or_none()
        if cursor_project is not None:
            query = query.where(
                (Project.default_order > cursor_project.default_order)
                | (
                    (Project.default_order == cursor_project.default_order)
                    & (Project.id > cursor_project.id)
                )
            )

    results = session.execute(query.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    else:
        return list(results), None


def search_projects(
    session: Session,
    *,
    query_str: str,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Project], str | None]:
    """Search projects by name (case-insensitive contains)."""
    q = (
        select(Project)
        .where(
            Project.is_deleted.is_(False),
            Project.name.ilike(f"%{query_str}%"),
        )
        .order_by(Project.default_order.asc(), Project.id.asc())
    )

    if cursor is not None:
        cursor_project = session.execute(
            select(Project.default_order, Project.id).where(Project.id == cursor)
        ).one_or_none()
        if cursor_project is not None:
            q = q.where(
                (Project.default_order > cursor_project.default_order)
                | (
                    (Project.default_order == cursor_project.default_order)
                    & (Project.id > cursor_project.id)
                )
            )

    results = session.execute(q.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    else:
        return list(results), None


# ============================================================================
# PROJECT MUTATIONS
# ============================================================================


def create_project(
    session: Session,
    *,
    name: str,
    creator_uid: str | None = None,
    description: str = "",
    parent_id: str | None = None,
    color: str = "charcoal",
    is_favorite: bool = False,
    view_style: str | None = None,
    workspace_id: str | None = None,
) -> Project:
    """Create a new project and return it."""
    now = now_iso()

    # Determine next default_order
    max_order = session.execute(
        select(func.coalesce(func.max(Project.default_order), -1))
    ).scalar_one()

    project = Project(
        id=generate_id("project"),
        name=name,
        description=description,
        parent_id=parent_id,
        color=color,
        is_favorite=is_favorite,
        view_style=view_style or "list",
        creator_uid=creator_uid,
        workspace_id=workspace_id,
        default_order=max_order + 1,
        created_at=now,
        updated_at=now,
    )
    session.add(project)
    session.flush()
    return project


def update_project(
    session: Session,
    *,
    project_id: str,
    name: str | None = None,
    description: str | None = None,
    color: str | None = None,
    is_favorite: bool | None = None,
    view_style: str | None = None,
    child_order: int | None = None,
    is_collapsed: bool | None = None,
) -> Project | None:
    """Partial-update a project. Only provided fields are changed.

    Returns the updated project, or None if not found.
    """
    project = get_project(session, project_id)
    if project is None:
        return None

    if name is not None:
        project.name = name
    if description is not None:
        project.description = description
    if color is not None:
        project.color = color
    if is_favorite is not None:
        project.is_favorite = is_favorite
    if view_style is not None:
        project.view_style = view_style
    if child_order is not None:
        project.child_order = child_order
    if is_collapsed is not None:
        project.is_collapsed = is_collapsed

    project.updated_at = now_iso()
    session.flush()
    return project


def delete_project(session: Session, project_id: str) -> bool:
    """Soft-delete a project. Returns False if not found."""
    project = get_project(session, project_id)
    if project is None:
        return False

    project.is_deleted = True
    project.updated_at = now_iso()
    session.flush()
    return True


def archive_project(session: Session, project_id: str) -> bool:
    """Archive a project. Returns False if not found."""
    project = get_project(session, project_id)
    if project is None:
        return False

    project.is_archived = True
    project.updated_at = now_iso()
    session.flush()
    return True


def unarchive_project(session: Session, project_id: str) -> bool:
    """Unarchive a project. Returns False if not found or not archived."""
    project = session.execute(
        select(Project).where(
            Project.id == project_id,
            Project.is_deleted.is_(False),
            Project.is_archived.is_(True),
        )
    ).scalar_one_or_none()
    if project is None:
        return False

    project.is_archived = False
    project.updated_at = now_iso()
    session.flush()
    return True


# ============================================================================
# TASK QUERIES
# ============================================================================


def get_task(session: Session, task_id: str) -> Task | None:
    """Get a single task by ID. Returns None if not found or deleted."""
    return session.execute(
        select(Task).where(Task.id == task_id, Task.is_deleted.is_(False))
    ).scalar_one_or_none()


def list_tasks(
    session: Session,
    *,
    project_id: str | None = None,
    section_id: str | None = None,
    parent_id: str | None = None,
    label: str | None = None,
    ids: list[str] | None = None,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Task], str | None]:
    """List active tasks with optional filters and cursor pagination."""
    query = (
        select(Task)
        .where(Task.is_deleted.is_(False), Task.checked.is_(False))
        .order_by(Task.child_order.asc(), Task.id.asc())
    )

    if project_id is not None:
        query = query.where(Task.project_id == project_id)
    if section_id is not None:
        query = query.where(Task.section_id == section_id)
    if parent_id is not None:
        query = query.where(Task.parent_id == parent_id)
    if label is not None:
        # labels is a JSONB array — check if it contains the label string
        query = query.where(Task.labels.op("??")(label))
    if ids is not None:
        query = query.where(Task.id.in_(ids))

    if cursor is not None:
        cursor_task = session.execute(
            select(Task.child_order, Task.id).where(Task.id == cursor)
        ).one_or_none()
        if cursor_task is not None:
            query = query.where(
                (Task.child_order > cursor_task.child_order)
                | (
                    (Task.child_order == cursor_task.child_order)
                    & (Task.id > cursor_task.id)
                )
            )

    results = session.execute(query.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    return list(results), None


# ============================================================================
# TASK MUTATIONS
# ============================================================================


def create_task(
    session: Session,
    *,
    content: str,
    user_id: str,
    project_id: str,
    description: str = "",
    section_id: str | None = None,
    parent_id: str | None = None,
    labels: list[str] | None = None,
    priority: int = 1,
    due: dict | None = None,
    deadline: dict | None = None,
    duration: dict | None = None,
    order: int | None = None,
    assignee_id: str | None = None,
) -> Task:
    """Create a new task and return it."""
    now = now_iso()

    # Determine child_order if not provided
    if order is not None:
        child_order = order
    else:
        max_order = session.execute(
            select(func.coalesce(func.max(Task.child_order), -1)).where(
                Task.project_id == project_id
            )
        ).scalar_one()
        child_order = max_order + 1

    task = Task(
        id=generate_id("task"),
        content=content,
        description=description,
        project_id=project_id,
        section_id=section_id,
        parent_id=parent_id,
        user_id=user_id,
        added_by_uid=user_id,
        responsible_uid=assignee_id,
        labels=labels or [],
        priority=priority,
        due=due,
        deadline=deadline,
        duration=duration,
        child_order=child_order,
        goal_ids=[],
        added_at=now,
        updated_at=now,
    )
    session.add(task)
    session.flush()
    return task


def update_task(
    session: Session,
    *,
    task_id: str,
    content: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    priority: int | None = None,
    due: dict | None = None,
    deadline: dict | None = None,
    duration: dict | None = None,
    assignee_id: str | None = None,
    child_order: int | None = None,
    day_order: int | None = None,
    is_collapsed: bool | None = None,
) -> Task | None:
    """Partial-update a task. Returns None if not found."""
    task = get_task(session, task_id)
    if task is None:
        return None

    if content is not None:
        task.content = content
    if description is not None:
        task.description = description
    if labels is not None:
        task.labels = labels
    if priority is not None:
        task.priority = priority
    if due is not None:
        task.due = due
    if deadline is not None:
        task.deadline = deadline
    if duration is not None:
        task.duration = duration
    if assignee_id is not None:
        task.responsible_uid = assignee_id
    if child_order is not None:
        task.child_order = child_order
    if day_order is not None:
        task.day_order = day_order
    if is_collapsed is not None:
        task.is_collapsed = is_collapsed

    task.updated_at = now_iso()
    session.flush()
    return task


def delete_task(session: Session, task_id: str) -> bool:
    """Soft-delete a task."""
    task = get_task(session, task_id)
    if task is None:
        return False
    task.is_deleted = True
    task.updated_at = now_iso()
    session.flush()
    return True


def close_task(session: Session, task_id: str, completed_by_uid: str) -> bool:
    """Mark a task as completed."""
    task = get_task(session, task_id)
    if task is None:
        return False
    task.checked = True
    task.completed_at = now_iso()
    task.completed_by_uid = completed_by_uid
    task.updated_at = now_iso()
    session.flush()
    return True


def reopen_task(session: Session, task_id: str) -> bool:
    """Reopen a completed task."""
    task = session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.is_deleted.is_(False),
            Task.checked.is_(True),
        )
    ).scalar_one_or_none()
    if task is None:
        return False
    task.checked = False
    task.completed_at = None
    task.completed_by_uid = None
    task.updated_at = now_iso()
    session.flush()
    return True


def move_task(
    session: Session,
    *,
    task_id: str,
    project_id: str | None = None,
    section_id: str | None = None,
    parent_id: str | None = None,
) -> Task | None:
    """Move a task to a different project, section, or parent."""
    task = get_task(session, task_id)
    if task is None:
        return None
    if project_id is not None:
        task.project_id = project_id
        task.section_id = None  # reset section when moving projects
    if section_id is not None:
        task.section_id = section_id
    if parent_id is not None:
        task.parent_id = parent_id
    task.updated_at = now_iso()
    session.flush()
    return task


# ============================================================================
# LABEL QUERIES
# ============================================================================


def get_label(session: Session, label_id: str) -> Label | None:
    """Get a single label by ID. Returns None if not found or deleted."""
    return session.execute(
        select(Label).where(Label.id == label_id, Label.is_deleted.is_(False))
    ).scalar_one_or_none()


def list_labels(
    session: Session,
    *,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Label], str | None]:
    """List labels with cursor pagination.

    Returns (labels, next_cursor). next_cursor is None when there are no more
    results.

    Cursor is the last label ID from the previous page — we order by
    order then id for stable pagination.
    """
    query = (
        select(Label)
        .where(Label.is_deleted.is_(False))
        .order_by(Label.order.asc().nulls_last(), Label.id.asc())
    )

    if cursor is not None:
        # Fetch the cursor row to get its ordering position
        cursor_label = session.execute(
            select(Label.order, Label.id).where(Label.id == cursor)
        ).one_or_none()
        if cursor_label is not None:
            if cursor_label.order is not None:
                query = query.where(
                    (Label.order > cursor_label.order)
                    | (Label.order.is_(None))
                    | (
                        (Label.order == cursor_label.order)
                        & (Label.id > cursor_label.id)
                    )
                )
            else:
                query = query.where(
                    (Label.order.is_(None)) & (Label.id > cursor_label.id)
                )

    # Fetch one extra to detect if there's a next page
    results = session.execute(query.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    else:
        return list(results), None


# ============================================================================
# LABEL MUTATIONS
# ============================================================================


def create_label(
    session: Session,
    *,
    name: str,
    order: int | None = None,
    color: str = "charcoal",
    is_favorite: bool = False,
) -> Label:
    """Create a new label and return it."""
    now = now_iso()

    label = Label(
        id=generate_id("label"),
        name=name,
        order=order,
        color=color,
        is_favorite=is_favorite,
        created_at=now,
        updated_at=now,
    )
    session.add(label)
    session.flush()
    return label


def update_label(
    session: Session,
    *,
    label_id: str,
    name: str | None = None,
    order: int | None = None,
    color: str | None = None,
    is_favorite: bool | None = None,
) -> Label | None:
    """Partial-update a label. Only provided fields are changed.

    Returns the updated label, or None if not found.
    """
    label = get_label(session, label_id)
    if label is None:
        return None

    if name is not None:
        label.name = name
    if order is not None:
        label.order = order
    if color is not None:
        label.color = color
    if is_favorite is not None:
        label.is_favorite = is_favorite

    label.updated_at = now_iso()
    session.flush()
    return label


def delete_label(session: Session, label_id: str) -> bool:
    """Soft-delete a label. Returns False if not found."""
    label = get_label(session, label_id)
    if label is None:
        return False

    label.is_deleted = True
    label.updated_at = now_iso()
    session.flush()
    return True
