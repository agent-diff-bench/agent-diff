# Entity Implementation: teams

You are implementing the **teams** resource for the Asana API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for teams

```json
{
  "paths": {
    "/teams": {
      "post": {
        "summary": "Create a team",
        "description": "Creates a team within the current workspace.",
        "tags": [
          "Teams"
        ],
        "operationId": "createTeam",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "custom_field_settings",
              "custom_field_settings.custom_field",
              "custom_field_settings.custom_field.asana_created_field",
              "custom_field_settings.custom_field.created_by",
              "custom_field_settings.custom_field.created_by.name",
              "custom_field_settings.custom_field.currency_code",
              "custom_field_settings.custom_field.custom_label",
              "custom_field_settings.custom_field.custom_label_position",
              "custom_field_settings.custom_field.date_value",
              "custom_field_settings.custom_field.date_value.date",
              "custom_field_settings.custom_field.date_value.date_time",
              "custom_field_settings.custom_field.default_access_level",
              "custom_field_settings.custom_field.description",
              "custom_field_settings.custom_field.display_value",
              "custom_field_settings.custom_field.enabled",
              "custom_field_settings.custom_field.enum_options",
              "custom_field_settings.custom_field.enum_options.color",
              "custom_field_settings.custom_field.enum_options.enabled",
              "custom_field_settings.custom_field.enum_options.name",
              "custom_field_settings.custom_field.enum_value",
              "custom_field_settings.custom_field.enum_value.color",
              "custom_field_settings.custom_field.enum_value.enabled",
              "custom_field_settings.custom_field.enum_value.name",
              "custom_field_settings.custom_field.format",
              "custom_field_settings.custom_field.has_notifications_enabled",
              "custom_field_settings.custom_field.id_prefix",
              "custom_field_settings.custom_field.input_restrictions",
              "custom_field_settings.custom_field.is_formula_field",
              "custom_field_settings.custom_field.is_global_to_workspace",
              "custom_field_settings.custom_field.is_value_read_only",
              "custom_field_settings.custom_field.multi_enum_values",
              "custom_field_settings.custom_field.multi_enum_values.color",
              "custom_field_settings.custom_field.multi_enum_values.enabled",
              "custom_field_settings.custom_field.multi_enum_values.name",
              "custom_field_settings.custom_field.name",
              "custom_field_settings.custom_field.number_value",
              "custom_field_settings.custom_field.people_value",
              "custom_field_settings.custom_field.people_value.name",
              "custom_field_settings.custom_field.precision",
              "custom_field_settings.custom_field.privacy_setting",
              "custom_field_settings.custom_field.reference_value",
              "custom_field_settings.custom_field.reference_value.name",
              "custom_field_settings.custom_field.representation_type",
              "custom_field_settings.custom_field.resource_subtype",
              "custom_field_settings.custom_field.text_value",
              "custom_field_settings.custom_field.type",
              "custom_field_settings.is_important",
              "custom_field_settings.parent",
              "custom_field_settings.parent.name",
              "custom_field_settings.project",
              "custom_field_settings.project.name",
              "description",
              "edit_team_name_or_description_access_level",
              "edit_team_visibility_or_trash_team_access_level",
              "endorsed",
              "guest_invite_management_access_level",
              "html_description",
              "join_request_management_access_level",
              "member_invite_management_access_level",
              "name",
              "organization",
              "organization.name",
              "permalink_url",
              "team_content_management_access_level",
              "team_member_removal_access_level",
              "visibility"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "custom_field_settings",
                  "custom_field_settings.custom_field",
                  "custom_field_settings.custom_field.asana_created_field",
                  "custom_field_settings.custom_field.created_by",
                  "custom_field_settings.custom_field.created_by.name",
                  "custom_field_settings.custom_field.currency_code",
                  "custom_field_settings.custom_field.custom_label",
                  "custom_field_settings.custom_field.custom_label_position",
                  "custom_field_settings.custom_field.date_value",
                  "custom_field_settings.custom_field.date_value.date",
                  "custom_field_settings.custom_field.date_value.date_time",
                  "custom_field_settings.custom_field.default_access_level",
                  "custom_field_settings.custom_field.description",
                  "custom_field_settings.custom_field.display_value",
                  "custom_field_settings.custom_field.enabled",
                  "custom_field_settings.custom_field.enum_options",
                  "custom_field_settings.custom_field.enum_options.color",
                  "custom_field_settings.custom_field.enum_options.enabled",
                  "custom_field_settings.custom_field.enum_options.name",
                  "custom_field_settings.custom_field.enum_value",
                  "custom_field_settings.custom_field.enum_value.color",
                  "custom_field_settings.custom_field.enum_value.enabled",
                  "custom_field_settings.custom_field.enum_value.name",
                  "custom_field_settings.custom_field.format",
                  "custom_field_settings.custom_field.has_notifications_enabled",
                  "custom_field_settings.custom_field.id_prefix",
                  "custom_field_settings.custom_field.input_restrictions",
                  "custom_field_settings.custom_field.is_formula_field",
                  "custom_field_settings.custom_field.is_global_to_workspace",
                  "custom_field_settings.custom_field.is_value_read_only",
                  "custom_field_settings.custom_field.multi_enum_values",
                  "custom_field_settings.custom_field.multi_enum_values.color",
                  "custom_field_settings.custom_field.multi_enum_values.enabled",
                  "custom_field_settings.custom_field.multi_enum_values.name",
                  "custom_field_settings.custom_field.name",
                  "custom_field_settings.custom_field.number_value",
                  "custom_field_settings.custom_field.people_value",
                  "custom_field_settings.custom_field.people_value.name",
                  "custom_field_settings.custom_field.precision",
                  "custom_field_settings.custom_field.privacy_setting",
                  "custom_field_settings.custom_field.reference_value",
                  "custom_field_settings.custom_field.reference_value.name",
                  "custom_field_settings.custom_field.representation_type",
                  "custom_field_settings.custom_field.resource_subtype",
                  "custom_field_settings.custom_field.text_value",
                  "custom_field_settings.custom_field.type",
                  "custom_field_settings.is_important",
                  "custom_field_settings.parent",
                  "custom_field_settings.parent.name",
                  "custom_field_settings.project",
                  "custom_field_settings.project.name",
                  "description",
                  "edit_team_name_or_description_access_level",
                  "edit_team_visibility_or_trash_team_access_level",
                  "endorsed",
                  "guest_invite_management_access_level",
                  "html_description",
                  "join_request_management_access_level",
                  "member_invite_management_access_level",
                  "name",
                  "organization",
                  "organization.name",
                  "permalink_url",
                  "team_content_management_access_level",
                  "team_member_removal_access_level",
                  "visibility"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "The team to create.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TeamRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully created a new team.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TeamResponse"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "401": {
            "$ref": "#/components/responses/Unauthorized"
          },
          "403": {
            "$ref": "#/components/responses/Forbidden"
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          },
          "500": {
            "$ref": "#/components/responses/InternalServerError"
          }
        },
        "security": [
          {
            "personalAccessToken": []
          },
          {
            "oauth2": []
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTeam result = client.teams.createTeam()\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet teamsApiInstance = new Asana.TeamsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The team to create.\nlet opts = { \n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,organization,organization.name,permalink_url,team_content_management_access_level,team_member_removal_access_level,visibility\"\n};\nteamsApiInstance.createTeam(body, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.teams.createTeam({field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nteams_api_instance = asana.TeamsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The team to create.\nopts = {\n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,organization,organization.name,permalink_url,team_content_management_access_level,team_member_removal_access_level,visibility\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Create a team\n    api_response = teams_api_instance.create_team(body, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TeamsApi->create_team: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.teams.create_team({'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->teams->createTeam(array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.teams.create_team(field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/teams/{team_gid}": {
      "get": {
        "summary": "Get a team",
        "description": "<b>Required scope: </b><code>teams:read</code>\n\nReturns the full record for a single team.",
        "tags": [
          "Teams"
        ],
        "operationId": "getTeam",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "custom_field_settings",
              "custom_field_settings.custom_field",
              "custom_field_settings.custom_field.asana_created_field",
              "custom_field_settings.custom_field.created_by",
              "custom_field_settings.custom_field.created_by.name",
              "custom_field_settings.custom_field.currency_code",
              "custom_field_settings.custom_field.custom_label",
              "custom_field_settings.custom_field.custom_label_position",
              "custom_field_settings.custom_field.date_value",
              "custom_field_settings.custom_field.date_value.date",
              "custom_field_settings.custom_field.date_value.date_time",
              "custom_field_settings.custom_field.default_access_level",
              "custom_field_settings.custom_field.description",
              "custom_field_settings.custom_field.display_value",
              "custom_field_settings.custom_field.enabled",
              "custom_field_settings.custom_field.enum_options",
              "custom_field_settings.custom_field.enum_options.color",
              "custom_field_settings.custom_field.enum_options.enabled",
              "custom_field_settings.custom_field.enum_options.name",
              "custom_field_settings.custom_field.enum_value",
              "custom_field_settings.custom_field.enum_value.color",
              "custom_field_settings.custom_field.enum_value.enabled",
              "custom_field_settings.custom_field.enum_value.name",
              "custom_field_settings.custom_field.format",
              "custom_field_settings.custom_field.has_notifications_enabled",
              "custom_field_settings.custom_field.id_prefix",
              "custom_field_settings.custom_field.input_restrictions",
              "custom_field_settings.custom_field.is_formula_field",
              "custom_field_settings.custom_field.is_global_to_workspace",
              "custom_field_settings.custom_field.is_value_read_only",
              "custom_field_settings.custom_field.multi_enum_values",
              "custom_field_settings.custom_field.multi_enum_values.color",
              "custom_field_settings.custom_field.multi_enum_values.enabled",
              "custom_field_settings.custom_field.multi_enum_values.name",
              "custom_field_settings.custom_field.name",
              "custom_field_settings.custom_field.number_value",
              "custom_field_settings.custom_field.people_value",
              "custom_field_settings.custom_field.people_value.name",
              "custom_field_settings.custom_field.precision",
              "custom_field_settings.custom_field.privacy_setting",
              "custom_field_settings.custom_field.reference_value",
              "custom_field_settings.custom_field.reference_value.name",
              "custom_field_settings.custom_field.representation_type",
              "custom_field_settings.custom_field.resource_subtype",
              "custom_field_settings.custom_field.text_value",
              "custom_field_settings.custom_field.type",
              "custom_field_settings.is_important",
              "custom_field_settings.parent",
              "custom_field_settings.parent.name",
              "custom_field_settings.project",
              "custom_field_settings.project.name",
              "description",
              "edit_team_name_or_description_access_level",
              "edit_team_visibility_or_trash_team_access_level",
              "endorsed",
              "guest_invite_management_access_level",
              "html_description",
              "join_request_management_access_level",
              "member_invite_management_access_level",
              "name",
              "organization",
              "organization.name",
              "permalink_url",
              "team_content_management_access_level",
              "team_member_removal_access_level",
              "visibility"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "custom_field_settings",
                  "custom_field_settings.custom_field",
                  "custom_field_settings.custom_field.asana_created_field",
                  "custom_field_settings.custom_field.created_by",
                  "custom_field_settings.custom_field.created_by.name",
                  "custom_field_settings.custom_field.currency_code",
                  "custom_field_settings.custom_field.custom_label",
                  "custom_field_settings.custom_field.custom_label_position",
                  "custom_field_settings.custom_field.date_value",
                  "custom_field_settings.custom_field.date_value.date",
                  "custom_field_settings.custom_field.date_value.date_time",
                  "custom_field_settings.custom_field.default_access_level",
                  "custom_field_settings.custom_field.description",
                  "custom_field_settings.custom_field.display_value",
                  "custom_field_settings.custom_field.enabled",
                  "custom_field_settings.custom_field.enum_options",
                  "custom_field_settings.custom_field.enum_options.color",
                  "custom_field_settings.custom_field.enum_options.enabled",
                  "custom_field_settings.custom_field.enum_options.name",
                  "custom_field_settings.custom_field.enum_value",
                  "custom_field_settings.custom_field.enum_value.color",
                  "custom_field_settings.custom_field.enum_value.enabled",
                  "custom_field_settings.custom_field.enum_value.name",
                  "custom_field_settings.custom_field.format",
                  "custom_field_settings.custom_field.has_notifications_enabled",
                  "custom_field_settings.custom_field.id_prefix",
                  "custom_field_settings.custom_field.input_restrictions",
                  "custom_field_settings.custom_field.is_formula_field",
                  "custom_field_settings.custom_field.is_global_to_workspace",
                  "custom_field_settings.custom_field.is_value_read_only",
                  "custom_field_settings.custom_field.multi_enum_values",
                  "custom_field_settings.custom_field.multi_enum_values.color",
                  "custom_field_settings.custom_field.multi_enum_values.enabled",
                  "custom_field_settings.custom_field.multi_enum_values.name",
                  "custom_field_settings.custom_field.name",
                  "custom_field_settings.custom_field.number_value",
                  "custom_field_settings.custom_field.people_value",
                  "custom_field_settings.custom_field.people_value.name",
                  "custom_field_settings.custom_field.precision",
                  "custom_field_settings.custom_field.privacy_setting",
                  "custom_field_settings.custom_field.reference_value",
                  "custom_field_settings.custom_field.reference_value.name",
                  "custom_field_settings.custom_field.representation_type",
                  "custom_field_settings.custom_field.resource_subtype",
                  "custom_field_settings.custom_field.text_value",
                  "custom_field_settings.custom_field.type",
                  "custom_field_settings.is_important",
                  "custom_field_settings.parent",
                  "custom_field_settings.parent.name",
                  "custom_field_settings.project",
                  "custom_field_settings.project.name",
                  "description",
                  "edit_team_name_or_description_access_level",
                  "edit_team_visibility_or_trash_team_access_level",
                  "endorsed",
                  "guest_invite_management_access_level",
                  "html_description",
                  "join_request_management_access_level",
                  "member_invite_management_access_level",
                  "name",
                  "organization",
                  "organization.name",
                  "permalink_url",
                  "team_content_management_access_level",
                  "team_member_removal_access_level",
                  "visibility"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Successfully retrieved the record for a single team.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TeamResponse"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "401": {
            "$ref": "#/components/responses/Unauthorized"
          },
          "403": {
            "$ref": "#/components/responses/Forbidden"
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          },
          "500": {
            "$ref": "#/components/responses/InternalServerError"
          }
        },
        "security": [
          {
            "personalAccessToken": []
          },
          {
            "oauth2": [
              "teams:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTeam result = client.teams.getTeam(teamGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet teamsApiInstance = new Asana.TeamsApi(client);\nlet team_gid = \"159874\"; // String | Globally unique identifier for the team.\nlet opts = { \n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,organization,organization.name,permalink_url,team_content_management_access_level,team_member_removal_access_level,visibility\"\n};\nteamsApiInstance.getTeam(team_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.teams.getTeam(teamGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nteams_api_instance = asana.TeamsApi(api_client)\nteam_gid = \"159874\" # str | Globally unique identifier for the team.\nopts = {\n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,organization,organization.name,permalink_url,team_content_management_access_level,team_member_removal_access_level,visibility\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get a team\n    api_response = teams_api_instance.get_team(team_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TeamsApi->get_team: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.teams.get_team(team_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->teams->getTeam($team_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.teams.get_team(team_gid: 'team_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "put": {
        "summary": "Update a team",
        "description": "Updates a team within the current workspace.",
        "tags": [
          "Teams"
        ],
        "operationId": "updateTeam",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "custom_field_settings",
              "custom_field_settings.custom_field",
              "custom_field_settings.custom_field.asana_created_field",
              "custom_field_settings.custom_field.created_by",
              "custom_field_settings.custom_field.created_by.name",
              "custom_field_settings.custom_field.currency_code",
              "custom_field_settings.custom_field.custom_label",
              "custom_field_settings.custom_field.custom_label_position",
              "custom_field_settings.custom_field.date_value",
              "custom_field_settings.custom_field.date_value.date",
              "custom_field_settings.custom_field.date_value.date_time",
              "custom_field_settings.custom_field.default_access_level",
              "custom_field_settings.custom_field.description",
              "custom_field_settings.custom_field.display_value",
              "custom_field_settings.custom_field.enabled",
              "custom_field_settings.custom_field.enum_options",
              "custom_field_settings.custom_field.enum_options.color",
              "custom_field_settings.custom_field.enum_options.enabled",
              "custom_field_settings.custom_field.enum_options.name",
              "custom_field_settings.custom_field.enum_value",
              "custom_field_settings.custom_field.enum_value.color",
              "custom_field_settings.custom_field.enum_value.enabled",
              "custom_field_settings.custom_field.enum_value.name",
              "custom_field_settings.custom_field.format",
              "custom_field_settings.custom_field.has_notifications_enabled",
              "custom_field_settings.custom_field.id_prefix",
              "custom_field_settings.custom_field.input_restrictions",
              "custom_field_settings.custom_field.is_formula_field",
              "custom_field_settings.custom_field.is_global_to_workspace",
              "custom_field_settings.custom_field.is_value_read_only",
              "custom_field_settings.custom_field.multi_enum_values",
              "custom_field_settings.custom_field.multi_enum_values.color",
              "custom_field_settings.custom_field.multi_enum_values.enabled",
              "custom_field_settings.custom_field.multi_enum_values.name",
              "custom_field_settings.custom_field.name",
              "custom_field_settings.custom_field.number_value",
              "custom_field_settings.custom_field.people_value",
              "custom_field_settings.custom_field.people_value.name",
              "custom_field_settings.custom_field.precision",
              "custom_field_settings.custom_field.privacy_setting",
              "custom_field_settings.custom_field.reference_value",
              "custom_field_settings.custom_field.reference_value.name",
              "custom_field_settings.custom_field.representation_type",
              "custom_field_settings.custom_field.resource_subtype",
              "custom_field_settings.custom_field.text_value",
              "custom_field_settings.custom_field.type",
              "custom_field_settings.is_important",
              "custom_field_settings.parent",
              "custom_field_settings.parent.name",
              "custom_field_settings.project",
              "custom_field_settings.project.name",
              "description",
              "edit_team_name_or_description_access_level",
              "edit_team_visibility_or_trash_team_access_level",
              "endorsed",
              "guest_invite_management_access_level",
              "html_description",
              "join_request_management_access_level",
              "member_invite_management_access_level",
              "name",
              "organization",
              "organization.name",
              "permalink_url",
              "team_content_management_access_level",
              "team_member_removal_access_level",
              "visibility"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "custom_field_settings",
                  "custom_field_settings.custom_field",
                  "custom_field_settings.custom_field.asana_created_field",
                  "custom_field_settings.custom_field.created_by",
                  "custom_field_settings.custom_field.created_by.name",
                  "custom_field_settings.custom_field.currency_code",
                  "custom_field_settings.custom_field.custom_label",
                  "custom_field_settings.custom_field.custom_label_position",
                  "custom_field_settings.custom_field.date_value",
                  "custom_field_settings.custom_field.date_value.date",
                  "custom_field_settings.custom_field.date_value.date_time",
                  "custom_field_settings.custom_field.default_access_level",
                  "custom_field_settings.custom_field.description",
                  "custom_field_settings.custom_field.display_value",
                  "custom_field_settings.custom_field.enabled",
                  "custom_field_settings.custom_field.enum_options",
                  "custom_field_settings.custom_field.enum_options.color",
                  "custom_field_settings.custom_field.enum_options.enabled",
                  "custom_field_settings.custom_field.enum_options.name",
                  "custom_field_settings.custom_field.enum_value",
                  "custom_field_settings.custom_field.enum_value.color",
                  "custom_field_settings.custom_field.enum_value.enabled",
                  "custom_field_settings.custom_field.enum_value.name",
                  "custom_field_settings.custom_field.format",
                  "custom_field_settings.custom_field.has_notifications_enabled",
                  "custom_field_settings.custom_field.id_prefix",
                  "custom_field_settings.custom_field.input_restrictions",
                  "custom_field_settings.custom_field.is_formula_field",
                  "custom_field_settings.custom_field.is_global_to_workspace",
                  "custom_field_settings.custom_field.is_value_read_only",
                  "custom_field_settings.custom_field.multi_enum_values",
                  "custom_field_settings.custom_field.multi_enum_values.color",
                  "custom_field_settings.custom_field.multi_enum_values.enabled",
                  "custom_field_settings.custom_field.multi_enum_values.name",
                  "custom_field_settings.custom_field.name",
                  "custom_field_settings.custom_field.number_value",
                  "custom_field_settings.custom_field.people_value",
                  "custom_field_settings.custom_field.people_value.name",
                  "custom_field_settings.custom_field.precision",
                  "custom_field_settings.custom_field.privacy_setting",
                  "custom_field_settings.custom_field.reference_value",
                  "custom_field_settings.custom_field.reference_value.name",
                  "custom_field_settings.custom_field.representation_type",
                  "custom_field_settings.custom_field.resource_subtype",
                  "custom_field_settings.custom_field.text_value",
                  "custom_field_settings.custom_field.type",
                  "custom_field_settings.is_important",
                  "custom_field_settings.parent",
                  "custom_field_settings.parent.name",
                  "custom_field_settings.project",
                  "custom_field_settings.project.name",
                  "description",
                  "edit_team_name_or_description_access_level",
                  "edit_team_visibility_or_trash_team_access_level",
                  "endorsed",
                  "guest_invite_management_access_level",
                  "html_description",
                  "join_request_management_access_level",
                  "member_invite_management_access_level",
                  "name",
                  "organization",
                  "organization.name",
                  "permalink_url",
                  "team_content_management_access_level",
                  "team_member_removal_access_level",
                  "visibility"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "The team to update.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TeamRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully updated the team.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TeamResponse"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "401": {
            "$ref": "#/components/responses/Unauthorized"
          },
          "403": {
            "$ref": "#/components/responses/Forbidden"
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          },
          "500": {
            "$ref": "#/components/responses/InternalServerError"
          }
        },
        "security": [
          {
            "personalAccessToken": []
          },
          {
            "oauth2": []
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTeam result = client.teams.updateTeam()\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet teamsApiInstance = new Asana.TeamsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The team to update.\nlet team_gid = \"159874\"; // String | Globally unique identifier for the team.\nlet opts = { \n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,organization,organization.name,permalink_url,team_content_management_access_level,team_member_removal_access_level,visibility\"\n};\nteamsApiInstance.updateTeam(body, team_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.teams.updateTeam(teamGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nteams_api_instance = asana.TeamsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The team to update.\nteam_gid = \"159874\" # str | Globally unique identifier for the team.\nopts = {\n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,organization,organization.name,permalink_url,team_content_management_access_level,team_member_removal_access_level,visibility\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Update a team\n    api_response = teams_api_instance.update_team(body, team_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TeamsApi->update_team: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.teams.update_team(team_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->teams->updateTeam(array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.teams.update_team(field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/workspaces/{workspace_gid}/teams": {
      "get": {
        "summary": "Get teams in a workspace",
        "description": "<b>Required scope: </b><code>teams:read</code>\n\nReturns the compact records for all teams in the workspace visible to the authorized user.",
        "tags": [
          "Teams"
        ],
        "operationId": "getTeamsForWorkspace",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "custom_field_settings",
              "custom_field_settings.custom_field",
              "custom_field_settings.custom_field.asana_created_field",
              "custom_field_settings.custom_field.created_by",
              "custom_field_settings.custom_field.created_by.name",
              "custom_field_settings.custom_field.currency_code",
              "custom_field_settings.custom_field.custom_label",
              "custom_field_settings.custom_field.custom_label_position",
              "custom_field_settings.custom_field.date_value",
              "custom_field_settings.custom_field.date_value.date",
              "custom_field_settings.custom_field.date_value.date_time",
              "custom_field_settings.custom_field.default_access_level",
              "custom_field_settings.custom_field.description",
              "custom_field_settings.custom_field.display_value",
              "custom_field_settings.custom_field.enabled",
              "custom_field_settings.custom_field.enum_options",
              "custom_field_settings.custom_field.enum_options.color",
              "custom_field_settings.custom_field.enum_options.enabled",
              "custom_field_settings.custom_field.enum_options.name",
              "custom_field_settings.custom_field.enum_value",
              "custom_field_settings.custom_field.enum_value.color",
              "custom_field_settings.custom_field.enum_value.enabled",
              "custom_field_settings.custom_field.enum_value.name",
              "custom_field_settings.custom_field.format",
              "custom_field_settings.custom_field.has_notifications_enabled",
              "custom_field_settings.custom_field.id_prefix",
              "custom_field_settings.custom_field.input_restrictions",
              "custom_field_settings.custom_field.is_formula_field",
              "custom_field_settings.custom_field.is_global_to_workspace",
              "custom_field_settings.custom_field.is_value_read_only",
              "custom_field_settings.custom_field.multi_enum_values",
              "custom_field_settings.custom_field.multi_enum_values.color",
              "custom_field_settings.custom_field.multi_enum_values.enabled",
              "custom_field_settings.custom_field.multi_enum_values.name",
              "custom_field_settings.custom_field.name",
              "custom_field_settings.custom_field.number_value",
              "custom_field_settings.custom_field.people_value",
              "custom_field_settings.custom_field.people_value.name",
              "custom_field_settings.custom_field.precision",
              "custom_field_settings.custom_field.privacy_setting",
              "custom_field_settings.custom_field.reference_value",
              "custom_field_settings.custom_field.reference_value.name",
              "custom_field_settings.custom_field.representation_type",
              "custom_field_settings.custom_field.resource_subtype",
              "custom_field_settings.custom_field.text_value",
              "custom_field_settings.custom_field.type",
              "custom_field_settings.is_important",
              "custom_field_settings.parent",
              "custom_field_settings.parent.name",
              "custom_field_settings.project",
              "custom_field_settings.project.name",
              "description",
              "edit_team_name_or_description_access_level",
              "edit_team_visibility_or_trash_team_access_level",
              "endorsed",
              "guest_invite_management_access_level",
              "html_description",
              "join_request_management_access_level",
              "member_invite_management_access_level",
              "name",
              "offset",
              "organization",
              "organization.name",
              "path",
              "permalink_url",
              "team_content_management_access_level",
              "team_member_removal_access_level",
              "uri",
              "visibility"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "custom_field_settings",
                  "custom_field_settings.custom_field",
                  "custom_field_settings.custom_field.asana_created_field",
                  "custom_field_settings.custom_field.created_by",
                  "custom_field_settings.custom_field.created_by.name",
                  "custom_field_settings.custom_field.currency_code",
                  "custom_field_settings.custom_field.custom_label",
                  "custom_field_settings.custom_field.custom_label_position",
                  "custom_field_settings.custom_field.date_value",
                  "custom_field_settings.custom_field.date_value.date",
                  "custom_field_settings.custom_field.date_value.date_time",
                  "custom_field_settings.custom_field.default_access_level",
                  "custom_field_settings.custom_field.description",
                  "custom_field_settings.custom_field.display_value",
                  "custom_field_settings.custom_field.enabled",
                  "custom_field_settings.custom_field.enum_options",
                  "custom_field_settings.custom_field.enum_options.color",
                  "custom_field_settings.custom_field.enum_options.enabled",
                  "custom_field_settings.custom_field.enum_options.name",
                  "custom_field_settings.custom_field.enum_value",
                  "custom_field_settings.custom_field.enum_value.color",
                  "custom_field_settings.custom_field.enum_value.enabled",
                  "custom_field_settings.custom_field.enum_value.name",
                  "custom_field_settings.custom_field.format",
                  "custom_field_settings.custom_field.has_notifications_enabled",
                  "custom_field_settings.custom_field.id_prefix",
                  "custom_field_settings.custom_field.input_restrictions",
                  "custom_field_settings.custom_field.is_formula_field",
                  "custom_field_settings.custom_field.is_global_to_workspace",
                  "custom_field_settings.custom_field.is_value_read_only",
                  "custom_field_settings.custom_field.multi_enum_values",
                  "custom_field_settings.custom_field.multi_enum_values.color",
                  "custom_field_settings.custom_field.multi_enum_values.enabled",
                  "custom_field_settings.custom_field.multi_enum_values.name",
                  "custom_field_settings.custom_field.name",
                  "custom_field_settings.custom_field.number_value",
                  "custom_field_settings.custom_field.people_value",
                  "custom_field_settings.custom_field.people_value.name",
                  "custom_field_settings.custom_field.precision",
                  "custom_field_settings.custom_field.privacy_setting",
                  "custom_field_settings.custom_field.reference_value",
                  "custom_field_settings.custom_field.reference_value.name",
                  "custom_field_settings.custom_field.representation_type",
                  "custom_field_settings.custom_field.resource_subtype",
                  "custom_field_settings.custom_field.text_value",
                  "custom_field_settings.custom_field.type",
                  "custom_field_settings.is_important",
                  "custom_field_settings.parent",
                  "custom_field_settings.parent.name",
                  "custom_field_settings.project",
                  "custom_field_settings.project.name",
                  "description",
                  "edit_team_name_or_description_access_level",
                  "edit_team_visibility_or_trash_team_access_level",
                  "endorsed",
                  "guest_invite_management_access_level",
                  "html_description",
                  "join_request_management_access_level",
                  "member_invite_management_access_level",
                  "name",
                  "offset",
                  "organization",
                  "organization.name",
                  "path",
                  "permalink_url",
                  "team_content_management_access_level",
                  "team_member_removal_access_level",
                  "uri",
                  "visibility"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Returns the team records for all teams in the organization or workspace accessible to the authenticated user.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TeamCompact"
                      }
                    },
                    "next_page": {
                      "$ref": "#/components/schemas/NextPage"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "401": {
            "$ref": "#/components/responses/Unauthorized"
          },
          "403": {
            "$ref": "#/components/responses/Forbidden"
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          },
          "500": {
            "$ref": "#/components/responses/InternalServerError"
          }
        },
        "security": [
          {
            "personalAccessToken": []
          },
          {
            "oauth2": [
              "teams:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Team> result = client.teams.getTeamsForWorkspace(workspaceGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet teamsApiInstance = new Asana.TeamsApi(client);\nlet workspace_gid = \"12345\"; // String | Globally unique identifier for the workspace or organization.\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,offset,organization,organization.name,path,permalink_url,team_content_management_access_level,team_member_removal_access_level,uri,visibility\"\n};\nteamsApiInstance.getTeamsForWorkspace(workspace_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.teams.getTeamsForWorkspace(workspaceGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nteams_api_instance = asana.TeamsApi(api_client)\nworkspace_gid = \"12345\" # str | Globally unique identifier for the workspace or organization.\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,offset,organization,organization.name,path,permalink_url,team_content_management_access_level,team_member_removal_access_level,uri,visibility\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get teams in a workspace\n    api_response = teams_api_instance.get_teams_for_workspace(workspace_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TeamsApi->get_teams_for_workspace: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.teams.get_teams_for_workspace(workspace_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->teams->getTeamsForWorkspace($workspace_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.teams.get_teams_for_workspace(workspace_gid: 'workspace_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/users/{user_gid}/teams": {
      "get": {
        "summary": "Get teams for a user",
        "description": "<b>Required scope: </b><code>teams:read</code>\n\nReturns the compact records for all teams to which the given user is assigned.",
        "tags": [
          "Teams"
        ],
        "operationId": "getTeamsForUser",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "custom_field_settings",
              "custom_field_settings.custom_field",
              "custom_field_settings.custom_field.asana_created_field",
              "custom_field_settings.custom_field.created_by",
              "custom_field_settings.custom_field.created_by.name",
              "custom_field_settings.custom_field.currency_code",
              "custom_field_settings.custom_field.custom_label",
              "custom_field_settings.custom_field.custom_label_position",
              "custom_field_settings.custom_field.date_value",
              "custom_field_settings.custom_field.date_value.date",
              "custom_field_settings.custom_field.date_value.date_time",
              "custom_field_settings.custom_field.default_access_level",
              "custom_field_settings.custom_field.description",
              "custom_field_settings.custom_field.display_value",
              "custom_field_settings.custom_field.enabled",
              "custom_field_settings.custom_field.enum_options",
              "custom_field_settings.custom_field.enum_options.color",
              "custom_field_settings.custom_field.enum_options.enabled",
              "custom_field_settings.custom_field.enum_options.name",
              "custom_field_settings.custom_field.enum_value",
              "custom_field_settings.custom_field.enum_value.color",
              "custom_field_settings.custom_field.enum_value.enabled",
              "custom_field_settings.custom_field.enum_value.name",
              "custom_field_settings.custom_field.format",
              "custom_field_settings.custom_field.has_notifications_enabled",
              "custom_field_settings.custom_field.id_prefix",
              "custom_field_settings.custom_field.input_restrictions",
              "custom_field_settings.custom_field.is_formula_field",
              "custom_field_settings.custom_field.is_global_to_workspace",
              "custom_field_settings.custom_field.is_value_read_only",
              "custom_field_settings.custom_field.multi_enum_values",
              "custom_field_settings.custom_field.multi_enum_values.color",
              "custom_field_settings.custom_field.multi_enum_values.enabled",
              "custom_field_settings.custom_field.multi_enum_values.name",
              "custom_field_settings.custom_field.name",
              "custom_field_settings.custom_field.number_value",
              "custom_field_settings.custom_field.people_value",
              "custom_field_settings.custom_field.people_value.name",
              "custom_field_settings.custom_field.precision",
              "custom_field_settings.custom_field.privacy_setting",
              "custom_field_settings.custom_field.reference_value",
              "custom_field_settings.custom_field.reference_value.name",
              "custom_field_settings.custom_field.representation_type",
              "custom_field_settings.custom_field.resource_subtype",
              "custom_field_settings.custom_field.text_value",
              "custom_field_settings.custom_field.type",
              "custom_field_settings.is_important",
              "custom_field_settings.parent",
              "custom_field_settings.parent.name",
              "custom_field_settings.project",
              "custom_field_settings.project.name",
              "description",
              "edit_team_name_or_description_access_level",
              "edit_team_visibility_or_trash_team_access_level",
              "endorsed",
              "guest_invite_management_access_level",
              "html_description",
              "join_request_management_access_level",
              "member_invite_management_access_level",
              "name",
              "offset",
              "organization",
              "organization.name",
              "path",
              "permalink_url",
              "team_content_management_access_level",
              "team_member_removal_access_level",
              "uri",
              "visibility"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "custom_field_settings",
                  "custom_field_settings.custom_field",
                  "custom_field_settings.custom_field.asana_created_field",
                  "custom_field_settings.custom_field.created_by",
                  "custom_field_settings.custom_field.created_by.name",
                  "custom_field_settings.custom_field.currency_code",
                  "custom_field_settings.custom_field.custom_label",
                  "custom_field_settings.custom_field.custom_label_position",
                  "custom_field_settings.custom_field.date_value",
                  "custom_field_settings.custom_field.date_value.date",
                  "custom_field_settings.custom_field.date_value.date_time",
                  "custom_field_settings.custom_field.default_access_level",
                  "custom_field_settings.custom_field.description",
                  "custom_field_settings.custom_field.display_value",
                  "custom_field_settings.custom_field.enabled",
                  "custom_field_settings.custom_field.enum_options",
                  "custom_field_settings.custom_field.enum_options.color",
                  "custom_field_settings.custom_field.enum_options.enabled",
                  "custom_field_settings.custom_field.enum_options.name",
                  "custom_field_settings.custom_field.enum_value",
                  "custom_field_settings.custom_field.enum_value.color",
                  "custom_field_settings.custom_field.enum_value.enabled",
                  "custom_field_settings.custom_field.enum_value.name",
                  "custom_field_settings.custom_field.format",
                  "custom_field_settings.custom_field.has_notifications_enabled",
                  "custom_field_settings.custom_field.id_prefix",
                  "custom_field_settings.custom_field.input_restrictions",
                  "custom_field_settings.custom_field.is_formula_field",
                  "custom_field_settings.custom_field.is_global_to_workspace",
                  "custom_field_settings.custom_field.is_value_read_only",
                  "custom_field_settings.custom_field.multi_enum_values",
                  "custom_field_settings.custom_field.multi_enum_values.color",
                  "custom_field_settings.custom_field.multi_enum_values.enabled",
                  "custom_field_settings.custom_field.multi_enum_values.name",
                  "custom_field_settings.custom_field.name",
                  "custom_field_settings.custom_field.number_value",
                  "custom_field_settings.custom_field.people_value",
                  "custom_field_settings.custom_field.people_value.name",
                  "custom_field_settings.custom_field.precision",
                  "custom_field_settings.custom_field.privacy_setting",
                  "custom_field_settings.custom_field.reference_value",
                  "custom_field_settings.custom_field.reference_value.name",
                  "custom_field_settings.custom_field.representation_type",
                  "custom_field_settings.custom_field.resource_subtype",
                  "custom_field_settings.custom_field.text_value",
                  "custom_field_settings.custom_field.type",
                  "custom_field_settings.is_important",
                  "custom_field_settings.parent",
                  "custom_field_settings.parent.name",
                  "custom_field_settings.project",
                  "custom_field_settings.project.name",
                  "description",
                  "edit_team_name_or_description_access_level",
                  "edit_team_visibility_or_trash_team_access_level",
                  "endorsed",
                  "guest_invite_management_access_level",
                  "html_description",
                  "join_request_management_access_level",
                  "member_invite_management_access_level",
                  "name",
                  "offset",
                  "organization",
                  "organization.name",
                  "path",
                  "permalink_url",
                  "team_content_management_access_level",
                  "team_member_removal_access_level",
                  "uri",
                  "visibility"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Returns the team records for all teams in the organization or workspace to which the given user is assigned.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TeamCompact"
                      }
                    },
                    "next_page": {
                      "$ref": "#/components/schemas/NextPage"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "401": {
            "$ref": "#/components/responses/Unauthorized"
          },
          "403": {
            "$ref": "#/components/responses/Forbidden"
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          },
          "500": {
            "$ref": "#/components/responses/InternalServerError"
          }
        },
        "security": [
          {
            "personalAccessToken": []
          },
          {
            "oauth2": [
              "teams:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Team> result = client.teams.getTeamsForUser(userGid, organization)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet teamsApiInstance = new Asana.TeamsApi(client);\nlet user_gid = \"me\"; // String | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nlet organization = \"1331\"; // String | The workspace or organization to filter teams on.\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,offset,organization,organization.name,path,permalink_url,team_content_management_access_level,team_member_removal_access_level,uri,visibility\"\n};\nteamsApiInstance.getTeamsForUser(user_gid, organization, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.teams.getTeamsForUser(userGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nteams_api_instance = asana.TeamsApi(api_client)\nuser_gid = \"me\" # str | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\norganization = \"1331\" # str | The workspace or organization to filter teams on.\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,endorsed,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,offset,organization,organization.name,path,permalink_url,team_content_management_access_level,team_member_removal_access_level,uri,visibility\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get teams for a user\n    api_response = teams_api_instance.get_teams_for_user(user_gid, organization, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TeamsApi->get_teams_for_user: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.teams.get_teams_for_user(user_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->teams->getTeamsForUser($user_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.teams.get_teams_for_user(user_gid: 'user_gid', organization: '&#x27;organization_example&#x27;', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/teams/{team_gid}/addUser": {
      "post": {
        "summary": "Add a user to a team",
        "description": "The user making this call must be a member of the team in order to add others. The user being added must exist in the same organization as the team.\n\nReturns the complete team membership record for the newly added user.",
        "tags": [
          "Teams"
        ],
        "operationId": "addUserForTeam",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "is_admin",
              "is_guest",
              "is_limited_access",
              "team",
              "team.name",
              "user",
              "user.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "is_admin",
                  "is_guest",
                  "is_limited_access",
                  "team",
                  "team.name",
                  "user",
                  "user.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "The user to add to the team.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TeamAddUserRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully added user to the team.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TeamMembershipResponse"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "401": {
            "$ref": "#/components/responses/Unauthorized"
          },
          "403": {
            "$ref": "#/components/responses/Forbidden"
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          },
          "500": {
            "$ref": "#/components/responses/InternalServerError"
          }
        },
        "security": [
          {
            "personalAccessToken": []
          },
          {
            "oauth2": []
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.teams.addUserForTeam(teamGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet teamsApiInstance = new Asana.TeamsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The user to add to the team.\nlet team_gid = \"159874\"; // String | Globally unique identifier for the team.\nlet opts = { \n    'opt_fields': \"is_admin,is_guest,is_limited_access,team,team.name,user,user.name\"\n};\nteamsApiInstance.addUserForTeam(body, team_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.teams.addUserForTeam(teamGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nteams_api_instance = asana.TeamsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The user to add to the team.\nteam_gid = \"159874\" # str | Globally unique identifier for the team.\nopts = {\n    'opt_fields': \"is_admin,is_guest,is_limited_access,team,team.name,user,user.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Add a user to a team\n    api_response = teams_api_instance.add_user_for_team(body, team_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TeamsApi->add_user_for_team: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.teams.add_user_for_team(team_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->teams->addUserForTeam($team_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.teams.add_user_for_team(team_gid: 'team_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/teams/{team_gid}/removeUser": {
      "post": {
        "summary": "Remove a user from a team",
        "description": "The user making this call must be a member of the team in order to remove themselves or others.",
        "tags": [
          "Teams"
        ],
        "operationId": "removeUserForTeam",
        "requestBody": {
          "description": "The user to remove from the team.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TeamRemoveUserRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Returns an empty data record",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/EmptyResponse"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "401": {
            "$ref": "#/components/responses/Unauthorized"
          },
          "403": {
            "$ref": "#/components/responses/Forbidden"
          },
          "404": {
            "$ref": "#/components/responses/NotFound"
          },
          "500": {
            "$ref": "#/components/responses/InternalServerError"
          }
        },
        "security": [
          {
            "personalAccessToken": []
          },
          {
            "oauth2": []
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.teams.removeUserForTeam(teamGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet teamsApiInstance = new Asana.TeamsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The user to remove from the team.\nlet team_gid = \"159874\"; // String | Globally unique identifier for the team.\n\nteamsApiInstance.removeUserForTeam(body, team_gid).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.teams.removeUserForTeam(teamGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nteams_api_instance = asana.TeamsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The user to remove from the team.\nteam_gid = \"159874\" # str | Globally unique identifier for the team.\n\n\ntry:\n    # Remove a user from a team\n    api_response = teams_api_instance.remove_user_for_team(body, team_gid)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TeamsApi->remove_user_for_team: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.teams.remove_user_for_team(team_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->teams->removeUserForTeam($team_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.teams.remove_user_for_team(team_gid: 'team_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    }
  },
  "schemas": {
    "TeamBase": {
      "$ref": "#/components/schemas/TeamCompact"
    },
    "CustomFieldSettingBase": {
      "$ref": "#/components/schemas/CustomFieldSettingCompact"
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
    "TeamMembershipBase": {
      "$ref": "#/components/schemas/TeamMembershipCompact"
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
            "$ref": "#/components/schemas/EnumOption"
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
              "$ref": "#/components/schemas/EnumOption"
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
            "$ref": "#/components/schemas/EnumOption"
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
    "TeamMembershipResponse": {
      "$ref": "#/components/schemas/TeamMembershipBase"
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
          "$ref": "#/components/schemas/UserCompact"
        },
        "team": {
          "$ref": "#/components/schemas/TeamCompact"
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
    "CustomFieldBase": {
      "allOf": [
        {
          "$ref": "#/components/schemas/CustomFieldCompact"
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
                "$ref": "#/components/schemas/EnumOption"
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
    "TeamRequest": {
      "allOf": [
        {
          "$ref": "#/components/schemas/TeamBase"
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
    "EmptyResponse": {
      "type": "object",
      "description": "An empty object. Some endpoints do not return an object on success. The success is conveyed through a 2-- status code and returning an empty object."
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
    "TeamResponse": {
      "allOf": [
        {
          "$ref": "#/components/schemas/TeamBase"
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
                  "$ref": "#/components/schemas/WorkspaceCompact"
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
                "$ref": "#/components/schemas/CustomFieldSettingResponse"
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
    "CustomFieldSettingResponse": {
      "allOf": [
        {
          "$ref": "#/components/schemas/CustomFieldSettingBase"
        },
        {
          "type": "object",
          "properties": {
            "project": {
              "allOf": [
                {
                  "$ref": "#/components/schemas/ProjectCompact"
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
                  "$ref": "#/components/schemas/ProjectCompact"
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
                  "$ref": "#/components/schemas/CustomFieldResponse"
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
    "CustomFieldResponse": {
      "allOf": [
        {
          "$ref": "#/components/schemas/CustomFieldBase"
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
                  "$ref": "#/components/schemas/UserCompact"
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
                "$ref": "#/components/schemas/UserCompact"
              }
            },
            "reference_value": {
              "description": "*Conditional*. Only relevant for custom fields of type `reference`. This array of objects reflects the values of a `reference` custom field.",
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/AsanaNamedResource"
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
    }
  },
  "primary_response_schema": {
    "type": "object",
    "properties": {
      "data": {
        "$ref": "#/components/schemas/TeamResponse"
      }
    }
  }
}
```

