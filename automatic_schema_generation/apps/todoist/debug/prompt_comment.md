# Entity Implementation: comments

You are implementing the **comments** resource for the Todoist API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for comments

```json
{
  "paths": {
    "/api/v1/comments/{comment_id}": {
      "delete": {
        "tags": [
          "Comments"
        ],
        "summary": "Delete Comment",
        "description": "Delete a comment by ID",
        "operationId": "delete_comment_api_v1_comments__comment_id__delete",
        "parameters": [
          {
            "name": "comment_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "description": "String ID of the comment",
              "examples": [
                "6XGgmFQrx44wfGHr"
              ],
              "title": "Comment Id"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "400": {
            "description": "Bad Request"
          },
          "401": {
            "description": "Unauthorized"
          },
          "403": {
            "description": "Forbidden"
          },
          "404": {
            "description": "Not Found"
          }
        }
      },
      "get": {
        "tags": [
          "Comments"
        ],
        "summary": "Get Comment",
        "description": "Returns a single comment by ID",
        "operationId": "get_comment_api_v1_comments__comment_id__get",
        "parameters": [
          {
            "name": "comment_id",
            "in": "path",
            "required": true,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "description": "String ID of the comment",
              "examples": [
                "6XGgmFVcrG5RRjVr"
              ],
              "title": "Comment Id"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/NoteSyncView"
                }
              }
            }
          },
          "400": {
            "description": "Bad Request"
          },
          "401": {
            "description": "Unauthorized"
          },
          "403": {
            "description": "Forbidden"
          },
          "404": {
            "description": "Not Found"
          }
        }
      },
      "post": {
        "tags": [
          "Comments"
        ],
        "summary": "Update Comment",
        "description": "Update a comment by ID and returns its content",
        "operationId": "update_comment_api_v1_comments__comment_id__post",
        "parameters": [
          {
            "name": "comment_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "description": "String ID of the comment",
              "examples": [
                "6XGgmFQrx44wfGHr"
              ],
              "title": "Comment Id"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Body_61d93e0e"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "anyOf": [
                    {
                      "$ref": "#/components/schemas/NoteSyncView"
                    },
                    {
                      "type": "null"
                    }
                  ],
                  "title": "Response Update Comment Api V1 Comments  Comment Id  Post"
                }
              }
            }
          },
          "400": {
            "description": "Bad Request"
          },
          "401": {
            "description": "Unauthorized"
          },
          "403": {
            "description": "Forbidden"
          },
          "404": {
            "description": "Not Found"
          }
        }
      }
    },
    "/api/v1/comments": {
      "post": {
        "tags": [
          "Comments"
        ],
        "summary": "Create Comment",
        "description": "Creates a new comment on a project or task and returns it.\n\nExactly one of `task_id` or `project_id` arguments is required. Providing\nneither or both will return an error.",
        "operationId": "create_comment_api_v1_comments_post",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Body_28d2b1b0"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/NoteSyncView"
                }
              }
            }
          },
          "400": {
            "description": "Bad Request"
          },
          "401": {
            "description": "Unauthorized"
          },
          "403": {
            "description": "Forbidden"
          },
          "404": {
            "description": "Not Found"
          }
        },
        "x-codeSamples": [
          {
            "lang": "curl",
            "source": "\n$ cat > /tmp/note.json\n{\n    \"task_id\": \"6X6WMMqgq2PWxjCX\",\n    \"content\": \"Need one bottle of milk\",\n    \"attachment\": {\n        \"resource_type\": \"file\",\n        \"file_url\": \"https://s3.amazonaws.com/domorebetter/Todoist+Setup+Guide.pdf\",\n        \"file_type\": \"application/pdf\",\n        \"file_name\": \"File.pdf\"\n    }\n}\n^C\n\n$ curl \"https://api.todoist.com/api/v1/comments\" \\\n    -X POST \\\n    --data @/tmp/note.json \\\n    -H \"Content-Type: application/json\" \\\n    -H \"X-Request-Id: $(uuidgen)\" \\\n    -H \"Authorization: Bearer $token\"\n"
          }
        ]
      },
      "get": {
        "tags": [
          "Comments"
        ],
        "summary": "Get Comments",
        "description": "Get all comments for a given task or project.\n\nExactly one of `task_id` or `project_id` arguments is required. Providing\nneither or both will return an error.\n\nThis is a paginated endpoint. See the [Pagination guide](#tag/Pagination) for details on using cursor-based pagination.",
        "operationId": "get_comments_api_v1_comments_get",
        "parameters": [
          {
            "name": "project_id",
            "in": "query",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "description": "String ID of the project",
              "examples": [
                "6XGgm6PHrGgMpCFX"
              ],
              "title": "Project Id"
            }
          },
          {
            "name": "task_id",
            "in": "query",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "description": "String ID of the task",
              "examples": [
                "6XGgmFVcrG5RRjVr"
              ],
              "title": "Task Id"
            }
          },
          {
            "name": "cursor",
            "in": "query",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string",
                  "minLength": 1,
                  "pattern": "^[0-9a-zA-Z_-]+\\.[0-9a-zA-Z_-]+$",
                  "description": "An opaque string used as the cursor for pagination. Must be used with the same parameters from the previous request",
                  "examples": [
                    "14540000435w8hj8pXXwPQJJch.X9DBH8ya2Xenok55"
                  ]
                },
                {
                  "type": "null"
                }
              ],
              "title": "Cursor"
            }
          },
          {
            "name": "limit",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "maximum": 200,
              "exclusiveMinimum": 0,
              "description": "The number of objects to return in a page",
              "default": 50,
              "title": "Limit"
            }
          },
          {
            "name": "public_key",
            "in": "query",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "Public Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/PaginatedList_NoteSyncView_"
                }
              }
            }
          },
          "400": {
            "description": "Bad Request"
          },
          "401": {
            "description": "Unauthorized"
          },
          "403": {
            "description": "Forbidden"
          },
          "404": {
            "description": "Not Found"
          }
        }
      }
    }
  },
  "schemas": {
    "Body_61d93e0e": {
      "properties": {
        "content": {
          "anyOf": [
            {
              "type": "string",
              "maxLength": 15000,
              "minLength": 1
            },
            {
              "type": "null"
            }
          ],
          "title": "Content",
          "description": "New content for the comment. If null or an empty string, no update is performed."
        }
      },
      "type": "object",
      "required": [
        "content"
      ],
      "title": "Body"
    },
    "NoteSyncView": {
      "properties": {
        "id": {
          "type": "string",
          "title": "Id"
        },
        "posted_uid": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Posted Uid"
        },
        "content": {
          "type": "string",
          "title": "Content",
          "default": ""
        },
        "file_attachment": {
          "anyOf": [
            {
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string"
                  },
                  {
                    "type": "integer"
                  },
                  {
                    "items": {},
                    "type": "array"
                  },
                  {
                    "additionalProperties": true,
                    "type": "object"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "title": "File Attachment"
        },
        "uids_to_notify": {
          "anyOf": [
            {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "title": "Uids To Notify"
        },
        "is_deleted": {
          "type": "boolean",
          "title": "Is Deleted"
        },
        "posted_at": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Posted At"
        },
        "reactions": {
          "anyOf": [
            {
              "additionalProperties": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              },
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "title": "Reactions"
        }
      },
      "type": "object",
      "required": [
        "id",
        "posted_uid",
        "file_attachment",
        "uids_to_notify",
        "is_deleted",
        "posted_at",
        "reactions"
      ],
      "title": "NoteSyncView",
      "description": "The base class for NoteSyncViews, to be extended for Items and Projects.\n\nThis class should generally not be instantiated directly, as it serves as a\ncommon structure for Items and Projects."
    },
    "PaginatedList_NoteSyncView_": {
      "properties": {
        "results": {
          "items": {
            "$ref": "#/components/schemas/NoteSyncView"
          },
          "type": "array",
          "title": "Results"
        },
        "next_cursor": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Next Cursor"
        }
      },
      "type": "object",
      "required": [
        "results",
        "next_cursor"
      ],
      "title": "PaginatedList"
    },
    "Body_28d2b1b0": {
      "properties": {
        "content": {
          "type": "string",
          "maxLength": 15000,
          "minLength": 1,
          "title": "Content",
          "description": "Content of the comment"
        },
        "project_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Project Id",
          "description": "String ID of the project",
          "examples": [
            "6XGgm6PHrGgMpCFX"
          ]
        },
        "task_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Task Id",
          "description": "String ID of the task",
          "examples": [
            "6XGgmFVcrG5RRjVr"
          ]
        },
        "attachment": {
          "anyOf": [
            {
              "additionalProperties": true,
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "title": "Attachment",
          "description": "A [File attachment](#tag/Sync/Comments/File-Attachments) object",
          "examples": [
            {
              "file_name": "File.pdf",
              "file_type": "application/pdf",
              "file_url": "https://s3.amazonaws.com/domorebetter/Todoist+Setup+Guide.pdf",
              "resource_type": "file"
            }
          ]
        },
        "uids_to_notify": {
          "anyOf": [
            {
              "items": {
                "type": "integer"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "title": "Uids To Notify",
          "description": "Optional list of user IDs to notify about this comment.",
          "examples": [
            [
              12345678,
              23456789
            ]
          ]
        }
      },
      "type": "object",
      "required": [
        "content"
      ],
      "title": "Body"
    }
  },
  "primary_response_schema": {
    "properties": {
      "id": {
        "type": "string",
        "title": "Id"
      },
      "posted_uid": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Posted Uid"
      },
      "content": {
        "type": "string",
        "title": "Content",
        "default": ""
      },
      "file_attachment": {
        "anyOf": [
          {
            "additionalProperties": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "integer"
                },
                {
                  "items": {},
                  "type": "array"
                },
                {
                  "additionalProperties": true,
                  "type": "object"
                },
                {
                  "type": "null"
                }
              ]
            },
            "type": "object"
          },
          {
            "type": "null"
          }
        ],
        "title": "File Attachment"
      },
      "uids_to_notify": {
        "anyOf": [
          {
            "items": {
              "type": "string"
            },
            "type": "array"
          },
          {
            "type": "null"
          }
        ],
        "title": "Uids To Notify"
      },
      "is_deleted": {
        "type": "boolean",
        "title": "Is Deleted"
      },
      "posted_at": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Posted At"
      },
      "reactions": {
        "anyOf": [
          {
            "additionalProperties": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "type": "object"
          },
          {
            "type": "null"
          }
        ],
        "title": "Reactions"
      }
    },
    "type": "object",
    "required": [
      "id",
      "posted_uid",
      "file_attachment",
      "uids_to_notify",
      "is_deleted",
      "posted_at",
      "reactions"
    ],
    "title": "NoteSyncView",
    "description": "The base class for NoteSyncViews, to be extended for Items and Projects.\n\nThis class should generally not be instantiated directly, as it serves as a\ncommon structure for Items and Projects."
  }
}
```

