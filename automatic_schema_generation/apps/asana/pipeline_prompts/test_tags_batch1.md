# Endpoint Verification: Asana — tags (batch 1/2)

You are verifying that **7** endpoints of the `asana`
replica behave correctly when called over HTTP. The replica has already been
implemented; your job is to drive it, observe the responses, fix the
implementation when it is wrong, and report the outcome.

## How the platform is wired

The backend runs in Docker on `http://localhost:8000`. It exposes a
control-plane API at `/api/platform/*` and mounts each service replica at
`/api/env/{env_id}/services/{app_slug}`.

To call any endpoint of `asana` you first need an environment id:

```bash
# 1. List templates and pick one for this service
curl -s http://localhost:8000/api/platform/templates | jq '.templates[] | select(.service == "asana")'

# 2. Initialise an isolated runtime environment from a template.
#    impersonateUserId is required when there is no testId — pick any
#    stable string ("test-user" works) and reuse it in the request header.
curl -s -X POST http://localhost:8000/api/platform/initEnv \
  -H 'Content-Type: application/json' \
  -d '{"templateService": "asana", "templateName": "<template-name-from-step-1>", "impersonateUserId": "test-user"}'
# -> returns {"environmentId": "...", ...}
```

Then call the replica with the returned environmentId and the impersonation
header (the platform middleware requires it):

```bash
ENV_ID=<environmentId>
curl -s -H 'x-impersonate-user-id: test-user' \
  http://localhost:8000/api/env/$ENV_ID/services/asana/<endpoint-path>
```

Each endpoint test must run inside its own freshly initialised environment.
Do not reuse one environmentId across multiple endpoint tests — state leaks
between tests will cause false failures.

## How to fix bugs and re-run