### Relationship manifest

```yaml
asana_teams:
  project_id:
    target_table: asana_projects
    target_column: id
    confidence: high
    reason: 'response schema: data.custom_field_settings[].project.gid'
  parent_id:
    target_table: asana_teams
    target_column: id
    confidence: high
    reason: 'response schema: data.custom_field_settings[].parent.gid'
  user_id:
    target_table: asana_users
    target_column: id
    confidence: high
    reason: 'request body on POST /teams/{team_gid}/addUser: data.user'

```

### FK dependency schemas (for stub creation if needed)

```json
{
  "projects": {
    "primary_response_schema": {
      "type": "object",
      "properties": {
        "data": {
          "$ref": "#/components/schemas/ProjectResponse"
        }
      }
    }
  },
  "users": {
    "primary_response_schema": {
      "type": "object",
      "properties": {
        "data": {
          "$ref": "#/components/schemas/UserResponse"
        }
      }
    }
  }
}
```

### ID format

Resource `team` uses: alphabet=ALPHANUMERIC, length=16

---

## Files you will edit

You will add to these four files. Each file already exists with app-level
scaffolding and possibly earlier entity implementations. Read the current
contents before editing.

1. **`database/schema.py`** — add the ORM model
2. **`database/operations.py`** — add CRUD functions
3. **`core/serializers.py`** — add serialization functions
4. **`api/routes.py`** — add handler functions and Route entries

