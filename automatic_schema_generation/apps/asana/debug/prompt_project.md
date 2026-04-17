# Entity Implementation: projects

You are implementing the **projects** resource for the Asana API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for projects

```json
{
  "paths": {
    "/projects": {
      "get": {
        "summary": "Get multiple projects",
        "description": "<b>Required scope: </b><code>projects:read</code>\n\nReturns the compact project records for some filtered set of projects. Use one or more of the parameters provided to filter the projects returned.\n*Note: This endpoint may timeout for large domains. Try filtering by team!*\n**The `team` filter is deprecated.** Please use `GET /memberships` with `{ member: team, resource_subtype: project_membership }` to find projects shared with a team.",
        "tags": [
          "Projects"
        ],
        "operationId": "getProjects",
        "parameters": [
          {
            "$ref": "#/components/parameters/limit"
          },
          {
            "$ref": "#/components/parameters/offset"
          },
          {
            "name": "workspace",
            "in": "query",
            "description": "The workspace or organization to filter projects on.",
            "schema": {
              "type": "string"
            },
            "example": "1331"
          },
          {
            "name": "team",
            "in": "query",
            "description": "**Deprecated.** The team to filter projects on. Please use `GET /memberships` with `{ member: team, resource_subtype: project_membership }` instead.",
            "schema": {
              "type": "string"
            },
            "example": "14916",
            "deprecated": true
          },
          {
            "$ref": "#/components/parameters/archived_query_param"
          },
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "archived",
              "color",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_from_template",
              "created_from_template.name",
              "current_status",
              "current_status.author",
              "current_status.author.name",
              "current_status.color",
              "current_status.created_at",
              "current_status.created_by",
              "current_status.created_by.name",
              "current_status.html_text",
              "current_status.modified_at",
              "current_status.text",
              "current_status.title",
              "current_status_update",
              "current_status_update.resource_subtype",
              "current_status_update.title",
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
              "custom_fields",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.display_value",
              "custom_fields.enabled",
              "custom_fields.enum_options",
              "custom_fields.enum_options.color",
              "custom_fields.enum_options.enabled",
              "custom_fields.enum_options.name",
              "custom_fields.enum_value",
              "custom_fields.enum_value.color",
              "custom_fields.enum_value.enabled",
              "custom_fields.enum_value.name",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.representation_type",
              "custom_fields.text_value",
              "custom_fields.type",
              "default_access_level",
              "default_view",
              "due_date",
              "due_on",
              "followers",
              "followers.name",
              "html_notes",
              "icon",
              "members",
              "members.name",
              "minimum_access_level_for_customization",
              "minimum_access_level_for_sharing",
              "modified_at",
              "name",
              "notes",
              "offset",
              "owner",
              "path",
              "permalink_url",
              "privacy_setting",
              "project_brief",
              "public",
              "start_on",
              "team",
              "team.name",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "archived",
                  "color",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_from_template",
                  "created_from_template.name",
                  "current_status",
                  "current_status.author",
                  "current_status.author.name",
                  "current_status.color",
                  "current_status.created_at",
                  "current_status.created_by",
                  "current_status.created_by.name",
                  "current_status.html_text",
                  "current_status.modified_at",
                  "current_status.text",
                  "current_status.title",
                  "current_status_update",
                  "current_status_update.resource_subtype",
                  "current_status_update.title",
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
                  "custom_fields",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.display_value",
                  "custom_fields.enabled",
                  "custom_fields.enum_options",
                  "custom_fields.enum_options.color",
                  "custom_fields.enum_options.enabled",
                  "custom_fields.enum_options.name",
                  "custom_fields.enum_value",
                  "custom_fields.enum_value.color",
                  "custom_fields.enum_value.enabled",
                  "custom_fields.enum_value.name",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.representation_type",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "default_access_level",
                  "default_view",
                  "due_date",
                  "due_on",
                  "followers",
                  "followers.name",
                  "html_notes",
                  "icon",
                  "members",
                  "members.name",
                  "minimum_access_level_for_customization",
                  "minimum_access_level_for_sharing",
                  "modified_at",
                  "name",
                  "notes",
                  "offset",
                  "owner",
                  "path",
                  "permalink_url",
                  "privacy_setting",
                  "project_brief",
                  "public",
                  "start_on",
                  "team",
                  "team.name",
                  "uri",
                  "workspace",
                  "workspace.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Successfully retrieved projects.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/ProjectCompact"
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
              "projects:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Project> result = client.projects.getProjects(archived, team, workspace)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'workspace': \"1331\", \n    'team': \"14916\", \n    'archived': false, \n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name\"\n};\nprojectsApiInstance.getProjects(opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.getProjects({param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'workspace': \"1331\", # str | The workspace or organization to filter projects on.\n    'team': \"14916\", # str | **Deprecated.** The team to filter projects on. Please use `GET /memberships` with `{ member: team, resource_subtype: project_membership }` instead.\n    'archived': False, # bool | Only return projects whose `archived` field takes on the value of this parameter.\n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get multiple projects\n    api_response = projects_api_instance.get_projects(opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->get_projects: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.get_projects({'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->getProjects(array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.get_projects(param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "post": {
        "summary": "Create a project",
        "description": "<b>Required scope: </b><code>projects:write</code>\n\nCreate a new project in a workspace or team.\n\nEvery project is required to be created in a specific workspace or\norganization, and this cannot be changed once set. Note that you can use\nthe `workspace` parameter regardless of whether or not it is an\norganization.\n\nIf the workspace for your project is an organization, you must also\nsupply a `team` to share the project with.\n\nReturns the full record of the newly created project.\n\n**Deprecation notice:** The `team` parameter and the `private_to_team`\nvalue for `privacy_setting` are deprecated. When either is included in\nthe request, the `Asana-Change` response header will indicate an affected\ndeprecation. Clients should switch to using `POST /memberships` with\n`{ parent: project, member: team }` to share a project with a team after\ncreation.",
        "tags": [
          "Projects"
        ],
        "operationId": "createProject",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "archived",
              "color",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_from_template",
              "created_from_template.name",
              "current_status",
              "current_status.author",
              "current_status.author.name",
              "current_status.color",
              "current_status.created_at",
              "current_status.created_by",
              "current_status.created_by.name",
              "current_status.html_text",
              "current_status.modified_at",
              "current_status.text",
              "current_status.title",
              "current_status_update",
              "current_status_update.resource_subtype",
              "current_status_update.title",
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
              "custom_fields",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.display_value",
              "custom_fields.enabled",
              "custom_fields.enum_options",
              "custom_fields.enum_options.color",
              "custom_fields.enum_options.enabled",
              "custom_fields.enum_options.name",
              "custom_fields.enum_value",
              "custom_fields.enum_value.color",
              "custom_fields.enum_value.enabled",
              "custom_fields.enum_value.name",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.representation_type",
              "custom_fields.text_value",
              "custom_fields.type",
              "default_access_level",
              "default_view",
              "due_date",
              "due_on",
              "followers",
              "followers.name",
              "html_notes",
              "icon",
              "members",
              "members.name",
              "minimum_access_level_for_customization",
              "minimum_access_level_for_sharing",
              "modified_at",
              "name",
              "notes",
              "owner",
              "permalink_url",
              "privacy_setting",
              "project_brief",
              "public",
              "start_on",
              "team",
              "team.name",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "archived",
                  "color",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_from_template",
                  "created_from_template.name",
                  "current_status",
                  "current_status.author",
                  "current_status.author.name",
                  "current_status.color",
                  "current_status.created_at",
                  "current_status.created_by",
                  "current_status.created_by.name",
                  "current_status.html_text",
                  "current_status.modified_at",
                  "current_status.text",
                  "current_status.title",
                  "current_status_update",
                  "current_status_update.resource_subtype",
                  "current_status_update.title",
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
                  "custom_fields",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.display_value",
                  "custom_fields.enabled",
                  "custom_fields.enum_options",
                  "custom_fields.enum_options.color",
                  "custom_fields.enum_options.enabled",
                  "custom_fields.enum_options.name",
                  "custom_fields.enum_value",
                  "custom_fields.enum_value.color",
                  "custom_fields.enum_value.enabled",
                  "custom_fields.enum_value.name",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.representation_type",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "default_access_level",
                  "default_view",
                  "due_date",
                  "due_on",
                  "followers",
                  "followers.name",
                  "html_notes",
                  "icon",
                  "members",
                  "members.name",
                  "minimum_access_level_for_customization",
                  "minimum_access_level_for_sharing",
                  "modified_at",
                  "name",
                  "notes",
                  "owner",
                  "permalink_url",
                  "privacy_setting",
                  "project_brief",
                  "public",
                  "start_on",
                  "team",
                  "team.name",
                  "workspace",
                  "workspace.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "The project to create.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/ProjectRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully retrieved projects.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/ProjectResponse"
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
              "projects:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nProject result = client.projects.createProject()\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The project to create.\nlet opts = { \n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\"\n};\nprojectsApiInstance.createProject(body, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.createProject({field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The project to create.\nopts = {\n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Create a project\n    api_response = projects_api_instance.create_project(body, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->create_project: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.create_project({'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->createProject(array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.create_project(field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/projects/{project_gid}": {
      "get": {
        "summary": "Get a project",
        "description": "<b>Required scope: </b><code>projects:read</code>\n\n<table>\n  <tr>\n    <th>Field</th>\n    <th>Required Scope</th>\n  </tr>\n  <tr>\n    <td><code>team</code></td>\n    <td><code>teams:read</code></td>\n  </tr>\n</table>\n\nReturns the complete project record for a single project.",
        "tags": [
          "Projects"
        ],
        "operationId": "getProject",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "archived",
              "color",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_from_template",
              "created_from_template.name",
              "current_status",
              "current_status.author",
              "current_status.author.name",
              "current_status.color",
              "current_status.created_at",
              "current_status.created_by",
              "current_status.created_by.name",
              "current_status.html_text",
              "current_status.modified_at",
              "current_status.text",
              "current_status.title",
              "current_status_update",
              "current_status_update.resource_subtype",
              "current_status_update.title",
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
              "custom_fields",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.display_value",
              "custom_fields.enabled",
              "custom_fields.enum_options",
              "custom_fields.enum_options.color",
              "custom_fields.enum_options.enabled",
              "custom_fields.enum_options.name",
              "custom_fields.enum_value",
              "custom_fields.enum_value.color",
              "custom_fields.enum_value.enabled",
              "custom_fields.enum_value.name",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.representation_type",
              "custom_fields.text_value",
              "custom_fields.type",
              "default_access_level",
              "default_view",
              "due_date",
              "due_on",
              "followers",
              "followers.name",
              "html_notes",
              "icon",
              "members",
              "members.name",
              "minimum_access_level_for_customization",
              "minimum_access_level_for_sharing",
              "modified_at",
              "name",
              "notes",
              "owner",
              "permalink_url",
              "privacy_setting",
              "project_brief",
              "public",
              "start_on",
              "team",
              "team.name",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "archived",
                  "color",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_from_template",
                  "created_from_template.name",
                  "current_status",
                  "current_status.author",
                  "current_status.author.name",
                  "current_status.color",
                  "current_status.created_at",
                  "current_status.created_by",
                  "current_status.created_by.name",
                  "current_status.html_text",
                  "current_status.modified_at",
                  "current_status.text",
                  "current_status.title",
                  "current_status_update",
                  "current_status_update.resource_subtype",
                  "current_status_update.title",
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
                  "custom_fields",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.display_value",
                  "custom_fields.enabled",
                  "custom_fields.enum_options",
                  "custom_fields.enum_options.color",
                  "custom_fields.enum_options.enabled",
                  "custom_fields.enum_options.name",
                  "custom_fields.enum_value",
                  "custom_fields.enum_value.color",
                  "custom_fields.enum_value.enabled",
                  "custom_fields.enum_value.name",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.representation_type",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "default_access_level",
                  "default_view",
                  "due_date",
                  "due_on",
                  "followers",
                  "followers.name",
                  "html_notes",
                  "icon",
                  "members",
                  "members.name",
                  "minimum_access_level_for_customization",
                  "minimum_access_level_for_sharing",
                  "modified_at",
                  "name",
                  "notes",
                  "owner",
                  "permalink_url",
                  "privacy_setting",
                  "project_brief",
                  "public",
                  "start_on",
                  "team",
                  "team.name",
                  "workspace",
                  "workspace.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Successfully retrieved the requested project.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/ProjectResponse"
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
              "projects:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nProject result = client.projects.getProject(projectGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet project_gid = \"1331\"; // String | Globally unique identifier for the project.\nlet opts = { \n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\"\n};\nprojectsApiInstance.getProject(project_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.getProject(projectGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nproject_gid = \"1331\" # str | Globally unique identifier for the project.\nopts = {\n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get a project\n    api_response = projects_api_instance.get_project(project_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->get_project: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.get_project(project_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->getProject($project_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.get_project(project_gid: 'project_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "put": {
        "summary": "Update a project",
        "description": "<b>Required scope: </b><code>projects:write</code>\n\nA specific, existing project can be updated by making a PUT request on\nthe URL for that project. Only the fields provided in the `data` block\nwill be updated; any unspecified fields will remain unchanged.\n\nWhen using this method, it is best to specify only those fields you wish\nto change, or else you may overwrite changes made by another user since\nyou last retrieved the task.\n\nReturns the complete updated project record.\n\n**Deprecation notice:** Updating the `team` field is deprecated. When this\nfield is included in the request, the `Asana-Change` response header will\nindicate an affected deprecation. Clients should switch to using\n`POST /memberships` with `{ parent: project, member: team }` to share a\nproject with a team.",
        "tags": [
          "Projects"
        ],
        "operationId": "updateProject",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "archived",
              "color",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_from_template",
              "created_from_template.name",
              "current_status",
              "current_status.author",
              "current_status.author.name",
              "current_status.color",
              "current_status.created_at",
              "current_status.created_by",
              "current_status.created_by.name",
              "current_status.html_text",
              "current_status.modified_at",
              "current_status.text",
              "current_status.title",
              "current_status_update",
              "current_status_update.resource_subtype",
              "current_status_update.title",
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
              "custom_fields",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.display_value",
              "custom_fields.enabled",
              "custom_fields.enum_options",
              "custom_fields.enum_options.color",
              "custom_fields.enum_options.enabled",
              "custom_fields.enum_options.name",
              "custom_fields.enum_value",
              "custom_fields.enum_value.color",
              "custom_fields.enum_value.enabled",
              "custom_fields.enum_value.name",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.representation_type",
              "custom_fields.text_value",
              "custom_fields.type",
              "default_access_level",
              "default_view",
              "due_date",
              "due_on",
              "followers",
              "followers.name",
              "html_notes",
              "icon",
              "members",
              "members.name",
              "minimum_access_level_for_customization",
              "minimum_access_level_for_sharing",
              "modified_at",
              "name",
              "notes",
              "owner",
              "permalink_url",
              "privacy_setting",
              "project_brief",
              "public",
              "start_on",
              "team",
              "team.name",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "archived",
                  "color",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_from_template",
                  "created_from_template.name",
                  "current_status",
                  "current_status.author",
                  "current_status.author.name",
                  "current_status.color",
                  "current_status.created_at",
                  "current_status.created_by",
                  "current_status.created_by.name",
                  "current_status.html_text",
                  "current_status.modified_at",
                  "current_status.text",
                  "current_status.title",
                  "current_status_update",
                  "current_status_update.resource_subtype",
                  "current_status_update.title",
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
                  "custom_fields",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.display_value",
                  "custom_fields.enabled",
                  "custom_fields.enum_options",
                  "custom_fields.enum_options.color",
                  "custom_fields.enum_options.enabled",
                  "custom_fields.enum_options.name",
                  "custom_fields.enum_value",
                  "custom_fields.enum_value.color",
                  "custom_fields.enum_value.enabled",
                  "custom_fields.enum_value.name",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.representation_type",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "default_access_level",
                  "default_view",
                  "due_date",
                  "due_on",
                  "followers",
                  "followers.name",
                  "html_notes",
                  "icon",
                  "members",
                  "members.name",
                  "minimum_access_level_for_customization",
                  "minimum_access_level_for_sharing",
                  "modified_at",
                  "name",
                  "notes",
                  "owner",
                  "permalink_url",
                  "privacy_setting",
                  "project_brief",
                  "public",
                  "start_on",
                  "team",
                  "team.name",
                  "workspace",
                  "workspace.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "The updated fields for the project.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/ProjectUpdateRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully updated the project.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/ProjectResponse"
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
              "projects:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nProject result = client.projects.updateProject(projectGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The updated fields for the project.\nlet project_gid = \"1331\"; // String | Globally unique identifier for the project.\nlet opts = { \n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\"\n};\nprojectsApiInstance.updateProject(body, project_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.updateProject(projectGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The updated fields for the project.\nproject_gid = \"1331\" # str | Globally unique identifier for the project.\nopts = {\n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Update a project\n    api_response = projects_api_instance.update_project(body, project_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->update_project: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.update_project(project_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->updateProject($project_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.update_project(project_gid: 'project_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "delete": {
        "summary": "Delete a project",
        "description": "<b>Required scope: </b><code>projects:delete</code>\n\nA specific, existing project can be deleted by making a DELETE request on\nthe URL for that project.\n\nReturns an empty data record.",
        "tags": [
          "Projects"
        ],
        "operationId": "deleteProject",
        "responses": {
          "200": {
            "description": "Successfully deleted the specified project.",
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
            "oauth2": [
              "projects:delete"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.projects.deleteProject(projectGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet project_gid = \"1331\"; // String | Globally unique identifier for the project.\n\nprojectsApiInstance.deleteProject(project_gid).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.deleteProject(projectGid)\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nproject_gid = \"1331\" # str | Globally unique identifier for the project.\n\n\ntry:\n    # Delete a project\n    api_response = projects_api_instance.delete_project(project_gid)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->delete_project: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.delete_project(project_gid, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->deleteProject($project_gid, array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.delete_project(project_gid: 'project_gid', options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/projects/{project_gid}/duplicate": {
      "post": {
        "summary": "Duplicate a project",
        "description": "<b>Required scope: </b><code>projects:write</code>\n\nCreates and returns a job that will asynchronously handle the duplication.",
        "tags": [
          "Projects"
        ],
        "operationId": "duplicateProject",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "new_graph_export",
              "new_graph_export.completed_at",
              "new_graph_export.created_at",
              "new_graph_export.download_url",
              "new_portfolio",
              "new_portfolio.name",
              "new_project",
              "new_project.name",
              "new_project_template",
              "new_project_template.name",
              "new_resource_export",
              "new_resource_export.completed_at",
              "new_resource_export.created_at",
              "new_resource_export.download_url",
              "new_task",
              "new_task.created_by",
              "new_task.name",
              "new_task.resource_subtype",
              "resource_subtype",
              "status"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "new_graph_export",
                  "new_graph_export.completed_at",
                  "new_graph_export.created_at",
                  "new_graph_export.download_url",
                  "new_portfolio",
                  "new_portfolio.name",
                  "new_project",
                  "new_project.name",
                  "new_project_template",
                  "new_project_template.name",
                  "new_resource_export",
                  "new_resource_export.completed_at",
                  "new_resource_export.created_at",
                  "new_resource_export.download_url",
                  "new_task",
                  "new_task.created_by",
                  "new_task.name",
                  "new_task.resource_subtype",
                  "resource_subtype",
                  "status"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "Describes the duplicate's name and the elements that will be duplicated.",
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/ProjectDuplicateRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully created the job to handle duplication.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/JobResponse"
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
              "projects:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJob result = client.projects.duplicateProject(projectGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet project_gid = \"1331\"; // String | Globally unique identifier for the project.\nlet opts = { \n    'body': {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}, \n    'opt_fields': \"new_graph_export,new_graph_export.completed_at,new_graph_export.created_at,new_graph_export.download_url,new_portfolio,new_portfolio.name,new_project,new_project.name,new_project_template,new_project_template.name,new_resource_export,new_resource_export.completed_at,new_resource_export.created_at,new_resource_export.download_url,new_task,new_task.created_by,new_task.name,new_task.resource_subtype,resource_subtype,status\"\n};\nprojectsApiInstance.duplicateProject(project_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.duplicateProject(projectGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nproject_gid = \"1331\" # str | Globally unique identifier for the project.\nopts = {\n    'body': {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}, # dict | Describes the duplicate's name and the elements that will be duplicated.\n    'opt_fields': \"new_graph_export,new_graph_export.completed_at,new_graph_export.created_at,new_graph_export.download_url,new_portfolio,new_portfolio.name,new_project,new_project.name,new_project_template,new_project_template.name,new_resource_export,new_resource_export.completed_at,new_resource_export.created_at,new_resource_export.download_url,new_task,new_task.created_by,new_task.name,new_task.resource_subtype,resource_subtype,status\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Duplicate a project\n    api_response = projects_api_instance.duplicate_project(project_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->duplicate_project: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.duplicate_project(project_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->duplicateProject($project_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.duplicate_project(project_gid: 'project_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tasks/{task_gid}/projects": {
      "get": {
        "summary": "Get projects a task is in",
        "description": "<b>Required scope: </b><code>projects:read</code>\n\nReturns a compact representation of all of the projects the task is in.",
        "tags": [
          "Projects"
        ],
        "operationId": "getProjectsForTask",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "archived",
              "color",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_from_template",
              "created_from_template.name",
              "current_status",
              "current_status.author",
              "current_status.author.name",
              "current_status.color",
              "current_status.created_at",
              "current_status.created_by",
              "current_status.created_by.name",
              "current_status.html_text",
              "current_status.modified_at",
              "current_status.text",
              "current_status.title",
              "current_status_update",
              "current_status_update.resource_subtype",
              "current_status_update.title",
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
              "custom_fields",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.display_value",
              "custom_fields.enabled",
              "custom_fields.enum_options",
              "custom_fields.enum_options.color",
              "custom_fields.enum_options.enabled",
              "custom_fields.enum_options.name",
              "custom_fields.enum_value",
              "custom_fields.enum_value.color",
              "custom_fields.enum_value.enabled",
              "custom_fields.enum_value.name",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.representation_type",
              "custom_fields.text_value",
              "custom_fields.type",
              "default_access_level",
              "default_view",
              "due_date",
              "due_on",
              "followers",
              "followers.name",
              "html_notes",
              "icon",
              "members",
              "members.name",
              "minimum_access_level_for_customization",
              "minimum_access_level_for_sharing",
              "modified_at",
              "name",
              "notes",
              "offset",
              "owner",
              "path",
              "permalink_url",
              "privacy_setting",
              "project_brief",
              "public",
              "start_on",
              "team",
              "team.name",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "archived",
                  "color",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_from_template",
                  "created_from_template.name",
                  "current_status",
                  "current_status.author",
                  "current_status.author.name",
                  "current_status.color",
                  "current_status.created_at",
                  "current_status.created_by",
                  "current_status.created_by.name",
                  "current_status.html_text",
                  "current_status.modified_at",
                  "current_status.text",
                  "current_status.title",
                  "current_status_update",
                  "current_status_update.resource_subtype",
                  "current_status_update.title",
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
                  "custom_fields",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.display_value",
                  "custom_fields.enabled",
                  "custom_fields.enum_options",
                  "custom_fields.enum_options.color",
                  "custom_fields.enum_options.enabled",
                  "custom_fields.enum_options.name",
                  "custom_fields.enum_value",
                  "custom_fields.enum_value.color",
                  "custom_fields.enum_value.enabled",
                  "custom_fields.enum_value.name",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.representation_type",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "default_access_level",
                  "default_view",
                  "due_date",
                  "due_on",
                  "followers",
                  "followers.name",
                  "html_notes",
                  "icon",
                  "members",
                  "members.name",
                  "minimum_access_level_for_customization",
                  "minimum_access_level_for_sharing",
                  "modified_at",
                  "name",
                  "notes",
                  "offset",
                  "owner",
                  "path",
                  "permalink_url",
                  "privacy_setting",
                  "project_brief",
                  "public",
                  "start_on",
                  "team",
                  "team.name",
                  "uri",
                  "workspace",
                  "workspace.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Successfully retrieved the projects for the given task.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/ProjectCompact"
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
              "projects:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Project> result = client.projects.getProjectsForTask(taskGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet task_gid = \"321654\"; // String | The task to operate on.\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name\"\n};\nprojectsApiInstance.getProjectsForTask(task_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.getProjectsForTask(taskGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\ntask_gid = \"321654\" # str | The task to operate on.\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get projects a task is in\n    api_response = projects_api_instance.get_projects_for_task(task_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->get_projects_for_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.get_projects_for_task(task_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->getProjectsForTask($task_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.get_projects_for_task(task_gid: 'task_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/teams/{team_gid}/projects": {
      "get": {
        "summary": "Get a team's projects",
        "description": "<b>Required scope: </b><code>projects:read</code>\n\nReturns the compact project records for all projects in the team.",
        "tags": [
          "Projects"
        ],
        "operationId": "getProjectsForTeam",
        "parameters": [
          {
            "$ref": "#/components/parameters/limit"
          },
          {
            "$ref": "#/components/parameters/offset"
          },
          {
            "$ref": "#/components/parameters/archived_query_param"
          },
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "archived",
              "color",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_from_template",
              "created_from_template.name",
              "current_status",
              "current_status.author",
              "current_status.author.name",
              "current_status.color",
              "current_status.created_at",
              "current_status.created_by",
              "current_status.created_by.name",
              "current_status.html_text",
              "current_status.modified_at",
              "current_status.text",
              "current_status.title",
              "current_status_update",
              "current_status_update.resource_subtype",
              "current_status_update.title",
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
              "custom_fields",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.display_value",
              "custom_fields.enabled",
              "custom_fields.enum_options",
              "custom_fields.enum_options.color",
              "custom_fields.enum_options.enabled",
              "custom_fields.enum_options.name",
              "custom_fields.enum_value",
              "custom_fields.enum_value.color",
              "custom_fields.enum_value.enabled",
              "custom_fields.enum_value.name",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.representation_type",
              "custom_fields.text_value",
              "custom_fields.type",
              "default_access_level",
              "default_view",
              "due_date",
              "due_on",
              "followers",
              "followers.name",
              "html_notes",
              "icon",
              "members",
              "members.name",
              "minimum_access_level_for_customization",
              "minimum_access_level_for_sharing",
              "modified_at",
              "name",
              "notes",
              "offset",
              "owner",
              "path",
              "permalink_url",
              "privacy_setting",
              "project_brief",
              "public",
              "start_on",
              "team",
              "team.name",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "archived",
                  "color",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_from_template",
                  "created_from_template.name",
                  "current_status",
                  "current_status.author",
                  "current_status.author.name",
                  "current_status.color",
                  "current_status.created_at",
                  "current_status.created_by",
                  "current_status.created_by.name",
                  "current_status.html_text",
                  "current_status.modified_at",
                  "current_status.text",
                  "current_status.title",
                  "current_status_update",
                  "current_status_update.resource_subtype",
                  "current_status_update.title",
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
                  "custom_fields",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.display_value",
                  "custom_fields.enabled",
                  "custom_fields.enum_options",
                  "custom_fields.enum_options.color",
                  "custom_fields.enum_options.enabled",
                  "custom_fields.enum_options.name",
                  "custom_fields.enum_value",
                  "custom_fields.enum_value.color",
                  "custom_fields.enum_value.enabled",
                  "custom_fields.enum_value.name",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.representation_type",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "default_access_level",
                  "default_view",
                  "due_date",
                  "due_on",
                  "followers",
                  "followers.name",
                  "html_notes",
                  "icon",
                  "members",
                  "members.name",
                  "minimum_access_level_for_customization",
                  "minimum_access_level_for_sharing",
                  "modified_at",
                  "name",
                  "notes",
                  "offset",
                  "owner",
                  "path",
                  "permalink_url",
                  "privacy_setting",
                  "project_brief",
                  "public",
                  "start_on",
                  "team",
                  "team.name",
                  "uri",
                  "workspace",
                  "workspace.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Successfully retrieved the requested team's projects.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/ProjectCompact"
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
              "projects:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Project> result = client.projects.getProjectsForTeam(teamGid, archived)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet team_gid = \"159874\"; // String | Globally unique identifier for the team.\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'archived': false, \n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name\"\n};\nprojectsApiInstance.getProjectsForTeam(team_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.getProjectsForTeam(teamGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nteam_gid = \"159874\" # str | Globally unique identifier for the team.\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'archived': False, # bool | Only return projects whose `archived` field takes on the value of this parameter.\n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get a team's projects\n    api_response = projects_api_instance.get_projects_for_team(team_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->get_projects_for_team: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.get_projects_for_team(team_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->getProjectsForTeam($team_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.get_projects_for_team(team_gid: 'team_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "post": {
        "summary": "Create a project in a team",
        "description": "<b>Required scope: </b><code>projects:write</code>\n\nCreates a project shared with the given team.\n\nReturns the full record of the newly created project.",
        "tags": [
          "Projects"
        ],
        "operationId": "createProjectForTeam",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "archived",
              "color",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_from_template",
              "created_from_template.name",
              "current_status",
              "current_status.author",
              "current_status.author.name",
              "current_status.color",
              "current_status.created_at",
              "current_status.created_by",
              "current_status.created_by.name",
              "current_status.html_text",
              "current_status.modified_at",
              "current_status.text",
              "current_status.title",
              "current_status_update",
              "current_status_update.resource_subtype",
              "current_status_update.title",
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
              "custom_fields",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.display_value",
              "custom_fields.enabled",
              "custom_fields.enum_options",
              "custom_fields.enum_options.color",
              "custom_fields.enum_options.enabled",
              "custom_fields.enum_options.name",
              "custom_fields.enum_value",
              "custom_fields.enum_value.color",
              "custom_fields.enum_value.enabled",
              "custom_fields.enum_value.name",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.representation_type",
              "custom_fields.text_value",
              "custom_fields.type",
              "default_access_level",
              "default_view",
              "due_date",
              "due_on",
              "followers",
              "followers.name",
              "html_notes",
              "icon",
              "members",
              "members.name",
              "minimum_access_level_for_customization",
              "minimum_access_level_for_sharing",
              "modified_at",
              "name",
              "notes",
              "owner",
              "permalink_url",
              "privacy_setting",
              "project_brief",
              "public",
              "start_on",
              "team",
              "team.name",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "archived",
                  "color",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_from_template",
                  "created_from_template.name",
                  "current_status",
                  "current_status.author",
                  "current_status.author.name",
                  "current_status.color",
                  "current_status.created_at",
                  "current_status.created_by",
                  "current_status.created_by.name",
                  "current_status.html_text",
                  "current_status.modified_at",
                  "current_status.text",
                  "current_status.title",
                  "current_status_update",
                  "current_status_update.resource_subtype",
                  "current_status_update.title",
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
                  "custom_fields",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.display_value",
                  "custom_fields.enabled",
                  "custom_fields.enum_options",
                  "custom_fields.enum_options.color",
                  "custom_fields.enum_options.enabled",
                  "custom_fields.enum_options.name",
                  "custom_fields.enum_value",
                  "custom_fields.enum_value.color",
                  "custom_fields.enum_value.enabled",
                  "custom_fields.enum_value.name",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.representation_type",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "default_access_level",
                  "default_view",
                  "due_date",
                  "due_on",
                  "followers",
                  "followers.name",
                  "html_notes",
                  "icon",
                  "members",
                  "members.name",
                  "minimum_access_level_for_customization",
                  "minimum_access_level_for_sharing",
                  "modified_at",
                  "name",
                  "notes",
                  "owner",
                  "permalink_url",
                  "privacy_setting",
                  "project_brief",
                  "public",
                  "start_on",
                  "team",
                  "team.name",
                  "workspace",
                  "workspace.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "The new project to create.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/ProjectRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully created the specified project.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/ProjectResponse"
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
              "projects:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nProject result = client.projects.createProjectForTeam(teamGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The new project to create.\nlet team_gid = \"159874\"; // String | Globally unique identifier for the team.\nlet opts = { \n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\"\n};\nprojectsApiInstance.createProjectForTeam(body, team_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.createProjectForTeam(teamGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The new project to create.\nteam_gid = \"159874\" # str | Globally unique identifier for the team.\nopts = {\n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Create a project in a team\n    api_response = projects_api_instance.create_project_for_team(body, team_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->create_project_for_team: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.create_project_for_team(team_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->createProjectForTeam($team_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.create_project_for_team(team_gid: 'team_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/workspaces/{workspace_gid}/projects": {
      "get": {
        "summary": "Get all projects in a workspace",
        "description": "<b>Required scope: </b><code>projects:read</code>\n\nReturns the compact project records for all projects in the workspace.\n*Note: This endpoint may timeout for large domains. To fetch projects shared with a specific team, use `GET /memberships` with `member` set to the team GID and `resource_subtype` set to `project_membership`.*",
        "tags": [
          "Projects"
        ],
        "operationId": "getProjectsForWorkspace",
        "parameters": [
          {
            "$ref": "#/components/parameters/limit"
          },
          {
            "$ref": "#/components/parameters/offset"
          },
          {
            "$ref": "#/components/parameters/archived_query_param"
          },
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "archived",
              "color",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_from_template",
              "created_from_template.name",
              "current_status",
              "current_status.author",
              "current_status.author.name",
              "current_status.color",
              "current_status.created_at",
              "current_status.created_by",
              "current_status.created_by.name",
              "current_status.html_text",
              "current_status.modified_at",
              "current_status.text",
              "current_status.title",
              "current_status_update",
              "current_status_update.resource_subtype",
              "current_status_update.title",
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
              "custom_fields",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.display_value",
              "custom_fields.enabled",
              "custom_fields.enum_options",
              "custom_fields.enum_options.color",
              "custom_fields.enum_options.enabled",
              "custom_fields.enum_options.name",
              "custom_fields.enum_value",
              "custom_fields.enum_value.color",
              "custom_fields.enum_value.enabled",
              "custom_fields.enum_value.name",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.representation_type",
              "custom_fields.text_value",
              "custom_fields.type",
              "default_access_level",
              "default_view",
              "due_date",
              "due_on",
              "followers",
              "followers.name",
              "html_notes",
              "icon",
              "members",
              "members.name",
              "minimum_access_level_for_customization",
              "minimum_access_level_for_sharing",
              "modified_at",
              "name",
              "notes",
              "offset",
              "owner",
              "path",
              "permalink_url",
              "privacy_setting",
              "project_brief",
              "public",
              "start_on",
              "team",
              "team.name",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "archived",
                  "color",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_from_template",
                  "created_from_template.name",
                  "current_status",
                  "current_status.author",
                  "current_status.author.name",
                  "current_status.color",
                  "current_status.created_at",
                  "current_status.created_by",
                  "current_status.created_by.name",
                  "current_status.html_text",
                  "current_status.modified_at",
                  "current_status.text",
                  "current_status.title",
                  "current_status_update",
                  "current_status_update.resource_subtype",
                  "current_status_update.title",
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
                  "custom_fields",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.display_value",
                  "custom_fields.enabled",
                  "custom_fields.enum_options",
                  "custom_fields.enum_options.color",
                  "custom_fields.enum_options.enabled",
                  "custom_fields.enum_options.name",
                  "custom_fields.enum_value",
                  "custom_fields.enum_value.color",
                  "custom_fields.enum_value.enabled",
                  "custom_fields.enum_value.name",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.representation_type",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "default_access_level",
                  "default_view",
                  "due_date",
                  "due_on",
                  "followers",
                  "followers.name",
                  "html_notes",
                  "icon",
                  "members",
                  "members.name",
                  "minimum_access_level_for_customization",
                  "minimum_access_level_for_sharing",
                  "modified_at",
                  "name",
                  "notes",
                  "offset",
                  "owner",
                  "path",
                  "permalink_url",
                  "privacy_setting",
                  "project_brief",
                  "public",
                  "start_on",
                  "team",
                  "team.name",
                  "uri",
                  "workspace",
                  "workspace.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Successfully retrieved the requested workspace's projects.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/ProjectCompact"
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
              "projects:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Project> result = client.projects.getProjectsForWorkspace(workspaceGid, archived)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet workspace_gid = \"12345\"; // String | Globally unique identifier for the workspace or organization.\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'archived': false, \n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name\"\n};\nprojectsApiInstance.getProjectsForWorkspace(workspace_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.getProjectsForWorkspace(workspaceGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nworkspace_gid = \"12345\" # str | Globally unique identifier for the workspace or organization.\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'archived': False, # bool | Only return projects whose `archived` field takes on the value of this parameter.\n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get all projects in a workspace\n    api_response = projects_api_instance.get_projects_for_workspace(workspace_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->get_projects_for_workspace: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.get_projects_for_workspace(workspace_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->getProjectsForWorkspace($workspace_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.get_projects_for_workspace(workspace_gid: 'workspace_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "post": {
        "summary": "Create a project in a workspace",
        "description": "<b>Required scope: </b><code>projects:write</code>\n\nCreates a project in the workspace.\n\nIf the workspace for your project is an organization, you must also\nsupply a team to share the project with.\n\nReturns the full record of the newly created project.",
        "tags": [
          "Projects"
        ],
        "operationId": "createProjectForWorkspace",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "archived",
              "color",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_from_template",
              "created_from_template.name",
              "current_status",
              "current_status.author",
              "current_status.author.name",
              "current_status.color",
              "current_status.created_at",
              "current_status.created_by",
              "current_status.created_by.name",
              "current_status.html_text",
              "current_status.modified_at",
              "current_status.text",
              "current_status.title",
              "current_status_update",
              "current_status_update.resource_subtype",
              "current_status_update.title",
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
              "custom_fields",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.display_value",
              "custom_fields.enabled",
              "custom_fields.enum_options",
              "custom_fields.enum_options.color",
              "custom_fields.enum_options.enabled",
              "custom_fields.enum_options.name",
              "custom_fields.enum_value",
              "custom_fields.enum_value.color",
              "custom_fields.enum_value.enabled",
              "custom_fields.enum_value.name",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.representation_type",
              "custom_fields.text_value",
              "custom_fields.type",
              "default_access_level",
              "default_view",
              "due_date",
              "due_on",
              "followers",
              "followers.name",
              "html_notes",
              "icon",
              "members",
              "members.name",
              "minimum_access_level_for_customization",
              "minimum_access_level_for_sharing",
              "modified_at",
              "name",
              "notes",
              "owner",
              "permalink_url",
              "privacy_setting",
              "project_brief",
              "public",
              "start_on",
              "team",
              "team.name",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "archived",
                  "color",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_from_template",
                  "created_from_template.name",
                  "current_status",
                  "current_status.author",
                  "current_status.author.name",
                  "current_status.color",
                  "current_status.created_at",
                  "current_status.created_by",
                  "current_status.created_by.name",
                  "current_status.html_text",
                  "current_status.modified_at",
                  "current_status.text",
                  "current_status.title",
                  "current_status_update",
                  "current_status_update.resource_subtype",
                  "current_status_update.title",
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
                  "custom_fields",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.display_value",
                  "custom_fields.enabled",
                  "custom_fields.enum_options",
                  "custom_fields.enum_options.color",
                  "custom_fields.enum_options.enabled",
                  "custom_fields.enum_options.name",
                  "custom_fields.enum_value",
                  "custom_fields.enum_value.color",
                  "custom_fields.enum_value.enabled",
                  "custom_fields.enum_value.name",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.representation_type",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "default_access_level",
                  "default_view",
                  "due_date",
                  "due_on",
                  "followers",
                  "followers.name",
                  "html_notes",
                  "icon",
                  "members",
                  "members.name",
                  "minimum_access_level_for_customization",
                  "minimum_access_level_for_sharing",
                  "modified_at",
                  "name",
                  "notes",
                  "owner",
                  "permalink_url",
                  "privacy_setting",
                  "project_brief",
                  "public",
                  "start_on",
                  "team",
                  "team.name",
                  "workspace",
                  "workspace.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "The new project to create.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/ProjectRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully created a new project in the specified workspace.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/ProjectResponse"
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
              "projects:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nProject result = client.projects.createProjectForWorkspace(workspaceGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The new project to create.\nlet workspace_gid = \"12345\"; // String | Globally unique identifier for the workspace or organization.\nlet opts = { \n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\"\n};\nprojectsApiInstance.createProjectForWorkspace(body, workspace_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.createProjectForWorkspace(workspaceGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The new project to create.\nworkspace_gid = \"12345\" # str | Globally unique identifier for the workspace or organization.\nopts = {\n    'opt_fields': \"archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.input_restrictions,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.reference_value,custom_field_settings.custom_field.reference_value.name,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Create a project in a workspace\n    api_response = projects_api_instance.create_project_for_workspace(body, workspace_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->create_project_for_workspace: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.create_project_for_workspace(workspace_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->createProjectForWorkspace($workspace_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.create_project_for_workspace(workspace_gid: 'workspace_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/projects/{project_gid}/addCustomFieldSetting": {
      "post": {
        "summary": "Add a custom field to a project",
        "description": "<b>Required scope: </b><code>projects:write</code>\n\nCustom fields are associated with projects by way of custom field settings.  This method creates a setting for the project.",
        "tags": [
          "Projects"
        ],
        "operationId": "addCustomFieldSettingForProject",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "custom_field",
              "custom_field.asana_created_field",
              "custom_field.created_by",
              "custom_field.created_by.name",
              "custom_field.currency_code",
              "custom_field.custom_label",
              "custom_field.custom_label_position",
              "custom_field.date_value",
              "custom_field.date_value.date",
              "custom_field.date_value.date_time",
              "custom_field.default_access_level",
              "custom_field.description",
              "custom_field.display_value",
              "custom_field.enabled",
              "custom_field.enum_options",
              "custom_field.enum_options.color",
              "custom_field.enum_options.enabled",
              "custom_field.enum_options.name",
              "custom_field.enum_value",
              "custom_field.enum_value.color",
              "custom_field.enum_value.enabled",
              "custom_field.enum_value.name",
              "custom_field.format",
              "custom_field.has_notifications_enabled",
              "custom_field.id_prefix",
              "custom_field.input_restrictions",
              "custom_field.is_formula_field",
              "custom_field.is_global_to_workspace",
              "custom_field.is_value_read_only",
              "custom_field.multi_enum_values",
              "custom_field.multi_enum_values.color",
              "custom_field.multi_enum_values.enabled",
              "custom_field.multi_enum_values.name",
              "custom_field.name",
              "custom_field.number_value",
              "custom_field.people_value",
              "custom_field.people_value.name",
              "custom_field.precision",
              "custom_field.privacy_setting",
              "custom_field.reference_value",
              "custom_field.reference_value.name",
              "custom_field.representation_type",
              "custom_field.resource_subtype",
              "custom_field.text_value",
              "custom_field.type",
              "is_important",
              "parent",
              "parent.name",
              "project",
              "project.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "custom_field",
                  "custom_field.asana_created_field",
                  "custom_field.created_by",
                  "custom_field.created_by.name",
                  "custom_field.currency_code",
                  "custom_field.custom_label",
                  "custom_field.custom_label_position",
                  "custom_field.date_value",
                  "custom_field.date_value.date",
                  "custom_field.date_value.date_time",
                  "custom_field.default_access_level",
                  "custom_field.description",
                  "custom_field.display_value",
                  "custom_field.enabled",
                  "custom_field.enum_options",
                  "custom_field.enum_options.color",
                  "custom_field.enum_options.enabled",
                  "custom_field.enum_options.name",
                  "custom_field.enum_value",
                  "custom_field.enum_value.color",
                  "custom_field.enum_value.enabled",
                  "custom_field.enum_value.name",
                  "custom_field.format",
                  "custom_field.has_notifications_enabled",
                  "custom_field.id_prefix",
                  "custom_field.input_restrictions",
                  "custom_field.is_formula_field",
                  "custom_field.is_global_to_workspace",
                  "custom_field.is_value_read_only",
                  "custom_field.multi_enum_values",
                  "custom_field.multi_enum_values.color",
                  "custom_field.multi_enum_values.enabled",
                  "custom_field.multi_enum_values.name",
                  "custom_field.name",
                  "custom_field.number_value",
                  "custom_field.people_value",
                  "custom_field.people_value.name",
                  "custom_field.precision",
                  "custom_field.privacy_setting",
                  "custom_field.reference_value",
                  "custom_field.reference_value.name",
                  "custom_field.representation_type",
                  "custom_field.resource_subtype",
                  "custom_field.text_value",
                  "custom_field.type",
                  "is_important",
                  "parent",
                  "parent.name",
                  "project",
                  "project.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "Information about the custom field setting.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/AddCustomFieldSettingRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully added the custom field to the project.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/CustomFieldSettingResponse"
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
              "projects:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nCustomFieldSetting result = client.projects.addCustomFieldSettingForProject(projectGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | Information about the custom field setting.\nlet project_gid = \"1331\"; // String | Globally unique identifier for the project.\nlet opts = { \n    'opt_fields': \"custom_field,custom_field.asana_created_field,custom_field.created_by,custom_field.created_by.name,custom_field.currency_code,custom_field.custom_label,custom_field.custom_label_position,custom_field.date_value,custom_field.date_value.date,custom_field.date_value.date_time,custom_field.default_access_level,custom_field.description,custom_field.display_value,custom_field.enabled,custom_field.enum_options,custom_field.enum_options.color,custom_field.enum_options.enabled,custom_field.enum_options.name,custom_field.enum_value,custom_field.enum_value.color,custom_field.enum_value.enabled,custom_field.enum_value.name,custom_field.format,custom_field.has_notifications_enabled,custom_field.id_prefix,custom_field.input_restrictions,custom_field.is_formula_field,custom_field.is_global_to_workspace,custom_field.is_value_read_only,custom_field.multi_enum_values,custom_field.multi_enum_values.color,custom_field.multi_enum_values.enabled,custom_field.multi_enum_values.name,custom_field.name,custom_field.number_value,custom_field.people_value,custom_field.people_value.name,custom_field.precision,custom_field.privacy_setting,custom_field.reference_value,custom_field.reference_value.name,custom_field.representation_type,custom_field.resource_subtype,custom_field.text_value,custom_field.type,is_important,parent,parent.name,project,project.name\"\n};\nprojectsApiInstance.addCustomFieldSettingForProject(body, project_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.addCustomFieldSettingForProject(projectGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | Information about the custom field setting.\nproject_gid = \"1331\" # str | Globally unique identifier for the project.\nopts = {\n    'opt_fields': \"custom_field,custom_field.asana_created_field,custom_field.created_by,custom_field.created_by.name,custom_field.currency_code,custom_field.custom_label,custom_field.custom_label_position,custom_field.date_value,custom_field.date_value.date,custom_field.date_value.date_time,custom_field.default_access_level,custom_field.description,custom_field.display_value,custom_field.enabled,custom_field.enum_options,custom_field.enum_options.color,custom_field.enum_options.enabled,custom_field.enum_options.name,custom_field.enum_value,custom_field.enum_value.color,custom_field.enum_value.enabled,custom_field.enum_value.name,custom_field.format,custom_field.has_notifications_enabled,custom_field.id_prefix,custom_field.input_restrictions,custom_field.is_formula_field,custom_field.is_global_to_workspace,custom_field.is_value_read_only,custom_field.multi_enum_values,custom_field.multi_enum_values.color,custom_field.multi_enum_values.enabled,custom_field.multi_enum_values.name,custom_field.name,custom_field.number_value,custom_field.people_value,custom_field.people_value.name,custom_field.precision,custom_field.privacy_setting,custom_field.reference_value,custom_field.reference_value.name,custom_field.representation_type,custom_field.resource_subtype,custom_field.text_value,custom_field.type,is_important,parent,parent.name,project,project.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Add a custom field to a project\n    api_response = projects_api_instance.add_custom_field_setting_for_project(body, project_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->add_custom_field_setting_for_project: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.add_custom_field_setting_for_project(project_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->addCustomFieldSettingForProject($project_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.add_custom_field_setting_for_project(project_gid: 'project_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/projects/{project_gid}/removeCustomFieldSetting": {
      "post": {
        "summary": "Remove a custom field from a project",
        "description": "<b>Required scope: </b><code>projects:write</code>\n\nRemoves a custom field setting from a project.",
        "tags": [
          "Projects"
        ],
        "operationId": "removeCustomFieldSettingForProject",
        "security": [
          {
            "personalAccessToken": []
          },
          {
            "oauth2": [
              "projects:write"
            ]
          }
        ],
        "requestBody": {
          "description": "Information about the custom field setting being removed.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/RemoveCustomFieldSettingRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully removed the custom field from the project.",
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
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.projects.removeCustomFieldSettingForProject(projectGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | Information about the custom field setting being removed.\nlet project_gid = \"1331\"; // String | Globally unique identifier for the project.\n\nprojectsApiInstance.removeCustomFieldSettingForProject(body, project_gid).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.removeCustomFieldSettingForProject(projectGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | Information about the custom field setting being removed.\nproject_gid = \"1331\" # str | Globally unique identifier for the project.\n\n\ntry:\n    # Remove a custom field from a project\n    api_response = projects_api_instance.remove_custom_field_setting_for_project(body, project_gid)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->remove_custom_field_setting_for_project: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.remove_custom_field_setting_for_project(project_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->removeCustomFieldSettingForProject($project_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.remove_custom_field_setting_for_project(project_gid: 'project_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/projects/{project_gid}/saveAsTemplate": {
      "post": {
        "summary": "Create a project template from a project",
        "description": "Creates and returns a job that will asynchronously handle the project template creation.",
        "tags": [
          "Projects"
        ],
        "operationId": "projectSaveAsTemplate",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "new_graph_export",
              "new_graph_export.completed_at",
              "new_graph_export.created_at",
              "new_graph_export.download_url",
              "new_portfolio",
              "new_portfolio.name",
              "new_project",
              "new_project.name",
              "new_project_template",
              "new_project_template.name",
              "new_resource_export",
              "new_resource_export.completed_at",
              "new_resource_export.created_at",
              "new_resource_export.download_url",
              "new_task",
              "new_task.created_by",
              "new_task.name",
              "new_task.resource_subtype",
              "resource_subtype",
              "status"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "new_graph_export",
                  "new_graph_export.completed_at",
                  "new_graph_export.created_at",
                  "new_graph_export.download_url",
                  "new_portfolio",
                  "new_portfolio.name",
                  "new_project",
                  "new_project.name",
                  "new_project_template",
                  "new_project_template.name",
                  "new_resource_export",
                  "new_resource_export.completed_at",
                  "new_resource_export.created_at",
                  "new_resource_export.download_url",
                  "new_task",
                  "new_task.created_by",
                  "new_task.name",
                  "new_task.resource_subtype",
                  "resource_subtype",
                  "status"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "Describes the inputs used for creating a project template, such as the resulting project template's name, which team it should be created in.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/ProjectSaveAsTemplateRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully created the job to handle project template creation.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/JobResponse"
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
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJob result = client.projects.projectSaveAsTemplate(projectGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet projectsApiInstance = new Asana.ProjectsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | Describes the inputs used for creating a project template, such as the resulting project template's name, which team it should be created in.\nlet project_gid = \"1331\"; // String | Globally unique identifier for the project.\nlet opts = { \n    'opt_fields': \"new_graph_export,new_graph_export.completed_at,new_graph_export.created_at,new_graph_export.download_url,new_portfolio,new_portfolio.name,new_project,new_project.name,new_project_template,new_project_template.name,new_resource_export,new_resource_export.completed_at,new_resource_export.created_at,new_resource_export.download_url,new_task,new_task.created_by,new_task.name,new_task.resource_subtype,resource_subtype,status\"\n};\nprojectsApiInstance.projectSaveAsTemplate(body, project_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.projects.projectSaveAsTemplate(projectGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nprojects_api_instance = asana.ProjectsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | Describes the inputs used for creating a project template, such as the resulting project template's name, which team it should be created in.\nproject_gid = \"1331\" # str | Globally unique identifier for the project.\nopts = {\n    'opt_fields': \"new_graph_export,new_graph_export.completed_at,new_graph_export.created_at,new_graph_export.download_url,new_portfolio,new_portfolio.name,new_project,new_project.name,new_project_template,new_project_template.name,new_resource_export,new_resource_export.completed_at,new_resource_export.created_at,new_resource_export.download_url,new_task,new_task.created_by,new_task.name,new_task.resource_subtype,resource_subtype,status\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Create a project template from a project\n    api_response = projects_api_instance.project_save_as_template(body, project_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling ProjectsApi->project_save_as_template: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.projects.project_save_as_template(project_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->projects->projectSaveAsTemplate($project_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.projects.project_save_as_template(project_gid: 'project_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    }
  },
  "schemas": {
    "ProjectResponse": {
      "allOf": [
        {
          "$ref": "#/components/schemas/ProjectBase"
        },
        {
          "type": "object",
          "properties": {
            "custom_fields": {
              "description": "Array of custom field values applied directly to the project itself. These represent the values set on the project, not the fields available for tasks in the project.",
              "readOnly": true,
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/CustomFieldCompact"
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
                  "$ref": "#/components/schemas/UserCompact"
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
                "$ref": "#/components/schemas/UserCompact"
              },
              "readOnly": true
            },
            "owner": {
              "description": "The current owner of the project, may be null.",
              "allOf": [
                {
                  "$ref": "#/components/schemas/UserCompact"
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
                  "$ref": "#/components/schemas/TeamCompact"
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
                  "$ref": "#/components/schemas/ProjectBriefCompact"
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
                  "$ref": "#/components/schemas/ProjectTemplateCompact"
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
                  "$ref": "#/components/schemas/WorkspaceCompact"
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
    "ProjectSaveAsTemplateRequest": {
      "type": "object",
      "required": [
        "name",
        "public"
      ],
      "properties": {
        "name": {
          "description": "The name of the new project template.",
          "type": "string",
          "example": "New Project Template"
        },
        "team": {
          "description": "Sets the team of the new project template. If the project exists in an organization, specify team and not workspace.",
          "type": "string",
          "example": "12345"
        },
        "workspace": {
          "description": "Sets the workspace of the new project template. Only specify workspace if the project exists in a workspace.",
          "type": "string",
          "example": "12345"
        },
        "public": {
          "description": "Sets the project template to public to its team.",
          "type": "boolean",
          "example": true
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
    "ProjectBase": {
      "allOf": [
        {
          "$ref": "#/components/schemas/ProjectCompact"
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
                  "$ref": "#/components/schemas/ProjectStatusResponse"
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
                  "$ref": "#/components/schemas/StatusUpdateCompact"
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
                "$ref": "#/components/schemas/CustomFieldSettingResponse"
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
                "$ref": "#/components/schemas/UserCompact"
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
    "RemoveCustomFieldSettingRequest": {
      "type": "object",
      "required": [
        "custom_field"
      ],
      "properties": {
        "custom_field": {
          "description": "The custom field to remove from this portfolio.",
          "type": "string",
          "example": "14916"
        }
      }
    },
    "ProjectStatusResponse": {
      "allOf": [
        {
          "$ref": "#/components/schemas/ProjectStatusBase"
        },
        {
          "type": "object",
          "properties": {
            "author": {
              "$ref": "#/components/schemas/UserCompact"
            },
            "created_at": {
              "description": "The time at which this resource was created.",
              "type": "string",
              "format": "date-time",
              "readOnly": true,
              "example": "2012-02-22T02:06:58.147Z"
            },
            "created_by": {
              "$ref": "#/components/schemas/UserCompact"
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
    "CustomFieldCreateRequest": {
      "allOf": [
        {
          "$ref": "#/components/schemas/CustomFieldRequest"
        },
        {
          "type": "object",
          "required": [
            "resource_subtype"
          ],
          "properties": {
            "resource_subtype": {
              "description": "The type of the custom field. Must be one of the given values.",
              "type": "string",
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
    "JobResponse": {
      "$ref": "#/components/schemas/JobBase"
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
          "$ref": "#/components/schemas/PortfolioCompact"
        },
        "new_project": {
          "$ref": "#/components/schemas/ProjectCompact"
        },
        "new_task": {
          "allOf": [
            {
              "$ref": "#/components/schemas/TaskCompact"
            },
            {
              "type": "object",
              "nullable": true
            }
          ]
        },
        "new_project_template": {
          "$ref": "#/components/schemas/ProjectTemplateCompact"
        },
        "new_graph_export": {
          "$ref": "#/components/schemas/GraphExportCompact"
        },
        "new_resource_export": {
          "$ref": "#/components/schemas/ResourceExportCompact"
        }
      }
    },
    "AddCustomFieldSettingRequest": {
      "type": "object",
      "required": [
        "custom_field"
      ],
      "properties": {
        "custom_field": {
          "oneOf": [
            {
              "type": "string",
              "description": "The custom field to associate with this container.",
              "example": "14916"
            },
            {
              "$ref": "#/components/schemas/CustomFieldCreateRequest"
            }
          ]
        },
        "is_important": {
          "description": "Whether this field should be considered important to this container (for instance, to display in the list view of items in the container).",
          "type": "boolean",
          "example": true
        },
        "insert_before": {
          "description": "A gid of a Custom Field Setting on this container, before which the new Custom Field Setting will be added.  `insert_before` and `insert_after` parameters cannot both be specified.",
          "type": "string",
          "example": "1331"
        },
        "insert_after": {
          "description": "A gid of a Custom Field Setting on this container, after which the new Custom Field Setting will be added.  `insert_before` and `insert_after` parameters cannot both be specified.",
          "type": "string",
          "example": "1331"
        }
      }
    },
    "EmptyResponse": {
      "type": "object",
      "description": "An empty object. Some endpoints do not return an object on success. The success is conveyed through a 2-- status code and returning an empty object."
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
    "CustomFieldRequest": {
      "allOf": [
        {
          "$ref": "#/components/schemas/CustomFieldBase"
        },
        {
          "type": "object",
          "required": [
            "workspace"
          ],
          "properties": {
            "workspace": {
              "type": "string",
              "description": "*Create-Only* The workspace to create a custom field in.",
              "example": "1331"
            },
            "owned_by_app": {
              "type": "boolean",
              "description": "*Allow-listed*. Instructs the API that this Custom Field is app-owned. This parameter is allow-listed to specific apps at this point in time. For apps that are not allow-listed, providing this parameter will result in a `403 Forbidden`."
            },
            "people_value": {
              "description": "*Conditional*. Only relevant for custom fields of type `people`. This array of user GIDs, emails, or the string \"me\", reflects the users to be written to a `people` custom field. Note that *write* operations will replace existing users (if any) in the custom field with the users specified in this array.",
              "type": "array",
              "items": {
                "type": "string",
                "description": "A string identifying a user. This can either be the string \"me\", an email, or the gid of a user."
              },
              "example": [
                "12345"
              ]
            },
            "reference_value": {
              "description": "*Conditional*. Only relevant for custom fields of type `reference`. This array of GIDs reflects the objects to be written to a `reference` custom field. Note that *write* operations will replace existing objects (if any) in the custom field with the objects specified in this array.",
              "type": "array",
              "items": {
                "type": "string",
                "description": "The GID of an object."
              },
              "example": [
                "12345"
              ]
            }
          }
        }
      ]
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
    "ProjectUpdateRequest": {
      "allOf": [
        {
          "$ref": "#/components/schemas/ProjectBase"
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
    "ProjectStatusBase": {
      "allOf": [
        {
          "$ref": "#/components/schemas/ProjectStatusCompact"
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
    "ProjectRequest": {
      "allOf": [
        {
          "$ref": "#/components/schemas/ProjectBase"
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
    "JobBase": {
      "$ref": "#/components/schemas/JobCompact"
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
    }
  },
  "primary_response_schema": {
    "type": "object",
    "properties": {
      "data": {
        "$ref": "#/components/schemas/ProjectResponse"
      }
    }
  }
}
```

### Relationship manifest

```yaml
asana_projects:
  parent_id:
    target_table: asana_projects
    target_column: id
    confidence: high
    reason: 'response schema: data.custom_field_settings[].parent.gid'
  team_id:
    target_table: asana_teams
    target_column: id
    confidence: high
    reason: 'response schema: data.team.gid'
  workspace_id:
    target_table: asana_workspaces
    target_column: id
    confidence: high
    reason: 'response schema: data.workspace.gid'

```

### FK dependency schemas (for stub creation if needed)

```json
{
  "teams": {
    "primary_response_schema": {
      "type": "object",
      "properties": {
        "data": {
          "$ref": "#/components/schemas/TeamResponse"
        }
      }
    }
  },
  "workspaces": {
    "primary_response_schema": {
      "type": "object",
      "properties": {
        "data": {
          "$ref": "#/components/schemas/WorkspaceResponse"
        }
      }
    }
  }
}
```

### ID format

Resource `project` uses: alphabet=ALPHANUMERIC, length=16

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

Add a class `Project(Base)` with:

- Table name: `asana_projects`
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
