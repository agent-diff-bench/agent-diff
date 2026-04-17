# Entity Implementation (Pass 1 — Base): tasks

You are implementing the **tasks** resource for the Asana API
replica. Build the base model, CRUD operations, serializers, and route handlers.

**Do NOT add ForeignKey columns, relationship() declarations, or association
tables in this pass.** Those will be added in a separate step. Focus only on
the resource's own columns, operations, and endpoints.

The full OpenAPI spec is available at: `/Users/azh/agent-diff/automatic_schema_generation/open_api_schemas/asana_oas.json`
If any information in this prompt is unclear or seems incorrect, read the
spec directly to resolve ambiguities.

Files to edit (all under `/Users/azh/agent-diff/backend/src/services/asana`):
- `database/schema.py`
- `database/operations.py`
- `core/serializers.py`
- `api/routes.py`

---

## Section 1: tasks

### Identity

- Table name: `asana_tasks`
- Model class: `AsanaTask`
- Primary key: `gid`

### Schemas

These component schemas represent **tasks** in the API. Build your
ORM model to cover the union of all fields across these schemas. Fields that
appear in only some schemas should be nullable.

```json
{
  "TaskBase": {
    "allOf": [
      {
        "$ref": "#/schemas/TaskCompact"
      },
      {
        "type": "object",
        "properties": {
          "approval_status": {
            "type": "string",
            "description": "*Conditional* Reflects the approval status of this task. This field is kept in sync with `completed`, meaning `pending` translates to false while `approved`, `rejected`, and `changes_requested` translate to true. If you set completed to true, this field will be set to `approved`.",
            "enum": [
              "pending",
              "approved",
              "rejected",
              "changes_requested"
            ],
            "example": "pending"
          },
          "assignee_status": {
            "description": "*Deprecated* Scheduling status of this task for the user it is assigned to. This field can only be set if the assignee is non-null. Setting this field to \"inbox\" or \"upcoming\" inserts it at the top of the section, while the other options will insert at the bottom.",
            "type": "string",
            "enum": [
              "today",
              "upcoming",
              "later",
              "new",
              "inbox"
            ],
            "example": "upcoming"
          },
          "assigned_by": {
            "allOf": [
              {
                "$ref": "#/schemas/UserCompact"
              },
              {
                "readOnly": true,
                "nullable": true,
                "description": "The user who assigned the task. This field is only returned when requesting it via opt_fields, and will be null if the task has no specific assigner (e.g., tasks created without an explicit assigner)."
              }
            ]
          },
          "completed": {
            "description": "True if the task is currently marked complete, false if not.",
            "type": "boolean",
            "example": false
          },
          "completed_at": {
            "description": "The time at which this task was completed, or null if the task is incomplete.",
            "type": "string",
            "format": "date-time",
            "readOnly": true,
            "nullable": true,
            "example": "2012-02-22T02:06:58.147Z"
          },
          "completed_by": {
            "allOf": [
              {
                "$ref": "#/schemas/UserCompact"
              },
              {
                "readOnly": true,
                "nullable": true
              }
            ]
          },
          "created_at": {
            "description": "The time at which this resource was created.",
            "type": "string",
            "format": "date-time",
            "readOnly": true,
            "example": "2012-02-22T02:06:58.147Z"
          },
          "dependencies": {
            "description": "[Opt In](/docs/inputoutput-options). Array of resources referencing tasks that this task depends on. The objects contain only the gid of the dependency.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/AsanaResource"
            },
            "readOnly": true
          },
          "dependents": {
            "description": "[Opt In](/docs/inputoutput-options). Array of resources referencing tasks that depend on this task. The objects contain only the ID of the dependent.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/AsanaResource"
            },
            "readOnly": true
          },
          "due_at": {
            "description": "The UTC date and time on which this task is due, or null if the task has no due time. This takes an ISO 8601 date string in UTC and should not be used together with `due_on`.",
            "type": "string",
            "format": "date-time",
            "example": "2019-09-15T02:06:58.147Z",
            "nullable": true
          },
          "due_on": {
            "description": "The localized date on which this task is due, or null if the task has no due date. This takes a date with `YYYY-MM-DD` format and should not be used together with `due_at`.",
            "type": "string",
            "format": "date",
            "example": "2019-09-15",
            "nullable": true
          },
          "external": {
            "description": "*OAuth Required*. *Conditional*. This field is returned only if external values are set or included by using [Opt In] (/docs/inputoutput-options).\nThe external field allows you to store app-specific metadata on tasks, including a gid that can be used to retrieve tasks and a data blob that can store app-specific character strings. Note that you will need to authenticate with Oauth to access or modify this data. Once an external gid is set, you can use the notation `external:custom_gid` to reference your object anywhere in the API where you may use the original object gid. See the page on Custom External Data for more details.",
            "type": "object",
            "properties": {
              "gid": {
                "type": "string",
                "example": "1234"
              },
              "data": {
                "type": "string",
                "example": "A blob of information."
              }
            },
            "example": {
              "gid": "my_gid",
              "data": "A blob of information"
            }
          },
          "html_notes": {
            "description": "[Opt In](/docs/inputoutput-options). The notes of the text with formatting as HTML.",
            "type": "string",
            "example": "<body>Mittens <em>really</em> likes the stuff from Humboldt.</body>"
          },
          "hearted": {
            "description": "*Deprecated - please use liked instead* True if the task is hearted by the authorized user, false if not.",
            "type": "boolean",
            "example": true,
            "readOnly": true
          },
          "hearts": {
            "description": "*Deprecated - please use likes instead* Array of likes for users who have hearted this task.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/Like"
            },
            "readOnly": true
          },
          "is_rendered_as_separator": {
            "description": "[Opt In](/docs/inputoutput-options). In some contexts tasks can be rendered as a visual separator; for instance, subtasks can appear similar to [sections](/reference/sections) without being true `section` objects. If a `task` object is rendered this way in any context it will have the property `is_rendered_as_separator` set to `true`. This parameter only applies to regular tasks with `resource_subtype` of `default_task`. Tasks with `resource_subtype` of `milestone`, `approval`, or custom task types will not have this property and cannot be rendered as separators.",
            "type": "boolean",
            "example": false,
            "readOnly": true
          },
          "liked": {
            "description": "True if the task is liked by the authorized user, false if not.",
            "type": "boolean",
            "example": true
          },
          "likes": {
            "description": "Array of likes for users who have liked this task.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/Like"
            },
            "readOnly": true
          },
          "memberships": {
            "description": "<p><strong style={{ color: \"#4573D2\" }}>Full object requires scope: </strong><code>projects:read</code>, <code>project_sections:read</code></p>\n\n*Create-only*. Array of projects this task is associated with and the section it is in. At task creation time, this array can be used to add the task to specific sections. After task creation, these associations can be modified using the `addProject` and `removeProject` endpoints. Note that over time, more types of memberships may be added to this property.",
            "type": "array",
            "readOnly": true,
            "items": {
              "type": "object",
              "properties": {
                "project": {
                  "$ref": "#/schemas/ProjectCompact"
                },
                "section": {
                  "$ref": "#/schemas/SectionCompact"
                }
              }
            }
          },
          "modified_at": {
            "description": "The time at which this task was last modified.\n\nThe following conditions will change `modified_at`:\n\n- story is created on a task\n- story is trashed on a task\n- attachment is trashed on a task\n- task is assigned or unassigned\n- custom field value is changed\n- the task itself is trashed\n- Or if any of the following fields are updated:\n  - completed\n  - name\n  - due_date\n  - description\n  - attachments\n  - items\n  - schedule_status\n\nThe following conditions will _not_ change `modified_at`:\n\n- moving to a new container (project, portfolio, etc)\n- comments being added to the task (but the stories they generate\n  _will_ affect `modified_at`)",
            "type": "string",
            "format": "date-time",
            "readOnly": true,
            "example": "2012-02-22T02:06:58.147Z"
          },
          "name": {
            "description": "Name of the task. This is generally a short sentence fragment that fits on a line in the UI for maximum readability. However, it can be longer.",
            "type": "string",
            "example": "Buy catnip"
          },
          "notes": {
            "description": "Free-form textual information associated with the task (i.e. its description).",
            "type": "string",
            "example": "Mittens really likes the stuff from Humboldt."
          },
          "num_hearts": {
            "description": "*Deprecated - please use likes instead* The number of users who have hearted this task.",
            "type": "integer",
            "example": 5,
            "readOnly": true
          },
          "num_likes": {
            "description": "The number of users who have liked this task.",
            "type": "integer",
            "example": 5,
            "readOnly": true
          },
          "num_subtasks": {
            "description": "[Opt In](/docs/inputoutput-options). The number of subtasks on this task.\n",
            "type": "integer",
            "example": 3,
            "readOnly": true
          },
          "start_at": {
            "description": "Date and time on which work begins for the task, or null if the task has no start time. This takes an ISO 8601 date string in UTC and should not be used together with `start_on`.\n*Note: `due_at` must be present in the request when setting or unsetting the `start_at` parameter.*",
            "type": "string",
            "nullable": true,
            "format": "date-time",
            "example": "2019-09-14T02:06:58.147Z"
          },
          "start_on": {
            "description": "The day on which work begins for the task , or null if the task has no start date. This takes a date with `YYYY-MM-DD` format and should not be used together with `start_at`.\n*Note: `due_on` or `due_at` must be present in the request when setting or unsetting the `start_on` parameter.*",
            "type": "string",
            "nullable": true,
            "format": "date",
            "example": "2019-09-14"
          },
          "actual_time_minutes": {
            "description": "<p><strong style={{ color: \"#4573D2\" }}>Full object requires scope: </strong><code>time_tracking_entries:read</code></p>\n\nThis value represents the sum of all the Time Tracking entries in the Actual Time field on a given Task. It is represented as a nullable long value.",
            "type": "number",
            "example": 200,
            "readOnly": true,
            "nullable": true
          }
        }
      }
    ]
  },
  "TaskCompact": {
    "description": "<p><strong style={{ color: \"#4573D2\" }}>Full object requires scope: </strong><code>tasks:read</code></p>\n\nThe *task* is the basic object around which many operations in Asana are centered.",
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
        "description": "The name of the task.",
        "type": "string",
        "example": "Bug Task"
      },
      "resource_subtype": {
        "type": "string",
        "description": "The subtype of this resource. Different subtypes retain many of the same fields and behavior, but may render differently in Asana or represent resources with different semantic meaning.\nThe resource_subtype `milestone` represent a single moment in time. This means tasks with this subtype cannot have a start_date.",
        "enum": [
          "default_task",
          "milestone",
          "approval",
          "custom"
        ],
        "example": "default_task"
      },
      "created_by": {
        "type": "object",
        "readOnly": true,
        "description": "[Opt In](/docs/inputoutput-options). A *user* object represents an account in Asana that can be given access to various workspaces, projects, and tasks.",
        "properties": {
          "gid": {
            "description": "Globally unique identifier of the resource.",
            "type": "string",
            "example": "1111"
          },
          "resource_type": {
            "description": "The type of resource.",
            "type": "string",
            "example": "user"
          }
        }
      }
    }
  },
  "TaskRequest": {
    "allOf": [
      {
        "$ref": "#/schemas/TaskBase"
      },
      {
        "type": "object",
        "properties": {
          "assignee": {
            "type": "string",
            "readOnly": false,
            "x-env-variable": true,
            "description": "A string identifying a user. This can either be the string \"me\", an email, or the gid of a user.",
            "example": "12345",
            "nullable": true
          },
          "assignee_section": {
            "nullable": true,
            "type": "string",
            "description": "The *assignee section* is a subdivision of a project that groups tasks together in the assignee's \"My tasks\" list. It can either be a header above a list of tasks in a list view or a column in a board view of \"My tasks.\"\nThe `assignee_section` property will be returned in the response only if the request was sent by the user who is the assignee of the task. Note that you can only write to `assignee_section` with the gid of an existing section visible in the user's \"My tasks\" list.",
            "example": "12345"
          },
          "custom_fields": {
            "description": "An object where each key is the GID of a custom field and its corresponding value is either an enum GID, string, number, object, or array (depending on the custom field type). See the [custom fields guide](/docs/custom-fields-guide) for details on creating and updating custom field values.",
            "type": "object",
            "additionalProperties": {
              "type": "string",
              "description": "\"{custom_field_gid}\" => Value (can be text, a number, etc.). For date, use format \"YYYY-MM-DD\" (e.g., 2019-09-15). For date-time, use ISO 8601 date string in UTC (e.g., 2019-09-15T02:06:58.147Z)."
            },
            "example": {
              "5678904321": "On Hold",
              "4578152156": "Not Started"
            }
          },
          "followers": {
            "type": "array",
            "description": "*Create-Only* An array of strings identifying users. These can either be the string \"me\", an email, or the gid of a user. In order to change followers on an existing task use `addFollowers` and `removeFollowers`.",
            "items": {
              "type": "string",
              "description": "A string identifying a user. This can either be the string \"me\", an email, or the gid of a user."
            },
            "example": [
              "12345"
            ]
          },
          "parent": {
            "type": "string",
            "readOnly": false,
            "x-env-variable": true,
            "description": "Gid of a task.",
            "example": "12345",
            "nullable": true
          },
          "projects": {
            "type": "array",
            "description": "*Create-Only* Array of project gids. In order to change projects on an existing task use `addProject` and `removeProject`.",
            "items": {
              "type": "string",
              "description": "Gid of a project."
            },
            "example": [
              "12345"
            ]
          },
          "tags": {
            "type": "array",
            "description": "*Create-Only* Array of tag gids. In order to change tags on an existing task use `addTag` and `removeTag`.",
            "items": {
              "type": "string",
              "description": "Gid of a tag."
            },
            "example": [
              "12345"
            ]
          },
          "workspace": {
            "type": "string",
            "readOnly": false,
            "x-env-variable": true,
            "description": "Gid of a workspace.",
            "example": "12345"
          },
          "custom_type": {
            "type": "string",
            "readOnly": false,
            "x-env-variable": true,
            "description": "*Conditional:* You can only set custom_type if task `resource_subtype` is `custom`. GID or globally-unique identifier of a task's custom type.",
            "example": "12345",
            "nullable": true
          },
          "custom_type_status_option": {
            "type": "string",
            "readOnly": false,
            "x-env-variable": true,
            "description": "*Conditional:* You can only set custom_type_status_option if task `resource_subtype` is `custom` GID or globally-unique identifier of a custom type's status option.",
            "example": "12345",
            "nullable": true
          }
        }
      }
    ]
  },
  "TaskResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/TaskBase"
      },
      {
        "type": "object",
        "properties": {
          "assignee": {
            "allOf": [
              {
                "$ref": "#/schemas/UserCompact"
              },
              {
                "nullable": true
              }
            ]
          },
          "assignee_section": {
            "allOf": [
              {
                "$ref": "#/schemas/SectionCompact"
              },
              {
                "type": "object",
                "nullable": true,
                "description": "The *assignee section* is a subdivision of a project that groups tasks together in the assignee's \"My tasks\" list. It can either be a header above a list of tasks in a list view or a column in a board view of \"My tasks.\"\nThe `assignee_section` property will be returned in the response only if the request was sent by the user who is the assignee of the task. Note that you can only write to `assignee_section` with the gid of an existing section visible in the user's \"My tasks\" list."
              }
            ]
          },
          "custom_fields": {
            "description": "Array of custom field values applied to the task. These represent the custom field values recorded on this project for a particular custom field. For example, these custom field values will contain an `enum_value` property for custom fields of type `enum`, a `text_value` property for custom fields of type `text`, and so on. Please note that the `gid` returned on each custom field value *is identical* to the `gid` of the custom field, which allows referencing the custom field metadata through the `/custom_fields/custom_field_gid` endpoint.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/CustomFieldResponse"
            },
            "readOnly": true
          },
          "custom_type": {
            "allOf": [
              {
                "$ref": "#/schemas/CustomTypeCompact"
              },
              {
                "nullable": true
              }
            ]
          },
          "custom_type_status_option": {
            "allOf": [
              {
                "$ref": "#/schemas/CustomTypeStatusOptionCompact"
              },
              {
                "nullable": true
              }
            ]
          },
          "followers": {
            "description": "Array of users following this task.",
            "type": "array",
            "readOnly": true,
            "items": {
              "$ref": "#/schemas/UserCompact"
            }
          },
          "parent": {
            "allOf": [
              {
                "$ref": "#/schemas/TaskCompact"
              },
              {
                "type": "object",
                "readOnly": true,
                "description": "The parent of this task, or `null` if this is not a subtask. This property cannot be modified using a PUT request but you can change it with the `setParent` endpoint. You can create subtasks by using the subtasks endpoint.",
                "nullable": true
              }
            ]
          },
          "projects": {
            "description": "*Create-only.* Array of projects this task is associated with. At task creation time, this array can be used to add the task to many projects at once. After task creation, these associations can be modified using the addProject and removeProject endpoints.",
            "type": "array",
            "readOnly": true,
            "items": {
              "$ref": "#/schemas/ProjectCompact"
            }
          },
          "tags": {
            "description": "Array of tags associated with this task. In order to change tags on an existing task use `addTag` and `removeTag`.",
            "type": "array",
            "readOnly": true,
            "items": {
              "$ref": "#/schemas/TagCompact"
            },
            "example": [
              {
                "gid": "59746",
                "name": "Grade A"
              }
            ]
          },
          "workspace": {
            "allOf": [
              {
                "$ref": "#/schemas/WorkspaceCompact"
              },
              {
                "type": "object",
                "readOnly": true,
                "description": "*Create-only*. The workspace this task is associated with. Once created, task cannot be moved to a different workspace. This attribute can only be specified at creation time."
              }
            ]
          },
          "permalink_url": {
            "type": "string",
            "readOnly": true,
            "description": "A url that points directly to the object within Asana.",
            "example": "https://app.asana.com/1/12345/task/123456789"
          }
        }
      }
    ]
  }
}
```

