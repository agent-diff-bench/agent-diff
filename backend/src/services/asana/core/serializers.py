"""Serialization helpers for the Asana API replica.

Each serialize function converts an ORM model into a dict matching the
source API's response shape. Functions are added one at a time during the
resource implementation loop.

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its serializer functions to this file incrementally.
"""

from __future__ import annotations

from typing import Any, Optional

from ..database.schema import AsanaProject, AsanaSection, AsanaStory, AsanaTag, AsanaTask, AsanaTeam, AsanaUser, AsanaWorkspace


def _compact_or_none(ref_obj, resource_type: str) -> Optional[dict[str, Any]]:
    """Serialize an ORM relationship object to a compact dict, or None."""
    if ref_obj is None:
        return None
    return {
        "gid": ref_obj.gid,
        "resource_type": resource_type,
        "name": getattr(ref_obj, "name", None),
    }


def _gid_compact(gid: Optional[str], resource_type: str) -> Optional[dict[str, Any]]:
    """Build a compact ref from a raw GID string, or None."""
    if gid is None:
        return None
    return {"gid": gid, "resource_type": resource_type}


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

def serialize_project(project: AsanaProject) -> dict[str, Any]:
    """Full ProjectResponse shape."""
    result: dict[str, Any] = {
        "gid": project.gid,
        "resource_type": project.resource_type or "project",
        "name": project.name,
        "archived": project.archived,
        "color": project.color,
        "icon": project.icon,
        "created_at": project.created_at,
        "current_status": project.current_status,
        "current_status_update": project.current_status_update,
        "custom_field_settings": project.custom_field_settings or [],
        "custom_fields": project.custom_fields or [],
        "default_view": project.default_view,
        "due_date": project.due_date,
        "due_on": project.due_on,
        "html_notes": project.html_notes,
        "members": project.members or [],
        "modified_at": project.modified_at,
        "notes": project.notes,
        "public": project.public,
        "privacy_setting": project.privacy_setting,
        "start_on": project.start_on,
        "default_access_level": project.default_access_level,
        "minimum_access_level_for_customization": project.minimum_access_level_for_customization,
        "minimum_access_level_for_sharing": project.minimum_access_level_for_sharing,
        "completed": project.completed,
        "completed_at": project.completed_at,
        "completed_by": _compact_or_none(project.completed_by_ref, "user"),
        "followers": project.followers or [],
        "owner": _compact_or_none(project.owner_ref, "user"),
        "team": _compact_or_none(project.team_ref, "team"),
        "workspace": _compact_or_none(project.workspace_ref, "workspace"),
        "permalink_url": project.permalink_url,
        "project_brief": project.project_brief,
        "created_from_template": project.created_from_template,
    }
    return result


def serialize_project_compact(project: AsanaProject) -> dict[str, Any]:
    """ProjectCompact shape for collection endpoints."""
    return {
        "gid": project.gid,
        "resource_type": project.resource_type or "project",
        "name": project.name,
    }


def serialize_project_list(
    projects: list[AsanaProject],
    next_cursor: Optional[str] = None,
) -> dict[str, Any]:
    """Paginated collection envelope."""
    result: dict[str, Any] = {
        "data": [serialize_project_compact(project) for project in projects],
    }
    if next_cursor is not None:
        result["next_page"] = {"offset": next_cursor}
    else:
        result["next_page"] = None
    return result


def serialize_task_compact(task: AsanaTask) -> dict[str, Any]:
    """TaskCompact shape for collection endpoints."""
    return {
        "gid": task.gid,
        "resource_type": task.resource_type or "task",
        "name": task.name,
        "resource_subtype": task.resource_subtype or "default_task",
    }