---

## Step 1: ORM model (`database/schema.py`)

Add a class `Team(Base)` with:

- Table name: `asana_teams`
- One column per field in the OpenAPI response schema
- Use the type mappings:
  - `string` → `String(N)` or `Text`
  - `integer` → `Integer`
  - `boolean` → `Boolean`
  - `object` (nested) → `JSONB` (if not queried), or a separate table (if queried)
  - nullable fields → `Mapped[Optional[T]]` with `nullable=True`
- For each FK listed in the relationship manifest:
  - Add `ForeignKey("target_table.id")` on the column
  - Add a `relationship()` on both sides
  - If the target entity does not yet have a model, create a **stub**:
    ```python
    # STUB — expand when implementing this resource
    class TargetEntity(Base):
        __tablename__ = "..."
        id: Mapped[str] = mapped_column(String(50), primary_key=True)
        # minimal fields for FK integrity only
    ```
- Add indexes on columns used for filtering (FK columns, status flags)
- Timestamps: store as `String(50)` if the API returns ISO strings

## Step 2: CRUD operations (`database/operations.py`)

Add functions for each operation in the OpenAPI excerpt. Follow these patterns:

**Get by ID:**
```python
def get_{{entity}}(session: Session, {{entity}}_id: str) -> {{Model}} | None:
    return session.execute(
        select({{Model}}).where({{Model}}.id == {{entity}}_id, {{Model}}.is_deleted.is_(False))
    ).scalar_one_or_none()
```