### Relationship manifest

```yaml
todoist_comments:
  posted_uid:
    target_table: todoist_user
    target_column: id
    confidence: high
    reason: 'response schema: posted_uid'
  project_id:
    target_table: todoist_projects
    target_column: id
    confidence: high
    reason: 'query param on GET /api/v1/comments: project_id'
  task_id:
    target_table: todoist_tasks
    target_column: id
    confidence: high
    reason: 'query param on GET /api/v1/comments: task_id'

```

### FK dependency schemas (for stub creation if needed)

```json
{
  "projects": {
    "primary_response_schema": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/PersonalProjectSyncView"
        },
        {
          "$ref": "#/components/schemas/WorkspaceProjectSyncView"
        }
      ],
      "title": "Response Get Project Api V1 Projects  Project Id  Get",
      "description": "Can be either a personal or a workspace project."
    }
  },
  "tasks": {
    "primary_response_schema": {
      "properties": {
        "user_id": {
          "type": "string",
          "title": "User Id"
        },
        "id": {
          "type": "string",
          "title": "Id"
        },
        "project_id": {
          "type": "string",
          "title": "Project Id"
        },
        "section_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Section Id"
        },
        "parent_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Parent Id"
        },
        "added_by_uid": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Added By Uid"
        },
        "assigned_by_uid": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Assigned By Uid"
        },
        "responsible_uid": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Responsible Uid"
        },
        "labels": {
          "items": {
            "type": "string"
          },
          "type": "array",
          "title": "Labels"
        },
        "deadline": {
          "anyOf": [
            {
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "title": "Deadline"
        },
        "duration": {
          "anyOf": [
            {
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "integer"
                  },
                  {
                    "type": "string"
                  }
                ]
              },
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "title": "Duration"
        },
        "is_collapsed": {
          "type": "boolean",
          "title": "Is Collapsed"
        },
        "checked": {
          "type": "boolean",
          "title": "Checked",
          "examples": [
            false
          ]
        },
        "is_deleted": {
          "type": "boolean",
          "title": "Is Deleted",
          "examples": [
            false
          ]
        },
        "added_at": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Added At"
        },
        "completed_at": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Completed At"
        },
        "completed_by_uid": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Completed By Uid"
        },
        "updated_at": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Updated At"
        },
        "due": {
          "anyOf": [
            {
              "additionalProperties": true,
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "title": "Due"
        },
        "priority": {
          "type": "integer",
          "title": "Priority"
        },
        "child_order": {
          "type": "integer",
          "title": "Child Order"
        },
        "content": {
          "type": "string",
          "title": "Content"
        },
        "description": {
          "type": "string",
          "title": "Description"
        },
        "note_count": {
          "type": "integer",
          "title": "Note Count",
          "description": "**Deprecated**: only returning 0 and is marked for removal",
          "examples": [
            0
          ]
        },
        "day_order": {
          "type": "integer",
          "title": "Day Order"
        },
        "goal_ids": {
          "items": {
            "type": "string"
          },
          "type": "array",
          "title": "Goal Ids"
        }
      },
      "type": "object",
      "required": [
        "user_id",
        "id",
        "project_id",
        "section_id",
        "parent_id",
        "added_by_uid",
        "assigned_by_uid",
        "responsible_uid",
        "labels",
        "deadline",
        "duration",
        "is_collapsed",
        "checked",
        "is_deleted",
        "added_at",
        "completed_at",
        "completed_by_uid",
        "updated_at",
        "due",
        "priority",
        "child_order",
        "content",
        "description",
        "note_count",
        "day_order",
        "goal_ids"
      ],
      "title": "ItemSyncView",
      "description": "A class with fields representing an ItemView which will be returned to\nclients in a sync (or sync-like) response."
    }
  },
  "user": {
    "primary_response_schema": {
      "properties": {
        "id": {
          "type": "string",
          "title": "Id",
          "description": "User ID"
        },
        "email": {
          "type": "string",
          "title": "Email",
          "description": "User's email address"
        },
        "full_name": {
          "type": "string",
          "title": "Full Name",
          "description": "The user's real name formatted as Firstname Lastname"
        },
        "has_password": {
          "type": "boolean",
          "title": "Has Password",
          "description": "Whether the user has a password set on the account. It will be false if they have only authenticated without a password (e.g. using Google, Facebook, etc.)"
        },
        "verification_status": {
          "type": "string",
          "enum": [
            "unverified",
            "verified",
            "blocked",
            "legacy"
          ],
          "title": "Verification Status",
          "description": "User's email verification status. unverified (just signed up), verified (verified email or social login), blocked (failed to verify in 7 days), legacy (signed up before August 2022)"
        },
        "mfa_enabled": {
          "type": "boolean",
          "title": "Mfa Enabled",
          "description": "Whether multi-factor authentication is enabled"
        },
        "token": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Token",
          "description": "The user's token that should be used to call the other API methods"
        },
        "is_premium": {
          "type": "boolean",
          "title": "Is Premium",
          "description": "Whether the user has a Todoist Pro subscription (a true or false value)"
        },
        "premium_status": {
          "anyOf": [
            {
              "type": "string",
              "enum": [
                "not_premium",
                "current_personal_plan",
                "legacy_personal_plan",
                "teams_business_member"
              ]
            },
            {
              "type": "null"
            }
          ],
          "title": "Premium Status",
          "description": "Outlines why a user is premium, possible values are: not_premium, current_personal_plan, legacy_personal_plan or teams_business_member"
        },
        "premium_until": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Premium Until",
          "description": "The date when the user's Todoist Pro subscription ends (null if not a Todoist Pro user). This should be used for informational purposes only as this does not include the grace period upon expiration"
        },
        "free_trial_expires": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Free Trial Expires",
          "description": "Date when free trial expires (ISO 8601 format)"
        },
        "has_started_a_trial": {
          "type": "boolean",
          "title": "Has Started A Trial",
          "description": "Whether the user has ever started a free trial"
        },
        "joined_at": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Joined At",
          "description": "Date when user joined Todoist (ISO 8601 format)"
        },
        "is_deleted": {
          "type": "boolean",
          "title": "Is Deleted",
          "description": "Whether the user is deleted",
          "default": false
        },
        "deleted_at": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Deleted At",
          "description": "Date when user was deleted (ISO 8601 format)"
        },
        "business_account_id": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "title": "Business Account Id",
          "description": "The ID of the user's business account"
        },
        "date_format": {
          "type": "integer",
          "enum": [
            0,
            1
          ],
          "title": "Date Format",
          "description": "Whether to use the DD-MM-YYYY date format (if set to 0), or the MM-DD-YYYY format (if set to 1)"
        },
        "time_format": {
          "anyOf": [
            {
              "type": "integer",
              "enum": [
                0,
                1
              ]
            },
            {
              "type": "null"
            }
          ],
          "title": "Time Format",
          "description": "Whether to use a 24h format such as 13:00 (if set to 0) when displaying time, or a 12h format such as 1:00pm (if set to 1)"
        },
        "sort_order": {
          "type": "integer",
          "enum": [
            0,
            1
          ],
          "title": "Sort Order",
          "description": "Whether to show projects in an oldest dates first order (if set to 0), or a oldest dates last order (if set to 1)"
        },
        "theme_id": {
          "type": "string",
          "title": "Theme Id",
          "description": "The currently selected Todoist theme (a number between 0 and 13)"
        },
        "start_day": {
          "type": "integer",
          "maximum": 7.0,
          "minimum": 1.0,
          "title": "Start Day",
          "description": "The first day of the week (between 1 and 7, where 1 is Monday and 7 is Sunday)"
        },
        "weekend_start_day": {
          "type": "integer",
          "maximum": 7.0,
          "minimum": 1.0,
          "title": "Weekend Start Day",
          "description": "The day used when a user chooses to schedule a task for the 'Weekend' (between 1 and 7, where 1 is Monday and 7 is Sunday)"
        },
        "next_week": {
          "type": "integer",
          "maximum": 7.0,
          "minimum": 1.0,
          "title": "Next Week",
          "description": "The day of the next week, that tasks will be postponed to (between 1 and 7, where 1 is Monday and 7 is Sunday)"
        },
        "auto_reminder": {
          "type": "integer",
          "title": "Auto Reminder",
          "description": "The default time in minutes for the automatic reminders set, whenever a due date has been specified for a task"
        },
        "urgent_reminder_device": {
          "anyOf": [
            {
              "$ref": "#/components/schemas/UrgentReminderDeviceView"
            },
            {
              "type": "null"
            }
          ],
          "description": "The device that should ring urgent reminders. Contains device_id, device_token, device_platform (ios or android), and optionally device_name."
        },
        "start_page": {
          "type": "string",
          "title": "Start Page",
          "description": "The user's default view on Todoist. The start page can be one of the following: inbox, teaminbox, today, next7days, project?id=1234 to open a project, label?name=abc to open a label, or filter?id=1234 to open a filter"
        },
        "inbox_project_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Inbox Project Id",
          "description": "The ID of the user's Inbox project"
        },
        "lang": {
          "type": "string",
          "enum": [
            "cs",
            "da",
            "de",
            "en",
            "es",
            "fi",
            "fr",
            "it",
            "ja",
            "ko",
            "nl",
            "pl",
            "pt_BR",
            "ru",
            "sv",
            "tr",
            "zh_CN",
            "zh_TW"
          ],
          "title": "Lang",
          "description": "The user's language"
        },
        "tz_info": {
          "additionalProperties": true,
          "type": "object",
          "title": "Tz Info",
          "description": "The user's timezone (a dictionary structure), which includes the following elements: the timezone as a string value, the hours and minutes difference from GMT, whether daylight saving time applies denoted by is_dst, and a string value of the time difference from GMT that is gmt_string"
        },
        "karma": {
          "type": "number",
          "title": "Karma",
          "description": "The user's karma score"
        },
        "karma_trend": {
          "anyOf": [
            {
              "type": "string",
              "enum": [
                "up",
                "down",
                "-"
              ]
            },
            {
              "type": "null"
            }
          ],
          "title": "Karma Trend",
          "description": "The user's karma trend. Can be 'up', 'down', or '-' (no change)"
        },
        "daily_goal": {
          "type": "integer",
          "title": "Daily Goal",
          "description": "The daily goal number of completed tasks for karma"
        },
        "weekly_goal": {
          "type": "integer",
          "title": "Weekly Goal",
          "description": "The target number of tasks to complete per week"
        },
        "days_off": {
          "items": {
            "type": "integer"
          },
          "type": "array",
          "title": "Days Off",
          "description": "Array of integers representing user's days off (between 1 and 7, where 1 is Monday and 7 is Sunday)"
        },
        "is_celebrations_enabled": {
          "type": "boolean",
          "title": "Is Celebrations Enabled",
          "description": "Whether celebration animations are enabled"
        },
        "completed_count": {
          "type": "integer",
          "title": "Completed Count",
          "description": "Total number of tasks completed by user"
        },
        "completed_today": {
          "type": "integer",
          "title": "Completed Today",
          "description": "Number of tasks completed today by the user"
        },
        "share_limit": {
          "type": "integer",
          "title": "Share Limit",
          "description": "Maximum number of collaborators allowed in shared projects"
        },
        "features": {
          "additionalProperties": true,
          "type": "object",
          "title": "Features",
          "description": "Feature flags and settings for the user"
        },
        "feature_identifier": {
          "type": "string",
          "title": "Feature Identifier",
          "description": "Feature identifier for feature flag evaluations"
        },
        "joinable_workspace": {
          "anyOf": [
            {
              "additionalProperties": true,
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "title": "Joinable Workspace",
          "description": "Information about workspaces the user can join"
        },
        "onboarding_completed": {
          "type": "boolean",
          "title": "Onboarding Completed",
          "description": "Whether the user has completed onboarding"
        },
        "onboarding_initiated": {
          "type": "boolean",
          "title": "Onboarding Initiated",
          "description": "Whether the user has initiated onboarding"
        },
        "onboarding_started": {
          "type": "boolean",
          "title": "Onboarding Started",
          "description": "Whether the user has started onboarding"
        },
        "onboarding_level": {
          "anyOf": [
            {
              "type": "string",
              "enum": [
                "beginner",
                "intermediate",
                "pro"
              ]
            },
            {
              "type": "null"
            }
          ],
          "title": "Onboarding Level",
          "description": "User's self-reported skill level during onboarding"
        },
        "onboarding_persona": {
          "anyOf": [
            {
              "type": "string",
              "enum": [
                "analog",
                "tasks",
                "calendar",
                "organic"
              ]
            },
            {
              "type": "null"
            }
          ],
          "title": "Onboarding Persona",
          "description": "User's onboarding persona selection"
        },
        "onboarding_role": {
          "anyOf": [
            {
              "type": "string",
              "enum": [
                "leader",
                "founder",
                "ic"
              ]
            },
            {
              "type": "null"
            }
          ],
          "title": "Onboarding Role",
          "description": "User's role selection during onboarding"
        },
        "onboarding_team_mode": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Onboarding Team Mode",
          "description": "Whether user selected team mode during onboarding"
        },
        "onboarding_use_cases": {
          "anyOf": [
            {
              "items": {
                "type": "string",
                "enum": [
                  "personal",
                  "work",
                  "education",
                  "teamwork",
                  "solo",
                  "teamcreator",
                  "simple",
                  "teamjoiner"
                ]
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "title": "Onboarding Use Cases",
          "description": "Use cases the user selected during onboarding"
        },
        "getting_started_guide_projects": {
          "anyOf": [
            {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "title": "Getting Started Guide Projects",
          "description": "List of project IDs for getting started guide"
        },
        "activated_user": {
          "type": "boolean",
          "title": "Activated User",
          "description": "Whether the user is considered activated (completed key onboarding actions)"
        },
        "has_magic_number": {
          "type": "boolean",
          "title": "Has Magic Number",
          "description": "Whether the user has reached a magic number milestone"
        },
        "image_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Image Id",
          "description": "The ID of the user's avatar"
        },
        "avatar_big": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Avatar Big",
          "description": "The link to a 195x195 pixels image of the user's avatar"
        },
        "avatar_medium": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Avatar Medium",
          "description": "The link to a 60x60 pixels image of the user's avatar"
        },
        "avatar_s640": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Avatar S640",
          "description": "The link to a 640x640 pixels image of the user's avatar"
        },
        "avatar_small": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Avatar Small",
          "description": "The link to a 35x35 pixels image of the user's avatar"
        },
        "websocket_url": {
          "type": "string",
          "title": "Websocket Url",
          "description": "WebSocket URL for real-time updates"
        }
      },
      "type": "object",
      "required": [
        "id",
        "email",
        "full_name",
        "has_password",
        "verification_status",
        "mfa_enabled",
        "is_premium",
        "has_started_a_trial",
        "date_format",
        "sort_order",
        "theme_id",
        "start_day",
        "weekend_start_day",
        "next_week",
        "auto_reminder",
        "start_page",
        "lang",
        "tz_info",
        "karma",
        "daily_goal",
        "weekly_goal",
        "days_off",
        "is_celebrations_enabled",
        "completed_count",
        "completed_today",
        "share_limit",
        "features",
        "feature_identifier",
        "joinable_workspace",
        "onboarding_completed",
        "onboarding_initiated",
        "onboarding_started",
        "activated_user",
        "has_magic_number",
        "websocket_url"
      ],
      "title": "UserSyncView",
      "description": "A model for the user objects returned by the sync/REST API.\n\nThis model is used purely for OpenAPI documentation generation and does not\nhandle actual serialization (which is handled by @todoist.models.json.user.generate)."
    }
  }
}
```

