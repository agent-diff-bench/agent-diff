"""Asana REST API routes.

Mounted under /api/env/{env_id}/services/__SERVICE_MOUNT_NAME__
DB session comes from request.state.db_session (IsolationMiddleware).
User impersonation comes from request.state.impersonate_user_id.

Route handlers and route entries are added one at a time during the resource
implementation loop. The request helpers below are universal.
"""

from __future__ import annotations

from typing import Any

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from ..core.errors import (
    AppAPIError,
    bad_request,
    handle_exception,
    not_found,
    unauthorized,
)
from ..core.serializers import (
    serialize_project,
    serialize_project_compact,
    serialize_project_list,
    serialize_section,
    serialize_section_list,
    serialize_story,
    serialize_story_list,
    serialize_tag,
    serialize_tag_compact,
    serialize_tag_list,
    serialize_task,
    serialize_task_compact,
    serialize_task_list,
    serialize_team,
    serialize_team_compact,
    serialize_team_list,
    serialize_user,
    serialize_user_compact,
    serialize_user_list,
    serialize_workspace,
    serialize_workspace_compact,
    serialize_workspace_list,
)
from ..database import operations as ops


# ---------------------------------------------------------------------------
# Request helpers — universal across apps
# ---------------------------------------------------------------------------


def _session(request: Request) -> Session:
    """Get the environment-scoped DB session from request.state."""
    session = getattr(request.state, "db_session", None)
    if session is None:
        raise unauthorized("Missing database session")
    return session


def _principal_user_id(request: Request) -> str:
    """Resolve the acting principal from request state."""
    principal = getattr(request.state, "impersonate_user_id", None)
    if principal is not None and str(principal).strip() != "":
        return str(principal)
    raise unauthorized("Missing user authentication")


async def _parse_json_body(request: Request) -> dict[str, Any]:
    """Parse JSON body. Raises app-shaped bad_request on malformed input."""
    try:
        return await request.json()
    except Exception as exc:
        raise bad_request(f"Invalid JSON body: {exc}") from exc


def _pagination_params(request: Request) -> tuple[str | None, int]:
    """Extract cursor and limit from query params (cursor-based pagination)."""
    cursor = request.query_params.get("cursor")
    limit_str = request.query_params.get("limit")
    limit = 50
    if limit_str is not None:
        try:
            limit = max(1, min(200, int(limit_str)))
        except ValueError:
            pass
    return cursor, limit


# ---------------------------------------------------------------------------
# Endpoint handlers — added per entity by entity scaffold
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------


