# Test Suite Extension Guide (For Agent Authors)

This guide explains:

1. How test suites are represented and loaded.
2. The exact assertion-engine semantics (critical for writing valid tests).
3. A practical workflow for extending Box, Slack, Calendar, and Linear suites safely.

It is based on the current code paths in:

- `backend/utils/seed_tests.py`
- `backend/src/platform/api/routes.py`
- `backend/src/platform/evaluationEngine/{compiler.py, dsl_schema.json, assertion.py, differ.py}`

Use code behavior as source-of-truth when this guide and older docs differ.

## 1) How Tests Are Created (Prompts + Assertions)

### 1.1 Canonical suite files

Current benchmark suites are JSON files under:

- `examples/box/testsuites/box_bench.json`
- `examples/slack/testsuites/slack_bench_v2.json`
- `examples/calendar/testsuites/calendar_bench.json`
- `examples/linear/testsuites/linear_bench.json`

For Docker/runtime seeding, mirrored files live in `backend/seeds/testsuites/`.

### 1.2 Suite-level structure

Top-level shape:

```json
{
  "id": "suite-id",
  "name": "Suite Name",
  "description": "What this suite measures",
  "service": "slack|box|calendar|linear",
  "ignore_fields": {
    "global": ["created_at", "updated_at"]
  },
  "tests": [ ... ]
}
```

Notes:

- `ignore_fields` is merged into each test's evaluation spec during seeding.
- `service` is metadata for humans/tooling; the DB row stores resolved `template_schema` per test.

### 1.3 Test-level structure

In benchmark files, tests are authored with `assertions` shorthand:

```json
{
  "id": "test_12",
  "name": "Human-readable name",
  "prompt": "Natural-language task for the agent",
  "type": "actionEval",
  "seed_template": "slack_bench_v2",
  "impersonate_user_id": "U01AGENBOT9",
  "assertions": [ ... ],
  "metadata": { ... }
}
```

Important seeding behavior from `seed_tests.py`:

- Required/used fields for DB `Test`: `name`, `prompt`, `type`, `seed_template`, `impersonate_user_id`, plus `assertions`/`expected_output`.
- `metadata` and Slack `_step_sequence` are currently ignored by runtime evaluation.
- If `expected_output` is present, it is used directly; else shorthand `assertions` becomes `{"assertions": ...}`.
- `ignore_fields` at suite level is merged into each test's `expected_output.ignore_fields`.
- Test/suite UUIDs are deterministic from suite name + test id (`uuid5`), so changing `id` changes DB identity.

### 1.4 Alternative creation path via API

You can also create tests via platform API:

- `POST /api/platform/testSuites`
- `POST /api/platform/testSuites/{suite_id}/tests`

In this path, each test item carries `expected_output` and `environmentTemplate`. DSL is validated before persistence (`CoreTestManager.validate_dsl`).

## 2) Assertion Engine Logic (Critical)

This section is the most important part for writing correct tests.

## 2.1 Evaluation pipeline

At `evaluateRun`:

1. A diff is computed (snapshot-based or replication journal).
2. A spec is selected:
   - request `expectedOutput` if provided, else
   - stored test `expected_output` (when run has `test_id`), else
   - `{"assertions": []}`.
3. Spec is compiled (`DSLCompiler.compile`):
   - JSON Schema validation against `dsl_schema.json`.
   - Predicate normalization.
4. Assertions run against diff via `AssertionEngine.evaluate`.

Implication:

- If a run has no `test_id` and you do not pass `expectedOutput`, route code builds `{"assertions": []}`.
- Current DSL schema requires at least one assertion (`minItems: 1`), so this path can fail validation and produce run status `error`.
- For reliable evaluation, always provide a real spec (via `test_id` or `expectedOutput`).

## 2.2 Diff payload shape (what assertions match against)

Diff model:

```json
{
  "inserts": [ { "__table__": "...", "...": "..." } ],
  "updates": [ { "__table__": "...", "before": {...}, "after": {...} } ],
  "deletes": [ { "__table__": "...", "...": "..." } ]
}
```