### ID format

Resource `comment` uses: alphabet=ALPHANUMERIC, length=16

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

Add a class `Comment(Base)` with:

- Table name: `todoist_comments`
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
"""ORM schema for the Todoist API replica.

Models mirror the Todoist REST API response shapes. Field names use snake_case
to match the API's JSON keys (Todoist uses snake_case natively).

Personal and workspace projects are unified into a single table. Workspace-only
fields are nullable.
"""

from typing import Any, Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# STUB — expand when implementing this resource
class Folder(Base):
    """Todoist folder (workspace-level project grouping).

    Stub model — only enough for FK integrity. Expand when implementing
    the folders resource.
    """

    __tablename__ = "todoist_folders"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationships
    projects: Mapped[list["Project"]] = relationship(back_populates="folder")


# STUB — expand when implementing this resource
class Section(Base):
    """Todoist section within a project.

    Stub model — only enough for FK integrity. Expand when implementing
    the sections resource.
    """

    __tablename__ = "todoist_sections"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("todoist_projects.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationships
    project: Mapped["Project"] = relationship()
    tasks: Mapped[list["Task"]] = relationship(back_populates="section")


class User(Base):
    """Todoist user — maps to UserJSON / UserSyncView in the API.

    This is a minimal version covering fields needed for FK integrity and the
    GET /user endpoint. The full UserJSON schema has 50+ fields; most are stored
    in the settings JSONB column rather than as individual columns.
    """

    __tablename__ = "todoist_users"

    # Identity
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Account state
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Timestamps
    joined_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    deleted_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # All remaining UserJSON fields — preferences, onboarding, karma, avatars,
    # feature flags, etc. Stored as JSONB to avoid 40+ rarely-queried columns.
    settings: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Relationships
    created_projects: Mapped[list["Project"]] = relationship(back_populates="creator")
    owned_tasks: Mapped[list["Task"]] = relationship(
        back_populates="user", foreign_keys="Task.user_id"
    )


class Project(Base):
    """Todoist project — personal or workspace.

    Maps to PersonalProjectSyncView / WorkspaceProjectSyncView in the API.
    """

    __tablename__ = "todoist_projects"
    __table_args__ = (
        Index("ix_todoist_projects_creator", "creator_uid"),
        Index("ix_todoist_projects_workspace", "workspace_id"),
        Index("ix_todoist_projects_parent", "parent_id"),
    )

    # Identity
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # Hierarchy
    parent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_projects.id"), nullable=True
    )
    child_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    default_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Display
    color: Mapped[str] = mapped_column(String(50), nullable=False, default="charcoal")
    view_style: Mapped[str] = mapped_column(String(20), nullable=False, default="list")
    is_collapsed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_favorite: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # State flags
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_frozen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    inbox_project: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Permissions / sharing
    is_shared: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_assign_tasks: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    can_comment: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    public_key: Mapped[str] = mapped_column(String(255), nullable=False, default="")

    # Nested access object — stored as JSONB since we don't query on it.
    # Shape: {"visibility": "...", "configuration": {...}}
    access: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Ownership
    creator_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )

    # Timestamps — stored as strings to match Todoist API format
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # --- Workspace-only fields (nullable for personal projects) ---
    workspace_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    folder_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_folders.id"), nullable=True
    )
    status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    collaborator_role_default: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    is_invite_only: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_link_sharing_enabled: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True
    )
    is_pending_default_collaborator_invites: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True
    )
    is_project_insights_enabled: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True
    )

    # Relationships
    creator: Mapped[Optional["User"]] = relationship(back_populates="created_projects")
    folder: Mapped[Optional["Folder"]] = relationship(back_populates="projects")
    parent: Mapped[Optional["Project"]] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Project"]] = relationship(back_populates="parent")
    tasks: Mapped[list["Task"]] = relationship(back_populates="project")


