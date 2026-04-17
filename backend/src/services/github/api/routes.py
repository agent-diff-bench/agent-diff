"""GitHub REST routes.

Mounted at ``/api/env/{env_id}/services/github``. Paths mirror
``https://api.github.com`` so existing GitHub clients work against the
replica by swapping the base URL.
"""

from __future__ import annotations

import json
import logging
from typing import Any, List, Optional

from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from src.services.github.database import operations as ops
from src.services.github.database.schema import Issue, Repository, User

logger = logging.getLogger(__name__)


def _session(request: Request) -> Session:
    session = getattr(request.state, "db_session", None)
    if session is None:
        raise RuntimeError("IsolationMiddleware did not attach a db_session")
    return session


def _error(status_code: int, message: str, *, doc_url: Optional[str] = None) -> Response:
    body: dict[str, Any] = {
        "message": message,
        "documentation_url": doc_url or "https://docs.github.com/rest",
        "status": str(status_code),
    }
    return JSONResponse(body, status_code=status_code)


def _principal(request: Request) -> Optional[User]:
    session = _session(request)
    user_id = getattr(request.state, "impersonate_user_id", None)
    if user_id:
        u = ops.get_user_by_id(session, str(user_id))
        if u:
            return u
    email = getattr(request.state, "impersonate_email", None)
    if email:
        u = ops.get_user_by_email(session, email)
        if u:
            return u
        u = ops.get_user_by_login(session, email)
        if u:
            return u
    return None


def _require_principal(request: Request) -> User | Response:
    user = _principal(request)
    if user is None:
        return _error(401, "Requires authentication")
    return user


def _require_repo(session: Session, owner: str, repo: str) -> Repository | Response:
    r = ops.get_repo(session, owner, repo)
    if r is None:
        return _error(404, "Not Found")
    return r


def _require_issue(
    session: Session, repo: Repository, number: int, *, expect_pr: Optional[bool] = None
) -> Issue | Response:
    issue = ops.get_issue(session, repo, number)
    if issue is None:
        return _error(404, "Not Found")
    if expect_pr is True and not issue.is_pull_request:
        return _error(404, "Not Found")
    if expect_pr is False and issue.is_pull_request:
        return _error(
            404,
            "Not Found — use the pull requests endpoint for this resource",
        )
    return issue


async def _json_body(request: Request) -> dict | Response:
    try:
        raw = await request.body()
        if not raw:
            return {}
        return json.loads(raw)
    except json.JSONDecodeError:
        return _error(400, "Problems parsing JSON")


def _resolve_users(session: Session, logins: List[str]) -> List[User]:
    users: List[User] = []
    for login in logins:
        u = ops.get_user_by_login(session, login)
        if u:
            users.append(u)
    return users


def _resolve_labels(session: Session, repo: Repository, names: List[str]):
    labels = []
    for name in names:
        lbl = ops.get_label(session, repo, name)
        if lbl:
            labels.append(lbl)
    return labels


# Repository metadata

async def get_repo_route(request: Request) -> Response:
    session = _session(request)
    result = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(result, Response):
        return result
    return JSONResponse(result.to_dict())


# Labels

async def list_labels_route(request: Request) -> Response:
    session = _session(request)
    result = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(result, Response):
        return result
    labels = ops.list_labels(session, result)
    return JSONResponse([lbl.to_dict() for lbl in labels])


async def create_label_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    name = body.get("name")
    if not name:
        return _error(422, "Validation Failed: name is required")
    if ops.get_label(session, repo, name):
        return _error(422, "Validation Failed: label already exists")
    label = ops.create_label(
        session,
        repo,
        name=name,
        color=body.get("color", "ededed"),
        description=body.get("description"),
    )
    return JSONResponse(label.to_dict(), status_code=201)


async def get_label_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    label = ops.get_label(session, repo, request.path_params["name"])
    if label is None:
        return _error(404, "Not Found")
    return JSONResponse(label.to_dict())


async def update_label_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    label = ops.get_label(session, repo, request.path_params["name"])
    if label is None:
        return _error(404, "Not Found")
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    ops.update_label(
        session,
        label,
        new_name=body.get("new_name"),
        color=body.get("color"),
        description=body.get("description"),
    )
    return JSONResponse(label.to_dict())