### Endpoints

Each entry below is an endpoint that operates on **tasks**. Build
one operation function and one route handler per endpoint.

#### DELETE /tasks/{task_gid}
_Delete a task_
Errors: 400, 401, 403, 404, 500

#### GET /projects/{project_gid}/tasks
_Get tasks from a project_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /sections/{section_gid}/tasks
_Get tasks from a section_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /tags/{tag_gid}/tasks
_Get tasks from a tag_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /tasks
_Get multiple tasks_
Parameters:
  - limit (query, optional): integer
  - offset (query, optional): string
  - assignee (query, optional): string
  - project (query, optional): string
  - section (query, optional): string
  - workspace (query, optional): string
  - completed_since (query, optional): string
  - modified_since (query, optional): string
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /tasks/{task_gid}
_Get a task_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /tasks/{task_gid}/dependencies
_Get dependencies from a task_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 402, 403, 404, 500

#### GET /tasks/{task_gid}/dependents
_Get dependents from a task_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 402, 403, 404, 500

#### GET /tasks/{task_gid}/subtasks
_Get subtasks from a task_
Parameters:
  - limit (query, optional): integer
  - offset (query, optional): string
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /tasks/{task_gid}/time_tracking_entries
_Get time tracking entries for a task_
Parameters:
  - limit (query, optional): integer
  - offset (query, optional): string
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /user_task_lists/{user_task_list_gid}/tasks
_Get tasks from a user task list_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id}
_Get a task for a given custom ID_
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/tasks/search
_Search tasks in a workspace_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### POST /tasks
_Create a task_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/addDependencies
_Set dependencies for a task_
Request body (application/json):
  - data: object
