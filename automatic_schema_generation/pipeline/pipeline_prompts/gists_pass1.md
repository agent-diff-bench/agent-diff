# Entity Implementation (Pass 1 — Base): gists

You are implementing the **gists** resource for the GitHub API
replica. Build the base model, CRUD operations, serializers, and route handlers.

**Do NOT add ForeignKey columns, relationship() declarations, or association
tables in this pass.** Those will be added in a separate step. Focus only on
the resource's own columns, operations, and endpoints.

The full OpenAPI spec is available at: `/Users/azh/agent-diff/automatic_schema_generation/apps/github/inputs/openapi.scoped.json`
If any information in this prompt is unclear or seems incorrect, read the
spec directly to resolve ambiguities.

Files to edit (all under `/Users/azh/backend/src/services/github`):
- `database/schema.py`
- `database/operations.py`
- `core/serializers.py`
- `api/routes.py`

---

## Section 1: gists

### Identity

- Table name: `github_gists`
- Model class: `GitHubGist`
- Primary key: `id`

### Schemas

These component schemas represent **gists** in the API. Build your
ORM model to cover the union of all fields across these schemas. Fields that
appear in only some schemas should be nullable.

```json
{
  "base-gist": {
    "title": "Base Gist",
    "description": "Base Gist",
    "type": "object",
    "properties": {
      "url": {
        "type": "string",
        "format": "uri"
      },
      "forks_url": {
        "type": "string",
        "format": "uri"
      },
      "commits_url": {
        "type": "string",
        "format": "uri"
      },
      "id": {
        "type": "string"
      },
      "node_id": {
        "type": "string"
      },
      "git_pull_url": {
        "type": "string",
        "format": "uri"
      },
      "git_push_url": {
        "type": "string",
        "format": "uri"
      },
      "html_url": {
        "type": "string",
        "format": "uri"
      },
      "files": {
        "type": "object",
        "additionalProperties": {
          "type": "object",
          "properties": {
            "filename": {
              "type": "string"
            },
            "type": {
              "type": "string"
            },
            "language": {
              "type": "string"
            },
            "raw_url": {
              "type": "string"
            },
            "size": {
              "type": "integer"
            },
            "encoding": {
              "type": "string",
              "description": "The encoding used for `content`. Currently, `\"utf-8\"` and `\"base64\"` are supported.",
              "default": "utf-8"
            }
          }
        }
      },
      "public": {
        "type": "boolean"
      },
      "created_at": {
        "type": "string",
        "format": "date-time"
      },
      "updated_at": {
        "type": "string",
        "format": "date-time"
      },
      "description": {
        "type": [
          "string",
          "null"
        ]
      },
      "comments": {
        "type": "integer"
      },
      "comments_enabled": {
        "type": "boolean"
      },
      "comments_url": {
        "type": "string",
        "format": "uri"
      },
      "owner": {
        "$ref": "#/schemas/simple-user"
      },
      "truncated": {
        "type": "boolean"
      }
    },
    "required": [
      "id",
      "node_id",
      "url",
      "forks_url",
      "commits_url",
      "git_pull_url",
      "git_push_url",
      "html_url",
      "comments_url",
      "public",
      "description",
      "comments",
      "files",
      "created_at",
      "updated_at"
    ]
  },
  "gist-simple": {
    "title": "Gist Simple",
    "description": "Gist Simple",
    "type": "object",
    "properties": {
      "fork_of": {
        "title": "Gist",
        "description": "Gist",
        "type": [
          "object",
          "null"
        ],
        "properties": {
          "url": {
            "type": "string",
            "format": "uri"
          },
          "forks_url": {
            "type": "string",
            "format": "uri"
          },
          "commits_url": {
            "type": "string",
            "format": "uri"
          },
          "id": {
            "type": "string"
          },
          "node_id": {
            "type": "string"
          },
          "git_pull_url": {
            "type": "string",
            "format": "uri"
          },
          "git_push_url": {
            "type": "string",
            "format": "uri"
          },
          "html_url": {
            "type": "string",
            "format": "uri"
          },
          "files": {
            "type": "object",
            "additionalProperties": {
              "type": "object",
              "properties": {
                "filename": {
                  "type": "string"
                },
                "type": {
                  "type": "string"
                },
                "language": {
                  "type": "string"
                },
                "raw_url": {
                  "type": "string"
                },
                "size": {
                  "type": "integer"
                }
              }
            }
          },
          "public": {
            "type": "boolean"
          },
          "created_at": {
            "type": "string",
            "format": "date-time"
          },
          "updated_at": {
            "type": "string",
            "format": "date-time"
          },
          "description": {
            "type": [
              "string",
              "null"
            ]
          },
          "comments": {
            "type": "integer"
          },
          "comments_enabled": {
            "type": "boolean"
          },
          "user": {
            "anyOf": [
              {
                "type": "null"
              },
              {
                "$ref": "#/schemas/simple-user"
              }
            ]
          },
          "comments_url": {
            "type": "string",
            "format": "uri"
          },
          "owner": {
            "anyOf": [
              {
                "type": "null"
              },
              {
                "$ref": "#/schemas/simple-user"
              }
            ]
          },
          "truncated": {
            "type": "boolean"
          },
          "forks": {
            "type": "array",
            "items": {}
          },
          "history": {
            "type": "array",
            "items": {}
          }
        },
        "required": [
          "id",
          "node_id",
          "url",
          "forks_url",
          "commits_url",
          "git_pull_url",
          "git_push_url",
          "html_url",
          "comments_url",
          "public",
          "description",
          "comments",
          "user",
          "files",
          "created_at",
          "updated_at"
        ]
      },
      "url": {
        "type": "string"
      },
      "forks_url": {
        "type": "string"
      },
      "commits_url": {
        "type": "string"
      },
      "id": {
        "type": "string"
      },
      "node_id": {
        "type": "string"
      },
      "git_pull_url": {
        "type": "string"
      },
      "git_push_url": {
        "type": "string"
      },
      "html_url": {
        "type": "string"
      },
      "files": {
        "type": "object",
        "additionalProperties": {
          "type": [
            "object",
            "null"
          ],
          "properties": {
            "filename": {
              "type": "string"
            },
            "type": {
              "type": "string"
            },
            "language": {
              "type": "string"
            },
            "raw_url": {
              "type": "string"
            },
            "size": {
              "type": "integer"
            },
            "truncated": {
              "type": "boolean"
            },
            "content": {
              "type": "string"
            },
            "encoding": {
              "type": "string",
              "description": "The encoding used for `content`. Currently, `\"utf-8\"` and `\"base64\"` are supported.",
              "default": "utf-8"
            }
          }
        }
      },
      "public": {
        "type": "boolean"
      },
      "created_at": {
        "type": "string"
      },
      "updated_at": {
        "type": "string"
      },
      "description": {
        "type": [
          "string",
          "null"
        ]
      },
      "comments": {
        "type": "integer"
      },
      "comments_enabled": {
        "type": "boolean"
      },
      "user": {
        "type": [
          "string",
          "null"
        ]
      },
      "comments_url": {
        "type": "string"
      },
      "owner": {
        "$ref": "#/schemas/simple-user"
      },
      "truncated": {
        "type": "boolean"
      }
    }
  }
}
```

### Endpoints

Each entry below is an endpoint that operates on **gists**. Build
one operation function and one route handler per endpoint.

#### DELETE /gists/{gist_id}
_Delete a gist_
Parameters:
  - gist_id (path, required): string
Response 204: no content

#### DELETE /gists/{gist_id}/comments/{comment_id}
_Delete a gist comment_
Parameters:
  - gist_id (path, required): string
  - comment_id (path, required): integer
Response 204: no content

#### DELETE /gists/{gist_id}/star
_Unstar a gist_
Parameters:
  - gist_id (path, required): string
Response 204: no content

#### GET /gists
_List gists for the authenticated user_
Parameters:
  - since (query, optional): string
  - per_page (query, optional): integer
  - page (query, optional): integer
Response 200: array of #/schemas/base-gist

#### GET /gists/public
_List public gists_
Parameters:
  - since (query, optional): string
  - per_page (query, optional): integer
  - page (query, optional): integer
Response 200: array of #/schemas/base-gist

#### GET /gists/starred
_List starred gists_
Parameters:
  - since (query, optional): string
  - per_page (query, optional): integer
  - page (query, optional): integer
Response 200: array of #/schemas/base-gist

#### GET /gists/{gist_id}
_Get a gist_
Parameters:
  - gist_id (path, required): string
Response 200: #/schemas/gist-simple

#### GET /gists/{gist_id}/comments
_List gist comments_
Parameters:
  - gist_id (path, required): string
  - per_page (query, optional): integer
  - page (query, optional): integer
Response 200: array of #/schemas/gist-comment

#### GET /gists/{gist_id}/comments/{comment_id}
_Get a gist comment_
Parameters:
  - gist_id (path, required): string
  - comment_id (path, required): integer
Response 200: #/schemas/gist-comment

#### GET /gists/{gist_id}/forks
_List gist forks_
Parameters:
  - gist_id (path, required): string
  - per_page (query, optional): integer
  - page (query, optional): integer
Response 200: array of #/schemas/gist-simple

#### GET /gists/{gist_id}/star
_Check if a gist is starred_
Parameters:
  - gist_id (path, required): string
Response 204: no content

#### GET /gists/{gist_id}/{sha}
_Get a gist revision_
Parameters:
  - gist_id (path, required): string
  - sha (path, required): string
Response 200: #/schemas/gist-simple

#### GET /users/{username}/gists
_List gists for a user_
Parameters:
  - username (path, required): string
  - since (query, optional): string
  - per_page (query, optional): integer
  - page (query, optional): integer
Response 200: array of #/schemas/base-gist

#### PATCH /gists/{gist_id}
_Update a gist_
Parameters:
  - gist_id (path, required): string
Request body (application/json):
  - description: string
  - files: object
Response 200: #/schemas/gist-simple

#### PATCH /gists/{gist_id}/comments/{comment_id}
_Update a gist comment_
Parameters:
  - gist_id (path, required): string
  - comment_id (path, required): integer
Request body (application/json):
  - body: string (required)
Response 200: #/schemas/gist-comment

#### POST /gists
_Create a gist_
Request body (application/json):
  - description: string
  - files: object (required)
  - public: object
Response 201: #/schemas/gist-simple

#### POST /gists/{gist_id}/comments
_Create a gist comment_
Parameters:
  - gist_id (path, required): string
Request body (application/json):
  - body: string (required)
Response 201: #/schemas/gist-comment

#### POST /gists/{gist_id}/forks
_Fork a gist_
Parameters:
  - gist_id (path, required): string
Response 201: #/schemas/base-gist

#### PUT /gists/{gist_id}/star
_Star a gist_
Parameters:
  - gist_id (path, required): string
Response 204: no content


### Referenced Schemas

These schemas appear in the endpoints above (as response bodies or request
bodies) but are not direct representations of **gists**. They
define the shapes your serializers must produce and your operations must
accept.

```json
{
  "gist-comment": {
    "title": "Gist Comment",
    "description": "A comment made to a gist.",
    "type": "object",
    "properties": {
      "id": {
        "type": "integer",
        "examples": [
          1
        ]
      },
      "node_id": {
        "type": "string",
        "examples": [
          "MDExOkdpc3RDb21tZW50MQ=="
        ]
      },
      "url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/gists/a6db0bec360bb87e9418/comments/1"
        ]
      },
      "body": {
        "description": "The comment text.",
        "type": "string",
        "maxLength": 65535,
        "examples": [
          "Body of the attachment"
        ]
      },
      "user": {
        "anyOf": [
          {
            "type": "null"
          },
          {
            "$ref": "#/schemas/simple-user"
          }
        ]
      },
      "created_at": {
        "type": "string",
        "format": "date-time",
        "examples": [
          "2011-04-18T23:23:56Z"
        ]
      },
      "updated_at": {
        "type": "string",
        "format": "date-time",
        "examples": [
          "2011-04-18T23:23:56Z"
        ]
      },
      "author_association": {
        "$ref": "#/schemas/author-association"
      }
    },
    "required": [
      "url",
      "id",
      "node_id",
      "user",
      "body",
      "author_association",
      "created_at",
      "updated_at"
    ]
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