async def delete_label_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    label = ops.get_label(session, repo, request.path_params["name"])
    if label is None:
        return _error(404, "Not Found")
    ops.delete_label(session, label)
    return Response(status_code=204)


# Issues

async def list_issues_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    state = request.query_params.get("state", "open")
    issues = ops.list_issues(session, repo, state=state, include_pulls=True)
    return JSONResponse([i.to_issue_dict() for i in issues])


async def create_issue_route(request: Request) -> Response:
    session = _session(request)
    principal = _require_principal(request)
    if isinstance(principal, Response):
        return principal
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    title = body.get("title")
    if not title:
        return _error(422, "Validation Failed: title is required")
    assignees = _resolve_users(session, list(body.get("assignees", []) or []))
    if body.get("assignee") and not assignees:
        assignees = _resolve_users(session, [body["assignee"]])
    labels = _resolve_labels(session, repo, list(body.get("labels", []) or []))
    issue = ops.create_issue(
        session,
        repo,
        title=title,
        body=body.get("body"),
        user=principal,
        assignees=assignees,
        labels=labels,
    )
    return JSONResponse(issue.to_issue_dict(), status_code=201)


async def get_issue_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    return JSONResponse(issue.to_issue_dict())


async def update_issue_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    state = body.get("state")
    if state is not None and state not in ("open", "closed"):
        return _error(422, "Validation Failed: state must be open or closed")
    ops.update_issue(
        session,
        issue,
        title=body.get("title"),
        body=body.get("body"),
        state=state,
        state_reason=body.get("state_reason"),
        locked=body.get("locked"),
    )
    if "assignees" in body:
        assignees = _resolve_users(session, list(body.get("assignees") or []))
        for ia in list(issue.assignees):
            session.delete(ia)
        session.flush()
        ops.set_issue_assignees(session, issue, assignees)
    if "labels" in body:
        labels = _resolve_labels(session, repo, list(body.get("labels") or []))
        ops.set_issue_labels(session, issue, labels)
    return JSONResponse(issue.to_issue_dict())


# Issue assignees

async def add_assignees_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    users = _resolve_users(session, list(body.get("assignees", []) or []))
    ops.set_issue_assignees(session, issue, users)
    return JSONResponse(issue.to_issue_dict(), status_code=201)


async def remove_assignees_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    users = _resolve_users(session, list(body.get("assignees", []) or []))
    ops.remove_issue_assignees(session, issue, users)
    return JSONResponse(issue.to_issue_dict())


# Issue labels

async def list_issue_labels_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    return JSONResponse([il.label.to_dict() for il in issue.labels if il.label])


async def add_issue_labels_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    names = body.get("labels") if isinstance(body, dict) else body
    if not isinstance(names, list):
        return _error(422, "Validation Failed: labels must be an array")
    labels = _resolve_labels(session, repo, [str(n) for n in names])
    attached = ops.add_issue_labels(session, issue, labels)
    return JSONResponse([lbl.to_dict() for lbl in attached])


async def set_issue_labels_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    names = body.get("labels") if isinstance(body, dict) else body
    if not isinstance(names, list):
        return _error(422, "Validation Failed: labels must be an array")
    labels = _resolve_labels(session, repo, [str(n) for n in names])
    set_labels = ops.set_issue_labels(session, issue, labels)
    return JSONResponse([lbl.to_dict() for lbl in set_labels])


async def remove_single_label_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    label = ops.get_label(session, repo, request.path_params["name"])
    if label is None:
        return _error(404, "Not Found")
    ops.remove_issue_label(session, issue, label)
    return JSONResponse([il.label.to_dict() for il in issue.labels if il.label])


async def clear_issue_labels_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    ops.clear_issue_labels(session, issue)
    return Response(status_code=204)


# Issue comments

async def list_issue_comments_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    return JSONResponse([c.to_dict() for c in ops.list_issue_comments(session, issue)])


