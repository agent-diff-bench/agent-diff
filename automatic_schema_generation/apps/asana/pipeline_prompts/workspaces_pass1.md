# Entity Implementation (Pass 1 — Base): workspaces

You are implementing the **workspaces** resource for the Asana API
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

## Section 1: workspaces

### Identity

- Table name: `asana_workspaces`
- Model class: `AsanaWorkspace`
- Primary key: `gid`

### Schemas

These component schemas represent **workspaces** in the API. Build your
ORM model to cover the union of all fields across these schemas. Fields that
appear in only some schemas should be nullable.

```json
{}
```

### Endpoints

Each entry below is an endpoint that operates on **workspaces**. Build
one operation function and one route handler per endpoint.

#### GET /workspaces
_Get multiple workspaces_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}
_Get a workspace_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/audit_log_events
_Get audit log events_
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/custom_fields
_Get a workspace's custom fields_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/events
_Get workspace events_
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/typeahead
_Get objects via typeahead_
Parameters:
  - opt_fields (query, optional): array
Errors: 400, 401, 403, 404, 500

#### GET /workspaces/{workspace_gid}/workspace_memberships
_Get the workspace memberships for a workspace_
Parameters:
  - opt_fields (query, optional): array

#### POST /workspaces/{workspace_gid}/addUser
_Add a user to a workspace or organization_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### POST /workspaces/{workspace_gid}/removeUser
_Remove a user from a workspace or organization_
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500

#### PUT /workspaces/{workspace_gid}
_Update a workspace_
Parameters:
  - opt_fields (query, optional): array
Request body (application/json):
  - data: object
Errors: 400, 401, 403, 404, 500


### Referenced Schemas

