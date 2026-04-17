# AGENTS.md — Agent-Diff Developer Guide

## Project Overview

Agent-Diff is a benchmarking platform for evaluating AI agents that interact with
real-world SaaS APIs (Slack, Linear, Box, Google Calendar). It provides **isolated,
reproducible environments** backed by PostgreSQL schema cloning.

## Architecture

```
┌──────────────────────────┐       ┌──────────────────────┐
│  Evaluation Client       │       │   Agent Sandbox      │
│  (SDK / notebooks)       │──────▶│   (Docker container) │
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

## Running Evaluations

### Using the SDK (Local, No External Dependencies)

The SDK can fetch test suites directly from the platform — no HuggingFace or
third-party tooling needed. This is the primary way to run evaluations.

```python
from agent_diff import AgentDiff, BashExecutorProxy

client = AgentDiff()  # uses AGENT_DIFF_API_KEY and AGENT_DIFF_BASE_URL env vars

# List available test suites
suites = client.list_test_suites()
for s in suites.suites:
    print(f"{s.id}  {s.name}")

# Get a specific suite with its tests
suite = client.get_test_suite(suite_id="<suite-uuid>", expand=True)

# Run each test
for test in suite.tests:
    env = client.init_env(
        templateService=test.type,
        templateName=test.template_schema,
        impersonateUserId=test.impersonate_user_id,
    )
    run = client.start_run(envId=env.environmentId)
    bash = BashExecutorProxy(env.environmentId, base_url=client.base_url, api_key=client.api_key)

    # --- your agent loop goes here, calling bash.execute(command) ---

    client.evaluate_run(runId=run.runId, expectedOutput=test.expected_output)
    result = client.get_results_for_run(runId=run.runId)
    print(f"{test.name}: {'PASS' if result.passed else 'FAIL'} score={result.score}")

    client.delete_env(envId=env.environmentId)
```

### Using HuggingFace Dataset

Alternatively, load tasks from the published HuggingFace dataset:

```python
from agent_diff import AgentDiff, BashExecutorProxy
from datasets import load_dataset

client = AgentDiff()
dataset = load_dataset("hubertmarek/agent-diff-bench", split="test")

for example in dataset:
    info = json.loads(example["info"])
    expected = json.loads(example["answer"])

    env = client.init_env(
        templateService=info["service"],
        templateName=info["seed_template"],
        impersonateUserId=info["impersonate_user_id"],
    )
    run = client.start_run(envId=env.environmentId)
    bash = BashExecutorProxy(env.environmentId, base_url=client.base_url, api_key=client.api_key)

    # --- your agent loop goes here, calling bash.execute(command) ---

    client.evaluate_run(runId=run.runId, expectedOutput=expected)
    result = client.get_results_for_run(runId=run.runId)
    print(f"{example['test_id']}: {'PASS' if result.passed else 'FAIL'} score={result.score}")

    client.delete_env(envId=env.environmentId)