async def create_issue_comment_route(request: Request) -> Response:
    session = _session(request)
    principal = _require_principal(request)
    if isinstance(principal, Response):
        return principal
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["issue_number"])
    issue = _require_issue(session, repo, number)
    if isinstance(issue, Response):
        return issue
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    text = body.get("body")
    if not text:
        return _error(422, "Validation Failed: body is required")
    comment = ops.create_comment(session, issue, user=principal, body=text)
    return JSONResponse(comment.to_dict(), status_code=201)


async def get_comment_route(request: Request) -> Response:
    session = _session(request)
    comment = ops.get_comment(session, str(request.path_params["comment_id"]))
    if comment is None:
        return _error(404, "Not Found")
    return JSONResponse(comment.to_dict())


async def update_comment_route(request: Request) -> Response:
    session = _session(request)
    comment = ops.get_comment(session, str(request.path_params["comment_id"]))
    if comment is None:
        return _error(404, "Not Found")
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    text = body.get("body")
    if text is None:
        return _error(422, "Validation Failed: body is required")
    ops.update_comment(session, comment, body=text)
    return JSONResponse(comment.to_dict())


async def delete_comment_route(request: Request) -> Response:
    session = _session(request)
    comment = ops.get_comment(session, str(request.path_params["comment_id"]))
    if comment is None:
        return _error(404, "Not Found")
    ops.delete_comment(session, comment)
    return Response(status_code=204)


# Pull requests

async def list_pulls_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    state = request.query_params.get("state", "open")
    q = session.query(Issue).filter(
        Issue.repository_id == repo.id, Issue.is_pull_request.is_(True)
    )
    if state != "all":
        q = q.filter(Issue.state == state)
    pulls = q.order_by(Issue.number.desc()).all()
    return JSONResponse([p.to_pull_dict() for p in pulls])


async def create_pull_route(request: Request) -> Response:
    session = _session(request)
    principal = _require_principal(request)
    if isinstance(principal, Response):
        return principal
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    title = body.get("title")
    head = body.get("head")
    base = body.get("base")
    if not title or not head or not base:
        return _error(422, "Validation Failed: title, head, base are required")
    pr = ops.create_issue(
        session,
        repo,
        title=title,
        body=body.get("body"),
        user=principal,
        is_pull_request=True,
        head_ref=head,
        base_ref=base,
        draft=bool(body.get("draft", False)),
    )
    return JSONResponse(pr.to_pull_dict(), status_code=201)


async def get_pull_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["pull_number"])
    pr = _require_issue(session, repo, number, expect_pr=True)
    if isinstance(pr, Response):
        return pr
    return JSONResponse(pr.to_pull_dict())


async def update_pull_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["pull_number"])
    pr = _require_issue(session, repo, number, expect_pr=True)
    if isinstance(pr, Response):
        return pr
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    ops.update_issue(
        session,
        pr,
        title=body.get("title"),
        body=body.get("body"),
        state=body.get("state"),
    )
    if "base" in body:
        pr.base_ref = body["base"]
        session.flush()
    return JSONResponse(pr.to_pull_dict())


async def merge_pull_route(request: Request) -> Response:
    session = _session(request)
    principal = _require_principal(request)
    if isinstance(principal, Response):
        return principal
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["pull_number"])
    pr = _require_issue(session, repo, number, expect_pr=True)
    if isinstance(pr, Response):
        return pr
    if pr.merged:
        return _error(405, "Pull Request is already merged")
    if pr.state != "open":
        return _error(405, "Pull Request is not mergeable")
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    sha = body.get("sha") if isinstance(body, dict) else None
    ops.merge_pull(session, pr, merger=principal, commit_sha=sha)
    return JSONResponse(
        {
            "sha": pr.merge_commit_sha,
            "merged": True,
            "message": "Pull Request successfully merged",
        }
    )


async def requested_reviewers_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["pull_number"])
    pr = _require_issue(session, repo, number, expect_pr=True)
    if isinstance(pr, Response):
        return pr
    reviewers = [prr.user.to_mini_dict() for prr in pr.requested_reviewers if prr.user]
    return JSONResponse({"users": reviewers, "teams": []})


