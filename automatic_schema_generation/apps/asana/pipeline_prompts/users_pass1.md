# Entity Implementation (Pass 1 — Base): users

You are implementing the **users** resource for the Asana API
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

## Section 1: users

### Identity

- Table name: `asana_users`
- Model class: `AsanaUser`
- Primary key: `gid`

### Schemas

These component schemas represent **users** in the API. Build your
ORM model to cover the union of all fields across these schemas. Fields that
appear in only some schemas should be nullable.

```json
{}
```

### Endpoints

Each entry below is an endpoint that operates on **users**. Build
one operation function and one route handler per endpoint.

#### GET /teams/{team_gid}/users
_Get users in a team_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /users
_Get multiple users_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /users/{user_gid}
_Get a user_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /users/{user_gid}/favorites
_Get a user's favorites_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /users/{user_gid}/team_memberships
_Get memberships from a user_
Parameters:
  - workspace (query, required): string
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /users/{user_gid}/user_task_list
_Get a user's task list_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /users/{user_gid}/workspace_memberships
_Get workspace memberships for a user_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/users
_Get users in a workspace or organization_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/users/{user_gid}
_Get a user in a workspace or organization_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### PUT /users/{user_gid}
_Update a user_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### PUT /workspaces/{workspace_gid}/users/{user_gid}
_Update a user in a workspace or organization_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500


### Referenced Schemas

These schemas appear in the endpoints above (as response bodies or request
bodies) but are not direct representations of **users**. They
define the shapes your serializers must produce and your operations must
accept.

