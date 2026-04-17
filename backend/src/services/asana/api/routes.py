"""Asana REST API routes.

Mounted under /api/env/{env_id}/services/asana
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

from ..core.errors import (
    AsanaAPIError,
    bad_request,
    handle_exception,
    not_found,
    unauthorized,
)
from ..core.serializers import (
    serialize_project,
    serialize_project_compact,
    serialize_project_list,
    serialize_tag_compact,
    serialize_task,
    serialize_task_compact,
    serialize_task_list,
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
    cursor = request.query_params.get("offset")
    limit_str = request.query_params.get("limit")
    limit = 50
    if limit_str is not None:
        try:
            limit = max(1, min(200, int(limit_str)))
        except ValueError:
            pass
    return cursor, limit


# ---------------------------------------------------------------------------
# Endpoint handlers — tasks
# ---------------------------------------------------------------------------


async def create_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        task = ops.create_task(session, data=data)
        return JSONResponse({"data": serialize_task(task)}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)

        tasks, next_cursor = ops.list_tasks(
            session,
            assignee=request.query_params.get("assignee"),
            project=request.query_params.get("project"),
            section=request.query_params.get("section"),
            workspace=request.query_params.get("workspace"),
            completed_since=request.query_params.get("completed_since"),
            modified_since=request.query_params.get("modified_since"),
            cursor=cursor,
            limit=limit,
        )
        return JSONResponse(serialize_task_list(tasks, next_cursor), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        task = ops.update_task(session, task_gid, data=data)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        deleted = ops.delete_task(session, task_gid)
        if not deleted:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks_for_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        tasks = ops.list_tasks_by_project(session, project_gid)
        return JSONResponse(serialize_task_list(tasks), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks_for_section(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        section_gid = request.path_params["section_gid"]
        tasks = ops.list_tasks_by_section(session, section_gid)
        return JSONResponse(serialize_task_list(tasks), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks_for_tag(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        tag_gid = request.path_params["tag_gid"]
        tasks = ops.list_tasks_by_tag(session, tag_gid)
        return JSONResponse(serialize_task_list(tasks), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tasks_for_user_task_list(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        user_task_list_gid = request.path_params["user_task_list_gid"]
        tasks = ops.list_tasks_by_user_task_list(session, user_task_list_gid)
        return JSONResponse(serialize_task_list(tasks), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_subtasks(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        cursor, limit = _pagination_params(request)
        tasks, next_cursor = ops.list_subtasks(session, task_gid, cursor=cursor, limit=limit)
        return JSONResponse(serialize_task_list(tasks, next_cursor), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_subtask(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        subtask = ops.create_subtask(session, task_gid, data=data)
        if subtask is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(subtask)}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_dependencies(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        dependencies = ops.get_dependencies(session, task_gid)
        return JSONResponse(serialize_task_list(dependencies), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_dependents(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        dependents = ops.get_dependents(session, task_gid)
        return JSONResponse(serialize_task_list(dependents), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_dependencies(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        dependency_gids = data.get("dependencies", [])
        if not isinstance(dependency_gids, list):
            raise bad_request("Field 'dependencies' must be an array")

        success = ops.add_dependencies(session, task_gid, dependency_gids=dependency_gids)
        if not success:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_dependencies(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        dependency_gids = data.get("dependencies", [])
        if not isinstance(dependency_gids, list):
            raise bad_request("Field 'dependencies' must be an array")

        success = ops.remove_dependencies(session, task_gid, dependency_gids=dependency_gids)
        if not success:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_dependents(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        dependent_gids = data.get("dependents", [])
        if not isinstance(dependent_gids, list):
            raise bad_request("Field 'dependents' must be an array")

        success = ops.add_dependents(session, task_gid, dependent_gids=dependent_gids)
        if not success:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_dependents(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        dependent_gids = data.get("dependents", [])
        if not isinstance(dependent_gids, list):
            raise bad_request("Field 'dependents' must be an array")

        success = ops.remove_dependents(session, task_gid, dependent_gids=dependent_gids)
        if not success:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_followers(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        follower_gids = data.get("followers", [])
        if not isinstance(follower_gids, list):
            raise bad_request("Field 'followers' must be an array")

        task = ops.add_followers(session, task_gid, follower_gids=follower_gids)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_followers(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        follower_gids = data.get("followers", [])
        if not isinstance(follower_gids, list):
            raise bad_request("Field 'followers' must be an array")

        task = ops.remove_followers(session, task_gid, follower_gids=follower_gids)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
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
            raise bad_request("Field 'project' is required")

        success = ops.add_project_to_task(session, task_gid, project_gid=project_gid)
        if not success:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
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
            raise bad_request("Field 'project' is required")

        success = ops.remove_project_from_task(session, task_gid, project_gid=project_gid)
        if not success:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_tag_to_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        tag_gid = data.get("tag")
        if not tag_gid:
            raise bad_request("Field 'tag' is required")

        success = ops.add_tag_to_task(session, task_gid, tag_gid=tag_gid)
        if not success:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_tag_from_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        tag_gid = data.get("tag")
        if not tag_gid:
            raise bad_request("Field 'tag' is required")

        success = ops.remove_tag_from_task(session, task_gid, tag_gid=tag_gid)
        if not success:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_projects_for_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        projects = [serialize_project_compact(project) for project in task.project_objects]
        return JSONResponse({"data": projects}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_tags_for_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        tags = [serialize_tag_compact(tag) for tag in task.tag_objects]
        return JSONResponse({"data": tags}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def duplicate_task(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})

        new_task = ops.duplicate_task(
            session,
            task_gid,
            name=data.get("name"),
            include=data.get("include"),
        )
        if new_task is None:
            raise not_found(f"task: Unknown object: {task_gid}")

        # Duplicate returns a Job response wrapping the new task
        job_response = {
            "gid": new_task.gid,
            "resource_type": "job",
            "resource_subtype": "duplicate_task",
            "status": "succeeded",
            "new_task": serialize_task_compact(new_task),
        }
        return JSONResponse({"data": job_response}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def set_parent(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        parent_gid = data.get("parent")

        task = ops.set_parent(session, task_gid, parent_gid=parent_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": serialize_task(task)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_time_tracking_entries(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        task = ops.get_task(session, task_gid)
        if task is None:
            raise not_found(f"task: Unknown object: {task_gid}")

        cursor, limit = _pagination_params(request)
        entries, next_cursor = ops.list_time_tracking_entries(
            session, task_gid, cursor=cursor, limit=limit,
        )
        result: dict[str, Any] = {"data": entries}
        if next_cursor is not None:
            result["next_page"] = {"offset": next_cursor, "path": None, "uri": None}
        else:
            result["next_page"] = None
        return JSONResponse(result, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_time_tracking_entry(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        task_gid = request.path_params["task_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        entry = ops.create_time_tracking_entry(session, task_gid, data=data)
        if entry is None:
            raise not_found(f"task: Unknown object: {task_gid}")
        return JSONResponse({"data": entry}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def search_tasks_in_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        tasks = ops.search_tasks(session, workspace_gid)
        return JSONResponse(serialize_task_list(tasks), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_task_by_custom_id(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        custom_id = request.path_params["custom_id"]
        task = ops.get_task_by_custom_id(session, workspace_gid, custom_id)
        if task is None:
            raise not_found(f"task: No task found with custom_id {custom_id}")
        return JSONResponse({"data": serialize_task(task)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Endpoint handlers — projects
# ---------------------------------------------------------------------------


async def create_project_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        project = ops.create_project(session, data=data)
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_projects_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)

        # Parse archived query param as boolean if present
        archived_param = request.query_params.get("archived")
        archived = None
        if archived_param is not None:
            archived = archived_param.lower() == "true"

        projects, next_cursor = ops.list_projects(
            session,
            workspace=request.query_params.get("workspace"),
            team=request.query_params.get("team"),
            archived=archived,
            cursor=cursor,
            limit=limit,
        )
        return JSONResponse(serialize_project_list(projects, next_cursor), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_project_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        project = ops.update_project(session, project_gid, data=data)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_project_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        deleted = ops.delete_project(session, project_gid)
        if not deleted:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_custom_field_settings(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": project.custom_field_settings or []}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_memberships(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        # Return member list as project_membership compact objects
        memberships = []
        for member_gid in (project.members or []):
            memberships.append({
                "gid": member_gid,
                "resource_type": "project_membership",
                "member": {"gid": member_gid, "resource_type": "user"},
                "access_level": "editor",
            })
        return JSONResponse({"data": memberships}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_portfolio_settings(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        # Portfolio settings are not modeled in Pass 1; return empty list
        return JSONResponse({"data": []}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_statuses(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        # Project statuses stored on current_status; return as single-item list if present
        statuses = []
        if project.current_status:
            statuses.append(project.current_status)
        return JSONResponse({"data": statuses, "next_page": None}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project_task_counts(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        # Count tasks via the relationship
        all_tasks = [task for task in project.tasks if not task.is_deleted]
        completed_tasks = [task for task in all_tasks if task.completed]
        incomplete_tasks = [task for task in all_tasks if not task.completed]
        milestones = [task for task in all_tasks if task.resource_subtype == "milestone"]
        completed_milestones = [task for task in milestones if task.completed]
        incomplete_milestones = [task for task in milestones if not task.completed]
        return JSONResponse({"data": {
            "num_tasks": len(all_tasks),
            "num_completed_tasks": len(completed_tasks),
            "num_incomplete_tasks": len(incomplete_tasks),
            "num_milestones": len(milestones),
            "num_completed_milestones": len(completed_milestones),
            "num_incomplete_milestones": len(incomplete_milestones),
        }}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_projects_for_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        cursor, limit = _pagination_params(request)

        archived_param = request.query_params.get("archived")
        archived = None
        if archived_param is not None:
            archived = archived_param.lower() == "true"

        projects, next_cursor = ops.list_projects(
            session, team=team_gid, archived=archived, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_project_list(projects, next_cursor), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_projects_for_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        cursor, limit = _pagination_params(request)

        archived_param = request.query_params.get("archived")
        archived = None
        if archived_param is not None:
            archived = archived_param.lower() == "true"

        projects, next_cursor = ops.list_projects(
            session, workspace=workspace_gid, archived=archived, cursor=cursor, limit=limit,
        )
        return JSONResponse(serialize_project_list(projects, next_cursor), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def search_projects_in_workspace_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        projects = ops.search_projects_in_workspace(session, workspace_gid)
        return JSONResponse(serialize_project_list(projects), status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project_in_team(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        team_gid = request.path_params["team_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        data["team"] = team_gid
        project = ops.create_project(session, data=data)
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project_in_workspace(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        workspace_gid = request.path_params["workspace_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        data["workspace"] = workspace_gid
        project = ops.create_project(session, data=data)
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def duplicate_project_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})

        new_project = ops.duplicate_project(
            session,
            project_gid,
            name=data.get("name"),
            team=data.get("team"),
            include=data.get("include"),
        )
        if new_project is None:
            raise not_found(f"project: Unknown object: {project_gid}")

        # Duplicate returns a Job response wrapping the new project
        job_response = {
            "gid": new_project.gid,
            "resource_type": "job",
            "resource_subtype": "duplicate_project",
            "status": "succeeded",
            "new_project": serialize_project_compact(new_project),
        }
        return JSONResponse({"data": job_response}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_custom_field_to_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not data.get("custom_field"):
            raise bad_request("Field 'custom_field' is required")

        project = ops.add_custom_field_setting_to_project(session, project_gid, data=data)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_custom_field_from_project(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        custom_field_gid = data.get("custom_field")
        if not custom_field_gid:
            raise bad_request("Field 'custom_field' is required")

        project = ops.remove_custom_field_setting_from_project(
            session, project_gid, custom_field_gid=custom_field_gid,
        )
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": {}}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_followers_to_project_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        followers_raw = data.get("followers", "")
        # Followers come as a comma-separated string
        if isinstance(followers_raw, str):
            follower_gids = [gid.strip() for gid in followers_raw.split(",") if gid.strip()]
        else:
            follower_gids = list(followers_raw)

        project = ops.add_followers_to_project(session, project_gid, follower_gids=follower_gids)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_followers_from_project_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        followers_raw = data.get("followers", "")
        if isinstance(followers_raw, str):
            follower_gids = [gid.strip() for gid in followers_raw.split(",") if gid.strip()]
        else:
            follower_gids = list(followers_raw)

        project = ops.remove_followers_from_project(session, project_gid, follower_gids=follower_gids)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_members_to_project_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        members_raw = data.get("members", "")
        if isinstance(members_raw, str):
            member_gids = [gid.strip() for gid in members_raw.split(",") if gid.strip()]
        else:
            member_gids = list(members_raw)

        project = ops.add_members_to_project(session, project_gid, member_gids=member_gids)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_members_from_project_handler(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        members_raw = data.get("members", "")
        if isinstance(members_raw, str):
            member_gids = [gid.strip() for gid in members_raw.split(",") if gid.strip()]
        else:
            member_gids = list(members_raw)

        project = ops.remove_members_from_project(session, project_gid, member_gids=member_gids)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")
        return JSONResponse({"data": serialize_project(project)}, status_code=status.HTTP_200_OK)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project_status(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")

        # Build a project status object and store as current_status
        from ..core.utils import generate_id, now_iso
        timestamp = now_iso()
        status_obj = {
            "gid": generate_id("project"),
            "resource_type": "project_status",
            "title": data.get("title"),
            "text": data.get("text"),
            "html_text": data.get("html_text"),
            "color": data.get("color"),
            "created_at": timestamp,
            "modified_at": timestamp,
        }
        project.current_status = status_obj
        project.modified_at = timestamp
        session.flush()
        return JSONResponse({"data": status_obj}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project_brief(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})
        if not isinstance(data, dict):
            raise bad_request("Field 'data' must be an object")

        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")

        from ..core.utils import generate_id, now_iso
        brief = {
            "gid": generate_id("project"),
            "resource_type": "project_brief",
            "title": data.get("title"),
            "html_text": data.get("html_text"),
            "text": data.get("text"),
            "permalink_url": f"https://app.asana.com/0/{project_gid}/brief",
            "project": serialize_project_compact(project),
        }
        project.project_brief = brief
        project.modified_at = now_iso()
        session.flush()
        return JSONResponse({"data": brief}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def save_project_as_template(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        project_gid = request.path_params["project_gid"]
        body = await _parse_json_body(request)
        data = body.get("data", {})

        project = ops.get_project(session, project_gid)
        if project is None:
            raise not_found(f"project: Unknown object: {project_gid}")

        from ..core.utils import generate_id
        template_gid = generate_id("project")
        job_response = {
            "gid": generate_id("job"),
            "resource_type": "job",
            "resource_subtype": "save_as_template",
            "status": "succeeded",
            "new_project_template": {
                "gid": template_gid,
                "resource_type": "project_template",
                "name": data.get("name", f"{project.name} template"),
            },
        }
        return JSONResponse({"data": job_response}, status_code=status.HTTP_201_CREATED)
    except AsanaAPIError as exc:
        return exc.to_response()
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
    # --- Task endpoints ---

    # Fixed collection endpoints
    Route("/tasks", get_tasks, methods=["GET"]),
    Route("/tasks", create_task, methods=["POST"]),

    # Nested collection endpoints (fixed parent resource paths)
    Route("/projects/{project_gid}/tasks", get_tasks_for_project, methods=["GET"]),
    Route("/sections/{section_gid}/tasks", get_tasks_for_section, methods=["GET"]),
    Route("/tags/{tag_gid}/tasks", get_tasks_for_tag, methods=["GET"]),
    Route("/user_task_lists/{user_task_list_gid}/tasks", get_tasks_for_user_task_list, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/tasks/search", search_tasks_in_workspace, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/tasks/custom_id/{custom_id}", get_task_by_custom_id, methods=["GET"]),

    # Task sub-resource action endpoints (fixed suffixes before parameterized)
    Route("/tasks/{task_gid}/subtasks", get_subtasks, methods=["GET"]),
    Route("/tasks/{task_gid}/subtasks", create_subtask, methods=["POST"]),
    Route("/tasks/{task_gid}/dependencies", get_dependencies, methods=["GET"]),
    Route("/tasks/{task_gid}/dependents", get_dependents, methods=["GET"]),
    Route("/tasks/{task_gid}/projects", get_projects_for_task, methods=["GET"]),
    Route("/tasks/{task_gid}/tags", get_tags_for_task, methods=["GET"]),
    Route("/tasks/{task_gid}/time_tracking_entries", get_time_tracking_entries, methods=["GET"]),
    Route("/tasks/{task_gid}/time_tracking_entries", create_time_tracking_entry, methods=["POST"]),
    Route("/tasks/{task_gid}/addDependencies", add_dependencies, methods=["POST"]),
    Route("/tasks/{task_gid}/addDependents", add_dependents, methods=["POST"]),
    Route("/tasks/{task_gid}/removeDependencies", remove_dependencies, methods=["POST"]),
    Route("/tasks/{task_gid}/removeDependents", remove_dependents, methods=["POST"]),
    Route("/tasks/{task_gid}/addFollowers", add_followers, methods=["POST"]),
    Route("/tasks/{task_gid}/removeFollowers", remove_followers, methods=["POST"]),
    Route("/tasks/{task_gid}/addProject", add_project_to_task, methods=["POST"]),
    Route("/tasks/{task_gid}/removeProject", remove_project_from_task, methods=["POST"]),
    Route("/tasks/{task_gid}/addTag", add_tag_to_task, methods=["POST"]),
    Route("/tasks/{task_gid}/removeTag", remove_tag_from_task, methods=["POST"]),
    Route("/tasks/{task_gid}/duplicate", duplicate_task, methods=["POST"]),
    Route("/tasks/{task_gid}/setParent", set_parent, methods=["POST"]),

    # Single-task CRUD (parameterized path last among /tasks/*)
    Route("/tasks/{task_gid}", get_task, methods=["GET"]),
    Route("/tasks/{task_gid}", update_task, methods=["PUT"]),
    Route("/tasks/{task_gid}", delete_task, methods=["DELETE"]),

    # --- Project endpoints ---

    # Fixed collection endpoints
    Route("/projects", get_projects_handler, methods=["GET"]),
    Route("/projects", create_project_handler, methods=["POST"]),

    # Nested collection endpoints (fixed parent resource paths)
    Route("/teams/{team_gid}/projects", get_projects_for_team, methods=["GET"]),
    Route("/teams/{team_gid}/projects", create_project_in_team, methods=["POST"]),
    Route("/workspaces/{workspace_gid}/projects/search", search_projects_in_workspace_handler, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/projects", get_projects_for_workspace, methods=["GET"]),
    Route("/workspaces/{workspace_gid}/projects", create_project_in_workspace, methods=["POST"]),

    # Project sub-resource and action endpoints
    Route("/projects/{project_gid}/custom_field_settings", get_project_custom_field_settings, methods=["GET"]),
    Route("/projects/{project_gid}/project_memberships", get_project_memberships, methods=["GET"]),
    Route("/projects/{project_gid}/project_portfolio_settings", get_project_portfolio_settings, methods=["GET"]),
    Route("/projects/{project_gid}/project_statuses", get_project_statuses, methods=["GET"]),
    Route("/projects/{project_gid}/project_statuses", create_project_status, methods=["POST"]),
    Route("/projects/{project_gid}/project_briefs", create_project_brief, methods=["POST"]),
    Route("/projects/{project_gid}/task_counts", get_project_task_counts, methods=["GET"]),
    Route("/projects/{project_gid}/addCustomFieldSetting", add_custom_field_to_project, methods=["POST"]),
    Route("/projects/{project_gid}/removeCustomFieldSetting", remove_custom_field_from_project, methods=["POST"]),
    Route("/projects/{project_gid}/addFollowers", add_followers_to_project_handler, methods=["POST"]),
    Route("/projects/{project_gid}/removeFollowers", remove_followers_from_project_handler, methods=["POST"]),
    Route("/projects/{project_gid}/addMembers", add_members_to_project_handler, methods=["POST"]),
    Route("/projects/{project_gid}/removeMembers", remove_members_from_project_handler, methods=["POST"]),
    Route("/projects/{project_gid}/duplicate", duplicate_project_handler, methods=["POST"]),
    Route("/projects/{project_gid}/saveAsTemplate", save_project_as_template, methods=["POST"]),

    # Single-project CRUD (parameterized path last among /projects/*)
    Route("/projects/{project_gid}", get_project_handler, methods=["GET"]),
    Route("/projects/{project_gid}", update_project_handler, methods=["PUT"]),
    Route("/projects/{project_gid}", delete_project_handler, methods=["DELETE"]),

    # --- Catch-all — MUST be the last entry ---
    Route(
        "/{_unknown_path:path}",
        unknown_endpoint,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
    ),
]