async def request_reviewers_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["pull_number"])
    pr = _require_issue(session, repo, number, expect_pr=True)
    if isinstance(pr, Response):
        return pr
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    users = _resolve_users(session, list(body.get("reviewers", []) or []))
    ops.set_requested_reviewers(session, pr, users)
    return JSONResponse(pr.to_pull_dict(), status_code=201)


async def remove_reviewers_route(request: Request) -> Response:
    session = _session(request)
    repo = _require_repo(
        session, request.path_params["owner"], request.path_params["repo"]
    )
    if isinstance(repo, Response):
        return repo
    number = int(request.path_params["pull_number"])
    pr = _require_issue(session, repo, number, expect_pr=True)
    if isinstance(pr, Response):
        return pr
    body = await _json_body(request)
    if isinstance(body, Response):
        return body
    users = _resolve_users(session, list(body.get("reviewers", []) or []))
    ops.remove_requested_reviewers(session, pr, users)
    return JSONResponse(pr.to_pull_dict())


routes = [
    # Repository metadata
    Route("/repos/{owner}/{repo}", get_repo_route, methods=["GET"]),
    # Labels
    Route("/repos/{owner}/{repo}/labels", list_labels_route, methods=["GET"]),
    Route("/repos/{owner}/{repo}/labels", create_label_route, methods=["POST"]),
    Route("/repos/{owner}/{repo}/labels/{name}", get_label_route, methods=["GET"]),
    Route("/repos/{owner}/{repo}/labels/{name}", update_label_route, methods=["PATCH"]),
    Route(
        "/repos/{owner}/{repo}/labels/{name}", delete_label_route, methods=["DELETE"]
    ),
    # Issues
    Route("/repos/{owner}/{repo}/issues", list_issues_route, methods=["GET"]),
    Route("/repos/{owner}/{repo}/issues", create_issue_route, methods=["POST"]),
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}",
        get_issue_route,
        methods=["GET"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}",
        update_issue_route,
        methods=["PATCH"],
    ),
    # Issue assignees
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}/assignees",
        add_assignees_route,
        methods=["POST"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}/assignees",
        remove_assignees_route,
        methods=["DELETE"],
    ),
    # Issue labels
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}/labels",
        list_issue_labels_route,
        methods=["GET"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}/labels",
        add_issue_labels_route,
        methods=["POST"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}/labels",
        set_issue_labels_route,
        methods=["PUT"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}/labels",
        clear_issue_labels_route,
        methods=["DELETE"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}/labels/{name}",
        remove_single_label_route,
        methods=["DELETE"],
    ),
    # Issue comments (also used by PRs — GitHub shares the route)
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}/comments",
        list_issue_comments_route,
        methods=["GET"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/{issue_number:int}/comments",
        create_issue_comment_route,
        methods=["POST"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/comments/{comment_id}",
        get_comment_route,
        methods=["GET"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/comments/{comment_id}",
        update_comment_route,
        methods=["PATCH"],
    ),
    Route(
        "/repos/{owner}/{repo}/issues/comments/{comment_id}",
        delete_comment_route,
        methods=["DELETE"],
    ),
    # Pull requests
    Route("/repos/{owner}/{repo}/pulls", list_pulls_route, methods=["GET"]),
    Route("/repos/{owner}/{repo}/pulls", create_pull_route, methods=["POST"]),
    Route(
        "/repos/{owner}/{repo}/pulls/{pull_number:int}",
        get_pull_route,
        methods=["GET"],
    ),
    Route(
        "/repos/{owner}/{repo}/pulls/{pull_number:int}",
        update_pull_route,
        methods=["PATCH"],
    ),
    Route(
        "/repos/{owner}/{repo}/pulls/{pull_number:int}/merge",
        merge_pull_route,
        methods=["PUT"],
    ),
    Route(
        "/repos/{owner}/{repo}/pulls/{pull_number:int}/requested_reviewers",
        requested_reviewers_route,
        methods=["GET"],
    ),
    Route(
        "/repos/{owner}/{repo}/pulls/{pull_number:int}/requested_reviewers",
        request_reviewers_route,
        methods=["POST"],
    ),
    Route(
        "/repos/{owner}/{repo}/pulls/{pull_number:int}/requested_reviewers",
        remove_reviewers_route,
        methods=["DELETE"],
    ),
]