class Task(Base):
    """Todoist task — maps to ItemSyncView in the API."""

    __tablename__ = "todoist_tasks"
    __table_args__ = (
        Index("ix_todoist_tasks_project", "project_id"),
        Index("ix_todoist_tasks_section", "section_id"),
        Index("ix_todoist_tasks_parent", "parent_id"),
        Index("ix_todoist_tasks_user", "user_id"),
    )

    # Identity
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # Hierarchy and placement
    project_id: Mapped[str] = mapped_column(
        ForeignKey("todoist_projects.id"), nullable=False
    )
    section_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_sections.id"), nullable=True
    )
    parent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_tasks.id"), nullable=True
    )
    child_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    day_order: Mapped[int] = mapped_column(Integer, nullable=False, default=-1)

    # Ownership and assignment
    user_id: Mapped[str] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=False
    )
    added_by_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )
    assigned_by_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )
    responsible_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )
    completed_by_uid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("todoist_users.id"), nullable=True
    )

    # State
    checked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_collapsed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Labels — stored as JSON array of strings
    labels: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Due date — nested object, stored as JSONB
    # Shape: {"date": "...", "string": "...", "lang": "...", "is_recurring": bool, "datetime": "..."}
    due: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Deadline — nested object, stored as JSONB
    # Shape: {"date": "...", "lang": "...", "is_recurring": bool}
    deadline: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Duration — nested object, stored as JSONB
    # Shape: {"amount": int, "unit": "minute"|"day"}
    duration: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Metadata
    note_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goal_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Timestamps
    added_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    completed_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="tasks")
    section: Mapped[Optional["Section"]] = relationship(back_populates="tasks")
    user: Mapped["User"] = relationship(
        back_populates="owned_tasks", foreign_keys=[user_id]
    )
    parent: Mapped[Optional["Task"]] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Task"]] = relationship(back_populates="parent")


