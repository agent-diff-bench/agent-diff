# Getting Started 

## Prerequisites

- Docker & Docker Compose
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/diff-the-universe.git
cd diff-the-universe
```

### 2. Configure Environment

```bash
cp env.example .env
```

Edit `.env` if needed. The defaults work for local development:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/diff_the_universe
SECRET_KEY=your-secret-key-here  # Auto-generated if not set
```

### 3. Start the Platform

```bash
cd ops
docker-compose up --build
```

This starts:
- **Backend** on http://localhost:8000
- **PostgreSQL** on localhost:5432

On first run, the backend automatically:
- Runs database migrations
- Creates a development user
- Generates an API key
- Seeds template tests and schema for slack envioroment

### 4. Get Your API Key

```bash
docker-compose logs backend | grep "Dev API Key"
# Output: Dev API Key: ak_dev_xxxxxxxxxx
```

Save this key - you'll need it for all API requests.


## Your First Test

Let's test a simple Slack agent that sends a message.

### Step 1: Initialize an Environment

```bash
curl -X POST http://localhost:8000/api/platform/initEnv \
  -H "X-API-Key: ak_dev_xxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "templateService": "slack",
    "templateName": "slack_default",
    "impersonateUserId": "U01AGENBOT9",
    "ttlSeconds": 3600
  }'
```

Response:
```json
{
  "environmentId": "abc123",
  "templateSchema": "slack_default",
  "schemaName": "state_abc123",
  "service": "slack",
  "environmentUrl": "/api/env/abc123/services/slack",
  "expiresAt": "2025-01-15T12:00:00Z"
}
```

Save the `environmentId`.

### Step 2: Start a Test Run

```bash
curl -X POST http://localhost:8000/api/platform/startRun \
  -H "X-API-Key: ak_dev_xxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "envId": "abc123"
  }'
```

Response:
```json
{
  "runId": "run_xyz789",
  "status": "running",
  "beforeSnapshot": "before_abc123_1234567890"
}
```

### Step 3: Agent Performs Actions

Now call service APIs against the environment:

```bash
curl -X POST http://localhost:8000/api/env/abc123/services/slack/chat.postMessage \
  -H "X-API-Key: ak_dev_xxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C01ABCD1234",
    "text": "hello world"
  }'
```

Response:
```json
{
  "ok": true,
  "channel": "C01ABCD1234",
  "ts": "1699564800.000123",
  "message": {
    "text": "hello world",
    "user": "U01AGENBOT9"
  }
}
```

### Step 4: Evaluate the Run

```bash
curl -X POST http://localhost:8000/api/platform/evaluateRun \
  -H "X-API-Key: ak_dev_xxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "runId": "run_xyz789",
    "expectedOutput": {
      "assertions": [
        {
          "diff_type": "added",
          "entity": "messages",
          "where": {
            "channel_id": "C01ABCD1234",
            "message_text": {"contains": "hello"}
          },
          "expected_count": 1
        }
      ]
    }
  }'
```

Response:
```json
{
  "runId": "run_xyz789",
  "status": "completed",
  "passed": true,
  "score": {
    "passed": 1,
    "total": 1,
    "percent": 100.0
  }
}
```

**Success!** The assertion passed because:
- 1 message was inserted
- In channel `C01ABCD1234`
- Containing "hello"

## Key Concepts

### Environments

An **environment** is an isolated PostgreSQL schema with its own copy of service data (users, channels, messages, etc.). Each environment:

- Has a unique ID (`env_abc123`)
- Lives for a configurable TTL (default: 1 hour)
- Is completely isolated from other environments

### Templates

A **template** is a pre-seeded schema that gets cloned for each environment. The `slack_default` template includes:

- 3 users (agent1, johndoe, janedoe)
- 2 channels (#general, #random)
- 3 sample messages

See `examples/slack/seeds/slack_default.json` for details.

### Runs

A **run** is a single test execution:

1. **Start** → Take "before" snapshot
2. **Execute** → Agent calls fake APIs
3. **End** → Take "after" snapshot, compute diff, evaluate assertions

### Diffs

A **diff** shows exactly what changed:

```json
{
  "inserts": [...],  // Rows added
  "updates": [...],  // Rows modified (with before/after)
  "deletes": [...]   // Rows removed
}
```

Every row includes `__table__` to identify which entity changed.

### Assertions

**Assertions** define expected outcomes using a JSON DSL:

- `diff_type`: `"added"` | `"removed"` | `"changed"` | `"unchanged"`
- `entity`: Table name (e.g., `"messages"`, `"channels"`)
- `where`: Filters to match specific rows
- `expected_count`: Exact number or `{min, max}` range
- `expected_changes`: For `"changed"` type, what fields should change

See [evaluation-dsl.md](evaluation-dsl.md) for full syntax.


##  Workflows

### Testing Message Sending

```json
{
  "assertions": [{
    "diff_type": "added",
    "entity": "messages",
    "where": {"channel_id": "C01ABCD1234"},
    "expected_count": 1
  }]
}
```

### Testing Channel Creation

```json
{
  "assertions": [{
    "diff_type": "added",
    "entity": "channels",
    "where": {"channel_name": "new-channel"},
    "expected_count": 1
  }]
}
```

### Testing Status Updates

```json
{
  "assertions": [{
    "diff_type": "changed",
    "entity": "issues",
    "where": {"id": {"eq": 42}},
    "expected_changes": {
      "status": {"from": {"eq": "Todo"}, "to": {"eq": "Done"}}
    }
  }]
}
```

### Testing Deletion

```json
{
  "assertions": [{
    "diff_type": "removed",
    "entity": "messages",
    "where": {"message_id": {"eq": "1699564800.000123"}},
    "expected_count": 1
  }]
}
```


### Check Logs

```bash
# Backend logs
docker-compose logs -f backend

# Database logs
docker-compose logs -f postgres
```

## Development Commands

```bash
# Start services
cd ops && docker-compose up

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# View logs
docker-compose logs -f backend

# Run tests
docker exec ops-backend-1 python -m pytest tests/

# Access database
docker exec -it ops-postgres-1 psql -U postgres -d matrixes
```
