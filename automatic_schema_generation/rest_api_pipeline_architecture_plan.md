# REST API Automatic Schema Generation Pipeline Specification

This document defines the standardized pipeline for generating new REST API app
replicas for Agent-Diff inside `automatic_schema_generation/`.

The purpose of this specification is to remove hidden assumptions. A generated
REST app must be buildable, verifiable, seedable, and benchmark-documentable
from a minimal, explicitly standardized input bundle. Optional extra material
may accelerate the process, but the pipeline must not rely on it.

This specification is intentionally stricter than the current hand-built apps.
It is written to minimize rework, maximize restartability, and make agent work
deterministic.

## 1. Scope

This document applies only to new REST API app generation.

It does not yet define the GraphQL pipeline. Linear-like generation will be
specified separately.

The pipeline defined here must produce outputs compatible with the current repo:

- isolated per-environment PostgreSQL schemas
- service-local SQLAlchemy models
- Starlette/FastAPI-compatible route handlers mounted by the platform
- deterministic seed templates
- benchmark-facing API documentation JSON

## 2. Design Principles

The pipeline MUST optimize for the following:

1. Determinism.
2. Restartability from checkpoints.
3. Minimal human input.
4. No undocumented assumptions.
5. Endpoint-by-endpoint agent work.
6. Live parity verification against the source app.
7. Standardized file layout and scaffold markers.
8. Strict separation between internal planning artifacts and final repo outputs.

The pipeline MUST prefer a blocked state over inventing behavior.

## 3. Normative Language

The words `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`, and `MAY`
are used in the RFC sense.

If this document says a file or checkpoint `MUST` exist, the pipeline is not
allowed to skip it even if an agent believes it can infer the missing step.

## 4. Non-Negotiable Rules

### 4.1 No hidden dependencies

The pipeline MUST assume that no human-authored supplementary docs exist beyond
the standardized input bundle defined below.

Optional extra inputs MAY be accepted, but they MUST be treated as accelerators,
not as structural requirements.

### 4.2 No direct endpoint coding before contract freeze

The pipeline MUST NOT start endpoint implementation before it has frozen:

- the resource catalog
- the entity/table plan
- the auth contract
- the pagination contract
- the error envelope contract
- the live verification policy

### 4.3 No uncontrolled writes to the source app

The pipeline MUST NOT run mutation parity checks against the real source app
without runtime-generated safety guards and deterministic cleanup.

If runtime safeguards cannot be inferred or enforced, mutation packets MUST be
marked blocked.

### 4.4 One endpoint packet, one unit of agent work

Each endpoint MUST be implemented through a standardized work packet. Agents
MUST NOT be asked to implement arbitrary bundles of unrelated endpoints in one
step.

### 4.5 Docs are part of the product

The benchmark-facing API documentation is a mandatory generated artifact, not a
nice-to-have side file.

## 5. Standardized Bare-Minimum External Input Bundle

The pipeline MUST require exactly one standardized input bundle per app:

```text
automatic_schema_generation/apps/<app_slug>/
  inputs/
    openapi.source.json
    source_app.yaml
```

No other external file is required.

Secrets MUST NOT be stored in repo files. `source_app.yaml` MUST reference
environment variable names, not raw secret values.

### 5.1 Required file: `openapi.source.json`

This is the raw source OpenAPI specification.

For MVP, only JSON OpenAPI input is supported.

The pipeline MUST treat it as immutable source material and MUST create a
normalized copy later instead of editing the raw file in place.

### 5.2 Required file: `source_app.yaml`

This file standardizes everything the pipeline needs that OpenAPI usually does
not fully capture.

It MUST contain the following fields:

| Field | Required | Description |
| --- | --- | --- |
| `app_name` | yes | Human-readable source app name |
| `app_slug` | yes | Stable repo/service slug |
| `service_mount_name` | yes | URL mount segment under `/services/<name>` |
| `source_base_url` | yes | Real source app API base URL |
| `auth.env` | yes | Map from logical credential name to env var name |
| `principal.kind` | yes | `user_id`, `email`, `account_id`, or `unknown` |
| `seed.minimum_principal_record` | yes | Minimal identity fields needed in the default seed |

MVP assumptions:

- OpenAPI input is JSON-only.
- Auth type is bearer-only.
- Default headers are inferred during live parity execution.
- Principal identity value lookup is inferred by the agent workflow.
- Read and write verification behavior is always attempted and runtime-guarded.
- Volatile fields and disallowed operations are inferred during execution.

