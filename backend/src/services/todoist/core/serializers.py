"""Serialization helpers for the Todoist API replica.

Each serialize function converts an ORM model into a dict matching the Todoist
API response shape. Todoist uses snake_case natively so no case conversion
is needed.
"""

from __future__ import annotations

from typing import Any

from ..database.schema import Label, Project, Task


def serialize_project(project: Project) -> dict[str, Any]:
    """Serialize a Project to match PersonalProjectSyncView / WorkspaceProjectSyncView."""
    result: dict[str, Any] = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "parent_id": project.parent_id,
        "child_order": project.child_order,
        "default_order": project.default_order,
        "color": project.color,
        "view_style": project.view_style,
        "is_collapsed": project.is_collapsed,
        "is_favorite": project.is_favorite,
        "is_archived": project.is_archived,
        "is_deleted": project.is_deleted,
        "is_frozen": project.is_frozen,
        "inbox_project": project.inbox_project,
        "is_shared": project.is_shared,
        "can_assign_tasks": project.can_assign_tasks,
        "can_comment": project.can_comment,
        "role": project.role,
        "public_key": project.public_key,
        "access": project.access,
        "creator_uid": project.creator_uid,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }

    # Workspace-only fields — include only when the project belongs to a workspace
    if project.workspace_id is not None:
        result["workspace_id"] = project.workspace_id
        result["folder_id"] = project.folder_id
        result["status"] = project.status
        result["collaborator_role_default"] = project.collaborator_role_default
        result["is_invite_only"] = project.is_invite_only
        result["is_link_sharing_enabled"] = project.is_link_sharing_enabled
        result["is_pending_default_collaborator_invites"] = (
            project.is_pending_default_collaborator_invites
        )
        result["is_project_insights_enabled"] = project.is_project_insights_enabled

    return result


def serialize_project_list(
    projects: list[Project],
    *,
    next_cursor: str | None,
) -> dict[str, Any]:
    """Serialize a paginated project list matching Todoist's PaginatedList shape."""
    return {
        "results": [serialize_project(p) for p in projects],
        "next_cursor": next_cursor,
    }


def serialize_task(task: Task) -> dict[str, Any]:
    """Serialize a Task to match ItemSyncView."""
    return {
        "id": task.id,
        "user_id": task.user_id,
        "project_id": task.project_id,
        "section_id": task.section_id,
        "parent_id": task.parent_id,
        "content": task.content,
        "description": task.description,
        "priority": task.priority,
        "child_order": task.child_order,
        "day_order": task.day_order,
        "labels": task.labels,
        "due": task.due,
        "deadline": task.deadline,
        "duration": task.duration,
        "checked": task.checked,
        "is_collapsed": task.is_collapsed,
        "is_deleted": task.is_deleted,
        "added_by_uid": task.added_by_uid,
        "assigned_by_uid": task.assigned_by_uid,
        "responsible_uid": task.responsible_uid,
        "completed_by_uid": task.completed_by_uid,
        "note_count": task.note_count,
        "goal_ids": task.goal_ids,
        "added_at": task.added_at,
        "completed_at": task.completed_at,
        "updated_at": task.updated_at,
    }


def serialize_task_list(
    tasks: list[Task],
    *,
    next_cursor: str | None,
) -> dict[str, Any]:
    """Serialize a paginated task list."""
    return {
        "results": [serialize_task(t) for t in tasks],
        "next_cursor": next_cursor,
    }


def serialize_label(label: Label) -> dict[str, Any]:
    """Serialize a Label to match LabelRestView."""
    return {
        "id": label.id,
        "name": label.name,
        "color": label.color,
        "order": label.order,
        "is_favorite": label.is_favorite,
    }


def serialize_label_list(
    labels: list[Label],
    *,
    next_cursor: str | None,
) -> dict[str, Any]:
    """Serialize a paginated label list."""
    return {
        "results": [serialize_label(l) for l in labels],
        "next_cursor": next_cursor,
    }