```

See `examples/react_agent_benchmark.ipynb` and `examples/langchain_agent_benchmark.ipynb`
for full runnable notebook examples.

---

## SessionManager & Isolation Architecture

The isolation system is the core of Agent-Diff. It allows every evaluation run to
operate on its own independent copy of a service's database without cross-contamination.

### SessionManager (`src/platform/isolationEngine/session.py`)

`SessionManager` wraps a single SQLAlchemy `Engine` and provides scoped sessions
at two levels:

1. **Meta sessions** — operate on the `public` schema where platform tables live
   (`TemplateEnvironment`, `RunTimeEnvironment`, `Test`, `TestSuite`, etc.):

   ```python
   with session_manager.with_meta_session() as session:
       # session is bound to `public` schema
       env = session.query(RunTimeEnvironment).filter(...).one()
   ```

2. **Environment sessions** — operate on an isolated `state_<uuid>` schema that
   contains the cloned service data for one evaluation run:

   ```python
   with session_manager.with_session_for_environment(env_id) as session:
       # session is bound to `state_abc123...` schema
       # all ORM queries hit the cloned tables for this environment only
   ```

   Internally this calls `lookup_environment(env_id)` to find the schema name from
   the `RunTimeEnvironment` table, then uses SQLAlchemy's `schema_translate_map`
   to redirect all unqualified table references to that schema:

   ```python
   translated = base_engine.execution_options(schema_translate_map={None: schema})
   ```

   This means service code (Box, Slack, etc.) never needs to know which schema it's
   hitting — the ORM models declare tables without a schema, and the engine-level
   translation handles routing transparently.

### IsolationMiddleware (`src/platform/api/middleware.py`)

`IsolationMiddleware` is the Starlette middleware that sits in front of all
`/api/env/{env_id}/services/...` requests. It is what connects HTTP requests to
the correct isolated database session:

1. **Extract `env_id`** from the URL path
2. **Authenticate** the API key via `get_principal_id()`
3. **Look up environment** in the meta DB to retrieve `impersonate_user_id`
4. **Open a scoped DB session** via `session_manager.with_session_for_environment(env_id)`
5. **Attach to `request.state`** so service handlers can access it:
   - `request.state.db_session` — SQLAlchemy session scoped to the environment schema
   - `request.state.environment_id` — the environment UUID string
   - `request.state.impersonate_user_id` — which user the agent is acting as
   - `request.state.impersonate_email` — alternative email-based impersonation
   - `request.state.principal_id` — the authenticated API key owner

Every service route handler accesses these via helper functions like:

```python
def _session(request: Request) -> Session:
    return getattr(request.state, "db_session", None)
```

### How Environments Are Created

When `initEnv` is called:

1. `TemplateManager.resolve_init_template()` finds the template by service+name (or ID)
2. `CoreIsolationEngine.create_environment()` either claims a pre-built schema from
   the pool or clones one from the template:
   - `PoolManager.claim_ready_schema()` — fast path, reuses a pre-built clone
   - `EnvironmentHandler.clone_schema_from_environment()` — slow path, creates schema +
     copies tables + copies data from the template
3. A `RunTimeEnvironment` row is written to the meta `public` schema with TTL and status
4. The environment ID is returned to the caller

---

## Adding a New Service

Each service follows a consistent pattern. Study the existing ones:

| Service  | API Style | Routes file | DB schema | DB operations |
|----------|-----------|------------|-----------|---------------|
| Slack    | Web API (flat endpoints) | `services/slack/api/methods.py` | `services/slack/database/schema.py` | `services/slack/database/operations.py` |
| Box      | REST (resource paths)    | `services/box/api/routes.py`    | `services/box/database/schema.py`   | `services/box/database/operations.py`   |
| Calendar | REST (Google style)      | `services/calendar/api/methods.py` | `services/calendar/database/schema.py` | `services/calendar/database/operations.py` |
| Linear   | GraphQL (Ariadne)        | `services/linear/api/resolvers.py` | `services/linear/database/schema.py` | (inline in resolvers) |

### Step-by-step

**1. Create the service directory structure:**

```
backend/src/services/myservice/
  __init__.py
  database/
    __init__.py
    base.py            # DeclarativeBase subclass
    schema.py          # SQLAlchemy ORM models
    operations.py      # CRUD functions (take a Session argument)
  api/
    __init__.py
    routes.py          # Starlette Route list
```

**2. Define the database schema** in `database/schema.py`:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime

class Base(DeclarativeBase):
    pass

class MyEntity(Base):
    __tablename__ = "my_entities"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    # ...
```

Each service has its own `Base` — this is important because `Base.metadata` is used
independently during schema creation and cloning.

**3. Write route handlers** that read from `request.state`:

```python
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

def _session(request: Request):
    return getattr(request.state, "db_session", None)

def _user_id(request: Request):
    return getattr(request.state, "impersonate_user_id", None)

async def list_entities(request: Request):
    session = _session(request)
    entities = session.query(MyEntity).all()
    return JSONResponse({"items": [...]})

routes = [
    Route("/entities", list_entities, methods=["GET"]),
    Route("/entities/{id}", get_entity, methods=["GET"]),
    # ...
]
```

The key contract: your handlers must only use `request.state.db_session` for DB access.
The IsolationMiddleware has already scoped this session to the correct environment schema.