The pipeline MUST reject the input bundle if any required field is missing.

### 5.3 Example `source_app.yaml`

```yaml
app_name: Acme Drive
app_slug: acme_drive
service_mount_name: acme_drive
source_base_url: https://api.acmedrive.com/v1

auth:
  env:
    token: ACME_DRIVE_TOKEN

principal:
  kind: user_id

seed:
  minimum_principal_record:
    id_env: ACME_DRIVE_USER_ID
    email_env: ACME_DRIVE_USER_EMAIL
    display_name_env: ACME_DRIVE_USER_NAME
```

## 6. Optional External Accelerators

The pipeline MAY accept extra source material such as:

- Postman collections
- vendor docs
- example responses
- handwritten field notes
- existing SDK snippets

These MUST be stored under:

```text
automatic_schema_generation/apps/<app_slug>/inputs/optional/
```

The pipeline MUST remain valid when this directory is empty.

## 7. Standardized App Workspace Layout

Each app under generation MUST use the following layout:

```text
automatic_schema_generation/apps/<app_slug>/
  inputs/
    openapi.source.json
    source_app.yaml
    optional/
  normalized/
    openapi.normalized.json
    app_manifest.yaml
    endpoint_catalog.json
    resource_catalog.json
    dependency_graph.json
    auth_contract.yaml
    error_contract.yaml
    pagination_contract.yaml
    docs_contract.yaml
    seed_contract.yaml
  checkpoints/
    00_intake/
    01_openapi_normalization/
    02_live_surface_survey/
    03_contract_freeze/
    04_scaffold_generation/
    05_foundation_implementation/
    06_endpoint_planning/
    07_endpoint_implementation/
    08_seed_synthesis/
    09_docs_assembly/
    10_validation_and_readiness/
  work_packets/
    000_<operation_slug>/
  prompts/
    system/
    endpoint/
  generated/
    app/
    repo_patch_plan/
  reports/
    intake_report.md
    parity_summary.md
    validation_summary.md
  AGENTS.md
```

The workspace MUST be treated as the system of record for generation. Final repo
outputs are derived from it.

## 8. Standardized Checkpoint Contract

Every checkpoint directory MUST contain:

- `status.yaml`
- `inputs.json`
- `outputs.json`
- `notes.md`

`status.yaml` MUST include:

| Field | Description |
| --- | --- |
| `stage_id` | Stable stage identifier |
| `stage_name` | Human-readable stage name |
| `status` | `pending`, `in_progress`, `passed`, `blocked`, or `failed` |
| `started_at` | ISO timestamp |
| `finished_at` | ISO timestamp or null |
| `input_hash` | Hash over declared stage inputs |
| `output_hash` | Hash over declared stage outputs |
| `blocked_reason` | Required if blocked |
| `owner` | `pipeline`, `agent`, or `human` |

The pipeline MUST NOT mutate a passed checkpoint without updating its hashes and
downstream invalidation records.

## 9. Required Pipeline Stages

The stages below are mandatory and ordered.

### 9.1 Stage 00: Intake

Purpose:

- validate the input bundle
- copy nothing yet
- fail early on missing required metadata

Required outputs:

- `reports/intake_report.md`
- `checkpoints/00_intake/status.yaml`
- `checkpoints/00_intake/inputs.json`
- `checkpoints/00_intake/outputs.json`

Pass criteria:

- OpenAPI file parses
- `source_app.yaml` validates against the standardized schema
- required secret env var names are present as names, not values

### 9.2 Stage 01: OpenAPI Normalization

Purpose:

- convert raw OpenAPI into a canonical machine-friendly form
- resolve `$ref`s
- flatten parameter inheritance
- normalize operation ids

Required outputs:

- `normalized/openapi.normalized.json`
- `normalized/endpoint_catalog.json`
- `checkpoints/01_openapi_normalization/*`

`endpoint_catalog.json` MUST contain one record per operation with:

- `operation_id`
- `method`
- `path`
- `summary`
- `tags`
- `request_body_schema_ref`
- `response_schema_refs`
- `security_requirements`
- `path_params`
- `query_params`
- `header_params`
- `depends_on_resources`

### 9.3 Stage 02: Live Surface Survey

Purpose:

- probe the real source app for behavior OpenAPI often omits
- confirm auth
- sample read responses
- detect undocumented headers and error envelopes

Required outputs:

- `normalized/auth_contract.yaml`
- `normalized/error_contract.yaml`
- `normalized/pagination_contract.yaml`
- `reports/live_surface_survey.md`
- `checkpoints/02_live_surface_survey/*`