async def create_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not data.get("name"):
            raise bad_request("name: Missing input")
        project = ops.create_project(session, data)
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_projects(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        workspace = request.query_params.get("workspace")
        team_param = request.query_params.get("team")
        archived_param = request.query_params.get("archived")
        archived = None
        if archived_param is not None:
            archived = archived_param.lower() == "true"
        projects, next_cursor = ops.list_projects(
            session,
            workspace=workspace,
            team=team_param,
            archived=archived,
            cursor=cursor,
            limit=limit,
        )
        return JSONResponse(serialize_project_list(projects, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": serialize_project(project)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        project = ops.update_project(session, project_gid, data)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": serialize_project(project)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        deleted = ops.delete_project(session, project_gid)
        if not deleted:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def duplicate_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not data.get("name"):
            raise bad_request("name: Missing input")
        new_project = ops.duplicate_project(session, project_gid, data)
        if new_project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        # Async operation — return a job-like response
        job = {
            "gid": new_project.gid,
            "resource_type": "job",
            "resource_subtype": "duplicate_project",
            "status": "succeeded",
            "new_project": {
                "gid": new_project.gid,
                "resource_type": "project",
                "name": new_project.name,
            },
        }
        return JSONResponse({"data": job}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_followers_to_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        followers_str = data.get("followers", "")
        if not followers_str:
            raise bad_request("followers: Missing input")
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        new_follower_gids = [gid.strip() for gid in followers_str.split(",") if gid.strip()]
        existing = project.followers or []
        existing_gids = {f["gid"] if isinstance(f, dict) else f for f in existing}
        for gid in new_follower_gids:
            if gid not in existing_gids:
                existing.append({"gid": gid, "resource_type": "user"})
        project.followers = list(existing)
        project.modified_at = ops.now_iso()
        flag_modified(project, "followers")
        session.flush()
        return JSONResponse({"data": serialize_project(project)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_followers_from_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        followers_str = data.get("followers", "")
        if not followers_str:
            raise bad_request("followers: Missing input")
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        remove_gids = {gid.strip() for gid in followers_str.split(",") if gid.strip()}
        existing = project.followers or []
        project.followers = [
            f for f in existing
            if (f["gid"] if isinstance(f, dict) else f) not in remove_gids
        ]
        project.modified_at = ops.now_iso()
        flag_modified(project, "followers")
        session.flush()
        return JSONResponse({"data": serialize_project(project)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_members_to_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        members_str = data.get("members", "")
        if not members_str:
            raise bad_request("members: Missing input")
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        new_member_gids = [gid.strip() for gid in members_str.split(",") if gid.strip()]
        existing = project.members or []
        existing_gids = {m["gid"] if isinstance(m, dict) else m for m in existing}
        for gid in new_member_gids:
            if gid not in existing_gids:
                existing.append({"gid": gid, "resource_type": "user"})
        project.members = list(existing)
        project.modified_at = ops.now_iso()
        flag_modified(project, "members")
        session.flush()
        return JSONResponse({"data": serialize_project(project)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_members_from_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        members_str = data.get("members", "")
        if not members_str:
            raise bad_request("members: Missing input")
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        remove_gids = {gid.strip() for gid in members_str.split(",") if gid.strip()}
        existing = project.members or []
        project.members = [
            m for m in existing
            if (m["gid"] if isinstance(m, dict) else m) not in remove_gids
        ]
        project.modified_at = ops.now_iso()
        flag_modified(project, "members")
        session.flush()
        return JSONResponse({"data": serialize_project(project)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_custom_field_setting_to_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        custom_field = data.get("custom_field")
        if not custom_field:
            raise bad_request("custom_field: Missing input")
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        is_important = data.get("is_important", False)
        # Build a custom field setting entry
        custom_field_gid = custom_field if isinstance(custom_field, str) else custom_field.get("gid", "")
        setting = {
            "gid": ops.generate_id("project"),
            "resource_type": "custom_field_setting",
            "is_important": is_important,
            "custom_field": {"gid": custom_field_gid, "resource_type": "custom_field"},
            "project": {"gid": project.gid, "resource_type": "project", "name": project.name},
            "parent": {"gid": project.gid, "resource_type": "project", "name": project.name},
        }
        settings = list(project.custom_field_settings or [])
        settings.append(setting)
        project.custom_field_settings = settings
        project.modified_at = ops.now_iso()
        flag_modified(project, "custom_field_settings")
        session.flush()
        return JSONResponse({"data": setting})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_custom_field_setting_from_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        custom_field_gid = data.get("custom_field")
        if not custom_field_gid:
            raise bad_request("custom_field: Missing input")
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        settings = project.custom_field_settings or []
        project.custom_field_settings = [
            setting for setting in settings
            if setting.get("custom_field", {}).get("gid") != custom_field_gid
        ]
        project.modified_at = ops.now_iso()
        flag_modified(project, "custom_field_settings")
        session.flush()
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_custom_field_settings_for_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        settings = project.custom_field_settings or []
        return JSONResponse({"data": settings, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_memberships(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        # Build membership entries from the members list
        memberships = []
        for member in (project.members or []):
            member_gid = member["gid"] if isinstance(member, dict) else member
            memberships.append({
                "gid": member_gid,
                "resource_type": "project_membership",
                "member": {"gid": member_gid, "resource_type": "user"},
                "access_level": "editor",
            })
        return JSONResponse({"data": memberships, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_portfolio_settings(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        # No portfolio settings stored yet — return empty list
        return JSONResponse({"data": [], "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_statuses(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        # Statuses stored inline in current_status; return as list if present
        statuses = []
        if project.current_status is not None:
            statuses.append(project.current_status)
        return JSONResponse({"data": statuses, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project_status(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        timestamp = ops.now_iso()
        user_gid = _principal_user_id(request)
        user_compact = {"gid": user_gid, "resource_type": "user", "name": None}
        status_entry = {
            "gid": ops.generate_id("project"),
            "resource_type": "project_status",
            "title": data.get("title", ""),
            "text": data.get("text", ""),
            "html_text": data.get("html_text"),
            "color": data.get("color", "green"),
            "author": user_compact,
            "created_by": user_compact,
            "created_at": timestamp,
            "modified_at": timestamp,
        }
        project.current_status = status_entry
        project.modified_at = timestamp
        session.flush()
        return JSONResponse({"data": status_entry}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_task_counts_for_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        # Placeholder counts — real counts require task association (Pass 2)
        counts = {
            "num_tasks": 0,
            "num_incomplete_tasks": 0,
            "num_completed_tasks": 0,
            "num_milestones": 0,
            "num_incomplete_milestones": 0,
            "num_completed_milestones": 0,
        }
        return JSONResponse({"data": counts})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_projects_for_task(request: Request) -> JSONResponse:
    """GET /tasks/{task_gid}/projects — returns projects a task belongs to."""
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        projects = ops.list_projects_for_task(session, task_gid)
        return JSONResponse({
            "data": [serialize_project_compact(project) for project in projects],
            "next_page": None,
        })
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks_for_project(request: Request) -> JSONResponse:
    """GET /projects/{project_gid}/tasks — returns tasks in a project."""
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        tasks = ops.list_tasks_for_project(session, project_gid)
        return JSONResponse({
            "data": [serialize_task_compact(task) for task in tasks],
            "next_page": None,
        })
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_projects_for_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        if ops.get_team(session, team_gid) is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        cursor, limit = _pagination_params(request)
        archived_param = request.query_params.get("archived")
        archived = None
        if archived_param is not None:
            archived = archived_param.lower() == "true"
        projects, next_cursor = ops.list_projects(
            session, team=team_gid, archived=archived, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_project_list(projects, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_projects_for_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        if ops.get_workspace(session, workspace_gid) is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        cursor, limit = _pagination_params(request)
        archived_param = request.query_params.get("archived")
        archived = None
        if archived_param is not None:
            archived = archived_param.lower() == "true"
        projects, next_cursor = ops.list_projects(
            session, workspace=workspace_gid, archived=archived, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_project_list(projects, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def search_projects_in_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        if ops.get_workspace(session, workspace_gid) is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        cursor, limit = _pagination_params(request)
        projects, _ = ops.list_projects(
            session, workspace=workspace_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse({"data": [serialize_project_compact(project) for project in projects]})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project_in_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        if ops.get_team(session, team_gid) is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not data.get("name"):
            raise bad_request("name: Missing input")
        data["team"] = team_gid
        project = ops.create_project(session, data)
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project_in_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        if ops.get_workspace(session, workspace_gid) is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not data.get("name"):
            raise bad_request("name: Missing input")
        data["workspace"] = workspace_gid
        project = ops.create_project(session, data)
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def save_project_as_template(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not data.get("name"):
            raise bad_request("name: Missing input")
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        template_gid = ops.generate_id("project")
        job = {
            "gid": template_gid,
            "resource_type": "job",
            "resource_subtype": "save_project_as_template",
            "status": "succeeded",
            "new_project_template": {
                "gid": template_gid,
                "resource_type": "project_template",
                "name": data["name"],
            },
        }
        return JSONResponse({"data": job}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project_brief(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        brief_gid = ops.generate_id("project")
        project.project_brief = brief_gid
        project.modified_at = ops.now_iso()
        session.flush()
        brief = {
            "gid": brief_gid,
            "resource_type": "project_brief",
            "title": data.get("title", ""),
            "html_text": data.get("html_text"),
            "text": data.get("text"),
            "permalink_url": f"https://app.asana.com/0/{project.gid}/{brief_gid}",
            "project": {
                "gid": project.gid,
                "resource_type": "project",
                "name": project.name,
            },
        }
        return JSONResponse({"data": brief}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


async def create_section_in_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not data.get("name"):
            raise bad_request("name: Missing input")
        section = ops.create_section(session, project_gid, data)
        return JSONResponse({"data": serialize_section(section)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_sections_for_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        cursor, limit = _pagination_params(request)
        sections, next_cursor = ops.list_sections_for_project(
            session, project_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_section_list(sections, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_section(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        section_gid = request.path_params["section_gid"]
        section = ops.get_section(session, section_gid)
        if section is None:
            raise not_found(f"section: Unknown object: {section_gid}")
        return JSONResponse({"data": serialize_section(section)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_section(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        section_gid = request.path_params["section_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        section = ops.update_section(session, section_gid, data)
        if section is None:
            raise not_found(f"section: Unknown object: {section_gid}")
        return JSONResponse({"data": serialize_section(section)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_section(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        section_gid = request.path_params["section_gid"]
        deleted = ops.delete_section(session, section_gid)
        if not deleted:
            raise not_found(f"section: Unknown object: {section_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def insert_section_in_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        body = await _parse_json_body(request)
        data = body.get("data", {})
        section_gid = data.get("section")
        if not section_gid:
            raise bad_request("section: Missing input")
        success = ops.insert_section_in_project(
            session,
            project_gid,
            section_gid,
            before_section=data.get("before_section"),
            after_section=data.get("after_section"),
        )
        if not success:
            raise not_found(f"section: Unknown object: {section_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_task_to_section(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        section_gid = request.path_params["section_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        task_gid = data.get("task")
        if not task_gid:
            raise bad_request("task: Missing input")
        success = ops.add_task_to_section(
            session,
            section_gid,
            task_gid,
            insert_before=data.get("insert_before"),
            insert_after=data.get("insert_after"),
        )
        if not success:
            raise not_found(f"section: Unknown object: {section_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------


async def create_tag_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        body = await _parse_json_body(request)
        data = body.get("data", {})
        tag = ops.create_tag(session, data)
        return JSONResponse({"data": serialize_tag(tag)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tags(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        workspace = request.query_params.get("workspace")
        tags, next_cursor = ops.list_tags(
            session, workspace=workspace, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_tag_list(tags, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tag(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        tag_gid = request.path_params["tag_gid"]
        tag = ops.get_tag(session, tag_gid)
        if tag is None:
            raise not_found(f"tag: Unknown object: {tag_gid}")
        return JSONResponse({"data": serialize_tag(tag)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_tag(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        tag_gid = request.path_params["tag_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        tag = ops.update_tag(session, tag_gid, data)
        if tag is None:
            raise not_found(f"tag: Unknown object: {tag_gid}")
        return JSONResponse({"data": serialize_tag(tag)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_tag(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        tag_gid = request.path_params["tag_gid"]
        deleted = ops.delete_tag(session, tag_gid)
        if not deleted:
            raise not_found(f"tag: Unknown object: {tag_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tags_for_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        tags = ops.list_tags_for_task(session, task_gid)
        return JSONResponse({
            "data": [serialize_tag_compact(tag) for tag in tags],
            "next_page": None,
        })
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tags_for_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        cursor, limit = _pagination_params(request)
        tags, next_cursor = ops.list_tags(
            session, workspace=workspace_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_tag_list(tags, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_tag_in_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        data["workspace"] = workspace_gid
        tag = ops.create_tag(session, data)
        return JSONResponse({"data": serialize_tag(tag)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks_for_tag(request: Request) -> JSONResponse:
    """GET /tags/{tag_gid}/tasks — returns tasks linked to a tag."""
    try:
        session = _session(request)
        tag_gid = request.path_params["tag_gid"]
        tag = ops.get_tag(session, tag_gid)
        if tag is None:
            raise not_found(f"tag: Unknown object: {tag_gid}")
        tasks = ops.list_tasks_for_tag(session, tag_gid)
        return JSONResponse({
            "data": [serialize_task_compact(task) for task in tasks],
            "next_page": None,
        })
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_tag_to_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_gid}/addTag — link a tag to a task."""
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        if ops.get_task(session, task_gid) is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        body = await _parse_json_body(request)
        data = body.get("data", {})
        tag_gid = data.get("tag")
        if not tag_gid:
            raise bad_request("tag: Missing input")
        ops.add_tag_to_task(session, task_gid, tag_gid)
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_tag_from_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_gid}/removeTag — unlink a tag from a task."""
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        if ops.get_task(session, task_gid) is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        body = await _parse_json_body(request)
        data = body.get("data", {})
        tag_gid = data.get("tag")
        if not tag_gid:
            raise bad_request("tag: Missing input")
        ops.remove_tag_from_task(session, task_gid, tag_gid)
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Stories
# ---------------------------------------------------------------------------


async def get_story(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        story_gid = request.path_params["story_gid"]
        story = ops.get_story(session, story_gid)
        if story is None:
            raise not_found(f"story: Unknown object: {story_gid}")
        return JSONResponse({"data": serialize_story(story)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_story(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        story_gid = request.path_params["story_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        story = ops.update_story(session, story_gid, data)
        if story is None:
            raise not_found(f"story: Unknown object: {story_gid}")
        return JSONResponse({"data": serialize_story(story)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_story(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        story_gid = request.path_params["story_gid"]
        deleted = ops.delete_story(session, story_gid)
        if not deleted:
            raise not_found(f"story: Unknown object: {story_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_stories_for_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        cursor, limit = _pagination_params(request)
        stories, next_cursor = ops.list_stories_for_task(
            session, task_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_story_list(stories, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_story_on_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        story = ops.create_story(session, data, target_gid=task_gid)
        return JSONResponse({"data": serialize_story(story)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_stories_for_goal(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        goal_gid = request.path_params["goal_gid"]
        cursor, limit = _pagination_params(request)
        stories, next_cursor = ops.list_stories_for_goal(
            session, goal_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_story_list(stories, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_story_on_goal(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        goal_gid = request.path_params["goal_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        story = ops.create_story(session, data, target_gid=goal_gid)
        return JSONResponse({"data": serialize_story(story)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------


async def create_team_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        body = await _parse_json_body(request)
        data = body.get("data", {})
        team = ops.create_team(session, data)
        return JSONResponse({"data": serialize_team(team)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_team_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        team = ops.get_team(session, team_gid)
        if team is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        return JSONResponse({"data": serialize_team(team)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_team_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        team = ops.update_team(session, team_gid, data)
        if team is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        return JSONResponse({"data": serialize_team(team)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_teams_for_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        cursor, limit = _pagination_params(request)
        teams, next_cursor = ops.list_teams_for_workspace(
            session, workspace_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_team_list(teams, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_teams_for_user(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_gid = request.path_params["user_gid"]
        organization = request.query_params.get("organization")
        cursor, limit = _pagination_params(request)
        teams, next_cursor = ops.list_teams_for_user(
            session, user_gid, organization=organization, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_team_list(teams, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_user_to_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        user_gid = data.get("user")
        if not user_gid:
            raise bad_request("user: Missing input")
        team = ops.add_user_to_team(session, team_gid, user_gid)
        if team is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        # Return a team membership response
        membership = {
            "gid": ops.generate_id("team_membership"),
            "resource_type": "team_membership",
            "user": {"gid": user_gid, "resource_type": "user"},
            "team": serialize_team_compact(team),
            "is_guest": False,
            "is_limited_access": False,
            "is_admin": False,
        }
        return JSONResponse({"data": membership})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_user_from_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        user_gid = data.get("user")
        if not user_gid:
            raise bad_request("user: Missing input")
        team = ops.remove_user_from_team(session, team_gid, user_gid)
        if team is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_team_memberships_for_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        team = ops.get_team(session, team_gid)
        if team is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        memberships = []
        for member in (team.members or []):
            member_gid = member["gid"] if isinstance(member, dict) else member
            memberships.append({
                "gid": member_gid,
                "resource_type": "team_membership",
                "user": {"gid": member_gid, "resource_type": "user"},
                "team": serialize_team_compact(team),
                "is_guest": False,
                "is_limited_access": False,
                "is_admin": False,
            })
        return JSONResponse({"data": memberships, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_custom_field_settings_for_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        team = ops.get_team(session, team_gid)
        if team is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        settings = team.custom_field_settings or []
        return JSONResponse({"data": settings, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_templates_for_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        team = ops.get_team(session, team_gid)
        if team is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        # Project templates are not a modeled resource; return empty list
        return JSONResponse({"data": [], "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------


async def get_users(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        workspace = request.query_params.get("workspace")
        users, next_cursor = ops.list_users(
            session, workspace=workspace, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_user_list(users, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_user(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_gid = request.path_params["user_gid"]
        user = ops.get_user(session, user_gid)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        return JSONResponse({"data": serialize_user(user)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_user(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_gid = request.path_params["user_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        user = ops.update_user(session, user_gid, data)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        return JSONResponse({"data": serialize_user(user)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_users_in_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        # Verify team exists before listing its members
        team = ops.get_team(session, team_gid)
        if team is None:
            raise not_found(f"team: Unknown object: {team_gid}")
        cursor, limit = _pagination_params(request)
        users, next_cursor = ops.list_users(
            session, team=team_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_user_list(users, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_user_to_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        user_gid = data.get("user")
        if not user_gid:
            raise bad_request("user: Missing input")
        user = ops.add_user_to_workspace(session, workspace_gid, user_gid)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        return JSONResponse({"data": serialize_user(user)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_user_from_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        user_gid = data.get("user")
        if not user_gid:
            raise bad_request("user: Missing input")
        user = ops.remove_user_from_workspace(session, workspace_gid, user_gid)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_users_in_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        # Verify workspace exists before listing its users
        workspace = ops.get_workspace(session, workspace_gid)
        if workspace is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        cursor, limit = _pagination_params(request)
        users, next_cursor = ops.list_users(
            session, workspace=workspace_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_user_list(users, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_user_in_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_gid = request.path_params["user_gid"]
        user = ops.get_user(session, user_gid)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        return JSONResponse({"data": serialize_user(user)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_user_in_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_gid = request.path_params["user_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        user = ops.update_user(session, user_gid, data)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        return JSONResponse({"data": serialize_user(user)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_user_favorites(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_gid = request.path_params["user_gid"]
        user = ops.get_user(session, user_gid)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        # Favorites are not a modeled resource; return empty list
        return JSONResponse({"data": [], "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_user_team_memberships(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_gid = request.path_params["user_gid"]
        user = ops.get_user(session, user_gid)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        workspace = request.query_params.get("workspace")
        # Build team memberships from teams that have this user as a member
        cursor, limit = _pagination_params(request)
        teams, _ = ops.list_teams_for_user(
            session, user_gid, organization=workspace, cursor=cursor, limit=limit,
        )
        memberships = []
        for team in teams:
            memberships.append({
                "gid": ops.generate_id("team_membership"),
                "resource_type": "team_membership",
                "user": serialize_user_compact(user),
                "team": serialize_team_compact(team),
                "is_guest": False,
                "is_limited_access": False,
                "is_admin": False,
            })
        return JSONResponse({"data": memberships, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_user_task_list(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_gid = request.path_params["user_gid"]
        user = ops.get_user(session, user_gid)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        # Synthesize a user task list from available data
        task_list_gid = ops.generate_id("user_task_list")
        workspace_compact = None
        # Prefer relationship objects (they carry the real name)
        if hasattr(user, "workspace_refs") and user.workspace_refs:
            first_workspace = user.workspace_refs[0]
            workspace_compact = {
                "gid": first_workspace.gid,
                "resource_type": "workspace",
                "name": first_workspace.name,
            }
        elif user.workspaces:
            first_workspace = user.workspaces[0]
            if isinstance(first_workspace, dict):
                workspace_compact = first_workspace
            else:
                workspace_compact = {"gid": first_workspace, "resource_type": "workspace"}
        workspace_name = (workspace_compact or {}).get("name") or "My Workspace"
        task_list = {
            "gid": task_list_gid,
            "resource_type": "user_task_list",
            "name": f"My tasks in {workspace_name}",
            "owner": serialize_user_compact(user),
            "workspace": workspace_compact,
        }
        return JSONResponse({"data": task_list})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_user_workspace_memberships(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_gid = request.path_params["user_gid"]
        user = ops.get_user(session, user_gid)
        if user is None:
            raise not_found(f"user: Unknown object: {user_gid}")
        # Build workspace memberships, preferring relationship objects
        memberships = []
        if hasattr(user, "workspace_refs") and user.workspace_refs:
            workspaces = [
                {"gid": workspace.gid, "resource_type": "workspace", "name": workspace.name}
                for workspace in user.workspace_refs
            ]
        else:
            workspaces = [
                workspace if isinstance(workspace, dict) else {"gid": workspace, "resource_type": "workspace"}
                for workspace in (user.workspaces or [])
            ]
        for workspace_compact in workspaces:
            memberships.append({
                "gid": ops.generate_id("workspace_membership"),
                "resource_type": "workspace_membership",
                "user": serialize_user_compact(user),
                "workspace": workspace_compact,
            })
        return JSONResponse({"data": memberships, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------


async def create_task_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        body = await _parse_json_body(request)
        data = body.get("data", {})
        task = ops.create_task(session, data)
        return JSONResponse({"data": serialize_task(task)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        assignee = request.query_params.get("assignee")
        project = request.query_params.get("project")
        section = request.query_params.get("section")
        workspace = request.query_params.get("workspace")
        completed_since = request.query_params.get("completed_since")
        modified_since = request.query_params.get("modified_since")
        tasks, next_cursor = ops.list_tasks(
            session,
            assignee=assignee,
            project=project,
            section=section,
            workspace=workspace,
            completed_since=completed_since,
            modified_since=modified_since,
            cursor=cursor,
            limit=limit,
        )
        return JSONResponse(serialize_task_list(tasks, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_task_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_task_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        task = ops.update_task(session, task_gid, data)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_task_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        deleted = ops.delete_task(session, task_gid)
        if not deleted:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_subtasks(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        cursor, limit = _pagination_params(request)
        subtasks, next_cursor = ops.list_subtasks(
            session, task_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_task_list(subtasks, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_subtask(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        parent = ops.get_task(session, task_gid)
        if parent is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        body = await _parse_json_body(request)
        data = body.get("data", {})
        task = ops.create_subtask(session, task_gid, data)
        return JSONResponse({"data": serialize_task(task)}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def set_task_parent(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        parent_gid = data.get("parent")
        task = ops.set_task_parent(session, task_gid, parent_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def duplicate_task_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        new_task = ops.duplicate_task(session, task_gid, data)
        if new_task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        job = {
            "gid": ops.generate_id("job"),
            "resource_type": "job",
            "resource_subtype": "duplicate_task",
            "status": "succeeded",
            "new_task": serialize_task_compact(new_task),
        }
        return JSONResponse({"data": job}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_followers_to_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        follower_gids = data.get("followers", [])
        if not follower_gids:
            raise bad_request("followers: Missing input")
        task = ops.add_task_followers(session, task_gid, follower_gids)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_followers_from_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        follower_gids = data.get("followers", [])
        if not follower_gids:
            raise bad_request("followers: Missing input")
        task = ops.remove_task_followers(session, task_gid, follower_gids)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_project_to_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        project_gid = data.get("project")
        if not project_gid:
            raise bad_request("project: Missing input")
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        ops.add_task_to_project(session, task_gid, project_gid)
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_project_from_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        project_gid = data.get("project")
        if not project_gid:
            raise bad_request("project: Missing input")
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        ops.remove_task_from_project(session, task_gid, project_gid)
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_dependencies_to_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        dependency_gids = data.get("dependencies", [])
        task = ops.add_task_dependencies(session, task_gid, dependency_gids)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_dependencies_from_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        dependency_gids = data.get("dependencies", [])
        task = ops.remove_task_dependencies(session, task_gid, dependency_gids)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_task_dependencies(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        dependencies = ops.get_task_dependencies(session, task_gid)
        if dependencies is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": dependencies, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_dependents_to_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        dependent_gids = data.get("dependents", [])
        task = ops.add_task_dependents(session, task_gid, dependent_gids)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_dependents_from_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        dependent_gids = data.get("dependents", [])
        task = ops.remove_task_dependents(session, task_gid, dependent_gids)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_task_dependents(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        dependents = ops.get_task_dependents(session, task_gid)
        if dependents is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": dependents, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks_for_section(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        section_gid = request.path_params["section_gid"]
        section = ops.get_section(session, section_gid)
        if section is None:
            raise not_found(f"section: Unknown object: {section_gid}")
        tasks = ops.list_tasks_for_section(session, section_gid)
        return JSONResponse({
            "data": [serialize_task_compact(task) for task in tasks],
            "next_page": None,
        })
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks_for_user_task_list(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        # user_task_list_gid is not a modeled entity; return empty list
        return JSONResponse({"data": [], "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_task_by_custom_id(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        custom_id = request.path_params["custom_id"]
        task = ops.get_task_by_custom_id(session, workspace_gid, custom_id)
        if task is None:
            raise not_found(f"task: No task found with custom_id: {custom_id}")
        return JSONResponse({"data": serialize_task(task)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def search_tasks_in_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        if ops.get_workspace(session, workspace_gid) is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        cursor, limit = _pagination_params(request)
        tasks, next_cursor = ops.search_tasks_in_workspace(
            session, workspace_gid, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_task_list(tasks, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_time_tracking_entries_for_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        entries = ops.get_time_tracking_entries(session, task_gid)
        if entries is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": entries, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_time_tracking_entry_for_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        entry = ops.create_time_tracking_entry(session, task_gid, data)
        if entry is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": entry}, status_code=status.HTTP_201_CREATED)
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Workspaces
# ---------------------------------------------------------------------------


async def get_workspaces(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        workspaces, next_cursor = ops.list_workspaces(
            session, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_workspace_list(workspaces, next_cursor))
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        workspace = ops.get_workspace(session, workspace_gid)
        if workspace is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        return JSONResponse({"data": serialize_workspace(workspace)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        workspace = ops.update_workspace(session, workspace_gid, data)
        if workspace is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        return JSONResponse({"data": serialize_workspace(workspace)})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_audit_log_events(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        workspace = ops.get_workspace(session, workspace_gid)
        if workspace is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        # Audit log events are not a modeled resource; return empty list
        return JSONResponse({"data": [], "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_workspace_custom_fields(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        workspace = ops.get_workspace(session, workspace_gid)
        if workspace is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        # Custom fields are not a modeled resource; return empty list
        return JSONResponse({"data": [], "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_workspace_events(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        workspace = ops.get_workspace(session, workspace_gid)
        if workspace is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        # Events are not a modeled resource; return empty list with sync token
        return JSONResponse({"data": [], "sync": "stub_sync_token", "has_more": False})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_workspace_typeahead(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        workspace = ops.get_workspace(session, workspace_gid)
        if workspace is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        # Typeahead is not a modeled resource; return empty list
        return JSONResponse({"data": []})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_workspace_memberships_for_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        workspace = ops.get_workspace(session, workspace_gid)
        if workspace is None:
            raise not_found(f"workspace: Unknown object: {workspace_gid}")
        # Build membership entries from the workspace's users association
        memberships = []
        for user in (workspace.users or []):
            memberships.append({
                "gid": ops.generate_id("workspace_membership"),
                "resource_type": "workspace_membership",
                "user": {
                    "gid": user.gid,
                    "resource_type": "user",
                    "name": user.name,
                },
                "workspace": serialize_workspace_compact(workspace),
            })
        return JSONResponse({"data": memberships, "next_page": None})
    except AppAPIError as error:
        return error.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Unknown-endpoint catch-all — universal across apps
# ---------------------------------------------------------------------------
#
# Any request whose path does not match a real route in the table below
# lands here. Returning the replica's native not-found envelope (via
# ``not_found().to_response()``) means agents calling unimplemented
# endpoints during development receive a response that is shape-compatible
# with the target API, instead of Starlette's default plain-text
# ``"Not Found"`` or — worse — an IsolationMiddleware 500.
#
# This makes the replica behave authentically even before every endpoint
# has been implemented: the agent cannot tell from the shape of a 404
# whether the endpoint is unimplemented or genuinely missing upstream.

async def unknown_endpoint(request: Request) -> JSONResponse:
    """Catch-all handler for requests that match no real route."""
    return not_found(
        f"Endpoint not found: {request.method} {request.url.path}"
    ).to_response()


# ---------------------------------------------------------------------------
# Route table — entries added per entity by entity scaffold
# ---------------------------------------------------------------------------

# AGENT INSTRUCTION: Add new Route entries ABOVE the catch-all at the
# bottom of this list. Two hard rules:
#
#   1. Fixed paths (e.g. /projects/archived) must come before parameterized
#      paths (e.g. /projects/{project_id}) so Starlette matches them first.
#   2. The ``/{_unknown_path:path}`` catch-all must always remain the LAST
#      entry in the list. Starlette matches in order, so any route placed
#      after it would be unreachable.

routes: list[Route] = [
    # --- Projects ---
    Route("/projects", create_project, methods=["POST"]),
    Route("/projects", get_projects, methods=["GET"]),
    Route("/projects/{project_gid}", get_project, methods=["GET"]),
    Route("/projects/{project_gid}", update_project, methods=["PUT"]),
    Route("/projects/{project_gid}", delete_project, methods=["DELETE"]),
    Route("/projects/{project_gid}/duplicate", duplicate_project, methods=["POST"]),
    Route("/projects/{project_gid}/addFollowers", add_followers_to_project, methods=["POST"]),
    Route("/projects/{project_gid}/removeFollowers", remove_followers_from_project, methods=["POST"]),
    Route("/projects/{project_gid}/addMembers", add_members_to_project, methods=["POST"]),
    Route("/projects/{project_gid}/removeMembers", remove_members_from_project, methods=["POST"]),
    Route("/projects/{project_gid}/addCustomFieldSetting", add_custom_field_setting_to_project, methods=["POST"]),
    Route("/projects/{project_gid}/removeCustomFieldSetting", remove_custom_field_setting_from_project, methods=["POST"]),
    Route("/projects/{project_gid}/custom_field_settings", get_custom_field_settings_for_project, methods=["GET"]),
    Route("/projects/{project_gid}/project_memberships", get_project_memberships, methods=["GET"]),
    Route("/projects/{project_gid}/project_portfolio_settings", get_project_portfolio_settings, methods=["GET"]),
    Route("/projects/{project_gid}/project_statuses", get_project_statuses, methods=["GET"]),
    Route("/projects/{project_gid}/project_statuses", create_project_status, methods=["POST"]),
    Route("/projects/{project_gid}/task_counts", get_task_counts_for_project, methods=["GET"]),
    Route("/projects/{project_gid}/project_briefs", create_project_brief, methods=["POST"]),
    Route("/projects/{project_gid}/tasks", get_tasks_for_project, methods=["GET"]),
    Route("/projects/{project_gid}/saveAsTemplate", save_project_as_template, methods=["POST"]),
    Route("/tasks/{task_gid}/projects", get_projects_for_task, methods=["GET"]),
    Route("/teams/{team_gid}/projects", get_projects_for_team, methods=["GET"]),
    Route("/teams/{team_gid}/projects", create_project_in_team, methods=["POST"]),
    Route("/workspaces/{workspace_gid}/projects/search", search_projects_in_workspace, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/projects", get_projects_for_workspace, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/projects", create_project_in_workspace, methods=["POST"]),

    # --- Sections ---
    Route("/projects/{project_gid}/sections/insert", insert_section_in_project, methods=["POST"]),
    Route("/projects/{project_gid}/sections", get_sections_for_project, methods=["GET"]),
    Route("/projects/{project_gid}/sections", create_section_in_project, methods=["POST"]),
    Route("/sections/{section_gid}/addTask", add_task_to_section, methods=["POST"]),
    Route("/sections/{section_gid}", get_section, methods=["GET"]),
    Route("/sections/{section_gid}", update_section, methods=["PUT"]),
    Route("/sections/{section_gid}", delete_section, methods=["DELETE"]),

    # --- Stories ---
    Route("/stories/{story_gid}", get_story, methods=["GET"]),
    Route("/stories/{story_gid}", update_story, methods=["PUT"]),
    Route("/stories/{story_gid}", delete_story, methods=["DELETE"]),
    Route("/tasks/{task_gid}/stories", get_stories_for_task, methods=["GET"]),
    Route("/tasks/{task_gid}/stories", create_story_on_task, methods=["POST"]),
    Route("/goals/{goal_gid}/stories", get_stories_for_goal, methods=["GET"]),
    Route("/goals/{goal_gid}/stories", create_story_on_goal, methods=["POST"]),

    # --- Tags ---
    Route("/tags", create_tag_handler, methods=["POST"]),
    Route("/tags", get_tags, methods=["GET"]),
    Route("/tags/{tag_gid}/tasks", get_tasks_for_tag, methods=["GET"]),
    Route("/tags/{tag_gid}", get_tag, methods=["GET"]),
    Route("/tags/{tag_gid}", update_tag, methods=["PUT"]),
    Route("/tags/{tag_gid}", delete_tag, methods=["DELETE"]),
    Route("/tasks/{task_gid}/addTag", add_tag_to_task, methods=["POST"]),
    Route("/tasks/{task_gid}/removeTag", remove_tag_from_task, methods=["POST"]),
    Route("/tasks/{task_gid}/tags", get_tags_for_task, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/tags", get_tags_for_workspace, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/tags", create_tag_in_workspace, methods=["POST"]),

    # --- Teams ---
    Route("/teams", create_team_handler, methods=["POST"]),
    Route("/teams/{team_gid}/addUser", add_user_to_team, methods=["POST"]),
    Route("/teams/{team_gid}/removeUser", remove_user_from_team, methods=["POST"]),
    Route("/teams/{team_gid}/team_memberships", get_team_memberships_for_team, methods=["GET"]),
    Route("/teams/{team_gid}/custom_field_settings", get_custom_field_settings_for_team, methods=["GET"]),
    Route("/teams/{team_gid}/project_templates", get_project_templates_for_team, methods=["GET"]),
    Route("/teams/{team_gid}", get_team_handler, methods=["GET"]),
    Route("/teams/{team_gid}", update_team_handler, methods=["PUT"]),
    Route("/users/{user_gid}/teams", get_teams_for_user, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/teams", get_teams_for_workspace, methods=["GET"]),

    # --- Users ---
    Route("/users", get_users, methods=["GET"]),
    Route("/users/{user_gid}/favorites", get_user_favorites, methods=["GET"]),
    Route("/users/{user_gid}/team_memberships", get_user_team_memberships, methods=["GET"]),
    Route("/users/{user_gid}/user_task_list", get_user_task_list, methods=["GET"]),
    Route("/users/{user_gid}/workspace_memberships", get_user_workspace_memberships, methods=["GET"]),
    Route("/users/{user_gid}", get_user, methods=["GET"]),
    Route("/users/{user_gid}", update_user, methods=["PUT"]),
    Route("/teams/{team_gid}/users", get_users_in_team, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/addUser", add_user_to_workspace, methods=["POST"]),
    Route("/workspaces/{workspace_gid}/removeUser", remove_user_from_workspace, methods=["POST"]),
    Route("/workspaces/{workspace_gid}/users/{user_gid}", get_user_in_workspace, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/users/{user_gid}", update_user_in_workspace, methods=["PUT"]),
    Route("/workspaces/{workspace_gid}/users", get_users_in_workspace, methods=["GET"]),

    # --- Tasks ---
    Route("/tasks", create_task_handler, methods=["POST"]),
    Route("/tasks", get_tasks, methods=["GET"]),
    Route("/tasks/{task_gid}/subtasks", get_subtasks, methods=["GET"]),
    Route("/tasks/{task_gid}/subtasks", create_subtask, methods=["POST"]),
    Route("/tasks/{task_gid}/setParent", set_task_parent, methods=["POST"]),
    Route("/tasks/{task_gid}/duplicate", duplicate_task_handler, methods=["POST"]),
    Route("/tasks/{task_gid}/addFollowers", add_followers_to_task, methods=["POST"]),
    Route("/tasks/{task_gid}/removeFollowers", remove_followers_from_task, methods=["POST"]),
    Route("/tasks/{task_gid}/addProject", add_project_to_task, methods=["POST"]),
    Route("/tasks/{task_gid}/removeProject", remove_project_from_task, methods=["POST"]),
    Route("/tasks/{task_gid}/addDependencies", add_dependencies_to_task, methods=["POST"]),
    Route("/tasks/{task_gid}/removeDependencies", remove_dependencies_from_task, methods=["POST"]),
    Route("/tasks/{task_gid}/dependencies", get_task_dependencies, methods=["GET"]),
    Route("/tasks/{task_gid}/addDependents", add_dependents_to_task, methods=["POST"]),
    Route("/tasks/{task_gid}/removeDependents", remove_dependents_from_task, methods=["POST"]),
    Route("/tasks/{task_gid}/dependents", get_task_dependents, methods=["GET"]),
    Route("/tasks/{task_gid}/time_tracking_entries", get_time_tracking_entries_for_task, methods=["GET"]),
    Route("/tasks/{task_gid}/time_tracking_entries", create_time_tracking_entry_for_task, methods=["POST"]),
    Route("/tasks/{task_gid}", get_task_handler, methods=["GET"]),
    Route("/tasks/{task_gid}", update_task_handler, methods=["PUT"]),
    Route("/tasks/{task_gid}", delete_task_handler, methods=["DELETE"]),
    Route("/sections/{section_gid}/tasks", get_tasks_for_section, methods=["GET"]),
    Route("/user_task_lists/{user_task_list_gid}/tasks", get_tasks_for_user_task_list, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/tasks/custom_id/{custom_id}", get_task_by_custom_id, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/tasks/search", search_tasks_in_workspace, methods=["GET"]),

    # --- Workspaces ---
    Route("/workspaces", get_workspaces, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/audit_log_events", get_audit_log_events, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/custom_fields", get_workspace_custom_fields, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/events", get_workspace_events, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/typeahead", get_workspace_typeahead, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/workspace_memberships", get_workspace_memberships_for_workspace, methods=["GET"]),
    Route("/workspaces/{workspace_gid}", get_workspace, methods=["GET"]),
    Route("/workspaces/{workspace_gid}", update_workspace, methods=["PUT"]),

    # --- Catch-all — MUST be the last entry ---
    Route(
        "/{_unknown_path:path}",
        unknown_endpoint,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
    ),
]
