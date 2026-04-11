"""Golden tests that lock Slack replica behavior to live-doc examples.

These cover the shapes and error semantics called out in the official docs.
"""

from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient

from .test_slack_api import (
    CHANNEL_GENERAL,
    CHANNEL_RANDOM,
    USER_AGENT,
    USER_JOHN,
)


HIGHLIGHT_START = "\ue000"
HIGHLIGHT_END = "\ue001"


def _unique_name(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


@pytest.mark.asyncio
class TestSlackDocsGolden:
    async def test_chat_post_message_doc_shape(self, slack_client: AsyncClient) -> None:
        attachments = [{"text": "Doc attachment", "fallback": "Doc fallback"}]
        payload = {
            "channel": CHANNEL_GENERAL,
            "text": "Documented message",
            "attachments": attachments,
        }

        resp = await slack_client.post("/chat.postMessage", json=payload)
        assert resp.status_code == 200
        data = resp.json()

        assert set(data.keys()) == {"ok", "channel", "ts", "message"}
        assert data["ok"] is True
        assert data["channel"] == CHANNEL_GENERAL

        message = data["message"]
        assert message["type"] == "message"
        assert message["user"] == USER_AGENT
        assert message["ts"] == data["ts"]
        assert message["text"] == "Documented message"
        assert message["attachments"] == attachments

    async def test_chat_post_message_error_shape(
        self, slack_client: AsyncClient
    ) -> None:
        resp = await slack_client.post(
            "/chat.postMessage", json={"channel": CHANNEL_GENERAL}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data == {"ok": False, "error": "no_text"}

    async def test_chat_delete_error_shape(self, slack_client: AsyncClient) -> None:
        resp = await slack_client.post(
            "/chat.delete", json={"channel": CHANNEL_GENERAL, "ts": "9999999999.999999"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data == {"ok": False, "error": "message_not_found"}

    async def test_conversations_create_doc_shape(
        self, slack_client: AsyncClient
    ) -> None:
        channel_name = _unique_name("doc-channel")
        resp = await slack_client.post(
            "/conversations.create", json={"name": channel_name, "is_private": False}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True

        channel = data["channel"]
        expected_keys = {
            "id",
            "name",
            "is_channel",
            "is_group",
            "is_im",
            "created",
            "creator",
            "is_archived",
            "is_general",
            "unlinked",
            "name_normalized",
            "is_shared",
            "is_ext_shared",
            "is_org_shared",
            "pending_shared",
            "is_pending_ext_shared",
            "is_member",
            "is_private",
            "is_mpim",
            "topic",
            "purpose",
            "previous_names",
            "updated",
            "priority",
        }
        assert expected_keys <= channel.keys()
        assert channel["name"] == channel_name
        assert channel["topic"] == {"value": "", "creator": "", "last_set": 0}
        assert channel["purpose"] == {"value": "", "creator": "", "last_set": 0}

    async def test_conversations_join_warning_shape(
        self, slack_client: AsyncClient
    ) -> None:
        resp = await slack_client.post(
            "/conversations.join", json={"channel": CHANNEL_GENERAL}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert data["warning"] == "already_in_channel"
        assert data["response_metadata"] == {"warnings": ["already_in_channel"]}

    async def test_conversations_history_doc_shape(
        self, slack_client: AsyncClient
    ) -> None:
        resp = await slack_client.get(
            f"/conversations.history?channel={CHANNEL_GENERAL}&limit=2"
        )
        assert resp.status_code == 200
        data = resp.json()

        assert {
            "ok",
            "messages",
            "has_more",
            "pin_count",
            "response_metadata",
        } <= data.keys()
        assert data["ok"] is True
        assert isinstance(data["messages"], list)
        assert "next_cursor" in data["response_metadata"]
        if data["messages"]:
            first = data["messages"][0]
            assert {"type", "user", "text", "ts"} <= first.keys()

    async def test_conversations_replies_doc_shape(
        self, slack_client: AsyncClient
    ) -> None:
        parent_resp = await slack_client.post(
            "/chat.postMessage",
            json={"channel": CHANNEL_GENERAL, "text": "Docs thread root"},
        )
        parent_ts = parent_resp.json()["ts"]

        await slack_client.post(
            "/chat.postMessage",
            json={
                "channel": CHANNEL_GENERAL,
                "text": "Docs first reply",
                "thread_ts": parent_ts,
            },
        )
        await slack_client.post(
            "/chat.postMessage",
            json={
                "channel": CHANNEL_GENERAL,
                "text": "Docs second reply",
                "thread_ts": parent_ts,
            },
        )

        resp = await slack_client.get(
            f"/conversations.replies?channel={CHANNEL_GENERAL}&ts={parent_ts}&limit=10"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert {"messages", "has_more", "response_metadata"} <= data.keys()
        assert "next_cursor" in data["response_metadata"]

        messages = data["messages"]
        assert len(messages) >= 3

        root = messages[0]
        assert {
            "type",
            "user",
            "text",
            "ts",
            "thread_ts",
            "reply_count",
            "subscribed",
            "last_read",
            "unread_count",
        } <= root.keys()

        reply = messages[1]
        assert {
            "type",
            "user",
            "text",
            "ts",
            "thread_ts",
            "parent_user_id",
        } <= reply.keys()

    async def test_conversations_info_dm_shape(self, slack_client: AsyncClient) -> None:
        open_dm = await slack_client.post(
            "/conversations.open", json={"users": USER_JOHN, "return_im": True}
        )
        assert open_dm.status_code == 200
        dm_id = open_dm.json()["channel"]["id"]

        msg_resp = await slack_client.post(
            "/chat.postMessage",
            json={"channel": dm_id, "text": "Doc DM latest"},
        )
        assert msg_resp.status_code == 200
        dm_latest_ts = msg_resp.json()["ts"]

        resp = await slack_client.get(f"/conversations.info?channel={dm_id}")
        assert resp.status_code == 200
        data = resp.json()

        channel = data["channel"]
        assert channel["is_im"] is True
        assert channel["user"] == USER_JOHN
        assert "last_read" in channel
        assert "latest" in channel
        assert channel["latest"] is not None
        assert channel["latest"]["type"] == "message"
        assert channel["latest"]["ts"] == dm_latest_ts
        assert channel["last_read"] == dm_latest_ts
        assert channel["is_open"] is True

    async def test_conversations_leave_not_in_channel_shape(
        self, slack_client: AsyncClient, slack_client_john: AsyncClient
    ) -> None:
        channel_name = _unique_name("doc-leave")
        create_resp = await slack_client_john.post(
            "/conversations.create", json={"name": channel_name, "is_private": True}
        )
        assert create_resp.status_code == 200
        channel_id = create_resp.json()["channel"]["id"]

        resp = await slack_client.post(
            "/conversations.leave", json={"channel": channel_id}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data == {"ok": False, "not_in_channel": True}

    async def test_conversations_set_topic_doc_shape(
        self, slack_client: AsyncClient
    ) -> None:
        channel_name = _unique_name("doc-topic")
        create_resp = await slack_client.post(
            "/conversations.create", json={"name": channel_name, "is_private": False}
        )
        assert create_resp.status_code == 200
        channel_id = create_resp.json()["channel"]["id"]

        resp = await slack_client.post(
            "/conversations.setTopic",
            json={"channel": channel_id, "topic": "Golden topic"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data == {"ok": True}

    async def test_reactions_get_doc_shape(self, slack_client: AsyncClient) -> None:
        post_resp = await slack_client.post(
            "/chat.postMessage",
            json={"channel": CHANNEL_RANDOM, "text": "Reaction doc sample"},
        )
        assert post_resp.status_code == 200
        ts = post_resp.json()["ts"]

        add_resp = await slack_client.post(
            "/reactions.add",
            json={"name": "rocket", "channel": CHANNEL_RANDOM, "timestamp": ts},
        )
        assert add_resp.status_code == 200

        resp = await slack_client.get(
            f"/reactions.get?channel={CHANNEL_RANDOM}&timestamp={ts}"
        )
        assert resp.status_code == 200
        data = resp.json()

        assert data["ok"] is True
        assert data["type"] == "message"
        message = data["message"]
        assert {"type", "text", "user", "ts", "team"} <= message.keys()
        assert "reactions" in message
        reaction = message["reactions"][0]
        assert reaction == {"name": "rocket", "users": [USER_AGENT], "count": 1}

    async def test_users_info_doc_shape(self, slack_client: AsyncClient) -> None:
        resp = await slack_client.get(f"/users.info?user={USER_AGENT}")
        assert resp.status_code == 200
        user = resp.json()["user"]

        assert user["id"] == USER_AGENT
        assert user["team_id"]
        profile = user["profile"]
        assert {
            "real_name",
            "display_name",
            "image_24",
            "image_512",
            "email",
        } <= profile.keys()
        assert profile["team"] == user["team_id"]

    async def test_search_messages_doc_shape(self, slack_client: AsyncClient) -> None:
        term = _unique_name("docsearch")
        await slack_client.post(
            "/chat.postMessage",
            json={"channel": CHANNEL_GENERAL, "text": f"Golden search {term}"},
        )

        resp = await slack_client.get(
            f"/search.messages?query={term}&highlight=true&count=1"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True

        messages = data["messages"]
        assert {
            "matches",
            "pagination",
            "paging",
            "total",
            "response_metadata",
        } <= messages.keys()
        assert isinstance(messages["matches"], list)
        assert "next_cursor" in messages["response_metadata"]
        assert messages["pagination"]["per_page"] == 1

        match = messages["matches"][0]
        expected_match_keys = {
            "channel",
            "iid",
            "permalink",
            "team",
            "text",
            "ts",
            "type",
            "user",
            "username",
        }
        assert expected_match_keys <= match.keys()
        assert HIGHLIGHT_START in match["text"] and HIGHLIGHT_END in match["text"]

    async def test_auth_test_doc_shape(self, slack_client: AsyncClient) -> None:
        resp = await slack_client.post("/auth.test", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert {"user_id", "user", "team_id", "team"} <= data.keys()
        assert data["user_id"] == USER_AGENT

    async def test_chat_update_doc_shape(self, slack_client: AsyncClient) -> None:
        post_resp = await slack_client.post(
            "/chat.postMessage",
            json={"channel": CHANNEL_GENERAL, "text": "Original text for update"},
        )
        assert post_resp.status_code == 200
        ts = post_resp.json()["ts"]

        resp = await slack_client.post(
            "/chat.update",
            json={"channel": CHANNEL_GENERAL, "ts": ts, "text": "Updated text"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert {"ok", "channel", "ts", "text"} <= data.keys()
        assert data["text"] == "Updated text"

    async def test_conversations_archive_doc_shape(
        self, slack_client: AsyncClient
    ) -> None:
        channel_name = _unique_name("doc-archive")
        create_resp = await slack_client.post(
            "/conversations.create", json={"name": channel_name, "is_private": False}
        )
        assert create_resp.status_code == 200
        channel_id = create_resp.json()["channel"]["id"]

        resp = await slack_client.post(
            "/conversations.archive", json={"channel": channel_id}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True

    async def test_conversations_unarchive_doc_shape(
        self, slack_client: AsyncClient
    ) -> None:
        channel_name = _unique_name("doc-unarch")
        create_resp = await slack_client.post(
            "/conversations.create", json={"name": channel_name, "is_private": False}
        )
        assert create_resp.status_code == 200
        channel_id = create_resp.json()["channel"]["id"]

        await slack_client.post(
            "/conversations.archive", json={"channel": channel_id}
        )

        resp = await slack_client.post(
            "/conversations.unarchive", json={"channel": channel_id}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True

    async def test_conversations_rename_doc_shape(
        self, slack_client: AsyncClient
    ) -> None:
        channel_name = _unique_name("doc-rename")
        create_resp = await slack_client.post(
            "/conversations.create", json={"name": channel_name, "is_private": False}
        )
        assert create_resp.status_code == 200
        channel_id = create_resp.json()["channel"]["id"]

        new_name = _unique_name("doc-renamed")
        resp = await slack_client.post(
            "/conversations.rename",
            json={"channel": channel_id, "name": new_name},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert data["channel"]["name"] == new_name

    async def test_conversations_kick_doc_shape(
        self, slack_client: AsyncClient, slack_client_john: AsyncClient
    ) -> None:
        channel_name = _unique_name("doc-kick")
        create_resp = await slack_client.post(
            "/conversations.create", json={"name": channel_name, "is_private": False}
        )
        assert create_resp.status_code == 200
        channel_id = create_resp.json()["channel"]["id"]

        await slack_client.post(
            "/conversations.invite",
            json={"channel": channel_id, "users": USER_JOHN},
        )

        resp = await slack_client.post(
            "/conversations.kick",
            json={"channel": channel_id, "user": USER_JOHN},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True

    async def test_conversations_members_doc_shape(
        self, slack_client: AsyncClient
    ) -> None:
        resp = await slack_client.get(
            f"/conversations.members?channel={CHANNEL_GENERAL}&limit=10"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert "members" in data
        assert isinstance(data["members"], list)
        assert "response_metadata" in data

    async def test_users_list_doc_shape(self, slack_client: AsyncClient) -> None:
        resp = await slack_client.get("/users.list?limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert "members" in data
        assert isinstance(data["members"], list)
        if data["members"]:
            user = data["members"][0]
            assert {"id", "name", "profile"} <= user.keys()

    async def test_users_conversations_doc_shape(
        self, slack_client: AsyncClient
    ) -> None:
        resp = await slack_client.get(f"/users.conversations?user={USER_AGENT}&limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert "channels" in data
        assert isinstance(data["channels"], list)
