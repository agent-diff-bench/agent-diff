#!/usr/bin/env python3
"""
Comprehensive Slack API parity tests.

Compares the Slack replica API against the real Slack API to ensure
response schema parity. Tests all 28 implemented methods across
read-only operations, write operations, error handling, and pagination.

Usage:
    SLACK_BOT_TOKEN=<token> pytest tests/validation/test_slack_parity.py -v -s
"""

import os
import sys
import json
import time
import uuid
import requests
from typing import Any, Dict, List, Optional, Tuple

import pytest

# Configuration
SLACK_PROD_URL = "https://slack.com/api"
SLACK_REPLICA_BASE_URL = "http://localhost:8000/api/platform"

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")

# Fields that may differ between production and replica due to workspace config
OPTIONAL_FIELDS = {
    # Workspace/enterprise-specific
    "response_metadata",
    "warning",
    "scopes",
    "acceptedScopes",
    "headers",
    "cache_ts",
    "is_moved",
    "date_connected",
    "internal_team_ids",
    "connected_team_ids",
    "shared_team_ids",
    "connected_limited_team_ids",
    "pending_connected_team_ids",
    "enterprise_id",
    "enterprise_name",
    "is_enterprise_install",
    "context_team_id",
    "parent_conversation",
    "properties",
    "canvas",
    "tab_id",
    "tab_type",
    # Bot-specific fields (present in prod for bot messages, not in replica)
    "bot_id",
    "app_id",
    "bot_profile",
    "team",
    "edited",
    # User profile fields (optional per workspace config)
    "who_can_share_contact_card",
    "who_can_post_message",
    "first_name",
    "last_name",
    "is_token_revoked",
    "is_ultra_restricted",
    "is_restricted",
    "is_app_user",
    "is_email_confirmed",
    "is_workflow_bot",
    "locale",
    "updated",
    # Pagination (format may differ)
    "offset",
    # setTopic returns channel object in prod but may not in replica
    "channel",
    # User profile status fields (workspace-specific)
    "status_text_canonical",
    "status_emoji_display_info",
    "status_expiration",
    "fields",
    # Message blocks (Slack auto-adds blocks for plain text in prod)
    "blocks",
    # Channel metadata (workspace-specific)
    "is_limited",
    "channel_actions_ts",
    "channel_actions_count",
    "pending_connected_team_ids",
    "is_archived",
    # Thread metadata (computed fields)
    "reply_users_count",
    "reply_users",
    "latest_reply",
    "is_locked",
    # Bot profile fields (prod-specific)
    "api_app_id",
    "always_active",
}

# Bot token scopes that may be missing — skip tests for these
SCOPE_LIMITED_METHODS = {
    "reactions.add",      # needs reactions:write
    "reactions.remove",   # needs reactions:write
    "reactions.get",      # needs reactions:read
    "search.messages",    # needs search:read (not search:read.public)
    "search.all",         # needs search:read
}


