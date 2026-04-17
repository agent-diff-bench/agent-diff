"""Integration tests for the GitHub API replica.

These exercise the routes over an ASGI transport against a freshly cloned
``github_default`` schema. Each test gets its own environment so that
mutations don't bleed across cases.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.services.github.api.routes import routes as github_routes


AGENT_USER_ID = "10000001"  # agent-bot
ALICE_ID = "10000002"
BOB_ID = "10000003"
CAROL_ID = "10000004"
REPO = "acme/widgets"
BASE = f"/repos/{REPO}"


def _app_for(session_manager, env_id: str, impersonate_user_id: str) -> Starlette:
    async def add_db_session(request, call_next):
        with session_manager.with_session_for_environment(env_id) as session:
            request.state.db_session = session
            request.state.environment_id = env_id
            request.state.impersonate_user_id = impersonate_user_id
            request.state.impersonate_email = None
            return await call_next(request)

    middleware = [Middleware(BaseHTTPMiddleware, dispatch=add_db_session)]
    return Starlette(routes=github_routes, middleware=middleware)


@pytest_asyncio.fixture
async def github_client(
    test_user_id, core_isolation_engine, session_manager, environment_handler
):
    env = core_isolation_engine.create_environment(
        template_schema="github_default",
        ttl_seconds=3600,
        created_by=test_user_id,
        impersonate_user_id=AGENT_USER_ID,
    )
    try:
        app = _app_for(session_manager, env.environment_id, AGENT_USER_ID)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    finally:
        environment_handler.drop_schema(env.schema_name)


@pytest_asyncio.fixture
async def github_client_alice(
    test_user_id, core_isolation_engine, session_manager, environment_handler
):
    env = core_isolation_engine.create_environment(
        template_schema="github_default",
        ttl_seconds=3600,
        created_by=test_user_id,
        impersonate_user_id=ALICE_ID,
    )
    try:
        app = _app_for(session_manager, env.environment_id, ALICE_ID)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    finally:
        environment_handler.drop_schema(env.schema_name)


@pytest.mark.asyncio
class TestRepository:
    async def test_get_repo(self, github_client: AsyncClient):
        resp = await github_client.get(BASE)
        assert resp.status_code == 200
        data = resp.json()
        assert data["full_name"] == REPO
        assert data["owner"]["login"] == "alice"
        assert data["default_branch"] == "main"

    async def test_get_missing_repo(self, github_client: AsyncClient):
        resp = await github_client.get("/repos/acme/nope")
        assert resp.status_code == 404


@pytest.mark.asyncio
class TestLabels:
    async def test_list_labels(self, github_client: AsyncClient):
        resp = await github_client.get(f"{BASE}/labels")
        assert resp.status_code == 200
        names = {lbl["name"] for lbl in resp.json()}
        assert {"bug", "enhancement", "documentation"} <= names

    async def test_create_label(self, github_client: AsyncClient):
        resp = await github_client.post(
            f"{BASE}/labels",
            json={"name": "security", "color": "b60205", "description": "SEC"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "security"
        assert data["color"] == "b60205"

        # Duplicate create is 422
        dup = await github_client.post(f"{BASE}/labels", json={"name": "security"})
        assert dup.status_code == 422

    async def test_update_label(self, github_client: AsyncClient):
        resp = await github_client.patch(
            f"{BASE}/labels/bug",
            json={"color": "ff0000", "description": "Critical bug"},
        )
        assert resp.status_code == 200
        assert resp.json()["color"] == "ff0000"

    async def test_delete_label(self, github_client: AsyncClient):
        resp = await github_client.delete(f"{BASE}/labels/needs-triage")
        assert resp.status_code == 204
        missing = await github_client.get(f"{BASE}/labels/needs-triage")
        assert missing.status_code == 404


@pytest.mark.asyncio
class TestIssues:
    async def test_list_open_issues(self, github_client: AsyncClient):
        resp = await github_client.get(f"{BASE}/issues")
        assert resp.status_code == 200
        numbers = {i["number"] for i in resp.json()}
        # Both issues and PRs come back on /issues in real GitHub.
        assert {1, 2, 4, 5} <= numbers
        # Closed issue #3 should not appear by default.
        assert 3 not in numbers

    async def test_list_all_states(self, github_client: AsyncClient):
        resp = await github_client.get(f"{BASE}/issues", params={"state": "all"})
        numbers = {i["number"] for i in resp.json()}
        assert 3 in numbers  # closed

    async def test_get_issue(self, github_client: AsyncClient):
        resp = await github_client.get(f"{BASE}/issues/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["number"] == 1
        assert data["title"].startswith("Widget factory")
        assert any(lbl["name"] == "bug" for lbl in data["labels"])
        assert "pull_request" not in data

    async def test_create_issue(self, github_client: AsyncClient):
        resp = await github_client.post(
            f"{BASE}/issues",
            json={
                "title": "Widget factory leaks memory",
                "body": "Leaks heap on large inputs.",
                "labels": ["bug"],
                "assignees": ["bob"],
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["state"] == "open"
        assert data["user"]["login"] == "agent-bot"
        assert data["number"] == 6  # next after seeded 1-5
        assert any(lbl["name"] == "bug" for lbl in data["labels"])
        assert data["assignees"][0]["login"] == "bob"

    async def test_close_issue(self, github_client: AsyncClient):
        resp = await github_client.patch(
            f"{BASE}/issues/2",
            json={"state": "closed", "state_reason": "completed"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["state"] == "closed"
        assert data["state_reason"] == "completed"
        assert data["closed_at"] is not None

    async def test_update_issue_labels_replaces(self, github_client: AsyncClient):
        resp = await github_client.patch(
            f"{BASE}/issues/1",
            json={"labels": ["documentation"]},
        )
        assert resp.status_code == 200
        names = {lbl["name"] for lbl in resp.json()["labels"]}
        assert names == {"documentation"}


@pytest.mark.asyncio
class TestIssueLabels:
    async def test_add_labels(self, github_client: AsyncClient):
        resp = await github_client.post(
            f"{BASE}/issues/2/labels", json={"labels": ["needs-triage"]}
        )
        assert resp.status_code == 200
        names = {lbl["name"] for lbl in resp.json()}
        assert "needs-triage" in names

    async def test_set_labels_replaces(self, github_client: AsyncClient):
        resp = await github_client.put(
            f"{BASE}/issues/1/labels", json={"labels": ["documentation"]}
        )
        assert resp.status_code == 200
        assert [lbl["name"] for lbl in resp.json()] == ["documentation"]

    async def test_remove_single_label(self, github_client: AsyncClient):
        resp = await github_client.delete(f"{BASE}/issues/1/labels/needs-triage")
        assert resp.status_code == 200
        names = {lbl["name"] for lbl in resp.json()}
        assert "needs-triage" not in names
        assert "bug" in names  # still there

    async def test_clear_labels(self, github_client: AsyncClient):
        resp = await github_client.delete(f"{BASE}/issues/1/labels")
        assert resp.status_code == 204
        listing = await github_client.get(f"{BASE}/issues/1/labels")
        assert listing.json() == []


@pytest.mark.asyncio
class TestIssueAssignees:
    async def test_add_assignees(self, github_client: AsyncClient):
        resp = await github_client.post(
            f"{BASE}/issues/1/assignees", json={"assignees": ["bob", "carol"]}
        )
        assert resp.status_code == 201
        logins = {u["login"] for u in resp.json()["assignees"]}
        assert {"bob", "carol"} <= logins

    async def test_remove_assignees(self, github_client: AsyncClient):
        await github_client.post(
            f"{BASE}/issues/1/assignees", json={"assignees": ["bob"]}
        )
        resp = await github_client.request(
            "DELETE",
            f"{BASE}/issues/1/assignees",
            json={"assignees": ["bob"]},
        )
        assert resp.status_code == 200
        logins = {u["login"] for u in resp.json()["assignees"]}
        assert "bob" not in logins


@pytest.mark.asyncio
class TestIssueComments:
    async def test_list_comments(self, github_client: AsyncClient):
        resp = await github_client.get(f"{BASE}/issues/1/comments")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    async def test_create_comment(self, github_client: AsyncClient):
        resp = await github_client.post(
            f"{BASE}/issues/1/comments",
            json={"body": "I can reproduce on 0.5.0 too."},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["body"].startswith("I can reproduce")
        assert data["user"]["login"] == "agent-bot"

        # comments_count should have bumped
        issue = await github_client.get(f"{BASE}/issues/1")
        assert issue.json()["comments"] == 2

    async def test_update_comment(self, github_client_alice: AsyncClient):
        resp = await github_client_alice.patch(
            f"{BASE}/issues/comments/50000001",
            json={"body": "Reproduced on 0.4.1 and 0.5.0 — triaging."},
        )
        assert resp.status_code == 200
        assert "0.5.0" in resp.json()["body"]

    async def test_delete_comment(self, github_client_alice: AsyncClient):
        resp = await github_client_alice.delete(f"{BASE}/issues/comments/50000001")
        assert resp.status_code == 204
        listing = await github_client_alice.get(f"{BASE}/issues/1/comments")
        assert listing.json() == []


@pytest.mark.asyncio
class TestPullRequests:
    async def test_list_open_pulls(self, github_client: AsyncClient):
        resp = await github_client.get(f"{BASE}/pulls")
        assert resp.status_code == 200
        numbers = {p["number"] for p in resp.json()}
        assert numbers == {4, 5}

    async def test_get_pull(self, github_client: AsyncClient):
        resp = await github_client.get(f"{BASE}/pulls/4")
        assert resp.status_code == 200
        data = resp.json()
        assert data["head"]["ref"] == "bob/fix-empty-input"
        assert data["base"]["ref"] == "main"
        assert data["merged"] is False

    async def test_get_pull_rejects_issue(self, github_client: AsyncClient):
        # #1 is an issue, not a PR — /pulls should not find it.
        resp = await github_client.get(f"{BASE}/pulls/1")
        assert resp.status_code == 404

    async def test_create_pull(self, github_client: AsyncClient):
        resp = await github_client.post(
            f"{BASE}/pulls",
            json={
                "title": "Docs: clarify lifecycle hooks",
                "head": "agent-bot/lifecycle-docs",
                "base": "main",
                "body": "Expands README §3.",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["head"]["ref"] == "agent-bot/lifecycle-docs"
        assert data["user"]["login"] == "agent-bot"
        assert data["merged"] is False

    async def test_request_and_remove_reviewers(self, github_client: AsyncClient):
        resp = await github_client.post(
            f"{BASE}/pulls/4/requested_reviewers",
            json={"reviewers": ["alice", "carol"]},
        )
        assert resp.status_code == 201
        logins = {u["login"] for u in resp.json()["requested_reviewers"]}
        assert {"alice", "carol"} <= logins

        rm = await github_client.request(
            "DELETE",
            f"{BASE}/pulls/4/requested_reviewers",
            json={"reviewers": ["alice"]},
        )
        assert rm.status_code == 200
        logins = {u["login"] for u in rm.json()["requested_reviewers"]}
        assert "alice" not in logins

    async def test_merge_pull(self, github_client_alice: AsyncClient):
        resp = await github_client_alice.put(f"{BASE}/pulls/4/merge", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert data["merged"] is True
        assert data["sha"]

        detail = await github_client_alice.get(f"{BASE}/pulls/4")
        detail_data = detail.json()
        assert detail_data["merged"] is True
        assert detail_data["state"] == "closed"
        assert detail_data["merged_by"]["login"] == "alice"

    async def test_merge_already_merged_is_405(self, github_client_alice: AsyncClient):
        first = await github_client_alice.put(f"{BASE}/pulls/4/merge", json={})
        assert first.status_code == 200
        again = await github_client_alice.put(f"{BASE}/pulls/4/merge", json={})
        assert again.status_code == 405