class Label(Base):
    """Todoist label — maps to LabelRestView in the API."""

    __tablename__ = "todoist_labels"
    __table_args__ = (
        Index("ix_todoist_labels_order", "order"),
    )

    # Identity
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False, default="charcoal")
    
    # Organization
    order: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # State
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Timestamps
    created_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

```

### `database/operations.py`

```python
"""Session-first CRUD operations for Todoist resources.

Every function takes a SQLAlchemy Session as the first argument. No function
accesses request state directly — that translation happens in the route layer.
"""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .schema import Label, Project, Task
from ..core.utils import generate_id, now_iso


# ============================================================================
# PROJECT QUERIES
# ============================================================================


def get_project(session: Session, project_id: str) -> Project | None:
    """Get a single project by ID. Returns None if not found or deleted."""
    return session.execute(
        select(Project).where(Project.id == project_id, Project.is_deleted.is_(False))
    ).scalar_one_or_none()


def list_projects(
    session: Session,
    *,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Project], str | None]:
    """List active (non-archived, non-deleted) projects with cursor pagination.

    Returns (projects, next_cursor). next_cursor is None when there are no more
    results.

    Cursor is the last project ID from the previous page — we order by
    default_order then id for stable pagination.
    """
    query = (
        select(Project)
        .where(Project.is_deleted.is_(False), Project.is_archived.is_(False))
        .order_by(Project.default_order.asc(), Project.id.asc())
    )

    if cursor is not None:
        # Fetch the cursor row to get its ordering position
        cursor_project = session.execute(
            select(Project.default_order, Project.id).where(Project.id == cursor)
        ).one_or_none()
        if cursor_project is not None:
            query = query.where(
                (Project.default_order > cursor_project.default_order)
                | (
                    (Project.default_order == cursor_project.default_order)
                    & (Project.id > cursor_project.id)
                )
            )

    # Fetch one extra to detect if there's a next page
    results = session.execute(query.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    else:
        return list(results), None


def list_archived_projects(
    session: Session,
    *,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Project], str | None]:
    """List archived projects with cursor pagination."""
    query = (
        select(Project)
        .where(Project.is_deleted.is_(False), Project.is_archived.is_(True))
        .order_by(Project.default_order.asc(), Project.id.asc())
    )

    if cursor is not None:
        cursor_project = session.execute(
            select(Project.default_order, Project.id).where(Project.id == cursor)
        ).one_or_none()
        if cursor_project is not None:
            query = query.where(
                (Project.default_order > cursor_project.default_order)
                | (
                    (Project.default_order == cursor_project.default_order)
                    & (Project.id > cursor_project.id)
                )
            )

    results = session.execute(query.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    else:
        return list(results), None


def search_projects(
    session: Session,
    *,
    query_str: str,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Project], str | None]:
    """Search projects by name (case-insensitive contains)."""
    q = (
        select(Project)
        .where(
            Project.is_deleted.is_(False),
            Project.name.ilike(f"%{query_str}%"),
        )
        .order_by(Project.default_order.asc(), Project.id.asc())
    )

    if cursor is not None:
        cursor_project = session.execute(
            select(Project.default_order, Project.id).where(Project.id == cursor)
        ).one_or_none()
        if cursor_project is not None:
            q = q.where(
                (Project.default_order > cursor_project.default_order)
                | (
                    (Project.default_order == cursor_project.default_order)
                    & (Project.id > cursor_project.id)
                )
            )

    results = session.execute(q.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    else:
        return list(results), None


# ============================================================================
# PROJECT MUTATIONS
# ============================================================================


def create_project(
    session: Session,
    *,
    name: str,
    creator_uid: str | None = None,
    description: str = "",
    parent_id: str | None = None,
    color: str = "charcoal",
    is_favorite: bool = False,
    view_style: str | None = None,
    workspace_id: str | None = None,
) -> Project:
    """Create a new project and return it."""
    now = now_iso()

    # Determine next default_order
    max_order = session.execute(
        select(func.coalesce(func.max(Project.default_order), -1))
    ).scalar_one()

    project = Project(
        id=generate_id("project"),
        name=name,
        description=description,
        parent_id=parent_id,
        color=color,
        is_favorite=is_favorite,
        view_style=view_style or "list",
        creator_uid=creator_uid,
        workspace_id=workspace_id,
        default_order=max_order + 1,
        created_at=now,
        updated_at=now,
    )
    session.add(project)
    session.flush()
    return project


def update_project(
    session: Session,
    *,
    project_id: str,
    name: str | None = None,
    description: str | None = None,
    color: str | None = None,
    is_favorite: bool | None = None,
    view_style: str | None = None,
    child_order: int | None = None,
    is_collapsed: bool | None = None,
) -> Project | None:
    """Partial-update a project. Only provided fields are changed.

    Returns the updated project, or None if not found.
    """
    project = get_project(session, project_id)
    if project is None:
        return None

    if name is not None:
        project.name = name
    if description is not None:
        project.description = description
    if color is not None:
        project.color = color
    if is_favorite is not None:
        project.is_favorite = is_favorite
    if view_style is not None:
        project.view_style = view_style
    if child_order is not None:
        project.child_order = child_order
    if is_collapsed is not None:
        project.is_collapsed = is_collapsed

    project.updated_at = now_iso()
    session.flush()
    return project


def delete_project(session: Session, project_id: str) -> bool:
    """Soft-delete a project. Returns False if not found."""
    project = get_project(session, project_id)
    if project is None:
        return False

    project.is_deleted = True
    project.updated_at = now_iso()
    session.flush()
    return True


def archive_project(session: Session, project_id: str) -> bool:
    """Archive a project. Returns False if not found."""
    project = get_project(session, project_id)
    if project is None:
        return False

    project.is_archived = True
    project.updated_at = now_iso()
    session.flush()
    return True


def unarchive_project(session: Session, project_id: str) -> bool:
    """Unarchive a project. Returns False if not found or not archived."""
    project = session.execute(
        select(Project).where(
            Project.id == project_id,
            Project.is_deleted.is_(False),
            Project.is_archived.is_(True),
        )
    ).scalar_one_or_none()
    if project is None:
        return False

    project.is_archived = False
    project.updated_at = now_iso()
    session.flush()
    return True


# ============================================================================
# TASK QUERIES
# ============================================================================


def get_task(session: Session, task_id: str) -> Task | None:
    """Get a single task by ID. Returns None if not found or deleted."""
    return session.execute(
        select(Task).where(Task.id == task_id, Task.is_deleted.is_(False))
    ).scalar_one_or_none()


def list_tasks(
    session: Session,
    *,
    project_id: str | None = None,
    section_id: str | None = None,
    parent_id: str | None = None,
    label: str | None = None,
    ids: list[str] | None = None,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Task], str | None]:
    """List active tasks with optional filters and cursor pagination."""
    query = (
        select(Task)
        .where(Task.is_deleted.is_(False), Task.checked.is_(False))
        .order_by(Task.child_order.asc(), Task.id.asc())
    )

    if project_id is not None:
        query = query.where(Task.project_id == project_id)
    if section_id is not None:
        query = query.where(Task.section_id == section_id)
    if parent_id is not None:
        query = query.where(Task.parent_id == parent_id)
    if label is not None:
        # labels is a JSONB array — check if it contains the label string
        query = query.where(Task.labels.op("??")(label))
    if ids is not None:
        query = query.where(Task.id.in_(ids))

    if cursor is not None:
        cursor_task = session.execute(
            select(Task.child_order, Task.id).where(Task.id == cursor)
        ).one_or_none()
        if cursor_task is not None:
            query = query.where(
                (Task.child_order > cursor_task.child_order)
                | (
                    (Task.child_order == cursor_task.child_order)
                    & (Task.id > cursor_task.id)
                )
            )

    results = session.execute(query.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    return list(results), None


# ============================================================================
# TASK MUTATIONS
# ============================================================================


def create_task(
    session: Session,
    *,
    content: str,
    user_id: str,
    project_id: str,
    description: str = "",
    section_id: str | None = None,
    parent_id: str | None = None,
    labels: list[str] | None = None,
    priority: int = 1,
    due: dict | None = None,
    deadline: dict | None = None,
    duration: dict | None = None,
    order: int | None = None,
    assignee_id: str | None = None,
) -> Task:
    """Create a new task and return it."""
    now = now_iso()

    # Determine child_order if not provided
    if order is not None:
        child_order = order
    else:
        max_order = session.execute(
            select(func.coalesce(func.max(Task.child_order), -1)).where(
                Task.project_id == project_id
            )
        ).scalar_one()
        child_order = max_order + 1

    task = Task(
        id=generate_id("task"),
        content=content,
        description=description,
        project_id=project_id,
        section_id=section_id,
        parent_id=parent_id,
        user_id=user_id,
        added_by_uid=user_id,
        responsible_uid=assignee_id,
        labels=labels or [],
        priority=priority,
        due=due,
        deadline=deadline,
        duration=duration,
        child_order=child_order,
        goal_ids=[],
        added_at=now,
        updated_at=now,
    )
    session.add(task)
    session.flush()
    return task


def update_task(
    session: Session,
    *,
    task_id: str,
    content: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    priority: int | None = None,
    due: dict | None = None,
    deadline: dict | None = None,
    duration: dict | None = None,
    assignee_id: str | None = None,
    child_order: int | None = None,
    day_order: int | None = None,
    is_collapsed: bool | None = None,
) -> Task | None:
    """Partial-update a task. Returns None if not found."""
    task = get_task(session, task_id)
    if task is None:
        return None

    if content is not None:
        task.content = content
    if description is not None:
        task.description = description
    if labels is not None:
        task.labels = labels
    if priority is not None:
        task.priority = priority
    if due is not None:
        task.due = due
    if deadline is not None:
        task.deadline = deadline
    if duration is not None:
        task.duration = duration
    if assignee_id is not None:
        task.responsible_uid = assignee_id
    if child_order is not None:
        task.child_order = child_order
    if day_order is not None:
        task.day_order = day_order
    if is_collapsed is not None:
        task.is_collapsed = is_collapsed

    task.updated_at = now_iso()
    session.flush()
    return task


def delete_task(session: Session, task_id: str) -> bool:
    """Soft-delete a task."""
    task = get_task(session, task_id)
    if task is None:
        return False
    task.is_deleted = True
    task.updated_at = now_iso()
    session.flush()
    return True


def close_task(session: Session, task_id: str, completed_by_uid: str) -> bool:
    """Mark a task as completed."""
    task = get_task(session, task_id)
    if task is None:
        return False
    task.checked = True
    task.completed_at = now_iso()
    task.completed_by_uid = completed_by_uid
    task.updated_at = now_iso()
    session.flush()
    return True


def reopen_task(session: Session, task_id: str) -> bool:
    """Reopen a completed task."""
    task = session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.is_deleted.is_(False),
            Task.checked.is_(True),
        )
    ).scalar_one_or_none()
    if task is None:
        return False
    task.checked = False
    task.completed_at = None
    task.completed_by_uid = None
    task.updated_at = now_iso()
    session.flush()
    return True


