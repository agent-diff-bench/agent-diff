# API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

All platform and service endpoints require authentication via API key:

```bash
-H "X-API-Key: ak_{key_id}_{secret}"
```

**Note:** API keys must be manually seeded in the database currently.

---

## Platform API

Platform endpoints for managing test environments and runs.

### Health Check

```http
GET /api/platform/health
```

Returns platform health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "diff-the-universe"
}
```

---

### List Test Suites

```http
GET /api/platform/testSuites
```

Returns all test suites.

**Note:** Test suites are currently read-only via API. Must be created directly in database.

**Response:**
```json
[
  {
    "id": "suite-123",
    "name": "Slack Agent Tests",
    "tests": [...]
  }
]
```

---

### Get Test Suite

```http
GET /api/platform/testSuites/{suiteId}
```

Returns a specific test suite with its tests.

**Response:**
```json
{
  "id": "suite-123",
  "name": "Slack Agent Tests",
  "tests": [
    {
      "id": "test-456",
      "name": "Post message to channel",
      "prompt": "Post 'Hello' to #general",
      "expectedOutput": {...}
    }
  ]
}
```

---

### Initialize Environment

```http
POST /api/platform/initEnv
```

Creates an isolated test environment with its own database schema.

**Request Body:**
```json
{
  "templateService": "slack",
  "templateName": "slack_default",
  "impersonateUserId": "U01AGENBOT9",
  "ttlSeconds": 1800
}
```

**Parameters:**
- `testId` (UUID, optional) - ID of the test definition
- `templateId` (UUID, optional) - Direct template ID selector
- `templateService` (string, optional) - Service name: `"box"`, `"linear"`, `"slack"`, `"calendar"`
- `templateName` (string, optional) - Template name (used with `templateService`)
- `templateSchema` (string, optional) - Legacy fallback: schema name to clone from
- `ttlSeconds` (number, optional) - Time-to-live in seconds
- `impersonateUserId` (string, optional) - User ID to impersonate in services
- `impersonateEmail` (string, optional) - Email to impersonate in services

Use `templateService` + `templateName` (preferred) or `templateId` to select a template.

**Response:**
```json
{
  "environmentId": "abc123",
  "templateSchema": "slack_default",
  "schemaName": "state_abc123",
  "service": "slack",
  "environmentUrl": "/api/env/abc123/services/slack",
  "expiresAt": "2025-10-12T20:00:00Z"
}
```

---

### Start Test Run

```http
POST /api/platform/startRun
```

Takes a "before" snapshot of the environment state.

**Request Body:**
```json
{
  "envId": "abc123",
  "testId": "test-uuid-optional",
  "testSuiteId": "suite-uuid-optional"
}
```

**Parameters:**
- `envId` (string, required) - Environment ID from `initEnv`
- `testId` (UUID, optional) - Links run to a specific test definition
- `testSuiteId` (UUID, optional) - Links run to a test suite

**Response:**
```json
{
  "runId": "run-789",
  "status": "running",
  "beforeSnapshot": "before_abc123_1234567890"
}
```

---

### Evaluate Run

```http
POST /api/platform/evaluateRun
```

Takes an "after" snapshot, computes diff, evaluates assertions.

**Request Body:**
```json
{
  "runId": "run-789",
  "expectedOutput": null
}
```

**Parameters:**
- `runId` (string, required) - Run ID from `startRun`
- `expectedOutput` (object, optional) - Assertion spec to evaluate against. If omitted, uses the stored test's `expected_output` (when run has a `test_id`).

**Response:**
```json
{
  "runId": "run-789",
  "status": "completed",
  "passed": true,
  "score": {
    "passed": 1,
    "total": 1,
    "percent": 100.0
  }
}
```

---

### Get Test Results

```http
GET /api/platform/results/{run_id}
```

Retrieves results for a completed test run.

**Response:**
```json
{
  "runId": "run-789",
  "status": "completed",
  "passed": true,
  "score": {
    "passed": 1,
    "total": 1,
    "percent": 100.0
  },
  "failures": [],
  "diff": {...},
  "createdAt": "2025-10-12T19:30:00Z"
}
```

---

### Delete Environment

```http
DELETE /api/platform/env/{envId}
```

Cleans up an environment and its database schema.

**Response:**
```json
{
  "environmentId": "abc123",
  "status": "deleted"
}
```

---

## Service APIs

Service endpoints mimic real service APIs but are isolated per environment.

### Slack API

Base path: `/api/env/{envId}/services/slack`

Implements Slack Web API methods:

#### Post Message

```http
POST /api/env/{envId}/services/slack/chat.postMessage
```

**Request Body:**
```json
{
  "channel": "C123456",
  "text": "Hello from agent!",
  "thread_ts": "1234567890.123456"
}
```

#### List Conversations

```http
GET /api/env/{envId}/services/slack/conversations.list
```

**Query Parameters:**
- `types` - Comma-separated list (e.g., "public_channel,private_channel")
- `limit` - Number of results to return

#### Get User Info

```http
GET /api/env/{envId}/services/slack/users.info?user=U123456
```

See [Slack Web API documentation](https://api.slack.com/web) for full method details.

---

### Box API

Base path: `/api/env/{envId}/services/box/2.0`

Implements Box REST API endpoints for files, folders, comments, tasks, collaborations, and search.

See [Box API documentation](https://developer.box.com/reference/) for method details.

---

### Calendar API

Base path: `/api/env/{envId}/services/calendar`

Implements Google Calendar-style REST API for calendars, events, ACLs, and channels.

See [Google Calendar API documentation](https://developers.google.com/calendar/api/v3/reference) for method details.

---

### Linear API

Base path: `/api/env/{envId}/services/linear`

Implements Linear's GraphQL API at `/api/env/{envId}/services/linear/graphql`.

See [Linear API documentation](https://developers.linear.app/docs/graphql/working-with-the-graphql-api) for query/mutation details.

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "ok": false,
  "error": "error_code",
  "detail": "Human-readable error message"
}
```

Common error codes:
- `not_authed` - Missing or invalid API key
- `invalid_environment_path` - Malformed environment ID
- `environment_not_found` - Environment doesn't exist or expired
- `internal_error` - Server error