**List with cursor pagination:**
```python
def list_{{entities}}(
    session: Session,
    *,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[{{Model}}], str | None]:
    query = select({{Model}}).where(...).order_by(...)
    if cursor is not None:
        # seek past the cursor position
        ...
    results = session.execute(query.limit(limit + 1)).scalars().all()
    if len(results) > limit:
        return list(results[:limit]), results[limit - 1].id
    return list(results), None
```

**Create:**
```python
def create_{{entity}}(session: Session, *, ...fields...) -> {{Model}}:
    record = {{Model}}(id=generate_id("{{entity}}"), ...fields..., created_at=now_iso(), updated_at=now_iso())
    session.add(record)
    session.flush()
    return record
```

**Update (partial):**
```python
def update_{{entity}}(session: Session, *, {{entity}}_id: str, ...optional_fields...) -> {{Model}} | None:
    record = get_{{entity}}(session, {{entity}}_id)
    if record is None:
        return None
    if field is not None:
        record.field = field  # for each optional field
    record.updated_at = now_iso()
    session.flush()
    return record
```

**Delete (soft):**
```python
def delete_{{entity}}(session: Session, {{entity}}_id: str) -> bool:
    record = get_{{entity}}(session, {{entity}}_id)
    if record is None:
        return False
    record.is_deleted = True
    record.updated_at = now_iso()
    session.flush()
    return True
```

