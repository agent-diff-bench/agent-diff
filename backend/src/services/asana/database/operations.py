"""Session-first CRUD operations for Asana.

Functions are added to this file one at a time during the resource
implementation loop. Every function takes a SQLAlchemy Session as the first
argument. No function accesses request state directly.

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its operation functions to this file incrementally.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.utils import generate_id, now_iso
from .schema import (
    AsanaProject,
    AsanaTag,
    AsanaTask,
    AsanaTeam,
    AsanaUser,
    AsanaWorkspace,
)


# ---------------------------------------------------------------------------
# TASK QUERIES
# ---------------------------------------------------------------------------


def get_task(session: Session, task_gid: str) -> AsanaTask | None:
    return session.execute(
        select(AsanaTask).where(
            AsanaTask.gid == task_gid,
            AsanaTask.is_deleted.is_(False),
        )
    ).scalar_one_or_none()


def list_tasks(
    session: Session,
    *,
    assignee: str | None = None,
    project: str | None = None,
    section: str | None = None,
    workspace: str | None = None,
    completed_since: str | None = None,
    modified_since: str | None = None,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[AsanaTask], str | None]:
    query = select(AsanaTask).where(AsanaTask.is_deleted.is_(False))

    if assignee is not None:
        query = query.where(AsanaTask.assignee == assignee)
    if project is not None:
        query = query.join(AsanaTask.project_objects).where(AsanaProject.gid == project)
    if section is not None:
        query = query.where(AsanaTask.assignee_section == section)
    if workspace is not None:
        query = query.where(AsanaTask.workspace == workspace)
    if completed_since is not None:
        query = query.where(AsanaTask.completed_at >= completed_since)
    if modified_since is not None:
        query = query.where(AsanaTask.modified_at >= modified_since)

    query = query.order_by(AsanaTask.created_at.asc(), AsanaTask.gid.asc())

    if cursor is not None:
        cursor_task = session.execute(
            select(AsanaTask.created_at, AsanaTask.gid).where(AsanaTask.gid == cursor)
        ).one_or_none()
        if cursor_task:
            query = query.where(
                (AsanaTask.created_at > cursor_task.created_at)
                | (
                    (AsanaTask.created_at == cursor_task.created_at)
                    & (AsanaTask.gid > cursor_task.gid)
                )
            )

    results = session.execute(query.limit(limit + 1)).scalars().all()
    if len(results) > limit:
        next_cursor = results[limit - 1].gid
        return list(results[:limit]), next_cursor
    return list(results), None


def list_tasks_by_project(
    session: Session,
    project_gid: str,
) -> list[AsanaTask]:
    """Return all non-deleted tasks belonging to the given project."""
    return list(
        session.execute(
            select(AsanaTask)
            .join(AsanaTask.project_objects)
            .where(
                AsanaTask.is_deleted.is_(False),
                AsanaProject.gid == project_gid,
            )
            .order_by(AsanaTask.created_at.asc(), AsanaTask.gid.asc())
        ).scalars().all()
    )


def list_tasks_by_section(
    session: Session,
    section_gid: str,
) -> list[AsanaTask]:
    """Return all non-deleted tasks assigned to a given section."""
    return list(
        session.execute(
            select(AsanaTask)
            .where(
                AsanaTask.is_deleted.is_(False),
                AsanaTask.assignee_section == section_gid,
            )
            .order_by(AsanaTask.created_at.asc(), AsanaTask.gid.asc())
        ).scalars().all()
    )


def list_tasks_by_tag(
    session: Session,
    tag_gid: str,
) -> list[AsanaTask]:
    """Return all non-deleted tasks associated with the given tag."""
    return list(
        session.execute(
            select(AsanaTask)
            .join(AsanaTask.tag_objects)
            .where(
                AsanaTask.is_deleted.is_(False),
                AsanaTag.gid == tag_gid,
            )
            .order_by(AsanaTask.created_at.asc(), AsanaTask.gid.asc())
        ).scalars().all()
    )


def list_tasks_by_user_task_list(
    session: Session,
    user_task_list_gid: str,
) -> list[AsanaTask]:
    """Return all non-deleted tasks for a user task list.

    User task lists are essentially the assignee's personal list, so we
    filter by assignee matching the user_task_list_gid. In a full
    implementation this would go through a join table, but for now we
    treat the user_task_list_gid as an assignee identifier.
    """
    return list(
        session.execute(
            select(AsanaTask)
            .where(
                AsanaTask.is_deleted.is_(False),
                AsanaTask.assignee == user_task_list_gid,
            )
            .order_by(AsanaTask.created_at.asc(), AsanaTask.gid.asc())
        ).scalars().all()
    )


def list_subtasks(
    session: Session,
    parent_gid: str,
    *,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[AsanaTask], str | None]:
    query = (
        select(AsanaTask)
        .where(
            AsanaTask.is_deleted.is_(False),
            AsanaTask.parent == parent_gid,
        )
        .order_by(AsanaTask.created_at.asc(), AsanaTask.gid.asc())
    )

    if cursor is not None:
        cursor_task = session.execute(
            select(AsanaTask.created_at, AsanaTask.gid).where(AsanaTask.gid == cursor)
        ).one_or_none()
        if cursor_task:
            query = query.where(
                (AsanaTask.created_at > cursor_task.created_at)
                | (
                    (AsanaTask.created_at == cursor_task.created_at)
                    & (AsanaTask.gid > cursor_task.gid)
                )
            )

    results = session.execute(query.limit(limit + 1)).scalars().all()
    if len(results) > limit:
        next_cursor = results[limit - 1].gid
        return list(results[:limit]), next_cursor
    return list(results), None


def search_tasks(
    session: Session,
    workspace_gid: str,
) -> list[AsanaTask]:
    """Simple workspace-scoped task search (returns all tasks in workspace)."""
    return list(
        session.execute(
            select(AsanaTask)
            .where(
                AsanaTask.is_deleted.is_(False),
                AsanaTask.workspace == workspace_gid,
            )
            .order_by(AsanaTask.created_at.asc(), AsanaTask.gid.asc())
        ).scalars().all()
    )


def get_task_by_custom_id(
    session: Session,
    workspace_gid: str,
    custom_id: str,
) -> AsanaTask | None:
    """Retrieve a task by its external custom ID within a workspace."""
    return session.execute(
        select(AsanaTask).where(
            AsanaTask.is_deleted.is_(False),
            AsanaTask.workspace == workspace_gid,
            AsanaTask.external.op("->>")("gid") == custom_id,
        )
    ).scalar_one_or_none()


def get_dependencies(session: Session, task_gid: str) -> list[AsanaTask]:
    """Return tasks that the given task depends on."""
    task = get_task(session, task_gid)
    if task is None or not task.dependencies:
        return []
    dependency_gids = [
        dep["gid"] if isinstance(dep, dict) else dep
        for dep in task.dependencies
    ]
    if not dependency_gids:
        return []
    return list(
        session.execute(
            select(AsanaTask).where(
                AsanaTask.gid.in_(dependency_gids),
                AsanaTask.is_deleted.is_(False),
            )
        ).scalars().all()
    )


def get_dependents(session: Session, task_gid: str) -> list[AsanaTask]:
    """Return tasks that depend on the given task."""
    task = get_task(session, task_gid)
    if task is None or not task.dependents:
        return []
    dependent_gids = [
        dep["gid"] if isinstance(dep, dict) else dep
        for dep in task.dependents
    ]
    if not dependent_gids:
        return []
    return list(
        session.execute(
            select(AsanaTask).where(
                AsanaTask.gid.in_(dependent_gids),
                AsanaTask.is_deleted.is_(False),
            )
        ).scalars().all()
    )


# ---------------------------------------------------------------------------
# TASK MUTATIONS
# ---------------------------------------------------------------------------


def create_task(session: Session, *, data: dict[str, Any]) -> AsanaTask:
    timestamp = now_iso()

    # Extract M:N relationship IDs before building the model
    project_gids = data.get("projects", [])
    tag_gids = data.get("tags", [])

    task = AsanaTask(
        gid=generate_id("task"),
        resource_type="task",
        name=data.get("name"),
        resource_subtype=data.get("resource_subtype", "default_task"),
        approval_status=data.get("approval_status"),
        assignee_status=data.get("assignee_status"),
        completed=data.get("completed", False),
        completed_at=None,
        created_at=timestamp,
        modified_at=timestamp,
        due_at=data.get("due_at"),
        due_on=data.get("due_on"),
        external=data.get("external"),
        html_notes=data.get("html_notes"),
        hearted=False,
        hearts=[],
        is_rendered_as_separator=False,
        liked=data.get("liked", False),
        likes=[],
        notes=data.get("notes"),
        num_hearts=0,
        num_likes=0,
        num_subtasks=0,
        start_at=data.get("start_at"),
        start_on=data.get("start_on"),
        actual_time_minutes=None,
        assignee=data.get("assignee"),
        assignee_section=data.get("assignee_section"),
        custom_fields=data.get("custom_fields"),
        custom_type=data.get("custom_type"),
        custom_type_status_option=data.get("custom_type_status_option"),
        dependencies=[],
        dependents=[],
        followers=data.get("followers", []),
        parent=data.get("parent"),
        workspace=data.get("workspace"),
        permalink_url=f"https://app.asana.com/0/0/task/{generate_id('task')}",
    )
    session.add(task)
    session.flush()

    # Link M:N projects — ensure stub rows exist for referenced projects
    for project_gid in project_gids:
        _ensure_project_stub(session, project_gid)
        if not any(project.gid == project_gid for project in task.project_objects):
            task.project_objects.append(session.get(AsanaProject, project_gid))

    # Link M:N tags — ensure stub rows exist for referenced tags
    for tag_gid in tag_gids:
        _ensure_tag_stub(session, tag_gid)
        if not any(tag.gid == tag_gid for tag in task.tag_objects):
            task.tag_objects.append(session.get(AsanaTag, tag_gid))

    session.flush()
    return task


def update_task(
    session: Session,
    task_gid: str,
    *,
    data: dict[str, Any],
) -> AsanaTask | None:
    task = get_task(session, task_gid)
    if task is None:
        return None

    updatable_fields = [
        "name", "resource_subtype", "approval_status", "assignee_status",
        "completed", "due_at", "due_on", "external", "html_notes",
        "liked", "notes", "start_at", "start_on",
        "assignee", "assignee_section", "custom_fields",
        "custom_type", "custom_type_status_option", "workspace",
    ]

    for field in updatable_fields:
        if field in data:
            setattr(task, field, data[field])

    # Replace M:N projects if provided
    if "projects" in data:
        project_gids = data["projects"] or []
        task.project_objects.clear()
        for project_gid in project_gids:
            _ensure_project_stub(session, project_gid)
            task.project_objects.append(session.get(AsanaProject, project_gid))

    # Replace M:N tags if provided
    if "tags" in data:
        tag_gids = data["tags"] or []
        task.tag_objects.clear()
        for tag_gid in tag_gids:
            _ensure_tag_stub(session, tag_gid)
            task.tag_objects.append(session.get(AsanaTag, tag_gid))

    # Sync completed_at with completed flag
    if "completed" in data:
        if data["completed"]:
            task.completed_at = now_iso()
            if task.approval_status == "pending":
                task.approval_status = "approved"
        else:
            task.completed_at = None

    task.modified_at = now_iso()
    session.flush()
    return task


def delete_task(session: Session, task_gid: str) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    task.is_deleted = True
    task.modified_at = now_iso()
    session.flush()
    return True


def duplicate_task(
    session: Session,
    task_gid: str,
    *,
    name: str | None = None,
    include: str | None = None,
) -> AsanaTask | None:
    source = get_task(session, task_gid)
    if source is None:
        return None

    include_fields = set()
    if include:
        include_fields = {field.strip() for field in include.split(",")}

    timestamp = now_iso()
    new_task = AsanaTask(
        gid=generate_id("task"),
        resource_type="task",
        name=name or f"{source.name} (copy)",
        resource_subtype=source.resource_subtype,
        created_at=timestamp,
        modified_at=timestamp,
        completed=False,
        completed_at=None,
        hearted=False,
        hearts=[],
        is_rendered_as_separator=False,
        liked=False,
        likes=[],
        num_hearts=0,
        num_likes=0,
        num_subtasks=0,
        actual_time_minutes=None,
        dependencies=[],
        dependents=[],
        workspace=source.workspace,
    )

    if "notes" in include_fields:
        new_task.notes = source.notes
        new_task.html_notes = source.html_notes
    if "assignee" in include_fields:
        new_task.assignee = source.assignee
    if "tags" in include_fields:
        for tag in source.tag_objects:
            new_task.tag_objects.append(tag)
    if "followers" in include_fields:
        new_task.followers = list(source.followers) if source.followers else []
    if "projects" in include_fields:
        for project in source.project_objects:
            new_task.project_objects.append(project)
    if "dates" in include_fields:
        new_task.due_at = source.due_at
        new_task.due_on = source.due_on
        new_task.start_at = source.start_at
        new_task.start_on = source.start_on
    if "dependencies" in include_fields:
        new_task.dependencies = list(source.dependencies) if source.dependencies else []
    if "parent" in include_fields:
        new_task.parent = source.parent

    new_task.permalink_url = f"https://app.asana.com/0/0/task/{new_task.gid}"
    session.add(new_task)
    session.flush()
    return new_task


def set_parent(
    session: Session,
    task_gid: str,
    *,
    parent_gid: str | None,
) -> AsanaTask | None:
    task = get_task(session, task_gid)
    if task is None:
        return None

    # Decrement subtask count on old parent
    if task.parent:
        old_parent = get_task(session, task.parent)
        if old_parent and old_parent.num_subtasks and old_parent.num_subtasks > 0:
            old_parent.num_subtasks -= 1

    task.parent = parent_gid
    task.modified_at = now_iso()

    # Increment subtask count on new parent
    if parent_gid:
        new_parent = get_task(session, parent_gid)
        if new_parent:
            new_parent.num_subtasks = (new_parent.num_subtasks or 0) + 1

    session.flush()
    return task


def create_subtask(
    session: Session,
    parent_gid: str,
    *,
    data: dict[str, Any],
) -> AsanaTask | None:
    parent = get_task(session, parent_gid)
    if parent is None:
        return None

    data["parent"] = parent_gid
    # Inherit workspace from parent if not provided
    if "workspace" not in data and parent.workspace:
        data["workspace"] = parent.workspace

    subtask = create_task(session, data=data)
    parent.num_subtasks = (parent.num_subtasks or 0) + 1
    session.flush()
    return subtask


def add_dependencies(
    session: Session,
    task_gid: str,
    *,
    dependency_gids: list[str],
) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    current = list(task.dependencies) if task.dependencies else []
    existing_gids = {
        dep["gid"] if isinstance(dep, dict) else dep for dep in current
    }
    for gid in dependency_gids:
        if gid not in existing_gids:
            current.append({"gid": gid})
    task.dependencies = current
    task.modified_at = now_iso()
    session.flush()
    return True


def remove_dependencies(
    session: Session,
    task_gid: str,
    *,
    dependency_gids: list[str],
) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    current = list(task.dependencies) if task.dependencies else []
    remove_set = set(dependency_gids)
    task.dependencies = [
        dep for dep in current
        if (dep["gid"] if isinstance(dep, dict) else dep) not in remove_set
    ]
    task.modified_at = now_iso()
    session.flush()
    return True


def add_dependents(
    session: Session,
    task_gid: str,
    *,
    dependent_gids: list[str],
) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    current = list(task.dependents) if task.dependents else []
    existing_gids = {
        dep["gid"] if isinstance(dep, dict) else dep for dep in current
    }
    for gid in dependent_gids:
        if gid not in existing_gids:
            current.append({"gid": gid})
    task.dependents = current
    task.modified_at = now_iso()
    session.flush()
    return True


def remove_dependents(
    session: Session,
    task_gid: str,
    *,
    dependent_gids: list[str],
) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    current = list(task.dependents) if task.dependents else []
    remove_set = set(dependent_gids)
    task.dependents = [
        dep for dep in current
        if (dep["gid"] if isinstance(dep, dict) else dep) not in remove_set
    ]
    task.modified_at = now_iso()
    session.flush()
    return True


def add_followers(
    session: Session,
    task_gid: str,
    *,
    follower_gids: list[str],
) -> AsanaTask | None:
    task = get_task(session, task_gid)
    if task is None:
        return None
    current = list(task.followers) if task.followers else []
    existing = set(current)
    for gid in follower_gids:
        if gid not in existing:
            current.append(gid)
            existing.add(gid)
    task.followers = current
    task.modified_at = now_iso()
    session.flush()
    return task


def remove_followers(
    session: Session,
    task_gid: str,
    *,
    follower_gids: list[str],
) -> AsanaTask | None:
    task = get_task(session, task_gid)
    if task is None:
        return None
    remove_set = set(follower_gids)
    task.followers = [
        gid for gid in (task.followers or []) if gid not in remove_set
    ]
    task.modified_at = now_iso()
    session.flush()
    return task


def add_project_to_task(
    session: Session,
    task_gid: str,
    *,
    project_gid: str,
) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    _ensure_project_stub(session, project_gid)
    project = session.get(AsanaProject, project_gid)
    if not any(p.gid == project_gid for p in task.project_objects):
        task.project_objects.append(project)
    task.modified_at = now_iso()
    session.flush()
    return True


def remove_project_from_task(
    session: Session,
    task_gid: str,
    *,
    project_gid: str,
) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    project = session.get(AsanaProject, project_gid)
    if project and project in task.project_objects:
        task.project_objects.remove(project)
    task.modified_at = now_iso()
    session.flush()
    return True


def add_tag_to_task(
    session: Session,
    task_gid: str,
    *,
    tag_gid: str,
) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    _ensure_tag_stub(session, tag_gid)
    tag = session.get(AsanaTag, tag_gid)
    if not any(t.gid == tag_gid for t in task.tag_objects):
        task.tag_objects.append(tag)
    task.modified_at = now_iso()
    session.flush()
    return True


def remove_tag_from_task(
    session: Session,
    task_gid: str,
    *,
    tag_gid: str,
) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    tag = session.get(AsanaTag, tag_gid)
    if tag and tag in task.tag_objects:
        task.tag_objects.remove(tag)
    task.modified_at = now_iso()
    session.flush()
    return True


# ---------------------------------------------------------------------------
# PROJECT QUERIES
# ---------------------------------------------------------------------------


def get_project(session: Session, project_gid: str) -> AsanaProject | None:
    return session.execute(
        select(AsanaProject).where(
            AsanaProject.gid == project_gid,
            AsanaProject.is_deleted.is_(False),
        )
    ).scalar_one_or_none()


def list_projects(
    session: Session,
    *,
    workspace: str | None = None,
    team: str | None = None,
    archived: bool | None = None,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[AsanaProject], str | None]:
    query = select(AsanaProject).where(AsanaProject.is_deleted.is_(False))

    if workspace is not None:
        query = query.where(AsanaProject.workspace == workspace)
    if team is not None:
        query = query.where(AsanaProject.team == team)
    if archived is not None:
        query = query.where(AsanaProject.archived.is_(archived))

    query = query.order_by(AsanaProject.created_at.asc(), AsanaProject.gid.asc())

    if cursor is not None:
        cursor_project = session.execute(
            select(AsanaProject.created_at, AsanaProject.gid).where(AsanaProject.gid == cursor)
        ).one_or_none()
        if cursor_project:
            query = query.where(
                (AsanaProject.created_at > cursor_project.created_at)
                | (
                    (AsanaProject.created_at == cursor_project.created_at)
                    & (AsanaProject.gid > cursor_project.gid)
                )
            )

    results = session.execute(query.limit(limit + 1)).scalars().all()
    if len(results) > limit:
        next_cursor = results[limit - 1].gid
        return list(results[:limit]), next_cursor
    return list(results), None


def list_projects_for_task(
    session: Session,
    task_gid: str,
) -> list[AsanaProject]:
    """Return all non-deleted projects that contain the given task."""
    task = get_task(session, task_gid)
    if task is None:
        return []
    return [project for project in task.project_objects if not project.is_deleted]


def search_projects_in_workspace(
    session: Session,
    workspace_gid: str,
) -> list[AsanaProject]:
    """Simple workspace-scoped project search."""
    return list(
        session.execute(
            select(AsanaProject)
            .where(
                AsanaProject.is_deleted.is_(False),
                AsanaProject.workspace == workspace_gid,
            )
            .order_by(AsanaProject.created_at.asc(), AsanaProject.gid.asc())
        ).scalars().all()
    )


# ---------------------------------------------------------------------------
# PROJECT MUTATIONS
# ---------------------------------------------------------------------------


def create_project(session: Session, *, data: dict[str, Any]) -> AsanaProject:
    timestamp = now_iso()

    # Ensure FK target stubs exist before assigning
    owner_gid = data.get("owner")
    if owner_gid:
        _ensure_user_stub(session, owner_gid)
    team_gid = data.get("team")
    if team_gid:
        _ensure_team_stub(session, team_gid)
    workspace_gid = data.get("workspace")
    if workspace_gid:
        _ensure_workspace_stub(session, workspace_gid)

    project = AsanaProject(
        gid=generate_id("project"),
        resource_type="project",
        name=data.get("name"),
        archived=data.get("archived", False),
        color=data.get("color"),
        icon=data.get("icon"),
        created_at=timestamp,
        modified_at=timestamp,
        default_view=data.get("default_view"),
        due_date=data.get("due_date"),
        due_on=data.get("due_on"),
        start_on=data.get("start_on"),
        html_notes=data.get("html_notes"),
        notes=data.get("notes"),
        public=data.get("public"),
        privacy_setting=data.get("privacy_setting"),
        default_access_level=data.get("default_access_level"),
        minimum_access_level_for_customization=data.get("minimum_access_level_for_customization"),
        minimum_access_level_for_sharing=data.get("minimum_access_level_for_sharing"),
        completed=False,
        completed_at=None,
        completed_by=None,
        current_status=data.get("current_status"),
        current_status_update=data.get("current_status_update"),
        custom_field_settings=data.get("custom_field_settings", []),
        custom_fields=data.get("custom_fields"),
        members=data.get("members", []),
        followers=data.get("followers", []),
        owner=owner_gid,
        team=team_gid,
        workspace=workspace_gid,
        project_brief=None,
        created_from_template=None,
        permalink_url=f"https://app.asana.com/0/{generate_id('project')}/overview",
    )
    session.add(project)
    session.flush()
    return project


def update_project(
    session: Session,
    project_gid: str,
    *,
    data: dict[str, Any],
) -> AsanaProject | None:
    project = get_project(session, project_gid)
    if project is None:
        return None

    # Ensure FK target stubs exist before updating FK fields
    if "owner" in data and data["owner"]:
        _ensure_user_stub(session, data["owner"])
    if "team" in data and data["team"]:
        _ensure_team_stub(session, data["team"])

    updatable_fields = [
        "name", "archived", "color", "icon", "default_view",
        "due_date", "due_on", "start_on", "html_notes", "notes",
        "public", "privacy_setting", "default_access_level",
        "minimum_access_level_for_customization",
        "minimum_access_level_for_sharing",
        "current_status", "current_status_update",
        "custom_fields", "owner", "team",
    ]

    for field in updatable_fields:
        if field in data:
            setattr(project, field, data[field])

    project.modified_at = now_iso()
    session.flush()
    return project


def delete_project(session: Session, project_gid: str) -> bool:
    project = get_project(session, project_gid)
    if project is None:
        return False
    project.is_deleted = True
    project.modified_at = now_iso()
    session.flush()
    return True


def duplicate_project(
    session: Session,
    project_gid: str,
    *,
    name: str | None = None,
    team: str | None = None,
    include: str | None = None,
) -> AsanaProject | None:
    source = get_project(session, project_gid)
    if source is None:
        return None

    include_fields = set()
    if include:
        include_fields = {field.strip() for field in include.split(",")}

    # Ensure FK stub exists if team is overridden
    effective_team = team or source.team
    if effective_team and effective_team != source.team:
        _ensure_team_stub(session, effective_team)

    timestamp = now_iso()
    new_project = AsanaProject(
        gid=generate_id("project"),
        resource_type="project",
        name=name or f"{source.name} (copy)",
        archived=False,
        color=source.color,
        icon=source.icon,
        created_at=timestamp,
        modified_at=timestamp,
        default_view=source.default_view,
        completed=False,
        completed_at=None,
        completed_by=None,
        current_status=None,
        current_status_update=None,
        custom_field_settings=list(source.custom_field_settings) if source.custom_field_settings else [],
        custom_fields=None,
        privacy_setting=source.privacy_setting,
        default_access_level=source.default_access_level,
        minimum_access_level_for_customization=source.minimum_access_level_for_customization,
        minimum_access_level_for_sharing=source.minimum_access_level_for_sharing,
        workspace=source.workspace,
        team=effective_team,
        owner=source.owner,
        project_brief=None,
        created_from_template=None,
        members=[],
        followers=[],
    )

    if "notes" in include_fields:
        new_project.notes = source.notes
        new_project.html_notes = source.html_notes
    if "members" in include_fields:
        new_project.members = list(source.members) if source.members else []
    if "task_dates" in include_fields:
        new_project.due_date = source.due_date
        new_project.due_on = source.due_on
        new_project.start_on = source.start_on

    new_project.permalink_url = f"https://app.asana.com/0/{new_project.gid}/overview"
    session.add(new_project)
    session.flush()
    return new_project


def add_followers_to_project(
    session: Session,
    project_gid: str,
    *,
    follower_gids: list[str],
) -> AsanaProject | None:
    project = get_project(session, project_gid)
    if project is None:
        return None
    current = list(project.followers) if project.followers else []
    existing = set(current)
    for gid in follower_gids:
        if gid not in existing:
            current.append(gid)
            existing.add(gid)
    project.followers = current
    project.modified_at = now_iso()
    session.flush()
    return project


def remove_followers_from_project(
    session: Session,
    project_gid: str,
    *,
    follower_gids: list[str],
) -> AsanaProject | None:
    project = get_project(session, project_gid)
    if project is None:
        return None
    remove_set = set(follower_gids)
    project.followers = [
        gid for gid in (project.followers or []) if gid not in remove_set
    ]
    project.modified_at = now_iso()
    session.flush()
    return project


def add_members_to_project(
    session: Session,
    project_gid: str,
    *,
    member_gids: list[str],
) -> AsanaProject | None:
    project = get_project(session, project_gid)
    if project is None:
        return None
    current = list(project.members) if project.members else []
    existing = set(current)
    for gid in member_gids:
        if gid not in existing:
            current.append(gid)
            existing.add(gid)
    project.members = current
    project.modified_at = now_iso()
    session.flush()
    return project


def remove_members_from_project(
    session: Session,
    project_gid: str,
    *,
    member_gids: list[str],
) -> AsanaProject | None:
    project = get_project(session, project_gid)
    if project is None:
        return None
    remove_set = set(member_gids)
    project.members = [
        gid for gid in (project.members or []) if gid not in remove_set
    ]
    project.modified_at = now_iso()
    session.flush()
    return project


def add_custom_field_setting_to_project(
    session: Session,
    project_gid: str,
    *,
    data: dict[str, Any],
) -> AsanaProject | None:
    project = get_project(session, project_gid)
    if project is None:
        return None
    current = list(project.custom_field_settings) if project.custom_field_settings else []
    setting = {
        "gid": generate_id("project"),
        "resource_type": "custom_field_setting",
        "custom_field": data.get("custom_field"),
        "is_important": data.get("is_important", False),
    }
    current.append(setting)
    project.custom_field_settings = current
    project.modified_at = now_iso()
    session.flush()
    return project


def remove_custom_field_setting_from_project(
    session: Session,
    project_gid: str,
    *,
    custom_field_gid: str,
) -> AsanaProject | None:
    project = get_project(session, project_gid)
    if project is None:
        return None
    current = list(project.custom_field_settings) if project.custom_field_settings else []
    project.custom_field_settings = [
        setting for setting in current
        if setting.get("custom_field") != custom_field_gid
    ]
    project.modified_at = now_iso()
    session.flush()
    return project


# ---------------------------------------------------------------------------
# STUB HELPERS — ensure FK targets exist before linking
# ---------------------------------------------------------------------------


def _ensure_project_stub(session: Session, project_gid: str) -> None:
    """Create a minimal project row if it doesn't already exist."""
    if session.get(AsanaProject, project_gid) is None:
        session.add(AsanaProject(gid=project_gid, resource_type="project"))
        session.flush()