These schemas appear in the endpoints above (as response bodies or request
bodies) but are not direct representations of **workspaces**. They
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
  "AuditLogEvent": {
    "description": "An object representing a single event within an Asana domain.\n\nEvery audit log event is comprised of an `event_type`, `actor`, `resource`, and `context`. Some events will include additional metadata about the event under `details`. See our [currently supported list of events](/docs/audit-log-events#supported-audit-log-events) for more details.",
    "type": "object",
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the `AuditLogEvent`, as a string.",
        "type": "string",
        "example": "12345",
        "x-insert-after": false
      },
      "created_at": {
        "description": "The time the event was created.",
        "type": "string",
        "format": "date-time",
        "example": "2021-01-01T00:00:00.000Z"
      },
      "event_type": {
        "description": "The type of the event.",
        "type": "string",
        "example": "task_deleted"
      },
      "event_category": {
        "description": "The category that this `event_type` belongs to.",
        "type": "string",
        "example": "deletion"
      },
      "actor": {
        "$ref": "#/schemas/AuditLogEventActor"
      },
      "resource": {
        "$ref": "#/schemas/AuditLogEventResource"
      },
      "details": {
        "$ref": "#/schemas/AuditLogEventDetails"
      },
      "context": {
        "$ref": "#/schemas/AuditLogEventContext"
      }
    }
  },
  "AuditLogEventActor": {
    "description": "The entity that triggered the event. Will typically be a user.",
    "type": "object",
    "properties": {
      "actor_type": {
        "description": "The type of actor.\nCan be one of `user`, `asana`, `asana_support`, `anonymous`, or `external_administrator`.",
        "type": "string",
        "enum": [
          "user",
          "asana",
          "asana_support",
          "anonymous",
          "external_administrator"
        ],
        "example": "user"
      },
      "gid": {
        "description": "Globally unique identifier of the actor, if it is a user.",
        "type": "string",
        "example": "1111"
      },
      "name": {
        "description": "The name of the actor, if it is a user.",
        "type": "string",
        "example": "Greg Sanchez"
      },
      "email": {
        "description": "The email of the actor, if it is a user.",
        "type": "string",
        "example": "gregsanchez@example.com"
      }
    }
  },
  "AuditLogEventContext": {
    "description": "The context from which this event originated.",
    "type": "object",
    "properties": {
      "context_type": {
        "description": "The type of context.\nCan be one of `web`, `desktop`, `mobile`, `asana_support`, `asana`, `email`, or `api`.",
        "type": "string",
        "enum": [
          "web",
          "desktop",
          "mobile",
          "asana_support",
          "asana",
          "email",
          "api"
        ],
        "example": "web"
      },
      "api_authentication_method": {
        "description": "The authentication method used in the context of an API request.\nOnly present if the `context_type` is `api`. Can be one of `cookie`, `oauth`, `personal_access_token`, or `service_account`.",
        "type": "string",
        "enum": [
          "cookie",
          "oauth",
          "personal_access_token",
          "service_account"
        ]
      },
      "client_ip_address": {
        "description": "The IP address of the client that initiated the event, if applicable.",
        "type": "string",
        "example": "1.1.1.1"
      },
      "user_agent": {
        "description": "The user agent of the client that initiated the event, if applicable.",
        "type": "string",
        "example": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
      },
      "oauth_app_name": {
        "description": "The name of the OAuth App that initiated the event.\nOnly present if the `api_authentication_method` is `oauth`.",
        "type": "string"
      },
      "rule_name": {
        "description": "The name of the automation rule that initiated the event.",
        "type": "string",
        "example": "When Task is added to this project"
      },
      "on_behalf_of_user_id": {
        "description": "The ID of the user who requested a change via support.",
        "type": "integer",
        "example": 12345
      }
    }
  },
  "AuditLogEventDetails": {
    "description": "Event specific details. The schema will vary depending on the `event_type`.",
    "type": "object",
    "properties": {
      "old_value": {
        "description": "The previous value of the field that was modified in the audited event.",
        "type": "string",
        "nullable": true
      },
      "new_value": {
        "description": "The new value after the modification in the audited event.",
        "type": "string",
        "nullable": true
      },
      "group": {
        "description": "The division or organizational unit where the event occurred. Primarily used to scope role change events (e.g., `user_division_admin_role_changed`), but may appear in other contexts involving group-level changes.",
        "type": "object",
        "additionalProperties": true
      },
      "saml_response": {
        "description": "The response received from the IdP when a user logs in with SAML SSO. Present on `user_login_failed` and `user_login_succeeded` events.",
        "type": "string",
        "nullable": true
      }
    },
    "additionalProperties": true
  },
  "AuditLogEventResource": {
    "description": "The primary object that was affected by this event.",
    "type": "object",
    "properties": {
      "resource_type": {
        "description": "The type of resource.",
        "type": "string",
        "example": "task"
      },
      "resource_subtype": {
        "description": "The subtype of resource. Most resources will not have a subtype.",
        "type": "string",
        "example": "milestone"
      },
      "gid": {
        "description": "Globally unique identifier of the resource.",
        "type": "string",
        "example": "1111"
      },
      "name": {
        "description": "The name of the resource.",
        "type": "string",
        "nullable": true,
        "example": "Example Task"
      },
      "email": {
        "description": "The email of the resource, if applicable.",
        "type": "string"
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
  "EventResponse": {
    "description": "An *event* is an object representing a change to a resource that was\nobserved by an event subscription or delivered asynchronously to\nthe target location of an active webhook.\n\nThe event may be triggered by a different `user` than the\nsubscriber. For example, if user A subscribes to a task and user B\nmodified it, the event's user will be user B. Note: Some events\nare generated by the system, and will have `null` as the user. API\nconsumers should make sure to handle this case.\n\nThe `resource` that triggered the event may be different from the one\nthat the events were requested for or the webhook is subscribed to. For\nexample, a subscription to a project will contain events for tasks\ncontained within the project.\n\n**Note:** pay close attention to the relationship between the fields\n`Event.action` and `Event.change.action`.\n`Event.action` represents the action taken on the resource\nitself, and `Event.change.action` represents how the information\nwithin the resource's fields have been modified.\n\nFor instance, consider these scenarios:\n\n\n* When at task is added to a project, `Event.action` will be\n`added`, `Event.parent` will be an object with the `id` and\n`type` of the project, and there will be no `change` field.\n\n\n* When an assignee is set on the task, `Event.parent` will be\n`null`, `Event.action` will be `changed`,\n`Event.change.action` will be `changed`, and `new_value` will\nbe an object with the user's `id` and `type`.\n\n\n* When a collaborator is added to the task, `Event.parent` will\nbe `null`, `Event.action` will be `changed`,\n`Event.change.action` will be `added`, and `added_value` will be\nan object with the user's `id` and `type`.",
    "type": "object",
    "properties": {
      "user": {
        "allOf": [
          {
            "$ref": "#/schemas/UserCompact"
          },
          {
            "description": "The user who triggered the event."
          }
        ]
      },
      "resource": {
        "allOf": [
          {
            "$ref": "#/schemas/AsanaNamedResource"
          },
          {
            "description": "The resource which has triggered the event by being modified in some way."
          }
        ]
      },
      "type": {
        "description": "*Deprecated: Refer to the resource_type of the resource.* The type of the resource that generated the event.",
        "type": "string",
        "readOnly": true,
        "example": "task"
      },
      "action": {
        "description": "The type of action taken on the **resource** that triggered the event.  This can be one of `changed`, `added`, `removed`, `deleted`, or `undeleted` depending on the nature of the event.",
        "type": "string",
        "readOnly": true,
        "example": "changed"
      },
      "parent": {
        "allOf": [
          {
            "$ref": "#/schemas/AsanaNamedResource"
          },
          {
            "description": "For added/removed events, the parent object that resource was added to or removed from. The parent will be `null` for other event types."
          }
        ]
      },
      "created_at": {
        "description": "The timestamp when the event occurred.",
        "type": "string",
        "format": "date-time",
        "readOnly": true,
        "example": "2012-02-22T02:06:58.147Z"
      },
      "change": {
        "type": "object",
        "description": "Information about the type of change that has occurred. This field is only present when the value of the property `action`, describing the action taken on the **resource**, is `changed`.",
        "readOnly": true,
        "properties": {
          "field": {
            "description": "The name of the field that has changed in the resource.",
            "type": "string",
            "readOnly": true,
            "example": "assignee"
          },
          "action": {
            "description": "The type of action taken on the **field** which has been changed.  This can be one of `changed`, `added`, or `removed` depending on the nature of the change.",
            "type": "string",
            "readOnly": true,
            "example": "changed"
          },
          "new_value": {
            "description": "*Conditional.* This property is only present when the value of the event's `change.action` is `changed` _and_ the `new_value` is an Asana resource. This will be only the `gid` and `resource_type` of the resource when the events come from webhooks; this will be the compact representation (and can have fields expanded with [opt_fields](/docs/inputoutput-options)) when using the [get events](/reference/getevents) endpoint.",
            "example": {
              "gid": "12345",
              "resource_type": "user"
            }
          },
          "added_value": {
            "description": "*Conditional.* This property is only present when the value of the event's `change.action` is `added` _and_ the `added_value` is an Asana resource. This will be only the `gid` and `resource_type` of the resource when the events come from webhooks; this will be the compact representation (and can have fields expanded with [opt_fields](/docs/inputoutput-options)) when using the [get events](/reference/getevents) endpoint.",
            "example": {
              "gid": "12345",
              "resource_type": "user"
            }
          },
          "removed_value": {
            "description": "*Conditional.* This property is only present when the value of the event's `change.action` is `removed` _and_ the `removed_value` is an Asana resource. This will be only the `gid` and `resource_type` of the resource when the events come from webhooks; this will be the compact representation (and can have fields expanded with [opt_fields](/docs/inputoutput-options)) when using the [get events](/reference/getevents) endpoint.",
            "example": {
              "gid": "12345",
              "resource_type": "user"
            }
          }
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
  "WorkspaceAddUserRequest": {
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
  "WorkspaceBase": {
    "$ref": "#/schemas/WorkspaceCompact"
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
  },
  "WorkspaceRemoveUserRequest": {
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
  "WorkspaceRequest": {
    "$ref": "#/schemas/WorkspaceBase"
  },
  "WorkspaceResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/WorkspaceBase"
      },
      {
        "type": "object",
        "properties": {
          "email_domains": {
            "description": "The email domains that are associated with this workspace.",
            "type": "array",
            "items": {
              "type": "string",
              "format": "uri"
            },
            "example": [
              "asana.com"
            ]
          },
          "is_organization": {
            "description": "Whether the workspace is an *organization*.",
            "type": "boolean",
            "example": false
          }
        }
      }
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

- Add a class `AsanaWorkspace(Base)` with `__tablename__ = "asana_workspaces"`
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
- Use `generate_id("workspace")` for new IDs
- Use `now_iso()` for timestamp fields
- Use `session.flush()` after mutations — never `session.commit()`
- Filter out `is_deleted` rows in all read queries
- Cursor pagination: fetch `limit + 1` rows, return next cursor from the last row

### Serializers (`core/serializers.py`)

- Return a dict matching the API response shape exactly
- Use the same key names and casing as the original API
- Include a `serialize_workspace_list()` for collection endpoints
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
workspaces in `database/schema.py`, marked with
`# STUB — expand when implementing this resource`. If you find a stub
for `AsanaWorkspace`, **replace it** with the full implementation.
Do not create a duplicate class — expand the stub in place.

### What NOT to do

- Do not modify `database/base.py`
- Do not remove or modify existing *completed* implementations for other
  resources — but DO expand any stubs that exist for workspaces
- Do not invent API behavior not present in the endpoint definitions above
- Do not hard-delete records — use soft-delete via `is_deleted`
- Do not add ForeignKey, relationship(), or association tables — Pass 2 handles those

Read the existing files in the target directory before editing. Preserve
all existing code for other resources — add your new models, functions,
and routes alongside what is already there.
