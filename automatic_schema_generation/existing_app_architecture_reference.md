# Existing App Architecture Reference

This document is the baseline reference for work in `automatic_schema_generation/`.
It documents how the four current app replicas in this repo are structured, what they
optimize for, and which architectural decisions matter if we want to generate new app
schemas and service scaffolding automatically.

The goal is not just to describe the current code. The goal is to identify the
contracts that the automatic generation pipeline must preserve.

## 1. What The Repo Actually Expects From A Service

Every service replica, regardless of API style, plugs into the same platform-level
runtime:

1. The platform creates an isolated PostgreSQL schema per evaluation run.
2. `IsolationMiddleware` resolves the environment and injects a DB session scoped to
   that schema.
3. Service code reads only from `request.state.db_session` or, for GraphQL, from the
   request-derived resolver context.
4. Service code uses service-local ORM models with no hardcoded schema name.
5. Template seeders create schemas, create tables from that service's `Base.metadata`,
   insert seed data in foreign-key-safe order, and register the template in the
   platform metadata DB.
6. Tests and evaluation benches assume the service can be cloned from a template and
   exercised in-process through Starlette/Ariadne.

At platform level this is wired in:

- `backend/src/platform/api/main.py`
- `backend/src/platform/api/middleware.py`
- `backend/src/platform/isolationEngine/session.py`

### Cross-service runtime contract

- Every service must have its own SQLAlchemy `Base`.
- ORM model declarations are schema-agnostic. The platform applies
  `schema_translate_map={None: state_<uuid>}` at session creation time.
- HTTP services must read auth/session state from `request.state`.
- GraphQL services must convert request state into resolver context.
- Template creation must be deterministic enough that cloning and diffing are stable.
- The evaluation engine compares database state, not response payloads, so service
  writes need to land in durable relational state.

### Cross-service file pattern

The repo does not enforce a single file layout, but the current implementations show
four patterns:

| Service | API style | Main API file(s) | Data layer | Serialization style |
| --- | --- | --- | --- | --- |
| Box | REST resource API | `api/routes.py` | `database/schema.py`, `database/operations.py`, `utils/*` | Mostly model `to_dict()` methods |
| Slack | Flat RPC/Web API | `api/methods.py` | `database/schema.py`, `database/operations.py` | Mostly API-layer serializers in `methods.py` |
| Calendar | REST resource API + batch | `api/methods.py`, `api/batch.py`, `api/__init__.py` | `database/schema.py`, `database/operations.py`, `core/*` | Dedicated serializer layer in `core/serializers.py` |
| Linear | GraphQL | `api/graphql_linear.py`, `api/resolvers.py`, `api/schema/Linear-API.graphql` | `database/schema.py` | GraphQL field resolvers + Ariadne default object serialization |

## 2. High-level Comparison

| Service | Mount path | API surface size | ORM table count | Seed templates created by script | Example bench tests |
| --- | --- | --- | --- | --- | --- |
| Box | `/api/env/{env_id}/services/box/2.0` | 33 Starlette routes | 11 tables | `box_base`, discovered JSON templates such as `box_default` | 48 |
| Slack | `/api/env/{env_id}/services/slack` | 2 routes, 27 dispatched methods | 15 tables | `slack_base`, plus discovered JSON templates such as `slack_default`, `slack_bench_default`, `slack_bench_v2` | 37 |
| Calendar | `/api/env/{env_id}/services/calendar` | 22 REST routes + 1 batch route | 10 tables | `calendar_base`, plus discovered JSON templates such as `calendar_default` | 60 |
| Linear | `/api/env/{env_id}/services/linear` | 57 queries + 134 mutations | 50 tables | `linear_base`, `linear_default`, `linear_expanded` | 57 |

Implementation size also varies a lot:

- Box: `routes.py` 2283 lines, `schema.py` 1540 lines, `operations.py` 2175 lines
- Slack: `methods.py` 3204 lines, `schema.py` 268 lines, `operations.py` 804 lines
- Calendar: `methods.py` 3259 lines, `batch.py` 646 lines, `operations.py` 2922 lines, `serializers.py` 1009 lines
- Linear: `resolvers.py` 18890 lines, GraphQL schema file 26769 lines, `schema.py` 2401 lines