- Add a class `GitHubGist(Base)` with `__tablename__ = "github_gists"`
- **Primary key**: look at the `id` field in the bound schemas —
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
- Use `generate_id("gist")` for new IDs
- Use `now_iso()` for timestamp fields
- Use `session.flush()` after mutations — never `session.commit()`
- Filter out `is_deleted` rows in all read queries
- Cursor pagination: fetch `limit + 1` rows, return next cursor from the last row

### Serializers (`core/serializers.py`)

- Return a dict matching the API response shape exactly
- Use the same key names and casing as the original API
- Include a `serialize_gist_list()` for collection endpoints
- For fields that reference other resources (e.g. `owner`, `user`), serialize
  them as the raw column value for now — Pass 2 will refine these

### Route handlers (`api/routes.py`)

- One async handler per endpoint, following the pattern in the file
- Insert Route entries **above** the `/{_unknown_path:path}` catch-all
- Fixed paths before parameterized paths
- Use `_session(request)`, `_principal_user_id(request)`, `_parse_json_body(request)`,
  `_pagination_params(request)` from the existing request helpers

### What NOT to do

- Do not modify `database/base.py`
- Do not remove or modify existing functions — only add new ones
- Do not invent API behavior not present in the endpoint definitions above
- Do not hard-delete records — use soft-delete via `is_deleted`
- Do not add ForeignKey, relationship(), or association tables — Pass 2 handles those

Read the existing files in the target directory before editing. Preserve
all existing code — add your new models, functions, and routes alongside
what is already there.
