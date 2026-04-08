# REST API MVP Implementation Plan

This document is the execution plan for building the REST schema-generation MVP.
It is intentionally shorter than the architecture spec and focuses on what to
implement next.

## 1. MVP Goal

Build a working pipeline that takes:

- `openapi.source.json`
- `source_app.yaml` (simplified contract)

and produces a runnable REST replica scaffold plus endpoint-by-endpoint outputs
that can be validated against the real source API.

## 2. MVP Assumptions

- OpenAPI input is JSON only.
- Auth type is bearer only.
- The agent is allowed high autonomy.
- Read and write parity are attempted by default.
- Safety constraints for mutation checks are inferred and enforced at runtime.

## 3. Scope In

- Intake validation for minimal input bundle.
- OpenAPI normalization and endpoint catalog.
- Contract freeze artifacts needed for implementation.
- Standard scaffold generation.
- Endpoint work-packet generation.
- Endpoint implementation loop (one endpoint at a time).
- Runtime parity checks and mismatch reporting.
- Seed base/default synthesis.
- Benchmark docs generation in standardized JSON format.

## 4. Scope Out (for MVP)

- GraphQL pipeline.
- Multiple auth types.
- YAML OpenAPI ingestion.
- Fully configurable verification-policy input schema.
- Advanced orchestration and scheduling.

## 5. Deliverables

Required deliverables for MVP completion:

1. Pipeline code under `automatic_schema_generation/pipeline/rest/`.
2. App workspace generation under `automatic_schema_generation/apps/<app_slug>/`.
3. Machine-readable schema validation for:
   - `source_app.yaml`
   - `app_manifest.yaml`
   - `endpoint_packet.yaml`
   - `docs_fragment.json`
   - `status.yaml`
4. Deterministic checkpointing and restart support.
5. Generated repo-ready service scaffold files.
6. Per-endpoint parity reports and docs fragments.
7. Final merged benchmark docs JSON.

## 6. Implementation Phases

### Phase 0: Project skeleton

Implement:

- pipeline package structure
- CLI entrypoint
- config loading
- checkpoint manager

Output:

- `pipeline/rest/` module imports cleanly
- `run_mvp_pipeline` command executes a no-op dry run

### Phase 1: Intake and normalization

Implement:

- input bundle validation
- OpenAPI JSON parse and normalization
- endpoint catalog extraction

Output:

- `normalized/openapi.normalized.json`
- `normalized/endpoint_catalog.json`
- stage `00` and `01` checkpoints

Acceptance:

- invalid input fails fast with actionable error
- valid input produces deterministic normalized artifacts

### Phase 2: Contract freeze artifacts

Implement:

- resource catalog extraction
- dependency graph
- initial `app_manifest.yaml`
- initial `docs_contract.yaml`
- initial `seed_contract.yaml`

Output:

- stage `03` checkpoint and artifacts in `normalized/`

Acceptance:

- every endpoint maps to at least one resource
- unresolved ambiguities are recorded as explicit blocked items

### Phase 3: Scaffold generation

Implement generator for mandatory service files:

- `api/routes.py`
- `core/errors.py`
- `core/serializers.py`
- `core/utils.py`
- `database/base.py`
- `database/schema.py`
- `database/operations.py`

Also generate:

- workspace `AGENTS.md`
- prompt templates

Acceptance:

- scaffold files include standard markers
- generated module tree imports without syntax errors

### Phase 4: Endpoint planning

Implement:

- one packet per endpoint
- dependency-aware ordering
- packet file creation:
  - `endpoint_packet.yaml`
  - `TASK.md`
  - `parity_case.yaml`
  - `docs_fragment.json` (initial skeleton)

Acceptance:

- all normalized endpoints have packets
- packet dependencies form an acyclic graph

### Phase 5: Endpoint implementation loop

Implement loop driver:

- dispatch one packet at a time to implementation agent
- enforce allowed file boundaries
- require packet completion report

Acceptance:

- implemented packets produce code + docs fragment + parity artifacts
- failed packets remain retryable without corrupting prior checkpoints

### Phase 6: Runtime parity engine (MVP)

Implement:

- source vs replica request execution
- response normalization for volatile fields inferred at runtime
- mutation safety guards:
  - deterministic namespacing/prefixing
  - deterministic cleanup plan
  - constrained replay and rate-limit-aware retries

Acceptance:

- parity report per packet:
  - status code
  - headers (required subset)
  - shape diffs
  - side-effect diffs for mutations

### Phase 7: Seeds and docs assembly

Implement:

- generation of `<app_slug>_base.json` and `<app_slug>_default.json`
- seed script scaffold
- docs fragment merge into:
  - `examples/<app_slug>/testsuites/<app_slug>_docs/<app_slug>_api_full_docs.json`

Acceptance:

- seed artifacts are deterministic
- docs file validates against standardized format

### Phase 8: Validation and readiness

Implement final gates:

- schema validity
- seed validity
- route mount smoke
- parity completion summary
- docs coverage and format checks

Output:

- `reports/validation_summary.md`
- `reports/parity_summary.md`
- readiness checkpoint

## 7. Execution Order for First Real App

Use this exact order for the first app integration:

1. Run phases 0-3 once.
2. Generate packets for read endpoints first.
3. Complete read parity baseline.
4. Enable mutation packets with runtime safety guards.
5. Generate seeds and docs.
6. Run full readiness gates.

## 8. Definition of MVP Done

MVP is complete when one REST app can go end-to-end through the pipeline and
produce all mandatory outputs without manual file creation.

Minimum success criteria:

1. Input bundle validates.
2. Endpoint packets generated for full OpenAPI surface.
3. At least one read and one mutation endpoint implemented via packet loop.
4. Parity reports generated with explicit pass/fail reasons.
5. Base/default seeds and benchmark docs JSON generated.
6. Final readiness report produced.

## 9. Immediate Next Tasks

1. Implement schema validators for the five contract files.
2. Build phases 0-1 and lock checkpoint format.
3. Build scaffold generator (phase 3) before endpoint automation.
4. Build packet generator (phase 4) and parity harness (phase 6).
5. Run first end-to-end trial on one small REST API surface.
