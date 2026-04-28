# Endpoint Verification: Asana — stories (batch 1/1)

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

### GET /stories/{story_gid}
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/StoryResponse"}}} — Successfully retrieved the specified story.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### PUT /stories/{story_gid}
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/StoryRequest"}}}
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/StoryResponse"}}} — Successfully retrieved the specified story.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### DELETE /stories/{story_gid}
Needs a seeded row before this endpoint can be exercised.
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/EmptyResponse"}}} — Successfully deleted the specified story.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /tasks/{task_gid}/stories
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/schemas/StoryCompact"}},"next_page":{"$ref":"#/schemas/NextPage"}}} — Successfully retrieved the specified task's stories.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### POST /tasks/{task_gid}/stories
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/StoryRequest"}}}
Responses:
  - 201: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/StoryResponse"}}} — Successfully created a new story.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### GET /goals/{goal_gid}/stories
Needs a seeded row before this endpoint can be exercised.
Query parameters: opt_fields: array
Responses:
  - 200: inline: {"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/schemas/StoryCompact"}},"next_page":{"$ref":"#/schemas/NextPage"}}} — Successfully retrieved the specified goal's stories.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.

### POST /goals/{goal_gid}/stories
Query parameters: opt_fields: array
Request body (application/json): inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/StoryRequest"}}}
Responses:
  - 201: inline: {"type":"object","properties":{"data":{"$ref":"#/schemas/StoryResponse"}}} — Successfully created a new story.
  - 400: `#/schemas/ErrorResponse` — This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.
  - 401: `#/schemas/ErrorResponse` — A valid authentication token was not provided with the request, so the API could not associate a user with the request.
  - 403: `#/schemas/ErrorResponse` — The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.
  - 404: `#/schemas/ErrorResponse` — Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.
  - 500: `#/schemas/ErrorResponse` — There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.


## Schema definitions referenced above