def move_task(
    session: Session,
    *,
    task_id: str,
    project_id: str | None = None,
    section_id: str | None = None,
    parent_id: str | None = None,
) -> Task | None:
    """Move a task to a different project, section, or parent."""
    task = get_task(session, task_id)
    if task is None:
        return None
    if project_id is not None:
        task.project_id = project_id
        task.section_id = None  # reset section when moving projects
    if section_id is not None:
        task.section_id = section_id
    if parent_id is not None:
        task.parent_id = parent_id
    task.updated_at = now_iso()
    session.flush()
    return task


# ============================================================================
# LABEL QUERIES
# ============================================================================


def get_label(session: Session, label_id: str) -> Label | None:
    """Get a single label by ID. Returns None if not found or deleted."""
    return session.execute(
        select(Label).where(Label.id == label_id, Label.is_deleted.is_(False))
    ).scalar_one_or_none()


def list_labels(
    session: Session,
    *,
    cursor: str | None = None,
    limit: int = 50,
) -> tuple[list[Label], str | None]:
    """List labels with cursor pagination.

    Returns (labels, next_cursor). next_cursor is None when there are no more
    results.

    Cursor is the last label ID from the previous page — we order by
    order then id for stable pagination.
    """
    query = (
        select(Label)
        .where(Label.is_deleted.is_(False))
        .order_by(Label.order.asc().nulls_last(), Label.id.asc())
    )

    if cursor is not None:
        # Fetch the cursor row to get its ordering position
        cursor_label = session.execute(
            select(Label.order, Label.id).where(Label.id == cursor)
        ).one_or_none()
        if cursor_label is not None:
            if cursor_label.order is not None:
                query = query.where(
                    (Label.order > cursor_label.order)
                    | (Label.order.is_(None))
                    | (
                        (Label.order == cursor_label.order)
                        & (Label.id > cursor_label.id)
                    )
                )
            else:
                query = query.where(
                    (Label.order.is_(None)) & (Label.id > cursor_label.id)
                )

    # Fetch one extra to detect if there's a next page
    results = session.execute(query.limit(limit + 1)).scalars().all()

    if len(results) > limit:
        next_cursor = results[limit - 1].id
        return list(results[:limit]), next_cursor
    else:
        return list(results), None


# ============================================================================
# LABEL MUTATIONS
# ============================================================================


def create_label(
    session: Session,
    *,
    name: str,
    order: int | None = None,
    color: str = "charcoal",
    is_favorite: bool = False,
) -> Label:
    """Create a new label and return it."""
    now = now_iso()

    label = Label(
        id=generate_id("label"),
        name=name,
        order=order,
        color=color,
        is_favorite=is_favorite,
        created_at=now,
        updated_at=now,
    )
    session.add(label)
    session.flush()
    return label


def update_label(
    session: Session,
    *,
    label_id: str,
    name: str | None = None,
    order: int | None = None,
    color: str | None = None,
    is_favorite: bool | None = None,
) -> Label | None:
    """Partial-update a label. Only provided fields are changed.

    Returns the updated label, or None if not found.
    """
    label = get_label(session, label_id)
    if label is None:
        return None

    if name is not None:
        label.name = name
    if order is not None:
        label.order = order
    if color is not None:
        label.color = color
    if is_favorite is not None:
        label.is_favorite = is_favorite

    label.updated_at = now_iso()
    session.flush()
    return label


def delete_label(session: Session, label_id: str) -> bool:
    """Soft-delete a label. Returns False if not found."""
    label = get_label(session, label_id)
    if label is None:
        return False

    label.is_deleted = True
    label.updated_at = now_iso()
    session.flush()
    return True

```

### `core/serializers.py`

```python
"""Serialization helpers for the Todoist API replica.

Each serialize function converts an ORM model into a dict matching the Todoist
API response shape. Todoist uses snake_case natively so no case conversion
is needed.
"""

from __future__ import annotations

from typing import Any

from ..database.schema import Label, Project, Task


def serialize_project(project: Project) -> dict[str, Any]:
    """Serialize a Project to match PersonalProjectSyncView / WorkspaceProjectSyncView."""
    result: dict[str, Any] = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "parent_id": project.parent_id,
        "child_order": project.child_order,
        "default_order": project.default_order,
        "color": project.color,
        "view_style": project.view_style,
        "is_collapsed": project.is_collapsed,
        "is_favorite": project.is_favorite,
        "is_archived": project.is_archived,
        "is_deleted": project.is_deleted,
        "is_frozen": project.is_frozen,
        "inbox_project": project.inbox_project,
        "is_shared": project.is_shared,
        "can_assign_tasks": project.can_assign_tasks,
        "can_comment": project.can_comment,
        "role": project.role,
        "public_key": project.public_key,
        "access": project.access,
        "creator_uid": project.creator_uid,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }

    # Workspace-only fields — include only when the project belongs to a workspace
    if project.workspace_id is not None:
        result["workspace_id"] = project.workspace_id
        result["folder_id"] = project.folder_id
        result["status"] = project.status
        result["collaborator_role_default"] = project.collaborator_role_default
        result["is_invite_only"] = project.is_invite_only
        result["is_link_sharing_enabled"] = project.is_link_sharing_enabled
        result["is_pending_default_collaborator_invites"] = (
            project.is_pending_default_collaborator_invites
        )
        result["is_project_insights_enabled"] = project.is_project_insights_enabled

    return result