The survey MUST execute read probes unconditionally.

Mutation probes MUST also be attempted by default with runtime safety guards.
If those guards cannot be established for a packet, that packet MUST be marked
blocked with an explicit reason.

### 9.4 Stage 03: Contract Freeze

Purpose:

- derive the resource model and relational storage plan before any endpoint coding

Required outputs:

- `normalized/resource_catalog.json`
- `normalized/dependency_graph.json`
- `normalized/app_manifest.yaml`
- `normalized/docs_contract.yaml`
- `normalized/seed_contract.yaml`
- `checkpoints/03_contract_freeze/*`

`app_manifest.yaml` MUST freeze:

- service slug and mount path
- primary resources
- table list
- foreign-key edges
- id generation policy
- timestamp policy
- null-vs-omitted response policy
- binary/blob handling policy
- pagination policy
- error envelope policy
- impersonation strategy inside Agent-Diff

No endpoint implementation may start before this stage passes.

### 9.5 Stage 04: Scaffold Generation

Purpose:

- emit all required files with standardized markers and empty implementations

Required outputs:

- workspace-local generated scaffolds under `generated/app/`
- generated `AGENTS.md`
- template prompt files under `prompts/`
- `checkpoints/04_scaffold_generation/*`

Every scaffolded file MUST contain reserved markers so endpoint-level agents can
edit targeted sections without restructuring the file.

### 9.6 Stage 05: Foundation Implementation

Purpose:

- implement shared infrastructure before per-endpoint work starts

Required outputs:

- functioning base ORM setup
- shared error helpers
- shared serializers/utilities
- empty but valid route registration file
- seed script skeleton
- validation test skeleton
- `checkpoints/05_foundation_implementation/*`

This stage MUST produce importable Python modules and a schema that can at least
run `Base.metadata.create_all()`.

### 9.7 Stage 06: Endpoint Planning

Purpose:

- break the API into one standardized work packet per endpoint
- order them by dependency

Required outputs:

- one directory under `work_packets/` per operation
- `reports/endpoint_plan.md`
- `checkpoints/06_endpoint_planning/*`

### 9.8 Stage 07: Endpoint Implementation

Purpose:

- execute the work packets one at a time

Required outputs:

- completed per-endpoint packets
- incremental code generation in `generated/app/`
- per-endpoint parity reports
- `checkpoints/07_endpoint_implementation/*`

### 9.9 Stage 08: Seed Synthesis

Purpose:

- generate deterministic base and default templates

Required outputs:

- seed JSON files
- seed script
- table order file
- seed validation report
- `checkpoints/08_seed_synthesis/*`

### 9.10 Stage 09: Docs Assembly

Purpose:

- produce standardized benchmark-facing API docs and richer internal docs

Required outputs:

- internal docs contract artifacts
- final benchmark docs JSON
- docs coverage report
- `checkpoints/09_docs_assembly/*`

### 9.11 Stage 10: Validation And Readiness

Purpose:

- prove the generated app is repo-compatible and minimally benchmark-ready

Required outputs:

- readiness report
- unresolved gaps report if any
- `checkpoints/10_validation_and_readiness/*`

## 10. Standardized Generated Repo Output

Every generated REST app MUST eventually emit the following repo files:

```text
backend/src/services/<app_slug>/
  __init__.py
  api/
    __init__.py
    routes.py
  core/
    __init__.py
    errors.py
    serializers.py
    utils.py
  database/
    __init__.py
    base.py
    schema.py
    operations.py

backend/utils/
  seed_<app_slug>_template.py

examples/<app_slug>/
  seeds/
    <app_slug>_base.json
    <app_slug>_default.json
  testsuites/
    <app_slug>_docs/
      <app_slug>_api_full_docs.json

backend/seeds/<app_slug>/
  <app_slug>_base.json
  <app_slug>_default.json

backend/tests/integration/
  test_<app_slug>_environment_lifecycle.py
  test_<app_slug>_api_smoke.py

backend/tests/validation/
  test_<app_slug>_api_parity.py
```

The workspace MAY generate additional helper artifacts, but it MUST NOT skip any
of the files above.

## 11. Standardized Scaffold Contracts

The scaffold layer MUST be universal across all generated REST apps.

### 11.1 Shared marker format

All scaffolded Python files MUST use explicit markers:

```python
# BEGIN AUTOGENERATED IMPORTS
# END AUTOGENERATED IMPORTS

# BEGIN SHARED HELPERS
# END SHARED HELPERS

# BEGIN RESOURCE DECLARATIONS
# END RESOURCE DECLARATIONS

# BEGIN ENDPOINT IMPLEMENTATIONS
# END ENDPOINT IMPLEMENTATIONS
```

Each file MAY use only the marker subsets relevant to that file, but the marker
names themselves MUST stay standardized.

### 11.2 `database/base.py`

This file MUST define:

- one service-local SQLAlchemy declarative base
- common typed mixins if used
- no business logic

### 11.3 `database/schema.py`

This file MUST contain:

- all ORM models
- all table names
- all foreign keys
- JSONB and blob field declarations
- serialization-neutral storage definitions

It MUST NOT contain route logic.

### 11.4 `database/operations.py`

This file MUST contain:

- all Session-first CRUD helpers
- list/filter/pagination helpers
- mutation helpers
- resource lookup helpers

Functions in this file MUST accept a Session-like object as the first argument
after any request-independent configuration values.

### 11.5 `core/errors.py`

This file MUST contain:

- app-native error envelope builders
- exception-to-response translation helpers
- reusable status and code mappings

### 11.6 `core/serializers.py`

This file MUST contain:

- request body normalization helpers
- response serialization helpers
- sparse field projection helpers if the app supports them
- null/omission enforcement helpers

### 11.7 `core/utils.py`

This file MUST contain only shared pure utilities such as:

- id formatting helpers
- timestamp normalization helpers
- header parsing helpers
- pagination token helpers
- content-type helpers

### 11.8 `api/routes.py`

This file MUST contain:

- route registration
- request-state access helpers
- endpoint handlers
- no inline schema declarations

Handlers MUST read DB access from `request.state.db_session`.

## 12. Standardized Generated AGENTS File

Each app workspace MUST contain:

```text
automatic_schema_generation/apps/<app_slug>/AGENTS.md
```

This file is mandatory and MUST be generated by the pipeline, not handwritten ad
hoc.

It MUST contain the following sections:

1. Service goal and scope.
2. Frozen app contract summary.
3. File ownership and allowed edit targets.
4. Standard endpoint implementation procedure.
5. Standard parity verification procedure.
6. Docs update procedure.
7. Seed safety and cleanup rules.
8. Stop conditions and blocked-state rules.

The AGENTS file MUST explicitly instruct agents to avoid inventing behavior not
supported by OpenAPI or live verification.

### 12.1 Standardized prompt templates

The workspace MUST also generate standardized prompt files under:

```text
automatic_schema_generation/apps/<app_slug>/prompts/
  system/
    foundation_system.md
    endpoint_system.md
  endpoint/
    foundation_task.md
    endpoint_task_template.md
    parity_repair_task.md
```

These prompt files MUST be treated as templates, not one-off notes.

`foundation_system.md` MUST define:

- the repo runtime contract
- the frozen app contract
- the standardized file layout
- the rule that behavior must not be invented

`endpoint_system.md` MUST define:

- the endpoint packet workflow
- editable file boundaries
- required parity and docs updates
- blocked-state escalation rules

`foundation_task.md` MUST be used only during stage 05 and MUST describe the
shared infrastructure to build before endpoint work begins.

`endpoint_task_template.md` MUST accept packet substitutions and MUST instruct
the agent to update code, docs, parity artifacts, and the completion report as
one atomic unit of work.

`parity_repair_task.md` MUST be used when an endpoint implementation exists but
the parity report fails. It MUST focus the agent on repairing mismatches instead
of broad refactoring.

## 13. Standardized Endpoint Work Packet

Each endpoint MUST have its own directory:

```text
automatic_schema_generation/apps/<app_slug>/work_packets/<nnn>_<operation_slug>/
  endpoint_packet.yaml
  TASK.md
  parity_case.yaml
  docs_fragment.json
  completion_report.yaml
```

### 13.1 `endpoint_packet.yaml`

This file MUST contain:

| Field | Description |
| --- | --- |
| `packet_id` | Stable packet id |
| `operation_id` | Canonical operation id |
| `method` | HTTP method |
| `path` | Source path |
| `resource` | Primary resource name |
| `category` | `auth`, `list`, `get`, `create`, `update`, `delete`, `search`, `nested`, `batch`, `upload`, `download`, or `other` |
| `dependencies` | Packet ids that must pass first |
| `schema_entities` | ORM entities touched |
| `operations_functions` | Operation helpers to create or edit |
| `serializers_needed` | Serializer helpers to create or edit |
| `request_contract` | Normalized request summary |
| `response_contract` | Normalized response summary |
| `error_contract` | Error behavior summary |
| `verification_mode` | `read_shape`, `write_shape`, or `write_side_effect` |
| `allowed_files` | Files the endpoint agent is allowed to edit |
| `docs_key` | Final docs JSON key, `METHOD /path` |
| `seed_preconditions` | Required seed rows or relationships |
| `acceptance_checks` | Concrete required checks |