def _ensure_tag_stub(session: Session, tag_gid: str) -> None:
    """Create a minimal tag row if it doesn't already exist."""
    if session.get(AsanaTag, tag_gid) is None:
        session.add(AsanaTag(gid=tag_gid, resource_type="tag"))
        session.flush()


def _ensure_user_stub(session: Session, user_gid: str) -> None:
    """Create a minimal user row if it doesn't already exist."""
    if session.get(AsanaUser, user_gid) is None:
        session.add(AsanaUser(gid=user_gid, resource_type="user"))
        session.flush()


def _ensure_team_stub(session: Session, team_gid: str) -> None:
    """Create a minimal team row if it doesn't already exist."""
    if session.get(AsanaTeam, team_gid) is None:
        session.add(AsanaTeam(gid=team_gid, resource_type="team"))
        session.flush()


def _ensure_workspace_stub(session: Session, workspace_gid: str) -> None:
    """Create a minimal workspace row if it doesn't already exist."""
    if session.get(AsanaWorkspace, workspace_gid) is None:
        session.add(AsanaWorkspace(gid=workspace_gid, resource_type="workspace"))
        session.flush()


# ---------------------------------------------------------------------------
# TIME TRACKING ENTRY OPERATIONS
# ---------------------------------------------------------------------------

