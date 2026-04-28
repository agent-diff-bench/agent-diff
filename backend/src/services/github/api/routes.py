"""GitHub REST API routes.

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

from ..core.errors import (
    AppAPIError,
    bad_request,
    forbidden,
    gone,
    handle_exception,
    not_found,
    unauthorized,
    unprocessable_entity,
    service_unavailable,
)
from ..core.serializers import (
    serialize_gist,
    serialize_gist_base,
    serialize_gist_comment,
    serialize_gist_comment_list,
    serialize_gist_commit_list,
    serialize_gist_list,
    serialize_issue,
    serialize_issue_list,
    serialize_issue_search_result,
    serialize_issue_comment as serialize_ic,
    serialize_issue_comment_list as serialize_ic_list,
    serialize_issue_event,
    serialize_issue_event_list,
    serialize_reaction,
    serialize_reaction_list,
    serialize_label_list,
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


def _page_params(request: Request) -> tuple[int, int]:
    """Extract per_page and page from query params (GitHub offset pagination)."""
    per_page = 30
    page = 1
    per_page_str = request.query_params.get("per_page")
    page_str = request.query_params.get("page")
    if per_page_str is not None:
        try:
            per_page = max(1, min(100, int(per_page_str)))
        except ValueError:
            pass
    if page_str is not None:
        try:
            page = max(1, int(page_str))
        except ValueError:
            pass
    return per_page, page


# ---------------------------------------------------------------------------
# Endpoint handlers — added per entity by entity scaffold
# ---------------------------------------------------------------------------

# AGENT INSTRUCTION: Add endpoint handler functions here during entity
# implementation. Each handler follows this pattern:
#
#   async def <operation>_<entity>(request: Request) -> JSONResponse:
#       try:
#           session = _session(request)
#           # ... extract params, call ops, serialize ...
#           return JSONResponse(payload, status_code=status.HTTP_200_OK)
#       except AppAPIError as exc:
#           return exc.to_response()
#       except Exception as exc:
#           return handle_exception(exc)


# ---------------------------------------------------------------------------
# Gists
# ---------------------------------------------------------------------------


async def list_gists(request: Request) -> JSONResponse:
    """GET /gists — list gists for the authenticated user."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        per_page, page = _page_params(request)
        since = request.query_params.get("since")
        gists = ops.list_gists(
            session, owner_id=user_id, since=since, per_page=per_page, page=page,
        )
        return JSONResponse(serialize_gist_list(gists))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_public_gists(request: Request) -> JSONResponse:
    """GET /gists/public — list public gists."""
    try:
        session = _session(request)
        per_page, page = _page_params(request)
        since = request.query_params.get("since")
        gists = ops.list_gists(
            session, public_only=True, since=since, per_page=per_page, page=page,
        )
        return JSONResponse(serialize_gist_list(gists))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_starred_gists(request: Request) -> JSONResponse:
    """GET /gists/starred — list starred gists."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        per_page, page = _page_params(request)
        since = request.query_params.get("since")
        gists = ops.list_starred_gists(
            session, user_id, since=since, per_page=per_page, page=page,
        )
        return JSONResponse(serialize_gist_list(gists))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_gist(request: Request) -> JSONResponse:
    """POST /gists — create a gist."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        body = await _parse_json_body(request)
        if not body.get("files"):
            raise unprocessable_entity("Validation Failed", errors=[
                {"resource": "Gist", "field": "files", "code": "missing_field"},
            ])
        gist = ops.create_gist(session, body, user_id)
        # Add initial commit to history
        ops._add_gist_commit(gist, user_id, session=session)
        session.flush()
        return JSONResponse(serialize_gist(gist), status_code=status.HTTP_201_CREATED)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_gist(request: Request) -> JSONResponse:
    """GET /gists/{gist_id} — get a gist."""
    try:
        session = _session(request)
        gist_id = request.path_params["gist_id"]
        gist = ops.get_gist(session, gist_id)
        if gist is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_gist(gist))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_gist(request: Request) -> JSONResponse:
    """PATCH /gists/{gist_id} — update a gist."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        gist_id = request.path_params["gist_id"]
        body = await _parse_json_body(request)
        gist = ops.update_gist(session, gist_id, body)
        if gist is None:
            raise not_found("Not Found")
        ops._add_gist_commit(gist, user_id, session=session)
        session.flush()
        return JSONResponse(serialize_gist(gist))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_gist(request: Request) -> JSONResponse:
    """DELETE /gists/{gist_id} — delete a gist."""
    try:
        session = _session(request)
        gist_id = request.path_params["gist_id"]
        deleted = ops.delete_gist(session, gist_id)
        if not deleted:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def star_gist(request: Request) -> JSONResponse:
    """PUT /gists/{gist_id}/star — star a gist."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        gist_id = request.path_params["gist_id"]
        result = ops.star_gist(session, gist_id, user_id)
        if not result:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def unstar_gist(request: Request) -> JSONResponse:
    """DELETE /gists/{gist_id}/star — unstar a gist."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        gist_id = request.path_params["gist_id"]
        result = ops.unstar_gist(session, gist_id, user_id)
        if not result:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def check_gist_star(request: Request) -> JSONResponse:
    """GET /gists/{gist_id}/star — check if a gist is starred."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        gist_id = request.path_params["gist_id"]
        result = ops.is_gist_starred(session, gist_id, user_id)
        if result is None:
            raise not_found("Not Found")
        if result:
            return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
        raise not_found("Not Found")
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_gist_comments(request: Request) -> JSONResponse:
    """GET /gists/{gist_id}/comments — list gist comments."""
    try:
        session = _session(request)
        gist_id = request.path_params["gist_id"]
        # Verify gist exists
        gist = ops.get_gist(session, gist_id)
        if gist is None:
            raise not_found("Not Found")
        per_page, page = _page_params(request)
        comments = ops.list_gist_comments(session, gist_id, per_page=per_page, page=page)
        return JSONResponse(serialize_gist_comment_list(comments))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_gist_comment(request: Request) -> JSONResponse:
    """POST /gists/{gist_id}/comments — create a gist comment."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        gist_id = request.path_params["gist_id"]
        body = await _parse_json_body(request)
        comment_body = body.get("body")
        if not comment_body:
            raise unprocessable_entity("Validation Failed", errors=[
                {"resource": "GistComment", "field": "body", "code": "missing_field"},
            ])
        comment = ops.create_gist_comment(session, gist_id, comment_body, user_id)
        if comment is None:
            raise not_found("Not Found")
        return JSONResponse(
            serialize_gist_comment(comment),
            status_code=status.HTTP_201_CREATED,
        )
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_gist_comment(request: Request) -> JSONResponse:
    """GET /gists/{gist_id}/comments/{comment_id} — get a gist comment."""
    try:
        session = _session(request)
        gist_id = request.path_params["gist_id"]
        comment_id = int(request.path_params["comment_id"])
        comment = ops.get_gist_comment(session, gist_id, comment_id)
        if comment is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_gist_comment(comment))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_gist_comment(request: Request) -> JSONResponse:
    """PATCH /gists/{gist_id}/comments/{comment_id} — update a gist comment."""
    try:
        session = _session(request)
        gist_id = request.path_params["gist_id"]
        comment_id = int(request.path_params["comment_id"])
        body = await _parse_json_body(request)
        comment_body = body.get("body")
        if not comment_body:
            raise unprocessable_entity("Validation Failed", errors=[
                {"resource": "GistComment", "field": "body", "code": "missing_field"},
            ])
        comment = ops.update_gist_comment(session, gist_id, comment_id, comment_body)
        if comment is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_gist_comment(comment))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_gist_comment(request: Request) -> JSONResponse:
    """DELETE /gists/{gist_id}/comments/{comment_id} — delete a gist comment."""
    try:
        session = _session(request)
        gist_id = request.path_params["gist_id"]
        comment_id = int(request.path_params["comment_id"])
        deleted = ops.delete_gist_comment(session, gist_id, comment_id)
        if not deleted:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_gist_commits(request: Request) -> JSONResponse:
    """GET /gists/{gist_id}/commits — list gist commits."""
    try:
        session = _session(request)
        gist_id = request.path_params["gist_id"]
        per_page, page = _page_params(request)
        commits = ops.list_gist_commits(session, gist_id, per_page=per_page, page=page)
        if commits is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_gist_commit_list(commits))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_gist_forks(request: Request) -> JSONResponse:
    """GET /gists/{gist_id}/forks — list gist forks."""
    try:
        session = _session(request)
        gist_id = request.path_params["gist_id"]
        per_page, page = _page_params(request)
        forks = ops.list_gist_forks(session, gist_id, per_page=per_page, page=page)
        if forks is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_gist_list(forks))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def fork_gist(request: Request) -> JSONResponse:
    """POST /gists/{gist_id}/forks — fork a gist."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        gist_id = request.path_params["gist_id"]
        forked = ops.fork_gist(session, gist_id, user_id)
        if forked is None:
            raise not_found("Not Found")
        # Add initial commit to the fork
        ops._add_gist_commit(forked, user_id, session=session)
        session.flush()
        return JSONResponse(
            serialize_gist_base(forked),
            status_code=status.HTTP_201_CREATED,
        )
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_gist_revision(request: Request) -> JSONResponse:
    """GET /gists/{gist_id}/{sha} — get a gist revision."""
    try:
        session = _session(request)
        gist_id = request.path_params["gist_id"]
        sha = request.path_params["sha"]
        gist = ops.get_gist_revision(session, gist_id, sha)
        if gist is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_gist(gist))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_user_gists(request: Request) -> JSONResponse:
    """GET /users/{username}/gists — list gists for a user."""
    try:
        session = _session(request)
        username = request.path_params["username"]
        per_page, page = _page_params(request)
        since = request.query_params.get("since")
        gists = ops.list_gists(
            session, owner_id=username, since=since, per_page=per_page, page=page,
        )
        return JSONResponse(serialize_gist_list(gists))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------