Errors: 400, 401, 402, 403, 404, 500

#### POST /tasks/{task_gid}/addDependents
_Set dependents for a task_
Request body (application/json):
  - data: object
Errors: 400, 401, 402, 403, 404, 500

#### POST /tasks/{task_gid}/addFollowers
_Add followers to a task_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/addProject
_Add a project to a task_
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/addTag
_Add a tag to a task_
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/duplicate
_Duplicate a task_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/removeDependencies
_Unlink dependencies from a task_
Request body (application/json):
  - data: object
Errors: 400, 401, 402, 403, 404, 500

#### POST /tasks/{task_gid}/removeDependents
_Unlink dependents from a task_
Request body (application/json):
  - data: object
Errors: 400, 401, 402, 403, 404, 500

#### POST /tasks/{task_gid}/removeFollowers
_Remove followers from a task_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/removeProject
_Remove a project from a task_
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/removeTag
_Remove a tag from a task_
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/setParent
_Set the parent of a task_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/subtasks
_Create a subtask_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /tasks/{task_gid}/time_tracking_entries
_Create a time tracking entry_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### PUT /tasks/{task_gid}
_Update a task_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500


### Referenced Schemas

These schemas appear in the endpoints above (as response bodies or request
bodies) but are not direct representations of **tasks**. They
define the shapes your serializers must produce and your operations must
accept.