```json
{
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
  "Like": {
    "type": "object",
    "description": "An object to represent a user's like.",
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the object, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345"
      },
      "user": {
        "$ref": "#/schemas/UserCompact"
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
  "Preview": {
    "type": "object",
    "description": "A collection of rich text that will be displayed as a preview to another app.\n\nThis is read-only except for a small group of whitelisted apps.",
    "readOnly": true,
    "properties": {
      "fallback": {
        "description": "Some fallback text to display if unable to display the full preview.",
        "type": "string",
        "example": "Greg: Great! I like this idea.\\n\\nhttps//a_company.slack.com/archives/ABCDEFG/12345678"
      },
      "footer": {
        "description": "Text to display in the footer.",
        "type": "string",
        "example": "Mar 17, 2019 1:25 PM"
      },
      "header": {
        "description": "Text to display in the header.",
        "type": "string",
        "example": "Asana for Slack"
      },
      "header_link": {
        "description": "Where the header will link to.",
        "type": "string",
        "example": "https://asana.comn/apps/slack"
      },
      "html_text": {
        "description": "HTML formatted text for the body of the preview.",
        "type": "string",
        "example": "<body>Great! I like this idea.</body>"
      },
      "text": {
        "description": "Text for the body of the preview.",
        "type": "string",
        "example": "Great! I like this idea."
      },
      "title": {
        "description": "Text to display as the title.",
        "type": "string",
        "example": "Greg"
      },
      "title_link": {
        "description": "Where to title will link to.",
        "type": "string",
        "example": "https://asana.slack.com/archives/ABCDEFG/12345678"
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
  "ReactionSummaryItemCompact": {
    "type": "object",
    "description": "A summary of an emoji reaction on an object.",
    "properties": {
      "emoji_base": {
        "description": "The emoji base character used in the reaction.",
        "type": "string",
        "example": "\ud83d\udc4e"
      },
      "variant": {
        "description": "The full emoji string used in the reaction.",
        "type": "string",
        "example": "\ud83d\udc4e\ud83c\udffc"
      },
      "count": {
        "description": "The number of reactions with the emoji variant on the object.",
        "type": "number",
        "example": 1
      },
      "reacted": {
        "description": "Whether the current user has reacted with the emoji variant on the object.",
        "type": "boolean",
        "example": false
      }
    }
  },
  "SectionCompact": {
    "description": "A *section* is a subdivision of a project that groups tasks together. It can either be a header above a list of tasks in a list view or a column in a board view of a project.",
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
        "example": "section",
        "x-insert-after": "gid"
      },
      "name": {
        "description": "The name of the section (i.e. the text displayed as the section header).",
        "type": "string",
        "example": "Next Actions"
      }
    }
  },
  "StoryBase": {
    "description": "A story represents an activity associated with an object in the Asana system.",
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
        "example": "story",
        "x-insert-after": "gid"
      },
      "created_at": {
        "description": "The time at which this resource was created.",
        "type": "string",
        "format": "date-time",
        "readOnly": true,
        "example": "2012-02-22T02:06:58.147Z"
      },
      "resource_subtype": {
        "description": "The subtype of this resource. Different subtypes retain many of the same fields and behavior, but may render differently in Asana or represent resources with different semantic meaning.",
        "type": "string",
        "readOnly": true,
        "example": "comment_added"
      },
      "text": {
        "description": "The plain text of the comment to add. Cannot be used with html_text.",
        "type": "string",
        "example": "This is a comment."
      },
      "html_text": {
        "description": "[Opt In](/docs/inputoutput-options). HTML formatted text for a comment. This will not include the name of the creator.",
        "type": "string",
        "example": "<body>This is a comment.</body>"
      },
      "is_pinned": {
        "description": "*Conditional*. Whether the story should be pinned on the resource.",
        "type": "boolean",
        "example": false
      },
      "sticker_name": {
        "description": "The name of the sticker in this story. `null` if there is no sticker.",
        "type": "string",
        "enum": [
          "green_checkmark",
          "people_dancing",
          "dancing_unicorn",
          "heart",
          "party_popper",
          "people_waving_flags",
          "splashing_narwhal",
          "trophy",
          "yeti_riding_unicorn",
          "celebrating_people",
          "determined_climbers",
          "phoenix_spreading_love"
        ],
        "example": "dancing_unicorn"
      }
    }
  },
  "StoryCompact": {
    "description": "A story represents an activity associated with an object in the Asana system.",
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
        "example": "story",
        "x-insert-after": "gid"
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
      "resource_subtype": {
        "description": "The subtype of this resource. Different subtypes retain many of the same fields and behavior, but may render differently in Asana or represent resources with different semantic meaning.",
        "type": "string",
        "readOnly": true,
        "example": "comment_added"
      },
      "text": {
        "description": "*Create-only*. Human-readable text for the story or comment.\nThis will not include the name of the creator.\n*Note: This is not guaranteed to be stable for a given type of story. For example, text for a reassignment may not always say \u201cassigned to \u2026\u201d as the text for a story can both be edited and change based on the language settings of the user making the request.*\nUse the `resource_subtype` property to discover the action that created the story.",
        "type": "string",
        "example": "marked today"
      }
    }
  },
  "StoryRequest": {
    "$ref": "#/schemas/StoryBase"
  },
  "StoryResponse": {
    "allOf": [
      {
        "$ref": "#/schemas/StoryBase"
      },
      {
        "type": "object",
        "properties": {
          "created_by": {
            "$ref": "#/schemas/UserCompact"
          },
          "type": {
            "type": "string",
            "enum": [
              "comment",
              "system"
            ],
            "readOnly": true,
            "example": "comment"
          },
          "is_editable": {
            "description": "*Conditional*. Whether the text of the story can be edited after creation.",
            "type": "boolean",
            "readOnly": true,
            "example": false
          },
          "is_edited": {
            "description": "*Conditional*. Whether the text of the story has been edited after creation.",
            "type": "boolean",
            "readOnly": true,
            "example": false
          },
          "hearted": {
            "description": "*Deprecated - please use likes instead*\n*Conditional*. True if the story is hearted by the authorized user, false if not.",
            "type": "boolean",
            "readOnly": true,
            "example": false
          },
          "hearts": {
            "description": "*Deprecated - please use likes instead*\n\n*Conditional*. Array of likes for users who have hearted this story.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/Like"
            },
            "readOnly": true
          },
          "num_hearts": {
            "description": "*Deprecated - please use likes instead*\n\n*Conditional*. The number of users who have hearted this story.",
            "type": "integer",
            "readOnly": true,
            "example": 5
          },
          "liked": {
            "description": "*Conditional*. True if the story is liked by the authorized user, false if not.",
            "type": "boolean",
            "readOnly": true,
            "example": false
          },
          "likes": {
            "description": "*Conditional*. Array of likes for users who have liked this story.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/Like"
            },
            "readOnly": true
          },
          "num_likes": {
            "description": "*Conditional*. The number of users who have liked this story.",
            "type": "integer",
            "readOnly": true,
            "example": 5
          },
          "reaction_summary": {
            "description": "Summary of emoji reactions on this story.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/ReactionSummaryItemCompact"
            },
            "readOnly": true
          },
          "previews": {
            "description": "<p><strong style={{ color: \"#4573D2\" }}>Full object requires scope: </strong><code>attachments:read</code></p>\n\n*Conditional*. A collection of previews to be displayed in the story.\n\n*Note: This property only exists for comment stories.*",
            "type": "array",
            "items": {
              "$ref": "#/schemas/Preview"
            },
            "readOnly": true
          },
          "old_name": {
            "description": "*Conditional* The previous name of the task before a name change.",
            "type": "string",
            "example": "This was the old name"
          },
          "new_name": {
            "description": "*Conditional* The updated name of the task after a name change.",
            "type": "string",
            "nullable": true,
            "readOnly": true,
            "example": "This is the new name"
          },
          "old_dates": {
            "$ref": "#/schemas/StoryResponseDates"
          },
          "new_dates": {
            "$ref": "#/schemas/StoryResponseDates"
          },
          "old_resource_subtype": {
            "description": "*Conditional*",
            "type": "string",
            "readOnly": true,
            "example": "default_task"
          },
          "new_resource_subtype": {
            "description": "*Conditional*",
            "type": "string",
            "readOnly": true,
            "example": "milestone"
          },
          "story": {
            "description": "*Conditional*",
            "$ref": "#/schemas/StoryCompact",
            "readOnly": true
          },
          "assignee": {
            "description": "*Conditional*",
            "$ref": "#/schemas/UserCompact",
            "readOnly": true
          },
          "follower": {
            "description": "*Conditional*",
            "$ref": "#/schemas/UserCompact",
            "readOnly": true
          },
          "old_section": {
            "description": "*Conditional*",
            "$ref": "#/schemas/SectionCompact",
            "readOnly": true
          },
          "new_section": {
            "description": "*Conditional*",
            "$ref": "#/schemas/SectionCompact",
            "readOnly": true
          },
          "task": {
            "description": "*Conditional*",
            "$ref": "#/schemas/TaskCompact",
            "readOnly": true
          },
          "project": {
            "description": "*Conditional*",
            "$ref": "#/schemas/ProjectCompact",
            "readOnly": true
          },
          "tag": {
            "description": "*Conditional*",
            "$ref": "#/schemas/TagCompact",
            "readOnly": true
          },
          "custom_field": {
            "description": "*Conditional*",
            "$ref": "#/schemas/CustomFieldCompact",
            "readOnly": true
          },
          "old_text_value": {
            "description": "*Conditional* The previous value of a text-type field before it was updated.",
            "type": "string",
            "readOnly": true,
            "example": "This was the old text"
          },
          "new_text_value": {
            "description": "*Conditional* The new value of a text-type field after it was updated.",
            "type": "string",
            "readOnly": true,
            "example": "This is the new text"
          },
          "old_number_value": {
            "description": "*Conditional* The previous value of a number-type custom field before the update.",
            "type": "integer",
            "nullable": true,
            "readOnly": true,
            "example": 1
          },
          "new_number_value": {
            "description": "*Conditional* The new value of a number-type custom field after the update.",
            "type": "integer",
            "readOnly": true,
            "example": 2
          },
          "old_enum_value": {
            "description": "*Conditional*",
            "$ref": "#/schemas/EnumOption",
            "readOnly": true
          },
          "new_enum_value": {
            "description": "*Conditional*",
            "$ref": "#/schemas/EnumOption",
            "readOnly": true
          },
          "old_date_value": {
            "allOf": [
              {
                "$ref": "#/schemas/StoryResponseDates"
              },
              {
                "description": "*Conditional*. The old value of a date custom field story."
              }
            ],
            "readOnly": true
          },
          "new_date_value": {
            "allOf": [
              {
                "$ref": "#/schemas/StoryResponseDates"
              },
              {
                "description": "*Conditional* The new value of a date custom field story."
              }
            ],
            "readOnly": true
          },
          "old_people_value": {
            "description": "*Conditional*. The old value of a people custom field story.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/UserCompact"
            },
            "readOnly": true
          },
          "new_people_value": {
            "description": "*Conditional*. The new value of a people custom field story.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/UserCompact"
            },
            "readOnly": true
          },
          "old_multi_enum_values": {
            "description": "*Conditional*. The old value of a multi-enum custom field story.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/EnumOption"
            },
            "readOnly": true
          },
          "new_multi_enum_values": {
            "description": "*Conditional*. The new value of a multi-enum custom field story.",
            "type": "array",
            "items": {
              "$ref": "#/schemas/EnumOption"
            },
            "readOnly": true
          },
          "new_approval_status": {
            "description": "*Conditional*. The new value of approval status.",
            "type": "string",
            "readOnly": true,
            "example": "approved"
          },
          "old_approval_status": {
            "description": "*Conditional*. The old value of approval status.",
            "type": "string",
            "readOnly": true,
            "example": "pending"
          },
          "duplicate_of": {
            "description": "*Conditional*",
            "$ref": "#/schemas/TaskCompact",
            "readOnly": true
          },
          "duplicated_from": {
            "description": "*Conditional*",
            "$ref": "#/schemas/TaskCompact",
            "readOnly": true
          },
          "dependency": {
            "description": "*Conditional*",
            "$ref": "#/schemas/TaskCompact",
            "readOnly": true
          },
          "source": {
            "description": "The component of the Asana product the user used to trigger the story.",
            "type": "string",
            "enum": [
              "web",
              "email",
              "mobile",
              "api",
              "unknown"
            ],
            "readOnly": true,
            "example": "web"
          },
          "target": {
            "allOf": [
              {
                "$ref": "#/schemas/TaskCompact"
              },
              {
                "type": "object",
                "readOnly": true,
                "description": "The object this story is associated with. Currently may only be a task."
              }
            ]
          }
        }
      }
    ]
  },
  "StoryResponseDates": {
    "description": "*Conditional*",
    "type": "object",
    "readOnly": true,
    "properties": {
      "start_on": {
        "description": "The day on which work for this goal begins, or null if the goal has no start date. This takes a date with `YYYY-MM-DD` format, and cannot be set unless there is an accompanying due date.",
        "type": "string",
        "format": "date",
        "example": "2019-09-14",
        "nullable": true
      },
      "due_at": {
        "description": "The UTC date and time on which this task is due, or null if the task has no due time. This takes an ISO 8601 date string in UTC and should not be used together with `due_on`.",
        "type": "string",
        "format": "date-time",
        "example": "2019-09-15T02:06:58.158Z",
        "nullable": true
      },
      "due_on": {
        "description": "The localized day on which this goal is due. This takes a date with format `YYYY-MM-DD`.",
        "type": "string",
        "format": "date",
        "example": "2019-09-15"
      }
    }
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
automatic_schema_generation/apps/asana/pipeline_out/test_results/stories_batch1.json
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