### 13.2 `TASK.md`

This file MUST translate the packet into agent-readable instructions and MUST
include:

- what to implement
- what not to change
- which files are editable
- what parity command to run
- what docs fragment to update
- what counts as done

### 13.3 `parity_case.yaml`

This file MUST define the exact source-app check for the endpoint, including:

- request template
- environment variable substitutions
- expected status code
- normalization rules
- side-effect verification reads if the endpoint mutates data

### 13.4 `docs_fragment.json`

This file MUST contain the benchmark-doc entry for that endpoint only.

The final benchmark docs file is assembled by merging these fragments in stage 09.

## 14. Required Endpoint Ordering Strategy

The pipeline MUST generate endpoint packets in a dependency-safe order.

The default order SHOULD be:

1. auth and self-identity endpoints
2. simple read endpoints: `GET /resource`, `GET /resource/{id}`
3. create endpoints
4. update and patch endpoints
5. delete endpoints
6. nested resource endpoints
7. search/filter/pagination variants
8. uploads/downloads/binary endpoints
9. bulk, batch, import/export, and long-running operations

The pipeline MAY override this order if the resource dependency graph requires it.

## 15. Standardized Live Verification Contract

Live verification is mandatory whenever the source app can be accessed safely.

The verification layer MUST compare:

- HTTP status code
- content type
- required response headers
- top-level response shape
- null-vs-missing behavior
- enum spellings
- pagination metadata
- documented error envelopes
- post-mutation readback state when applicable

The verification layer MUST normalize only runtime-generated volatile-field
artifacts. It MUST NOT silently ignore mismatches.

### 15.1 Verification modes

- `read_shape`: compare read endpoint output shape
- `write_shape`: compare immediate mutation response shape
- `write_side_effect`: compare subsequent read state after mutation

### 15.2 MVP mutation safety rules

Mutation-like packets in categories `create`, `update`, `delete`, `upload`,
`batch`, or `other` MUST be attempted by default.

Before each mutation check, the parity harness MUST apply runtime safety guards:

- deterministic test resource namespacing/prefixing
- deterministic cleanup plan
- constrained replay and rate-limit-aware execution

If cleanup cannot be guaranteed for a mutation packet, that packet MUST be
blocked and recorded as unresolved.

Disallowed operations and rate-limit constraints MUST be inferred during
execution and recorded in validation artifacts.

## 16. Standardized Seed Contract

Every generated REST app MUST create two template seeds:

- `<app_slug>_base`
- `<app_slug>_default`

### 16.1 `<app_slug>_base`

This MUST be the minimal valid environment:

- all tables present
- the acting principal exists
- required parent/container/workspace objects exist
- zero or near-zero business objects beyond structural necessities

### 16.2 `<app_slug>_default`

This MUST be the minimum useful non-empty environment:

- principal record exists
- at least one realistic container or workspace exists
- enough objects exist to exercise list/get/update/delete flows
- ids are deterministic
- timestamps are deterministic where possible

### 16.3 Seed artifacts

The seed stage MUST produce:

```text
normalized/seed_contract.yaml
generated/app/examples/<app_slug>/seeds/<app_slug>_base.json
generated/app/examples/<app_slug>/seeds/<app_slug>_default.json
generated/app/backend/utils/seed_<app_slug>_template.py
generated/app/backend/src/services/<app_slug>/database/table_order.json
```

The actual repo may not need `table_order.json` at runtime, but the workspace
MUST keep a machine-readable table order artifact.

## 17. Standardized Benchmark Documentation Contract

The benchmark-facing docs file is mandatory:

```text
examples/<app_slug>/testsuites/<app_slug>_docs/<app_slug>_api_full_docs.json
```

This file is for downstream benchmark and test-suite creation. It MUST use a
strict standardized format.

### 17.1 Top-level structure

- top level MUST be a JSON object
- each key MUST be `METHOD /path`
- keys MUST be sorted in packet order

### 17.2 Required per-endpoint fields

Each endpoint entry MUST contain:

| Field | Required | Notes |
| --- | --- | --- |
| `description` | yes | Plain-language endpoint summary |
| `parameters.path` | yes | Object, possibly empty |
| `parameters.query` | yes | Object, possibly empty |
| `parameters.header` | yes | Object, possibly empty |
| `parameters.body` | yes | Object, possibly empty |
| `response` | yes | Normalized success-response contract |
| `errors` | yes | List of standardized error cases |
| `example_request` | yes | One canonical example |
| `example_response` | yes | One canonical example |
| `source` | yes | Traceability metadata |

Empty parameter groups MUST be `{}`. The file MUST NOT use `"None"` strings.

### 17.3 Required `source` subfields

Each endpoint's `source` object MUST contain:

- `operation_id`
- `openapi_present`
- `live_verified`
- `verification_mode`
- `notes`

### 17.4 Internal docs vs benchmark docs

The pipeline MUST keep richer internal contracts under `normalized/`.

The benchmark docs JSON MUST remain simpler and stable. It is not the place to
store every internal planning detail.

## 18. Standardized Example Snapshot Contract

Because benchmark creation will depend on examples later, the pipeline MUST also
generate canonical parity-backed snapshots per endpoint under:

```text
automatic_schema_generation/apps/<app_slug>/reports/parity_snapshots/<operation_id>/
```

Each such directory MUST contain:

- `request.json`
- `source_response.json`
- `replica_response.json`
- `normalized_diff.json`

These are internal artifacts. They do not replace the benchmark docs JSON.

## 19. Standardized Validation Gates

The generated REST app is not ready until it passes all mandatory gates below.

### 19.1 Gate A: Input validity

- input bundle parses
- required fields present

### 19.2 Gate B: Contract completeness

- endpoint catalog complete
- resource catalog complete
- seed contract frozen
- docs contract frozen

### 19.3 Gate C: Schema validity

- service imports successfully
- `Base.metadata.create_all()` succeeds
- foreign keys resolve

### 19.4 Gate D: Seed validity

- base seed loads
- default seed loads
- template registration works
- schema clone works

### 19.5 Gate E: Endpoint smoke validity

- generated routes mount successfully
- required handlers return non-500 responses for smoke cases

### 19.6 Gate F: Parity validity

- all unblocked read packets pass parity
- all allowed write packets pass shape and side-effect parity
- blocked packets are explicitly accounted for

### 19.7 Gate G: Docs validity

- every implemented endpoint has a docs fragment
- final docs JSON merges cleanly
- parameter groups always use objects
- docs keys exactly match packet `docs_key` values

### 19.8 Gate H: Repo readiness

- required repo output tree exists
- required tests exist
- readiness report lists no unknown gaps

## 20. Mandatory Blocked States

The pipeline MUST stop and mark the stage as blocked, not improvise, when:

1. OpenAPI omits critical request or response structure and live verification cannot resolve it.
2. Auth works only through undocumented browser/session flows that are not standardized yet.
3. Mutation verification is required but runtime safety and cleanup guarantees cannot be established.
4. The resource model cannot be mapped to deterministic relational storage without a manual contract decision.
5. Binary transport or async job semantics require unsupported infrastructure.

Blocked states MUST generate a concrete artifact describing what additional input
is required to proceed.

## 21. No-Rework Operating Rules

The pipeline MUST follow these rules to avoid expensive rewrites:

1. Freeze the entity model before endpoint coding.
2. Implement shared infrastructure before the first endpoint packet.
3. Treat each endpoint packet as responsible for code, docs, parity, and report updates together.
4. Do not let later packets silently redefine tables or shared helper semantics.
5. If a packet requires a contract change, reopen stage 03 explicitly and invalidate downstream checkpoints.

## 22. Minimum Definition Of Done For A Generated REST App

A REST app generated by this pipeline is considered ready only when all of the
following are true:

1. The app has a complete workspace under `automatic_schema_generation/apps/<app_slug>/`.
2. The standardized repo output tree exists.
3. Base and default seeds exist and can be cloned through the isolation engine.
4. All unblocked endpoint packets are implemented and have completion reports.
5. Live parity results exist for all unblocked packets.
6. Benchmark-facing docs JSON exists in the standardized format.
7. Validation and readiness reports exist with no unknown failures.

## 23. Recommended Next Implementation Step

Before writing any generator code, the repo should define machine-readable schemas
for the following files first:

- `source_app.yaml`
- `app_manifest.yaml`
- `endpoint_packet.yaml`
- `docs_fragment.json`
- `status.yaml`

That should be the first implementation milestone. Without those schemas, the
pipeline will drift immediately.
