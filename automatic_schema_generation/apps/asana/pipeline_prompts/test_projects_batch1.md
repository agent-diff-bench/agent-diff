# Endpoint Verification: Asana — projects (batch 1/4)

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

### POST /projects
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/ProjectRequest"}}}
Responses:
  - 201: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/ProjectResponse"}}} — Successfully retrieved projects.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /projects
Query parameters: workspace: string, team: string, opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/schemas/ProjectCompact"}},"next_page":{"$ref":"#/schemas/NextPage"}}} — Successfully retrieved projects.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /projects/{project_gid}
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/ProjectResponse"}}} — Successfully retrieved the requested project.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### PUT /projects/{project_gid}
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/ProjectUpdateRequest"}}}
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/ProjectResponse"}}} — Successfully updated the project.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### DELETE /projects/{project_gid}
Needs a seeded row before this endpoint can be exercised.
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/EmptyResponse"}}} — Successfully deleted the specified project.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### POST /projects/{project_gid}/duplicate
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/ProjectDuplicateRequest"}}}
Responses:
  - 201: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/JobResponse"}}} — Successfully created the job to handle duplication.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### POST /projects/{project_gid}/addFollowers
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/AddFollowersRequest"}}}
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/ProjectResponse"}}} — Successfully added followers to the project.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.


## Schema definitions referenced above

