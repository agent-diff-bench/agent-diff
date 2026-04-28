# Entity Implementation (Pass 1 — Base): tags

You are implementing the **tags** resource for the Asana API
replica. Build the base model, CRUD operations, serializers, and route handlers.

**Do NOT add ForeignKey columns, relationship() declarations, or association
tables in this pass.** Those will be added in a separate step. Focus only on
the resource's own columns, operations, and endpoints.

The full OpenAPI spec is available at: `/Users/azh/agent-diff/automatic_schema_generation/apps/asana/inputs/openapi.scoped.json`
If any information in this prompt is unclear or seems incorrect, read the
spec directly to resolve ambiguities.

Files to edit (all under `/Users/azh/agent-diff/backend/src/services/asana`):
- `database/schema.py`
- `database/operations.py`
- `core/serializers.py`
- `api/routes.py`

---

## Section 1: tags

### Identity

- Table name: `asana_tags`
- Model class: `AsanaTag`
- Primary key: `gid`

### Schemas

These component schemas represent **tags** in the API. Build your
ORM model to cover the union of all fields across these schemas. Fields that
appear in only some schemas should be nullable.

```json
{}
```

### Endpoints

Each entry below is an endpoint that operates on **tags**. Build
one operation function and one route handler per endpoint.

#### DELETE /tags/{tag_gid}
_Delete a tag_
Errors: 400, 401, 403, 404, 500

#### GET /tags
_Get multiple tags_
Parameters:
  - limit (query, optional): integer
  - offset (query, optional): string
  - workspace (query, optional): string
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /tags/{tag_gid}
_Get a tag_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /tasks/{task_gid}/tags
_Get a task's tags_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/tags
_Get tags in a workspace_
Parameters:
  - limit (query, optional): integer
  - offset (query, optional): string
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### POST /tags
_Create a tag_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /workspaces/{workspace_gid}/tags
_Create a tag in a workspace_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### PUT /tags/{tag_gid}
_Update a tag_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500


### Referenced Schemas

These schemas appear in the endpoints above (as response bodies or request
bodies) but are not direct representations of **tags**. They
define the shapes your serializers must produce and your operations must
accept.

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
  "TagCreateTagForWorkspaceRequest": {
    "allOf": [
      {
        "$ref": "#/schemas/TagBase"
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

---

## Implementation Rules

### Files you will edit

1. **`database/schema.py`** — add the ORM model class
2. **`database/operations.py`** — add CRUD functions
3. **`core/serializers.py`** — add serialization functions
4. **`api/routes.py`** — add handler functions and Route entries

### ORM model (`database/schema.py`)

- Add a class `AsanaTag(Base)` with `__tablename__ = "asana_tags"`
- **Primary key**: look at the `gid` field in the bound schemas —
  check its `type`, `format`, and `examples` to determine the correct column
  type. Use `Integer` for integer IDs, `String(50)` for opaque string IDs,
  `String(36)` for UUID-formatted strings, etc.
- One column per field in the schemas above. Use these type mappings:
  - `string` → `String(N)` or `Text` for long content
  - `integer` → `Integer`
  - `boolean` → `Boolean`
  - `object` (nested) → `JSONB`. Use JSONB for nested objects that represent
    settings, metadata, permissions, file maps, or any structure the API
    returns as-is without filtering on individual sub-fields
  - nullable fields → `Mapped[Optional[T]]` with `nullable=True`
- Store timestamps as `String(50)` when the API returns ISO strings
- Add `is_deleted: Mapped[bool]` with `default=False` for soft-delete support
- **Do NOT add any ForeignKey columns or relationship() declarations** — those
  will be added in Pass 2

### CRUD operations (`database/operations.py`)

- Every function takes `Session` as the first argument
- Use `generate_id("tag")` for new IDs
- Use `now_iso()` for timestamp fields
- Use `session.flush()` after mutations — never `session.commit()`
- Filter out `is_deleted` rows in all read queries
- Cursor pagination: fetch `limit + 1` rows, return next cursor from the last row

### Serializers (`core/serializers.py`)

- Return a dict matching the API response shape exactly
- Use the same key names and casing as the original API
- Include a `serialize_tag_list()` for collection endpoints
- For fields that reference other resources (e.g. `owner`, `user`), serialize
  them as the raw column value for now — Pass 2 will refine these

### Route handlers (`api/routes.py`)

- One async handler per endpoint, following the pattern in the file
- Insert Route entries **above** the `/{_unknown_path:path}` catch-all
- Fixed paths before parameterized paths
- Use `_session(request)`, `_principal_user_id(request)`, `_parse_json_body(request)`,
- **Error responses**: Already implemented in `core/errors.py`: `bad_request()`, `unauthorized()`, `forbidden()`, `not_found()`, `handle_exception()`

For error codes not covered above, implement the response inline or add a new constructor to `core/errors.py`.
  `_pagination_params(request)` from the existing request helpers

### Stubs from previous implementations

Previous resource implementations may have created **stub models** for
tags in `database/schema.py`, marked with
`# STUB — expand when implementing this resource`. If you find a stub
for `AsanaTag`, **replace it** with the full implementation.
Do not create a duplicate class — expand the stub in place.

### What NOT to do

- Do not modify `database/base.py`
- Do not remove or modify existing *completed* implementations for other
  resources — but DO expand any stubs that exist for tags
- Do not invent API behavior not present in the endpoint definitions above
- Do not hard-delete records — use soft-delete via `is_deleted`
- Do not add ForeignKey, relationship(), or association tables — Pass 2 handles those

Read the existing files in the target directory before editing. Preserve
all existing code for other resources — add your new models, functions,
and routes alongside what is already there.