def serialize_task(task: AsanaTask) -> dict[str, Any]:
    """Full TaskResponse shape."""
    result: dict[str, Any] = {
        "gid": task.gid,
        "resource_type": task.resource_type or "task",
        "name": task.name,
        "resource_subtype": task.resource_subtype or "default_task",
        "created_by": task.created_by,
        "approval_status": task.approval_status,
        "assignee_status": task.assignee_status,
        "assignee": _compact_or_none(task.assignee_ref, "user") if hasattr(task, "assignee_ref") and task.assignee_ref else _gid_compact(task.assignee_gid, "user"),
        "assignee_section": _compact_or_none(task.assignee_section_ref, "section") if hasattr(task, "assignee_section_ref") and task.assignee_section_ref else _gid_compact(task.assignee_section_gid, "section"),
        "assigned_by": _compact_or_none(task.assigned_by_ref, "user") if hasattr(task, "assigned_by_ref") and task.assigned_by_ref else _gid_compact(task.assigned_by_gid, "user"),
        "completed": task.completed,
        "completed_at": task.completed_at,
        "completed_by": _compact_or_none(task.completed_by_ref, "user") if hasattr(task, "completed_by_ref") and task.completed_by_ref else _gid_compact(task.completed_by_gid, "user"),
        "created_at": task.created_at,
        "dependencies": task.dependencies or [],
        "dependents": task.dependents or [],
        "due_at": task.due_at,
        "due_on": task.due_on,
        "external": task.external,
        "html_notes": task.html_notes,
        "hearted": task.hearted,
        "hearts": task.hearts or [],
        "is_rendered_as_separator": task.is_rendered_as_separator,
        "liked": task.liked,
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
        "custom_fields": task.custom_fields or [],
        "custom_type": _gid_compact(task.custom_type_gid, "custom_type"),
        "custom_type_status_option": _gid_compact(task.custom_type_status_option_gid, "custom_type_status_option"),
        "followers": task.followers or [],
        "parent": _compact_or_none(task.parent, "task") if hasattr(task, "parent") and task.parent else _gid_compact(task.parent_gid, "task"),
        "projects": [
            serialize_project_compact(project) for project in task.projects
        ] if task.projects else [],
        "tags": [
            serialize_tag_compact(tag) for tag in task.tags
        ] if task.tags else [],
        "workspace": _compact_or_none(task.workspace_ref, "workspace") if hasattr(task, "workspace_ref") and task.workspace_ref else _gid_compact(task.workspace_gid, "workspace"),
        "permalink_url": task.permalink_url,
    }
    return result


def serialize_task_list(
    tasks: list[AsanaTask],
    next_cursor: Optional[str] = None,
) -> dict[str, Any]:
    """Paginated collection envelope."""
    result: dict[str, Any] = {
        "data": [serialize_task_compact(task) for task in tasks],
    }
    if next_cursor is not None:
        result["next_page"] = {"offset": next_cursor}
    else:
        result["next_page"] = None
    return result


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def serialize_section(section: AsanaSection) -> dict[str, Any]:
    """Full SectionResponse shape."""
    project_compact = _compact_or_none(section.project, "project")
    return {
        "gid": section.gid,
        "resource_type": section.resource_type or "section",
        "name": section.name,
        "created_at": section.created_at,
        "project": project_compact,
        "projects": [project_compact] if project_compact else [],
    }


def serialize_section_compact(section: AsanaSection) -> dict[str, Any]:
    """SectionCompact shape for collection endpoints."""
    return {
        "gid": section.gid,
        "resource_type": section.resource_type or "section",
        "name": section.name,
    }


def serialize_section_list(
    sections: list[AsanaSection],
    next_cursor: Optional[str] = None,
) -> dict[str, Any]:
    """Paginated collection envelope."""
    result: dict[str, Any] = {
        "data": [serialize_section_compact(section) for section in sections],
    }
    if next_cursor is not None:
        result["next_page"] = {"offset": next_cursor}
    else:
        result["next_page"] = None
    return result


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------

def serialize_tag(tag: AsanaTag) -> dict[str, Any]:
    """Full TagResponse shape."""
    return {
        "gid": tag.gid,
        "resource_type": tag.resource_type or "tag",
        "name": tag.name,
        "color": tag.color,
        "notes": tag.notes,
        "created_at": tag.created_at,
        "followers": tag.followers or [],
        "workspace": _compact_or_none(tag.workspace_ref, "workspace"),
        "permalink_url": tag.permalink_url,
    }


def serialize_tag_compact(tag: AsanaTag) -> dict[str, Any]:
    """TagCompact shape for collection endpoints."""
    return {
        "gid": tag.gid,
        "resource_type": tag.resource_type or "tag",
        "name": tag.name,
    }


