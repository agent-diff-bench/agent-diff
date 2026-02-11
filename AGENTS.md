# AGENTS.md — Agent-Diff Developer Guide

## Project Overview

Agent-Diff is a benchmarking platform for evaluating AI agents that interact with
real-world SaaS APIs (Slack, Linear, Box, Google Calendar). It provides **isolated,
reproducible environments** backed by PostgreSQL schema cloning.

## Architecture

```
┌──────────────────────────┐       ┌──────────────────────┐
│  Evaluation Client       │       │   Agent Sandbox      │
│  (prime eval / SDK)      │──────▶│   (Docker container) │
│                          │       │                      │
│  1. initEnv              │       │  Runs agent code     │
│  2. startRun             │       │  Makes API calls ──┐ │
│  3. evaluateRun          │       └────────────────────┼─┘
│  4. getResults           │                            │
└──────────┬───────────────┘                            │
           │                                            │
           ▼                                            ▼
┌──────────────────────────────────────────────────────────┐
│  AgentDiff Backend (FastAPI/Starlette)                    │
│                                                          │
│  Platform API (/api/platform/*)                          │
│    - initEnv, startRun, evaluateRun, diffRun             │
│    - Template & test suite management                    │
│                                                          │
│  Service APIs (/api/env/{env_id}/services/{service}/*)   │
│    - Box REST API replica   (/services/box/2.0/*)        │
│    - Slack API replica      (/services/slack/*)          │
│    - Linear GraphQL replica (/services/linear/*)         │
│    - Calendar API replica   (/services/calendar/*)       │
│                                                          │
│  Middleware:                                             │
│    PlatformMiddleware  → API key auth for platform calls │
│    IsolationMiddleware → per-env DB session + auth       │
└──────────────────────────────────────────────────────────┘
```

## Environment Lifecycle

### 1. Create an Isolated Environment (initEnv)

Every evaluation starts by creating an isolated copy of a template database schema.

**Via SDK (Python):**
```python
from agent_diff import AgentDiff

client = AgentDiff(
    api_key="ad_live_sk_...",
    base_url="https://api.agentdiff.dev",  # or http://localhost:8000
)

env = client.init_env(
    templateService="box",              # "box" | "linear" | "slack" | "calendar"
    templateName="box_default",         # name of the seeded template
    impersonateUserId="27512847635",    # user ID from the seed data
)
# env.environmentId  → hex string, e.g. "824d0c408eeb42368f20e24d2d9f03c3"
# env.environmentUrl → "/api/env/{env_id}/services/box"
```

**Via curl:**
```bash
curl -X POST https://api.agentdiff.dev/api/platform/initEnv \
  -H "X-API-Key: ad_live_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "templateService": "box",
    "templateName": "box_default",
    "impersonateUserId": "27512847635"
  }'
```

**What happens internally:**
1. `templateManager.resolve_init_template()` finds the template by service+name
2. `CoreIsolationEngine.create_environment()` clones the template PostgreSQL schema
3. A new `state_<uuid>` schema is created with all tables and data copied
4. A `RunTimeEnvironment` record is stored in the meta schema with TTL

### 2. Make API Calls Against the Environment

Once the environment is created, API calls go to the service replica endpoints:

```
Base URL: {base_url}/api/env/{env_id}/services/{service}

Box:      /api/env/{env_id}/services/box/2.0/search?query=fomc
Linear:   /api/env/{env_id}/services/linear/graphql
Slack:    /api/env/{env_id}/services/slack/conversations.list
Calendar: /api/env/{env_id}/services/calendar/calendars/{calendarId}/events
```

Each request goes through `IsolationMiddleware` which:
1. Validates the API key via control plane (`get_principal_id`)
2. Looks up the environment in meta DB to get impersonate_user_id
3. Opens a DB session scoped to the environment's `state_<uuid>` schema
4. Passes the request to the service route handler

### 3. Start a Run & Evaluate

```python
run = client.start_run(envId=env.environmentId)
# ... agent makes API calls that modify the environment ...
result = client.evaluate_run(runId=run.runId, expectedOutput={...})
results = client.get_results_for_run(runId=run.runId)
```

### 4. Cleanup

```python
client.delete_env(envId=env.environmentId)
```

## Available Templates

