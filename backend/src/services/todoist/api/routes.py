"""Todoist REST API routes.

Mounted under /api/env/{env_id}/services/todoist/api/v1
DB session comes from request.state.db_session (IsolationMiddleware).
User impersonation comes from request.state.impersonate_user_id.
"""

from __future__ import annotations

from typing import Any

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from sqlalchemy.orm import Session

from ..core.errors import (
    TodoistAPIError,
    bad_request,
    handle_exception,
    not_found,
    unauthorized,
)
from ..core.serializers import (
    serialize_label,
    serialize_label_list,
    serialize_project,
    serialize_project_list,
    serialize_task,
    serialize_task_list,
)
from ..database import operations as ops


# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------


def _session(request: Request) -> Session:
    session = getattr(request.state, "db_session", None)
    if session is None:
        raise unauthorized("Missing database session")
    return session


def _principal_user_id(request: Request) -> str:
    principal = getattr(request.state, "impersonate_user_id", None)
    if principal is not None and str(principal).strip() != "":
        return str(principal)
    raise unauthorized("Missing user authentication")


async def _parse_json_body(request: Request) -> dict[str, Any]:
    try:
        return await request.json()
    except Exception as exc:
        raise bad_request(f"Invalid JSON body: {exc}") from exc


def _pagination_params(request: Request) -> tuple[str | None, int]:
    """Extract cursor and limit from query params."""
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
# Project endpoints
# ---------------------------------------------------------------------------