**Action (e.g. archive):**
```python
def archive_{{entity}}(session: Session, {{entity}}_id: str) -> bool:
    record = get_{{entity}}(session, {{entity}}_id)
    if record is None:
        return False
    record.is_archived = True
    record.updated_at = now_iso()
    session.flush()
    return True
```

Rules:
- Every function takes `Session` as the first argument
- Use `generate_id("{{entity}}")` for new IDs
- Use `now_iso()` for timestamps
- Use `session.flush()` after mutations (not `session.commit()`)
- Filter out `is_deleted` rows in all queries

## Step 3: Serializers (`core/serializers.py`)

Add:

```python
def serialize_{{entity}}(record: {{Model}}) -> dict[str, Any]:
    # Return a dict matching the OpenAPI response schema exactly.
    # Include every field from the response. Use the same key names
    # as the API (preserve casing).
```

```python
def serialize_{{entity}}_list(
    records: list[{{Model}}],
    *,
    next_cursor: str | None,
) -> dict[str, Any]:
    return {
        "results": [serialize_{{entity}}(r) for r in records],
        "next_cursor": next_cursor,
    }
```

Rules:
- Field names in the output dict must match the API response exactly
- Conditionally include fields that only appear for certain subtypes
  (e.g. workspace-only fields when workspace_id is set)