This matters for generation work. The pipeline should not assume one implementation
shape scales across all API styles.

## 3. Shared Architectural Decisions That Matter For Generation

Before going service by service, these are the recurring repo-level choices that show
up everywhere:

### 3.1 Isolation is schema-based, not database-per-env

- The core artifact is a cloned PostgreSQL schema.
- A generated app must be able to live entirely inside one schema namespace.
- Unqualified ORM models are required so `schema_translate_map` can redirect them.

### 3.2 External API fidelity matters more than internal normalization

- Models and responses are designed to look like the external API or SDK.
- This often means denormalized or duplicated data is stored intentionally.
- JSONB is used aggressively for nested payloads and variant fields.

### 3.3 Seedability is a first-class design constraint

- Every service ships an empty base template and at least one seeded template.
- Seed JSON shape is table-oriented, not entity-graph-oriented.
- Insert order is explicitly controlled.
- Generated apps need a deterministic table order or dependency graph.

### 3.4 Service code is allowed to be pragmatic, not perfectly layered

- Box has a clean split between route handlers, operations, and model serializers.
- Slack keeps a large amount of behavior directly in one API file.
- Calendar uses the most explicit layering.
- Linear inlines most business logic in resolvers and openly acknowledges auto-generated code.

The generator should support multiple output patterns depending on API style and
complexity, not force all apps into one template.

### 3.5 Not all parity is implemented at the same depth

- Some services are deliberately partial or pragmatic replicas.
- Calendar has watch stubs and batch support.
- Box has modern Hubs support gated by `box-version: 2025.0`.
- Linear is intentionally "shape-faithful" even where business logic is approximate.

The pipeline should produce explicit capability metadata: fully implemented, partially
implemented, stubbed, or shape-only.

## 4. Box

### 4.1 File layout

Relevant files:

- `backend/src/services/box/api/routes.py`
- `backend/src/services/box/database/base.py`
- `backend/src/services/box/database/schema.py`
- `backend/src/services/box/database/operations.py`
- `backend/src/services/box/utils/enums.py`
- `backend/src/services/box/utils/errors.py`
- `backend/src/services/box/utils/ids.py`
- `backend/utils/seed_box_template.py`
- `examples/box/seeds/box_default.json`
- `examples/box/testsuites/box_bench.json`

### 4.2 API shape

Box is implemented as a REST resource API that mirrors Box v2 resource paths. The
service is mounted at:

`/api/env/{env_id}/services/box/2.0`

The route file exposes 33 Starlette routes covering:

- current user
- search
- folders
- files
- file upload and new version upload
- file content download redirect flow
- comments
- tasks
- hubs
- collections

Notable API-level behavior:

- Box uses a `fields` query parameter for sparse fieldsets.
- Responses carry `BOX-REQUEST-ID` and `Cache-Control: no-cache, no-store`.
- File download is modeled as a two-step flow:
  - `/files/{id}/content` returns a 302 redirect
  - `/files/{id}/download` returns binary content
- Hubs require `box-version: 2025.0`.
- Errors use Box-specific envelope structure, not generic JSON error responses.

### 4.3 Request/session/auth pattern

Box follows the standard HTTP pattern:

- `_session(request)` reads `request.state.db_session`
- `_principal_user_id(request)` resolves the acting Box user from
  `impersonate_user_id` or `impersonate_email`

This is a clean, reusable pattern for REST replicas.

### 4.4 Error and response modeling

Box has dedicated utilities for:

- Box error codes
- HTTP status mapping
- request id generation
- resource id generation
- etag/sequence id generation

Important detail: Box is stricter than Slack about HTTP status semantics. The API
layer intentionally constructs Box-shaped error payloads instead of relying on
framework exceptions.

### 4.5 Data model shape

Box defines 11 ORM tables:

- `box_collections`
- `box_users`
- `box_folders`
- `box_files`
- `box_file_versions`
- `box_file_contents`
- `box_comments`
- `box_tasks`
- `box_task_assignments`
- `box_hubs`
- `box_hub_items`

The data model is intentionally rich. It is not only a minimal relational backing
store for CRUD.

#### Core design choices

1. The ORM models embed API serialization logic directly via `to_dict()` and
   `to_mini_dict()` methods.