```json
{
  "AddFollowersRequest": {
    "type": "object",
    "required": [
      "followers"
    ],
    "properties": {
      "followers": {
        "description": "An array of strings identifying users. These can either be the string \"me\", an email, or the gid of a user.",
        "type": "string",
        "example": "521621,621373"
      }
    }
  },
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
  "CustomFieldBase": {
    "allOf": [
      {
        "$ref": "#/schemas/CustomFieldCompact"
      },
      {
        "type": "object",
        "properties": {
          "description": {
            "description": "[Opt In](/docs/inputoutput-options). The description of the custom field.",
            "type": "string",
            "example": "Development team priority"
          },
          "enum_options": {
            "description": "*Conditional*. Only relevant for custom fields of type `enum` or `multi_enum`. This array specifies the possible values which an `enum` custom field can adopt. To modify the enum options, refer to [working with enum options](/reference/createenumoptionforcustomfield).",
            "type": "array",
            "items": {
              "$ref": "#/schemas/EnumOption"
            }
          },
          "precision": {
            "description": "Only relevant for custom fields of type `Number`. This field dictates the number of places after the decimal to round to, i.e. 0 is integer values, 1 rounds to the nearest tenth, and so on. Must be between 0 and 6, inclusive.\nFor percentage format, this may be unintuitive, as a value of 0.25 has a precision of 0, while a value of 0.251 has a precision of 1. This is due to 0.25 being displayed as 25%.\nThe identifier format will always have a precision of 0.",
            "type": "integer",
            "example": 2
          },
          "format": {
            "description": "The format of this custom field.",
            "type": "string",
            "enum": [
              "currency",
              "identifier",
              "percentage",
              "custom",
              "duration",
              "none"
            ],
            "example": "custom"
          },
          "currency_code": {
            "description": "ISO 4217 currency code to format this custom field. This will be null if the `format` is not `currency`.",
            "type": "string",
            "nullable": true,
            "example": "EUR"
          },
          "custom_label": {
            "description": "This is the string that appears next to the custom field value. This will be null if the `format` is not `custom`.",
            "type": "string",
            "nullable": true,
            "example": "gold pieces"
          },
          "custom_label_position": {
            "description": "Only relevant for custom fields with `custom` format. This depicts where to place the custom label. This will be null if the `format` is not `custom`.",
            "type": "string",
            "nullable": true,
            "enum": [
              "prefix",
              "suffix",
              null
            ],
            "example": "suffix"
          },
          "is_global_to_workspace": {
            "description": "This flag describes whether this custom field is available to every container in the workspace. Before project-specific custom fields, this field was always true.",
            "type": "boolean",
            "example": true,
            "readOnly": true
          },
          "has_notifications_enabled": {
            "description": "*Conditional*. This flag describes whether a follower of a task with this field should receive inbox notifications from changes to this field.",
            "type": "boolean",
            "example": true
          },
          "asana_created_field": {
            "description": "*Conditional*. A unique identifier to associate this field with the template source of truth.",
            "type": "string",
            "readOnly": true,
            "nullable": true,
            "enum": [
              "a_v_requirements",
              "account_name",
              "actionable",
              "align_shipping_link",
              "align_status",
              "allotted_time",
              "appointment",
              "approval_stage",
              "approved",
              "article_series",
              "board_committee",
              "browser",
              "campaign_audience",
              "campaign_project_status",
              "campaign_regions",
              "channel_primary",
              "client_topic_type",
              "complete_by",
              "contact",
              "contact_email_address",
              "content_channels",
              "content_channels_needed",
              "content_stage",
              "content_type",
              "contract",
              "contract_status",
              "cost",
              "creation_stage",
              "creative_channel",
              "creative_needed",
              "creative_needs",
              "data_sensitivity",
              "deal_size",
              "delivery_appt",
              "delivery_appt_date",
              "department",
              "department_responsible",
              "design_request_needed",
              "design_request_type",
              "discussion_category",
              "do_this_task",
              "editorial_content_status",
              "editorial_content_tag",
              "editorial_content_type",
              "effort",
              "effort_level",
              "est_completion_date",
              "estimated_time",
              "estimated_value",
              "expected_cost",
              "external_steps_needed",
              "favorite_idea",
              "feedback_type",
              "financial",
              "funding_amount",
              "grant_application_process",
              "hiring_candidate_status",
              "idea_status",
              "ids_link",
              "ids_patient_link",
              "implementation_stage",
              "insurance",
              "interview_area",
              "interview_question_score",
              "itero_scan_link",
              "job_s_applied_to",
              "lab",
              "launch_status",
              "lead_status",
              "localization_language",
              "localization_market_team",
              "localization_status",
              "meeting_minutes",
              "meeting_needed",
              "minutes",
              "mrr",
              "must_localize",
              "name_of_foundation",
              "need_to_follow_up",
              "next_appointment",
              "next_steps_sales",
              "num_people",
              "number_of_user_reports",
              "office_location",
              "onboarding_activity",
              "owner",
              "participants_needed",
              "patient_date_of_birth",
              "patient_email",
              "patient_phone",
              "patient_status",
              "phone_number",
              "planning_category",
              "point_of_contact",
              "position",
              "post_format",
              "prescription",
              "priority",
              "priority_level",
              "product",
              "product_stage",
              "progress",
              "project_size",
              "project_status",
              "proposed_budget",
              "publish_status",
              "reason_for_scan",
              "referral",
              "request_type",
              "research_status",
              "responsible_department",
              "responsible_team",
              "risk_assessment_status",
              "room_name",
              "sales_counterpart",
              "sentiment",
              "shipping_link",
              "social_channels",
              "stage",
              "status",
              "status_design",
              "status_of_initiative",
              "system_setup",
              "task_progress",
              "team",
              "team_marketing",
              "team_responsible",
              "time_it_takes_to_complete_tasks",
              "timeframe",
              "treatment_type",
              "type_work_requests_it",
              "use_agency",
              "user_name",
              "vendor_category",
              "vendor_type",
              "word_count",
              null
            ],
            "example": "priority"
          }
        }
      }
    ]
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
  "CustomFieldResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/CustomFieldBase"
      },
      {
        "type": "object",
        "properties": {
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
              "custom_id",
              "reference"
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
          "is_value_read_only": {
            "description": "*Conditional*. This flag describes whether a custom field is read only.",
            "type": "boolean",
            "example": false
          },
          "created_by": {
            "allOf": [
              {
                "$ref": "#/schemas/UserCompact"
              },
              {
                "nullable": true
              }
            ]
          },
          "people_value": {
            "description": "*Conditional*. Only relevant for custom fields of type `people`. This array of [compact user](/reference/users) objects reflects the values of a `people` custom field.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/UserCompact"
            }
          },
          "reference_value": {
            "description": "*Conditional*. Only relevant for custom fields of type `reference`. This array of objects reflects the values of a `reference` custom field.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/AsanaNamedResource"
            }
          },
          "privacy_setting": {
            "description": "The privacy setting of the custom field. *Note: Administrators in your organization may restrict the values of `privacy_setting`.*",
            "type": "string",
            "enum": [
              "public_with_guests",
              "public",
              "private"
            ],
            "example": "public_with_guests"
          },
          "default_access_level": {
            "description": "The default access level when inviting new members to the custom field. This isn't applied when the `privacy_setting` is `private`, or the user is a guest. For local fields in a project or portfolio, the user must additionally have permission to modify the container itself.",
            "type": "string",
            "enum": [
              "admin",
              "editor",
              "user"
            ],
            "example": "user"
          },
          "resource_subtype": {
            "description": "The type of the custom field. Must be one of the given values.\n",
            "type": "string",
            "readOnly": true,
            "example": "text",
            "enum": [
              "text",
              "enum",
              "multi_enum",
              "number",
              "date",
              "people",
              "reference"
            ]
          }
        }
      }
    ]
  },
  "CustomFieldSettingBase": {
    "$ref": "#/schemas/CustomFieldSettingCompact"
  },
  "CustomFieldSettingCompact": {
    "description": "Custom Fields Settings objects represent the many-to-many join of the Custom Field and Project as well as stores information that is relevant to that particular pairing.",
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
        "example": "custom_field_setting",
        "x-insert-after": "gid"
      }
    }
  },
  "CustomFieldSettingResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/CustomFieldSettingBase"
      },
      {
        "type": "object",
        "properties": {
          "project": {
            "allOf": [
              {
                "$ref": "#/schemas/ProjectCompact"
              },
              {
                "type": "object",
                "description": "*Deprecated: new integrations should prefer the `parent` field.* The id of the project that this custom field settings refers to.",
                "readOnly": true
              }
            ]
          },
          "is_important": {
            "description": "`is_important` is used in the Asana web application to determine if this custom field is displayed in the list/grid view of a project or portfolio.",
            "type": "boolean",
            "readOnly": true,
            "example": false
          },
          "parent": {
            "allOf": [
              {
                "$ref": "#/schemas/ProjectCompact"
              },
              {
                "type": "object",
                "description": "The parent to which the custom field is applied. This can be a project or portfolio and indicates that the tasks or projects that the parent contains may be given custom field values for this custom field.",
                "readOnly": true
              }
            ]
          },
          "custom_field": {
            "allOf": [
              {
                "$ref": "#/schemas/CustomFieldResponse"
              },
              {
                "type": "object",
                "description": "The custom field that is applied to the `parent`.",
                "readOnly": true
              }
            ]
          }
        }
      }
    ]
  },
  "EmptyResponse": {
    "type": "object",
    "description": "An empty object. Some endpoints do not return an object on success. The success is conveyed through a 2-- status code and returning an empty object."
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
  "ProjectBase": {
    "allOf": [
      {
        "$ref": "#/schemas/ProjectCompact"
      },
      {
        "type": "object",
        "properties": {
          "archived": {
            "description": "True if the project is archived, false if not. Archived projects do not show in the UI by default and may be treated differently for queries.",
            "type": "boolean",
            "example": false
          },
          "color": {
            "description": "Color of the project.",
            "type": "string",
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
              "none",
              null
            ],
            "example": "light-green"
          },
          "icon": {
            "description": "The icon for a project.",
            "type": "string",
            "nullable": true,
            "enum": [
              "list",
              "board",
              "timeline",
              "calendar",
              "rocket",
              "people",
              "graph",
              "star",
              "bug",
              "light_bulb",
              "globe",
              "gear",
              "notebook",
              "computer",
              "check",
              "target",
              "html",
              "megaphone",
              "chat_bubbles",
              "briefcase",
              "page_layout",
              "mountain_flag",
              "puzzle",
              "presentation",
              "line_and_symbols",
              "speed_dial",
              "ribbon",
              "shoe",
              "shopping_basket",
              "map",
              "ticket",
              "coins"
            ],
            "example": "chat_bubbles"
          },
          "created_at": {
            "description": "The time at which this resource was created.",
            "type": "string",
            "format": "date-time",
            "readOnly": true,
            "example": "2012-02-22T02:06:58.147Z"
          },
          "current_status": {
            "allOf": [
              {
                "$ref": "#/schemas/ProjectStatusResponse"
              },
              {
                "type": "object",
                "nullable": true,
                "description": "*Deprecated: new integrations should prefer the `current_status_update` resource.*"
              }
            ]
          },
          "current_status_update": {
            "allOf": [
              {
                "$ref": "#/schemas/StatusUpdateCompact"
              },
              {
                "type": "object",
                "nullable": true,
                "description": "The latest `status_update` posted to this project."
              }
            ]
          },
          "custom_field_settings": {
            "description": "Array of custom field definitions that are enabled for the project. These represent which custom fields are available to be used on tasks within the project, but do not include any values.",
            "readOnly": true,
            "type": "array",
            "items": {
              "$ref": "#/schemas/CustomFieldSettingResponse"
            }
          },
          "default_view": {
            "description": "The default view (list, board, calendar, or timeline) of a project.",
            "type": "string",
            "enum": [
              "list",
              "board",
              "calendar",
              "timeline"
            ],
            "example": "calendar"
          },
          "due_date": {
            "description": "*Deprecated: new integrations should prefer the `due_on` field.*",
            "type": "string",
            "nullable": true,
            "format": "date",
            "example": "2019-09-15"
          },
          "due_on": {
            "description": "The day on which this project is due. This takes a date with format YYYY-MM-DD.",
            "type": "string",
            "nullable": true,
            "format": "date",
            "example": "2019-09-15"
          },
          "html_notes": {
            "description": "[Opt In](/docs/inputoutput-options). The notes of the project with formatting as HTML.",
            "type": "string",
            "example": "<body>These are things we need to purchase.</body>"
          },
          "members": {
            "description": "Array of users who are members of this project.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/UserCompact"
            },
            "readOnly": true
          },
          "modified_at": {
            "description": "The time at which this project was last modified.\n*Note: This does not currently reflect any changes in associations such as tasks or comments that may have been added or removed from the project.*",
            "type": "string",
            "readOnly": true,
            "format": "date-time",
            "example": "2012-02-22T02:06:58.147Z"
          },
          "notes": {
            "description": "Free-form textual information associated with the project (ie., its description).",
            "type": "string",
            "example": "These are things we need to purchase."
          },
          "public": {
            "description": "*Deprecated:* new integrations use `privacy_setting` instead.",
            "type": "boolean",
            "deprecated": true,
            "example": false
          },
          "privacy_setting": {
            "description": "The privacy setting of the project. *Note: Administrators in your organization may restrict the values of `privacy_setting`.* The value `private_to_team` is deprecated. Use `POST /memberships` to share a project with a team after creation.",
            "type": "string",
            "enum": [
              "public_to_workspace",
              "private_to_team",
              "private"
            ],
            "example": "public_to_workspace"
          },
          "start_on": {
            "description": "The day on which work for this project begins, or null if the project has no start date. This takes a date with `YYYY-MM-DD` format. *Note: `due_on` or `due_at` must be present in the request when setting or unsetting the `start_on` parameter. Additionally, `start_on` and `due_on` cannot be the same date.*",
            "type": "string",
            "nullable": true,
            "format": "date",
            "example": "2019-09-14"
          },
          "default_access_level": {
            "description": "The default access for users or teams who join or are added as members to the project.",
            "type": "string",
            "enum": [
              "admin",
              "editor",
              "commenter",
              "viewer"
            ],
            "example": "admin"
          },
          "minimum_access_level_for_customization": {
            "description": "The minimum access level needed for project members to modify this project's workflow and appearance.",
            "type": "string",
            "enum": [
              "admin",
              "editor"
            ],
            "example": "admin"
          },
          "minimum_access_level_for_sharing": {
            "description": "The minimum access level needed for project members to share the project and manage project memberships.",
            "type": "string",
            "enum": [
              "admin",
              "editor"
            ],
            "example": "admin"
          }
        }
      }
    ]
  },
  "ProjectBriefCompact": {
    "description": "A *Project Brief* allows you to explain the what and why of the project to your team.",
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
        "example": "project_brief",
        "x-insert-after": "gid"
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
  "ProjectDuplicateRequest": {
    "type": "object",
    "required": [
      "name"
    ],
    "properties": {
      "name": {
        "description": "The name of the new project.",
        "type": "string",
        "example": "New Project Name"
      },
      "team": {
        "description": "Sets the team of the new project. If team is not defined, the new project will be in the same team as the the original project.",
        "type": "string",
        "example": "12345"
      },
      "include": {
        "description": "A comma-separated list of elements to include when duplicating a project.\nSome elements are automatically included and cannot be excluded,\nwhile others are **optional** and must be explicitly specified in this field.\n\n**Auto-included fields (non-configurable)**\n- Tasks\n- [Project Views](https://asana.com/features/project-management/project-views)\n(i.e., tabs in a project such as List, Board, Dashboard, etc.)\n- [Rules](https://help.asana.com/s/article/rules)\n\n*Note: The Owner of the Rules copied to the new project is the user who performs the API call.\nIf the duplication is performed using a [Service Account](/docs/authentication#/service-account),\nnote that Service Accounts cannot access the UI to modify or pause Rules.\nTo prevent unwanted automation behavior, consider pausing Rules in the source project before duplication \u2014\ntheir active/paused state is preserved in the new project.*\n\n**Optional fields (configurable)**\n- allocations\n- forms\n- members\n- notes\n- permissions\n- task_assignee\n- task_attachments\n- task_dates\n- task_dependencies\n- task_followers\n- task_notes\n- task_projects\n- task_subtasks\n- task_tags\n- task_templates\n- task_type_default",
        "type": "string",
        "pattern": "([allocations|forms|members|notes|permissions|task_assignee|task_attachments|task_dates|task_dependencies|task_followers|task_notes|task_projects|task_subtasks|task_tags|task_templates|task_type_default])(,\\1)*",
        "example": [
          "allocations,forms,members,notes,permissions,task_assignee,task_attachments,task_dates,task_dependencies,task_followers,task_notes,task_projects,task_subtasks,task_tags,task_templates,task_type_default"
        ]
      },
      "schedule_dates": {
        "description": "A dictionary of options to auto-shift dates. `task_dates` must be included to use this option. Requires `should_skip_weekends` and either `start_on` or `due_on`, but not both.",
        "type": "object",
        "properties": {
          "should_skip_weekends": {
            "description": "**Required**: Determines if the auto-shifted dates should skip weekends.",
            "type": "boolean",
            "example": true
          },
          "due_on": {
            "description": "Sets the last due date in the duplicated project to the given date. The rest of the due dates will be offset by the same amount as the due dates in the original project.",
            "type": "string",
            "example": "2019-05-21"
          },
          "start_on": {
            "description": "Sets the first start date in the duplicated project to the given date. The rest of the start dates will be offset by the same amount as the start dates in the original project.",
            "type": "string",
            "example": "2019-05-21"
          }
        }
      }
    }
  },
  "ProjectRequest": {
    "allOf": [
      {
        "$ref": "#/schemas/ProjectBase"
      },
      {
        "type": "object",
        "properties": {
          "custom_fields": {
            "description": "An object where each key is the GID of a custom field and its corresponding value is either an enum GID, string, number, or object (depending on the custom field type). See the [custom fields guide](/docs/custom-fields-guide) for details on creating and updating custom field values.",
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
            "description": "*Create-only*. Comma separated string of users. Followers are a subset of members who have opted in to receive \"tasks added\" notifications for a project.",
            "type": "string",
            "example": "12345,23456"
          },
          "owner": {
            "description": "The current owner of the project, may be null.",
            "nullable": true,
            "type": "string",
            "example": "12345"
          },
          "team": {
            "description": "*Deprecated:* The team to share this project with is deprecated. Use `POST /memberships` with `{ parent: project, member: team }` to share a project with a team after creation.",
            "deprecated": true,
            "type": "string",
            "example": "12345"
          },
          "workspace": {
            "type": "string",
            "description": "The `gid` of a workspace.",
            "example": "12345"
          }
        }
      }
    ]
  },
  "ProjectResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/ProjectBase"
      },
      {
        "type": "object",
        "properties": {
          "custom_fields": {
            "description": "Array of custom field values applied directly to the project itself. These represent the values set on the project, not the fields available for tasks in the project.",
            "readOnly": true,
            "type": "array",
            "items": {
              "$ref": "#/schemas/CustomFieldCompact"
            }
          },
          "completed": {
            "description": "True if the project is currently marked complete, false if not.",
            "type": "boolean",
            "readOnly": true,
            "example": false
          },
          "completed_at": {
            "description": "The time at which this project was completed, or null if the project is not completed.",
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
                "description": "The user that marked this project complete, or null if the project is not completed.",
                "readOnly": true,
                "nullable": true
              }
            ]
          },
          "followers": {
            "description": "Array of users following this project. Followers are a subset of members who have opted in to receive \"tasks added\" notifications for a project.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/UserCompact"
            },
            "readOnly": true
          },
          "owner": {
            "description": "The current owner of the project, may be null.",
            "allOf": [
              {
                "$ref": "#/schemas/UserCompact"
              },
              {
                "type": "object",
                "nullable": true
              }
            ]
          },
          "team": {
            "allOf": [
              {
                "$ref": "#/schemas/TeamCompact"
              },
              {
                "type": "object",
                "description": "The team that this project is shared with."
              }
            ]
          },
          "permalink_url": {
            "type": "string",
            "readOnly": true,
            "description": "A url that points directly to the object within Asana.",
            "example": "https://app.asana.com/1/12345/project/123456789"
          },
          "project_brief": {
            "allOf": [
              {
                "$ref": "#/schemas/ProjectBriefCompact"
              },
              {
                "type": "object",
                "description": "[Opt In](/docs/inputoutput-options). The project brief associated with this project.",
                "nullable": true
              }
            ]
          },
          "created_from_template": {
            "allOf": [
              {
                "$ref": "#/schemas/ProjectTemplateCompact"
              },
              {
                "type": "object",
                "description": "[Opt In](/docs/inputoutput-options). The project template from which this project was created. If the project was not created from a template, this field will be null.",
                "nullable": true
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
                "description": "*Create-only*. The workspace or organization this project is associated with. Once created, projects cannot be moved to a different workspace. This attribute can only be specified at creation time. If the workspace for your project is an organization, you must also supply a `team` in the request body."
              }
            ]
          }
        }
      }
    ]
  },
  "ProjectStatusBase": {
    "allOf": [
      {
        "$ref": "#/schemas/ProjectStatusCompact"
      },
      {
        "type": "object",
        "properties": {
          "text": {
            "description": "The text content of the status update.",
            "type": "string",
            "example": "The project is moving forward according to plan..."
          },
          "html_text": {
            "description": "[Opt In](/docs/inputoutput-options). The text content of the status update with formatting as HTML.",
            "type": "string",
            "example": "<body>The project <strong>is</strong> moving forward according to plan...</body>"
          },
          "color": {
            "description": "The color associated with the status update.",
            "type": "string",
            "enum": [
              "green",
              "yellow",
              "red",
              "blue",
              "complete"
            ]
          }
        }
      }
    ]
  },
  "ProjectStatusCompact": {
    "description": "*Deprecated: new integrations should prefer the `status_update` resource.*\nA *project status* is an update on the progress of a particular project, and is sent out to all project followers when created. These updates include both text describing the update and a color code intended to represent the overall state of the project: \"green\" for projects that are on track, \"yellow\" for projects at risk, and \"red\" for projects that are behind.",
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
        "example": "project_status",
        "x-insert-after": "gid"
      },
      "title": {
        "description": "The title of the project status update.",
        "type": "string",
        "example": "Status Update - Jun 15"
      }
    }
  },
  "ProjectStatusResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/ProjectStatusBase"
      },
      {
        "type": "object",
        "properties": {
          "author": {
            "$ref": "#/schemas/UserCompact"
          },
          "created_at": {
            "description": "The time at which this resource was created.",
            "type": "string",
            "format": "date-time",
            "readOnly": true,
            "example": "2012-02-22T02:06:58.147Z"
          },
          "created_by": {
            "$ref": "#/schemas/UserCompact"
          },
          "modified_at": {
            "description": "The time at which this project status was last modified.\n*Note: This does not currently reflect any changes in associations such as comments that may have been added or removed from the project status.*",
            "type": "string",
            "format": "date-time",
            "readOnly": true,
            "example": "2012-02-22T02:06:58.147Z"
          }
        }
      }
    ]
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
  "ProjectUpdateRequest": {
    "allOf": [
      {
        "$ref": "#/schemas/ProjectBase"
      },
      {
        "type": "object",
        "properties": {
          "custom_fields": {
            "description": "An object where each key is the GID of a custom field and its corresponding value is either an enum GID, string, number, or object (depending on the custom field type). See the [custom fields guide](/docs/custom-fields-guide) for details on creating and updating custom field values.",
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
            "description": "*Create-only*. Comma separated string of users. Followers are a subset of members who have opted in to receive \"tasks added\" notifications for a project.",
            "type": "string",
            "example": "12345,23456"
          },
          "owner": {
            "description": "The current owner of the project, may be null.",
            "nullable": true,
            "type": "string",
            "example": "12345"
          },
          "team": {
            "description": "*Deprecated:* Updating the team a project is shared with is deprecated. Use `POST /memberships` with `{ parent: project, member: team }` instead to manage team sharing.",
            "deprecated": true,
            "type": "string",
            "example": "12345"
          }
        }
      }
    ]
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
  "StatusUpdateCompact": {
    "description": "A *status update* is an update on the progress of a particular project, portfolio, or goal, and is sent out to all of its parent's followers when created. These updates include both text describing the update and a `status_type` intended to represent the overall state of the object.",
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
        "example": "status_update",
        "x-insert-after": "gid"
      },
      "title": {
        "description": "The title of the status update.",
        "type": "string",
        "example": "Status Update - Jun 15"
      },
      "resource_subtype": {
        "type": "string",
        "description": "The subtype of this resource. Different subtypes retain many of the same fields and behavior, but may render differently in Asana or represent resources with different semantic meaning.\nThe `resource_subtype`s for `status` objects represent the type of their parent.",
        "enum": [
          "project_status_update",
          "portfolio_status_update",
          "goal_status_update"
        ],
        "example": "project_status_update",
        "readOnly": true
      }
    }
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
automatic_schema_generation/apps/asana/pipeline_out/test_results/projects_batch1.json
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