def serialize_project_list(
    projects: list[Project],
    *,
    next_cursor: str | None,
) -> dict[str, Any]:
    """Serialize a paginated project list matching Todoist's PaginatedList shape."""
    return {
        "results": [serialize_project(p) for p in projects],
        "next_cursor": next_cursor,
    }


def serialize_task(task: Task) -> dict[str, Any]:
    """Serialize a Task to match ItemSyncView."""
    return {
        "id": task.id,
        "user_id": task.user_id,
        "project_id": task.project_id,
        "section_id": task.section_id,
        "parent_id": task.parent_id,
        "content": task.content,
        "description": task.description,
        "priority": task.priority,
        "child_order": task.child_order,
        "day_order": task.day_order,
        "labels": task.labels,
        "due": task.due,
        "deadline": task.deadline,
        "duration": task.duration,
        "checked": task.checked,
        "is_collapsed": task.is_collapsed,
        "is_deleted": task.is_deleted,
        "added_by_uid": task.added_by_uid,
        "assigned_by_uid": task.assigned_by_uid,
        "responsible_uid": task.responsible_uid,
        "completed_by_uid": task.completed_by_uid,
        "note_count": task.note_count,
        "goal_ids": task.goal_ids,
        "added_at": task.added_at,
        "completed_at": task.completed_at,
        "updated_at": task.updated_at,
    }


def serialize_task_list(
    tasks: list[Task],
    *,
    next_cursor: str | None,
) -> dict[str, Any]:
    """Serialize a paginated task list."""
    return {
        "results": [serialize_task(t) for t in tasks],
        "next_cursor": next_cursor,
    }


def serialize_label(label: Label) -> dict[str, Any]:
    """Serialize a Label to match LabelRestView."""
    return {
        "id": label.id,
        "name": label.name,
        "color": label.color,
        "order": label.order,
        "is_favorite": label.is_favorite,
    }


def serialize_label_list(
    labels: list[Label],
    *,
    next_cursor: str | None,
) -> dict[str, Any]:
    """Serialize a paginated label list."""
    return {
        "results": [serialize_label(l) for l in labels],
        "next_cursor": next_cursor,
    }

```

### `api/routes.py`

```python
"""Todoist REST API routes.

Mounted under /api/env/{env_id}/services/todoist/api/v1
DB session comes from request.state.db_session (IsolationMiddleware).
User impersonation comes from request.state.impersonate_user_id.
"""

from __future__ import annotations

from typing import Any

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from sqlalchemy.orm import Session

from ..core.errors import (
    TodoistAPIError,
    bad_request,
    handle_exception,
    not_found,
    unauthorized,
)
from ..core.serializers import (
    serialize_label,
    serialize_label_list,
    serialize_project,
    serialize_project_list,
    serialize_task,
    serialize_task_list,
)
from ..database import operations as ops


# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------


def _session(request: Request) -> Session:
    session = getattr(request.state, "db_session", None)
    if session is None:
        raise unauthorized("Missing database session")
    return session


def _principal_user_id(request: Request) -> str:
    principal = getattr(request.state, "impersonate_user_id", None)
    if principal is not None and str(principal).strip() != "":
        return str(principal)
    raise unauthorized("Missing user authentication")


async def _parse_json_body(request: Request) -> dict[str, Any]:
    try:
        return await request.json()
    except Exception as exc:
        raise bad_request(f"Invalid JSON body: {exc}") from exc


def _pagination_params(request: Request) -> tuple[str | None, int]:
    """Extract cursor and limit from query params."""
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
# Project endpoints
# ---------------------------------------------------------------------------


