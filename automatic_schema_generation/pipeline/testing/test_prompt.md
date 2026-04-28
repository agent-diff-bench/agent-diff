# Endpoint Verification: {{APP_NAME}} — {{SUBJECT}} (batch {{BATCH_INDEX}}/{{BATCH_TOTAL}})

You are verifying that **{{ENDPOINT_COUNT}}** endpoints of the `{{APP_SLUG}}`
replica behave correctly when called over HTTP. The replica has already been
implemented; your job is to drive it, observe the responses, fix the
implementation when it is wrong, and report the outcome.

## How the platform is wired

The backend runs in Docker on `http://localhost:8000`. It exposes a
control-plane API at `/api/platform/*` and mounts each service replica at
`/api/env/{env_id}/services/{app_slug}{{MOUNT_SUFFIX_HINT}}`.

To call any endpoint of `{{APP_SLUG}}` you first need an environment id:

```bash
# 1. List templates and pick one for this service
curl -s http://localhost:8000/api/platform/templates | jq '.templates[] | select(.service == "{{APP_SLUG}}")'

# 2. Initialise an isolated runtime environment from a template.
#    impersonateUserId is required when there is no testId — pick any
#    stable string ("test-user" works) and reuse it in the request header.
curl -s -X POST http://localhost:8000/api/platform/initEnv \
  -H 'Content-Type: application/json' \
  -d '{"templateService": "{{APP_SLUG}}", "templateName": "<template-name-from-step-1>", "impersonateUserId": "test-user"}'
# -> returns {"environmentId": "...", ...}
```

Then call the replica with the returned environmentId and the impersonation
header (the platform middleware requires it):

```bash
ENV_ID=<environmentId>
curl -s -H 'x-impersonate-user-id: test-user' \
  http://localhost:8000/api/env/$ENV_ID/services/{{APP_SLUG}}{{MOUNT_SUFFIX_HINT}}/<endpoint-path>
```

Each endpoint test must run inside its own freshly initialised environment.
Do not reuse one environmentId across multiple endpoint tests — state leaks
between tests will cause false failures.

## How to fix bugs and re-run

If an endpoint misbehaves, edit the replica source under
`{{TARGET_DIR_RELATIVE}}` (typically `database/operations.py`,
`core/serializers.py`, or `api/routes.py`). The dev backend runs uvicorn
with `--reload`, so file edits take effect within ~1 second — **no restart
is needed**. If you ever do need a hard restart (rare — only for
import-time errors), run from the repo's `ops/` directory:

```bash
cd <repo>/ops && SEED=false docker compose up -d --force-recreate backend
```

`SEED=false` is critical: a normal restart re-seeds every template database
from scratch, which wipes any environment you have already initialised.

After any code edit, re-test the endpoint that triggered the fix from a
**fresh environment** (init a new env), since the previous env may hold state
from the broken behaviour.

You may not edit any file outside `{{TARGET_DIR_RELATIVE}}` and may not
restart postgres or run alembic migrations.

## Iteration budget

For each endpoint, you have **at most {{MAX_ITERATIONS}} fix-and-retry
iterations**. If after that many attempts the endpoint still fails, mark it
as `passed: false` with a clear `diagnosis` and move on — do not block the
batch.

## Endpoints to verify

{{ENDPOINTS_BLOCK}}

## Schema definitions referenced above

```json
{{SCHEMAS_JSON}}
```

## What "verified" means for each endpoint

For every endpoint:

1. **Happy path** — call it with valid input. Response status must match the
   declared 2xx code; response body must match the declared schema shape
   (correct keys, correct types, lists where lists are declared, etc.).
   Where the endpoint requires referenced rows to exist (e.g. a `project_gid`
   for a task endpoint), seed them first via the relevant `POST` endpoint.
2. **Not-found path** — for `GET`, `PUT`, `PATCH`, `DELETE` on a path with a
   `{...}` parameter, call it with a clearly fake id. Response must be a 404
   shaped like the `{{APP_NAME}}` error envelope, not a 500.
3. **Soft-delete consistency** — if an endpoint deletes, a subsequent `GET`
   for the same id must return 404, not the deleted row.

Skip checks that do not apply (e.g. no not-found check for collection
`GET /...` endpoints with no path parameter).

## Output

When you finish the batch, write the results as JSON to:

```
{{OUTPUT_PATH}}
```

The file must be valid JSON with this exact shape — the pipeline parses it
and merges it back into `test_registry.json`:

```json
{
  "results": [
    {
      "method": "GET",
      "path": "/tasks/{task_gid}",
      "passed": true,
      "iterations": 1,
      "diagnosis": "Returns task by gid; 404 on bogus id; soft-deleted task returns 404.",
      "curl_examples": [
        "curl -H 'x-impersonate-user-id: test-user' http://localhost:8000/api/env/$ENV/services/{{APP_SLUG}}/tasks/<gid>"
      ],
      "code_changes": []
    },
    {
      "method": "POST",
      "path": "/tasks",
      "passed": false,
      "iterations": 3,
      "diagnosis": "Create returns 200 but response body omits the 'gid' field.",
      "curl_examples": ["..."],
      "code_changes": [
        {"file": "backend/src/services/{{APP_SLUG}}/core/serializers.py", "summary": "Added gid to serialize_task output"}
      ]
    }
  ]
}
```

`diagnosis` should be one or two sentences describing what you observed
(pass) or what is broken and why your fix did not resolve it (fail).
`code_changes` lists every file you edited during this batch with a one-line
summary of the change. Leave it empty if you made no edits.

Write **one entry per endpoint listed above**, in the same order. Do not
omit endpoints — if you ran out of time on one, write it with `passed:
false` and an honest diagnosis.

Do not write any other files. Do not modify `test_registry.json` directly —
the pipeline will do that after parsing your JSON output.