def serialize_tag_list(
    tags: list[AsanaTag],
    next_cursor: Optional[str] = None,
) -> dict[str, Any]:
    """Paginated collection envelope."""
    result: dict[str, Any] = {
        "data": [serialize_tag_compact(tag) for tag in tags],
    }
    if next_cursor is not None:
        result["next_page"] = {"offset": next_cursor}
    else:
        result["next_page"] = None
    return result


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------

def serialize_team(team: AsanaTeam) -> dict[str, Any]:
    """Full TeamResponse shape."""
    return {
        "gid": team.gid,
        "resource_type": team.resource_type or "team",
        "name": team.name,
        "description": team.description,
        "html_description": team.html_description,
        "organization": _compact_or_none(team.organization_ref, "workspace") if hasattr(team, "organization_ref") and team.organization_ref else _gid_compact(team.organization_gid, "workspace"),
        "permalink_url": team.permalink_url,
        "visibility": team.visibility,
        "edit_team_name_or_description_access_level": team.edit_team_name_or_description_access_level,
        "edit_team_visibility_or_trash_team_access_level": team.edit_team_visibility_or_trash_team_access_level,
        "member_invite_management_access_level": team.member_invite_management_access_level,
        "guest_invite_management_access_level": team.guest_invite_management_access_level,
        "join_request_management_access_level": team.join_request_management_access_level,
        "team_member_removal_access_level": team.team_member_removal_access_level,
        "team_content_management_access_level": team.team_content_management_access_level,
        "endorsed": team.endorsed,
        "custom_field_settings": team.custom_field_settings or [],
    }


def serialize_team_compact(team: AsanaTeam) -> dict[str, Any]:
    """TeamCompact shape for collection endpoints."""
    return {
        "gid": team.gid,
        "resource_type": team.resource_type or "team",
        "name": team.name,
    }


def serialize_team_list(
    teams: list[AsanaTeam],
    next_cursor: Optional[str] = None,
) -> dict[str, Any]:
    """Paginated collection envelope."""
    result: dict[str, Any] = {
        "data": [serialize_team_compact(team) for team in teams],
    }
    if next_cursor is not None:
        result["next_page"] = {"offset": next_cursor}
    else:
        result["next_page"] = None
    return result


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def serialize_user(user: AsanaUser) -> dict[str, Any]:
    """Full UserResponse shape."""
    # Prefer workspace relationship objects when loaded, fall back to JSONB
    if hasattr(user, "workspace_refs") and user.workspace_refs:
        workspaces = [
            _compact_or_none(workspace, "workspace")
            for workspace in user.workspace_refs
        ]
    else:
        workspaces = user.workspaces or []
    return {
        "gid": user.gid,
        "resource_type": user.resource_type or "user",
        "name": user.name,
        "email": user.email,
        "photo": user.photo,
        "workspaces": workspaces,
        "custom_fields": user.custom_fields or [],
    }


def serialize_user_compact(user: AsanaUser) -> dict[str, Any]:
    """UserCompact shape for collection endpoints."""
    return {
        "gid": user.gid,
        "resource_type": user.resource_type or "user",
        "name": user.name,
    }


def serialize_user_list(
    users: list[AsanaUser],
    next_cursor: Optional[str] = None,
) -> dict[str, Any]:
    """Paginated collection envelope."""
    result: dict[str, Any] = {
        "data": [serialize_user_compact(user) for user in users],
    }
    if next_cursor is not None:
        result["next_page"] = {"offset": next_cursor}
    else:
        result["next_page"] = None
    return result


# ---------------------------------------------------------------------------
# Workspaces
# ---------------------------------------------------------------------------

def serialize_workspace(workspace: AsanaWorkspace) -> dict[str, Any]:
    """Full WorkspaceResponse shape."""
    return {
        "gid": workspace.gid,
        "resource_type": workspace.resource_type or "workspace",
        "name": workspace.name,
        "email_domains": workspace.email_domains or [],
        "is_organization": workspace.is_organization,
    }


def serialize_workspace_compact(workspace: AsanaWorkspace) -> dict[str, Any]:
    """WorkspaceCompact shape for collection endpoints."""
    return {
        "gid": workspace.gid,
        "resource_type": workspace.resource_type or "workspace",
        "name": workspace.name,
    }


