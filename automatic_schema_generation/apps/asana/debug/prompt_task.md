# Entity Implementation: tasks

You are implementing the **tasks** resource for the Asana API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for tasks

```json
{
  "paths": {
    "/tasks": {
      "get": {
        "summary": "Get multiple tasks",
        "description": "<b>Required scope: </b><code>tasks:read</code>\n\nReturns the compact task records for some filtered set of tasks. Use one or more of the parameters provided to filter the tasks returned. You must specify a `project` or `tag` if you do not specify `assignee` and `workspace`.\n\nFor more complex task retrieval, use [workspaces/{workspace_gid}/tasks/search](/reference/searchtasksforworkspace).",
        "tags": [
          "Tasks"
        ],
        "operationId": "getTasks",
        "parameters": [
          {
            "$ref": "#/components/parameters/limit"
          },
          {
            "$ref": "#/components/parameters/offset"
          },
          {
            "name": "assignee",
            "in": "query",
            "description": "The assignee to filter tasks on. If searching for unassigned tasks, assignee.any = null can be specified.\n*Note: If you specify `assignee`, you must also specify the `workspace` to filter on.*",
            "schema": {
              "type": "string"
            },
            "x-env-variable": "assignee",
            "example": "14641"
          },
          {
            "name": "project",
            "in": "query",
            "description": "The project to filter tasks on.",
            "schema": {
              "type": "string"
            },
            "example": "321654",
            "x-env-variable": "project"
          },
          {
            "name": "section",
            "in": "query",
            "description": "The section to filter tasks on.",
            "schema": {
              "type": "string"
            },
            "example": "321654",
            "x-env-variable": "section"
          },
          {
            "name": "workspace",
            "in": "query",
            "description": "The workspace to filter tasks on.\n*Note: If you specify `workspace`, you must also specify the `assignee` to filter on.*",
            "schema": {
              "type": "string"
            },
            "example": "321654",
            "x-env-variable": "workspace"
          },
          {
            "name": "completed_since",
            "in": "query",
            "description": "Only return tasks that are either incomplete or that have been completed since this time.",
            "schema": {
              "type": "string",
              "format": "date-time",
              "example": "2012-02-22T02:06:58.158Z"
            }
          },
          {
            "name": "modified_since",
            "in": "query",
            "description": "Only return tasks that have been modified since the given time.\n\n*Note: A task is considered \u201cmodified\u201d if any of its properties\nchange, or associations between it and other objects are modified\n(e.g.  a task being added to a project). A task is not considered\nmodified just because another object it is associated with (e.g. a\nsubtask) is modified. Actions that count as modifying the task\ninclude assigning, renaming, completing, and adding stories.*",
            "schema": {
              "type": "string",
              "format": "date-time"
            },
            "example": "2012-02-22T02:06:58.158Z"
          },
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "actual_time_minutes",
              "approval_status",
              "assigned_by",
              "assigned_by.name",
              "assignee",
              "assignee.name",
              "assignee_section",
              "assignee_section.name",
              "assignee_status",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_by",
              "custom_fields",
              "custom_fields.asana_created_field",
              "custom_fields.created_by",
              "custom_fields.created_by.name",
              "custom_fields.currency_code",
              "custom_fields.custom_label",
              "custom_fields.custom_label_position",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.default_access_level",
              "custom_fields.description",
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
              "custom_fields.format",
              "custom_fields.has_notifications_enabled",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.is_global_to_workspace",
              "custom_fields.is_value_read_only",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.people_value",
              "custom_fields.people_value.name",
              "custom_fields.precision",
              "custom_fields.privacy_setting",
              "custom_fields.reference_value",
              "custom_fields.reference_value.name",
              "custom_fields.representation_type",
              "custom_fields.resource_subtype",
              "custom_fields.text_value",
              "custom_fields.type",
              "custom_type",
              "custom_type.name",
              "custom_type_status_option",
              "custom_type_status_option.name",
              "dependencies",
              "dependents",
              "due_at",
              "due_on",
              "external",
              "external.data",
              "followers",
              "followers.name",
              "hearted",
              "hearts",
              "hearts.user",
              "hearts.user.name",
              "html_notes",
              "is_rendered_as_separator",
              "liked",
              "likes",
              "likes.user",
              "likes.user.name",
              "memberships",
              "memberships.project",
              "memberships.project.name",
              "memberships.section",
              "memberships.section.name",
              "modified_at",
              "name",
              "notes",
              "num_hearts",
              "num_likes",
              "num_subtasks",
              "offset",
              "parent",
              "parent.created_by",
              "parent.name",
              "parent.resource_subtype",
              "path",
              "permalink_url",
              "projects",
              "projects.name",
              "resource_subtype",
              "start_at",
              "start_on",
              "tags",
              "tags.name",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "actual_time_minutes",
                  "approval_status",
                  "assigned_by",
                  "assigned_by.name",
                  "assignee",
                  "assignee.name",
                  "assignee_section",
                  "assignee_section.name",
                  "assignee_status",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_by",
                  "custom_fields",
                  "custom_fields.asana_created_field",
                  "custom_fields.created_by",
                  "custom_fields.created_by.name",
                  "custom_fields.currency_code",
                  "custom_fields.custom_label",
                  "custom_fields.custom_label_position",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.default_access_level",
                  "custom_fields.description",
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
                  "custom_fields.format",
                  "custom_fields.has_notifications_enabled",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.is_global_to_workspace",
                  "custom_fields.is_value_read_only",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.people_value",
                  "custom_fields.people_value.name",
                  "custom_fields.precision",
                  "custom_fields.privacy_setting",
                  "custom_fields.reference_value",
                  "custom_fields.reference_value.name",
                  "custom_fields.representation_type",
                  "custom_fields.resource_subtype",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "custom_type",
                  "custom_type.name",
                  "custom_type_status_option",
                  "custom_type_status_option.name",
                  "dependencies",
                  "dependents",
                  "due_at",
                  "due_on",
                  "external",
                  "external.data",
                  "followers",
                  "followers.name",
                  "hearted",
                  "hearts",
                  "hearts.user",
                  "hearts.user.name",
                  "html_notes",
                  "is_rendered_as_separator",
                  "liked",
                  "likes",
                  "likes.user",
                  "likes.user.name",
                  "memberships",
                  "memberships.project",
                  "memberships.project.name",
                  "memberships.section",
                  "memberships.section.name",
                  "modified_at",
                  "name",
                  "notes",
                  "num_hearts",
                  "num_likes",
                  "num_subtasks",
                  "offset",
                  "parent",
                  "parent.created_by",
                  "parent.name",
                  "parent.resource_subtype",
                  "path",
                  "permalink_url",
                  "projects",
                  "projects.name",
                  "resource_subtype",
                  "start_at",
                  "start_on",
                  "tags",
                  "tags.name",
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
            "description": "Successfully retrieved requested tasks.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TaskCompact"
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
              "tasks:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Task> result = client.tasks.getTasks(modifiedSince, completedSince, workspace, section, project, assignee)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'assignee': \"14641\", \n    'project': \"321654\", \n    'section': \"321654\", \n    'workspace': \"321654\", \n    'completed_since': \"2012-02-22T02:06:58.158Z\", \n    'modified_since': \"2012-02-22T02:06:58.158Z\", \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\"\n};\ntasksApiInstance.getTasks(opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.getTasks({param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'assignee': \"14641\", # str | The assignee to filter tasks on. If searching for unassigned tasks, assignee.any = null can be specified. *Note: If you specify `assignee`, you must also specify the `workspace` to filter on.*\n    'project': \"321654\", # str | The project to filter tasks on.\n    'section': \"321654\", # str | The section to filter tasks on.\n    'workspace': \"321654\", # str | The workspace to filter tasks on. *Note: If you specify `workspace`, you must also specify the `assignee` to filter on.*\n    'completed_since': '2012-02-22T02:06:58.158Z', # datetime | Only return tasks that are either incomplete or that have been completed since this time.\n    'modified_since': '2012-02-22T02:06:58.158Z', # datetime | Only return tasks that have been modified since the given time.  *Note: A task is considered \u201cmodified\u201d if any of its properties change, or associations between it and other objects are modified (e.g.  a task being added to a project). A task is not considered modified just because another object it is associated with (e.g. a subtask) is modified. Actions that count as modifying the task include assigning, renaming, completing, and adding stories.*\n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get multiple tasks\n    api_response = tasks_api_instance.get_tasks(opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->get_tasks: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.get_tasks({'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->getTasks(array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.get_tasks(param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "post": {
        "summary": "Create a task",
        "description": "<b>Required scope: </b><code>tasks:write</code>\n\nCreating a new task is as easy as POSTing to the `/tasks` endpoint with a\ndata block containing the fields you\u2019d like to set on the task. Any\nunspecified fields will take on default values.\n\nEvery task is required to be created in a specific workspace, and this\nworkspace cannot be changed once set. The workspace need not be set\nexplicitly if you specify `projects` or a `parent` task instead.",
        "tags": [
          "Tasks"
        ],
        "operationId": "createTask",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "actual_time_minutes",
              "approval_status",
              "assigned_by",
              "assigned_by.name",
              "assignee",
              "assignee.name",
              "assignee_section",
              "assignee_section.name",
              "assignee_status",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_by",
              "custom_fields",
              "custom_fields.asana_created_field",
              "custom_fields.created_by",
              "custom_fields.created_by.name",
              "custom_fields.currency_code",
              "custom_fields.custom_label",
              "custom_fields.custom_label_position",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.default_access_level",
              "custom_fields.description",
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
              "custom_fields.format",
              "custom_fields.has_notifications_enabled",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.is_global_to_workspace",
              "custom_fields.is_value_read_only",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.people_value",
              "custom_fields.people_value.name",
              "custom_fields.precision",
              "custom_fields.privacy_setting",
              "custom_fields.reference_value",
              "custom_fields.reference_value.name",
              "custom_fields.representation_type",
              "custom_fields.resource_subtype",
              "custom_fields.text_value",
              "custom_fields.type",
              "custom_type",
              "custom_type.name",
              "custom_type_status_option",
              "custom_type_status_option.name",
              "dependencies",
              "dependents",
              "due_at",
              "due_on",
              "external",
              "external.data",
              "followers",
              "followers.name",
              "hearted",
              "hearts",
              "hearts.user",
              "hearts.user.name",
              "html_notes",
              "is_rendered_as_separator",
              "liked",
              "likes",
              "likes.user",
              "likes.user.name",
              "memberships",
              "memberships.project",
              "memberships.project.name",
              "memberships.section",
              "memberships.section.name",
              "modified_at",
              "name",
              "notes",
              "num_hearts",
              "num_likes",
              "num_subtasks",
              "parent",
              "parent.created_by",
              "parent.name",
              "parent.resource_subtype",
              "permalink_url",
              "projects",
              "projects.name",
              "resource_subtype",
              "start_at",
              "start_on",
              "tags",
              "tags.name",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "actual_time_minutes",
                  "approval_status",
                  "assigned_by",
                  "assigned_by.name",
                  "assignee",
                  "assignee.name",
                  "assignee_section",
                  "assignee_section.name",
                  "assignee_status",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_by",
                  "custom_fields",
                  "custom_fields.asana_created_field",
                  "custom_fields.created_by",
                  "custom_fields.created_by.name",
                  "custom_fields.currency_code",
                  "custom_fields.custom_label",
                  "custom_fields.custom_label_position",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.default_access_level",
                  "custom_fields.description",
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
                  "custom_fields.format",
                  "custom_fields.has_notifications_enabled",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.is_global_to_workspace",
                  "custom_fields.is_value_read_only",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.people_value",
                  "custom_fields.people_value.name",
                  "custom_fields.precision",
                  "custom_fields.privacy_setting",
                  "custom_fields.reference_value",
                  "custom_fields.reference_value.name",
                  "custom_fields.representation_type",
                  "custom_fields.resource_subtype",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "custom_type",
                  "custom_type.name",
                  "custom_type_status_option",
                  "custom_type_status_option.name",
                  "dependencies",
                  "dependents",
                  "due_at",
                  "due_on",
                  "external",
                  "external.data",
                  "followers",
                  "followers.name",
                  "hearted",
                  "hearts",
                  "hearts.user",
                  "hearts.user.name",
                  "html_notes",
                  "is_rendered_as_separator",
                  "liked",
                  "likes",
                  "likes.user",
                  "likes.user.name",
                  "memberships",
                  "memberships.project",
                  "memberships.project.name",
                  "memberships.section",
                  "memberships.section.name",
                  "modified_at",
                  "name",
                  "notes",
                  "num_hearts",
                  "num_likes",
                  "num_subtasks",
                  "parent",
                  "parent.created_by",
                  "parent.name",
                  "parent.resource_subtype",
                  "permalink_url",
                  "projects",
                  "projects.name",
                  "resource_subtype",
                  "start_at",
                  "start_on",
                  "tags",
                  "tags.name",
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
          "description": "The task to create.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TaskRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully created a new task.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TaskResponse"
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
              "tasks:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTask result = client.tasks.createTask()\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The task to create.\nlet opts = { \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name\"\n};\ntasksApiInstance.createTask(body, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.createTask({field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The task to create.\nopts = {\n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Create a task\n    api_response = tasks_api_instance.create_task(body, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->create_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.create_task({'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->createTask(array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.create_task(field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tasks/{task_gid}": {
      "get": {
        "summary": "Get a task",
        "description": "<b>Required scope: </b><code>tasks:read</code>\n\n<table>\n  <tr>\n    <th>Field</th>\n    <th>Required Scope</th>\n  </tr>\n  <tr>\n    <td><code>memberships</code></td>\n    <td><code>projects:read</code>, <code>project_sections:read</code></td>\n  </tr>\n  <tr>\n    <td><code>actual_time_minutes</code></td>\n    <td><code>time_tracking_entries:read</code></td>\n  </tr>\n</table>\n\nReturns the complete task record for a single task.",
        "tags": [
          "Tasks"
        ],
        "operationId": "getTask",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "actual_time_minutes",
              "approval_status",
              "assigned_by",
              "assigned_by.name",
              "assignee",
              "assignee.name",
              "assignee_section",
              "assignee_section.name",
              "assignee_status",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_by",
              "custom_fields",
              "custom_fields.asana_created_field",
              "custom_fields.created_by",
              "custom_fields.created_by.name",
              "custom_fields.currency_code",
              "custom_fields.custom_label",
              "custom_fields.custom_label_position",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.default_access_level",
              "custom_fields.description",
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
              "custom_fields.format",
              "custom_fields.has_notifications_enabled",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.is_global_to_workspace",
              "custom_fields.is_value_read_only",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.people_value",
              "custom_fields.people_value.name",
              "custom_fields.precision",
              "custom_fields.privacy_setting",
              "custom_fields.reference_value",
              "custom_fields.reference_value.name",
              "custom_fields.representation_type",
              "custom_fields.resource_subtype",
              "custom_fields.text_value",
              "custom_fields.type",
              "custom_type",
              "custom_type.name",
              "custom_type_status_option",
              "custom_type_status_option.name",
              "dependencies",
              "dependents",
              "due_at",
              "due_on",
              "external",
              "external.data",
              "followers",
              "followers.name",
              "hearted",
              "hearts",
              "hearts.user",
              "hearts.user.name",
              "html_notes",
              "is_rendered_as_separator",
              "liked",
              "likes",
              "likes.user",
              "likes.user.name",
              "memberships",
              "memberships.project",
              "memberships.project.name",
              "memberships.section",
              "memberships.section.name",
              "modified_at",
              "name",
              "notes",
              "num_hearts",
              "num_likes",
              "num_subtasks",
              "parent",
              "parent.created_by",
              "parent.name",
              "parent.resource_subtype",
              "permalink_url",
              "projects",
              "projects.name",
              "resource_subtype",
              "start_at",
              "start_on",
              "tags",
              "tags.name",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "actual_time_minutes",
                  "approval_status",
                  "assigned_by",
                  "assigned_by.name",
                  "assignee",
                  "assignee.name",
                  "assignee_section",
                  "assignee_section.name",
                  "assignee_status",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_by",
                  "custom_fields",
                  "custom_fields.asana_created_field",
                  "custom_fields.created_by",
                  "custom_fields.created_by.name",
                  "custom_fields.currency_code",
                  "custom_fields.custom_label",
                  "custom_fields.custom_label_position",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.default_access_level",
                  "custom_fields.description",
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
                  "custom_fields.format",
                  "custom_fields.has_notifications_enabled",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.is_global_to_workspace",
                  "custom_fields.is_value_read_only",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.people_value",
                  "custom_fields.people_value.name",
                  "custom_fields.precision",
                  "custom_fields.privacy_setting",
                  "custom_fields.reference_value",
                  "custom_fields.reference_value.name",
                  "custom_fields.representation_type",
                  "custom_fields.resource_subtype",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "custom_type",
                  "custom_type.name",
                  "custom_type_status_option",
                  "custom_type_status_option.name",
                  "dependencies",
                  "dependents",
                  "due_at",
                  "due_on",
                  "external",
                  "external.data",
                  "followers",
                  "followers.name",
                  "hearted",
                  "hearts",
                  "hearts.user",
                  "hearts.user.name",
                  "html_notes",
                  "is_rendered_as_separator",
                  "liked",
                  "likes",
                  "likes.user",
                  "likes.user.name",
                  "memberships",
                  "memberships.project",
                  "memberships.project.name",
                  "memberships.section",
                  "memberships.section.name",
                  "modified_at",
                  "name",
                  "notes",
                  "num_hearts",
                  "num_likes",
                  "num_subtasks",
                  "parent",
                  "parent.created_by",
                  "parent.name",
                  "parent.resource_subtype",
                  "permalink_url",
                  "projects",
                  "projects.name",
                  "resource_subtype",
                  "start_at",
                  "start_on",
                  "tags",
                  "tags.name",
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
            "description": "Successfully retrieved the specified task.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TaskResponse"
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
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTask result = client.tasks.getTask(taskGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet task_gid = \"321654\"; // String | The task to operate on.\nlet opts = { \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name\"\n};\ntasksApiInstance.getTask(task_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.getTask(taskGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\ntask_gid = \"321654\" # str | The task to operate on.\nopts = {\n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get a task\n    api_response = tasks_api_instance.get_task(task_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->get_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.get_task(task_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->getTask($task_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.get_task(task_gid: 'task_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "put": {
        "summary": "Update a task",
        "description": "<b>Required scope: </b><code>tasks:write</code>\n\nA specific, existing task can be updated by making a PUT request on the\nURL for that task. Only the fields provided in the `data` block will be\nupdated; any unspecified fields will remain unchanged.\n\nWhen using this method, it is best to specify only those fields you wish\nto change, or else you may overwrite changes made by another user since\nyou last retrieved the task.\n\nReturns the complete updated task record.",
        "tags": [
          "Tasks"
        ],
        "operationId": "updateTask",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "actual_time_minutes",
              "approval_status",
              "assigned_by",
              "assigned_by.name",
              "assignee",
              "assignee.name",
              "assignee_section",
              "assignee_section.name",
              "assignee_status",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_by",
              "custom_fields",
              "custom_fields.asana_created_field",
              "custom_fields.created_by",
              "custom_fields.created_by.name",
              "custom_fields.currency_code",
              "custom_fields.custom_label",
              "custom_fields.custom_label_position",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.default_access_level",
              "custom_fields.description",
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
              "custom_fields.format",
              "custom_fields.has_notifications_enabled",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.is_global_to_workspace",
              "custom_fields.is_value_read_only",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.people_value",
              "custom_fields.people_value.name",
              "custom_fields.precision",
              "custom_fields.privacy_setting",
              "custom_fields.reference_value",
              "custom_fields.reference_value.name",
              "custom_fields.representation_type",
              "custom_fields.resource_subtype",
              "custom_fields.text_value",
              "custom_fields.type",
              "custom_type",
              "custom_type.name",
              "custom_type_status_option",
              "custom_type_status_option.name",
              "dependencies",
              "dependents",
              "due_at",
              "due_on",
              "external",
              "external.data",
              "followers",
              "followers.name",
              "hearted",
              "hearts",
              "hearts.user",
              "hearts.user.name",
              "html_notes",
              "is_rendered_as_separator",
              "liked",
              "likes",
              "likes.user",
              "likes.user.name",
              "memberships",
              "memberships.project",
              "memberships.project.name",
              "memberships.section",
              "memberships.section.name",
              "modified_at",
              "name",
              "notes",
              "num_hearts",
              "num_likes",
              "num_subtasks",
              "parent",
              "parent.created_by",
              "parent.name",
              "parent.resource_subtype",
              "permalink_url",
              "projects",
              "projects.name",
              "resource_subtype",
              "start_at",
              "start_on",
              "tags",
              "tags.name",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "actual_time_minutes",
                  "approval_status",
                  "assigned_by",
                  "assigned_by.name",
                  "assignee",
                  "assignee.name",
                  "assignee_section",
                  "assignee_section.name",
                  "assignee_status",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_by",
                  "custom_fields",
                  "custom_fields.asana_created_field",
                  "custom_fields.created_by",
                  "custom_fields.created_by.name",
                  "custom_fields.currency_code",
                  "custom_fields.custom_label",
                  "custom_fields.custom_label_position",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.default_access_level",
                  "custom_fields.description",
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
                  "custom_fields.format",
                  "custom_fields.has_notifications_enabled",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.is_global_to_workspace",
                  "custom_fields.is_value_read_only",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.people_value",
                  "custom_fields.people_value.name",
                  "custom_fields.precision",
                  "custom_fields.privacy_setting",
                  "custom_fields.reference_value",
                  "custom_fields.reference_value.name",
                  "custom_fields.representation_type",
                  "custom_fields.resource_subtype",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "custom_type",
                  "custom_type.name",
                  "custom_type_status_option",
                  "custom_type_status_option.name",
                  "dependencies",
                  "dependents",
                  "due_at",
                  "due_on",
                  "external",
                  "external.data",
                  "followers",
                  "followers.name",
                  "hearted",
                  "hearts",
                  "hearts.user",
                  "hearts.user.name",
                  "html_notes",
                  "is_rendered_as_separator",
                  "liked",
                  "likes",
                  "likes.user",
                  "likes.user.name",
                  "memberships",
                  "memberships.project",
                  "memberships.project.name",
                  "memberships.section",
                  "memberships.section.name",
                  "modified_at",
                  "name",
                  "notes",
                  "num_hearts",
                  "num_likes",
                  "num_subtasks",
                  "parent",
                  "parent.created_by",
                  "parent.name",
                  "parent.resource_subtype",
                  "permalink_url",
                  "projects",
                  "projects.name",
                  "resource_subtype",
                  "start_at",
                  "start_on",
                  "tags",
                  "tags.name",
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
          "description": "The task to update.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TaskRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully updated the specified task.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TaskResponse"
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
              "tasks:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTask result = client.tasks.updateTask(taskGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The task to update.\nlet task_gid = \"321654\"; // String | The task to operate on.\nlet opts = { \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name\"\n};\ntasksApiInstance.updateTask(body, task_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.updateTask(taskGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The task to update.\ntask_gid = \"321654\" # str | The task to operate on.\nopts = {\n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Update a task\n    api_response = tasks_api_instance.update_task(body, task_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->update_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.update_task(task_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->updateTask($task_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.update_task(task_gid: 'task_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      },
      "delete": {
        "summary": "Delete a task",
        "description": "<b>Required scope: </b><code>tasks:delete</code>\n\nA specific, existing task can be deleted by making a DELETE request on\nthe URL for that task. Deleted tasks go into the \u201ctrash\u201d of the user\nmaking the delete request. Tasks can be recovered from the trash within a\nperiod of 30 days; afterward they are completely removed from the system.\n\nReturns an empty data record.",
        "tags": [
          "Tasks"
        ],
        "operationId": "deleteTask",
        "responses": {
          "200": {
            "description": "Successfully deleted the specified task.",
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
              "tasks:delete"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.tasks.deleteTask(taskGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet task_gid = \"321654\"; // String | The task to operate on.\n\ntasksApiInstance.deleteTask(task_gid).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.deleteTask(taskGid)\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\ntask_gid = \"321654\" # str | The task to operate on.\n\n\ntry:\n    # Delete a task\n    api_response = tasks_api_instance.delete_task(task_gid)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->delete_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.delete_task(task_gid, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->deleteTask($task_gid, array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.delete_task(task_gid: 'task_gid', options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tasks/{task_gid}/duplicate": {
      "post": {
        "summary": "Duplicate a task",
        "description": "<b>Required scope: </b><code>tasks:write</code>\n\nCreates and returns a job that will asynchronously handle the duplication.",
        "tags": [
          "Tasks"
        ],
        "operationId": "duplicateTask",
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
          "description": "Describes the duplicate's name and the fields that will be duplicated.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TaskDuplicateRequest"
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
              "tasks:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJob result = client.tasks.duplicateTask(taskGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | Describes the duplicate's name and the fields that will be duplicated.\nlet task_gid = \"321654\"; // String | The task to operate on.\nlet opts = { \n    'opt_fields': \"new_graph_export,new_graph_export.completed_at,new_graph_export.created_at,new_graph_export.download_url,new_portfolio,new_portfolio.name,new_project,new_project.name,new_project_template,new_project_template.name,new_resource_export,new_resource_export.completed_at,new_resource_export.created_at,new_resource_export.download_url,new_task,new_task.created_by,new_task.name,new_task.resource_subtype,resource_subtype,status\"\n};\ntasksApiInstance.duplicateTask(body, task_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.duplicateTask(taskGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | Describes the duplicate's name and the fields that will be duplicated.\ntask_gid = \"321654\" # str | The task to operate on.\nopts = {\n    'opt_fields': \"new_graph_export,new_graph_export.completed_at,new_graph_export.created_at,new_graph_export.download_url,new_portfolio,new_portfolio.name,new_project,new_project.name,new_project_template,new_project_template.name,new_resource_export,new_resource_export.completed_at,new_resource_export.created_at,new_resource_export.download_url,new_task,new_task.created_by,new_task.name,new_task.resource_subtype,resource_subtype,status\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Duplicate a task\n    api_response = tasks_api_instance.duplicate_task(body, task_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->duplicate_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.duplicate_task(task_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->duplicateTask($task_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.duplicate_task(task_gid: 'task_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/projects/{project_gid}/tasks": {
      "get": {
        "summary": "Get tasks from a project",
        "description": "<b>Required scope: </b><code>tasks:read</code>\n\nReturns the compact task records for all tasks within the given project, ordered by their priority within the project. Tasks can exist in more than one project at a time.",
        "tags": [
          "Tasks"
        ],
        "operationId": "getTasksForProject",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "actual_time_minutes",
              "approval_status",
              "assigned_by",
              "assigned_by.name",
              "assignee",
              "assignee.name",
              "assignee_section",
              "assignee_section.name",
              "assignee_status",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_by",
              "custom_fields",
              "custom_fields.asana_created_field",
              "custom_fields.created_by",
              "custom_fields.created_by.name",
              "custom_fields.currency_code",
              "custom_fields.custom_label",
              "custom_fields.custom_label_position",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.default_access_level",
              "custom_fields.description",
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
              "custom_fields.format",
              "custom_fields.has_notifications_enabled",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.is_global_to_workspace",
              "custom_fields.is_value_read_only",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.people_value",
              "custom_fields.people_value.name",
              "custom_fields.precision",
              "custom_fields.privacy_setting",
              "custom_fields.reference_value",
              "custom_fields.reference_value.name",
              "custom_fields.representation_type",
              "custom_fields.resource_subtype",
              "custom_fields.text_value",
              "custom_fields.type",
              "custom_type",
              "custom_type.name",
              "custom_type_status_option",
              "custom_type_status_option.name",
              "dependencies",
              "dependents",
              "due_at",
              "due_on",
              "external",
              "external.data",
              "followers",
              "followers.name",
              "hearted",
              "hearts",
              "hearts.user",
              "hearts.user.name",
              "html_notes",
              "is_rendered_as_separator",
              "liked",
              "likes",
              "likes.user",
              "likes.user.name",
              "memberships",
              "memberships.project",
              "memberships.project.name",
              "memberships.section",
              "memberships.section.name",
              "modified_at",
              "name",
              "notes",
              "num_hearts",
              "num_likes",
              "num_subtasks",
              "offset",
              "parent",
              "parent.created_by",
              "parent.name",
              "parent.resource_subtype",
              "path",
              "permalink_url",
              "projects",
              "projects.name",
              "resource_subtype",
              "start_at",
              "start_on",
              "tags",
              "tags.name",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "actual_time_minutes",
                  "approval_status",
                  "assigned_by",
                  "assigned_by.name",
                  "assignee",
                  "assignee.name",
                  "assignee_section",
                  "assignee_section.name",
                  "assignee_status",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_by",
                  "custom_fields",
                  "custom_fields.asana_created_field",
                  "custom_fields.created_by",
                  "custom_fields.created_by.name",
                  "custom_fields.currency_code",
                  "custom_fields.custom_label",
                  "custom_fields.custom_label_position",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.default_access_level",
                  "custom_fields.description",
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
                  "custom_fields.format",
                  "custom_fields.has_notifications_enabled",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.is_global_to_workspace",
                  "custom_fields.is_value_read_only",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.people_value",
                  "custom_fields.people_value.name",
                  "custom_fields.precision",
                  "custom_fields.privacy_setting",
                  "custom_fields.reference_value",
                  "custom_fields.reference_value.name",
                  "custom_fields.representation_type",
                  "custom_fields.resource_subtype",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "custom_type",
                  "custom_type.name",
                  "custom_type_status_option",
                  "custom_type_status_option.name",
                  "dependencies",
                  "dependents",
                  "due_at",
                  "due_on",
                  "external",
                  "external.data",
                  "followers",
                  "followers.name",
                  "hearted",
                  "hearts",
                  "hearts.user",
                  "hearts.user.name",
                  "html_notes",
                  "is_rendered_as_separator",
                  "liked",
                  "likes",
                  "likes.user",
                  "likes.user.name",
                  "memberships",
                  "memberships.project",
                  "memberships.project.name",
                  "memberships.section",
                  "memberships.section.name",
                  "modified_at",
                  "name",
                  "notes",
                  "num_hearts",
                  "num_likes",
                  "num_subtasks",
                  "offset",
                  "parent",
                  "parent.created_by",
                  "parent.name",
                  "parent.resource_subtype",
                  "path",
                  "permalink_url",
                  "projects",
                  "projects.name",
                  "resource_subtype",
                  "start_at",
                  "start_on",
                  "tags",
                  "tags.name",
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
            "description": "Successfully retrieved the requested project's tasks.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TaskCompact"
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
              "tasks:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Task> result = client.tasks.getTasksForProject(projectGid, completedSince)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet project_gid = \"1331\"; // String | Globally unique identifier for the project.\nlet opts = { \n    'completed_since': \"2012-02-22T02:06:58.158Z\", \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\"\n};\ntasksApiInstance.getTasksForProject(project_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.getTasksForProject(projectGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nproject_gid = \"1331\" # str | Globally unique identifier for the project.\nopts = {\n    'completed_since': \"2012-02-22T02:06:58.158Z\", # str | Only return tasks that are either incomplete or that have been completed since this time. Accepts a date-time string or the keyword *now*. \n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get tasks from a project\n    api_response = tasks_api_instance.get_tasks_for_project(project_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->get_tasks_for_project: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.get_tasks_for_project(project_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->getTasksForProject($project_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.get_tasks_for_project(project_gid: 'project_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/sections/{section_gid}/tasks": {
      "get": {
        "summary": "Get tasks from a section",
        "description": "<b>Required scope: </b><code>tasks:read</code>\n\n*Board view only*: Returns the compact section records for all tasks within the given section.",
        "tags": [
          "Tasks"
        ],
        "operationId": "getTasksForSection",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "actual_time_minutes",
              "approval_status",
              "assigned_by",
              "assigned_by.name",
              "assignee",
              "assignee.name",
              "assignee_section",
              "assignee_section.name",
              "assignee_status",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_by",
              "custom_fields",
              "custom_fields.asana_created_field",
              "custom_fields.created_by",
              "custom_fields.created_by.name",
              "custom_fields.currency_code",
              "custom_fields.custom_label",
              "custom_fields.custom_label_position",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.default_access_level",
              "custom_fields.description",
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
              "custom_fields.format",
              "custom_fields.has_notifications_enabled",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.is_global_to_workspace",
              "custom_fields.is_value_read_only",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.people_value",
              "custom_fields.people_value.name",
              "custom_fields.precision",
              "custom_fields.privacy_setting",
              "custom_fields.reference_value",
              "custom_fields.reference_value.name",
              "custom_fields.representation_type",
              "custom_fields.resource_subtype",
              "custom_fields.text_value",
              "custom_fields.type",
              "custom_type",
              "custom_type.name",
              "custom_type_status_option",
              "custom_type_status_option.name",
              "dependencies",
              "dependents",
              "due_at",
              "due_on",
              "external",
              "external.data",
              "followers",
              "followers.name",
              "hearted",
              "hearts",
              "hearts.user",
              "hearts.user.name",
              "html_notes",
              "is_rendered_as_separator",
              "liked",
              "likes",
              "likes.user",
              "likes.user.name",
              "memberships",
              "memberships.project",
              "memberships.project.name",
              "memberships.section",
              "memberships.section.name",
              "modified_at",
              "name",
              "notes",
              "num_hearts",
              "num_likes",
              "num_subtasks",
              "offset",
              "parent",
              "parent.created_by",
              "parent.name",
              "parent.resource_subtype",
              "path",
              "permalink_url",
              "projects",
              "projects.name",
              "resource_subtype",
              "start_at",
              "start_on",
              "tags",
              "tags.name",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "actual_time_minutes",
                  "approval_status",
                  "assigned_by",
                  "assigned_by.name",
                  "assignee",
                  "assignee.name",
                  "assignee_section",
                  "assignee_section.name",
                  "assignee_status",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_by",
                  "custom_fields",
                  "custom_fields.asana_created_field",
                  "custom_fields.created_by",
                  "custom_fields.created_by.name",
                  "custom_fields.currency_code",
                  "custom_fields.custom_label",
                  "custom_fields.custom_label_position",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.default_access_level",
                  "custom_fields.description",
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
                  "custom_fields.format",
                  "custom_fields.has_notifications_enabled",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.is_global_to_workspace",
                  "custom_fields.is_value_read_only",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.people_value",
                  "custom_fields.people_value.name",
                  "custom_fields.precision",
                  "custom_fields.privacy_setting",
                  "custom_fields.reference_value",
                  "custom_fields.reference_value.name",
                  "custom_fields.representation_type",
                  "custom_fields.resource_subtype",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "custom_type",
                  "custom_type.name",
                  "custom_type_status_option",
                  "custom_type_status_option.name",
                  "dependencies",
                  "dependents",
                  "due_at",
                  "due_on",
                  "external",
                  "external.data",
                  "followers",
                  "followers.name",
                  "hearted",
                  "hearts",
                  "hearts.user",
                  "hearts.user.name",
                  "html_notes",
                  "is_rendered_as_separator",
                  "liked",
                  "likes",
                  "likes.user",
                  "likes.user.name",
                  "memberships",
                  "memberships.project",
                  "memberships.project.name",
                  "memberships.section",
                  "memberships.section.name",
                  "modified_at",
                  "name",
                  "notes",
                  "num_hearts",
                  "num_likes",
                  "num_subtasks",
                  "offset",
                  "parent",
                  "parent.created_by",
                  "parent.name",
                  "parent.resource_subtype",
                  "path",
                  "permalink_url",
                  "projects",
                  "projects.name",
                  "resource_subtype",
                  "start_at",
                  "start_on",
                  "tags",
                  "tags.name",
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
            "description": "Successfully retrieved the section's tasks.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TaskCompact"
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
              "tasks:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Task> result = client.tasks.getTasksForSection(sectionGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet section_gid = \"321654\"; // String | The globally unique identifier for the section.\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'completed_since': \"2012-02-22T02:06:58.158Z\", \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\"\n};\ntasksApiInstance.getTasksForSection(section_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.getTasksForSection(sectionGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nsection_gid = \"321654\" # str | The globally unique identifier for the section.\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'completed_since': \"2012-02-22T02:06:58.158Z\", # str | Only return tasks that are either incomplete or that have been completed since this time. Accepts a date-time string or the keyword *now*. \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get tasks from a section\n    api_response = tasks_api_instance.get_tasks_for_section(section_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->get_tasks_for_section: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.get_tasks_for_section(section_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->getTasksForSection($section_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.get_tasks_for_section(section_gid: 'section_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tags/{tag_gid}/tasks": {
      "get": {
        "summary": "Get tasks from a tag",
        "description": "<b>Required scope: </b><code>tasks:read</code>\n\nReturns the compact task records for all tasks with the given tag. Tasks can have more than one tag at a time.",
        "tags": [
          "Tasks"
        ],
        "operationId": "getTasksForTag",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "actual_time_minutes",
              "approval_status",
              "assigned_by",
              "assigned_by.name",
              "assignee",
              "assignee.name",
              "assignee_section",
              "assignee_section.name",
              "assignee_status",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_by",
              "custom_fields",
              "custom_fields.asana_created_field",
              "custom_fields.created_by",
              "custom_fields.created_by.name",
              "custom_fields.currency_code",
              "custom_fields.custom_label",
              "custom_fields.custom_label_position",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.default_access_level",
              "custom_fields.description",
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
              "custom_fields.format",
              "custom_fields.has_notifications_enabled",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.is_global_to_workspace",
              "custom_fields.is_value_read_only",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.people_value",
              "custom_fields.people_value.name",
              "custom_fields.precision",
              "custom_fields.privacy_setting",
              "custom_fields.reference_value",
              "custom_fields.reference_value.name",
              "custom_fields.representation_type",
              "custom_fields.resource_subtype",
              "custom_fields.text_value",
              "custom_fields.type",
              "custom_type",
              "custom_type.name",
              "custom_type_status_option",
              "custom_type_status_option.name",
              "dependencies",
              "dependents",
              "due_at",
              "due_on",
              "external",
              "external.data",
              "followers",
              "followers.name",
              "hearted",
              "hearts",
              "hearts.user",
              "hearts.user.name",
              "html_notes",
              "is_rendered_as_separator",
              "liked",
              "likes",
              "likes.user",
              "likes.user.name",
              "memberships",
              "memberships.project",
              "memberships.project.name",
              "memberships.section",
              "memberships.section.name",
              "modified_at",
              "name",
              "notes",
              "num_hearts",
              "num_likes",
              "num_subtasks",
              "offset",
              "parent",
              "parent.created_by",
              "parent.name",
              "parent.resource_subtype",
              "path",
              "permalink_url",
              "projects",
              "projects.name",
              "resource_subtype",
              "start_at",
              "start_on",
              "tags",
              "tags.name",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "actual_time_minutes",
                  "approval_status",
                  "assigned_by",
                  "assigned_by.name",
                  "assignee",
                  "assignee.name",
                  "assignee_section",
                  "assignee_section.name",
                  "assignee_status",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_by",
                  "custom_fields",
                  "custom_fields.asana_created_field",
                  "custom_fields.created_by",
                  "custom_fields.created_by.name",
                  "custom_fields.currency_code",
                  "custom_fields.custom_label",
                  "custom_fields.custom_label_position",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.default_access_level",
                  "custom_fields.description",
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
                  "custom_fields.format",
                  "custom_fields.has_notifications_enabled",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.is_global_to_workspace",
                  "custom_fields.is_value_read_only",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.people_value",
                  "custom_fields.people_value.name",
                  "custom_fields.precision",
                  "custom_fields.privacy_setting",
                  "custom_fields.reference_value",
                  "custom_fields.reference_value.name",
                  "custom_fields.representation_type",
                  "custom_fields.resource_subtype",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "custom_type",
                  "custom_type.name",
                  "custom_type_status_option",
                  "custom_type_status_option.name",
                  "dependencies",
                  "dependents",
                  "due_at",
                  "due_on",
                  "external",
                  "external.data",
                  "followers",
                  "followers.name",
                  "hearted",
                  "hearts",
                  "hearts.user",
                  "hearts.user.name",
                  "html_notes",
                  "is_rendered_as_separator",
                  "liked",
                  "likes",
                  "likes.user",
                  "likes.user.name",
                  "memberships",
                  "memberships.project",
                  "memberships.project.name",
                  "memberships.section",
                  "memberships.section.name",
                  "modified_at",
                  "name",
                  "notes",
                  "num_hearts",
                  "num_likes",
                  "num_subtasks",
                  "offset",
                  "parent",
                  "parent.created_by",
                  "parent.name",
                  "parent.resource_subtype",
                  "path",
                  "permalink_url",
                  "projects",
                  "projects.name",
                  "resource_subtype",
                  "start_at",
                  "start_on",
                  "tags",
                  "tags.name",
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
            "description": "Successfully retrieved the tasks associated with the specified tag.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TaskCompact"
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
              "tasks:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Task> result = client.tasks.getTasksForTag(tagGid)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet tag_gid = \"11235\"; // String | Globally unique identifier for the tag.\nlet opts = { \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\"\n};\ntasksApiInstance.getTasksForTag(tag_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.getTasksForTag(tagGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\ntag_gid = \"11235\" # str | Globally unique identifier for the tag.\nopts = {\n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get tasks from a tag\n    api_response = tasks_api_instance.get_tasks_for_tag(tag_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->get_tasks_for_tag: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.get_tasks_for_tag(tag_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->getTasksForTag($tag_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.get_tasks_for_tag(tag_gid: 'tag_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/user_task_lists/{user_task_list_gid}/tasks": {
      "get": {
        "summary": "Get tasks from a user task list",
        "description": "<b>Required scope: </b><code>tasks:read</code>\n\nReturns the compact list of tasks in a user\u2019s My Tasks list.\n*Note: Access control is enforced for this endpoint as with all Asana API endpoints, meaning a user\u2019s private tasks will be filtered out if the API-authenticated user does not have access to them.*\n*Note: Both complete and incomplete tasks are returned by default unless they are filtered out (for example, setting `completed_since=now` will return only incomplete tasks, which is the default view for \u201cMy Tasks\u201d in Asana.)*",
        "tags": [
          "Tasks"
        ],
        "operationId": "getTasksForUserTaskList",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "actual_time_minutes",
              "approval_status",
              "assigned_by",
              "assigned_by.name",
              "assignee",
              "assignee.name",
              "assignee_section",
              "assignee_section.name",
              "assignee_status",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_by",
              "custom_fields",
              "custom_fields.asana_created_field",
              "custom_fields.created_by",
              "custom_fields.created_by.name",
              "custom_fields.currency_code",
              "custom_fields.custom_label",
              "custom_fields.custom_label_position",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.default_access_level",
              "custom_fields.description",
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
              "custom_fields.format",
              "custom_fields.has_notifications_enabled",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.is_global_to_workspace",
              "custom_fields.is_value_read_only",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.people_value",
              "custom_fields.people_value.name",
              "custom_fields.precision",
              "custom_fields.privacy_setting",
              "custom_fields.reference_value",
              "custom_fields.reference_value.name",
              "custom_fields.representation_type",
              "custom_fields.resource_subtype",
              "custom_fields.text_value",
              "custom_fields.type",
              "custom_type",
              "custom_type.name",
              "custom_type_status_option",
              "custom_type_status_option.name",
              "dependencies",
              "dependents",
              "due_at",
              "due_on",
              "external",
              "external.data",
              "followers",
              "followers.name",
              "hearted",
              "hearts",
              "hearts.user",
              "hearts.user.name",
              "html_notes",
              "is_rendered_as_separator",
              "liked",
              "likes",
              "likes.user",
              "likes.user.name",
              "memberships",
              "memberships.project",
              "memberships.project.name",
              "memberships.section",
              "memberships.section.name",
              "modified_at",
              "name",
              "notes",
              "num_hearts",
              "num_likes",
              "num_subtasks",
              "offset",
              "parent",
              "parent.created_by",
              "parent.name",
              "parent.resource_subtype",
              "path",
              "permalink_url",
              "projects",
              "projects.name",
              "resource_subtype",
              "start_at",
              "start_on",
              "tags",
              "tags.name",
              "uri",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "actual_time_minutes",
                  "approval_status",
                  "assigned_by",
                  "assigned_by.name",
                  "assignee",
                  "assignee.name",
                  "assignee_section",
                  "assignee_section.name",
                  "assignee_status",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_by",
                  "custom_fields",
                  "custom_fields.asana_created_field",
                  "custom_fields.created_by",
                  "custom_fields.created_by.name",
                  "custom_fields.currency_code",
                  "custom_fields.custom_label",
                  "custom_fields.custom_label_position",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.default_access_level",
                  "custom_fields.description",
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
                  "custom_fields.format",
                  "custom_fields.has_notifications_enabled",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.is_global_to_workspace",
                  "custom_fields.is_value_read_only",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.people_value",
                  "custom_fields.people_value.name",
                  "custom_fields.precision",
                  "custom_fields.privacy_setting",
                  "custom_fields.reference_value",
                  "custom_fields.reference_value.name",
                  "custom_fields.representation_type",
                  "custom_fields.resource_subtype",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "custom_type",
                  "custom_type.name",
                  "custom_type_status_option",
                  "custom_type_status_option.name",
                  "dependencies",
                  "dependents",
                  "due_at",
                  "due_on",
                  "external",
                  "external.data",
                  "followers",
                  "followers.name",
                  "hearted",
                  "hearts",
                  "hearts.user",
                  "hearts.user.name",
                  "html_notes",
                  "is_rendered_as_separator",
                  "liked",
                  "likes",
                  "likes.user",
                  "likes.user.name",
                  "memberships",
                  "memberships.project",
                  "memberships.project.name",
                  "memberships.section",
                  "memberships.section.name",
                  "modified_at",
                  "name",
                  "notes",
                  "num_hearts",
                  "num_likes",
                  "num_subtasks",
                  "offset",
                  "parent",
                  "parent.created_by",
                  "parent.name",
                  "parent.resource_subtype",
                  "path",
                  "permalink_url",
                  "projects",
                  "projects.name",
                  "resource_subtype",
                  "start_at",
                  "start_on",
                  "tags",
                  "tags.name",
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
            "description": "Successfully retrieved the user task list's tasks.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/TaskCompact"
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
              "tasks:read"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nList<Task> result = client.tasks.getTasksForUserTaskList(userTaskListGid, completedSince)\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet user_task_list_gid = \"12345\"; // String | Globally unique identifier for the user task list.\nlet opts = { \n    'completed_since': \"2012-02-22T02:06:58.158Z\", \n    'limit': 50, \n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\"\n};\ntasksApiInstance.getTasksForUserTaskList(user_task_list_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.getTasksForUserTaskList(userTaskListGid, {param: \"value\", param: \"value\", opt_pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nuser_task_list_gid = \"12345\" # str | Globally unique identifier for the user task list.\nopts = {\n    'completed_since': \"2012-02-22T02:06:58.158Z\", # str | Only return tasks that are either incomplete or that have been completed since this time. Accepts a date-time string or the keyword *now*. \n    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.\n    'offset': \"eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9\", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*\n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Get tasks from a user task list\n    api_response = tasks_api_instance.get_tasks_for_user_task_list(user_task_list_gid, opts)\n    for data in api_response:\n        pprint(data)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->get_tasks_for_user_task_list: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.get_tasks_for_user_task_list(user_task_list_gid, {'param': 'value', 'param': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->getTasksForUserTaskList($user_task_list_gid, array('param' => 'value', 'param' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.get_tasks_for_user_task_list(user_task_list_gid: 'user_task_list_gid', param: \"value\", param: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tasks/{task_gid}/setParent": {
      "post": {
        "summary": "Set the parent of a task",
        "description": "<b>Required scope: </b><code>tasks:write</code>\n\nUpdates the parent of a given task. This endpoint can be used to make a task a subtask of another task, or to remove its existing parent.\nWhen using `insert_before` and `insert_after`, at most one of those two options can be specified, and they must already be subtasks of the parent.\nReturns the complete, updated record of the affected [task](/reference/tasks#/task).",
        "tags": [
          "Tasks"
        ],
        "operationId": "setParentForTask",
        "parameters": [
          {
            "name": "opt_fields",
            "in": "query",
            "description": "This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.",
            "required": false,
            "example": [
              "actual_time_minutes",
              "approval_status",
              "assigned_by",
              "assigned_by.name",
              "assignee",
              "assignee.name",
              "assignee_section",
              "assignee_section.name",
              "assignee_status",
              "completed",
              "completed_at",
              "completed_by",
              "completed_by.name",
              "created_at",
              "created_by",
              "custom_fields",
              "custom_fields.asana_created_field",
              "custom_fields.created_by",
              "custom_fields.created_by.name",
              "custom_fields.currency_code",
              "custom_fields.custom_label",
              "custom_fields.custom_label_position",
              "custom_fields.date_value",
              "custom_fields.date_value.date",
              "custom_fields.date_value.date_time",
              "custom_fields.default_access_level",
              "custom_fields.description",
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
              "custom_fields.format",
              "custom_fields.has_notifications_enabled",
              "custom_fields.id_prefix",
              "custom_fields.input_restrictions",
              "custom_fields.is_formula_field",
              "custom_fields.is_global_to_workspace",
              "custom_fields.is_value_read_only",
              "custom_fields.multi_enum_values",
              "custom_fields.multi_enum_values.color",
              "custom_fields.multi_enum_values.enabled",
              "custom_fields.multi_enum_values.name",
              "custom_fields.name",
              "custom_fields.number_value",
              "custom_fields.people_value",
              "custom_fields.people_value.name",
              "custom_fields.precision",
              "custom_fields.privacy_setting",
              "custom_fields.reference_value",
              "custom_fields.reference_value.name",
              "custom_fields.representation_type",
              "custom_fields.resource_subtype",
              "custom_fields.text_value",
              "custom_fields.type",
              "custom_type",
              "custom_type.name",
              "custom_type_status_option",
              "custom_type_status_option.name",
              "dependencies",
              "dependents",
              "due_at",
              "due_on",
              "external",
              "external.data",
              "followers",
              "followers.name",
              "hearted",
              "hearts",
              "hearts.user",
              "hearts.user.name",
              "html_notes",
              "is_rendered_as_separator",
              "liked",
              "likes",
              "likes.user",
              "likes.user.name",
              "memberships",
              "memberships.project",
              "memberships.project.name",
              "memberships.section",
              "memberships.section.name",
              "modified_at",
              "name",
              "notes",
              "num_hearts",
              "num_likes",
              "num_subtasks",
              "parent",
              "parent.created_by",
              "parent.name",
              "parent.resource_subtype",
              "permalink_url",
              "projects",
              "projects.name",
              "resource_subtype",
              "start_at",
              "start_on",
              "tags",
              "tags.name",
              "workspace",
              "workspace.name"
            ],
            "schema": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "actual_time_minutes",
                  "approval_status",
                  "assigned_by",
                  "assigned_by.name",
                  "assignee",
                  "assignee.name",
                  "assignee_section",
                  "assignee_section.name",
                  "assignee_status",
                  "completed",
                  "completed_at",
                  "completed_by",
                  "completed_by.name",
                  "created_at",
                  "created_by",
                  "custom_fields",
                  "custom_fields.asana_created_field",
                  "custom_fields.created_by",
                  "custom_fields.created_by.name",
                  "custom_fields.currency_code",
                  "custom_fields.custom_label",
                  "custom_fields.custom_label_position",
                  "custom_fields.date_value",
                  "custom_fields.date_value.date",
                  "custom_fields.date_value.date_time",
                  "custom_fields.default_access_level",
                  "custom_fields.description",
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
                  "custom_fields.format",
                  "custom_fields.has_notifications_enabled",
                  "custom_fields.id_prefix",
                  "custom_fields.input_restrictions",
                  "custom_fields.is_formula_field",
                  "custom_fields.is_global_to_workspace",
                  "custom_fields.is_value_read_only",
                  "custom_fields.multi_enum_values",
                  "custom_fields.multi_enum_values.color",
                  "custom_fields.multi_enum_values.enabled",
                  "custom_fields.multi_enum_values.name",
                  "custom_fields.name",
                  "custom_fields.number_value",
                  "custom_fields.people_value",
                  "custom_fields.people_value.name",
                  "custom_fields.precision",
                  "custom_fields.privacy_setting",
                  "custom_fields.reference_value",
                  "custom_fields.reference_value.name",
                  "custom_fields.representation_type",
                  "custom_fields.resource_subtype",
                  "custom_fields.text_value",
                  "custom_fields.type",
                  "custom_type",
                  "custom_type.name",
                  "custom_type_status_option",
                  "custom_type_status_option.name",
                  "dependencies",
                  "dependents",
                  "due_at",
                  "due_on",
                  "external",
                  "external.data",
                  "followers",
                  "followers.name",
                  "hearted",
                  "hearts",
                  "hearts.user",
                  "hearts.user.name",
                  "html_notes",
                  "is_rendered_as_separator",
                  "liked",
                  "likes",
                  "likes.user",
                  "likes.user.name",
                  "memberships",
                  "memberships.project",
                  "memberships.project.name",
                  "memberships.section",
                  "memberships.section.name",
                  "modified_at",
                  "name",
                  "notes",
                  "num_hearts",
                  "num_likes",
                  "num_subtasks",
                  "parent",
                  "parent.created_by",
                  "parent.name",
                  "parent.resource_subtype",
                  "permalink_url",
                  "projects",
                  "projects.name",
                  "resource_subtype",
                  "start_at",
                  "start_on",
                  "tags",
                  "tags.name",
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
          "description": "The new parent of the subtask.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TaskSetParentRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully changed the parent of the specified subtask.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "$ref": "#/components/schemas/TaskResponse"
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
              "tasks:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nTask result = client.tasks.setParentForTask(taskGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The new parent of the subtask.\nlet task_gid = \"321654\"; // String | The task to operate on.\nlet opts = { \n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name\"\n};\ntasksApiInstance.setParentForTask(body, task_gid, opts).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.setParentForTask(taskGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The new parent of the subtask.\ntask_gid = \"321654\" # str | The task to operate on.\nopts = {\n    'opt_fields': \"actual_time_minutes,approval_status,assigned_by,assigned_by.name,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.input_restrictions,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.reference_value,custom_fields.reference_value.name,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name\", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.\n}\n\ntry:\n    # Set the parent of a task\n    api_response = tasks_api_instance.set_parent_for_task(body, task_gid, opts)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->set_parent_for_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.set_parent_for_task(task_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->setParentForTask($task_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.set_parent_for_task(task_gid: 'task_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tasks/{task_gid}/addProject": {
      "post": {
        "summary": "Add a project to a task",
        "description": "<b>Required scope: </b><code>tasks:write</code>\n\nAdds the task to the specified project, in the optional location\nspecified. If no location arguments are given, the task will be added to\nthe end of the project.\n\n`addProject` can also be used to reorder a task within a project or\nsection that already contains it.\n\n**Positioning the task:**\n- Use `insert_before` or `insert_after` with a task ID to position relative to another task\n- Use `section` alone to add the task to the end of a section\n- Use `section` with `insert_after: null` to add to the **beginning** of a section\n- Use `section` with `insert_before: null` to add to the **end** of a section\n- Use `section` with `insert_before` or `insert_after` (non-null) to position relative to a task within that section. The anchor task must be in the specified section.\n\nAt most one of `insert_before` or `insert_after` should be specified (both cannot be used together).\n\nA task can have at most 20 projects multi-homed to it.\n\nReturns an empty data block.",
        "tags": [
          "Tasks"
        ],
        "operationId": "addProjectForTask",
        "requestBody": {
          "description": "The project to add the task to.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TaskAddProjectRequest"
                  }
                }
              },
              "examples": {
                "addToEndOfSection": {
                  "summary": "Add task to end of a section",
                  "value": {
                    "data": {
                      "project": "13579",
                      "section": "987654"
                    }
                  }
                },
                "addToBeginningOfSection": {
                  "summary": "Add task to beginning of a section",
                  "value": {
                    "data": {
                      "project": "13579",
                      "section": "987654"
                    }
                  }
                },
                "addAfterTaskInSection": {
                  "summary": "Add task after another task in a section",
                  "value": {
                    "data": {
                      "project": "13579",
                      "section": "987654",
                      "insert_after": "124816"
                    }
                  }
                },
                "addBeforeTaskInSection": {
                  "summary": "Add task before another task in a section",
                  "value": {
                    "data": {
                      "project": "13579",
                      "section": "987654",
                      "insert_before": "432134"
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully added the specified project to the task.",
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
              "tasks:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.tasks.addProjectForTask(taskGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The project to add the task to.\nlet task_gid = \"321654\"; // String | The task to operate on.\n\ntasksApiInstance.addProjectForTask(body, task_gid).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.addProjectForTask(taskGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The project to add the task to.\ntask_gid = \"321654\" # str | The task to operate on.\n\n\ntry:\n    # Add a project to a task\n    api_response = tasks_api_instance.add_project_for_task(body, task_gid)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->add_project_for_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.add_project_for_task(task_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->addProjectForTask($task_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.add_project_for_task(task_gid: 'task_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tasks/{task_gid}/removeProject": {
      "post": {
        "summary": "Remove a project from a task",
        "description": "<b>Required scope: </b><code>tasks:write</code>\n\nRemoves the task from the specified project. The task will still exist in\nthe system, but it will not be in the project anymore.\n\nReturns an empty data block.",
        "tags": [
          "Tasks"
        ],
        "operationId": "removeProjectForTask",
        "requestBody": {
          "description": "The project to remove the task from.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TaskRemoveProjectRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully removed the specified project from the task.",
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
              "tasks:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.tasks.removeProjectForTask(taskGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The project to remove the task from.\nlet task_gid = \"321654\"; // String | The task to operate on.\n\ntasksApiInstance.removeProjectForTask(body, task_gid).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.removeProjectForTask(taskGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The project to remove the task from.\ntask_gid = \"321654\" # str | The task to operate on.\n\n\ntry:\n    # Remove a project from a task\n    api_response = tasks_api_instance.remove_project_for_task(body, task_gid)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->remove_project_for_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.remove_project_for_task(task_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->removeProjectForTask($task_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.remove_project_for_task(task_gid: 'task_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tasks/{task_gid}/addTag": {
      "post": {
        "summary": "Add a tag to a task",
        "description": "<b>Required scope: </b><code>tasks:write</code>\n\nAdds a tag to a task. Returns an empty data block.",
        "tags": [
          "Tasks"
        ],
        "operationId": "addTagForTask",
        "requestBody": {
          "description": "The tag to add to the task.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TaskAddTagRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully added the specified tag to the task.",
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
              "tasks:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.tasks.addTagForTask(taskGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The tag to add to the task.\nlet task_gid = \"321654\"; // String | The task to operate on.\n\ntasksApiInstance.addTagForTask(body, task_gid).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.addTagForTask(taskGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The tag to add to the task.\ntask_gid = \"321654\" # str | The task to operate on.\n\n\ntry:\n    # Add a tag to a task\n    api_response = tasks_api_instance.add_tag_for_task(body, task_gid)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->add_tag_for_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.add_tag_for_task(task_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->addTagForTask($task_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.add_tag_for_task(task_gid: 'task_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    },
    "/tasks/{task_gid}/removeTag": {
      "post": {
        "summary": "Remove a tag from a task",
        "description": "<b>Required scope: </b><code>tasks:write</code>\n\nRemoves a tag from a task. Returns an empty data block.",
        "tags": [
          "Tasks"
        ],
        "operationId": "removeTagForTask",
        "requestBody": {
          "description": "The tag to remove from the task.",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "data": {
                    "$ref": "#/components/schemas/TaskRemoveTagRequest"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully removed the specified tag from the task.",
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
              "tasks:write"
            ]
          }
        ],
        "x-readme": {
          "code-samples": [
            {
              "language": "java",
              "install": "<dependency><groupId>com.asana</groupId><artifactId>asana</artifactId><version>1.0.0</version></dependency>",
              "code": "import com.asana.Client;\n\nClient client = Client.accessToken(\"PERSONAL_ACCESS_TOKEN\");\n\nJsonElement result = client.tasks.removeTagForTask(taskGid)\n    .data(\"field\", \"value\")\n    .data(\"field\", \"value\")\n    .option(\"pretty\", true)\n    .execute();"
            },
            {
              "language": "node",
              "install": "npm install asana",
              "code": "const Asana = require('asana');\n\nlet client = new Asana.ApiClient();\nclient.authentications.token.accessToken = '<YOUR_ACCESS_TOKEN>';\n\nlet tasksApiInstance = new Asana.TasksApi(client);\nlet body = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}}; // Object | The tag to remove from the task.\nlet task_gid = \"321654\"; // String | The task to operate on.\n\ntasksApiInstance.removeTagForTask(body, task_gid).then((result) => {\n    console.log('API called successfully. Returned data: ' + JSON.stringify(result.data, null, 2));\n}, (error) => {\n    console.error(error.response.body);\n});",
              "name": "node-sdk-v3"
            },
            {
              "language": "node",
              "install": "npm install asana@1.0.5",
              "code": "const asana = require('asana');\n\nconst client = asana.Client.create().useAccessToken('PERSONAL_ACCESS_TOKEN');\n\nclient.tasks.removeTagForTask(taskGid, {field: \"value\", field: \"value\", pretty: true})\n    .then((result) => {\n        console.log(result);\n    });",
              "name": "node-sdk-v1"
            },
            {
              "language": "python",
              "install": "pip install asana",
              "code": "import asana\nfrom asana.rest import ApiException\nfrom pprint import pprint\n\nconfiguration = asana.Configuration()\nconfiguration.access_token = '<YOUR_ACCESS_TOKEN>'\napi_client = asana.ApiClient(configuration)\n\n# create an instance of the API class\ntasks_api_instance = asana.TasksApi(api_client)\nbody = {\"data\": {\"<PARAM_1>\": \"<VALUE_1>\", \"<PARAM_2>\": \"<VALUE_2>\",}} # dict | The tag to remove from the task.\ntask_gid = \"321654\" # str | The task to operate on.\n\n\ntry:\n    # Remove a tag from a task\n    api_response = tasks_api_instance.remove_tag_for_task(body, task_gid)\n    pprint(api_response)\nexcept ApiException as e:\n    print(\"Exception when calling TasksApi->remove_tag_for_task: %s\\n\" % e)",
              "name": "python-sdk-v5"
            },
            {
              "language": "python",
              "install": "pip install asana==3.2.3",
              "code": "import asana\n\nclient = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')\n\nresult = client.tasks.remove_tag_for_task(task_gid, {'field': 'value', 'field': 'value'}, opt_pretty=True)",
              "name": "python-sdk-v3"
            },
            {
              "language": "php",
              "install": "composer require asana/asana",
              "code": "<?php\nrequire 'vendor/autoload.php';\n\n$client = Asana\\Client::accessToken('PERSONAL_ACCESS_TOKEN');\n\n$result = $client->tasks->removeTagForTask($task_gid, array('field' => 'value', 'field' => 'value'), array('opt_pretty' => 'true'))"
            },
            {
              "language": "ruby",
              "install": "gem install asana",
              "code": "require 'asana'\n\nclient = Asana::Client.new do |c|\n    c.authentication :access_token, 'PERSONAL_ACCESS_TOKEN'\nend\n\nresult = client.tasks.remove_tag_for_task(task_gid: 'task_gid', field: \"value\", field: \"value\", options: {pretty: true})"
            }
          ]
        }
      }
    }
  },
  "schemas": {
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
    "TaskBase": {
      "allOf": [
        {
          "$ref": "#/components/schemas/TaskCompact"
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
                  "$ref": "#/components/schemas/UserCompact"
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
                  "$ref": "#/components/schemas/UserCompact"
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
                "$ref": "#/components/schemas/AsanaResource"
              },
              "readOnly": true
            },
            "dependents": {
              "description": "[Opt In](/docs/inputoutput-options). Array of resources referencing tasks that depend on this task. The objects contain only the ID of the dependent.",
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/AsanaResource"
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
                "$ref": "#/components/schemas/Like"
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
                "$ref": "#/components/schemas/Like"
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
                    "$ref": "#/components/schemas/ProjectCompact"
                  },
                  "section": {
                    "$ref": "#/components/schemas/SectionCompact"
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
    "AsanaResource": {
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
        }
      }
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
    "TaskResponse": {
      "allOf": [
        {
          "$ref": "#/components/schemas/TaskBase"
        },
        {
          "type": "object",
          "properties": {
            "assignee": {
              "allOf": [
                {
                  "$ref": "#/components/schemas/UserCompact"
                },
                {
                  "nullable": true
                }
              ]
            },
            "assignee_section": {
              "allOf": [
                {
                  "$ref": "#/components/schemas/SectionCompact"
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
                "$ref": "#/components/schemas/CustomFieldResponse"
              },
              "readOnly": true
            },
            "custom_type": {
              "allOf": [
                {
                  "$ref": "#/components/schemas/CustomTypeCompact"
                },
                {
                  "nullable": true
                }
              ]
            },
            "custom_type_status_option": {
              "allOf": [
                {
                  "$ref": "#/components/schemas/CustomTypeStatusOptionCompact"
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
                "$ref": "#/components/schemas/UserCompact"
              }
            },
            "parent": {
              "allOf": [
                {
                  "$ref": "#/components/schemas/TaskCompact"
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
                "$ref": "#/components/schemas/ProjectCompact"
              }
            },
            "tags": {
              "description": "Array of tags associated with this task. In order to change tags on an existing task use `addTag` and `removeTag`.",
              "type": "array",
              "readOnly": true,
              "items": {
                "$ref": "#/components/schemas/TagCompact"
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
                  "$ref": "#/components/schemas/WorkspaceCompact"
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
    "EmptyResponse": {
      "type": "object",
      "description": "An empty object. Some endpoints do not return an object on success. The success is conveyed through a 2-- status code and returning an empty object."
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
    "CustomTypeCompact": {
      "description": "Custom Types extend the types of Asana Objects, currently only Custom Tasks are supported.",
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
          "example": "custom_type",
          "x-insert-after": "gid"
        },
        "name": {
          "type": "string",
          "description": "The name of the custom type.",
          "example": "Bug ticket"
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
    "TaskRequest": {
      "allOf": [
        {
          "$ref": "#/components/schemas/TaskBase"
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
          "$ref": "#/components/schemas/UserCompact"
        }
      }
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
    "JobBase": {
      "$ref": "#/components/schemas/JobCompact"
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
    "CustomTypeStatusOptionCompact": {
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
          "example": "custom_type_status_option",
          "x-insert-after": "gid"
        },
        "name": {
          "type": "string",
          "description": "The name of the custom type status option.",
          "example": "Solution pending"
        }
      }
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
        "$ref": "#/components/schemas/TaskResponse"
      }
    }
  }
}
```

