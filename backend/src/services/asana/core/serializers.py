"""Serialization helpers for the Asana API replica.

Each serialize function converts an ORM model into a dict matching the
source API's response shape. Functions are added one at a time during the
resource implementation loop.

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its serializer functions to this file incrementally.
"""

from __future__ import annotations

from typing import Any

from ..database.schema import (
    AsanaProject,
    AsanaSection,
    AsanaTag,
    AsanaTask,
    AsanaTeam,
    AsanaUser,
    AsanaWorkspace,
)


# ---------------------------------------------------------------------------
# COMPACT SERIALIZERS FOR RELATED RESOURCES
# ---------------------------------------------------------------------------


def serialize_project_compact(project: AsanaProject) -> dict[str, Any]:
    return {
        "gid": project.gid,
        "resource_type": project.resource_type or "project",
        "name": project.name,
    }


def serialize_section_compact(section: AsanaSection) -> dict[str, Any]:
    return {
        "gid": section.gid,
        "resource_type": section.resource_type or "section",
        "name": section.name,
    }


def serialize_tag_compact(tag: AsanaTag) -> dict[str, Any]:
    return {
        "gid": tag.gid,
        "resource_type": tag.resource_type or "tag",
        "name": tag.name,
    }


def serialize_user_compact(user: AsanaUser) -> dict[str, Any]:
    return {
        "gid": user.gid,
        "resource_type": user.resource_type or "user",
        "name": user.name,
    }


def serialize_team_compact(team: AsanaTeam) -> dict[str, Any]:
    return {
        "gid": team.gid,
        "resource_type": team.resource_type or "team",
        "name": team.name,
    }


def serialize_workspace_compact(workspace: AsanaWorkspace) -> dict[str, Any]:
    return {
        "gid": workspace.gid,
        "resource_type": workspace.resource_type or "workspace",
        "name": workspace.name,
    }


# ---------------------------------------------------------------------------
# PROJECT SERIALIZERS
# ---------------------------------------------------------------------------


def serialize_project(project: AsanaProject) -> dict[str, Any]:
    """Full project representation matching ProjectResponse schema."""

    # Serialize owner as compact user or None
    owner_value: Any = None
    if project.owner_object:
        owner_value = serialize_user_compact(project.owner_object)
    elif project.owner:
        owner_value = {"gid": project.owner, "resource_type": "user"}

    # Serialize completed_by as compact user or None
    completed_by_value: Any = None
    if project.completed_by_object:
        completed_by_value = serialize_user_compact(project.completed_by_object)
    elif project.completed_by:
        completed_by_value = {"gid": project.completed_by, "resource_type": "user"}

    # Serialize team as compact object or None
    team_value: Any = None
    if project.team_object:
        team_value = serialize_team_compact(project.team_object)
    elif project.team:
        team_value = {"gid": project.team, "resource_type": "team"}

    # Serialize workspace as compact object or None
    workspace_value: Any = None
    if project.workspace_object:
        workspace_value = serialize_workspace_compact(project.workspace_object)
    elif project.workspace:
        workspace_value = {"gid": project.workspace, "resource_type": "workspace"}

    return {
        "gid": project.gid,
        "resource_type": project.resource_type or "project",
        "name": project.name,
        "archived": project.archived or False,
        "color": project.color,
        "icon": project.icon,
        "created_at": project.created_at,
        "modified_at": project.modified_at,
        "default_view": project.default_view,
        "due_date": project.due_date,
        "due_on": project.due_on,
        "start_on": project.start_on,
        "html_notes": project.html_notes,
        "notes": project.notes,
        "public": project.public,
        "privacy_setting": project.privacy_setting,
        "default_access_level": project.default_access_level,
        "minimum_access_level_for_customization": project.minimum_access_level_for_customization,
        "minimum_access_level_for_sharing": project.minimum_access_level_for_sharing,
        "completed": project.completed or False,
        "completed_at": project.completed_at,
        "completed_by": completed_by_value,
        "current_status": project.current_status,
        "current_status_update": project.current_status_update,
        "custom_field_settings": project.custom_field_settings or [],
        "custom_fields": project.custom_fields or [],
        "members": project.members or [],
        "followers": project.followers or [],
        "owner": owner_value,
        "team": team_value,
        "workspace": workspace_value,
        "permalink_url": project.permalink_url,
        "project_brief": project.project_brief,
        "created_from_template": project.created_from_template,
    }