```json
{
  "AsanaNamedResource": {
    "description": "A generic Asana Resource, containing a globally unique identifier.",
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
        "example": "task",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "The name of the object.",
        "type": "string",
        "example": "Bug Task"
      }
    }
  },
  "CustomFieldCompact": {
    "description": "Custom Fields store the metadata that is used in order to add user-specified information to tasks in Asana. Be sure to reference the [custom fields](/reference/custom-fields) developer documentation for more information about how custom fields relate to various resources in Asana.\n\nUsers in Asana can [lock custom fields](https://asana.com/guide/help/premium/custom-fields#gl-lock-fields), which will make them read-only when accessed by other users. Attempting to edit a locked custom field will return HTTP error code `403 Forbidden`.",
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
        "example": "custom_field",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "The name of the custom field.",
        "type": "string",
        "example": "Status"
      },
      "type": {
        "description": "*Deprecated: new integrations should prefer the resource_subtype field.* The type of the custom field. Must be one of the given values.\n",
        "type": "string",
        "readOnly": true,
        "enum": [
          "text",
          "enum",
          "multi_enum",
          "number",
          "date",
          "people"
        ]
      },
      "enum_options": {
        "description": "*Conditional*. Only relevant for custom fields of type `enum` or `multi_enum`. This array specifies the possible values which an `enum` custom field can adopt. To modify the enum options, refer to [working with enum options](/reference/createenumoptionforcustomfield).",
        "type": "array",
        "items": {
          "$ref": "#/schemas/EnumOption"
        }
      },
      "enabled": {
        "description": "*Conditional*. This field applies only to [custom field values](/docs/custom-fields-guide#/accessing-custom-field-values-on-tasks-or-projects) and is not available for [custom field definitions](/docs/custom-fields-guide#/accessing-custom-field-definitions).\nDetermines if the custom field is enabled or not. For more details, see the [Custom Fields documentation](/docs/custom-fields-guide#/enabled-and-disabled-values).",
        "type": "boolean",
        "readOnly": true,
        "example": true
      },
      "representation_type": {
        "description": "This field tells the type of the custom field.",
        "type": "string",
        "example": "number",
        "readOnly": true,
        "enum": [
          "text",
          "enum",
          "multi_enum",
          "number",
          "date",
          "people",
          "formula",
          "custom_id"
        ]
      },
      "id_prefix": {
        "description": "This field is the unique custom ID string for the custom field.",
        "type": "string",
        "nullable": true,
        "example": "ID"
      },
      "input_restrictions": {
        "description": "*Conditional*. Only relevant for custom fields of type `reference`. This array of strings reflects the allowed types of objects that can be written to a `reference` custom field value.",
        "type": "array",
        "items": {
          "type": "string"
        },
        "example": "task"
      },
      "is_formula_field": {
        "description": "*Conditional*. This flag describes whether a custom field is a formula custom field.",
        "type": "boolean",
        "example": false
      },
      "date_value": {
        "description": "*Conditional*. Only relevant for custom fields of type `date`. This object reflects the chosen date (and optionally, time) value of a `date` custom field. If no date is selected, the value of `date_value` will be `null`.",
        "type": "object",
        "nullable": true,
        "properties": {
          "date": {
            "type": "string",
            "description": "A string representing the date in YYYY-MM-DD format.",
            "example": "2024-08-23"
          },
          "date_time": {
            "type": "string",
            "description": "A string representing the date in ISO 8601 format. If no time value is selected, the value of `date-time` will be `null`.",
            "example": "2024-08-23T22:00:00.000Z"
          }
        }
      },
      "enum_value": {
        "allOf": [
          {
            "$ref": "#/schemas/EnumOption"
          },
          {
            "type": "object",
            "nullable": true,
            "description": "*Conditional*. Only relevant for custom fields of type `enum`. This object is the chosen value of an `enum` custom field."
          }
        ]
      },
      "multi_enum_values": {
        "description": "*Conditional*. Only relevant for custom fields of type `multi_enum`. This object is the chosen values of a `multi_enum` custom field.",
        "type": "array",
        "items": {
          "$ref": "#/schemas/EnumOption"
        }
      },
      "number_value": {
        "description": "*Conditional*. This number is the value of a `number` custom field.",
        "type": "number",
        "nullable": true,
        "example": 5.2
      },
      "text_value": {
        "description": "*Conditional*. This string is the value of a `text` custom field.",
        "type": "string",
        "nullable": true,
        "example": "Some Value"
      },
      "display_value": {
        "description": "A string representation for the value of the custom field. Integrations that don't require the underlying type should use this field to read values. Using this field will future-proof an app against new custom field types.",
        "type": "string",
        "readOnly": true,
        "example": "blue",
        "nullable": true
      }
    }
  },
  "EnumOption": {
    "description": "Enum options are the possible values which an enum custom field can adopt. An enum custom field must contain at least 1 enum option but no more than 500.\n\nYou can add enum options to a custom field by using the `POST /custom_fields/custom_field_gid/enum_options` endpoint.\n\n**It is not possible to remove or delete an enum option**. Instead, enum options can be disabled by updating the `enabled` field to false with the `PUT /enum_options/enum_option_gid` endpoint. Other attributes can be updated similarly.\n\nOn creation of an enum option, `enabled` is always set to `true`, meaning the enum option is a selectable value for the custom field. Setting `enabled=false` is equivalent to \u201ctrashing\u201d the enum option in the Asana web app within the \u201cEdit Fields\u201d dialog. The enum option will no longer be selectable but, if the enum option value was previously set within a task, the task will retain the value.\n\nEnum options are an ordered list and by default new enum options are inserted at the end. Ordering in relation to existing enum options can be specified on creation by using `insert_before` or `insert_after` to reference an existing enum option. Only one of `insert_before` and `insert_after` can be provided when creating a new enum option.\n\nAn enum options list can be reordered with the `POST /custom_fields/custom_field_gid/enum_options/insert` endpoint.",
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
        "example": "enum_option",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "The name of the enum option.",
        "type": "string",
        "example": "Low"
      },
      "enabled": {
        "description": "Whether or not the enum option is a selectable value for the custom field.",
        "type": "boolean",
        "example": true
      },
      "color": {
        "description": "The color of the enum option. Defaults to `none`.",
        "type": "string",
        "example": "blue"
      }
    }
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
  "TeamCompact": {
    "description": "<p><strong style={{ color: \"#4573D2\" }}>Full object requires scope: </strong><code>teams:read</code></p>\n\nA *team* is used to group related projects and people together within an organization. Each project in an organization is associated with a team.",
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
        "example": "team",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "The name of the team.",
        "type": "string",
        "example": "Marketing"
      }
    }
  },
  "TeamMembershipCompact": {
    "description": "This object represents a user's connection to a team.",
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
        "example": "team_membership",
        "x-insert-after": "gid"
      },
      "user": {
        "$ref": "#/schemas/UserCompact"
      },
      "team": {
        "$ref": "#/schemas/TeamCompact"
      },
      "is_guest": {
        "type": "boolean",
        "description": "Describes if the user is a guest in the team.",
        "example": false
      },
      "is_limited_access": {
        "type": "boolean",
        "readOnly": true,
        "description": "Describes if the user has limited access to the team.",
        "example": false
      },
      "is_admin": {
        "type": "boolean",
        "description": "Describes if the user is a team admin.",
        "example": false
      }
    }
  },
  "UserBase": {
    "$ref": "#/schemas/UserCompact"
  },
  "UserBaseResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/UserBase"
      },
      {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "format": "email",
            "readOnly": true,
            "description": "The user's email address.",
            "example": "gsanchez@example.com"
          },
          "photo": {
            "type": "object",
            "nullable": true,
            "properties": {
              "image_21x21": {
                "type": "string",
                "format": "uri",
                "description": "PNG image of the user at 21x21 pixels."
              },
              "image_27x27": {
                "type": "string",
                "format": "uri",
                "description": "PNG image of the user at 27x27 pixels."
              },
              "image_36x36": {
                "type": "string",
                "format": "uri",
                "description": "PNG image of the user at 36x36 pixels."
              },
              "image_60x60": {
                "type": "string",
                "format": "uri",
                "description": "PNG image of the user at 60x60 pixels."
              },
              "image_128x128": {
                "type": "string",
                "format": "uri",
                "description": "PNG image of the user at 128x128 pixels."
              },
              "image_1024x1024": {
                "type": "string",
                "format": "uri",
                "description": "JPEG image of the user at 1024x1024 pixels."
              }
            },
            "readOnly": true,
            "description": "A map of the user's profile photo in various sizes, or null if no photo is set. Sizes provided are 21, 27, 36, 60, 128, and 1024. All images are in PNG format, except for 1024 (which is in JPEG format).",
            "example": {
              "image_21x21": "https://...",
              "image_27x27": "https://...",
              "image_36x36": "https://...",
              "image_60x60": "https://...",
              "image_128x128": "https://...",
              "image_1024x1024": "https://..."
            }
          }
        }
      }
    ]
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
  "UserRequest": {
    "$ref": "#/schemas/UserBase"
  },
  "UserResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/UserBaseResponse"
      },
      {
        "type": "object",
        "properties": {
          "workspaces": {
            "description": "Workspaces and organizations this user may access.\nNote\\: The API will only return workspaces and organizations that also contain the authenticated user.",
            "readOnly": true,
            "type": "array",
            "items": {
              "$ref": "#/schemas/WorkspaceCompact"
            }
          },
          "custom_fields": {
            "description": "Array of Custom Fields.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/CustomFieldCompact"
            }
          }
        }
      }
    ]
  },
  "UserTaskListBase": {
    "$ref": "#/schemas/UserTaskListCompact"
  },
  "UserTaskListCompact": {
    "description": "A user task list represents the tasks assigned to a particular user. It provides API access to a user\u2019s [My tasks](https://asana.com/guide/help/fundamentals/my-tasks) view in Asana.",
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
        "example": "user_task_list",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "The name of the user task list.",
        "type": "string",
        "example": "My tasks in My Workspace"
      },
      "owner": {
        "description": "The owner of the user task list, i.e. the person whose My Tasks is represented by this resource.",
        "readOnly": true,
        "allOf": [
          {
            "$ref": "#/schemas/UserCompact"
          }
        ]
      },
      "workspace": {
        "description": "The workspace in which the user task list is located.",
        "readOnly": true,
        "allOf": [
          {
            "$ref": "#/schemas/WorkspaceCompact"
          }
        ]
      }
    }
  },
  "UserTaskListResponse": {
    "$ref": "#/schemas/UserTaskListBase"
  },
  "UserUpdateRequest": {
    "allOf": [
      {
        "$ref": "#/schemas/UserRequest"
      },
      {
        "type": "object",
        "properties": {
          "custom_fields": {
            "description": "An object where each key is the GID of a custom field and its corresponding value is either an enum GID, string, number, or object (depending on the custom field type). See the [custom fields guide](/docs/custom-fields-guide) for details on creating and updating custom field values.",
            "type": "object",
            "additionalProperties": {
              "type": "string",
              "description": "\"{custom_field_gid}\" => Value (can be text, enum GID, a number, etc.). For date, use format \"YYYY-MM-DD\" (e.g., 2019-09-15). For date-time, use ISO 8601 date string in UTC (e.g., 2019-09-15T02:06:58.147Z)."
            },
            "example": {
              "5678904321": "On Hold",
              "4578152156": "Not Started"
            }
          }
        }
      }
    ]
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
  },
  "WorkspaceMembershipCompact": {
    "description": "This object determines if a user is a member of a workspace.",
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
        "example": "workspace_membership",
        "x-insert-after": "gid"
      },
      "user": {
        "$ref": "#/schemas/UserCompact"
      },
      "workspace": {
        "$ref": "#/schemas/WorkspaceCompact"
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

- Add a class `AsanaUser(Base)` with `__tablename__ = "asana_users"`
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
- Use `generate_id("user")` for new IDs
- Use `now_iso()` for timestamp fields
- Use `session.flush()` after mutations — never `session.commit()`
- Filter out `is_deleted` rows in all read queries
- Cursor pagination: fetch `limit + 1` rows, return next cursor from the last row

### Serializers (`core/serializers.py`)

- Return a dict matching the API response shape exactly
- Use the same key names and casing as the original API
- Include a `serialize_user_list()` for collection endpoints
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
users in `database/schema.py`, marked with
`# STUB — expand when implementing this resource`. If you find a stub
for `AsanaUser`, **replace it** with the full implementation.
Do not create a duplicate class — expand the stub in place.

### What NOT to do

- Do not modify `database/base.py`
- Do not remove or modify existing *completed* implementations for other
  resources — but DO expand any stubs that exist for users
- Do not invent API behavior not present in the endpoint definitions above
- Do not hard-delete records — use soft-delete via `is_deleted`
- Do not add ForeignKey, relationship(), or association tables — Pass 2 handles those

Read the existing files in the target directory before editing. Preserve
all existing code for other resources — add your new models, functions,
and routes alongside what is already there.