## Step 4: Route handlers (`api/routes.py`)

Add one handler per operation. Every handler follows this pattern:

```python
async def <operation>_{{entity}}(request: Request) -> JSONResponse:
    try:
        session = _session(request)
        # extract path params, query params, or JSON body as needed
        # call the appropriate ops.* function
        # serialize the result
        return JSONResponse(payload, status_code=status.HTTP_200_OK)
    except AppAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)
```

Then add Route entries to the `routes` list.

Rules:
- Fixed paths before parameterized paths (e.g. `/search` before `/{id}`)
- **The catch-all `Route("/{_unknown_path:path}", unknown_endpoint, ...)`
  at the bottom of the list MUST remain the last entry.** Insert your
  new routes ABOVE it. Starlette matches in order, so anything placed
  after the catch-all would be unreachable.
- Do NOT remove, rename, or modify the `unknown_endpoint` handler or
  the catch-all Route entry — it is the replica's universal fallback
  for unimplemented endpoints and must be preserved across every
  resource implementation.
- Use `_session(request)` for DB access
- Use `_principal_user_id(request)` for the acting user
- Use `_parse_json_body(request)` for POST/PUT/PATCH bodies
- Use `_pagination_params(request)` for cursor + limit
- Validate required fields and raise `bad_request()` if missing