```json
{
  "CreateTimeTrackingEntryRequest": {
    "type": "object",
    "properties": {
      "duration_minutes": {
        "description": "Time in minutes tracked by the entry. Must be greater than 0",
        "type": "integer",
        "example": 12
      },
      "entered_on": {
        "description": "*Optional*. The day that this entry is logged on. Defaults to today if not specified",
        "type": "string",
        "format": "date",
        "example": "2023-03-19"
      },
      "attributable_to": {
        "type": "string",
        "description": "*Optional*. The gid of the project which the time is attributable to.",
        "example": "987654"
      },
      "billable_status": {
        "description": "*Optional*. The current billable status of the entry.",
        "type": "string",
        "enum": [
          "billable",
          "nonBillable",
          "notApplicable"
        ],
        "example": "billable"
      },
      "description": {
        "description": "*Optional*. The description of the entry.",
        "type": "string",
        "example": "My description of work done on this entry"
      },
      "categories": {
        "description": "*Optional*. The gids of time tracking categories to assign to this time tracking entry. Existing categories will be overridden. Currently limited to a maximum of 1 category.",
        "type": "array",
        "items": {
          "type": "string"
        },
        "example": [
          "12345"
        ]
      }
    }
  },
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
  "GraphExportCompact": {
    "description": "A *graph_export* object represents a request to export the data starting from a parent object",
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
        "example": "graph_export",
        "x-insert-after": "gid"
      },
      "created_at": {
        "description": "The time at which this resource was created.",
        "type": "string",
        "format": "date-time",
        "readOnly": true,
        "example": "2012-02-22T02:06:58.147Z"
      },
      "download_url": {
        "description": "Download this URL to retrieve the full export\nin JSON format. It will be compressed in a gzip (.gz) container.\n\n*Note: May be null if the export is still in progress or\nfailed.  If present, this URL may only be valid for 1 hour from\nthe time of retrieval. You should avoid persisting this URL\nsomewhere and rather refresh on demand to ensure you do not keep\nstale URLs.*",
        "type": "string",
        "format": "uri",
        "readOnly": true,
        "nullable": true,
        "example": "https://asana-export-us-east-1.s3.us-east-1.amazonaws.com/2563645399633793/domain_export/7588024658887731/download/ domain_export_2563645399633793_7588024658887731_2023018-201726.json.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256& X-Amz-Content-Sha256=xxxxxxxx&X-Amz-Date=xxxxxxxx&X-Amz-Expires=300&X-Amz-Security-Token=xxxxxxxx& X-Amz-Signature=xxxxxxxx&X-Amz-SignedHeaders=host&x-id=GetObject#_=_"
      },
      "completed_at": {
        "description": "The time at which this resource was completed.",
        "type": "string",
        "format": "date-time",
        "readOnly": true,
        "example": "2012-02-22T03:06:58.147Z"
      }
    }
  },
  "JobBase": {
    "$ref": "#/schemas/JobCompact"
  },
  "JobCompact": {
    "description": "A *job* is an object representing a process that handles asynchronous work.",
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
        "example": "job",
        "x-insert-after": "gid"
      },
      "resource_subtype": {
        "description": "The subtype of this resource. Different subtypes retain many of the same fields and behavior, but may render differently in Asana or represent resources with different semantic meaning.",
        "type": "string",
        "readOnly": true,
        "example": "duplicate_task"
      },
      "status": {
        "description": "The current status of this job.",
        "type": "string",
        "enum": [
          "not_started",
          "in_progress",
          "succeeded",
          "failed"
        ],
        "readOnly": true,
        "example": "in_progress"
      },
      "new_portfolio": {
        "$ref": "#/schemas/PortfolioCompact"
      },
      "new_project": {
        "$ref": "#/schemas/ProjectCompact"
      },
      "new_task": {
        "allOf": [
          {
            "$ref": "#/schemas/TaskCompact"
          },
          {
            "type": "object",
            "nullable": true
          }
        ]
      },
      "new_project_template": {
        "$ref": "#/schemas/ProjectTemplateCompact"
      },
      "new_graph_export": {
        "$ref": "#/schemas/GraphExportCompact"
      },
      "new_resource_export": {
        "$ref": "#/schemas/ResourceExportCompact"
      }
    }
  },
  "JobResponse": {
    "$ref": "#/schemas/JobBase"
  },
  "ModifyDependenciesRequest": {
    "type": "object",
    "properties": {
      "dependencies": {
        "description": "An array of task gids that a task depends on.",
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    },
    "example": {
      "dependencies": [
        "133713",
        "184253"
      ]
    }
  },
  "ModifyDependentsRequest": {
    "description": "A set of dependent tasks.",
    "type": "object",
    "properties": {
      "dependents": {
        "description": "An array of task gids that are dependents of the given task.",
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    },
    "example": {
      "dependents": [
        "133713",
        "184253"
      ]
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
  "PortfolioCompact": {
    "description": "A *portfolio* gives a high-level overview of the status of multiple initiatives in Asana. Portfolios provide a dashboard overview of the state of multiple projects, including a progress report and the most recent [project status](/reference/project-statuses) update.\nPortfolios have some restrictions on size. Each portfolio has a max of 1500 items and, like projects, a max of 20 custom fields.",
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
        "example": "portfolio",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "The name of the portfolio.",
        "type": "string",
        "example": "Bug Portfolio"
      }
    }
  },
  "ProjectCompact": {
    "description": "A *project* represents a prioritized list of tasks in Asana or a board with columns of tasks represented as cards. It exists in a single workspace or organization and is accessible to a subset of users in that workspace or organization, depending on its permissions.",
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
        "example": "project",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "Name of the project. This is generally a short sentence fragment that fits on a line in the UI for maximum readability. However, it can be longer.",
        "type": "string",
        "example": "Stuff to buy"
      }
    }
  },
  "ProjectTemplateCompact": {
    "description": "A *project template* is an object that allows new projects to be created with a predefined setup, which may include tasks, sections, Rules, etc. It simplifies the process of running a workflow that involves a similar set of work every time.",
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
        "example": "project_template",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "Name of the project template.",
        "type": "string",
        "example": "Packing list"
      }
    }
  },
  "ResourceExportCompact": {
    "description": "A *resource_export* object represents a request to bulk export objects for one or more resources.",
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
        "example": "export_request",
        "x-insert-after": "gid"
      },
      "created_at": {
        "description": "The time at which the resource export object was created.",
        "type": "string",
        "format": "date-time",
        "readOnly": true,
        "example": "2012-02-22T02:06:58.147Z"
      },
      "download_url": {
        "description": "Download this URL to retrieve the full export\nin [JSON Lines](https://jsonlines.org/) format. It will be compressed in a gzip (.gz) container.\n\n*Note: May be null if the export is still in progress or failed.*",
        "type": "string",
        "format": "uri",
        "readOnly": true,
        "nullable": true,
        "example": "https://asana-export-us-east-1.s3.us-east-1.amazonaws.com/2563645399633793/object_export/7588024658887731/download/ object_export_2563645399633793_7588024658887731_2023018-201726.jsonl.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256& X-Amz-Credential=xxxxxxxx&X-Amz-Date=xxxxxxxx&X-Amz-Expires=300&X-Amz-Security-Token=xxxxxxxx& X-Amz-Signature=xxxxxxxx&X-Amz-SignedHeaders=host"
      },
      "completed_at": {
        "description": "The time at which this resource was completed. This will be null if the export is still in progress.",
        "type": "string",
        "format": "date-time",
        "readOnly": true,
        "example": "2012-02-22T03:06:58.147Z"
      }
    }
  },
  "TaskAddFollowersRequest": {
    "type": "object",
    "properties": {
      "followers": {
        "description": "An array of strings identifying users. These can either be the string \"me\", an email, or the gid of a user.",
        "type": "array",
        "items": {
          "type": "string"
        },
        "example": [
          "13579",
          "321654"
        ]
      }
    },
    "required": [
      "followers"
    ]
  },
  "TaskAddProjectRequest": {
    "type": "object",
    "properties": {
      "project": {
        "description": "The project to add the task to.",
        "type": "string",
        "example": "13579"
      },
      "insert_after": {
        "description": "A task in the project to insert the task after, or `null` to insert at the beginning of the list. When used with `section`, `null` will insert at the beginning of the specified section, otherwise the task must be in the specified section.",
        "type": "string",
        "nullable": true,
        "example": "124816"
      },
      "insert_before": {
        "description": "A task in the project to insert the task before, or `null` to insert at the end of the list. When used with `section`, `null` will insert at the end of the specified section, otherwise the task must be in the specified section.",
        "type": "string",
        "nullable": true,
        "example": "432134"
      },
      "section": {
        "description": "A section in the project to insert the task into. The task will be inserted at the bottom of the section unless combined with `insert_before: null` (end of section) or `insert_after: null` (beginning of section). Can also be combined with non-null `insert_before` or `insert_after` to position relative to a task within the section.",
        "type": "string",
        "nullable": true,
        "example": "987654"
      }
    },
    "required": [
      "project"
    ]
  },
  "TaskAddTagRequest": {
    "type": "object",
    "properties": {
      "tag": {
        "description": "The tag's gid to add to the task.",
        "type": "string",
        "example": "13579"
      }
    },
    "required": [
      "tag"
    ]
  },
  "TaskDuplicateRequest": {
    "type": "object",
    "properties": {
      "name": {
        "description": "The name of the new task.",
        "type": "string",
        "example": "New Task Name"
      },
      "include": {
        "description": "A comma-separated list of fields that will be duplicated to the new task.\n##### Fields\n- assignee\n- attachments\n- dates\n- dependencies\n- followers\n- notes\n- parent\n- projects\n- subtasks\n- tags",
        "type": "string",
        "pattern": "([notes|assignee|subtasks|attachments|tags|followers|projects|dates|dependencies|parent])(,\\1)*",
        "example": [
          "notes,assignee,subtasks,attachments,tags,followers,projects,dates,dependencies,parent"
        ]
      }
    }
  },
  "TaskRemoveFollowersRequest": {
    "type": "object",
    "properties": {
      "followers": {
        "description": "An array of strings identifying users. These can either be the string \"me\", an email, or the gid of a user.",
        "type": "array",
        "items": {
          "type": "string"
        },
        "example": [
          "13579",
          "321654"
        ]
      }
    },
    "required": [
      "followers"
    ]
  },
  "TaskRemoveProjectRequest": {
    "type": "object",
    "properties": {
      "project": {
        "description": "The project to remove the task from.",
        "type": "string",
        "example": "13579"
      }
    },
    "required": [
      "project"
    ]
  },
  "TaskRemoveTagRequest": {
    "type": "object",
    "properties": {
      "tag": {
        "description": "The tag's gid to remove from the task.",
        "type": "string",
        "example": "13579"
      }
    },
    "required": [
      "tag"
    ]
  },
  "TaskSetParentRequest": {
    "type": "object",
    "properties": {
      "parent": {
        "description": "The new parent of the task, or `null` for no parent.",
        "type": "string",
        "example": "987654"
      },
      "insert_after": {
        "description": "A subtask of the parent to insert the task after, or `null` to insert at the beginning of the list.",
        "type": "string",
        "example": "null"
      },
      "insert_before": {
        "description": "A subtask of the parent to insert the task before, or `null` to insert at the end of the list.",
        "type": "string",
        "example": "124816"
      }
    },
    "required": [
      "parent"
    ]
  },
  "TimeTrackingCategoryCompact": {
    "description": "A *time tracking category* is a label that can be assigned to time tracking entries. Categories are workspace-scoped and allow users to classify logged time (e.g., 'Development', 'Meetings').",
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
        "example": "time_tracking_category",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "The name of the time tracking category.",
        "type": "string",
        "example": "Development"
      },
      "color": {
        "description": "The color associated with this category for display purposes.",
        "type": "string",
        "enum": [
          "none",
          "red",
          "orange",
          "yellow-orange",
          "yellow",
          "yellow-green",
          "green",
          "blue-green",
          "aqua",
          "blue",
          "indigo",
          "purple",
          "magenta",
          "hot-pink",
          "pink",
          "cool-gray"
        ],
        "example": "blue"
      }
    }
  },
  "TimeTrackingEntryBase": {
    "allOf": [
      {
        "$ref": "#/schemas/TimeTrackingEntryCompact"
      },
      {
        "type": "object",
        "properties": {
          "task": {
            "$ref": "#/schemas/TaskCompact",
            "readOnly": true
          },
          "created_at": {
            "description": "The time at which this resource was created.",
            "type": "string",
            "format": "date-time",
            "readOnly": true,
            "example": "2012-02-22T02:06:58.147Z"
          },
          "approval_status": {
            "description": "*Optional*. The current approval status of the entry.",
            "type": "string",
            "readOnly": true,
            "enum": [
              "DRAFT",
              "SUBMITTED",
              "APPROVED",
              "REJECTED"
            ],
            "example": "DRAFT"
          },
          "billable_status": {
            "description": "*Optional*. The current billable status of the entry.",
            "type": "string",
            "readOnly": true,
            "enum": [
              "billable",
              "nonBillable",
              "notApplicable"
            ],
            "example": "billable"
          },
          "description": {
            "description": "*Optional*. The description of the entry.",
            "type": "string",
            "readOnly": true,
            "example": "My description of work done on this entry"
          }
        }
      }
    ]
  },
  "TimeTrackingEntryCompact": {
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
        "example": "time_tracking_entry",
        "x-insert-after": "gid"
      },
      "duration_minutes": {
        "description": "Time in minutes tracked by the entry.",
        "type": "integer",
        "example": 12
      },
      "entered_on": {
        "description": "The day that this entry is logged on.",
        "type": "string",
        "format": "date",
        "example": "2015-03-14"
      },
      "attributable_to": {
        "allOf": [
          {
            "$ref": "#/schemas/ProjectCompact"
          },
          {
            "type": "object",
            "description": "The attributable to project specifies which project's budget a time entry should be counted toward, if the task belongs to more than one project. If it only belongs to one project, it should be that project."
          }
        ]
      },
      "created_by": {
        "$ref": "#/schemas/UserCompact",
        "readOnly": true
      },
      "categories": {
        "description": "The categories linked to this time tracking entry.",
        "type": "array",
        "items": {
          "$ref": "#/schemas/TimeTrackingCategoryCompact"
        },
        "readOnly": true
      }
    }
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

- Add a class `AsanaTask(Base)` with `__tablename__ = "asana_tasks"`
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
- Use `generate_id("task")` for new IDs
- Use `now_iso()` for timestamp fields
- Use `session.flush()` after mutations — never `session.commit()`
- Filter out `is_deleted` rows in all read queries
- Cursor pagination: fetch `limit + 1` rows, return next cursor from the last row

### Serializers (`core/serializers.py`)

- Return a dict matching the API response shape exactly
- Use the same key names and casing as the original API
- Include a `serialize_task_list()` for collection endpoints
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
tasks in `database/schema.py`, marked with
`# STUB — expand when implementing this resource`. If you find a stub
for `AsanaTask`, **replace it** with the full implementation.
Do not create a duplicate class — expand the stub in place.

### What NOT to do

- Do not modify `database/base.py`
- Do not remove or modify existing *completed* implementations for other
  resources — but DO expand any stubs that exist for tasks
- Do not invent API behavior not present in the endpoint definitions above
- Do not hard-delete records — use soft-delete via `is_deleted`
- Do not add ForeignKey, relationship(), or association tables — Pass 2 handles those

Read the existing files in the target directory before editing. Preserve
all existing code for other resources — add your new models, functions,
and routes alongside what is already there.