Routing by `diff_type`:

- `added` -> matches rows in `inserts`
- `removed` -> matches rows in `deletes`
- `changed` -> matches rows in `updates`

Rows are filtered by `entity` via `row["__table__"] == entity`.

## 2.3 DSL validation constraints

From `dsl_schema.json`:

- Supported `diff_type`: `added`, `removed`, `changed`.
- `unchanged` is not accepted by schema.
- `assertions` is required and must contain at least 1 item.
- `where` values must be either:
  - predicate object, or
  - primitive shorthand (string/number/bool/null), normalized to `{"eq": value}`.

### Non-obvious mismatch to know

Some older tests/docs mention `unchanged` and logical combinators like `and`/`or`. Current schema/engine path does not support these as benchmark DSL inputs.

## 2.4 Predicate semantics (actual runtime)

Implemented operators:

- Equality: `eq`, `ne`
- Membership: `in`, `not_in`
- String: `contains`, `not_contains`, `i_contains`, `starts_with`, `ends_with`, `i_starts_with`, `i_ends_with`, `regex`
- Numeric/order: `gt`, `gte`, `lt`, `lte`
- Existence/list: `exists`, `has_any`, `has_all`

Behavior details:

- Multiple operators in one predicate object are ANDed.
- Multiple `where` fields are ANDed.
- Dot paths are supported for nested objects (`start.timeZone`).
- Date/datetime values are normalized to ISO strings before comparison.
- For `contains`/`i_contains` on dict/list, runtime stringifies JSON first.

## 2.5 `added` / `removed` semantics

For each assertion:

1. Candidate rows are selected by table + bucket.
2. `where` filter applied.
3. Match count checked against `expected_count`.

If `expected_count` is omitted:

- Default is at least 1 match (`actual >= 1`).

## 2.6 `changed` semantics (most common failure source)

For each update row:

1. Row matches if `where` matches `after` OR `before`.
2. Changed fields are computed by keywise inequality (`before.get(k) != after.get(k)`), excluding ignore fields.
3. `expected_changes` field checks are applied.

### `strict` mode (default `true`)

When `strict=true`, changed field set must be a subset of expected field names.

This is the key rule:

- Any extra changed field not listed in `expected_changes` fails the assertion.

When `strict=false`:

- Extra changed fields are allowed; only declared expected fields are validated.

### `expected_changes` semantics

Per field:

- Must have changed (field must be in computed changed set).
- Optional `from` predicate checks `before[field]`.
- Optional `to` predicate checks `after[field]`.

Shorthand normalization by compiler:

- `"expected_changes": {"status": "done"}` becomes `"status": {"to": {"eq": "done"}}`.
- Primitive `from`/`to` also normalize to `{"eq": ...}`.

### `changed` + missing `expected_count`

Default remains at least one matched update (`actual >= 1`).

## 2.7 `expected_count` semantics

Supported forms:

- Exact: integer
- Range: object with `min` and/or `max`

Examples:

- `1`
- `{"min": 1}`
- `{"max": 3}`
- `{"min": 1, "max": 3}`

Use explicit `expected_count` whenever possible for deterministic scoring.

## 2.8 Ignore-field precedence

Ignore set for each assertion is union of:

1. suite/test spec `ignore_fields.global`
2. suite/test spec `ignore_fields[entity]`
3. assertion-level `ignore` (or `ignore_fields` alias in runtime)

Ignored fields are excluded from changed-field computation in `changed` assertions.

## 2.9 Scoring semantics

Output score:

```json
{
  "passed": <bool>,
  "score": { "passed": X, "total": Y, "percent": ... },
  "failures": [ ... ]
}
```

Scoring is assertion-level:

- One assertion index failing multiple rows still counts as one failed assertion in score.
- Failure list may include multiple messages for that assertion.

## 2.10 Features present in schema but not enforced in runtime evaluator

- `aggregates` is defined in schema but not used by `AssertionEngine.evaluate`.

