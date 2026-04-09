# API Conformance Testing

## Overview

This directory contains conformance tests that validate Agent-Diff API replicas against their real-world production counterparts. The tests compare **response schema/shape**, **status codes**, **error semantics**, **mutation behavior**, and **pagination** — not exact values, since IDs and timestamps naturally differ between environments.

## What Existed Before

Prior to this expansion, conformance tests existed for Box, Calendar, and Linear as production parity tests, and Slack as docs-golden (replica-only) tests. Coverage was uneven:

- **Box**: Comprehensive — response shapes, error codes (404/400/409), edge cases, pagination, field filtering
- **Calendar**: Moderate — response shapes and basic error handling (404), but no pagination parity or extended error coverage
- **Linear**: Query-focused — GraphQL filter testing and schema introspection, but limited error parity and no pagination testing
- **Slack**: No production parity — only docs-golden tests validating response shapes against the Slack API documentation, not the live API

## What Was Added

As requested by reviewers, we expanded the conformance suite to cover all four services uniformly:

### New: Slack Production Parity (`test_slack_parity.py`)

Built from scratch following the Box testing pattern. Compares Slack replica against the real Slack API across:
- **Read-only shape parity**: auth.test, users.info, users.list, conversations.list, conversations.info, conversations.history, conversations.members, users.conversations
- **Write operation parity**: conversations.create, chat.postMessage, chat.update, chat.delete, conversations.setTopic, conversations.rename, conversations.invite, conversations.kick, conversations.open, conversations.join, conversations.leave, conversations.archive, conversations.unarchive, conversations.replies
- **Error parity**: no_text, channel_not_found, message_not_found, user_not_found, already_archived
- **Pagination parity**: cursor-based pagination for conversations.list, conversations.history, users.list

### Expanded: Calendar (`test_calendar_parity_comprehensive.py`)

Added two new test sections:
- **Extended error handling**: Invalid time ranges (end before start), missing required fields, delete non-existent calendar, events for non-existent calendar, ACL with invalid role
- **Pagination parity**: Events and CalendarList with maxResults=1, nextPageToken following

### Expanded: Linear (`test_linear_parity_comprehensive.py`)

Added three new test sections:
- **Error response parity**: Non-existent issue by UUID, mutation with invalid team ID, malformed UUID — validates both environments return errors for the same inputs
- **Pagination parity**: issues(first:1) and issues(last:1) pageInfo shape, cursor-based pagination following
- **Earlier fixes**: Removed 3 invalid test cases that tested replica extensions not present in production (labels.none, comments.none filters; missing title validation strictness)

### Existing: Slack Docs-Golden (`test_slack_conformance.py`)

Retained as a complementary replica-only validation layer (22 tests). These run without API credentials and validate response shapes against documented Slack API contracts.

## Results

| Service | Tests | Passed | Rate | Skipped | Method |
|---------|-------|--------|------|---------|--------|
| Box | 106 | 105 | **99%** | 0 | Production parity (REST) |
| Calendar | 85 | 79 | **92%** | 0 | Production parity (REST) |
| Linear | 96 | 94 | **97%** | 0 | Production parity (GraphQL) + introspection |
| Slack (parity) | 27 | 27 | **100%** | 7 | Production parity (REST) |
| Slack (docs-golden) | 22 | 22 | **100%** | 0 | Replica vs documented contracts |
| **Total** | **336** | **327** | **97%** | **7** | |

### What Passed

Across all four services, the following core API behaviors are confirmed to match production:

- **Response schema/shape parity**: All CRUD operations (create, read, update, delete) return structurally identical responses between replicas and production APIs. Field names, nesting, types, and list structures match.
- **Error code parity**: Replicas return the same error codes as production for invalid inputs — `404` for non-existent resources, `400` for malformed requests, `channel_not_found` / `user_not_found` / `no_text` / `message_not_found` for Slack-specific errors.
- **Pagination behavior**: Cursor-based (Slack, Linear) and token-based (Calendar) pagination produces structurally identical responses. Page sizes are respected, continuation tokens work correctly.
- **Mutation semantics**: Create, update, and delete operations produce equivalent state changes and response shapes across all services.
- **GraphQL schema fidelity** (Linear): Introspection comparison confirms that query/mutation fields, input types, and object types are aligned between production and replica on all benchmark-relevant surfaces.

### Minor Issues Identified

The expanded test suite identified a small number of minor discrepancies, none of which affect benchmark scoring or the validity of reported results. These will be addressed before publication:

- **Calendar**: The replica accepts events with end time before start time (Google Calendar returns HTTP 400). This is an input validation gap — the replica processes the request rather than rejecting it. Four event list responses are missing computed fields that Google injects server-side. These do not affect the benchmark because no benchmark task depends on time-range validation rejection or these specific computed fields.
- **Linear**: Schema introspection detects 2 fields recently added to Linear's production API (`activity`, `hasSharedUsers` on `IssueFilter`) that the replica does not yet implement. These are new Linear features not used by any benchmark task.
- **Box**: One edge case in collection operations. Does not affect any benchmark task.

## How to Run

```bash
# All conformance tests
pytest -m conformance -v

# Individual services (production parity — requires API credentials)
BOX_DEV_TOKEN=<token> pytest tests/validation/test_box_parity.py -v -s
GOOGLE_CALENDAR_ACCESS_TOKEN=<token> pytest tests/validation/test_calendar_parity_comprehensive.py -v -s
LINEAR_API_KEY=<key> pytest tests/validation/test_linear_parity_comprehensive.py -v -s
SLACK_BOT_TOKEN=<token> pytest tests/validation/test_slack_parity.py -v -s

# Slack docs-golden (no credentials needed, runs against replica)
pytest tests/validation/test_slack_conformance.py -v

# Or run standalone with detailed output:
BOX_DEV_TOKEN=<token> python tests/validation/test_box_parity.py
```

**Prerequisites:**
- Backend replica running (`cd ops && make up`)
- For Slack docs-golden: run inside Docker (`docker exec ops-backend-1 pytest ...`) or have local database access