### Relationship manifest

```yaml
asana_tasks:
  user_id:
    target_table: asana_users
    target_column: id
    confidence: high
    reason: 'response schema: data.hearts[].user.gid'
  project_id:
    target_table: asana_projects
    target_column: id
    confidence: high
    reason: 'response schema: data.memberships[].project.gid'
  section_id:
    target_table: asana_sections
    target_column: id
    confidence: high
    reason: 'response schema: data.memberships[].section.gid'
  parent_id:
    target_table: asana_tasks
    target_column: id
    confidence: high
    reason: 'response schema: data.parent.gid'
  workspace_id:
    target_table: asana_workspaces
    target_column: id
    confidence: high
    reason: 'response schema: data.workspace.gid'
  tag_id:
    target_table: asana_tags
    target_column: id
    confidence: high
    reason: 'request body on POST /tasks/{task_gid}/addTag: data.tag'

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
  "sections": {
    "primary_response_schema": {
      "type": "object",
      "properties": {
        "data": {
          "$ref": "#/components/schemas/SectionResponse"
        }
      }
    }
  },
  "tags": {
    "primary_response_schema": {
      "type": "object",
      "properties": {
        "data": {
          "$ref": "#/components/schemas/TagResponse"
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

Resource `task` uses: alphabet=ALPHANUMERIC, length=16

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

Add a class `Task(Base)` with:

- Table name: `asana_tasks`
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