Do not rely on aggregates unless runtime evaluator is extended first.

## 3) How To Extend Suites Safely (Agent Workflow)

### 3.1 Authoring checklist per new test

1. Choose stable template/user:
   - `seed_template` must exist and contain all prerequisite entities.
   - `impersonate_user_id` must map to realistic permissions.
2. Write prompt with clear end-state:
   - Describe target objects and final conditions, not implementation details.
3. Add minimal-but-sufficient assertions:
   - Prefer 1-4 precise assertions over many weak ones.
4. For `changed` assertions:
   - Include `expected_changes`.
   - Decide `strict` intentionally (default strict is often good, but brittle if noisy fields change).
5. Set `expected_count` explicitly when cardinality matters.
6. Add/maintain `ignore_fields` for nondeterministic fields (timestamps, etags, etc.).
7. Avoid unsupported DSL constructs (`unchanged`, `and`/`or`, `aggregates` runtime assumptions).

### 3.2 Robust assertion patterns

Added row:

```json
{
  "diff_type": "added",
  "entity": "messages",
  "where": {
    "channel_id": { "eq": "C01ABCD1234" },
    "message_text": { "contains": "hello" }
  },
  "expected_count": 1
}
```

Changed row with from/to:

```json
{
  "diff_type": "changed",
  "entity": "issues",
  "where": { "id": { "eq": "ISSUE-1" } },
  "expected_changes": {
    "assigneeId": {
      "from": { "eq": "old-user" },
      "to": { "eq": "new-user" }
    }
  },
  "expected_count": 1
}
```

Changed with minimum affected rows:

```json
{
  "diff_type": "changed",
  "entity": "calendar_events",
  "where": { "calendar_id": { "eq": "cal_ops" } },
  "expected_changes": {
    "status": { "to": { "eq": "cancelled" } }
  },
  "expected_count": { "min": 1 }
}
```

Nested JSON field check:

```json
{
  "diff_type": "added",
  "entity": "calendar_events",
  "where": {
    "start.timeZone": { "eq": "America/Los_Angeles" }
  },
  "expected_count": 1
}
```

### 3.3 Common failure modes to avoid

- Missing `expected_count` unintentionally allowing "any >=1" semantics.
- `changed` assertion failing because strict mode catches extra changed fields.
- Using stale DSL forms (`unchanged`, combinators) that fail schema validation.
- Over-asserting volatile fields (`updated_at`, `etag`, generated ids).
- Writing prompts that do not force a unique, verifiable state change.
- Starting/evaluating runs without `test_id` and without `expectedOutput` (this can hit the empty-assertion fallback and fail schema validation).

### 3.4 Updating and seeding suites

1. Edit canonical file in `examples/<service>/testsuites/*.json`.
2. Mirror to `backend/seeds/testsuites/*.json` for Docker seed path.
3. Reseed:

```bash
cd backend
python utils/seed_tests.py
```

4. Run integration/perf validations relevant to your service.

## 4) Service-specific extension notes

- Slack:
  - Channel/message ids are stable in seed; good for deterministic `where`.
  - Consider thread/reaction side effects when using strict `changed`.
- Box:
  - Ignore volatile metadata (`etag`, timestamps, hash/version fields) at suite level.
  - Use entity-specific assertions for files/folders/comments/tasks as needed.
- Calendar:
  - JSON-like fields (`start`, `end`) are best checked with dot-path predicates.
  - Cancellation/clear flows often affect multiple rows; use range counts.
- Linear:
  - Many workflows are relational; combine one primary state-change assertion with one integrity assertion.
  - `from` + `to` checks are especially useful for assignee/state transitions.

## 5) Quick Pre-PR Review Checklist

- [ ] Prompt describes a unique end state.
- [ ] Assertions map directly to diffable DB effects.
- [ ] DSL validates under current schema.
- [ ] No unsupported DSL constructs used.
- [ ] `expected_count` and `strict` choices are intentional.
- [ ] Volatile fields ignored appropriately.
- [ ] Seed template and impersonated user are correct for the scenario.