| Service  | Template Name     | Impersonate User ID                    |
|----------|-------------------|----------------------------------------|
| box      | box_default       | 27512847635                            |
| linear   | linear_default    | 2790a7ee-fde0-4537-9588-e233aa5a68d1   |
| slack    | slack_default     | U01AGENBOT9                            |
| calendar | calendar_base     | (varies by seed)                       |

## Writing Tests

### Integration Tests (in-process, no HTTP server)

Tests create environments via `core_isolation_engine.create_environment()` and
wire up an `AsyncClient` with middleware that injects the DB session:

```python
@pytest_asyncio.fixture
async def box_client(test_user_id, core_isolation_engine, session_manager, environment_handler):
    env_result = core_isolation_engine.create_environment(
        template_schema="box_default",
        ttl_seconds=3600,
        created_by=test_user_id,
        impersonate_user_id="27512847635",
    )

    async def add_db_session(request, call_next):
        with session_manager.with_session_for_environment(env_result.environment_id) as session:
            request.state.db_session = session
            request.state.environment_id = env_result.environment_id
            request.state.impersonate_user_id = "27512847635"
            request.state.impersonate_email = None
            response = await call_next(request)
            return response

    from src.services.box.api.routes import routes as box_routes
    app = Starlette(routes=box_routes)
    app.middleware("http")(add_db_session)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    environment_handler.drop_schema(env_result.schema_name)
```

### Running Tests

```bash
cd backend
# Requires DATABASE_URL in .env or environment
pytest tests/performance/test_box_bench_perf.py -v -s
pytest tests/integration/ -v
```

## Running Evaluations Locally

```bash
# 1. Activate the bench environment's venv
source third_party/prime-environments/environments/agent_diff_bench/.venv/bin/activate

# 2. Install the environment package
cd third_party/prime-environments/environments/agent_diff_bench
uv pip install -e .

# 3. Run evaluation (from the agent_diff_bench directory)
uv run prime eval run agent-diff-bench \
  -m "openai/gpt-5-mini" \
  -n 5 -r 3 -s \
  -a '{"agentdiff_api_key": "ad_live_sk_..."}'
```

Results are saved to: `third_party/prime-environments/environments/agent_diff_bench/eval_results/`

## Database Seeding

Templates are seeded from JSON files in `backend/seeds/` (Docker) or `examples/` (local).

Seed scripts in `backend/utils/`:
- `seed_box_template.py` — creates box_default, box_base templates
- `seed_linear_template.py` — creates linear_default, linear_base, linear_expanded
- `seed_slack_template.py` — creates slack_default, slack_bench_default
- `seed_calendar_template.py` — creates calendar_base
- `seed_tests.py` — loads test suite JSON files

On Railway, seeding runs automatically on deploy when `SEED=true` env var is set.
The Dockerfile startup script runs Alembic migrations then all seed scripts.

## Performance Profiling

All `[PERF]` log lines are instrumented for performance tracking:

- **Middleware**: `[PERF] GET /api/env/.../services/box/... total=Xms auth=Xms meta_db=Xms handler=Xms`
- **Box operations**: `[PERF] search_content TOTAL=Xms`, `[PERF] get_folder_by_id(...) time=Xms`
- **Box schema**: `[PERF] File._get_path_collection depth=N time=Xms`
- **Calendar**: `[PERF] Calendar events_list took Xms`

Filter with: `grep "\[PERF\]"` in Railway logs.

## Key Directories

```
backend/
  src/
    platform/          # Platform API (initEnv, runs, evaluation)
    services/
      box/             # Box API replica
      slack/           # Slack API replica
      linear/          # Linear API replica
      calendar/        # Calendar API replica
  tests/
    integration/       # Full-stack integration tests
    performance/       # Performance/benchmark tests
    validation/        # API parity tests
    unit/              # Unit tests
  utils/               # Seed scripts
  seeds/               # Seed data JSON files (for Docker)

sdk/agent-diff-python/ # Python SDK (agent_diff package)

examples/
  box/                 # Box seed data + test suites
  linear/              # Linear seed data + test suites
  slack/               # Slack seed data + test suites
  calendar/            # Calendar seed data

third_party/prime-environments/environments/agent_diff_bench/
  agent_diff_bench.py  # Entry point for prime eval
  src/environment.py   # Environment setup (initEnv, startRun, etc.)
```