2. The database schema mirrors Box SDK response shapes closely.
3. Several nested response fragments are stored as JSONB instead of being normalized:
   `shared_link`, `permissions`, `classification`, `representations`,
   `notification_email`, `enterprise`, `collections`, `tags`, metadata blobs.
4. Folder and file hierarchy uses a materialized `path` column to avoid repeated
   ancestor lookups during listing and search serialization.
5. File binary payload is stored separately in `box_file_contents`.
6. Root folder is a special record with ID `"0"`.
7. Favorites collection is a special singleton concept that may be auto-created.

#### ID conventions

`backend/src/services/box/utils/ids.py` hardcodes Box-style numeric string IDs:

- user: 11 digits
- folder: 12 digits
- file: 13 digits
- file version: 13 digits
- comment: 9 digits
- task: 11 digits
- collection: 6 digits
- root folder: `"0"`

This is very important for generation. External ID semantics are part of fidelity.
The generator cannot assume UUIDs are always acceptable.

#### Serialization strategy

Box is the most model-centric service in the repo:

- models know how to serialize themselves into API-ready dicts
- operations mostly manipulate ORM objects
- routes apply Box-specific request parsing, validation, field filtering, and HTTP response wrapping

This works well when the external API has many reusable "mini" and "full" resource
shapes.

### 4.6 Data access layer

`database/operations.py` is large and meaningful. It is not just thin CRUD. It
contains:

- path computation
- hierarchical folder/file operations
- cascade path updates on moves
- partial update semantics using `UNSET`
- content search with eager loading and ancestor prefetch
- collection handling
- hub management
- file version creation

Important design decisions:

- Search performance is explicitly optimized.
- Box search uses joined loading and a bulk-prefetch ancestor cache.
- Box seed setup creates `pg_trgm` indexes on searchable name/description columns.
- Partial update semantics distinguish:
  - omitted field
  - explicit null
  - updated value

That distinction is critical if we later generate update handlers for APIs with patch
semantics.

### 4.7 Seeding strategy

`backend/utils/seed_box_template.py` is the most sophisticated seeder of the four.

Important details:

1. It creates `box_base` and discovered JSON templates such as `box_default`.
2. It validates schema/table/column identifiers before dynamic SQL insertion.
3. It computes folder and file materialized paths at seed time.
4. It loads binary file contents from filesystem paths referenced in
   `box_file_versions.local_path`.
5. It registers `table_order` in the platform environment metadata.
6. It can run in strict mode via `SEED_STRICT=true` and fail if referenced files are
   missing.

This means generated apps may need more than "table JSON -> INSERT statements". Some
services need pre-insert transformation, derived columns, binary asset import, and
index creation.

### 4.8 Seed data shape

`examples/box/seeds/box_default.json` is table-oriented. It currently seeds:

- 3 users
- 28 folders
- 131 files
- 131 file versions
- 17 comments
- 11 tasks
- 3 hubs
- 0 hub items

The seed JSON does not include every table. Some records are derived during seed
processing:

- `box_file_contents` is generated from filesystem assets
- `path` values are computed

### 4.9 Test and benchmark posture

Box currently has:

- dedicated parity validation against the real Box API
- Box bench suite with 48 tests
- seed files that include realistic filesystem payloads

This indicates Box is treated as a high-fidelity REST/file-storage replica.

### 4.10 What matters for automatic generation

If we generate a Box-like app, we need support for:

- resource-oriented REST routing
- service-specific ID generators
- model-level serializers for mini/full resource shapes
- JSONB fields for nested API fragments
- derived hierarchy columns like materialized paths
- binary asset ingestion during seeding
- request-specific sparse field filtering
- sub-API version gating via headers
- redirect and binary content endpoints

## 5. Slack

### 5.1 File layout

Relevant files:

- `backend/src/services/slack/api/methods.py`
- `backend/src/services/slack/database/base.py`
- `backend/src/services/slack/database/schema.py`
- `backend/src/services/slack/database/operations.py`
- `backend/src/services/slack/core/actions.py`
- `backend/utils/seed_slack_template.py`
- `examples/slack/seeds/*.json`
- `examples/slack/testsuites/*.json`