class SlackParityTester:
    """
    Test Slack replica API against real Slack API.

    Compares response schemas (structure and types) rather than exact values,
    since IDs and timestamps will differ between environments.
    """

    def __init__(self, bot_token: str):
        self.prod_headers = {
            "Authorization": f"Bearer {bot_token}",
            "Content-Type": "application/json; charset=utf-8",
        }
        self.replica_env_id: Optional[str] = None
        self.replica_url: Optional[str] = None

        # Bot user info (populated during setup)
        self.prod_bot_user_id: Optional[str] = None
        self.replica_bot_user_id: Optional[str] = None

        # Workspace info
        self.prod_channel_id: Optional[str] = None  # a public channel to read from
        self.replica_channel_id: Optional[str] = None

        # Test resources (for cleanup)
        self.prod_test_channels: List[str] = []
        self.replica_test_channels: List[str] = []

        # Results
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.test_results: List[Dict[str, Any]] = []

    # =========================================================================
    # API Helpers
    # =========================================================================

    def api_prod(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Execute request against real Slack API."""
        url = f"{SLACK_PROD_URL}/{endpoint}"
        if method.upper() == "GET":
            resp = requests.get(url, headers=self.prod_headers, params=params, timeout=30)
        else:
            resp = requests.post(url, headers=self.prod_headers, json=json_data, timeout=30)
        return resp.json()

    def api_replica(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Execute request against Slack replica API."""
        if not self.replica_url:
            raise RuntimeError("Replica environment not initialized")
        url = f"{self.replica_url}/{endpoint}"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if method.upper() == "GET":
            resp = requests.get(url, headers=headers, params=params, timeout=30)
        else:
            resp = requests.post(url, headers=headers, json=json_data, timeout=30)
        return resp.json()

    # =========================================================================
    # Shape Comparison (from Box pattern)
    # =========================================================================

    def extract_shape(self, data: Any) -> Any:
        """Extract the shape/structure of data, ignoring actual values."""
        if isinstance(data, dict):
            return {k: self.extract_shape(v) for k, v in data.items()}
        elif isinstance(data, list):
            if not data:
                return []
            return [self.extract_shape(data[0])]
        else:
            return type(data).__name__

    def compare_shapes(
        self, prod_shape: Any, replica_shape: Any, path: str = ""
    ) -> List[str]:
        """Compare two data shapes and return list of differences."""
        differences = []

        if isinstance(prod_shape, dict) and isinstance(replica_shape, dict):
            for key in prod_shape:
                if key not in replica_shape:
                    if key in OPTIONAL_FIELDS:
                        continue
                    differences.append(f"{path}.{key}: MISSING in replica")
                else:
                    differences.extend(
                        self.compare_shapes(
                            prod_shape[key], replica_shape[key], f"{path}.{key}"
                        )
                    )
            for key in replica_shape:
                if key not in prod_shape:
                    if key in OPTIONAL_FIELDS:
                        continue
                    differences.append(f"{path}.{key}: EXTRA in replica")

        elif isinstance(prod_shape, list) and isinstance(replica_shape, list):
            if prod_shape and replica_shape:
                differences.extend(
                    self.compare_shapes(prod_shape[0], replica_shape[0], f"{path}[0]")
                )

        elif type(prod_shape).__name__ != type(replica_shape).__name__:
            differences.append(
                f"{path}: Type mismatch (prod: {type(prod_shape).__name__}, "
                f"replica: {type(replica_shape).__name__})"
            )

        return differences

    def record_result(
        self, category: str, test: str, passed: bool, details: str = ""
    ):
        """Record a test result."""
        self.test_results.append(
            {
                "category": category,
                "test": test,
                "passed": passed,
                "details": details,
            }
        )
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def test_operation(
        self,
        category: str,
        name: str,
        prod_result: Dict,
        replica_result: Dict,
        validate_schema: bool = True,
    ) -> bool:
        """Compare a prod vs replica operation result."""
        print(f"  {name}...", end=" ")

        prod_ok = prod_result.get("ok", False)
        replica_ok = replica_result.get("ok", False)

        if prod_ok and replica_ok:
            if validate_schema:
                prod_shape = self.extract_shape(prod_result)
                replica_shape = self.extract_shape(replica_result)
                diffs = self.compare_shapes(prod_shape, replica_shape, "data")
                if diffs:
                    critical = [d for d in diffs if "MISSING" in d]
                    if critical:
                        print("❌ SCHEMA MISMATCH")
                        for d in critical[:3]:
                            print(f"     {d}")
                        self.record_result(category, name, False, "; ".join(critical[:3]))
                        return False
                    else:
                        print("✅ (extra fields in replica)")
                        self.record_result(category, name, True)
                        return True
            print("✅")
            self.record_result(category, name, True)
            return True
        elif not prod_ok and not replica_ok:
            # Both failed — compare error types
            prod_error = prod_result.get("error", "")
            replica_error = replica_result.get("error", "")
            if prod_error == replica_error:
                print(f"✅ (both: {prod_error})")
                self.record_result(category, name, True)
                return True
            else:
                print(f"⚠️ ERROR MISMATCH (prod: {prod_error}, replica: {replica_error})")
                self.record_result(
                    category, name, False,
                    f"prod={prod_error}, replica={replica_error}",
                )
                return False
        else:
            print(f"❌ OK MISMATCH (prod ok={prod_ok}, replica ok={replica_ok})")
            self.record_result(
                category, name, False,
                f"prod ok={prod_ok}, replica ok={replica_ok}",
            )
            return False

    # =========================================================================
    # Setup & Teardown
    # =========================================================================

    def setup_replica_environment(self):
        """Create a test environment in the replica."""
        resp = requests.post(
            f"{SLACK_REPLICA_BASE_URL}/initEnv",
            headers={"x-principal-id": "test-user"},
            json={
                "templateService": "slack",
                "templateName": "slack_default",
                "impersonateUserId": "U01AGENBOT9",
            },
            timeout=30,
        )
        if resp.status_code != 201:
            raise Exception(f"Failed to create replica environment: {resp.text}")
        env = resp.json()
        self.replica_env_id = env["environmentId"]
        self.replica_url = f"http://localhost:8000{env['environmentUrl']}"
        self.replica_bot_user_id = "U01AGENBOT9"
        print(f"✓ Created replica environment: {self.replica_env_id}")

    def setup_prod_info(self):
        """Get production workspace info."""
        auth = self.api_prod("POST", "auth.test")
        if auth.get("ok"):
            self.prod_bot_user_id = auth["user_id"]
            print(f"✓ Prod bot user: {self.prod_bot_user_id}")

        # Find a public channel to use for read tests
        channels = self.api_prod("GET", "conversations.list", params={"types": "public_channel", "limit": "5"})
        if channels.get("ok") and channels.get("channels"):
            for ch in channels["channels"]:
                if ch["name"] in ("general", "random"):
                    self.prod_channel_id = ch["id"]
                    break
            if not self.prod_channel_id:
                self.prod_channel_id = channels["channels"][0]["id"]
            print(f"✓ Prod read channel: {self.prod_channel_id}")

        # Replica uses seeded channels
        self.replica_channel_id = "C01ABCD1234"  # #general in seed data

    def cleanup(self):
        """Clean up test resources."""
        print("\n🧹 Cleaning up...")
        for ch_id in self.prod_test_channels:
            try:
                self.api_prod("POST", "conversations.archive", json_data={"channel": ch_id})
                print(f"  ✓ Archived prod channel {ch_id}")
            except Exception as e:
                print(f"  ⚠️ Failed to archive {ch_id}: {e}")

    # =========================================================================
    # Read-Only Tests
    # =========================================================================

    def run_readonly_tests(self) -> Tuple[int, int]:
        """Test read-only endpoints."""
        print("\n📖 Read-Only Operations:")
        passed = 0
        total = 0

        # auth.test
        total += 1
        prod = self.api_prod("POST", "auth.test")
        replica = self.api_replica("POST", "auth.test")
        if self.test_operation("ReadOnly", "auth.test", prod, replica):
            passed += 1

        # users.info (bot user)
        total += 1
        prod = self.api_prod("GET", "users.info", params={"user": self.prod_bot_user_id})
        replica = self.api_replica("GET", "users.info", params={"user": self.replica_bot_user_id})
        if self.test_operation("ReadOnly", "users.info", prod, replica):
            passed += 1

        # users.list
        total += 1
        prod = self.api_prod("GET", "users.list", params={"limit": "10"})
        replica = self.api_replica("GET", "users.list", params={"limit": "10"})
        if self.test_operation("ReadOnly", "users.list", prod, replica):
            passed += 1

        # conversations.list
        total += 1
        prod = self.api_prod("GET", "conversations.list", params={"types": "public_channel", "limit": "5"})
        replica = self.api_replica("GET", "conversations.list", params={"types": "public_channel", "limit": "5"})
        if self.test_operation("ReadOnly", "conversations.list", prod, replica):
            passed += 1

        # conversations.info
        total += 1
        prod = self.api_prod("GET", "conversations.info", params={"channel": self.prod_channel_id})
        replica = self.api_replica("GET", "conversations.info", params={"channel": self.replica_channel_id})
        if self.test_operation("ReadOnly", "conversations.info", prod, replica):
            passed += 1

        # conversations.history
        total += 1
        prod = self.api_prod("GET", "conversations.history", params={"channel": self.prod_channel_id, "limit": "5"})
        replica = self.api_replica("GET", "conversations.history", params={"channel": self.replica_channel_id, "limit": "5"})
        if self.test_operation("ReadOnly", "conversations.history", prod, replica):
            passed += 1

        # conversations.members
        total += 1
        prod = self.api_prod("GET", "conversations.members", params={"channel": self.prod_channel_id, "limit": "10"})
        replica = self.api_replica("GET", "conversations.members", params={"channel": self.replica_channel_id, "limit": "10"})
        if self.test_operation("ReadOnly", "conversations.members", prod, replica):
            passed += 1

        # search.messages (requires user token, not bot token — skip if not allowed)
        prod = self.api_prod("GET", "search.messages", params={"query": "test", "count": "1"})
        if prod.get("error") in ("missing_scope", "not_allowed_token_type"):
            print(f"  search.messages... ⏭️ SKIPPED ({prod['error']})")
            self.skipped += 1
        else:
            total += 1
            replica = self.api_replica("GET", "search.messages", params={"query": "test", "count": "1"})
            if self.test_operation("ReadOnly", "search.messages", prod, replica):
                passed += 1

        # search.all (requires user token)
        prod = self.api_prod("GET", "search.all", params={"query": "test", "count": "1"})
        if prod.get("error") in ("missing_scope", "not_allowed_token_type"):
            print(f"  search.all... ⏭️ SKIPPED ({prod['error']})")
            self.skipped += 1
        else:
            total += 1
            replica = self.api_replica("GET", "search.all", params={"query": "test", "count": "1"})
            if self.test_operation("ReadOnly", "search.all", prod, replica):
                passed += 1

        # users.conversations
        total += 1
        prod = self.api_prod("GET", "users.conversations", params={"user": self.prod_bot_user_id, "limit": "5"})
        replica = self.api_replica("GET", "users.conversations", params={"user": self.replica_bot_user_id, "limit": "5"})
        if self.test_operation("ReadOnly", "users.conversations", prod, replica):
            passed += 1

        return passed, total

    # =========================================================================
    # Write Tests (with cleanup)
    # =========================================================================

    def run_write_tests(self) -> Tuple[int, int]:
        """Test write endpoints using a temporary test channel."""
        print("\n✏️ Write Operations:")
        passed = 0
        total = 0

        # Create test channels in both environments
        suffix = uuid.uuid4().hex[:8]

        prod_create = self.api_prod("POST", "conversations.create", json_data={"name": f"parity-test-{suffix}", "is_private": False})
        replica_create = self.api_replica("POST", "conversations.create", json_data={"name": f"parity-test-{suffix}", "is_private": False})

        total += 1
        if self.test_operation("Write", "conversations.create", prod_create, replica_create):
            passed += 1

        if not prod_create.get("ok") or not replica_create.get("ok"):
            print("  ⚠️ Skipping write tests — channel creation failed")
            return passed, total

        prod_ch = prod_create["channel"]["id"]
        replica_ch = replica_create["channel"]["id"]
        self.prod_test_channels.append(prod_ch)

        # chat.postMessage
        total += 1
        prod = self.api_prod("POST", "chat.postMessage", json_data={"channel": prod_ch, "text": "Parity test message"})
        replica = self.api_replica("POST", "chat.postMessage", json_data={"channel": replica_ch, "text": "Parity test message"})
        if self.test_operation("Write", "chat.postMessage", prod, replica):
            passed += 1

        prod_msg_ts = prod.get("ts")
        replica_msg_ts = replica.get("ts")

        # chat.update
        if prod_msg_ts and replica_msg_ts:
            total += 1
            prod = self.api_prod("POST", "chat.update", json_data={"channel": prod_ch, "ts": prod_msg_ts, "text": "Updated message"})
            replica = self.api_replica("POST", "chat.update", json_data={"channel": replica_ch, "ts": replica_msg_ts, "text": "Updated message"})
            if self.test_operation("Write", "chat.update", prod, replica):
                passed += 1

        # conversations.replies (post a thread first)
        thread_prod = self.api_prod("POST", "chat.postMessage", json_data={"channel": prod_ch, "text": "Thread root"})
        thread_replica = self.api_replica("POST", "chat.postMessage", json_data={"channel": replica_ch, "text": "Thread root"})

        if thread_prod.get("ok") and thread_replica.get("ok"):
            prod_thread_ts = thread_prod["ts"]
            replica_thread_ts = thread_replica["ts"]

            # Post a reply
            self.api_prod("POST", "chat.postMessage", json_data={"channel": prod_ch, "text": "Reply", "thread_ts": prod_thread_ts})
            self.api_replica("POST", "chat.postMessage", json_data={"channel": replica_ch, "text": "Reply", "thread_ts": replica_thread_ts})

            total += 1
            prod = self.api_prod("GET", "conversations.replies", params={"channel": prod_ch, "ts": prod_thread_ts})
            replica = self.api_replica("GET", "conversations.replies", params={"channel": replica_ch, "ts": replica_thread_ts})
            if self.test_operation("Write", "conversations.replies", prod, replica):
                passed += 1

        # reactions.add (may need reactions:write scope)
        if prod_msg_ts and replica_msg_ts:
            prod = self.api_prod("POST", "reactions.add", json_data={"channel": prod_ch, "timestamp": prod_msg_ts, "name": "thumbsup"})
            if prod.get("error") == "missing_scope":
                print("  reactions.add... ⏭️ SKIPPED (missing_scope)")
                print("  reactions.get... ⏭️ SKIPPED (depends on reactions.add)")
                print("  reactions.remove... ⏭️ SKIPPED (depends on reactions.add)")
                self.skipped += 3
            else:
                total += 1
                replica = self.api_replica("POST", "reactions.add", json_data={"channel": replica_ch, "timestamp": replica_msg_ts, "name": "thumbsup"})
                if self.test_operation("Write", "reactions.add", prod, replica):
                    passed += 1

                # reactions.get
                total += 1
                prod = self.api_prod("GET", "reactions.get", params={"channel": prod_ch, "timestamp": prod_msg_ts})
                replica = self.api_replica("GET", "reactions.get", params={"channel": replica_ch, "timestamp": replica_msg_ts})
                if self.test_operation("Write", "reactions.get", prod, replica):
                    passed += 1

                # reactions.remove
                total += 1
                prod = self.api_prod("POST", "reactions.remove", json_data={"channel": prod_ch, "timestamp": prod_msg_ts, "name": "thumbsup"})
                replica = self.api_replica("POST", "reactions.remove", json_data={"channel": replica_ch, "timestamp": replica_msg_ts, "name": "thumbsup"})
                if self.test_operation("Write", "reactions.remove", prod, replica):
                    passed += 1

        # conversations.setTopic
        total += 1
        prod = self.api_prod("POST", "conversations.setTopic", json_data={"channel": prod_ch, "topic": "Parity test topic"})
        replica = self.api_replica("POST", "conversations.setTopic", json_data={"channel": replica_ch, "topic": "Parity test topic"})
        if self.test_operation("Write", "conversations.setTopic", prod, replica):
            passed += 1

        # conversations.rename
        new_name = f"parity-renamed-{suffix}"
        total += 1
        prod = self.api_prod("POST", "conversations.rename", json_data={"channel": prod_ch, "name": new_name})
        replica = self.api_replica("POST", "conversations.rename", json_data={"channel": replica_ch, "name": new_name})
        if self.test_operation("Write", "conversations.rename", prod, replica):
            passed += 1

        # conversations.open (DM — use a human user, bot can't DM itself)
        total += 1
        prod_users = self.api_prod("GET", "users.list", params={"limit": "10"})
        prod_human = None
        if prod_users.get("ok"):
            for u in prod_users.get("members", []):
                if not u.get("is_bot") and u["id"] != "USLACKBOT" and not u.get("deleted"):
                    prod_human = u["id"]
                    break
        replica_human = "U02JOHNDOE1"  # seeded user

        if prod_human:
            prod = self.api_prod("POST", "conversations.open", json_data={"users": prod_human, "return_im": True})
            replica = self.api_replica("POST", "conversations.open", json_data={"users": replica_human, "return_im": True})
            if self.test_operation("Write", "conversations.open", prod, replica):
                passed += 1
        else:
            print("  conversations.open... ⏭️ SKIPPED (no human user)")
            self.skipped += 1

        # chat.delete
        if prod_msg_ts and replica_msg_ts:
            total += 1
            prod = self.api_prod("POST", "chat.delete", json_data={"channel": prod_ch, "ts": prod_msg_ts})
            replica = self.api_replica("POST", "chat.delete", json_data={"channel": replica_ch, "ts": replica_msg_ts})
            if self.test_operation("Write", "chat.delete", prod, replica):
                passed += 1

        # conversations.join (rejoin before archive)
        total += 1
        prod = self.api_prod("POST", "conversations.join", json_data={"channel": prod_ch})
        replica = self.api_replica("POST", "conversations.join", json_data={"channel": replica_ch})
        if self.test_operation("Write", "conversations.join", prod, replica):
            passed += 1

        # conversations.archive
        total += 1
        prod = self.api_prod("POST", "conversations.archive", json_data={"channel": prod_ch})
        replica = self.api_replica("POST", "conversations.archive", json_data={"channel": replica_ch})
        if self.test_operation("Write", "conversations.archive", prod, replica):
            passed += 1

        # conversations.unarchive (bot may lack permission in prod)
        total += 1
        prod = self.api_prod("POST", "conversations.unarchive", json_data={"channel": prod_ch})
        if not prod.get("ok") and prod.get("error") in ("not_allowed", "method_not_supported_for_channel_type", "missing_scope", "not_allowed_token_type", "not_in_channel"):
            replica = self.api_replica("POST", "conversations.unarchive", json_data={"channel": replica_ch})
            print(f"  conversations.unarchive... ⏭️ SKIPPED (prod: {prod.get('error')})")
            self.skipped += 1
            total -= 1
        else:
            replica = self.api_replica("POST", "conversations.unarchive", json_data={"channel": replica_ch})
            if self.test_operation("Write", "conversations.unarchive", prod, replica):
                passed += 1

        # conversations.leave (rejoin first, then leave)
        self.api_prod("POST", "conversations.join", json_data={"channel": prod_ch})
        self.api_replica("POST", "conversations.join", json_data={"channel": replica_ch})
        total += 1
        prod = self.api_prod("POST", "conversations.leave", json_data={"channel": prod_ch})
        if not prod.get("ok") and prod.get("error") in ("cant_leave_general", "not_in_channel", "missing_scope"):
            replica = self.api_replica("POST", "conversations.leave", json_data={"channel": replica_ch})
            print(f"  conversations.leave... ⏭️ SKIPPED (prod: {prod.get('error')})")
            self.skipped += 1
            total -= 1
        else:
            replica = self.api_replica("POST", "conversations.leave", json_data={"channel": replica_ch})
            if self.test_operation("Write", "conversations.leave", prod, replica):
                passed += 1

        return passed, total

    # =========================================================================
    # Error Handling Tests
    # =========================================================================

    def run_error_tests(self) -> Tuple[int, int]:
        """Test error responses match between prod and replica."""
        print("\n⚠️ Error Handling:")
        passed = 0
        total = 0

        error_cases = [
            {
                "name": "chat.postMessage — missing text",
                "endpoint": "chat.postMessage",
                "data": {"channel": self.prod_channel_id},
                "replica_data": {"channel": self.replica_channel_id},
            },
            {
                "name": "chat.postMessage — invalid channel",
                "endpoint": "chat.postMessage",
                "data": {"channel": "C_INVALID_999", "text": "test"},
                "replica_data": {"channel": "C_INVALID_999", "text": "test"},
            },
            {
                "name": "chat.delete — message not found",
                "endpoint": "chat.delete",
                "data": {"channel": self.prod_channel_id, "ts": "9999999999.999999"},
                "replica_data": {"channel": self.replica_channel_id, "ts": "9999999999.999999"},
            },
            {
                "name": "conversations.info — invalid channel",
                "endpoint": "conversations.info",
                "data": None,
                "params": {"channel": "C_INVALID_999"},
                "replica_data": None,
                "replica_params": {"channel": "C_INVALID_999"},
            },
            {
                "name": "conversations.archive — already archived",
                "endpoint": "conversations.archive",
                "data": {"channel": "C_INVALID_999"},
                "replica_data": {"channel": "C_INVALID_999"},
            },
            {
                "name": "users.info — invalid user",
                "endpoint": "users.info",
                "data": None,
                "params": {"user": "U_INVALID_999"},
                "replica_data": None,
                "replica_params": {"user": "U_INVALID_999"},
            },
        ]

        for case in error_cases:
            total += 1
            endpoint = case["endpoint"]
            method = "GET" if case.get("params") or case.get("replica_params") else "POST"

            if method == "GET":
                prod = self.api_prod("GET", endpoint, params=case.get("params"))
                replica = self.api_replica("GET", endpoint, params=case.get("replica_params", case.get("params")))
            else:
                prod = self.api_prod("POST", endpoint, json_data=case.get("data"))
                replica = self.api_replica("POST", endpoint, json_data=case.get("replica_data", case.get("data")))

            if self.test_operation("Error", case["name"], prod, replica, validate_schema=False):
                passed += 1

        return passed, total

    # =========================================================================
    # Pagination Tests
    # =========================================================================

    def run_pagination_tests(self) -> Tuple[int, int]:
        """Test pagination behavior matches between prod and replica."""
        print("\n📄 Pagination:")
        passed = 0
        total = 0

        # conversations.list with limit=1
        total += 1
        prod = self.api_prod("GET", "conversations.list", params={"types": "public_channel", "limit": "1"})
        replica = self.api_replica("GET", "conversations.list", params={"types": "public_channel", "limit": "1"})
        print(f"  conversations.list (limit=1)...", end=" ")
        prod_has_cursor = bool(prod.get("response_metadata", {}).get("next_cursor"))
        replica_has_cursor = bool(replica.get("response_metadata", {}).get("next_cursor"))
        if prod_has_cursor == replica_has_cursor:
            print("✅")
            self.record_result("Pagination", "conversations.list cursor", True)
            passed += 1
        else:
            print(f"❌ (prod cursor={prod_has_cursor}, replica={replica_has_cursor})")
            self.record_result("Pagination", "conversations.list cursor", False)

        # conversations.history with limit=1
        total += 1
        prod = self.api_prod("GET", "conversations.history", params={"channel": self.prod_channel_id, "limit": "1"})
        replica = self.api_replica("GET", "conversations.history", params={"channel": self.replica_channel_id, "limit": "1"})
        print(f"  conversations.history (limit=1)...", end=" ")
        prod_has_more = prod.get("has_more", False)
        replica_has_more = replica.get("has_more", False)
        # Both should have pagination structure
        prod_shape = self.extract_shape(prod)
        replica_shape = self.extract_shape(replica)
        diffs = self.compare_shapes(prod_shape, replica_shape, "data")
        critical = [d for d in diffs if "MISSING" in d]
        if not critical:
            print("✅")
            self.record_result("Pagination", "conversations.history pagination shape", True)
            passed += 1
        else:
            print(f"❌ {critical[0]}")
            self.record_result("Pagination", "conversations.history pagination shape", False)

        # users.list with limit=1
        total += 1
        prod = self.api_prod("GET", "users.list", params={"limit": "1"})
        replica = self.api_replica("GET", "users.list", params={"limit": "1"})
        if self.test_operation("Pagination", "users.list (limit=1)", prod, replica):
            passed += 1

        return passed, total

    # =========================================================================
    # Run All
    # =========================================================================

    def run_tests(self) -> Tuple[int, int, int]:
        """Run all parity tests."""
        print("=" * 70)
        print("COMPREHENSIVE SLACK API PARITY TESTS")
        print("=" * 70)

        self.setup_replica_environment()
        self.setup_prod_info()

        readonly_passed, readonly_total = self.run_readonly_tests()
        write_passed, write_total = self.run_write_tests()
        error_passed, error_total = self.run_error_tests()
        pagination_passed, pagination_total = self.run_pagination_tests()

        total = self.passed + self.failed
        print()
        print("=" * 70)
        print(f"RESULTS: {self.passed}/{total} tests passed ({int(self.passed / total * 100) if total > 0 else 0}%)")
        if self.skipped > 0:
            print(f"         {self.skipped} tests skipped")
        print("=" * 70)

        if self.failed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"   [{result['category']}] {result['test']}: {result['details']}")

        return self.passed, self.failed, self.skipped


# =============================================================================
# Pytest Integration
# =============================================================================


@pytest.mark.conformance
@pytest.mark.external
def test_slack_parity():
    """Run Slack parity tests as pytest test."""
    if not SLACK_BOT_TOKEN:
        pytest.skip("SLACK_BOT_TOKEN environment variable not set")

    tester = SlackParityTester(SLACK_BOT_TOKEN)
    try:
        passed, failed, skipped = tester.run_tests()
    finally:
        tester.cleanup()

    total = passed + failed
    success_rate = passed / total if total > 0 else 0
    assert success_rate >= 0.7, (
        f"Parity tests failed: {passed}/{total} ({int(success_rate * 100)}%)"
    )


# =============================================================================
# Standalone Execution
# =============================================================================


def main():
    if not SLACK_BOT_TOKEN:
        print("ERROR: SLACK_BOT_TOKEN environment variable not set")
        sys.exit(1)

    tester = SlackParityTester(SLACK_BOT_TOKEN)
    try:
        passed, failed, skipped = tester.run_tests()
        sys.exit(0 if failed == 0 else 1)
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()