If an endpoint misbehaves, edit the replica source under
`backend/src/services/asana` (typically `database/operations.py`,
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

You may not edit any file outside `backend/src/services/asana` and may not
restart postgres or run alembic migrations.

## Iteration budget

For each endpoint, you have **at most 3 fix-and-retry
iterations**. If after that many attempts the endpoint still fails, mark it
as `passed: false` with a clear `diagnosis` and move on — do not block the
batch.

## Endpoints to verify

### POST /tags
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TagCreateRequest"}}}
Responses:
  - 201: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TagResponse"}}} — Successfully created the newly specified tag.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /tags
Query parameters: workspace: string, opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/schemas/TagCompact"}},"next_page":{"$ref":"#/schemas/NextPage"}}} — Successfully retrieved the specified set of tags.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /tags/{tag_gid}
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TagResponse"}}} — Successfully retrieved the specified tag.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### PUT /tags/{tag_gid}
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TagUpdateRequest"}}}
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TagResponse"}}} — Successfully updated the specified tag.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### DELETE /tags/{tag_gid}
Needs a seeded row before this endpoint can be exercised.
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/EmptyResponse"}}} — Successfully deleted the specified tag.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /tasks/{task_gid}/tags
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/schemas/TagCompact"}},"next_page":{"$ref":"#/schemas/NextPage"}}} — Successfully retrieved the tags for the given task.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /workspaces/{workspace_gid}/tags
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/schemas/TagCompact"}},"next_page":{"$ref":"#/schemas/NextPage"}}} — Successfully retrieved the specified set of tags.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.


## Schema definitions referenced above

```json
{
  "EmptyResponse": {
    "type": "object",
    "description": "An empty object. Some endpoints do not return an object on success. The success is conveyed through a 2-- status code and returning an empty object."
  },
  "Error": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "readOnly": true,
        "description": "Message providing more detail about the error that occurred, if available.",
        "example": "project: Missing input"
      },
      "help": {
        "type": "string",
        "readOnly": true,
        "description": "Additional information directing developers to resources on how to address and fix the problem, if available.",
        "example": "For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors'"
      },
      "phrase": {
        "type": "string",
        "readOnly": true,
        "description": "*500 errors only*. A unique error phrase which can be used when contacting developer support to help identify the exact occurrence of the problem in Asana's logs.",
        "example": "6 sad squid snuggle softly"
      }
    }
  },
  "ErrorResponse": {
    "description": "Sadly, sometimes requests to the API are not successful. Failures can\noccur for a wide range of reasons. In all cases, the API should return\nan HTTP Status Code that indicates the nature of the failure,\nwith a response body in JSON format containing additional information.\n\n\nIn the event of a server error the response body will contain an error\nphrase. These phrases are automatically generated using the\n[node-asana-phrase\nlibrary](https://github.com/Asana/node-asana-phrase) and can be used by\nAsana support to quickly look up the incident that caused the server\nerror.",
    "type": "object",
    "properties": {
      "errors": {
        "type": "array",
        "items": {
          "$ref": "#/schemas/Error"
        }
      }
    }
  },
  "NextPage": {
    "type": "object",
    "nullable": true,
    "description": "*Conditional*. This property is only present when a limit query parameter is provided in the request. When making a paginated request, the API will return a number of results as specified by the limit parameter. If more results exist, then the response will contain a next_page attribute, which will include an offset, a relative path attribute, and a full uri attribute. If there are no more pages available, next_page will be null and no offset will be provided. Note that an offset token will expire after some time, as data may have changed.",
    "properties": {
      "offset": {
        "type": "string",
        "readOnly": true,
        "description": "Pagination offset for the request.",
        "example": "eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9"
      },
      "path": {
        "type": "string",
        "readOnly": true,
        "description": "A relative path containing the query parameters to fetch for next_page",
        "example": "/tasks/12345/attachments?limit=2&offset=eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9"
      },
      "uri": {
        "type": "string",
        "format": "uri",
        "readOnly": true,
        "description": "A full uri containing the query parameters to fetch for next_page",
        "example": "https://app.asana.com/api/1.0/tasks/12345/attachments?limit=2&offset=eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9"
      }
    }
  },
  "TagBase": {
    "allOf": [
      {
        "$ref": "#/schemas/TagCompact"
      },
      {
        "type": "object",
        "properties": {
          "color": {
            "type": "string",
            "description": "Color of the tag.",
            "nullable": true,
            "enum": [
              "dark-pink",
              "dark-green",
              "dark-blue",
              "dark-red",
              "dark-teal",
              "dark-brown",
              "dark-orange",
              "dark-purple",
              "dark-warm-gray",
              "light-pink",
              "light-green",
              "light-blue",
              "light-red",
              "light-teal",
              "light-brown",
              "light-orange",
              "light-purple",
              "light-warm-gray",
              null
            ],
            "example": "light-green"
          },
          "notes": {
            "description": "Free-form textual information associated with the tag (i.e. its description).",
            "type": "string",
            "example": "Mittens really likes the stuff from Humboldt."
          }
        }
      }
    ]
  },
  "TagBaseRequest": {
    "$ref": "#/schemas/TagBase"
  },
  "TagCompact": {
    "description": "A *tag* is a label that can be attached to any task in Asana. It exists in a single workspace or organization.",
    "type": "object",
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      },
      "resource_type": {
        "description": "The base type of this resource.",
        "type": "string",
        "readOnly": true,
        "example": "tag",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "Name of the tag. This is generally a short sentence fragment that fits on a line in the UI for maximum readability. However, it can be longer.",
        "type": "string",
        "example": "Stuff to buy"
      }
    }
  },
  "TagCreateRequest": {
    "allOf": [
      {
        "$ref": "#/schemas/TagBaseRequest"
      },
      {
        "type": "object",
        "properties": {
          "followers": {
            "type": "array",
            "description": "An array of strings identifying users. These can either be the string \"me\", an email, or the gid of a user.",
            "items": {
              "type": "string"
            },
            "example": [
              "12345",
              "42563"
            ]
          },
          "workspace": {
            "type": "string",
            "x-env-variable": true,
            "description": "Gid of an object.",
            "example": "12345"
          }
        }
      }
    ]
  },
  "TagResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/TagBase"
      },
      {
        "type": "object",
        "properties": {
          "created_at": {
            "description": "The time at which this resource was created.",
            "type": "string",
            "format": "date-time",
            "readOnly": true,
            "example": "2012-02-22T02:06:58.147Z"
          },
          "followers": {
            "description": "Array of users following this tag.",
            "type": "array",
            "readOnly": true,
            "items": {
              "$ref": "#/schemas/UserCompact"
            }
          },
          "workspace": {
            "$ref": "#/schemas/WorkspaceCompact"
          },
          "permalink_url": {
            "type": "string",
            "readOnly": true,
            "description": "A url that points directly to the object within Asana.",
            "example": "https://app.asana.com/0/resource/123456789/list"
          }
        }
      }
    ]
  },
  "TagUpdateRequest": {
    "$ref": "#/schemas/TagBaseRequest"
  },
  "UserCompact": {
    "description": "A *user* object represents an account in Asana that can be given access to various workspaces, projects, and tasks.",
    "type": "object",
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      },
      "resource_type": {
        "description": "The base type of this resource.",
        "type": "string",
        "readOnly": true,
        "example": "user",
        "x-insert-after": "gid"
      },
      "name": {
        "type": "string",
        "description": "*Read-only except when same user as requester*. The user's name.",
        "example": "Greg Sanchez"
      }
    }
  },
  "WorkspaceCompact": {
    "description": "A *workspace* is the highest-level organizational unit in Asana. All projects and tasks have an associated workspace.",
    "type": "object",
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      },
      "resource_type": {
        "description": "The base type of this resource.",
        "type": "string",
        "readOnly": true,
        "example": "workspace",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "The name of the workspace.",
        "type": "string",
        "example": "My Company Workspace"
      }
    }
  }
}
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
   shaped like the `Asana` error envelope, not a 500.
3. **Soft-delete consistency** — if an endpoint deletes, a subsequent `GET`
   for the same id must return 404, not the deleted row.

Skip checks that do not apply (e.g. no not-found check for collection
`GET /...` endpoints with no path parameter).

## Output

When you finish the batch, write the results as JSON to:

```
automatic_schema_generation/apps/asana/pipeline_out/test_results/tags_batch1.json
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
        "curl -H 'x-impersonate-user-id: test-user' http://localhost:8000/api/env/$ENV/services/asana/tasks/<gid>"
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
        {"file": "backend/src/services/asana/core/serializers.py", "summary": "Added gid to serialize_task output"}
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