---

## What NOT to do

- Do not modify `database/base.py`
- Do not modify or remove existing functions in any file — you may only add
  new functions, classes, and Route entries alongside what already exists
- Do not invent API behavior not present in the OpenAPI excerpt
- Do not add fields not present in the OpenAPI response schema
- Do not use `session.commit()` — only `session.flush()`
- Do not hard-delete records unless the API explicitly requires it

## What you MAY do beyond the four files above

- You may add new helper functions to `core/utils.py` if this entity needs
  supporting utilities (e.g. cursor encoding, field normalization, enum
  validation, timestamp format conversion). Do not modify existing functions.
- You may add new error constructors to `core/errors.py` if this entity
  requires error types not yet defined. Do not modify existing constructors.


---

## Current file contents

Below are the current contents of each file you will edit. You must preserve all existing code and add your new code alongside it.

### `database/schema.py`

```python
"""ORM schema for the Asana API replica.

Entities are added to this file one at a time during the resource
implementation loop. Each entity implementation may also add stub models
for FK dependencies marked with: # STUB — expand when implementing this resource

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its model class to this file incrementally.
"""

from typing import Any, Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

```

### `database/operations.py`

```python
"""Session-first CRUD operations for Asana.

Functions are added to this file one at a time during the resource
implementation loop. Every function takes a SQLAlchemy Session as the first
argument. No function accesses request state directly.

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its operation functions to this file incrementally.
"""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..core.utils import generate_id, now_iso

```

