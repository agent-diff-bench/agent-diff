# API Conformance Testing

## Overview

This directory contains conformance tests that validate Agent-Diff API replicas against their real-world production counterparts. The tests compare **response schema/shape** (field presence, types, and structure), **status codes**, **error semantics**, and **mutation behavior** -- not exact values, since IDs and timestamps will naturally differ between environments.

## Per-Service Methodology

### Box (REST API)

**Approach:** Dual-fire against production Box API and replica. Each operation is executed against both environments, and response schemas are compared using recursive shape extraction.

- **Token:** `BOX_DEV_TOKEN` (Box developer token)
- **Endpoints tested:** 33/33 implemented endpoints
- **What is validated:** Response field presence and types, status code parity, error shapes (404, 400, 409), CRUD operations (folders, files, comments, tasks, hubs, collections, search), file upload/download, file version upload
- **Enterprise-only fields** (54 fields like `role`, `enterprise`, `sync_state`) are excluded from comparison, as they only appear for enterprise Box accounts
- **Last run:** 105/106 passed (99%)

### Google Calendar (REST API)

**Approach:** Dual-fire against Google Calendar API v3 and replica. Creates matching resources (calendars, events) in both environments, then validates all operations.

- **Token:** `GOOGLE_CALENDAR_ACCESS_TOKEN` (OAuth2 bearer token)
- **Endpoints tested:** 37/37 implemented endpoints (calendars, calendarList, events, ACL, settings, colors, freeBusy, batch, watch, channels)
- **What is validated:** Response schema parity, status codes, CRUD operations, recurring events, quickAdd, event move, ETag behavior, batch requests, error handling, delete operations
- **Optional data-dependent fields** (55+ fields like `nextPageToken`, `attendees`, `conferenceData`) are excluded from comparison

### Linear (GraphQL API)

**Approach:** Dual-fire against Linear production GraphQL API and replica. Creates matching resources (issues, labels, comments) in both environments, then validates queries and mutations. Additionally runs **focused schema introspection** to detect drift between production and replica GraphQL schemas.

- **Token:** `LINEAR_API_KEY` (Linear API key)
- **Operations tested:** 31 queries + 16 mutations + schema introspection
- **Queries validated:** Issue filters (string, number, ID, team, assignee, creator, state, date, label, comment comparators), search operations (with pagination, ordering, partial match), resource queries (teams, projects, users, workflowStates, issueLabels, viewer), pagination/sorting, query by identifier, error handling
- **Mutations validated:** issueCreate, issueUpdate, issueDelete, issueArchive/Unarchive, commentCreate, commentUpdate, commentDelete, issueLabelCreate, issueLabelUpdate, issueLabelDelete, issueAddLabel, issueRemoveLabel
- **Schema introspection:** Compares focused type surfaces (StringComparator, IssueFilter, Issue, Query, Mutation, etc.) between production and replica schemas
- **Last run:** 89/90 passed (98%) -- single failure is schema drift on newer Linear API fields (expected as Linear evolves their API)

### Slack (Docs-Golden)

**Approach:** Replica-only, validated against documented Slack API contracts. Unlike Box/Calendar/Linear, Slack conformance does not compare against a live Slack workspace because live-workspace parity is difficult to standardize (workspace state, installed apps, and permissions vary).

- **No external token required**
- **Methods tested:** 22/28 implemented methods
- **What is validated:** Response field presence (exact key sets), error semantics (`ok: false` with specific error codes), warning shapes, pagination structure
- **Methods covered:** auth.test, chat.postMessage, chat.update, chat.delete, conversations.create, conversations.join, conversations.history, conversations.replies, conversations.info, conversations.leave, conversations.setTopic, conversations.archive, conversations.unarchive, conversations.rename, conversations.kick, conversations.members, reactions.add, reactions.get, users.info, users.list, users.conversations, search.messages
- **Last run:** 22/22 passed (100%)

## How to Run

```bash
# All conformance tests (requires all tokens set)
pytest -m conformance -v

# Individual services
BOX_DEV_TOKEN=<token> pytest tests/validation/test_box_parity.py -v -s
GOOGLE_CALENDAR_ACCESS_TOKEN=<token> pytest tests/validation/test_calendar_parity_comprehensive.py -v -s
LINEAR_API_KEY=<key> pytest tests/validation/test_linear_parity_comprehensive.py -v -s

# Slack (no external token needed)
pytest tests/validation/test_slack_conformance.py -v

# Or run standalone (with detailed output):
BOX_DEV_TOKEN=<token> python tests/validation/test_box_parity.py
GOOGLE_CALENDAR_ACCESS_TOKEN=<token> python tests/validation/test_calendar_parity_comprehensive.py
LINEAR_API_KEY=<key> python tests/validation/test_linear_parity_comprehensive.py
```

**Prerequisites:**
- Backend replica must be running (`docker-compose up` from `ops/`)
- For Slack tests: must run inside Docker (`docker exec ops-backend-1 pytest ...`) or have local database access

## Interpreting Results

- **Pass threshold:** pytest entry points assert >= 70% pass rate. This threshold allows for minor schema differences (e.g., enterprise-only fields, newer API fields) while catching significant divergence.
- **Schema mismatches** indicate fields present in one environment but not the other. These are logged with the specific field path and should be investigated -- many are benign (optional fields, tier-specific fields).
- **Error parity** means both environments return the same error class (e.g., both return 404, or both return a GraphQL error with similar keywords). Exact error messages may differ.

## Coverage Summary

| Service  | Protocol | Endpoints Tested | Test Count | Pass Rate | Methodology |
|----------|----------|-----------------|------------|-----------|-------------|
| Box      | REST     | 33/33           | 106        | 99%       | Production parity |
| Calendar | REST     | 37/37           | 77         | 100%      | Production parity |
| Linear   | GraphQL  | 47 operations   | 90         | 98%       | Production parity + introspection |
| Slack    | REST     | 22/28 methods   | 22         | 100%      | Docs-golden |