### 5.2 API shape

Slack is implemented as a flat method-dispatch RPC API, not as resource routes.

It exposes only two Starlette routes:

- `/{endpoint}`
- `/api/{endpoint}`

Those routes dispatch to 27 supported Slack methods via `SLACK_HANDLERS`.

Supported method families include:

- `auth.test`
- `chat.*`
- `conversations.*`
- `reactions.*`
- `users.*`
- `search.*`

This is the clearest example in the repo of an API surface where routing is not the
primary modeling tool. The method name string is the contract.

### 5.3 Request/session/auth pattern

Slack also uses:

- `_session(request)`
- `_principal_user_id(request)`

But most of the app logic lives in the single API file itself. The operations module
is smaller and mostly handles DB mutations and queries.

### 5.4 Error semantics

Slack has a very important quirk:

- In strict compatibility mode, many Slack API errors return HTTP 200 with
  `"ok": false`.
- In relaxed mode, they can use standard HTTP error statuses.

This behavior is controlled by `SLACK_COMPAT_MODE`.

This is a strong reminder for the generator: transport semantics may be app-specific.
We cannot assume "error means 4xx/5xx".

### 5.5 Data model shape

Slack defines 15 ORM tables:

- `users`
- `teams`
- `channels`
- `messages`
- `channel_members`
- `user_roles`
- `message_reactions`
- `team_roles`
- `team_settings`
- `files`
- `user_settings`
- `file_messages`
- `user_teams`
- `user_mentions`
- `message_edits`

The default seed uses only a smaller subset, but the schema supports more than the
minimal bench data needs.

#### Core design choices

1. Slack models the product with a small normalized core:
   users, teams, channels, messages, memberships, reactions.
2. Channel types are represented with flags on one table:
   `is_private`, `is_dm`, `is_gc`.
3. Message primary key is the Slack timestamp string itself.
4. Rich response payloads are mostly synthesized in the API layer instead of being
   stored verbatim.
5. Block Kit validation and mrkdwn fallback rendering happen in `methods.py`.

This is very different from Box. Slack optimizes for behavior and response shape
construction at request time rather than packing everything into model `to_dict()`
methods.

#### ID conventions

Slack-style IDs are generated with prefixes plus 10 random alphanumeric characters:

- team IDs start with `T`
- user IDs start with `U`
- channel IDs start with `C`

Message IDs use timestamp strings like real Slack `ts` values.

Again, this is generator-critical. Prefix semantics and timestamp IDs are part of
observable API behavior.

### 5.6 Serialization strategy

Slack serialization is API-layer-heavy:

- `_serialize_conversation()` constructs conversation payloads
- `_serialize_user()` constructs user payloads
- message response envelopes are built inline per handler

This makes sense because Slack response shape depends heavily on endpoint context:

- `conversations.list` shape differs from `conversations.info`
- DMs and regular channels serialize differently
- message payloads include computed fields like `thread_ts`

### 5.7 Behavior encoded in API layer

`api/methods.py` includes a lot of app-specific logic:

- JSON/form parameter parsing
- Block Kit validation
- channel name and channel ID resolution
- DM channel creation
- pagination cursor encoding/decoding
- search query parsing and highlighting
- membership and permission checks
- response shape assembly

This shows that some apps are better represented by generated endpoint-specific
behavior functions than by a generic CRUD abstraction.

### 5.8 Data access layer

`database/operations.py` provides focused primitives:

- create team/user/channel
- invite/kick/join/leave channel
- send/update/delete message
- add/remove reaction
- find or create DM channel
- list user channels, members, history, thread replies

The operations layer is intentionally smaller than Box and Calendar. Slack-specific
API behavior mostly sits above it.

### 5.9 Seeding strategy

`backend/utils/seed_slack_template.py`:

- creates `slack_base`
- discovers all JSON files in the Slack seeds directory and creates templates from them
- uses a simple explicit `TABLE_ORDER`
- inserts records with dynamic SQL
- registers public templates

Compared to Box, Slack seeding is simple. There are no derived binary assets, no
quoted identifiers, and no complex preprocessing beyond order.

### 5.10 Seed data shape

`examples/slack/seeds/slack_default.json` currently seeds:

- 1 team
- 3 users
- 2 channels
- 3 `user_teams` memberships
- 6 `channel_members`
- 3 messages

The schema supports more features than the base seed uses. That pattern matters for
generation: create a fuller schema than the initial seed necessarily exercises.

### 5.11 Test and benchmark posture

Slack has:

- integration tests for API behavior
- integration tests specifically checking response doc shape
- bench suites such as `slack_bench.json` and `slack_bench_v2.json`

This suggests Slack is optimized for endpoint behavior compatibility and agent-facing
task realism more than exhaustive domain modeling.

### 5.12 What matters for automatic generation

If we generate a Slack-like app, we need support for:

- flat RPC method dispatch
- nonstandard HTTP error semantics
- prefixed external IDs
- API-layer response synthesis
- endpoint-context-specific serializers
- channel subtype flags on a shared table
- cursor-based pagination helpers
- on-the-fly validation for rich request payloads

## 6. Google Calendar

### 6.1 File layout

Relevant files:

- `backend/src/services/calendar/api/methods.py`
- `backend/src/services/calendar/api/batch.py`
- `backend/src/services/calendar/api/__init__.py`
- `backend/src/services/calendar/core/errors.py`
- `backend/src/services/calendar/core/utils.py`
- `backend/src/services/calendar/core/serializers.py`
- `backend/src/services/calendar/core/batch_parser.py`
- `backend/src/services/calendar/core/batch_builder.py`
- `backend/src/services/calendar/database/schema.py`
- `backend/src/services/calendar/database/operations.py`
- `backend/utils/seed_calendar_template.py`
- `examples/calendar/seeds/calendar_default.json`
- `examples/calendar/testsuites/calendar_bench.json`

### 6.2 API shape

Calendar is a REST resource API with Google-style nested paths plus a multipart batch
endpoint.

Mounted path:

`/api/env/{env_id}/services/calendar`

Route groups:

- calendars
- calendarList
- events
- acl
- channels
- colors
- freeBusy
- settings
- batch

The API layer is explicitly organized into route groups and then re-exported from
`api/__init__.py`.

This is the cleanest service in the repo in terms of module boundaries.

### 6.3 Request/session/auth pattern

Calendar uses:

- `_get_session(request)`
- `get_user_id(request)`
- `get_user_email(request)`
- `resolve_calendar_id(request, calendar_id)`

Important detail: `"primary"` is resolved to the user's actual primary calendar.
That concept is built into both API handlers and DB operations.

### 6.4 Error and serializer architecture

Calendar has the strongest explicit support layers:

- `core/errors.py` defines Google-style error types
- `core/serializers.py` builds API responses
- `core/utils.py` handles IDs, ETags, RFC3339, recurrence, pagination, fixed clock
- `api/batch.py` plus parser/builder modules implement multipart batch requests

This service is a good template for APIs that have:

- a large but structured resource surface
- well-defined response envelopes
- complex helper logic that should not live in ORM models

### 6.5 Data model shape

Calendar defines 10 ORM tables:

- `calendar_users`
- `calendars`
- `calendar_list_entries`
- `calendar_events`
- `calendar_event_attendees`
- `calendar_event_reminders`
- `calendar_acl_rules`
- `calendar_settings`
- `calendar_channels`
- `calendar_sync_tokens`

#### Core design choices

1. Calendar mixes normalized relational entities with JSONB-heavy event fields.
2. Event time is stored twice:
   - original API-like JSON structures in `start` and `end`
   - denormalized indexed datetime/date columns for filtering and ordering
3. Recurring events are stored as master events plus exception rows; virtual instances
   are synthesized at read time.
4. ACL and calendar list entries are separate first-class resources.
5. Sync tokens are persisted so incremental sync can be modeled.
6. The replica clock is fixed by `REPLICA_NOW_RFC3339` for deterministic tests.

This is a strong example of the repo favoring benchmark determinism over real-time
behavior.

#### Enum strategy

Calendar defines multiple PostgreSQL-backed enums in the public schema:

- access roles
- event status
- transparency
- visibility
- event type
- attendee response status
- ACL scope type
- reminder method

This matters for generation. Some apps need real enum types, not plain strings.

#### ID conventions

Calendar utilities generate:

- event IDs using lowercase base32hex UUID encoding
- primary calendar IDs as the owner's email
- secondary calendar IDs like `c_<random>@group.calendar.google.com`
- iCal UIDs derived from event ID and calendar domain
- ACL rule IDs derived from scope and calendar
- channel IDs and sync tokens

These are very API-specific conventions and should be generator-configurable.

### 6.6 Data access layer

`database/operations.py` is rich and includes:

- user creation that can auto-create:
  - primary calendar
  - calendar list entry
  - owner ACL rule
  - default settings
- full CRUD for calendars, calendar list, events, ACL, settings, channels
- recurrence expansion and instance handling
- sync token validation and issuance
- access checks using both calendar list membership and ACL rules
- batched free/busy access resolution

Two especially important architectural decisions:

1. The read model for recurring events is more complex than the write model.
2. Access control is part of core operations, not just middleware.

### 6.7 Batch support

Calendar is the only current service with a first-class batch transport:

- parses multipart/mixed batch requests
- executes each part against the same replica
- returns multipart responses
- handles per-part errors without failing the entire batch

If we generate apps for ecosystems like Google APIs, batch support may need to be a
pluggable generation feature.

### 6.8 Watch support and stubbing

Calendar includes watch-related resources and routes:

- `*.watch`
- `channels.stop`

But these are not fully equivalent to Google's production infrastructure. This is a
good example of modeling the shape and workflow even when the full external system
cannot or should not be reproduced.

### 6.9 Seeding strategy

`backend/utils/seed_calendar_template.py`:

- creates `calendar_base`
- discovers JSON templates such as `calendar_default`
- uses quoted identifiers for inserts
- JSON-serializes dict/list fields before insertion
- stores `table_order` in template metadata

The quoting behavior matters. The generation pipeline must understand when seed
insertion should preserve identifier case or avoid reserved-word issues.

### 6.10 Seed data shape

`examples/calendar/seeds/calendar_default.json` currently seeds:

- 89 users
- 104 calendars
- 66 calendar list entries
- 286 events
- 7 attendees
- 121 ACL rules
- 6 settings
- 4 channels

This is a much larger, richer seed than Slack and resembles a realistic benchmark
dataset rather than a toy fixture.

### 6.11 Test and benchmark posture

Calendar has:

- unit tests
- integration tests
- dedicated performance tests
- comprehensive parity validation against the real Google Calendar API
- a large bench suite with 60 tests

This service is the strongest example of a benchmark-oriented, fidelity-conscious,
deterministic REST replica.

### 6.12 What matters for automatic generation

If we generate a Calendar-like app, we need support for:

- nested REST resources
- dedicated serializer and error modules
- JSONB plus denormalized query columns
- enum generation
- deterministic clock injection
- virtual read-time entities such as recurring instances
- persisted access-control resources
- sync token support
- batch transport parsing and building
- explicit stubs for unsupported but shape-relevant features

## 7. Linear

### 7.1 File layout

Relevant files:

- `backend/src/services/linear/api/graphql_linear.py`
- `backend/src/services/linear/api/resolvers.py`
- `backend/src/services/linear/api/schema/Linear-API.graphql`
- `backend/src/services/linear/database/schema.py`
- `backend/utils/seed_linear_template.py`
- `examples/linear/seeds/linear_default.json`
- `examples/linear/seeds/linear_expanded.json`
- `examples/linear/testsuites/linear_bench.json`

### 7.2 API shape

Linear is the only GraphQL service in the repo.

Mounted path:

`/api/env/{env_id}/services/linear`

The service consists of:

- a large SDL file: `Linear-API.graphql`
- Ariadne `QueryType`, `MutationType`, and selected `ObjectType` bindables
- a custom `LinearGraphQL` wrapper that builds resolver context from request state

Measured surface in the current resolver file:

- 57 root queries
- 134 root mutations

### 7.3 Resolver architecture

`api/resolvers.py` is explicitly described as mostly auto-generated from the official
Linear GraphQL schema. That statement is important. The project already treats
generation as acceptable here, as long as the result preserves useful shapes and
passes parity checks.

Key implications:

- the repo already tolerates generated service code
- exact business logic is not always the priority
- response shape compatibility and enough mutation behavior for benchmarks are the real target