### `core/serializers.py`

```python
"""Serialization helpers for the Asana API replica.

Each serialize function converts an ORM model into a dict matching the
source API's response shape. Functions are added one at a time during the
resource implementation loop.

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its serializer functions to this file incrementally.
"""

from __future__ import annotations

from typing import Any

```

### `api/routes.py`

```python
"""Asana REST API routes.

Mounted under /api/env/{env_id}/services/asana
DB session comes from request.state.db_session (IsolationMiddleware).
User impersonation comes from request.state.impersonate_user_id.

Route handlers and route entries are added one at a time during the resource
implementation loop. The request helpers below are universal.
"""

from __future__ import annotations

from typing import Any

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from sqlalchemy.orm import Session

from ..core.errors import (
    AppAPIError,
    bad_request,
    handle_exception,
    not_found,
    unauthorized,
)
from ..database import operations as ops


# ---------------------------------------------------------------------------
# Request helpers — universal across apps
# ---------------------------------------------------------------------------


def _session(request: Request) -> Session:
    """Get the environment-scoped DB session from request.state."""
    session = getattr(request.state, "db_session", None)
    if session is None:
        raise unauthorized("Missing database session")
    return session


def _principal_user_id(request: Request) -> str:
    """Resolve the acting principal from request state."""
    principal = getattr(request.state, "impersonate_user_id", None)
    if principal is not None and str(principal).strip() != "":
        return str(principal)
    raise unauthorized("Missing user authentication")


async def _parse_json_body(request: Request) -> dict[str, Any]:
    """Parse JSON body. Raises app-shaped bad_request on malformed input."""
    try:
        return await request.json()
    except Exception as exc:
        raise bad_request(f"Invalid JSON body: {exc}") from exc


def _pagination_params(request: Request) -> tuple[str | None, int]:
    """Extract cursor and limit from query params (cursor-based pagination)."""
    cursor = request.query_params.get("cursor")
    limit_str = request.query_params.get("limit")
    limit = 50
    if limit_str is not None:
        try:
            limit = max(1, min(200, int(limit_str)))
        except ValueError:
            pass
    return cursor, limit


# ---------------------------------------------------------------------------
# Endpoint handlers — added per entity by entity scaffold
# ---------------------------------------------------------------------------

# AGENT INSTRUCTION: Add endpoint handler functions here during entity
# implementation. Each handler follows this pattern:
#
#   async def <operation>_<entity>(request: Request) -> JSONResponse:
#       try:
#           session = _session(request)
#           # ... extract params, call ops, serialize ...
#           return JSONResponse(payload, status_code=status.HTTP_200_OK)
#       except AppAPIError as exc:
#           return exc.to_response()
#       except Exception as exc:
#           return handle_exception(exc)


# ---------------------------------------------------------------------------
# Unknown-endpoint catch-all — universal across apps
# ---------------------------------------------------------------------------
#
# Any request whose path does not match a real route in the table below
# lands here. Returning the replica's native not-found envelope (via
# ``not_found().to_response()``) means agents calling unimplemented
# endpoints during development receive a response that is shape-compatible
# with the target API, instead of Starlette's default plain-text
# ``"Not Found"`` or — worse — an IsolationMiddleware 500.
#
# This makes the replica behave authentically even before every endpoint
# has been implemented: the agent cannot tell from the shape of a 404
# whether the endpoint is unimplemented or genuinely missing upstream.

async def unknown_endpoint(request: Request) -> JSONResponse:
    """Catch-all handler for requests that match no real route."""
    return not_found(
        f"Endpoint not found: {request.method} {request.url.path}"
    ).to_response()


# ---------------------------------------------------------------------------
# Route table — entries added per entity by entity scaffold
# ---------------------------------------------------------------------------

# AGENT INSTRUCTION: Add new Route entries ABOVE the catch-all at the
# bottom of this list. Two hard rules:
#
#   1. Fixed paths (e.g. /projects/archived) must come before parameterized
#      paths (e.g. /projects/{project_id}) so Starlette matches them first.
#   2. The ``/{_unknown_path:path}`` catch-all must always remain the LAST
#      entry in the list. Starlette matches in order, so any route placed
#      after it would be unreachable.

routes: list[Route] = [
    # --- Real endpoints go here (added by the entity implementation loop) ---

    # --- Catch-all — MUST be the last entry ---
    Route(
        "/{_unknown_path:path}",
        unknown_endpoint,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
    ),
]

```


---

## Output format

Return the **complete updated contents** of each file you modified. Use this
exact format for each file:

### FILE: database/schema.py
```python
<complete file contents>
```

### FILE: database/operations.py
```python
<complete file contents>
```

### FILE: core/serializers.py
```python
<complete file contents>
```

### FILE: api/routes.py
```python
<complete file contents>
```

If you also modify core/utils.py or core/errors.py, include them too:

### FILE: core/utils.py
```python
<complete file contents>
```

IMPORTANT: Return the COMPLETE file contents for each file, not just the
additions. The files will be overwritten with your output.