**4. Mount the service in `src/platform/api/main.py`:**

```python
from src.services.myservice.api.routes import routes as myservice_routes

# Inside create_app():
myservice_router = Router(myservice_routes)
app.mount("/api/env/{env_id}/services/myservice", myservice_router)
```

**5. Register the service with the platform API** in `src/platform/api/models.py`.
Add it to the `Service` enum so `initEnv` (and other platform endpoints that take
a `templateService`) will accept the new value:

```python
class Service(str, Enum):
    slack = "slack"
    linear = "linear"
    calendar = "calendar"
    box = "box"
    myservice = "myservice"   # ← add this
```

If you skip this step, `POST /api/platform/initEnv` returns a Pydantic enum
validation error even though the template rows exist and the router is mounted.

**6. Write a seed script** in `backend/utils/seed_myservice_template.py` that:
- Creates the PostgreSQL schema (e.g. `myservice_default`)
- Uses `Base.metadata.create_all()` to create tables
- Inserts seed data from a JSON file
- Registers the template via `EnvironmentHandler.register_template()`

Follow `seed_slack_template.py` as a reference — it shows the full pattern including
schema creation, table ordering, and template registration.

**7. Add seed data** in `examples/myservice/seeds/myservice_default.json` and copy to
`backend/seeds/myservice/` for Docker builds.

**8. Register the seed script** in the Docker startup command in `ops/docker-compose.yml`:

```yaml
command: >
  sh -c "
    alembic upgrade head &&
    if [ \"$$SEED\" = 'true' ]; then
      # ... existing seed scripts ...
      python utils/seed_myservice_template.py;
    fi &&
    uvicorn src.platform.api.main:app --host 0.0.0.0 --port 8000
  "
```

### GraphQL Services (Linear Pattern)

If the service uses GraphQL instead of REST, follow the Linear pattern:

- Define a `.graphql` schema file in `services/myservice/api/schema/`
- Write Ariadne resolvers in `services/myservice/api/resolvers.py`
- Create a custom `GraphQL` subclass (like `LinearGraphQL`) that extracts
  `request.state.db_session` and passes it into the resolver context
- Mount with `app.mount(...)` passing the GraphQL ASGI app directly

---

## Adding Test Suites

Test suites define evaluation tasks with expected state-change assertions. They are
loaded into the platform DB by `backend/utils/seed_tests.py`.

### Test Suite JSON Format

```json
{
  "name": "My Service Bench",
  "description": "Benchmark tests for MyService",
  "owner": "dev-user",
  "ignore_fields": {
    "global": ["created_at", "modified_at"]
  },
  "tests": [
    {
      "id": "test_1",
      "name": "Create an entity",
      "prompt": "Create an entity named 'foo' in the workspace.",
      "type": "actionEval",
      "seed_template": "myservice_default",
      "impersonate_user_id": "user-123",
      "assertions": [
        {
          "diff_type": "added",
          "entity": "my_entities",
          "where": { "name": { "eq": "foo" } },
          "expected_count": 1
        }
      ]
    }
  ]
}
```

Key fields per test:
- **`id`** — unique string ID within the suite (used to generate deterministic UUIDs)
- **`prompt`** — the natural language task given to the agent
- **`type`** — typically `"actionEval"` for state-diff-based evaluation
- **`seed_template`** — which template schema to clone (e.g. `"slack_default"`)
- **`impersonate_user_id`** — which user the agent acts as
- **`assertions`** — list of expected state diffs (added/updated/deleted rows, field
  value checks). See the existing bench files for assertion patterns.

Suite-level `ignore_fields` are merged into every test's expected output — use for
timestamps and auto-generated fields that vary between runs.

### Where to Put Test Suite Files

Test suites live in two mirrored locations:

- **`examples/{service}/testsuites/{suite_name}.json`** — canonical source for local dev
- **`backend/seeds/testsuites/{suite_name}.json`** — copied here for Docker builds

The seed script `seed_tests.py` checks `backend/seeds/testsuites/` first (Docker path),
then falls back to scanning `examples/*/testsuites/*.json` (local dev path).