def serialize_workspace_list(
    workspaces: list[AsanaWorkspace],
    next_cursor: Optional[str] = None,
) -> dict[str, Any]:
    """Paginated collection envelope."""
    result: dict[str, Any] = {
        "data": [serialize_workspace_compact(workspace) for workspace in workspaces],
    }
    if next_cursor is not None:
        result["next_page"] = {"offset": next_cursor}
    else:
        result["next_page"] = None
    return result


# ---------------------------------------------------------------------------
# Stories
# ---------------------------------------------------------------------------

def serialize_story(story: AsanaStory) -> dict[str, Any]:
    """Full StoryResponse shape."""
    result: dict[str, Any] = {
        "gid": story.gid,
        "resource_type": story.resource_type or "story",
        "created_at": story.created_at,
        "created_by": _compact_or_none(story.created_by_ref, "user"),
        "resource_subtype": story.resource_subtype,
        "text": story.text,
        "html_text": story.html_text,
        "is_pinned": story.is_pinned,
        "sticker_name": story.sticker_name,
        "type": story.type,
        "is_editable": story.is_editable,
        "is_edited": story.is_edited,
        "hearted": story.hearted,
        "hearts": story.hearts or [],
        "num_hearts": story.num_hearts or 0,
        "liked": story.liked,
        "likes": story.likes or [],
        "num_likes": story.num_likes or 0,
        "reaction_summary": story.reaction_summary or [],
        "previews": story.previews or [],
        "source": story.source,
        "old_name": story.old_name,
        "new_name": story.new_name,
        "old_resource_subtype": story.old_resource_subtype,
        "new_resource_subtype": story.new_resource_subtype,
        "old_text_value": story.old_text_value,
        "new_text_value": story.new_text_value,
        "old_number_value": story.old_number_value,
        "new_number_value": story.new_number_value,
        "old_approval_status": story.old_approval_status,
        "new_approval_status": story.new_approval_status,
        "old_dates": story.old_dates,
        "new_dates": story.new_dates,
        "old_date_value": story.old_date_value,
        "new_date_value": story.new_date_value,
        "old_enum_value": story.old_enum_value,
        "new_enum_value": story.new_enum_value,
        "old_multi_enum_values": story.old_multi_enum_values,
        "new_multi_enum_values": story.new_multi_enum_values,
        "old_people_value": story.old_people_value,
        "new_people_value": story.new_people_value,
        # Conditional references — use relationship objects where available
        "story": _compact_or_none(story.parent_story, "story"),
        "assignee": _compact_or_none(story.assignee_ref, "user"),
        "follower": _compact_or_none(story.follower_ref, "user"),
        "old_section": _compact_or_none(story.old_section_ref, "section"),
        "new_section": _compact_or_none(story.new_section_ref, "section"),
        "task": _compact_or_none(story.task_ref, "task"),
        "project": _compact_or_none(story.project, "project"),
        "tag": _compact_or_none(story.tag_ref, "tag"),
        "custom_field": _gid_compact(story.custom_field_gid, "custom_field"),
        "duplicate_of": _compact_or_none(story.duplicate_of_ref, "task"),
        "duplicated_from": _compact_or_none(story.duplicated_from_ref, "task"),
        "dependency": _compact_or_none(story.dependency_ref, "task"),
        "target": _gid_compact(story.target_gid, "task"),
    }
    return result


def serialize_story_compact(story: AsanaStory) -> dict[str, Any]:
    """StoryCompact shape for collection endpoints."""
    return {
        "gid": story.gid,
        "resource_type": story.resource_type or "story",
        "created_at": story.created_at,
        "created_by": _compact_or_none(story.created_by_ref, "user") if story.created_by_ref else _gid_compact(story.created_by_gid, "user"),
        "resource_subtype": story.resource_subtype,
        "text": story.text,
    }


def serialize_story_list(
    stories: list[AsanaStory],
    next_cursor: Optional[str] = None,
) -> dict[str, Any]:
    """Paginated collection envelope."""
    result: dict[str, Any] = {
        "data": [serialize_story_compact(story) for story in stories],
    }
    if next_cursor is not None:
        result["next_page"] = {"offset": next_cursor}
    else:
        result["next_page"] = None
    return result