def serialize_project_list(
    projects: list[AsanaProject],
    next_page: str | None = None,
) -> dict[str, Any]:
    """Collection envelope matching Asana's paginated response shape."""
    result: dict[str, Any] = {
        "data": [serialize_project_compact(project) for project in projects],
    }
    if next_page is not None:
        result["next_page"] = {
            "offset": next_page,
            "path": None,
            "uri": None,
        }
    else:
        result["next_page"] = None
    return result


# ---------------------------------------------------------------------------
# TASK SERIALIZERS
# ---------------------------------------------------------------------------


def serialize_task_compact(task: AsanaTask) -> dict[str, Any]:
    """Minimal task representation used in list endpoints."""
    return {
        "gid": task.gid,
        "resource_type": task.resource_type or "task",
        "name": task.name,
        "resource_subtype": task.resource_subtype or "default_task",
    }


def serialize_task(task: AsanaTask) -> dict[str, Any]:
    """Full task representation matching TaskResponse schema."""

    # Serialize assignee as compact user object or None
    assignee_value: Any = None
    if task.assignee_object:
        assignee_value = serialize_user_compact(task.assignee_object)
    elif task.assignee:
        assignee_value = {"gid": task.assignee, "resource_type": "user"}

    # Serialize assignee_section as compact section object or None
    assignee_section_value: Any = None
    if task.assignee_section_object:
        assignee_section_value = serialize_section_compact(task.assignee_section_object)
    elif task.assignee_section:
        assignee_section_value = {"gid": task.assignee_section, "resource_type": "section"}

    # Serialize parent as compact task or None
    parent_value: Any = None
    if task.parent_task:
        parent_value = serialize_task_compact(task.parent_task)
    elif task.parent:
        parent_value = {"gid": task.parent, "resource_type": "task"}

    # Serialize workspace as compact object or None
    workspace_value: Any = None
    if task.workspace_object:
        workspace_value = serialize_workspace_compact(task.workspace_object)
    elif task.workspace:
        workspace_value = {"gid": task.workspace, "resource_type": "workspace"}

    # Serialize M:N projects
    projects_value = [
        serialize_project_compact(project) for project in task.project_objects
    ]

    # Serialize M:N tags
    tags_value = [
        serialize_tag_compact(tag) for tag in task.tag_objects
    ]

    result: dict[str, Any] = {
        "gid": task.gid,
        "resource_type": task.resource_type or "task",
        "name": task.name,
        "resource_subtype": task.resource_subtype or "default_task",
        "created_by": task.created_by,
        "approval_status": task.approval_status,
        "assignee_status": task.assignee_status,
        "completed": task.completed or False,
        "completed_at": task.completed_at,
        "completed_by": task.completed_by,
        "created_at": task.created_at,
        "due_at": task.due_at,
        "due_on": task.due_on,
        "external": task.external,
        "html_notes": task.html_notes,
        "hearted": task.hearted or False,
        "hearts": task.hearts or [],
        "is_rendered_as_separator": task.is_rendered_as_separator or False,
        "liked": task.liked or False,
        "likes": task.likes or [],
        "memberships": task.memberships or [],
        "modified_at": task.modified_at,
        "notes": task.notes,
        "num_hearts": task.num_hearts or 0,
        "num_likes": task.num_likes or 0,
        "num_subtasks": task.num_subtasks or 0,
        "start_at": task.start_at,
        "start_on": task.start_on,
        "actual_time_minutes": task.actual_time_minutes,
        # Reference fields — now serialized as nested compact objects
        "assignee": assignee_value,
        "assignee_section": assignee_section_value,
        "assigned_by": task.assigned_by,
        "custom_fields": task.custom_fields or [],
        "custom_type": task.custom_type,
        "custom_type_status_option": task.custom_type_status_option,
        "dependencies": task.dependencies or [],
        "dependents": task.dependents or [],
        "followers": task.followers or [],
        "parent": parent_value,
        "projects": projects_value,
        "tags": tags_value,
        "workspace": workspace_value,
        "permalink_url": task.permalink_url,
    }
    return result


def serialize_task_list(
    tasks: list[AsanaTask],
    next_page: str | None = None,
) -> dict[str, Any]:
    """Collection envelope matching Asana's paginated response shape."""
    result: dict[str, Any] = {
        "data": [serialize_task_compact(task) for task in tasks],
    }
    if next_page is not None:
        result["next_page"] = {
            "offset": next_page,
            "path": None,
            "uri": None,
        }
    else:
        result["next_page"] = None
    return result
