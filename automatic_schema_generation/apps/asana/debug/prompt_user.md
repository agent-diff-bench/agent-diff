# Entity Implementation: users

You are implementing the **users** resource for the Asana API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for users

```json
{
  "paths": {
    "/users/{user_gid}/user_task_list": {
      "get": {
        "summary": "Get a user's task list",
        "description": "<b>Required scope: </b><code>tasks:read</code>\n\nReturns the full record for a user's task list.",
        "tags": [
          "User task lists"
        ],
        "operationId": "getUserTaskListForUser",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "name",
              "owner",
              "workspace"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "name",
                  "owner",
                  "workspace"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Successfully retrieved the user's task list.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/UserTaskListResponse"
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
              "tasks:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nUserTaskList result = client.usertasklists.getUserTaskListForUser(userGid, workspace)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet userTaskListsApiInstance = new Asana.UserTaskListsApi(client);\nlet user_gid = \"me\"; // String | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nlet workspace = \"1234\"; // String | The workspace in which to get the user task list.\nlet opts = { \n    'opt_fields': \"name,owner,workspace\"\n};\nuserTaskListsApiInstance.getUserTaskListForUser(user_gid, workspace, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.usertasklists.getUserTaskListForUser(userGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nuser_task_lists_api_instance = asana.UserTaskListsApi(api_client)\nuser_gid = \"me\" # str | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nworkspace = \"1234\" # str | The workspace in which to get the user task list.\nopts = {\n    'opt_fields': \"name,owner,workspace\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get a user's task list\n    api_response = user_task_lists_api_instance.get_user_task_list_for_user(user_gid, workspace, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling UserTaskListsApi->get_user_task_list_for_user: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.user_task_lists.get_user_task_list_for_user(user_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->usertasklists->getUserTaskListForUser($user_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.user_task_lists.get_user_task_list_for_user(user_gid: 'user_gid', workspace: '&#x27;workspace_example&#x27;', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/users": {
      "get": {
        "summary": "Get multiple users",
        "description": "<b>Required scope: </b><code>users:read</code>\n\nReturns the user records for all users in all workspaces and organizations accessible to the authenticated user. Accepts an optional workspace ID parameter.\nResults are sorted by user ID.",
        "tags": [
          "Users"
        ],
        "operationId": "getUsers",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
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
              "email",
              "name",
              "offset",
              "path",
              "photo",
              "photo.image_1024x1024",
              "photo.image_128x128",
              "photo.image_21x21",
              "photo.image_27x27",
              "photo.image_36x36",
              "photo.image_60x60",
              "uri",
              "workspaces",
              "workspaces.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
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
                  "email",
                  "name",
                  "offset",
                  "path",
                  "photo",
                  "photo.image_1024x1024",
                  "photo.image_128x128",
                  "photo.image_21x21",
                  "photo.image_27x27",
                  "photo.image_36x36",
                  "photo.image_60x60",
                  "uri",
                  "workspaces",
                  "workspaces.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Successfully retrieved the requested user records.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/UserCompact"
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
              "users:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<User> result = client.users.getUsers(team, workspace)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet usersApiInstance = new Asana.UsersApi(client);\nlet opts = { \n    'workspace': \"1331\", \n    'team': \"15627\", \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,offset,path,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,uri,workspaces,workspaces.name\"\n};\nusersApiInstance.getUsers(opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.users.getUsers({param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nusers_api_instance = asana.UsersApi(api_client)\nopts = {\n    'workspace': \"1331\", # str | The workspace or organization ID to filter users on.\n    'team': \"15627\", # str | The team ID to filter users on.\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,offset,path,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,uri,workspaces,workspaces.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get multiple users\n    api_response = users_api_instance.get_users(opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling UsersApi->get_users: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.users.get_users({'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->users->getUsers(array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.users.get_users(param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/users/{user_gid}": {
      "get": {
        "summary": "Get a user",
        "description": "<b>Required scope: </b><code>users:read</code>\n\nReturns the full user record for the single user with the provided ID.",
        "tags": [
          "Users"
        ],
        "operationId": "getUser",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
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
              "email",
              "name",
              "photo",
              "photo.image_1024x1024",
              "photo.image_128x128",
              "photo.image_21x21",
              "photo.image_27x27",
              "photo.image_36x36",
              "photo.image_60x60",
              "workspaces",
              "workspaces.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
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
                  "email",
                  "name",
                  "photo",
                  "photo.image_1024x1024",
                  "photo.image_128x128",
                  "photo.image_21x21",
                  "photo.image_27x27",
                  "photo.image_36x36",
                  "photo.image_60x60",
                  "workspaces",
                  "workspaces.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Returns the user specified.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/UserResponse"
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
              "users:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nUser result = client.users.getUser(userGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet usersApiInstance = new Asana.UsersApi(client);\nlet user_gid = \"me\"; // String | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nlet opts = { \n    'workspace': \"12345\", \n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\"\n};\nusersApiInstance.getUser(user_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.users.getUser(userGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nusers_api_instance = asana.UsersApi(api_client)\nuser_gid = \"me\" # str | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nopts = {\n    'workspace': \"12345\", # str | The workspace to filter results on.\n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get a user\n    api_response = users_api_instance.get_user(user_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling UsersApi->get_user: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.users.get_user(user_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->users->getUser($user_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.users.get_user(user_gid: 'user_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "put": {
        "summary": "Update a user",
        "description": "A specific, existing user can be updated by making a PUT request on the\nURL for that user. Only the fields provided in the `data` block will be\nupdated; any unspecified fields will remain unchanged.\n\nReturns the complete updated user record.",
        "tags": [
          "Users"
        ],
        "operationId": "updateUser",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
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
              "email",
              "name",
              "photo",
              "photo.image_1024x1024",
              "photo.image_128x128",
              "photo.image_21x21",
              "photo.image_27x27",
              "photo.image_36x36",
              "photo.image_60x60",
              "workspaces",
              "workspaces.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
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
                  "email",
                  "name",
                  "photo",
                  "photo.image_1024x1024",
                  "photo.image_128x128",
                  "photo.image_21x21",
                  "photo.image_27x27",
                  "photo.image_36x36",
                  "photo.image_60x60",
                  "workspaces",
                  "workspaces.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "The user to update.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/UserUpdateRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully updated the specified user.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/UserResponse"
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
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet usersApiInstance = new Asana.UsersApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The user to update.\nlet user_gid = \"me\"; // String | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nlet opts = { \n    'workspace': \"12345\", \n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\"\n};\nusersApiInstance.updateUser(body, user_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nusers_api_instance = asana.UsersApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The user to update.\nuser_gid = \"me\" # str | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nopts = {\n    'workspace': \"12345\", # str | The workspace to filter results on.\n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Update a user\n    api_response = users_api_instance.update_user(body, user_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling UsersApi->update_user: %s\\n\" % e)",
              "name": "python-sdk-v5"
            }
          ]
        }
      }
    },
    "/teams/{team_gid}/users": {
      "get": {
        "summary": "Get users in a team",
        "description": "<b>Required scope: </b><code>users:read</code>\n\nReturns the compact records for all users that are members of the team.\nResults are sorted alphabetically and limited to 2000. For more results use the `/users` endpoint.",
        "tags": [
          "Users"
        ],
        "operationId": "getUsersForTeam",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
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
              "email",
              "name",
              "photo",
              "photo.image_1024x1024",
              "photo.image_128x128",
              "photo.image_21x21",
              "photo.image_27x27",
              "photo.image_36x36",
              "photo.image_60x60",
              "workspaces",
              "workspaces.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
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
                  "email",
                  "name",
                  "photo",
                  "photo.image_1024x1024",
                  "photo.image_128x128",
                  "photo.image_21x21",
                  "photo.image_27x27",
                  "photo.image_36x36",
                  "photo.image_60x60",
                  "workspaces",
                  "workspaces.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Returns the user records for all the members of the team, including guests and limited access users.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/UserCompact"
                      }
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
              "users:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<User> result = client.users.getUsersForTeam(teamGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet usersApiInstance = new Asana.UsersApi(client);\nlet team_gid = \"159874\"; // String | Globally unique identifier for the team.\nlet opts = { \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\"\n};\nusersApiInstance.getUsersForTeam(team_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.users.getUsersForTeam(teamGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nusers_api_instance = asana.UsersApi(api_client)\nteam_gid = \"159874\" # str | Globally unique identifier for the team.\nopts = {\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get users in a team\n    api_response = users_api_instance.get_users_for_team(team_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling UsersApi->get_users_for_team: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.users.get_users_for_team(team_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->users->getUsersForTeam($team_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.users.get_users_for_team(team_gid: 'team_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/workspaces/{workspace_gid}/users": {
      "get": {
        "summary": "Get users in a workspace or organization",
        "description": "<b>Required scope: </b><code>users:read</code>\n\nReturns the compact records for all users in the specified workspace or organization.\nResults are sorted alphabetically and limited to 2000. For more results use the `/users` endpoint.",
        "tags": [
          "Users"
        ],
        "operationId": "getUsersForWorkspace",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
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
              "email",
              "name",
              "photo",
              "photo.image_1024x1024",
              "photo.image_128x128",
              "photo.image_21x21",
              "photo.image_27x27",
              "photo.image_36x36",
              "photo.image_60x60",
              "workspaces",
              "workspaces.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
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
                  "email",
                  "name",
                  "photo",
                  "photo.image_1024x1024",
                  "photo.image_128x128",
                  "photo.image_21x21",
                  "photo.image_27x27",
                  "photo.image_36x36",
                  "photo.image_60x60",
                  "workspaces",
                  "workspaces.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Return the users in the specified workspace or org.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/UserCompact"
                      }
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
              "users:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<User> result = client.users.getUsersForWorkspace(workspaceGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet usersApiInstance = new Asana.UsersApi(client);\nlet workspace_gid = \"12345\"; // String | Globally unique identifier for the workspace or organization.\nlet opts = { \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\"\n};\nusersApiInstance.getUsersForWorkspace(workspace_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.users.getUsersForWorkspace(workspaceGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nusers_api_instance = asana.UsersApi(api_client)\nworkspace_gid = \"12345\" # str | Globally unique identifier for the workspace or organization.\nopts = {\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get users in a workspace or organization\n    api_response = users_api_instance.get_users_for_workspace(workspace_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling UsersApi->get_users_for_workspace: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.users.get_users_for_workspace(workspace_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->users->getUsersForWorkspace($workspace_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.users.get_users_for_workspace(workspace_gid: 'workspace_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/workspaces/{workspace_gid}/users/{user_gid}": {
      "get": {
        "summary": "Get a user in a workspace or organization",
        "description": "<b>Required scope: </b><code>users:read</code>\n\nReturns the full user record for the single user with the provided ID in the specified workspace or organization.",
        "tags": [
          "Users"
        ],
        "operationId": "getUserForWorkspace",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
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
              "email",
              "name",
              "photo",
              "photo.image_1024x1024",
              "photo.image_128x128",
              "photo.image_21x21",
              "photo.image_27x27",
              "photo.image_36x36",
              "photo.image_60x60",
              "workspaces",
              "workspaces.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
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
                  "email",
                  "name",
                  "photo",
                  "photo.image_1024x1024",
                  "photo.image_128x128",
                  "photo.image_21x21",
                  "photo.image_27x27",
                  "photo.image_36x36",
                  "photo.image_60x60",
                  "workspaces",
                  "workspaces.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "responses": {
          "200": {
            "description": "Returns the user specified.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/UserResponse"
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
              "users:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet usersApiInstance = new Asana.UsersApi(client);\nlet workspace_gid = \"12345\"; // String | Globally unique identifier for the workspace or organization.\nlet user_gid = \"me\"; // String | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nlet opts = { \n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\"\n};\nusersApiInstance.getUserForWorkspace(workspace_gid, user_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nusers_api_instance = asana.UsersApi(api_client)\nworkspace_gid = \"12345\" # str | Globally unique identifier for the workspace or organization.\nuser_gid = \"me\" # str | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nopts = {\n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get a user in a workspace or organization\n    api_response = users_api_instance.get_user_for_workspace(workspace_gid, user_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling UsersApi->get_user_for_workspace: %s\\n\" % e)",
              "name": "python-sdk-v5"
            }
          ]
        }
      },
      "put": {
        "summary": "Update a user in a workspace or organization",
        "description": "An existing user can be updated by making a PUT request on the URL for that user in the specified workspace or organization. Only the fields provided in the `data` block will be updated; any unspecified fields will remain unchanged.",
        "tags": [
          "Users"
        ],
        "operationId": "updateUserForWorkspace",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
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
              "email",
              "name",
              "photo",
              "photo.image_1024x1024",
              "photo.image_128x128",
              "photo.image_21x21",
              "photo.image_27x27",
              "photo.image_36x36",
              "photo.image_60x60",
              "workspaces",
              "workspaces.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
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
                  "email",
                  "name",
                  "photo",
                  "photo.image_1024x1024",
                  "photo.image_128x128",
                  "photo.image_21x21",
                  "photo.image_27x27",
                  "photo.image_36x36",
                  "photo.image_60x60",
                  "workspaces",
                  "workspaces.name"
                ]
              }
            },
            "style": "form",
            "explode": false
          }
        ],
        "requestBody": {
          "description": "The user to update.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/UserUpdateRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully updated the specified user.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/UserResponse"
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
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet usersApiInstance = new Asana.UsersApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The user to update.\nlet workspace_gid = \"12345\"; // String | Globally unique identifier for the workspace or organization.\nlet user_gid = \"me\"; // String | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nlet opts = { \n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\"\n};\nusersApiInstance.updateUserForWorkspace(body, workspace_gid, user_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\nusers_api_instance = asana.UsersApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The user to update.\nworkspace_gid = \"12345\" # str | Globally unique identifier for the workspace or organization.\nuser_gid = \"me\" # str | A string identifying a user. This can either be the string \\\"me\\\", an email, or the gid of a user.\nopts = {\n    'opt_fields': \"custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Update a user in a workspace or organization\n    api_response = users_api_instance.update_user_for_workspace(body, workspace_gid, user_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling UsersApi->update_user_for_workspace: %s\\n\" % e)",
              "name": "python-sdk-v5"
            }
          ]
        }
      }
    }
  },
  "schemas": {
    "UserTaskListBase": {
      "$ref": "#/components/schemas/UserTaskListCompact"
    },
    "UserUpdateRequest": {
      "allOf": [
        {
          "$ref": "#/components/schemas/UserRequest"
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
    "UserTaskListResponse": {
      "$ref": "#/components/schemas/UserTaskListBase"
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
              "$ref": "#/components/schemas/UserCompact"
            }
          ]
        },
        "workspace": {
          "description": "The workspace in which the user task list is located.",
          "readOnly": true,
          "allOf": [
            {
              "$ref": "#/components/schemas/WorkspaceCompact"
            }
          ]
        }
      }
    },
    "UserResponse": {
      "allOf": [
        {
          "$ref": "#/components/schemas/UserBaseResponse"
        },
        {
          "type": "object",
          "properties": {
            "workspaces": {
              "description": "Workspaces and organizations this user may access.\nNote\\: The API will only return workspaces and organizations that also contain the authenticated user.",
              "readOnly": true,
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/WorkspaceCompact"
              }
            },
            "custom_fields": {
              "description": "Array of Custom Fields.",
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/CustomFieldCompact"
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
    },
    "UserBase": {
      "$ref": "#/components/schemas/UserCompact"
    },
    "UserBaseResponse": {
      "allOf": [
        {
          "$ref": "#/components/schemas/UserBase"
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
    "UserRequest": {
      "$ref": "#/components/schemas/UserBase"
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
        "$ref": "#/components/schemas/UserResponse"
      }
    }
  }
}
```

### Relationship manifest

```yaml
# No FK relationships for this resource
```

### FK dependency schemas (for stub creation if needed)

```json
{}
```

### ID format

Resource `user` uses: alphabet=ALPHANUMERIC, length=16

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

Add a class `User(Base)` with:

- Table name: `asana_users`
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