async def get_projects(request: Request) -> JSONResponse:
    """GET /projects"""
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        projects, next_cursor = ops.list_projects(
            session, cursor=cursor, limit=limit
        )
        return JSONResponse(
            serialize_project_list(projects, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_project(request: Request) -> JSONResponse:
    """POST /projects"""
    try:
        session = _session(request)
        principal_id = _principal_user_id(request)
        body = await _parse_json_body(request)

        name = body.get("name")
        if not isinstance(name, str) or not name.strip():
            raise bad_request("Field 'name' is required")

        project = ops.create_project(
            session,
            name=name.strip(),
            creator_uid=principal_id,
            description=body.get("description", ""),
            parent_id=body.get("parent_id"),
            color=body.get("color", "charcoal"),
            is_favorite=body.get("is_favorite", False),
            view_style=body.get("view_style"),
            workspace_id=body.get("workspace_id"),
        )
        return JSONResponse(
            serialize_project(project), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_project(request: Request) -> JSONResponse:
    """GET /projects/{project_id}"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        project = ops.get_project(session, project_id)
        if project is None:
            raise not_found("Project not found")
        return JSONResponse(
            serialize_project(project), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_project(request: Request) -> JSONResponse:
    """POST /projects/{project_id}"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        body = await _parse_json_body(request)

        project = ops.update_project(
            session,
            project_id=project_id,
            name=body.get("name"),
            description=body.get("description"),
            color=body.get("color"),
            is_favorite=body.get("is_favorite"),
            view_style=body.get("view_style"),
            child_order=body.get("child_order"),
            is_collapsed=body.get("is_collapsed"),
        )
        if project is None:
            raise not_found("Project not found")
        return JSONResponse(
            serialize_project(project), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_project(request: Request) -> JSONResponse:
    """DELETE /projects/{project_id}"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        deleted = ops.delete_project(session, project_id)
        if not deleted:
            raise not_found("Project not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def archive_project(request: Request) -> JSONResponse:
    """POST /projects/{project_id}/archive"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        archived = ops.archive_project(session, project_id)
        if not archived:
            raise not_found("Project not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def unarchive_project(request: Request) -> JSONResponse:
    """POST /projects/{project_id}/unarchive"""
    try:
        session = _session(request)
        project_id = request.path_params["project_id"]
        unarchived = ops.unarchive_project(session, project_id)
        if not unarchived:
            raise not_found("Project not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_archived_projects(request: Request) -> JSONResponse:
    """GET /projects/archived"""
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        projects, next_cursor = ops.list_archived_projects(
            session, cursor=cursor, limit=limit
        )
        return JSONResponse(
            serialize_project_list(projects, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def search_projects(request: Request) -> JSONResponse:
    """GET /projects/search"""
    try:
        session = _session(request)
        query_str = request.query_params.get("query", "")
        cursor, limit = _pagination_params(request)
        projects, next_cursor = ops.search_projects(
            session, query_str=query_str, cursor=cursor, limit=limit
        )
        return JSONResponse(
            serialize_project_list(projects, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Task endpoints
# ---------------------------------------------------------------------------


async def get_tasks(request: Request) -> JSONResponse:
    """GET /tasks"""
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)

        # Optional filters
        project_id = request.query_params.get("project_id")
        section_id = request.query_params.get("section_id")
        parent_id = request.query_params.get("parent_id")
        label = request.query_params.get("label")
        ids_param = request.query_params.get("ids")
        ids = ids_param.split(",") if ids_param else None

        tasks, next_cursor = ops.list_tasks(
            session,
            project_id=project_id,
            section_id=section_id,
            parent_id=parent_id,
            label=label,
            ids=ids,
            cursor=cursor,
            limit=limit,
        )
        return JSONResponse(
            serialize_task_list(tasks, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_task(request: Request) -> JSONResponse:
    """POST /tasks"""
    try:
        session = _session(request)
        principal_id = _principal_user_id(request)
        body = await _parse_json_body(request)

        content = body.get("content")
        if not isinstance(content, str) or not content.strip():
            raise bad_request("Field 'content' is required")

        # Build due object from due_string/due_date/due_datetime if provided
        due = None
        if any(body.get(k) for k in ("due_string", "due_date", "due_datetime")):
            due = {
                "string": body.get("due_string"),
                "date": body.get("due_date"),
                "datetime": body.get("due_datetime"),
                "lang": body.get("due_lang", "en"),
                "is_recurring": False,
            }

        # Build deadline from deadline_date if provided
        deadline = None
        if body.get("deadline_date"):
            deadline = {"date": body["deadline_date"], "lang": body.get("due_lang", "en")}

        # Build duration from duration + duration_unit if provided
        duration = None
        if body.get("duration") is not None and body.get("duration_unit"):
            duration = {"amount": body["duration"], "unit": body["duration_unit"]}

        task = ops.create_task(
            session,
            content=content.strip(),
            user_id=principal_id,
            project_id=body.get("project_id", ""),
            description=body.get("description", ""),
            section_id=body.get("section_id"),
            parent_id=body.get("parent_id"),
            labels=body.get("labels"),
            priority=body.get("priority", 1),
            due=due,
            deadline=deadline,
            duration=duration,
            order=body.get("order"),
            assignee_id=body.get("assignee_id"),
        )
        return JSONResponse(
            serialize_task(task), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_task(request: Request) -> JSONResponse:
    """GET /tasks/{task_id}"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        task = ops.get_task(session, task_id)
        if task is None:
            raise not_found("Task not found")
        return JSONResponse(
            serialize_task(task), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_id}"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        body = await _parse_json_body(request)

        # Build due/deadline/duration from flat fields if provided
        due = None
        if any(body.get(k) for k in ("due_string", "due_date", "due_datetime")):
            due = {
                "string": body.get("due_string"),
                "date": body.get("due_date"),
                "datetime": body.get("due_datetime"),
                "lang": body.get("due_lang", "en"),
                "is_recurring": False,
            }

        deadline = None
        if body.get("deadline_date"):
            deadline = {"date": body["deadline_date"], "lang": body.get("due_lang", "en")}

        duration = None
        if body.get("duration") is not None and body.get("duration_unit"):
            duration = {"amount": body["duration"], "unit": body["duration_unit"]}

        task = ops.update_task(
            session,
            task_id=task_id,
            content=body.get("content"),
            description=body.get("description"),
            labels=body.get("labels"),
            priority=body.get("priority"),
            due=due,
            deadline=deadline,
            duration=duration,
            assignee_id=body.get("assignee_id"),
            child_order=body.get("child_order"),
            day_order=body.get("day_order"),
            is_collapsed=body.get("is_collapsed"),
        )
        if task is None:
            raise not_found("Task not found")
        return JSONResponse(
            serialize_task(task), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_task(request: Request) -> JSONResponse:
    """DELETE /tasks/{task_id}"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        deleted = ops.delete_task(session, task_id)
        if not deleted:
            raise not_found("Task not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def close_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_id}/close"""
    try:
        session = _session(request)
        principal_id = _principal_user_id(request)
        task_id = request.path_params["task_id"]
        closed = ops.close_task(session, task_id, completed_by_uid=principal_id)
        if not closed:
            raise not_found("Task not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def reopen_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_id}/reopen"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        reopened = ops.reopen_task(session, task_id)
        if not reopened:
            raise not_found("Task not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def move_task(request: Request) -> JSONResponse:
    """POST /tasks/{task_id}/move"""
    try:
        session = _session(request)
        task_id = request.path_params["task_id"]
        body = await _parse_json_body(request)

        task = ops.move_task(
            session,
            task_id=task_id,
            project_id=body.get("project_id"),
            section_id=body.get("section_id"),
            parent_id=body.get("parent_id"),
        )
        if task is None:
            raise not_found("Task not found")
        return JSONResponse(
            serialize_task(task), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Label endpoints
# ---------------------------------------------------------------------------


async def get_labels(request: Request) -> JSONResponse:
    """GET /labels"""
    try:
        session = _session(request)
        cursor, limit = _pagination_params(request)
        labels, next_cursor = ops.list_labels(
            session, cursor=cursor, limit=limit
        )
        return JSONResponse(
            serialize_label_list(labels, next_cursor=next_cursor),
            status_code=status.HTTP_200_OK,
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def create_label(request: Request) -> JSONResponse:
    """POST /labels"""
    try:
        session = _session(request)
        body = await _parse_json_body(request)

        name = body.get("name")
        if not isinstance(name, str) or not name.strip():
            raise bad_request("Field 'name' is required")

        label = ops.create_label(
            session,
            name=name.strip(),
            order=body.get("order"),
            color=body.get("color", "charcoal"),
            is_favorite=body.get("is_favorite", False),
        )
        return JSONResponse(
            serialize_label(label), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def get_label(request: Request) -> JSONResponse:
    """GET /labels/{label_id}"""
    try:
        session = _session(request)
        label_id = request.path_params["label_id"]
        label = ops.get_label(session, label_id)
        if label is None:
            raise not_found("Label not found")
        return JSONResponse(
            serialize_label(label), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def update_label(request: Request) -> JSONResponse:
    """POST /labels/{label_id}"""
    try:
        session = _session(request)
        label_id = request.path_params["label_id"]
        body = await _parse_json_body(request)

        label = ops.update_label(
            session,
            label_id=label_id,
            name=body.get("name"),
            order=body.get("order"),
            color=body.get("color"),
            is_favorite=body.get("is_favorite"),
        )
        if label is None:
            raise not_found("Label not found")
        return JSONResponse(
            serialize_label(label), status_code=status.HTTP_200_OK
        )
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


async def delete_label(request: Request) -> JSONResponse:
    """DELETE /labels/{label_id}"""
    try:
        session = _session(request)
        label_id = request.path_params["label_id"]
        deleted = ops.delete_label(session, label_id)
        if not deleted:
            raise not_found("Label not found")
        return JSONResponse({}, status_code=status.HTTP_200_OK)
    except TodoistAPIError as exc:
        return exc.to_response()
    except Exception as exc:
        return handle_exception(exc)


# ---------------------------------------------------------------------------
# Route table
# ---------------------------------------------------------------------------

# Note: fixed paths (archived, search, filter, completed, quick) must come
# before parameterized {id} paths so Starlette matches them first.

routes = [
    # Projects
    Route("/projects", get_projects, methods=["GET"]),
    Route("/projects", create_project, methods=["POST"]),
    Route("/projects/archived", get_archived_projects, methods=["GET"]),
    Route("/projects/search", search_projects, methods=["GET"]),
    Route("/projects/{project_id}", get_project, methods=["GET"]),
    Route("/projects/{project_id}", update_project, methods=["POST"]),
    Route("/projects/{project_id}", delete_project, methods=["DELETE"]),
    Route("/projects/{project_id}/archive", archive_project, methods=["POST"]),
    Route("/projects/{project_id}/unarchive", unarchive_project, methods=["POST"]),
    # Tasks
    Route("/tasks", get_tasks, methods=["GET"]),
    Route("/tasks", create_task, methods=["POST"]),
    Route("/tasks/{task_id}", get_task, methods=["GET"]),
    Route("/tasks/{task_id}", update_task, methods=["POST"]),
    Route("/tasks/{task_id}", delete_task, methods=["DELETE"]),
    Route("/tasks/{task_id}/close", close_task, methods=["POST"]),
    Route("/tasks/{task_id}/reopen", reopen_task, methods=["POST"]),
    Route("/tasks/{task_id}/move", move_task, methods=["POST"]),
    # Labels
    Route("/labels", get_labels, methods=["GET"]),
    Route("/labels", create_label, methods=["POST"]),
    Route("/labels/{label_id}", get_label, methods=["GET"]),
    Route("/labels/{label_id}", update_label, methods=["POST"]),
    Route("/labels/{label_id}", delete_label, methods=["DELETE"]),
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