### 7.4 Context/auth pattern

`graphql_linear.py` converts request state into GraphQL context:

- `session`
- `environment_id`
- `user_id`
- `impersonate_user_id`
- `impersonate_email`

Resolvers then pull `info.context["session"]` and often `info.context["user_id"]`.

This is the GraphQL equivalent of the REST services' `request.state` contract.

### 7.5 Data model shape

Linear defines 50 ORM tables. The model is large and closely follows the GraphQL
domain:

- issues
- attachments
- comments
- cycles
- teams
- team memberships
- organizations
- workflow states
- projects and project metadata
- initiatives and initiative metadata
- notifications
- external users
- templates
- imports
- user settings and flags
- many association and history tables

Important characteristics:

1. Column names preserve GraphQL-style camelCase heavily.
2. The schema is broad, even where only a subset is seeded by default.
3. Relationships are extensive and mirror GraphQL object graph traversal.
4. JSONB is used for flexible substructures and connection-like data.

This is the best example of "schema completeness first, seeded subset second."

### 7.6 ID and field conventions

Linear mostly uses string IDs that behave like UUIDs.

Important conventions:

- field names intentionally preserve GraphQL casing
- many payloads include `lastSyncId`
- issue identifiers combine team key plus counter
- some counters are monotonic and must be concurrency-safe

The generator must preserve external field naming, especially for GraphQL-backed apps.
Over-normalizing to snake_case would break API fidelity.

### 7.7 Scalar and schema strategy

Resolvers define custom GraphQL scalars:

- `DateTime`
- `TimelessDate`

This matters because some generated apps will need:

- SDL ingestion
- scalar generation
- input/output coercion logic

### 7.8 Behavior encoded directly in resolvers

Unlike Calendar or Box, Linear does not have a separate `operations.py`.

Business logic lives directly in resolvers. Examples:

- `viewer` resolves from auth context
- `issueCreate`:
  - validates team and assignee
  - allocates issue numbers under row lock
  - generates identifier, branch name, URL
  - defaults state to the team's backlog state
  - syncs label relationships
- `teamCreate`:
  - chooses organization from explicit input or current user
  - auto-creates team membership for creator
  - auto-creates default workflow states
  - sets default issue state

This is very important for generation. For GraphQL services, the generator may need
to emit resolver-local mutation logic rather than trying to force everything through a
generic CRUD layer.

### 7.9 Seeding strategy

`backend/utils/seed_linear_template.py`:

- creates `linear_base`
- creates `linear_default`
- creates `linear_expanded`
- quotes column identifiers
- JSON-serializes dict/list values before insert
- stores `table_order` in template metadata

The table order is long and explicit because the schema is large.

### 7.10 Seed data shape

`examples/linear/seeds/linear_default.json` currently seeds only a core subset:

- 1 organization
- 3 users
- 2 teams
- 7 workflow states
- 3 issue labels
- 4 issues
- 1 comment
- 3 team memberships

This is a critical pattern for generation:

- generate a broad schema
- seed only the minimum subset needed for benchmark realism
- leave the rest of the domain structurally available

### 7.11 Test and benchmark posture

Linear has:

- integration setup through Ariadne
- comprehensive parity validation against the real Linear GraphQL API
- a bench suite with 57 tests

### 7.12 What matters for automatic generation

If we generate a Linear-like app, we need support for:

- schema-first GraphQL generation from official SDL
- custom scalar generation
- context-aware resolver scaffolding
- large ORM graph generation
- field casing preservation
- generated resolver payload wrappers
- inline mutation logic for high-value operations
- derived defaults and side effects like auto-created workflow states
- concurrency-safe counters for externally visible identifiers

## 8. Cross-App Design Lessons For The Automatic Generation Pipeline

These are the most important takeaways from comparing all four apps.

### 8.1 The generator must branch by API style

We should not generate every app using one scaffold.

We need at least these modes:

- REST resource mode
- RPC/method-dispatch mode
- GraphQL schema-first mode

### 8.2 There are three viable serialization placements

Current repo patterns:

- model-centric serialization: Box
- handler-centric serialization: Slack
- dedicated serializer module: Calendar

The generator should select the simplest one that fits the external API:

- Box-like SDK resources benefit from model mini/full serializers
- Slack-like method APIs benefit from handler-specific serializers
- Calendar-like APIs benefit from a dedicated serializer layer

### 8.3 Seeders are part of the product, not a side script

Generation must produce:

- `Base.metadata.create_all()`-compatible schemas
- explicit table order or dependency graph
- JSON seed ingestion
- optional preprocessing hooks
- template registration logic

And optionally:

- identifier quoting
- binary asset import
- derived field computation
- index creation

### 8.4 External IDs are first-class API behavior

Examples:

- Box numeric IDs by resource type
- Slack prefix IDs plus timestamp message IDs
- Calendar email and base32hex IDs
- Linear UUID-like IDs and human-readable issue identifiers

Generated apps must specify:

- primary ID format
- secondary human-facing identifier format
- resource-specific ID generators

### 8.5 JSONB is not a smell in this repo

It is used intentionally to preserve:

- nested API payload fragments
- flexible metadata
- variant fields
- GraphQL-like substructures

The generator should prefer JSONB when the external API has deep nested blobs that do
not need heavy relational querying, but should denormalize query-critical fields when
filtering, ordering, or indexing matter.

### 8.6 Determinism matters for benchmarking

Examples:

- schema cloning
- fixed Calendar replica clock
- explicit table order
- generated issue identifiers under lock

Generated services should expose a deterministic mode by default.

### 8.7 Not every externally visible behavior maps 1:1 to stored rows

Examples:

- Calendar recurring instances are synthesized
- Slack conversation payloads are synthesized from normalized tables
- Box field filtering alters response shape without altering storage

The pipeline must model:

- stored entities
- derived entities
- transport-only response shaping

### 8.8 Partial fidelity is acceptable if it is deliberate

The current repo already accepts:

- shape-faithful generated Linear resolvers
- Calendar watch stubs
- pragmatic implementations of Box/Slack features

So the generator should support explicit capability annotations like:

- full
- partial
- stub
- shape-only

## 9. Concrete Requirements For The Automatic Schema Generation Work

Based on the current repo, an automatically generated app package should eventually be
able to produce at least the following artifacts:

1. Service-local SQLAlchemy `Base`
2. `schema.py` with service-local tables and relationships
3. API surface in the correct style:
   - REST routes
   - RPC method dispatch
   - GraphQL SDL + resolvers
4. Request/session/auth glue compatible with `IsolationMiddleware`
5. Service-specific serializers
6. Error model compatible with the external app
7. Seed script creating:
   - base template
   - one or more populated templates
   - platform metadata registration
8. Example seed JSON in repo-supported format
9. Optional test scaffold:
   - integration smoke tests
   - parity-oriented tests
   - bench suite seed hooks

## 10. Recommended Generation Heuristics

This is the distilled set of heuristics we should carry into the next steps.

### 10.1 Choose storage style by API need

- Use normalized relational tables for core entities and permissions.
- Use JSONB for nested optional payload fragments.
- Add denormalized indexed columns when query semantics need them.

### 10.2 Choose implementation shape by API style

- REST resource APIs: route file + operations + serializers
- RPC APIs: dispatcher + per-method handlers + focused operations
- GraphQL APIs: SDL + generated schema layer + resolvers with targeted handwritten patches

### 10.3 Generate seeders with hooks

Support hooks for:

- computing derived fields
- remapping asset paths
- validating identifiers
- quoting identifiers
- creating custom indexes/extensions

### 10.4 Preserve external naming

- Preserve resource names, field names, header names, and route names.
- Do not normalize away casing or ID prefixes if the external product exposes them.

### 10.5 Separate capability from completeness

The generator can create a large schema and a small default seed. That is already the
Linear pattern and is compatible with this repo.

## 11. Bottom Line

The repo does not have one "app schema format". It has one platform contract and four
different service implementation styles layered on top of it.

The automatic generation pipeline therefore needs to generate:

- a service schema compatible with per-schema isolation
- a transport layer that matches the external API style
- a seed pipeline that can populate deterministic templates
- enough behavior to make database diffs and benchmark tasks meaningful

If we preserve those four things, the generated apps will fit the repo.
If we only generate tables, they will not.
