# Entity Implementation: tags

You are implementing the **tags** resource for the Asana API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for tags

```json
{
  "paths": {
    "/tags": {
      "get": {
        "summary": "Get multiple tags",
        "description": "<b>Required scope: </b><code>tags:read</code>\n\nReturns the compact tag records for some filtered set of tags. Use one or more of the parameters provided to filter the tags returned.",
        "tags": [
          "Tags"
        ],
        "operationId": "getTags",
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
            "description": "The workspace to filter tags on.",
            "schema": {
              "type": "string"
            },
            "example": "1331"
          },
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "color",
              "created_at",
              "followers",
              "followers.name",
              "name",
              "notes",
              "offset",
              "path",
              "permalink_url",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "color",
                  "created_at",
                  "followers",
                  "followers.name",
                  "name",
                  "notes",
                  "offset",
                  "path",
                  "permalink_url",
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
            "description": "Successfully retrieved the specified set of tags.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TagCompact"
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
              "tags:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Tag> result = client.tags.getTags(workspace)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tagsApiInstance = new Asana.TagsApi(client);\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'workspace': \"1331\", \n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,offset,path,permalink_url,uri,workspace,workspace.name\"\n};\ntagsApiInstance.getTags(opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tags.getTags({param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntags_api_instance = asana.TagsApi(api_client)\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'workspace': \"1331\", # str | The workspace to filter tags on.\n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,offset,path,permalink_url,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get multiple tags\n    api_response = tags_api_instance.get_tags(opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TagsApi->get_tags: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tags.get_tags({'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tags->getTags(array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tags.get_tags(param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "post": {
        "summary": "Create a tag",
        "description": "<b>Required scope: </b><code>tags:write</code>\n\nCreates a new tag in a workspace or organization.\n\nEvery tag is required to be created in a specific workspace or\norganization, and this cannot be changed once set. Note that you can use\nthe workspace parameter regardless of whether or not it is an\norganization.\n\nReturns the full record of the newly created tag.",
        "tags": [
          "Tags"
        ],
        "operationId": "createTag",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "color",
              "created_at",
              "followers",
              "followers.name",
              "name",
              "notes",
              "permalink_url",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "color",
                  "created_at",
                  "followers",
                  "followers.name",
                  "name",
                  "notes",
                  "permalink_url",
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
          "description": "The tag to create.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TagCreateRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully created the newly specified tag.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TagResponse"
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
              "tags:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTag result = client.tags.createTag()\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tagsApiInstance = new Asana.TagsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The tag to create.\nlet opts = { \n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,permalink_url,workspace,workspace.name\"\n};\ntagsApiInstance.createTag(body, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tags.createTag({field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntags_api_instance = asana.TagsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The tag to create.\nopts = {\n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,permalink_url,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Create a tag\n    api_response = tags_api_instance.create_tag(body, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TagsApi->create_tag: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tags.create_tag({'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tags->createTag(array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tags.create_tag(field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tags/{tag_gid}": {
      "get": {
        "summary": "Get a tag",
        "description": "<b>Required scope: </b><code>tags:read</code>\n\nReturns the complete tag record for a single tag.",
        "tags": [
          "Tags"
        ],
        "operationId": "getTag",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "color",
              "created_at",
              "followers",
              "followers.name",
              "name",
              "notes",
              "permalink_url",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "color",
                  "created_at",
                  "followers",
                  "followers.name",
                  "name",
                  "notes",
                  "permalink_url",
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
            "description": "Successfully retrieved the specified tag.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TagResponse"
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
              "tags:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTag result = client.tags.getTag(tagGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tagsApiInstance = new Asana.TagsApi(client);\nlet tag_gid = \"11235\"; // String | Globally unique identifier for the tag.\nlet opts = { \n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,permalink_url,workspace,workspace.name\"\n};\ntagsApiInstance.getTag(tag_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tags.getTag(tagGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntags_api_instance = asana.TagsApi(api_client)\ntag_gid = \"11235\" # str | Globally unique identifier for the tag.\nopts = {\n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,permalink_url,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get a tag\n    api_response = tags_api_instance.get_tag(tag_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TagsApi->get_tag: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tags.get_tag(tag_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tags->getTag($tag_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tags.get_tag(tag_gid: 'tag_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "put": {
        "summary": "Update a tag",
        "description": "<b>Required scope: </b><code>tags:write</code>\n\nUpdates the properties of a tag. Only the fields provided in the `data`\nblock will be updated; any unspecified fields will remain unchanged.\n\nWhen using this method, it is best to specify only those fields you wish\nto change, or else you may overwrite changes made by another user since\nyou last retrieved the tag.\n\nReturns the complete updated tag record.",
        "tags": [
          "Tags"
        ],
        "operationId": "updateTag",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "color",
              "created_at",
              "followers",
              "followers.name",
              "name",
              "notes",
              "permalink_url",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "color",
                  "created_at",
                  "followers",
                  "followers.name",
                  "name",
                  "notes",
                  "permalink_url",
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
          "description": "The tag to update.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TagUpdateRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully updated the specified tag.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TagResponse"
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
              "tags:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTag result = client.tags.updateTag(tagGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tagsApiInstance = new Asana.TagsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The tag to update.\nlet tag_gid = \"11235\"; // String | Globally unique identifier for the tag.\nlet opts = { \n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,permalink_url,workspace,workspace.name\"\n};\ntagsApiInstance.updateTag(body, tag_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tags.updateTag(tagGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntags_api_instance = asana.TagsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The tag to update.\ntag_gid = \"11235\" # str | Globally unique identifier for the tag.\nopts = {\n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,permalink_url,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Update a tag\n    api_response = tags_api_instance.update_tag(body, tag_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TagsApi->update_tag: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tags.update_tag(tag_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tags->updateTag($tag_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tags.update_tag(tag_gid: 'tag_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "delete": {
        "summary": "Delete a tag",
        "description": "A specific, existing tag can be deleted by making a DELETE request on\nthe URL for that tag.\n\nReturns an empty data record.",
        "tags": [
          "Tags"
        ],
        "operationId": "deleteTag",
        "responses": {
          "200": {
            "description": "Successfully deleted the specified tag.",
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
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.tags.deleteTag(tagGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tagsApiInstance = new Asana.TagsApi(client);\nlet tag_gid = \"11235\"; // String | Globally unique identifier for the tag.\n\ntagsApiInstance.deleteTag(tag_gid).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tags.deleteTag(tagGid)\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntags_api_instance = asana.TagsApi(api_client)\ntag_gid = \"11235\" # str | Globally unique identifier for the tag.\n\n\ntry:\n    # Delete a tag\n    api_response = tags_api_instance.delete_tag(tag_gid)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TagsApi->delete_tag: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tags.delete_tag(tag_gid, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tags->deleteTag($tag_gid, array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tags.delete_tag(tag_gid: 'tag_gid', options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tasks/{task_gid}/tags": {
      "get": {
        "summary": "Get a task's tags",
        "description": "<b>Required scope: </b><code>tags:read</code>\n\nGet a compact representation of all of the tags the task has.",
        "tags": [
          "Tags"
        ],
        "operationId": "getTagsForTask",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "color",
              "created_at",
              "followers",
              "followers.name",
              "name",
              "notes",
              "offset",
              "path",
              "permalink_url",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "color",
                  "created_at",
                  "followers",
                  "followers.name",
                  "name",
                  "notes",
                  "offset",
                  "path",
                  "permalink_url",
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
            "description": "Successfully retrieved the tags for the given task.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TagCompact"
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
              "tags:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Tag> result = client.tags.getTagsForTask(taskGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tagsApiInstance = new Asana.TagsApi(client);\nlet task_gid = \"321654\"; // String | The task to operate on.\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,offset,path,permalink_url,uri,workspace,workspace.name\"\n};\ntagsApiInstance.getTagsForTask(task_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tags.getTagsForTask(taskGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntags_api_instance = asana.TagsApi(api_client)\ntask_gid = \"321654\" # str | The task to operate on.\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,offset,path,permalink_url,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get a task's tags\n    api_response = tags_api_instance.get_tags_for_task(task_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TagsApi->get_tags_for_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tags.get_tags_for_task(task_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tags->getTagsForTask($task_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tags.get_tags_for_task(task_gid: 'task_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/workspaces/{workspace_gid}/tags": {
      "get": {
        "summary": "Get tags in a workspace",
        "description": "<b>Required scope: </b><code>tags:read</code>\n\nReturns the compact tag records for some filtered set of tags. Use one or more of the parameters provided to filter the tags returned.",
        "tags": [
          "Tags"
        ],
        "operationId": "getTagsForWorkspace",
        "parameters": [
          {
            "$ref": "#/components/parameters/limit"
          },
          {
            "$ref": "#/components/parameters/offset"
          },
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "color",
              "created_at",
              "followers",
              "followers.name",
              "name",
              "notes",
              "offset",
              "path",
              "permalink_url",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "color",
                  "created_at",
                  "followers",
                  "followers.name",
                  "name",
                  "notes",
                  "offset",
                  "path",
                  "permalink_url",
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
            "description": "Successfully retrieved the specified set of tags.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TagCompact"
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
              "tags:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Tag> result = client.tags.getTagsForWorkspace(workspaceGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tagsApiInstance = new Asana.TagsApi(client);\nlet workspace_gid = \"12345\"; // String | Globally unique identifier for the workspace or organization.\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,offset,path,permalink_url,uri,workspace,workspace.name\"\n};\ntagsApiInstance.getTagsForWorkspace(workspace_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tags.getTagsForWorkspace(workspaceGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntags_api_instance = asana.TagsApi(api_client)\nworkspace_gid = \"12345\" # str | Globally unique identifier for the workspace or organization.\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,offset,path,permalink_url,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get tags in a workspace\n    api_response = tags_api_instance.get_tags_for_workspace(workspace_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TagsApi->get_tags_for_workspace: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tags.get_tags_for_workspace(workspace_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tags->getTagsForWorkspace($workspace_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tags.get_tags_for_workspace(workspace_gid: 'workspace_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "post": {
        "summary": "Create a tag in a workspace",
        "description": "<b>Required scope: </b><code>tags:write</code>\n\nCreates a new tag in a workspace or organization.\n\nEvery tag is required to be created in a specific workspace or\norganization, and this cannot be changed once set. Note that you can use\nthe workspace parameter regardless of whether or not it is an\norganization.\n\nReturns the full record of the newly created tag.",
        "tags": [
          "Tags"
        ],
        "operationId": "createTagForWorkspace",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "color",
              "created_at",
              "followers",
              "followers.name",
              "name",
              "notes",
              "permalink_url",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "color",
                  "created_at",
                  "followers",
                  "followers.name",
                  "name",
                  "notes",
                  "permalink_url",
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
          "description": "The tag to create.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TagCreateTagForWorkspaceRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully created the newly specified tag.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TagResponse"
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
              "tags:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTag result = client.tags.createTagForWorkspace(workspaceGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tagsApiInstance = new Asana.TagsApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The tag to create.\nlet workspace_gid = \"12345\"; // String | Globally unique identifier for the workspace or organization.\nlet opts = { \n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,permalink_url,workspace,workspace.name\"\n};\ntagsApiInstance.createTagForWorkspace(body, workspace_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tags.createTagForWorkspace(workspaceGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntags_api_instance = asana.TagsApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The tag to create.\nworkspace_gid = \"12345\" # str | Globally unique identifier for the workspace or organization.\nopts = {\n    'opt_fields': \"color,created_at,followers,followers.name,name,notes,permalink_url,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Create a tag in a workspace\n    api_response = tags_api_instance.create_tag_for_workspace(body, workspace_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TagsApi->create_tag_for_workspace: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tags.create_tag_for_workspace(workspace_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tags->createTagForWorkspace($workspace_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tags.create_tag_for_workspace(workspace_gid: 'workspace_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    }
  },
  "schemas": {
    "TagUpdateRequest": {
      "$ref": "#/components/schemas/TagBaseRequest"
    },
    "TagCreateRequest": {
      "allOf": [
        {
          "$ref": "#/components/schemas/TagBaseRequest"
        },
        {
          "type": "object",
          "properties": {
            "followers": {
              "type": "array",
              "description": "An array of strings identifying users. These can either be the string \"me\", an email, or the gid of a user.",
              "items": {
                "type": "string"
              },
              "example": [
                "12345",
                "42563"
              ]
            },
            "workspace": {
              "type": "string",
              "x-env-variable": true,
              "description": "Gid of an object.",
              "example": "12345"
            }
          }
        }
      ]
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
    "TagBaseRequest": {
      "$ref": "#/components/schemas/TagBase"
    },
    "TagResponse": {
      "allOf": [
        {
          "$ref": "#/components/schemas/TagBase"
        },
        {
          "type": "object",
          "properties": {
            "created_at": {
              "description": "The time at which this resource was created.",
              "type": "string",
              "format": "date-time",
              "readOnly": true,
              "example": "2012-02-22T02:06:58.147Z"
            },
            "followers": {
              "description": "Array of users following this tag.",
              "type": "array",
              "readOnly": true,
              "items": {
                "$ref": "#/components/schemas/UserCompact"
              }
            },
            "workspace": {
              "$ref": "#/components/schemas/WorkspaceCompact"
            },
            "permalink_url": {
              "type": "string",
              "readOnly": true,
              "description": "A url that points directly to the object within Asana.",
              "example": "https://app.asana.com/0/resource/123456789/list"
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
    "TagCreateTagForWorkspaceRequest": {
      "allOf": [
        {
          "$ref": "#/components/schemas/TagBase"
        },
        {
          "type": "object",
          "properties": {
            "followers": {
              "type": "array",
              "description": "An array of strings identifying users. These can either be the string \"me\", an email, or the gid of a user.",
              "items": {
                "type": "string"
              },
              "example": [
                "12345",
                "42563"
              ]
            }
          }
        }
      ]
    },
    "TagBase": {
      "allOf": [
        {
          "$ref": "#/components/schemas/TagCompact"
        },
        {
          "type": "object",
          "properties": {
            "color": {
              "type": "string",
              "description": "Color of the tag.",
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
                null
              ],
              "example": "light-green"
            },
            "notes": {
              "description": "Free-form textual information associated with the tag (i.e. its description).",
              "type": "string",
              "example": "Mittens really likes the stuff from Humboldt."
            }
          }
        }
      ]
    },
    "EmptyResponse": {
      "type": "object",
      "description": "An empty object. Some endpoints do not return an object on success. The success is conveyed through a 2-- status code and returning an empty object."
    }
  },
  "primary_response_schema": {
    "type": "object",
    "properties": {
      "data": {
        "$ref": "#/components/schemas/TagResponse"
      }
    }
  }
}
```

### Relationship manifest

```yaml
asana_tags:
  workspace_id:
    target_table: asana_workspaces
    target_column: id
    confidence: high
    reason: 'response schema: data.workspace.gid'

```

### FK dependency schemas (for stub creation if needed)

```json
{
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

Resource `tag` uses: alphabet=ALPHANUMERIC, length=16

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

Add a class `Tag(Base)` with:

- Table name: `asana_tags`
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