### How Seeding Works

`seed_tests.py` is idempotent — it can be re-run safely:

1. Scans for `*.json` files in the testsuites directory
2. For each file, checks if a suite with the same `name` + `owner` already exists
3. If it exists, deletes all its tests and memberships, then re-creates them
4. If new, creates a `TestSuite` with a deterministic UUID (from `uuid5(namespace, "suite:{owner}:{name}")`)
5. Creates a `Test` row for each test entry, with a deterministic UUID
6. Creates `TestMembership` rows linking tests to the suite

### Running the Seeder

```bash
# Local (requires DATABASE_URL in env or .env)
cd backend
python utils/seed_tests.py

# Docker (runs automatically when SEED=true)
docker-compose up  # in ops/
```

---

## Database Seeding (Templates)

Templates are seeded from JSON files in `backend/seeds/` (Docker) or `examples/` (local).

Seed scripts in `backend/utils/`:
- `seed_box_template.py` — creates box_default, box_base templates
- `seed_linear_template.py` — creates linear_default, linear_base, linear_expanded
- `seed_slack_template.py` — creates slack_default, slack_bench_default
- `seed_calendar_template.py` — creates calendar_base
- `seed_tests.py` — loads test suite JSON files

Each seed script follows the same pattern:
1. Create the PostgreSQL schema with `CREATE SCHEMA {name}`
2. Create tables using the service's `Base.metadata.create_all()`
3. Insert data from the JSON seed file in foreign-key-safe table order
4. Register the template in `TemplateEnvironment` with service, name, location, table_order

On Railway, seeding runs automatically on deploy when `SEED=true` env var is set.
The Dockerfile startup script runs Alembic migrations then all seed scripts.

## Git LFS

Large binary and data files are tracked with Git LFS. Patterns are defined in
`.gitattributes`:

- `examples/box/seeds/filesystem/**` — Box seed files (PDFs, CSVs, mhtml, etc.)
- `experiments/kdd 2026/evaluation_outputs/**/*.json` — experiment checkpoint JSONs
- `experiments/kdd 2026/bayesian_bootstrap_results/qualitative/*` — bootstrap results

If you add new large files (>1MB), add a matching pattern to `.gitattributes` **before**
committing them. Adding the pattern after the fact only affects future commits — files
already committed as regular blobs need `git lfs migrate import --no-rewrite` to convert.

## Key Directories

```
backend/
  src/
    platform/
      api/
        main.py          # App factory, middleware wiring, service mounting
        middleware.py     # PlatformMiddleware + IsolationMiddleware
        routes.py        # Platform API endpoints (initEnv, runs, evaluation)
      isolationEngine/
        session.py       # SessionManager (meta + environment sessions)
        core.py          # CoreIsolationEngine (create/delete environments)
        environment.py   # EnvironmentHandler (schema cloning, template registration)
        pool.py          # PoolManager (pre-built schema pool)
        templateManager.py # Template resolution logic
      evaluationEngine/  # State-diff evaluation, assertion engine
      testManager/       # Test suite management
      db/schema.py       # Platform ORM models (TemplateEnvironment, RunTimeEnvironment, Test, etc.)
    services/
      box/               # Box API replica (REST)
      slack/             # Slack API replica (Web API)
      linear/            # Linear API replica (GraphQL / Ariadne)
      calendar/          # Calendar API replica (REST, Google style)
  tests/
    integration/         # Full-stack integration tests
    performance/         # Performance/benchmark tests
    validation/          # API parity tests
    unit/                # Unit tests
  utils/                 # Seed scripts (seed_*_template.py, seed_tests.py)
  seeds/                 # Seed data JSON files (for Docker)

sdk/agent-diff-python/   # Python SDK (agent_diff package)

examples/
  box/                   # Box seed data + test suites
  linear/                # Linear seed data + test suites
  slack/                 # Slack seed data + test suites
  calendar/              # Calendar seed data
  react_agent_benchmark.ipynb       # ReAct agent evaluation notebook
  langchain_agent_benchmark.ipynb   # LangChain agent evaluation notebook
```