async def get_projects(request: Request) -> JSONResponse:
    """GET /projects"""
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        projects, next_cursor = ops.list_projects(
            session, cursor=cursor, limit=limit
        )
        return JSONResponse(
            serialize_project_list(projects, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project(request: Request) -> JSONResponse:
    """POST /projects"""
    try:
        session = _session(request)
        principal_id = _principal_user_id(request)
        body = await _parse_json_body(request)

        name = body.get("name")
        if not isinstance(name, str) or not name.strip():
            raise bad_request("Field 'name' is required")

        project = ops.create_project(
            session,
            name=name.strip(),
            creator_uid=principal_id,
            description=body.get("description", ""),
            parent_id=body.get("parent_id"),
            color=body.get("color", "charcoal"),
            is_favorite=body.get("is_favorite", False),
            view_style=body.get("view_style"),
            workspace_id=body.get("workspace_id"),
        )
        return JSONResponse(
            serialize_project(project), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project(request: Request) -> JSONResponse:
    """GET /projects/{project_id}"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        project = ops.get_project(session, project_id)
        if project is None:
            raise not_found("Project not found")
        return JSONResponse(
            serialize_project(project), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_project(request: Request) -> JSONResponse:
    """POST /projects/{project_id}"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        body = await _parse_json_body(request)

        project = ops.update_project(
            session,
            project_id=project_id,
            name=body.get("name"),
            description=body.get("description"),
            color=body.get("color"),
            is_favorite=body.get("is_favorite"),
            view_style=body.get("view_style"),
            child_order=body.get("child_order"),
            is_collapsed=body.get("is_collapsed"),
        )
        if project is None:
            raise not_found("Project not found")
        return JSONResponse(
            serialize_project(project), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_project(request: Request) -> JSONResponse:
    """DELETE /projects/{project_id}"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        deleted = ops.delete_project(session, project_id)
        if not deleted:
            raise not_found("Project not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def archive_project(request: Request) -> JSONResponse:
    """POST /projects/{project_id}/archive"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        archived = ops.archive_project(session, project_id)
        if not archived:
            raise not_found("Project not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def unarchive_project(request: Request) -> JSONResponse:
    """POST /projects/{project_id}/unarchive"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        unarchived = ops.unarchive_project(session, project_id)
        if not unarchived:
            raise not_found("Project not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_archived_projects(request: Request) -> JSONResponse:
    """GET /projects/archived"""
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        projects, next_cursor = ops.list_archived_projects(
            session, cursor=cursor, limit=limit
        )
        return JSONResponse(
            serialize_project_list(projects, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def search_projects(request: Request) -> JSONResponse:
    """GET /projects/search"""
    try:
        session = _session(request)
        query_str = request.query_params.get("query", "")
        cursor, limit = _pagination_params(request)
        projects, next_cursor = ops.search_projects(
            session, query_str=query_str, cursor=cursor, limit=limit
        )
        return JSONResponse(
            serialize_project_list(projects, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Task endpoints
# ---------------------------------------------------------------------------


async def get_tasks(request: Request) -> JSONResponse:
    """GET /tasks"""
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)

        # Optional filters
        project_id = request.query_params.get("project_id")
        section_id = request.query_params.get("section_id")
        parent_id = request.query_params.get("parent_id")
        label = request.query_params.get("label")
        ids_param = request.query_params.get("ids")
        ids = ids_param.split(",") if ids_param else None

        tasks, next_cursor = ops.list_tasks(
            session,
            project_id=project_id,
            section_id=section_id,
            parent_id=parent_id,
            label=label,
            ids=ids,
            cursor=cursor,
            limit=limit,
        )
        return JSONResponse(
            serialize_task_list(tasks, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_task(request: Request) -> JSONResponse:
    """POST /tasks"""
    try:
        session = _session(request)
        principal_id = _principal_user_id(request)
        body = await _parse_json_body(request)

        content = body.get("content")
        if not isinstance(content, str) or not content.strip():
            raise bad_request("Field 'content' is required")

        # Build due object from due_string/due_date/due_datetime if provided
        due = None
        if any(body.get(k) for k in ("due_string", "due_date", "due_datetime")):
            due = {
                "string": body.get("due_string"),
                "date": body.get("due_date"),
                "datetime": body.get("due_datetime"),
                "lang": body.get("due_lang", "en"),
                "is_recurring": False,
            }

        # Build deadline from deadline_date if provided
        deadline = None
        if body.get("deadline_date"):
            deadline = {"date": body["deadline_date"], "lang": body.get("due_lang", "en")}

        # Build duration from duration + duration_unit if provided
        duration = None
        if body.get("duration") is not None and body.get("duration_unit"):
            duration = {"amount": body["duration"], "unit": body["duration_unit"]}

        task = ops.create_task(
            session,
            content=content.strip(),
            user_id=principal_id,
            project_id=body.get("project_id", ""),
            description=body.get("description", ""),
            section_id=body.get("section_id"),
            parent_id=body.get("parent_id"),
            labels=body.get("labels"),
            priority=body.get("priority", 1),
            due=due,
            deadline=deadline,
            duration=duration,
            order=body.get("order"),
            assignee_id=body.get("assignee_id"),
        )
        return JSONResponse(
            serialize_task(task), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_task(request: Request) -> JSONResponse:
    """GET /tasks/{task_id}"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        task = ops.get_task(session, task_id)
        if task is None:
            raise not_found("Task not found")
        return JSONResponse(
            serialize_task(task), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_id}"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        body = await _parse_json_body(request)

        # Build due/deadline/duration from flat fields if provided
        due = None
        if any(body.get(k) for k in ("due_string", "due_date", "due_datetime")):
            due = {
                "string": body.get("due_string"),
                "date": body.get("due_date"),
                "datetime": body.get("due_datetime"),
                "lang": body.get("due_lang", "en"),
                "is_recurring": False,
            }

        deadline = None
        if body.get("deadline_date"):
            deadline = {"date": body["deadline_date"], "lang": body.get("due_lang", "en")}

        duration = None
        if body.get("duration") is not None and body.get("duration_unit"):
            duration = {"amount": body["duration"], "unit": body["duration_unit"]}

        task = ops.update_task(
            session,
            task_id=task_id,
            content=body.get("content"),
            description=body.get("description"),
            labels=body.get("labels"),
            priority=body.get("priority"),
            due=due,
            deadline=deadline,
            duration=duration,
            assignee_id=body.get("assignee_id"),
            child_order=body.get("child_order"),
            day_order=body.get("day_order"),
            is_collapsed=body.get("is_collapsed"),
        )
        if task is None:
            raise not_found("Task not found")
        return JSONResponse(
            serialize_task(task), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_task(request: Request) -> JSONResponse:
    """DELETE /tasks/{task_id}"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        deleted = ops.delete_task(session, task_id)
        if not deleted:
            raise not_found("Task not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def close_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_id}/close"""
    try:
        session = _session(request)
        principal_id = _principal_user_id(request)
        task_id = request.path_params["task_id"]
        closed = ops.close_task(session, task_id, completed_by_uid=principal_id)
        if not closed:
            raise not_found("Task not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def reopen_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_id}/reopen"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        reopened = ops.reopen_task(session, task_id)
        if not reopened:
            raise not_found("Task not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def move_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_id}/move"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        body = await _parse_json_body(request)

        task = ops.move_task(
            session,
            task_id=task_id,
            project_id=body.get("project_id"),
            section_id=body.get("section_id"),
            parent_id=body.get("parent_id"),
        )
        if task is None:
            raise not_found("Task not found")
        return JSONResponse(
            serialize_task(task), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Label endpoints
# ---------------------------------------------------------------------------


async def get_labels(request: Request) -> JSONResponse:
    """GET /labels"""
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        labels, next_cursor = ops.list_labels(
            session, cursor=cursor, limit=limit
        )
        return JSONResponse(
            serialize_label_list(labels, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_label(request: Request) -> JSONResponse:
    """POST /labels"""
    try:
        session = _session(request)
        body = await _parse_json_body(request)

        name = body.get("name")
        if not isinstance(name, str) or not name.strip():
            raise bad_request("Field 'name' is required")

        label = ops.create_label(
            session,
            name=name.strip(),
            order=body.get("order"),
            color=body.get("color", "charcoal"),
            is_favorite=body.get("is_favorite", False),
        )
        return JSONResponse(
            serialize_label(label), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_label(request: Request) -> JSONResponse:
    """GET /labels/{label_id}"""
    try:
        session = _session(request)
        label_id = request.path_params["label_id"]
        label = ops.get_label(session, label_id)
        if label is None:
            raise not_found("Label not found")
        return JSONResponse(
            serialize_label(label), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_label(request: Request) -> JSONResponse:
    """POST /labels/{label_id}"""
    try:
        session = _session(request)
        label_id = request.path_params["label_id"]
        body = await _parse_json_body(request)

        label = ops.update_label(
            session,
            label_id=label_id,
            name=body.get("name"),
            order=body.get("order"),
            color=body.get("color"),
            is_favorite=body.get("is_favorite"),
        )
        if label is None:
            raise not_found("Label not found")
        return JSONResponse(
            serialize_label(label), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_label(request: Request) -> JSONResponse:
    """DELETE /labels/{label_id}"""
    try:
        session = _session(request)
        label_id = request.path_params["label_id"]
        deleted = ops.delete_label(session, label_id)
        if not deleted:
            raise not_found("Label not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Route table
# ---------------------------------------------------------------------------

# Note: fixed paths (archived, search, filter, completed, quick) must come
# before parameterized {id} paths so Starlette matches them first.

routes = [
    # Projects
    Route("/projects", get_projects, methods=["GET"]),
    Route("/projects", create_project, methods=["POST"]),
    Route("/projects/archived", get_archived_projects, methods=["GET"]),
    Route("/projects/search", search_projects, methods=["GET"]),
    Route("/projects/{project_id}", get_project, methods=["GET"]),
    Route("/projects/{project_id}", update_project, methods=["POST"]),
    Route("/projects/{project_id}", delete_project, methods=["DELETE"]),
    Route("/projects/{project_id}/archive", archive_project, methods=["POST"]),
    Route("/projects/{project_id}/unarchive", unarchive_project, methods=["POST"]),
    # Tasks
    Route("/tasks", get_tasks, methods=["GET"]),
    Route("/tasks", create_task, methods=["POST"]),
    Route("/tasks/{task_id}", get_task, methods=["GET"]),
    Route("/tasks/{task_id}", update_task, methods=["POST"]),
    Route("/tasks/{task_id}", delete_task, methods=["DELETE"]),
    Route("/tasks/{task_id}/close", close_task, methods=["POST"]),
    Route("/tasks/{task_id}/reopen", reopen_task, methods=["POST"]),
    Route("/tasks/{task_id}/move", move_task, methods=["POST"]),
    # Labels
    Route("/labels", get_labels, methods=["GET"]),
    Route("/labels", create_label, methods=["POST"]),
    Route("/labels/{label_id}", get_label, methods=["GET"]),
    Route("/labels/{label_id}", update_label, methods=["POST"]),
    Route("/labels/{label_id}", delete_label, methods=["DELETE"]),
]