async def list_authenticated_user_issues(request: Request) -> JSONResponse:
    """GET /issues — list issues assigned to the authenticated user."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        per_page, page = _page_params(request)
        state = request.query_params.get("state", "open")
        sort = request.query_params.get("sort", "created")
        direction = request.query_params.get("direction", "desc")
        since = request.query_params.get("since")
        issues = ops.list_issues_for_user(
            session, user_id, state=state, sort=sort, direction=direction,
            since=since, per_page=per_page, page=page,
        )
        return JSONResponse(serialize_issue_list(issues))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_org_issues(request: Request) -> JSONResponse:
    """GET /orgs/{org}/issues — list organization issues assigned to the authenticated user."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        per_page, page = _page_params(request)
        state = request.query_params.get("state", "open")
        sort = request.query_params.get("sort", "created")
        direction = request.query_params.get("direction", "desc")
        since = request.query_params.get("since")
        issues = ops.list_issues_for_user(
            session, user_id, state=state, sort=sort, direction=direction,
            since=since, per_page=per_page, page=page,
        )
        return JSONResponse(serialize_issue_list(issues))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_user_issues(request: Request) -> JSONResponse:
    """GET /user/issues — list user account issues."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        per_page, page = _page_params(request)
        state = request.query_params.get("state", "open")
        sort = request.query_params.get("sort", "created")
        direction = request.query_params.get("direction", "desc")
        since = request.query_params.get("since")
        issues = ops.list_issues_for_user(
            session, user_id, state=state, sort=sort, direction=direction,
            since=since, per_page=per_page, page=page,
        )
        return JSONResponse(serialize_issue_list(issues))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_repo_issues(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues — list repository issues."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        per_page, page = _page_params(request)
        state = request.query_params.get("state", "open")
        sort = request.query_params.get("sort", "created")
        direction = request.query_params.get("direction", "desc")
        since = request.query_params.get("since")
        assignee = request.query_params.get("assignee")
        creator = request.query_params.get("creator")
        milestone = request.query_params.get("milestone")
        labels = request.query_params.get("labels")
        issues = ops.list_issues(
            session, owner=owner, repo=repo, state=state, sort=sort,
            direction=direction, since=since, assignee=assignee,
            creator=creator, milestone=milestone, labels=labels,
            per_page=per_page, page=page,
        )
        return JSONResponse(serialize_issue_list(issues))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_issue_handler(request: Request) -> JSONResponse:
    """POST /repos/{owner}/{repo}/issues — create an issue."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        body = await _parse_json_body(request)
        if not body.get("title"):
            raise unprocessable_entity("Validation Failed", errors=[
                {"resource": "Issue", "field": "title", "code": "missing_field"},
            ])
        issue = ops.create_issue(session, owner, repo, body, user_id)
        return JSONResponse(serialize_issue(issue), status_code=status.HTTP_201_CREATED)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_issue_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number} — get an issue."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        issue = ops.get_issue(session, owner, repo, issue_number)
        if issue is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue(issue))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_issue_handler(request: Request) -> JSONResponse:
    """PATCH /repos/{owner}/{repo}/issues/{issue_number} — update an issue."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        issue = ops.update_issue(session, owner, repo, issue_number, body)
        if issue is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue(issue))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Issue comments
# ---------------------------------------------------------------------------


async def list_repo_issue_comments(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/comments — list issue comments for a repository."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        per_page, page = _page_params(request)
        sort = request.query_params.get("sort", "created")
        direction = request.query_params.get("direction", "desc")
        since = request.query_params.get("since")
        comments = ops.list_issue_comments_for_repo(
            session, owner, repo, sort=sort, direction=direction,
            since=since, per_page=per_page, page=page,
        )
        return JSONResponse(serialize_ic_list(comments))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_issue_comment_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/comments/{comment_id} — get an issue comment."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        comment_id = int(request.path_params["comment_id"])
        comment = ops.get_issue_comment(session, owner, repo, comment_id)
        if comment is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_ic(comment))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_issue_comment_handler(request: Request) -> JSONResponse:
    """PATCH /repos/{owner}/{repo}/issues/comments/{comment_id} — update an issue comment."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        comment_id = int(request.path_params["comment_id"])
        body = await _parse_json_body(request)
        comment_body = body.get("body")
        if not comment_body:
            raise unprocessable_entity("Validation Failed", errors=[
                {"resource": "IssueComment", "field": "body", "code": "missing_field"},
            ])
        comment = ops.update_issue_comment(session, owner, repo, comment_id, comment_body)
        if comment is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_ic(comment))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_issue_comment_handler(request: Request) -> JSONResponse:
    """DELETE /repos/{owner}/{repo}/issues/comments/{comment_id} — delete an issue comment."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        comment_id = int(request.path_params["comment_id"])
        deleted = ops.delete_issue_comment(session, owner, repo, comment_id)
        if not deleted:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def pin_issue_comment_handler(request: Request) -> JSONResponse:
    """PUT /repos/{owner}/{repo}/issues/comments/{comment_id}/pin — pin an issue comment."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        comment_id = int(request.path_params["comment_id"])
        comment = ops.pin_issue_comment(session, owner, repo, comment_id, user_id)
        if comment is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_ic(comment))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def unpin_issue_comment_handler(request: Request) -> JSONResponse:
    """DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}/pin — unpin an issue comment."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        comment_id = int(request.path_params["comment_id"])
        result = ops.unpin_issue_comment(session, owner, repo, comment_id)
        if not result:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_issue_comment_reactions_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions — list reactions for an issue comment."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        comment_id = int(request.path_params["comment_id"])
        per_page, page = _page_params(request)
        content = request.query_params.get("content")
        reactions = ops.list_issue_comment_reactions(
            session, owner, repo, comment_id, content=content,
            per_page=per_page, page=page,
        )
        if reactions is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_reaction_list(reactions))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_issue_comment_reaction_handler(request: Request) -> JSONResponse:
    """POST /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions — create reaction for an issue comment."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        comment_id = int(request.path_params["comment_id"])
        body = await _parse_json_body(request)
        content = body.get("content")
        if not content:
            raise unprocessable_entity("Validation Failed", errors=[
                {"resource": "Reaction", "field": "content", "code": "missing_field"},
            ])
        reaction, created = ops.create_issue_comment_reaction(
            session, owner, repo, comment_id, content, user_id,
        )
        if reaction is None:
            raise unprocessable_entity("Validation Failed")
        code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return JSONResponse(serialize_reaction(reaction), status_code=code)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_issue_comment_reaction_handler(request: Request) -> JSONResponse:
    """DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions/{reaction_id}."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        comment_id = int(request.path_params["comment_id"])
        reaction_id = int(request.path_params["reaction_id"])
        ops.delete_issue_comment_reaction(session, owner, repo, comment_id, reaction_id)
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Issue events
# ---------------------------------------------------------------------------


async def list_repo_issue_events(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/events — list issue events for a repository."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        per_page, page = _page_params(request)
        events = ops.list_issue_events_for_repo(session, owner, repo, per_page=per_page, page=page)
        return JSONResponse(serialize_issue_event_list(events))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_issue_event_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/events/{event_id} — get an issue event."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        event_id = int(request.path_params["event_id"])
        event = ops.get_issue_event(session, owner, repo, event_id)
        if event is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue_event(event))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Issue sub-resources (per-issue)
# ---------------------------------------------------------------------------


async def list_issue_comments_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number}/comments — list issue comments."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        per_page, page = _page_params(request)
        since = request.query_params.get("since")
        comments = ops.list_issue_comments_for_issue(
            session, owner, repo, issue_number, since=since,
            per_page=per_page, page=page,
        )
        if comments is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_ic_list(comments))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_issue_comment_handler(request: Request) -> JSONResponse:
    """POST /repos/{owner}/{repo}/issues/{issue_number}/comments — create an issue comment."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        comment_body = body.get("body")
        if not comment_body:
            raise unprocessable_entity("Validation Failed", errors=[
                {"resource": "IssueComment", "field": "body", "code": "missing_field"},
            ])
        comment = ops.create_issue_comment(session, owner, repo, issue_number, comment_body, user_id)
        if comment is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_ic(comment), status_code=status.HTTP_201_CREATED)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_issue_events_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number}/events — list issue events."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        per_page, page = _page_params(request)
        events = ops.list_issue_events_for_issue(
            session, owner, repo, issue_number, per_page=per_page, page=page,
        )
        if events is None:
            raise gone("Gone")
        return JSONResponse(serialize_issue_event_list(events))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_issue_labels_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number}/labels — list labels for an issue."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        per_page, page = _page_params(request)
        labels = ops.list_labels_for_issue(session, owner, repo, issue_number, per_page=per_page, page=page)
        if labels is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_label_list(labels))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_issue_labels_handler(request: Request) -> JSONResponse:
    """POST /repos/{owner}/{repo}/issues/{issue_number}/labels — add labels to an issue."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        labels = ops.add_labels_to_issue(session, owner, repo, issue_number, body)
        if labels is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_label_list(labels))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def set_issue_labels_handler(request: Request) -> JSONResponse:
    """PUT /repos/{owner}/{repo}/issues/{issue_number}/labels — set labels for an issue."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        labels = ops.set_labels_on_issue(session, owner, repo, issue_number, body)
        if labels is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_label_list(labels))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_issue_label_handler(request: Request) -> JSONResponse:
    """DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels/{name} — remove a label from an issue."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        label_name = request.path_params["name"]
        labels = ops.remove_label_from_issue(session, owner, repo, issue_number, label_name)
        if labels is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_label_list(labels))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_all_issue_labels_handler(request: Request) -> JSONResponse:
    """DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels — remove all labels."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        result = ops.remove_all_labels_from_issue(session, owner, repo, issue_number)
        if result is None:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def lock_issue_handler(request: Request) -> JSONResponse:
    """PUT /repos/{owner}/{repo}/issues/{issue_number}/lock — lock an issue."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = {}
        try:
            body = await request.json()
        except Exception:
            pass
        lock_reason = body.get("lock_reason") if body else None
        issue = ops.lock_issue(session, owner, repo, issue_number, lock_reason)
        if issue is None:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def unlock_issue_handler(request: Request) -> JSONResponse:
    """DELETE /repos/{owner}/{repo}/issues/{issue_number}/lock — unlock an issue."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        issue = ops.unlock_issue(session, owner, repo, issue_number)
        if issue is None:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_issue_reactions_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number}/reactions — list reactions for an issue."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        per_page, page = _page_params(request)
        content = request.query_params.get("content")
        reactions = ops.list_issue_reactions(
            session, owner, repo, issue_number, content=content,
            per_page=per_page, page=page,
        )
        if reactions is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_reaction_list(reactions))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_issue_reaction_handler(request: Request) -> JSONResponse:
    """POST /repos/{owner}/{repo}/issues/{issue_number}/reactions — create reaction for an issue."""
    try:
        session = _session(request)
        user_id = _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        content = body.get("content")
        if not content:
            raise unprocessable_entity("Validation Failed", errors=[
                {"resource": "Reaction", "field": "content", "code": "missing_field"},
            ])
        reaction, created = ops.create_issue_reaction(
            session, owner, repo, issue_number, content, user_id,
        )
        if reaction is None:
            raise unprocessable_entity("Validation Failed")
        code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return JSONResponse(serialize_reaction(reaction), status_code=code)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_issue_reaction_handler(request: Request) -> JSONResponse:
    """DELETE /repos/{owner}/{repo}/issues/{issue_number}/reactions/{reaction_id}."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        reaction_id = int(request.path_params["reaction_id"])
        ops.delete_issue_reaction(session, owner, repo, issue_number, reaction_id)
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_issue_timeline_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number}/timeline — list timeline events."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        per_page, page = _page_params(request)
        # Timeline is composed from events and comments
        events = ops.list_issue_events_for_issue(
            session, owner, repo, issue_number, per_page=per_page, page=page,
        )
        if events is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue_event_list(events))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Issue dependencies
# ---------------------------------------------------------------------------


async def list_issue_deps_blocked_by(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        per_page, page = _page_params(request)
        issues = ops.list_issue_dependencies_blocked_by(
            session, owner, repo, issue_number, per_page=per_page, page=page,
        )
        if issues is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue_list(issues))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_issue_dep_blocked_by(request: Request) -> JSONResponse:
    """POST /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        issue_id = body.get("issue_id")
        if issue_id is None:
            raise unprocessable_entity("Validation Failed")
        issue = ops.add_issue_dependency(session, owner, repo, issue_number, issue_id)
        if issue is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue(issue), status_code=status.HTTP_201_CREATED)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_issue_dep_blocked_by(request: Request) -> JSONResponse:
    """DELETE /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by/{issue_id}."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        issue_id = int(request.path_params["issue_id"])
        issue = ops.remove_issue_dependency(session, owner, repo, issue_number, issue_id)
        if issue is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue(issue))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def list_issue_deps_blocking(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocking."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        per_page, page = _page_params(request)
        issues = ops.list_issue_dependencies_blocking(
            session, owner, repo, issue_number, per_page=per_page, page=page,
        )
        if issues is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue_list(issues))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Sub-issues
# ---------------------------------------------------------------------------


async def list_sub_issues_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number}/sub_issues — list sub-issues."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        per_page, page = _page_params(request)
        issues = ops.list_sub_issues(
            session, owner, repo, issue_number, per_page=per_page, page=page,
        )
        if issues is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue_list(issues))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_sub_issue_handler(request: Request) -> JSONResponse:
    """POST /repos/{owner}/{repo}/issues/{issue_number}/sub_issues — add sub-issue."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        sub_issue_id = body.get("sub_issue_id")
        if sub_issue_id is None:
            raise unprocessable_entity("Validation Failed")
        replace_parent = body.get("replace_parent", False)
        issue = ops.add_sub_issue(session, owner, repo, issue_number, sub_issue_id, replace_parent)
        if issue is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue(issue), status_code=status.HTTP_201_CREATED)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def remove_sub_issue_handler(request: Request) -> JSONResponse:
    """DELETE /repos/{owner}/{repo}/issues/{issue_number}/sub_issue — remove sub-issue."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        sub_issue_id = body.get("sub_issue_id")
        if sub_issue_id is None:
            raise bad_request("Missing sub_issue_id")
        issue = ops.remove_sub_issue(session, owner, repo, issue_number, sub_issue_id)
        if issue is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue(issue))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def reprioritize_sub_issue_handler(request: Request) -> JSONResponse:
    """PATCH /repos/{owner}/{repo}/issues/{issue_number}/sub_issues/priority — reprioritize sub-issue."""
    try:
        session = _session(request)
        _principal_user_id(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        sub_issue_id = body.get("sub_issue_id")
        if sub_issue_id is None:
            raise unprocessable_entity("Validation Failed")
        issue = ops.reprioritize_sub_issue(
            session, owner, repo, issue_number, sub_issue_id,
            after_id=body.get("after_id"), before_id=body.get("before_id"),
        )
        if issue is None:
            raise not_found("Not Found")
        return JSONResponse(serialize_issue(issue))
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Issue field values (repository_id-based endpoints)
# ---------------------------------------------------------------------------


async def list_issue_field_values_handler(request: Request) -> JSONResponse:
    """GET /repos/{owner}/{repo}/issues/{issue_number}/issue-field-values."""
    try:
        session = _session(request)
        owner = request.path_params["owner"]
        repo = request.path_params["repo"]
        issue_number = int(request.path_params["issue_number"])
        per_page, page = _page_params(request)
        field_values = ops.list_issue_field_values(
            session, owner, repo, issue_number, per_page=per_page, page=page,
        )
        if field_values is None:
            raise not_found("Not Found")
        return JSONResponse(field_values)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def set_issue_field_values_handler(request: Request) -> JSONResponse:
    """PUT /repositories/{repository_id}/issues/{issue_number}/issue-field-values."""
    try:
        session = _session(request)
        _principal_user_id(request)
        repository_id = int(request.path_params["repository_id"])
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        field_values = body.get("issue_field_values", [])
        result = ops.set_issue_field_values(session, repository_id, issue_number, field_values)
        if result is None:
            raise not_found("Not Found")
        return JSONResponse(result)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def add_issue_field_values_handler(request: Request) -> JSONResponse:
    """POST /repositories/{repository_id}/issues/{issue_number}/issue-field-values."""
    try:
        session = _session(request)
        _principal_user_id(request)
        repository_id = int(request.path_params["repository_id"])
        issue_number = int(request.path_params["issue_number"])
        body = await _parse_json_body(request)
        field_values = body.get("issue_field_values", [])
        result = ops.add_issue_field_values(session, repository_id, issue_number, field_values)
        if result is None:
            raise not_found("Not Found")
        return JSONResponse(result)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_issue_field_value_handler(request: Request) -> JSONResponse:
    """DELETE /repositories/{repository_id}/issues/{issue_number}/issue-field-values/{issue_field_id}."""
    try:
        session = _session(request)
        _principal_user_id(request)
        repository_id = int(request.path_params["repository_id"])
        issue_number = int(request.path_params["issue_number"])
        issue_field_id = int(request.path_params["issue_field_id"])
        deleted = ops.delete_issue_field_value(session, repository_id, issue_number, issue_field_id)
        if not deleted:
            raise not_found("Not Found")
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Search issues
# ---------------------------------------------------------------------------


async def search_issues_handler(request: Request) -> JSONResponse:
    """GET /search/issues — search issues and pull requests."""
    try:
        session = _session(request)
        query = request.query_params.get("q", "")
        per_page, page = _page_params(request)
        sort = request.query_params.get("sort")
        order = request.query_params.get("order", "desc")
        items, total_count = ops.search_issues(
            session, query, sort=sort, order=order, per_page=per_page, page=page,
        )
        return JSONResponse({
            "total_count": total_count,
            "incomplete_results": False,
            "items": [serialize_issue_search_result(item) for item in items],
        })
    except AppAPIError as exc:
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
    # --- Gist endpoints ---
    # Fixed paths first
    Route("/gists/public", list_public_gists, methods=["GET"]),
    Route("/gists/starred", list_starred_gists, methods=["GET"]),
    # Collection + create
    Route("/gists", list_gists, methods=["GET"]),
    Route("/gists", create_gist, methods=["POST"]),
    # Gist sub-resources (fixed sub-paths before parameterized)
    Route("/gists/{gist_id}/comments/{comment_id}", get_gist_comment, methods=["GET"]),
    Route("/gists/{gist_id}/comments/{comment_id}", update_gist_comment, methods=["PATCH"]),
    Route("/gists/{gist_id}/comments/{comment_id}", delete_gist_comment, methods=["DELETE"]),
    Route("/gists/{gist_id}/comments", list_gist_comments, methods=["GET"]),
    Route("/gists/{gist_id}/comments", create_gist_comment, methods=["POST"]),
    Route("/gists/{gist_id}/commits", list_gist_commits, methods=["GET"]),
    Route("/gists/{gist_id}/forks", list_gist_forks, methods=["GET"]),
    Route("/gists/{gist_id}/forks", fork_gist, methods=["POST"]),
    Route("/gists/{gist_id}/star", check_gist_star, methods=["GET"]),
    Route("/gists/{gist_id}/star", star_gist, methods=["PUT"]),
    Route("/gists/{gist_id}/star", unstar_gist, methods=["DELETE"]),
    # Gist revision (must come before single-gist GET to avoid conflict — but both use {gist_id})
    Route("/gists/{gist_id}/{sha}", get_gist_revision, methods=["GET"]),
    # Single gist CRUD
    Route("/gists/{gist_id}", get_gist, methods=["GET"]),
    Route("/gists/{gist_id}", update_gist, methods=["PATCH"]),
    Route("/gists/{gist_id}", delete_gist, methods=["DELETE"]),
    # User gists
    Route("/users/{username}/gists", list_user_gists, methods=["GET"]),

    # --- Issue endpoints ---
    # Top-level issue list endpoints
    Route("/issues", list_authenticated_user_issues, methods=["GET"]),
    Route("/user/issues", list_user_issues, methods=["GET"]),
    Route("/orgs/{org}/issues", list_org_issues, methods=["GET"]),
    Route("/search/issues", search_issues_handler, methods=["GET"]),

    # Repo-level issue comment endpoints (fixed paths before parameterized)
    Route("/repos/{owner}/{repo}/issues/comments/{comment_id}/pin", pin_issue_comment_handler, methods=["PUT"]),
    Route("/repos/{owner}/{repo}/issues/comments/{comment_id}/pin", unpin_issue_comment_handler, methods=["DELETE"]),
    Route("/repos/{owner}/{repo}/issues/comments/{comment_id}/reactions/{reaction_id}", delete_issue_comment_reaction_handler, methods=["DELETE"]),
    Route("/repos/{owner}/{repo}/issues/comments/{comment_id}/reactions", list_issue_comment_reactions_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/comments/{comment_id}/reactions", create_issue_comment_reaction_handler, methods=["POST"]),
    Route("/repos/{owner}/{repo}/issues/comments/{comment_id}", get_issue_comment_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/comments/{comment_id}", update_issue_comment_handler, methods=["PATCH"]),
    Route("/repos/{owner}/{repo}/issues/comments/{comment_id}", delete_issue_comment_handler, methods=["DELETE"]),
    Route("/repos/{owner}/{repo}/issues/comments", list_repo_issue_comments, methods=["GET"]),

    # Repo-level issue event endpoints
    Route("/repos/{owner}/{repo}/issues/events/{event_id}", get_issue_event_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/events", list_repo_issue_events, methods=["GET"]),

    # Per-issue sub-resources
    Route("/repos/{owner}/{repo}/issues/{issue_number}/comments", list_issue_comments_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/comments", create_issue_comment_handler, methods=["POST"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by/{issue_id}", remove_issue_dep_blocked_by, methods=["DELETE"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by", list_issue_deps_blocked_by, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by", add_issue_dep_blocked_by, methods=["POST"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocking", list_issue_deps_blocking, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/events", list_issue_events_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/issue-field-values", list_issue_field_values_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/labels/{name}", remove_issue_label_handler, methods=["DELETE"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/labels", list_issue_labels_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/labels", add_issue_labels_handler, methods=["POST"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/labels", set_issue_labels_handler, methods=["PUT"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/labels", remove_all_issue_labels_handler, methods=["DELETE"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/lock", lock_issue_handler, methods=["PUT"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/lock", unlock_issue_handler, methods=["DELETE"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/reactions/{reaction_id}", delete_issue_reaction_handler, methods=["DELETE"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/reactions", list_issue_reactions_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/reactions", create_issue_reaction_handler, methods=["POST"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/sub_issues/priority", reprioritize_sub_issue_handler, methods=["PATCH"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/sub_issues", list_sub_issues_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/sub_issues", add_sub_issue_handler, methods=["POST"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/sub_issue", remove_sub_issue_handler, methods=["DELETE"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}/timeline", list_issue_timeline_handler, methods=["GET"]),

    # Single issue CRUD
    Route("/repos/{owner}/{repo}/issues/{issue_number}", get_issue_handler, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues/{issue_number}", update_issue_handler, methods=["PATCH"]),

    # Issue collection + create
    Route("/repos/{owner}/{repo}/issues", list_repo_issues, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues", create_issue_handler, methods=["POST"]),

    # Repository-ID based issue field value endpoints
    Route("/repositories/{repository_id}/issues/{issue_number}/issue-field-values/{issue_field_id}", delete_issue_field_value_handler, methods=["DELETE"]),
    Route("/repositories/{repository_id}/issues/{issue_number}/issue-field-values", set_issue_field_values_handler, methods=["PUT"]),
    Route("/repositories/{repository_id}/issues/{issue_number}/issue-field-values", add_issue_field_values_handler, methods=["POST"]),

    # --- Catch-all — MUST be the last entry ---
    Route(
        "/{_unknown_path:path}",
        unknown_endpoint,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
    ),
]
