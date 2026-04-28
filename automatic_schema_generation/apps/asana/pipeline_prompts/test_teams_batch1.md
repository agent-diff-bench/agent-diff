# Endpoint Verification: Asana — teams (batch 1/2)

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

### POST /teams
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TeamRequest"}}}
Responses:
  - 201: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TeamResponse"}}} — Successfully created a new team.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### POST /teams/{team_gid}/addUser
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TeamAddUserRequest"}}}
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TeamMembershipResponse"}}} — Successfully added user to the team.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### POST /teams/{team_gid}/removeUser
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TeamRemoveUserRequest"}}}
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/EmptyResponse"}}} — Returns an empty data record
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /teams/{team_gid}/team_memberships
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/schemas/TeamMembershipCompact"}},"next_page":{"$ref":"#/schemas/NextPage"}}} — Successfully retrieved the requested team's memberships.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /teams/{team_gid}/custom_field_settings
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/schemas/CustomFieldSettingResponse"}}}} — Successfully retrieved custom field settings objects for a team.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /teams/{team_gid}/project_templates
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/schemas/ProjectTemplateCompact"}},"next_page":{"$ref":"#/schemas/NextPage"}}} — Successfully retrieved the requested team's project templates.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /teams/{team_gid}
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/TeamResponse"}}} — Successfully retrieved the record for a single team.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.


## Schema definitions referenced above

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
  "TeamAddUserRequest": {
    "type": "object",
    "description": "A user identification object for specification with the addUser/removeUser endpoints.",
    "properties": {
      "user": {
        "description": "A string identifying a user. This can either be the string \"me\", an email, or the gid of a user.",
        "type": "string",
        "example": "12345"
      }
    }
  },
  "TeamBase": {
    "$ref": "#/schemas/TeamCompact"
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
  "TeamMembershipBase": {
    "$ref": "#/schemas/TeamMembershipCompact"
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
  "TeamMembershipResponse": {
    "$ref": "#/schemas/TeamMembershipBase"
  },
  "TeamRemoveUserRequest": {
    "type": "object",
    "description": "A user identification object for specification with the addUser/removeUser endpoints.",
    "properties": {
      "user": {
        "description": "A string identifying a user. This can either be the string \"me\", an email, or the gid of a user.",
        "type": "string",
        "example": "12345"
      }
    }
  },
  "TeamRequest": {
    "allOf": [
      {
        "$ref": "#/schemas/TeamBase"
      },
      {
        "type": "object",
        "properties": {
          "description": {
            "description": "The description of the team.\n",
            "type": "string",
            "example": "All developers should be members of this team."
          },
          "html_description": {
            "description": "The description of the team with formatting as HTML.\n",
            "type": "string",
            "example": "<body><em>All</em> developers should be members of this team.</body>"
          },
          "organization": {
            "type": "string",
            "description": "The organization/workspace the team belongs to. This must be the same organization you are in and cannot be changed once set.\n",
            "example": "123456789"
          },
          "visibility": {
            "description": "The visibility of the team to users in the same organization\n",
            "type": "string",
            "enum": [
              "secret",
              "request_to_join",
              "public"
            ]
          },
          "edit_team_name_or_description_access_level": {
            "description": "Controls who can edit team name and description\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "edit_team_visibility_or_trash_team_access_level": {
            "description": "Controls who can edit team visibility and trash teams\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "member_invite_management_access_level": {
            "description": "Controls who can accept or deny member invites for a given team\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "guest_invite_management_access_level": {
            "description": "Controls who can accept or deny guest invites for a given team\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "join_request_management_access_level": {
            "description": "Controls who can accept or deny join team requests for a Membership by Request team. This field can only be updated when the team's `visibility` field is `request_to_join`.\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "team_member_removal_access_level": {
            "description": "Controls who can remove team members\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "team_content_management_access_level": {
            "description": "Controls who can create and share content with the team\n",
            "type": "string",
            "enum": [
              "no_restriction",
              "only_team_admins"
            ]
          },
          "endorsed": {
            "description": "Whether the team has been endorsed\n",
            "type": "boolean",
            "example": false
          }
        }
      }
    ]
  },
  "TeamResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/TeamBase"
      },
      {
        "type": "object",
        "properties": {
          "description": {
            "description": "[Opt In](/docs/inputoutput-options). The description of the team.\n",
            "type": "string",
            "example": "All developers should be members of this team."
          },
          "html_description": {
            "description": "[Opt In](/docs/inputoutput-options). The description of the team with formatting as HTML.\n",
            "type": "string",
            "example": "<body><em>All</em> developers should be members of this team.</body>"
          },
          "organization": {
            "allOf": [
              {
                "$ref": "#/schemas/WorkspaceCompact"
              },
              {
                "type": "object",
                "description": "The organization/workspace the team belongs to.\n"
              }
            ]
          },
          "permalink_url": {
            "type": "string",
            "readOnly": true,
            "description": "A url that points directly to the object within Asana.",
            "example": "https://app.asana.com/0/resource/123456789/list"
          },
          "visibility": {
            "description": "The visibility of the team to users in the same organization\n",
            "type": "string",
            "enum": [
              "secret",
              "request_to_join",
              "public"
            ]
          },
          "edit_team_name_or_description_access_level": {
            "description": "Controls who can edit team name and description\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "edit_team_visibility_or_trash_team_access_level": {
            "description": "Controls who can edit team visibility and trash teams\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "member_invite_management_access_level": {
            "description": "Controls who can accept or deny member invites for a given team\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "guest_invite_management_access_level": {
            "description": "Controls who can accept or deny guest invites for a given team\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "join_request_management_access_level": {
            "description": "Controls who can accept or deny join team requests for a Membership by Request team. This field can only be updated when the team's `visibility` field is `request_to_join`.\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "team_member_removal_access_level": {
            "description": "Controls who can remove team members\n",
            "type": "string",
            "enum": [
              "all_team_members",
              "only_team_admins"
            ]
          },
          "team_content_management_access_level": {
            "description": "Controls who can create and share content with the team\n",
            "type": "string",
            "enum": [
              "no_restriction",
              "only_team_admins"
            ]
          },
          "endorsed": {
            "description": "Whether the team has been endorsed\n",
            "type": "boolean",
            "example": false
          },
          "custom_field_settings": {
            "description": "Array of Custom Field Settings applied to the team.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/CustomFieldSettingResponse"
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
automatic_schema_generation/apps/asana/pipeline_out/test_results/teams_batch1.json
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