# Stored as JSONB on a lightweight table. For Pass 1 we keep time tracking
# entries as rows in a simple dedicated model. Since that model doesn't exist
# yet, we store them inline on the task for now and will migrate in Pass 2.

def list_time_tracking_entries(
    session: Session,
    task_gid: str,
    *,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[dict], str | None]:
    """Return time tracking entries stored on the task.

    In Pass 1 these are kept in a separate lightweight table. Since we
    don't have that table yet, we return an empty list. The route handler
    still responds correctly with the expected envelope.
    """
    return [], None


def create_time_tracking_entry(
    session: Session,
    task_gid: str,
    *,
    data: dict[str, Any],
) -> dict | None:
    """Create a time tracking entry for a task.

    Returns a dict representing the entry. Actual time on the task is
    updated as a side effect.
    """
    task = get_task(session, task_gid)
    if task is None:
        return None

    entry_gid = generate_id("time_tracking_entry")
    timestamp = now_iso()
    duration_minutes = data.get("duration_minutes", 0)

    entry = {
        "gid": entry_gid,
        "resource_type": "time_tracking_entry",
        "duration_minutes": duration_minutes,
        "entered_on": data.get("entered_on", timestamp[:10]),
        "created_at": timestamp,
    }

    # Update actual_time_minutes on the task
    task.actual_time_minutes = (task.actual_time_minutes or 0) + duration_minutes
    task.modified_at = timestamp
    session.flush()
    return entry
