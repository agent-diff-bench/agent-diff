# Entity Implementation: issues

You are implementing the **issues** resource for the GitHub API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for issues

```json
{
  "paths": {
    "/issues": {
      "get": {
        "summary": "List issues assigned to the authenticated user",
        "description": "List issues assigned to the authenticated user across all visible repositories including owned repositories, member\nrepositories, and organization repositories. You can use the `filter` query parameter to fetch issues that are not\nnecessarily assigned to you.\n\n> [!NOTE]\n> GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, \"Issues\" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from \"Issues\" endpoints will be an _issue id_. To find out the pull request id, use the \"[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)\" endpoint.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "issues"
        ],
        "operationId": "issues/list",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/issues/issues#list-issues-assigned-to-the-authenticated-user"
        },
        "parameters": [
          {
            "name": "filter",
            "description": "Indicates which sorts of issues to return. `assigned` means issues assigned to you. `created` means issues created by you. `mentioned` means issues mentioning you. `subscribed` means issues you're subscribed to updates for. `all` or `repos` means all issues you can see, regardless of participation or creation.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "assigned",
                "created",
                "mentioned",
                "subscribed",
                "repos",
                "all"
              ],
              "default": "assigned"
            }
          },
          {
            "name": "state",
            "description": "Indicates the state of the issues to return.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "open",
                "closed",
                "all"
              ],
              "default": "open"
            }
          },
          {
            "$ref": "#/components/parameters/labels"
          },
          {
            "name": "sort",
            "description": "What to sort results by.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "created",
                "updated",
                "comments"
              ],
              "default": "created"
            }
          },
          {
            "$ref": "#/components/parameters/direction"
          },
          {
            "$ref": "#/components/parameters/since"
          },
          {
            "name": "collab",
            "in": "query",
            "required": false,
            "schema": {
              "type": "boolean"
            }
          },
          {
            "name": "orgs",
            "in": "query",
            "required": false,
            "schema": {
              "type": "boolean"
            }
          },
          {
            "name": "owned",
            "in": "query",
            "required": false,
            "schema": {
              "type": "boolean"
            }
          },
          {
            "name": "pulls",
            "in": "query",
            "required": false,
            "schema": {
              "type": "boolean"
            }
          },
          {
            "$ref": "#/components/parameters/per-page"
          },
          {
            "$ref": "#/components/parameters/page"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/issue"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/issue-with-repo-items"
                  }
                }
              }
            },
            "headers": {
              "Link": {
                "$ref": "#/components/headers/link"
              }
            }
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "issues",
          "subcategory": "issues"
        }
      }
    },
    "/orgs/{org}/issues": {
      "get": {
        "summary": "List organization issues assigned to the authenticated user",
        "description": "List issues in an organization assigned to the authenticated user.\n\n> [!NOTE]\n> GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, \"Issues\" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from \"Issues\" endpoints will be an _issue id_. To find out the pull request id, use the \"[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)\" endpoint.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "issues"
        ],
        "operationId": "issues/list-for-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/issues/issues#list-organization-issues-assigned-to-the-authenticated-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "name": "filter",
            "description": "Indicates which sorts of issues to return. `assigned` means issues assigned to you. `created` means issues created by you. `mentioned` means issues mentioning you. `subscribed` means issues you're subscribed to updates for. `all` or `repos` means all issues you can see, regardless of participation or creation.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "assigned",
                "created",
                "mentioned",
                "subscribed",
                "repos",
                "all"
              ],
              "default": "assigned"
            }
          },
          {
            "name": "state",
            "description": "Indicates the state of the issues to return.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "open",
                "closed",
                "all"
              ],
              "default": "open"
            }
          },
          {
            "$ref": "#/components/parameters/labels"
          },
          {
            "name": "type",
            "description": "Can be the name of an issue type.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "sort",
            "description": "What to sort results by.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "created",
                "updated",
                "comments"
              ],
              "default": "created"
            }
          },
          {
            "$ref": "#/components/parameters/direction"
          },
          {
            "$ref": "#/components/parameters/since"
          },
          {
            "$ref": "#/components/parameters/per-page"
          },
          {
            "$ref": "#/components/parameters/page"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/issue"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/issue-with-repo-items"
                  }
                }
              }
            },
            "headers": {
              "Link": {
                "$ref": "#/components/headers/link"
              }
            }
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "issues",
          "subcategory": "issues"
        }
      }
    },
    "/repos/{owner}/{repo}/issues": {
      "get": {
        "summary": "List repository issues",
        "description": "List issues in a repository. Only open issues will be listed.\n\n> [!NOTE]\n> GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, \"Issues\" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from \"Issues\" endpoints will be an _issue id_. To find out the pull request id, use the \"[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)\" endpoint.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "issues"
        ],
        "operationId": "issues/list-for-repo",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/issues/issues#list-repository-issues"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "name": "milestone",
            "description": "If an `integer` is passed, it should refer to a milestone by its `number` field. If the string `*` is passed, issues with any milestone are accepted. If the string `none` is passed, issues without milestones are returned.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "state",
            "description": "Indicates the state of the issues to return.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "open",
                "closed",
                "all"
              ],
              "default": "open"
            }
          },
          {
            "name": "assignee",
            "description": "Can be the name of a user. Pass in `none` for issues with no assigned user, and `*` for issues assigned to any user.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "type",
            "description": "Can be the name of an issue type. If the string `*` is passed, issues with any type are accepted. If the string `none` is passed, issues without type are returned.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "creator",
            "description": "The user that created the issue.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "mentioned",
            "description": "A user that's mentioned in the issue.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "$ref": "#/components/parameters/labels"
          },
          {
            "name": "sort",
            "description": "What to sort results by.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "created",
                "updated",
                "comments"
              ],
              "default": "created"
            }
          },
          {
            "$ref": "#/components/parameters/direction"
          },
          {
            "$ref": "#/components/parameters/since"
          },
          {
            "$ref": "#/components/parameters/per-page"
          },
          {
            "$ref": "#/components/parameters/page"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/issue"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/issue-items"
                  }
                }
              }
            },
            "headers": {
              "Link": {
                "$ref": "#/components/headers/link"
              }
            }
          },
          "301": {
            "$ref": "#/components/responses/moved_permanently"
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "issues",
          "subcategory": "issues"
        }
      },
      "post": {
        "summary": "Create an issue",
        "description": "Any user with pull access to a repository can create an issue. If [issues are disabled in the repository](https://docs.github.com/articles/disabling-issues/), the API returns a `410 Gone` status.\n\nThis endpoint triggers [notifications](https://docs.github.com/github/managing-subscriptions-and-notifications-on-github/about-notifications). Creating content too quickly using this endpoint may result in secondary rate limiting. For more information, see \"[Rate limits for the API](https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api#about-secondary-rate-limits)\"\nand \"[Best practices for using the REST API](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api).\"\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "issues"
        ],
        "operationId": "issues/create",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/issues/issues#create-an-issue"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "title": {
                    "oneOf": [
                      {
                        "type": "string"
                      },
                      {
                        "type": "integer"
                      }
                    ],
                    "description": "The title of the issue."
                  },
                  "body": {
                    "type": "string",
                    "description": "The contents of the issue."
                  },
                  "milestone": {
                    "oneOf": [
                      {
                        "type": "string"
                      },
                      {
                        "type": "integer",
                        "description": "The `number` of the milestone to associate this issue with. _NOTE: Only users with push access can set the milestone for new issues. The milestone is silently dropped otherwise._"
                      }
                    ],
                    "type": [
                      "null",
                      "string",
                      "integer"
                    ]
                  },
                  "labels": {
                    "type": "array",
                    "description": "Labels to associate with this issue. _NOTE: Only users with push access can set labels for new issues. Labels are silently dropped otherwise._",
                    "items": {
                      "oneOf": [
                        {
                          "type": "string"
                        },
                        {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer"
                            },
                            "name": {
                              "type": "string"
                            },
                            "description": {
                              "type": [
                                "string",
                                "null"
                              ]
                            },
                            "color": {
                              "type": [
                                "string",
                                "null"
                              ]
                            }
                          }
                        }
                      ]
                    }
                  },
                  "assignees": {
                    "type": "array",
                    "description": "Logins for Users to assign to this issue. _NOTE: Only users with push access can set assignees for new issues. Assignees are silently dropped otherwise._",
                    "items": {
                      "type": "string"
                    }
                  },
                  "type": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "description": "The name of the issue type to associate with this issue. _NOTE: Only users with push access can set the type for new issues. The type is silently dropped otherwise._",
                    "examples": [
                      "Epic"
                    ]
                  }
                },
                "required": [
                  "title"
                ]
              },
              "examples": {
                "default": {
                  "value": {
                    "title": "Found a bug",
                    "body": "I'm having a problem with this.",
                    "assignees": [
                      "octocat"
                    ],
                    "milestone": 1,
                    "labels": [
                      "bug"
                    ]
                  }
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/issue"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/issue"
                  }
                }
              }
            },
            "headers": {
              "Location": {
                "example": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
                "schema": {
                  "type": "string"
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/bad_request"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          },
          "503": {
            "$ref": "#/components/responses/service_unavailable"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "410": {
            "$ref": "#/components/responses/gone"
          }
        },
        "x-github": {
          "triggersNotification": true,
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "issues",
          "subcategory": "issues"
        }
      }
    },
    "/repos/{owner}/{repo}/issues/{issue_number}": {
      "get": {
        "summary": "Get an issue",
        "description": "The API returns a [`301 Moved Permanently` status](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api#follow-redirects) if the issue was\n[transferred](https://docs.github.com/articles/transferring-an-issue-to-another-repository/) to another repository. If\nthe issue was transferred to or deleted from a repository where the authenticated user lacks read access, the API\nreturns a `404 Not Found` status. If the issue was deleted from a repository where the authenticated user has read\naccess, the API returns a `410 Gone` status. To receive webhook events for transferred and deleted issues, subscribe\nto the [`issues`](https://docs.github.com/webhooks/event-payloads/#issues) webhook.\n\n> [!NOTE]\n> GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, \"Issues\" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from \"Issues\" endpoints will be an _issue id_. To find out the pull request id, use the \"[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)\" endpoint.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "issues"
        ],
        "operationId": "issues/get",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/issues/issues#get-an-issue"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "$ref": "#/components/parameters/issue-number"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/issue"
                },
                "examples": {
                  "default": {
                    "summary": "Issue",
                    "value": {
                      "$ref": "#/components/examples/issue"
                    }
                  },
                  "pinned_comment": {
                    "summary": "Issue with pinned comment",
                    "value": {
                      "$ref": "#/components/examples/issue-with-pinned-comment"
                    }
                  }
                }
              }
            }
          },
          "301": {
            "$ref": "#/components/responses/moved_permanently"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "410": {
            "$ref": "#/components/responses/gone"
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "issues",
          "subcategory": "issues"
        }
      },
      "patch": {
        "summary": "Update an issue",
        "description": "Issue owners and users with push access or Triage role can edit an issue.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "issues"
        ],
        "operationId": "issues/update",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/issues/issues#update-an-issue"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "$ref": "#/components/parameters/issue-number"
          }
        ],
        "requestBody": {
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "title": {
                    "oneOf": [
                      {
                        "type": "string"
                      },
                      {
                        "type": "integer"
                      }
                    ],
                    "description": "The title of the issue.",
                    "type": [
                      "null",
                      "string",
                      "integer"
                    ]
                  },
                  "body": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "description": "The contents of the issue."
                  },
                  "state": {
                    "type": "string",
                    "description": "The open or closed state of the issue.",
                    "enum": [
                      "open",
                      "closed"
                    ]
                  },
                  "state_reason": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "enum": [
                      "completed",
                      "not_planned",
                      "duplicate",
                      "reopened",
                      null
                    ],
                    "description": "The reason for the state change. Ignored unless `state` is changed.",
                    "examples": [
                      "not_planned"
                    ]
                  },
                  "milestone": {
                    "oneOf": [
                      {
                        "type": "string"
                      },
                      {
                        "type": "integer",
                        "description": "The `number` of the milestone to associate this issue with or use `null` to remove the current milestone. Only users with push access can set the milestone for issues. Without push access to the repository, milestone changes are silently dropped."
                      }
                    ],
                    "type": [
                      "null",
                      "string",
                      "integer"
                    ]
                  },
                  "labels": {
                    "type": "array",
                    "description": "Labels to associate with this issue. Pass one or more labels to _replace_ the set of labels on this issue. Send an empty array (`[]`) to clear all labels from the issue. Only users with push access can set labels for issues. Without push access to the repository, label changes are silently dropped.",
                    "items": {
                      "oneOf": [
                        {
                          "type": "string"
                        },
                        {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer"
                            },
                            "name": {
                              "type": "string"
                            },
                            "description": {
                              "type": [
                                "string",
                                "null"
                              ]
                            },
                            "color": {
                              "type": [
                                "string",
                                "null"
                              ]
                            }
                          }
                        }
                      ]
                    }
                  },
                  "assignees": {
                    "type": "array",
                    "description": "Usernames to assign to this issue. Pass one or more user logins to _replace_ the set of assignees on this issue. Send an empty array (`[]`) to clear all assignees from the issue. Only users with push access can set assignees for new issues. Without push access to the repository, assignee changes are silently dropped.",
                    "items": {
                      "type": "string"
                    }
                  },
                  "issue_field_values": {
                    "type": "array",
                    "description": "An array of issue field values to set on this issue. Each field value must include the field ID and the value to set. Only users with push access can set field values for issues",
                    "items": {
                      "type": "object",
                      "properties": {
                        "field_id": {
                          "type": "integer",
                          "description": "The ID of the issue field to set"
                        },
                        "value": {
                          "oneOf": [
                            {
                              "type": "string"
                            },
                            {
                              "type": "number"
                            }
                          ],
                          "description": "The value to set for the field"
                        }
                      },
                      "required": [
                        "field_id",
                        "value"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "type": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "description": "The name of the issue type to associate with this issue or use `null` to remove the current issue type. Only users with push access can set the type for issues. Without push access to the repository, type changes are silently dropped.",
                    "examples": [
                      "Epic"
                    ]
                  }
                }
              },
              "examples": {
                "default": {
                  "value": {
                    "title": "Found a bug",
                    "body": "I'm having a problem with this.",
                    "assignees": [
                      "octocat"
                    ],
                    "milestone": 1,
                    "state": "open",
                    "labels": [
                      "bug"
                    ]
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/issue"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/issue"
                  }
                }
              }
            }
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          },
          "503": {
            "$ref": "#/components/responses/service_unavailable"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "301": {
            "$ref": "#/components/responses/moved_permanently"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "410": {
            "$ref": "#/components/responses/gone"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "issues",
          "subcategory": "issues"
        }
      }
    },
    "/search/issues": {
      "get": {
        "summary": "Search issues and pull requests",
        "description": "Find issues by state and keyword. This method returns up to 100 results [per page](https://docs.github.com/rest/guides/using-pagination-in-the-rest-api).\n\nWhen searching for issues, you can get text match metadata for the issue **title**, issue **body**, and issue **comment body** fields when you pass the `text-match` media type. For more details about how to receive highlighted\nsearch results, see [Text match metadata](https://docs.github.com/rest/search/search#text-match-metadata).\n\nFor example, if you want to find the oldest unresolved Python bugs on Windows. Your query might look something like this.\n\n`q=windows+label:bug+language:python+state:open&sort=created&order=asc`\n\nThis query searches for the keyword `windows`, within any open issue that is labeled as `bug`. The search runs across repositories whose primary language is Python. The results are sorted by creation date in ascending order, which means the oldest issues appear first in the search results.\n\n> [!NOTE]\n> For requests made by GitHub Apps with a user access token, you can't retrieve a combination of issues and pull requests in a single query. Requests that don't include the `is:issue` or `is:pull-request` qualifier will receive an HTTP `422 Unprocessable Entity` response. To get results for both issues and pull requests, you must send separate queries for issues and pull requests. For more information about the `is` qualifier, see \"[Searching only issues or pull requests](https://docs.github.com/github/searching-for-information-on-github/searching-issues-and-pull-requests#search-only-issues-or-pull-requests).\"",
        "tags": [
          "search"
        ],
        "operationId": "search/issues-and-pull-requests",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/search/search#search-issues-and-pull-requests"
        },
        "parameters": [
          {
            "name": "q",
            "description": "The query contains one or more search keywords and qualifiers. Qualifiers allow you to limit your search to specific areas of GitHub. The REST API supports the same qualifiers as the web interface for GitHub. To learn more about the format of the query, see [Constructing a search query](https://docs.github.com/rest/search/search#constructing-a-search-query). See \"[Searching issues and pull requests](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests)\" for a detailed list of qualifiers.",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "sort",
            "description": "Sorts the results of your query by the number of `comments`, `reactions`, `reactions-+1`, `reactions--1`, `reactions-smile`, `reactions-thinking_face`, `reactions-heart`, `reactions-tada`, or `interactions`. You can also sort results by how recently the items were `created` or `updated`, Default: [best match](https://docs.github.com/rest/search/search#ranking-search-results)",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "comments",
                "reactions",
                "reactions-+1",
                "reactions--1",
                "reactions-smile",
                "reactions-thinking_face",
                "reactions-heart",
                "reactions-tada",
                "interactions",
                "created",
                "updated"
              ]
            }
          },
          {
            "$ref": "#/components/parameters/order"
          },
          {
            "$ref": "#/components/parameters/per-page"
          },
          {
            "$ref": "#/components/parameters/page"
          },
          {
            "$ref": "#/components/parameters/issues-advanced-search"
          },
          {
            "$ref": "#/components/parameters/search-type"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "required": [
                    "total_count",
                    "incomplete_results",
                    "items",
                    "search_type"
                  ],
                  "properties": {
                    "total_count": {
                      "type": "integer"
                    },
                    "incomplete_results": {
                      "type": "boolean"
                    },
                    "items": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/issue-search-result-item"
                      }
                    },
                    "search_type": {
                      "type": "string",
                      "description": "The type of search that was performed. Possible values are `lexical`, `semantic`, or `hybrid`.",
                      "enum": [
                        "lexical",
                        "semantic",
                        "hybrid"
                      ]
                    },
                    "lexical_fallback_reason": {
                      "type": "array",
                      "description": "When a semantic or hybrid search falls back to lexical search, this field contains the reasons for the fallback. Only present when a fallback occurred.",
                      "items": {
                        "type": "string",
                        "enum": [
                          "no_text_terms",
                          "quoted_text",
                          "non_issue_target",
                          "or_boolean_not_supported",
                          "no_accessible_repos",
                          "server_error",
                          "only_non_semantic_fields_requested"
                        ]
                      }
                    }
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/issue-search-result-item-paginated"
                  },
                  "lexical-fallback": {
                    "$ref": "#/components/examples/issue-search-result-item-paginated-lexical-fallback"
                  }
                }
              }
            }
          },
          "503": {
            "$ref": "#/components/responses/service_unavailable"
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "401": {
            "$ref": "#/components/responses/requires_authentication"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "search",
          "subcategory": "search"
        }
      }
    },
    "/user/issues": {
      "get": {
        "summary": "List user account issues assigned to the authenticated user",
        "description": "List issues across owned and member repositories assigned to the authenticated user.\n\n> [!NOTE]\n> GitHub's REST API considers every pull request an issue, but not every issue is a pull request. For this reason, \"Issues\" endpoints may return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from \"Issues\" endpoints will be an _issue id_. To find out the pull request id, use the \"[List pull requests](https://docs.github.com/rest/pulls/pulls#list-pull-requests)\" endpoint.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "issues"
        ],
        "operationId": "issues/list-for-authenticated-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/issues/issues#list-user-account-issues-assigned-to-the-authenticated-user"
        },
        "parameters": [
          {
            "name": "filter",
            "description": "Indicates which sorts of issues to return. `assigned` means issues assigned to you. `created` means issues created by you. `mentioned` means issues mentioning you. `subscribed` means issues you're subscribed to updates for. `all` or `repos` means all issues you can see, regardless of participation or creation.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "assigned",
                "created",
                "mentioned",
                "subscribed",
                "repos",
                "all"
              ],
              "default": "assigned"
            }
          },
          {
            "name": "state",
            "description": "Indicates the state of the issues to return.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "open",
                "closed",
                "all"
              ],
              "default": "open"
            }
          },
          {
            "$ref": "#/components/parameters/labels"
          },
          {
            "name": "sort",
            "description": "What to sort results by.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "created",
                "updated",
                "comments"
              ],
              "default": "created"
            }
          },
          {
            "$ref": "#/components/parameters/direction"
          },
          {
            "$ref": "#/components/parameters/since"
          },
          {
            "$ref": "#/components/parameters/per-page"
          },
          {
            "$ref": "#/components/parameters/page"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/issue"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/issue-with-repo-items"
                  }
                }
              }
            },
            "headers": {
              "Link": {
                "$ref": "#/components/headers/link"
              }
            }
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "issues",
          "subcategory": "issues"
        }
      }
    }
  },
  "schemas": {
    "integration": {
      "title": "GitHub app",
      "description": "GitHub apps are a new way to extend GitHub. They can be installed directly on organizations and user accounts and granted access to specific repositories. They come with granular permissions and built-in webhooks. GitHub apps are first class actors within GitHub.",
      "type": [
        "object",
        "null"
      ],
      "properties": {
        "id": {
          "description": "Unique identifier of the GitHub app",
          "type": "integer",
          "examples": [
            37
          ]
        },
        "slug": {
          "description": "The slug name of the GitHub app",
          "type": "string",
          "examples": [
            "probot-owners"
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDExOkludGVncmF0aW9uMQ=="
          ]
        },
        "client_id": {
          "type": "string",
          "examples": [
            "\"Iv1.25b5d1e65ffc4022\""
          ]
        },
        "owner": {
          "oneOf": [
            {
              "$ref": "#/components/schemas/simple-user"
            },
            {
              "$ref": "#/components/schemas/enterprise"
            }
          ]
        },
        "name": {
          "description": "The name of the GitHub app",
          "type": "string",
          "examples": [
            "Probot Owners"
          ]
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "The description of the app."
          ]
        },
        "external_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://example.com"
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/apps/super-ci"
          ]
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2017-07-08T16:18:44-04:00"
          ]
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2017-07-08T16:18:44-04:00"
          ]
        },
        "permissions": {
          "description": "The set of permissions for the GitHub app",
          "type": "object",
          "properties": {
            "issues": {
              "type": "string"
            },
            "checks": {
              "type": "string"
            },
            "metadata": {
              "type": "string"
            },
            "contents": {
              "type": "string"
            },
            "deployments": {
              "type": "string"
            }
          },
          "additionalProperties": {
            "type": "string"
          },
          "example": {
            "issues": "read",
            "deployments": "write"
          }
        },
        "events": {
          "description": "The list of events for the GitHub app. Note that the `installation_target`, `security_advisory`, and `meta` events are not included because they are global events and not specific to an installation.",
          "type": "array",
          "items": {
            "type": "string"
          },
          "examples": [
            "label",
            "deployment"
          ]
        },
        "installations_count": {
          "description": "The number of installations associated with the GitHub app. Only returned when the integration is requesting details about itself.",
          "type": "integer",
          "examples": [
            5
          ]
        }
      },
      "required": [
        "id",
        "node_id",
        "owner",
        "name",
        "description",
        "external_url",
        "html_url",
        "created_at",
        "updated_at",
        "permissions",
        "events"
      ]
    },
    "pinned-issue-comment": {
      "title": "Pinned Issue Comment",
      "description": "Context around who pinned an issue comment and when it was pinned.",
      "type": "object",
      "properties": {
        "pinned_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2011-04-14T16:00:49Z"
          ]
        },
        "pinned_by": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/simple-user"
            }
          ]
        }
      },
      "required": [
        "pinned_at",
        "pinned_by"
      ]
    },
    "issue-dependencies-summary": {
      "title": "Issue Dependencies Summary",
      "type": "object",
      "properties": {
        "blocked_by": {
          "type": "integer"
        },
        "blocking": {
          "type": "integer"
        },
        "total_blocked_by": {
          "type": "integer"
        },
        "total_blocking": {
          "type": "integer"
        }
      },
      "required": [
        "blocked_by",
        "blocking",
        "total_blocked_by",
        "total_blocking"
      ]
    },
    "license-simple": {
      "title": "License Simple",
      "description": "License Simple",
      "type": "object",
      "properties": {
        "key": {
          "type": "string",
          "examples": [
            "mit"
          ]
        },
        "name": {
          "type": "string",
          "examples": [
            "MIT License"
          ]
        },
        "url": {
          "type": [
            "string",
            "null"
          ],
          "format": "uri",
          "examples": [
            "https://api.github.com/licenses/mit"
          ]
        },
        "spdx_id": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "MIT"
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDc6TGljZW5zZW1pdA=="
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri"
        }
      },
      "required": [
        "key",
        "name",
        "url",
        "spdx_id",
        "node_id"
      ]
    },
    "enterprise": {
      "title": "Enterprise",
      "description": "An enterprise on GitHub.",
      "type": "object",
      "properties": {
        "description": {
          "description": "A short description of the enterprise.",
          "type": [
            "string",
            "null"
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/enterprises/octo-business"
          ]
        },
        "website_url": {
          "description": "The enterprise's website URL.",
          "type": [
            "string",
            "null"
          ],
          "format": "uri"
        },
        "id": {
          "description": "Unique identifier of the enterprise",
          "type": "integer",
          "examples": [
            42
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDEwOlJlcG9zaXRvcnkxMjk2MjY5"
          ]
        },
        "name": {
          "description": "The name of the enterprise.",
          "type": "string",
          "examples": [
            "Octo Business"
          ]
        },
        "slug": {
          "description": "The slug url identifier for the enterprise.",
          "type": "string",
          "examples": [
            "octo-business"
          ]
        },
        "created_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2019-01-26T19:01:12Z"
          ]
        },
        "updated_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2019-01-26T19:14:43Z"
          ]
        },
        "avatar_url": {
          "type": "string",
          "format": "uri"
        }
      },
      "required": [
        "id",
        "node_id",
        "name",
        "slug",
        "html_url",
        "created_at",
        "updated_at",
        "avatar_url"
      ]
    },
    "issue-field-value": {
      "title": "Issue Field Value",
      "description": "A value assigned to an issue field",
      "type": "object",
      "properties": {
        "issue_field_id": {
          "description": "Unique identifier for the issue field.",
          "type": "integer",
          "format": "int64",
          "examples": [
            1
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "IFT_GDKND"
          ]
        },
        "data_type": {
          "description": "The data type of the issue field",
          "type": "string",
          "enum": [
            "text",
            "single_select",
            "number",
            "date"
          ],
          "examples": [
            "text"
          ]
        },
        "value": {
          "description": "The value of the issue field",
          "anyOf": [
            {
              "type": "string",
              "examples": [
                "Sample text"
              ]
            },
            {
              "type": "number",
              "examples": [
                42.5
              ]
            },
            {
              "type": "integer",
              "examples": [
                1
              ]
            }
          ],
          "type": [
            "null",
            "string",
            "number",
            "integer"
          ]
        },
        "single_select_option": {
          "description": "Details about the selected option (only present for single_select fields)",
          "type": [
            "object",
            "null"
          ],
          "properties": {
            "id": {
              "description": "Unique identifier for the option.",
              "type": "integer",
              "format": "int64",
              "examples": [
                1
              ]
            },
            "name": {
              "description": "The name of the option",
              "type": "string",
              "examples": [
                "High"
              ]
            },
            "color": {
              "description": "The color of the option",
              "type": "string",
              "examples": [
                "red"
              ]
            }
          },
          "required": [
            "id",
            "name",
            "color"
          ]
        }
      },
      "required": [
        "issue_field_id",
        "node_id",
        "data_type",
        "value"
      ]
    },
    "search-result-text-matches": {
      "title": "Search Result Text Matches",
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "object_url": {
            "type": "string"
          },
          "object_type": {
            "type": [
              "string",
              "null"
            ]
          },
          "property": {
            "type": "string"
          },
          "fragment": {
            "type": "string"
          },
          "matches": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "text": {
                  "type": "string"
                },
                "indices": {
                  "type": "array",
                  "items": {
                    "type": "integer"
                  }
                }
              }
            }
          }
        }
      }
    },
    "simple-user": {
      "title": "Simple User",
      "description": "A GitHub user.",
      "type": "object",
      "properties": {
        "name": {
          "type": [
            "string",
            "null"
          ]
        },
        "email": {
          "type": [
            "string",
            "null"
          ]
        },
        "login": {
          "type": "string",
          "examples": [
            "octocat"
          ]
        },
        "id": {
          "type": "integer",
          "format": "int64",
          "examples": [
            1
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDQ6VXNlcjE="
          ]
        },
        "avatar_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/images/error/octocat_happy.gif"
          ]
        },
        "gravatar_id": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "41d064eb2195891e12d0413f63227ea7"
          ]
        },
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat"
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat"
          ]
        },
        "followers_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/followers"
          ]
        },
        "following_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/users/octocat/following{/other_user}"
          ]
        },
        "gists_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/users/octocat/gists{/gist_id}"
          ]
        },
        "starred_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/users/octocat/starred{/owner}{/repo}"
          ]
        },
        "subscriptions_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/subscriptions"
          ]
        },
        "organizations_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/orgs"
          ]
        },
        "repos_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/repos"
          ]
        },
        "events_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/users/octocat/events{/privacy}"
          ]
        },
        "received_events_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/received_events"
          ]
        },
        "type": {
          "type": "string",
          "examples": [
            "User"
          ]
        },
        "site_admin": {
          "type": "boolean"
        },
        "starred_at": {
          "type": "string",
          "examples": [
            "\"2020-07-09T00:17:55Z\""
          ]
        },
        "user_view_type": {
          "type": "string",
          "examples": [
            "public"
          ]
        }
      },
      "required": [
        "avatar_url",
        "events_url",
        "followers_url",
        "following_url",
        "gists_url",
        "gravatar_id",
        "html_url",
        "id",
        "node_id",
        "login",
        "organizations_url",
        "received_events_url",
        "repos_url",
        "site_admin",
        "starred_url",
        "subscriptions_url",
        "type",
        "url"
      ]
    },
    "issue": {
      "title": "Issue",
      "description": "Issues are a great way to keep track of tasks, enhancements, and bugs for your projects.",
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "format": "int64"
        },
        "node_id": {
          "type": "string"
        },
        "url": {
          "description": "URL for the issue",
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repositories/42/issues/1"
          ]
        },
        "repository_url": {
          "type": "string",
          "format": "uri"
        },
        "labels_url": {
          "type": "string"
        },
        "comments_url": {
          "type": "string",
          "format": "uri"
        },
        "events_url": {
          "type": "string",
          "format": "uri"
        },
        "html_url": {
          "type": "string",
          "format": "uri"
        },
        "number": {
          "description": "Number uniquely identifying the issue within its repository",
          "type": "integer",
          "examples": [
            42
          ]
        },
        "state": {
          "description": "State of the issue; either 'open' or 'closed'",
          "type": "string",
          "examples": [
            "open"
          ]
        },
        "state_reason": {
          "description": "The reason for the current state",
          "type": [
            "string",
            "null"
          ],
          "enum": [
            "completed",
            "reopened",
            "not_planned",
            "duplicate",
            null
          ],
          "examples": [
            "not_planned"
          ]
        },
        "title": {
          "description": "Title of the issue",
          "type": "string",
          "examples": [
            "Widget creation fails in Safari on OS X 10.8"
          ]
        },
        "body": {
          "description": "Contents of the issue",
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "It looks like the new widget form is broken on Safari. When I try and create the widget, Safari crashes. This is reproducible on 10.8, but not 10.9. Maybe a browser bug?"
          ]
        },
        "user": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/simple-user"
            }
          ]
        },
        "labels": {
          "description": "Labels to associate with this issue; pass one or more label names to replace the set of labels on this issue; send an empty array to clear all labels from the issue; note that the labels are silently dropped for users without push access to the repository",
          "type": "array",
          "items": {
            "oneOf": [
              {
                "type": "string"
              },
              {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "integer",
                    "format": "int64"
                  },
                  "node_id": {
                    "type": "string"
                  },
                  "url": {
                    "type": "string",
                    "format": "uri"
                  },
                  "name": {
                    "type": "string"
                  },
                  "description": {
                    "type": [
                      "string",
                      "null"
                    ]
                  },
                  "color": {
                    "type": [
                      "string",
                      "null"
                    ]
                  },
                  "default": {
                    "type": "boolean"
                  }
                }
              }
            ]
          },
          "examples": [
            "bug",
            "registration"
          ]
        },
        "assignees": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "milestone": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/milestone"
            }
          ]
        },
        "locked": {
          "type": "boolean"
        },
        "active_lock_reason": {
          "type": [
            "string",
            "null"
          ]
        },
        "comments": {
          "type": "integer"
        },
        "pull_request": {
          "type": "object",
          "properties": {
            "merged_at": {
              "type": [
                "string",
                "null"
              ],
              "format": "date-time",
              "nullable": false
            },
            "diff_url": {
              "type": [
                "string",
                "null"
              ],
              "format": "uri",
              "nullable": false
            },
            "html_url": {
              "type": [
                "string",
                "null"
              ],
              "format": "uri",
              "nullable": false
            },
            "patch_url": {
              "type": [
                "string",
                "null"
              ],
              "format": "uri",
              "nullable": false
            },
            "url": {
              "type": [
                "string",
                "null"
              ],
              "format": "uri",
              "nullable": false
            }
          },
          "required": [
            "diff_url",
            "html_url",
            "patch_url",
            "url"
          ]
        },
        "closed_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time"
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        },
        "draft": {
          "type": "boolean"
        },
        "closed_by": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/simple-user"
            }
          ]
        },
        "body_html": {
          "type": "string"
        },
        "body_text": {
          "type": "string"
        },
        "timeline_url": {
          "type": "string",
          "format": "uri"
        },
        "type": {
          "$ref": "#/components/schemas/issue-type"
        },
        "repository": {
          "$ref": "#/components/schemas/repository"
        },
        "performed_via_github_app": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/integration"
            }
          ]
        },
        "author_association": {
          "$ref": "#/components/schemas/author-association"
        },
        "reactions": {
          "$ref": "#/components/schemas/reaction-rollup"
        },
        "sub_issues_summary": {
          "$ref": "#/components/schemas/sub-issues-summary"
        },
        "parent_issue_url": {
          "description": "URL to get the parent issue of this issue, if it is a sub-issue",
          "type": [
            "string",
            "null"
          ],
          "format": "uri"
        },
        "pinned_comment": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/issue-comment"
            }
          ]
        },
        "issue_dependencies_summary": {
          "$ref": "#/components/schemas/issue-dependencies-summary"
        },
        "issue_field_values": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/issue-field-value"
          }
        }
      },
      "required": [
        "closed_at",
        "comments",
        "comments_url",
        "events_url",
        "html_url",
        "id",
        "node_id",
        "labels",
        "labels_url",
        "milestone",
        "number",
        "repository_url",
        "state",
        "locked",
        "title",
        "url",
        "user",
        "created_at",
        "updated_at"
      ]
    },
    "author-association": {
      "title": "author_association",
      "type": "string",
      "description": "How the author is associated with the repository.",
      "enum": [
        "COLLABORATOR",
        "CONTRIBUTOR",
        "FIRST_TIMER",
        "FIRST_TIME_CONTRIBUTOR",
        "MANNEQUIN",
        "MEMBER",
        "NONE",
        "OWNER"
      ],
      "examples": [
        "OWNER"
      ]
    },
    "repository": {
      "title": "Repository",
      "description": "A repository on GitHub.",
      "type": "object",
      "properties": {
        "id": {
          "description": "Unique identifier of the repository",
          "type": "integer",
          "format": "int64",
          "examples": [
            42
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDEwOlJlcG9zaXRvcnkxMjk2MjY5"
          ]
        },
        "name": {
          "description": "The name of the repository.",
          "type": "string",
          "examples": [
            "Team Environment"
          ]
        },
        "full_name": {
          "type": "string",
          "examples": [
            "octocat/Hello-World"
          ]
        },
        "license": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/license-simple"
            }
          ]
        },
        "forks": {
          "type": "integer"
        },
        "permissions": {
          "type": "object",
          "properties": {
            "admin": {
              "type": "boolean"
            },
            "pull": {
              "type": "boolean"
            },
            "triage": {
              "type": "boolean"
            },
            "push": {
              "type": "boolean"
            },
            "maintain": {
              "type": "boolean"
            }
          },
          "required": [
            "admin",
            "pull",
            "push"
          ]
        },
        "owner": {
          "$ref": "#/components/schemas/simple-user"
        },
        "private": {
          "description": "Whether the repository is private or public.",
          "default": false,
          "type": "boolean"
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat/Hello-World"
          ]
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "This your first repo!"
          ]
        },
        "fork": {
          "type": "boolean"
        },
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World"
          ]
        },
        "archive_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}"
          ]
        },
        "assignees_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/assignees{/user}"
          ]
        },
        "blobs_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}"
          ]
        },
        "branches_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/branches{/branch}"
          ]
        },
        "collaborators_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}"
          ]
        },
        "comments_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/comments{/number}"
          ]
        },
        "commits_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/commits{/sha}"
          ]
        },
        "compare_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}"
          ]
        },
        "contents_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/contents/{+path}"
          ]
        },
        "contributors_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/contributors"
          ]
        },
        "deployments_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/deployments"
          ]
        },
        "downloads_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/downloads"
          ]
        },
        "events_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/events"
          ]
        },
        "forks_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/forks"
          ]
        },
        "git_commits_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/commits{/sha}"
          ]
        },
        "git_refs_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/refs{/sha}"
          ]
        },
        "git_tags_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/tags{/sha}"
          ]
        },
        "git_url": {
          "type": "string",
          "examples": [
            "git:github.com/octocat/Hello-World.git"
          ]
        },
        "issue_comment_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/issues/comments{/number}"
          ]
        },
        "issue_events_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/issues/events{/number}"
          ]
        },
        "issues_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/issues{/number}"
          ]
        },
        "keys_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/keys{/key_id}"
          ]
        },
        "labels_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/labels{/name}"
          ]
        },
        "languages_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/languages"
          ]
        },
        "merges_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/merges"
          ]
        },
        "milestones_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/milestones{/number}"
          ]
        },
        "notifications_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}"
          ]
        },
        "pulls_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/pulls{/number}"
          ]
        },
        "releases_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/releases{/id}"
          ]
        },
        "ssh_url": {
          "type": "string",
          "examples": [
            "git@github.com:octocat/Hello-World.git"
          ]
        },
        "stargazers_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/stargazers"
          ]
        },
        "statuses_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/statuses/{sha}"
          ]
        },
        "subscribers_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/subscribers"
          ]
        },
        "subscription_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/subscription"
          ]
        },
        "tags_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/tags"
          ]
        },
        "teams_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/teams"
          ]
        },
        "trees_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/trees{/sha}"
          ]
        },
        "clone_url": {
          "type": "string",
          "examples": [
            "https://github.com/octocat/Hello-World.git"
          ]
        },
        "mirror_url": {
          "type": [
            "string",
            "null"
          ],
          "format": "uri",
          "examples": [
            "git:git.example.com/octocat/Hello-World"
          ]
        },
        "hooks_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/hooks"
          ]
        },
        "svn_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://svn.github.com/octocat/Hello-World"
          ]
        },
        "homepage": {
          "type": [
            "string",
            "null"
          ],
          "format": "uri",
          "examples": [
            "https://github.com"
          ]
        },
        "language": {
          "type": [
            "string",
            "null"
          ]
        },
        "forks_count": {
          "type": "integer",
          "examples": [
            9
          ]
        },
        "stargazers_count": {
          "type": "integer",
          "examples": [
            80
          ]
        },
        "watchers_count": {
          "type": "integer",
          "examples": [
            80
          ]
        },
        "size": {
          "description": "The size of the repository, in kilobytes. Size is calculated hourly. When a repository is initially created, the size is 0.",
          "type": "integer",
          "examples": [
            108
          ]
        },
        "default_branch": {
          "description": "The default branch of the repository.",
          "type": "string",
          "examples": [
            "master"
          ]
        },
        "open_issues_count": {
          "type": "integer",
          "examples": [
            0
          ]
        },
        "is_template": {
          "description": "Whether this repository acts as a template that can be used to generate new repositories.",
          "default": false,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "topics": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "has_issues": {
          "description": "Whether issues are enabled.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_projects": {
          "description": "Whether projects are enabled.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_wiki": {
          "description": "Whether the wiki is enabled.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_pages": {
          "type": "boolean"
        },
        "has_discussions": {
          "description": "Whether discussions are enabled.",
          "default": false,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_pull_requests": {
          "description": "Whether pull requests are enabled.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "pull_request_creation_policy": {
          "description": "The policy controlling who can create pull requests: all or collaborators_only.",
          "type": "string",
          "enum": [
            "all",
            "collaborators_only"
          ],
          "examples": [
            "all"
          ]
        },
        "archived": {
          "description": "Whether the repository is archived.",
          "default": false,
          "type": "boolean"
        },
        "disabled": {
          "type": "boolean",
          "description": "Returns whether or not this repository disabled."
        },
        "visibility": {
          "description": "The repository visibility: public, private, or internal.",
          "default": "public",
          "type": "string"
        },
        "pushed_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:06:43Z"
          ]
        },
        "created_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "updated_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:14:43Z"
          ]
        },
        "allow_rebase_merge": {
          "description": "Whether to allow rebase merges for pull requests.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "temp_clone_token": {
          "type": "string"
        },
        "allow_squash_merge": {
          "description": "Whether to allow squash merges for pull requests.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "allow_auto_merge": {
          "description": "Whether to allow Auto-merge to be used on pull requests.",
          "default": false,
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "delete_branch_on_merge": {
          "description": "Whether to delete head branches when pull requests are merged",
          "default": false,
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "allow_update_branch": {
          "description": "Whether or not a pull request head branch that is behind its base branch can always be updated even if it is not required to be up to date before merging.",
          "default": false,
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "squash_merge_commit_title": {
          "type": "string",
          "enum": [
            "PR_TITLE",
            "COMMIT_OR_PR_TITLE"
          ],
          "description": "The default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit)."
        },
        "squash_merge_commit_message": {
          "type": "string",
          "enum": [
            "PR_BODY",
            "COMMIT_MESSAGES",
            "BLANK"
          ],
          "description": "The default value for a squash merge commit message:\n\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message."
        },
        "merge_commit_title": {
          "type": "string",
          "enum": [
            "PR_TITLE",
            "MERGE_MESSAGE"
          ],
          "description": "The default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name)."
        },
        "merge_commit_message": {
          "type": "string",
          "enum": [
            "PR_BODY",
            "PR_TITLE",
            "BLANK"
          ],
          "description": "The default value for a merge commit message.\n\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message."
        },
        "allow_merge_commit": {
          "description": "Whether to allow merge commits for pull requests.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "allow_forking": {
          "description": "Whether to allow forking this repo",
          "type": "boolean"
        },
        "web_commit_signoff_required": {
          "description": "Whether to require contributors to sign off on web-based commits",
          "default": false,
          "type": "boolean"
        },
        "open_issues": {
          "type": "integer"
        },
        "watchers": {
          "type": "integer"
        },
        "starred_at": {
          "type": "string",
          "examples": [
            "\"2020-07-09T00:17:42Z\""
          ]
        },
        "anonymous_access_enabled": {
          "type": "boolean",
          "description": "Whether anonymous git access is enabled for this repository"
        },
        "code_search_index_status": {
          "type": "object",
          "description": "The status of the code search index for this repository",
          "properties": {
            "lexical_search_ok": {
              "type": "boolean"
            },
            "lexical_commit_sha": {
              "type": "string"
            }
          }
        }
      },
      "required": [
        "archive_url",
        "assignees_url",
        "blobs_url",
        "branches_url",
        "collaborators_url",
        "comments_url",
        "commits_url",
        "compare_url",
        "contents_url",
        "contributors_url",
        "deployments_url",
        "description",
        "downloads_url",
        "events_url",
        "fork",
        "forks_url",
        "full_name",
        "git_commits_url",
        "git_refs_url",
        "git_tags_url",
        "hooks_url",
        "html_url",
        "id",
        "node_id",
        "issue_comment_url",
        "issue_events_url",
        "issues_url",
        "keys_url",
        "labels_url",
        "languages_url",
        "merges_url",
        "milestones_url",
        "name",
        "notifications_url",
        "owner",
        "private",
        "pulls_url",
        "releases_url",
        "stargazers_url",
        "statuses_url",
        "subscribers_url",
        "subscription_url",
        "tags_url",
        "teams_url",
        "trees_url",
        "url",
        "clone_url",
        "default_branch",
        "forks",
        "forks_count",
        "git_url",
        "has_issues",
        "has_projects",
        "has_wiki",
        "has_pages",
        "homepage",
        "language",
        "archived",
        "disabled",
        "mirror_url",
        "open_issues",
        "open_issues_count",
        "license",
        "pushed_at",
        "size",
        "ssh_url",
        "stargazers_count",
        "svn_url",
        "watchers",
        "watchers_count",
        "created_at",
        "updated_at"
      ]
    },
    "milestone": {
      "title": "Milestone",
      "description": "A collection of related issues and pull requests.",
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/milestones/1"
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat/Hello-World/milestones/v1.0"
          ]
        },
        "labels_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels"
          ]
        },
        "id": {
          "type": "integer",
          "examples": [
            1002604
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDk6TWlsZXN0b25lMTAwMjYwNA=="
          ]
        },
        "number": {
          "description": "The number of the milestone.",
          "type": "integer",
          "examples": [
            42
          ]
        },
        "state": {
          "description": "The state of the milestone.",
          "type": "string",
          "enum": [
            "open",
            "closed"
          ],
          "default": "open",
          "examples": [
            "open"
          ]
        },
        "title": {
          "description": "The title of the milestone.",
          "type": "string",
          "examples": [
            "v1.0"
          ]
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "Tracking milestone for version 1.0"
          ]
        },
        "creator": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/simple-user"
            }
          ]
        },
        "open_issues": {
          "type": "integer",
          "examples": [
            4
          ]
        },
        "closed_issues": {
          "type": "integer",
          "examples": [
            8
          ]
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2011-04-10T20:09:31Z"
          ]
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2014-03-03T18:58:10Z"
          ]
        },
        "closed_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2013-02-12T13:22:01Z"
          ]
        },
        "due_on": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2012-10-09T23:39:01Z"
          ]
        }
      },
      "required": [
        "closed_issues",
        "creator",
        "description",
        "due_on",
        "closed_at",
        "id",
        "node_id",
        "labels_url",
        "html_url",
        "number",
        "open_issues",
        "state",
        "title",
        "url",
        "created_at",
        "updated_at"
      ]
    },
    "sub-issues-summary": {
      "title": "Sub-issues Summary",
      "type": "object",
      "properties": {
        "total": {
          "type": "integer"
        },
        "completed": {
          "type": "integer"
        },
        "percent_completed": {
          "type": "integer"
        }
      },
      "required": [
        "total",
        "completed",
        "percent_completed"
      ]
    },
    "issue-type": {
      "title": "Issue Type",
      "description": "The type of issue.",
      "type": [
        "object",
        "null"
      ],
      "properties": {
        "id": {
          "type": "integer",
          "description": "The unique identifier of the issue type."
        },
        "node_id": {
          "type": "string",
          "description": "The node identifier of the issue type."
        },
        "name": {
          "type": "string",
          "description": "The name of the issue type."
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "description": "The description of the issue type."
        },
        "color": {
          "type": [
            "string",
            "null"
          ],
          "description": "The color of the issue type.",
          "enum": [
            "gray",
            "blue",
            "green",
            "yellow",
            "orange",
            "red",
            "pink",
            "purple",
            null
          ]
        },
        "created_at": {
          "type": "string",
          "description": "The time the issue type created.",
          "format": "date-time"
        },
        "updated_at": {
          "type": "string",
          "description": "The time the issue type last updated.",
          "format": "date-time"
        },
        "is_enabled": {
          "type": "boolean",
          "description": "The enabled state of the issue type."
        }
      },
      "required": [
        "id",
        "node_id",
        "name",
        "description"
      ]
    },
    "issue-search-result-item": {
      "title": "Issue Search Result Item",
      "description": "Issue Search Result Item",
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri"
        },
        "repository_url": {
          "type": "string",
          "format": "uri"
        },
        "labels_url": {
          "type": "string"
        },
        "comments_url": {
          "type": "string",
          "format": "uri"
        },
        "events_url": {
          "type": "string",
          "format": "uri"
        },
        "html_url": {
          "type": "string",
          "format": "uri"
        },
        "id": {
          "type": "integer",
          "format": "int64"
        },
        "node_id": {
          "type": "string"
        },
        "number": {
          "type": "integer"
        },
        "title": {
          "type": "string"
        },
        "locked": {
          "type": "boolean"
        },
        "active_lock_reason": {
          "type": [
            "string",
            "null"
          ]
        },
        "assignees": {
          "type": [
            "array",
            "null"
          ],
          "items": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "user": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/simple-user"
            }
          ]
        },
        "labels": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "integer",
                "format": "int64"
              },
              "node_id": {
                "type": "string"
              },
              "url": {
                "type": "string"
              },
              "name": {
                "type": "string"
              },
              "color": {
                "type": "string"
              },
              "default": {
                "type": "boolean"
              },
              "description": {
                "type": [
                  "string",
                  "null"
                ]
              }
            }
          }
        },
        "sub_issues_summary": {
          "$ref": "#/components/schemas/sub-issues-summary"
        },
        "issue_dependencies_summary": {
          "$ref": "#/components/schemas/issue-dependencies-summary"
        },
        "issue_field_values": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/issue-field-value"
          }
        },
        "state": {
          "type": "string"
        },
        "state_reason": {
          "type": [
            "string",
            "null"
          ]
        },
        "milestone": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/milestone"
            }
          ]
        },
        "comments": {
          "type": "integer"
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        },
        "closed_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time"
        },
        "text_matches": {
          "$ref": "#/components/schemas/search-result-text-matches"
        },
        "pull_request": {
          "type": "object",
          "properties": {
            "merged_at": {
              "type": [
                "string",
                "null"
              ],
              "format": "date-time"
            },
            "diff_url": {
              "type": [
                "string",
                "null"
              ],
              "format": "uri"
            },
            "html_url": {
              "type": [
                "string",
                "null"
              ],
              "format": "uri"
            },
            "patch_url": {
              "type": [
                "string",
                "null"
              ],
              "format": "uri"
            },
            "url": {
              "type": [
                "string",
                "null"
              ],
              "format": "uri"
            }
          },
          "required": [
            "diff_url",
            "html_url",
            "patch_url",
            "url"
          ]
        },
        "body": {
          "type": "string"
        },
        "score": {
          "type": "number"
        },
        "author_association": {
          "$ref": "#/components/schemas/author-association"
        },
        "draft": {
          "type": "boolean"
        },
        "repository": {
          "$ref": "#/components/schemas/repository"
        },
        "body_html": {
          "type": "string"
        },
        "body_text": {
          "type": "string"
        },
        "timeline_url": {
          "type": "string",
          "format": "uri"
        },
        "type": {
          "$ref": "#/components/schemas/issue-type"
        },
        "performed_via_github_app": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/integration"
            }
          ]
        },
        "pinned_comment": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/issue-comment"
            }
          ]
        },
        "reactions": {
          "$ref": "#/components/schemas/reaction-rollup"
        }
      },
      "required": [
        "closed_at",
        "comments",
        "comments_url",
        "events_url",
        "html_url",
        "id",
        "node_id",
        "labels",
        "labels_url",
        "milestone",
        "number",
        "repository_url",
        "state",
        "locked",
        "title",
        "url",
        "user",
        "author_association",
        "created_at",
        "updated_at",
        "score"
      ]
    },
    "reaction-rollup": {
      "title": "Reaction Rollup",
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri"
        },
        "total_count": {
          "type": "integer"
        },
        "+1": {
          "type": "integer"
        },
        "-1": {
          "type": "integer"
        },
        "laugh": {
          "type": "integer"
        },
        "confused": {
          "type": "integer"
        },
        "heart": {
          "type": "integer"
        },
        "hooray": {
          "type": "integer"
        },
        "eyes": {
          "type": "integer"
        },
        "rocket": {
          "type": "integer"
        }
      },
      "required": [
        "url",
        "total_count",
        "+1",
        "-1",
        "laugh",
        "confused",
        "heart",
        "hooray",
        "eyes",
        "rocket"
      ]
    },
    "issue-comment": {
      "title": "Issue Comment",
      "description": "Comments provide a way for people to collaborate on an issue.",
      "type": "object",
      "properties": {
        "id": {
          "description": "Unique identifier of the issue comment",
          "type": "integer",
          "format": "int64",
          "examples": [
            42
          ]
        },
        "node_id": {
          "type": "string"
        },
        "url": {
          "description": "URL for the issue comment",
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repositories/42/issues/comments/1"
          ]
        },
        "body": {
          "description": "Contents of the issue comment",
          "type": "string",
          "examples": [
            "What version of Safari were you using when you observed this bug?"
          ]
        },
        "body_text": {
          "type": "string"
        },
        "body_html": {
          "type": "string"
        },
        "html_url": {
          "type": "string",
          "format": "uri"
        },
        "user": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/simple-user"
            }
          ]
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2011-04-14T16:00:49Z"
          ]
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2011-04-14T16:00:49Z"
          ]
        },
        "issue_url": {
          "type": "string",
          "format": "uri"
        },
        "author_association": {
          "$ref": "#/components/schemas/author-association"
        },
        "performed_via_github_app": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/integration"
            }
          ]
        },
        "reactions": {
          "$ref": "#/components/schemas/reaction-rollup"
        },
        "pin": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/pinned-issue-comment"
            }
          ]
        }
      },
      "required": [
        "id",
        "node_id",
        "html_url",
        "issue_url",
        "user",
        "url",
        "created_at",
        "updated_at"
      ]
    }
  },
  "primary_response_schema": {
    "title": "Issue",
    "description": "Issues are a great way to keep track of tasks, enhancements, and bugs for your projects.",
    "type": "object",
    "properties": {
      "id": {
        "type": "integer",
        "format": "int64"
      },
      "node_id": {
        "type": "string"
      },
      "url": {
        "description": "URL for the issue",
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/repositories/42/issues/1"
        ]
      },
      "repository_url": {
        "type": "string",
        "format": "uri"
      },
      "labels_url": {
        "type": "string"
      },
      "comments_url": {
        "type": "string",
        "format": "uri"
      },
      "events_url": {
        "type": "string",
        "format": "uri"
      },
      "html_url": {
        "type": "string",
        "format": "uri"
      },
      "number": {
        "description": "Number uniquely identifying the issue within its repository",
        "type": "integer",
        "examples": [
          42
        ]
      },
      "state": {
        "description": "State of the issue; either 'open' or 'closed'",
        "type": "string",
        "examples": [
          "open"
        ]
      },
      "state_reason": {
        "description": "The reason for the current state",
        "type": [
          "string",
          "null"
        ],
        "enum": [
          "completed",
          "reopened",
          "not_planned",
          "duplicate",
          null
        ],
        "examples": [
          "not_planned"
        ]
      },
      "title": {
        "description": "Title of the issue",
        "type": "string",
        "examples": [
          "Widget creation fails in Safari on OS X 10.8"
        ]
      },
      "body": {
        "description": "Contents of the issue",
        "type": [
          "string",
          "null"
        ],
        "examples": [
          "It looks like the new widget form is broken on Safari. When I try and create the widget, Safari crashes. This is reproducible on 10.8, but not 10.9. Maybe a browser bug?"
        ]
      },
      "user": {
        "anyOf": [
          {
            "type": "null"
          },
          {
            "$ref": "#/components/schemas/simple-user"
          }
        ]
      },
      "labels": {
        "description": "Labels to associate with this issue; pass one or more label names to replace the set of labels on this issue; send an empty array to clear all labels from the issue; note that the labels are silently dropped for users without push access to the repository",
        "type": "array",
        "items": {
          "oneOf": [
            {
              "type": "string"
            },
            {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer",
                  "format": "int64"
                },
                "node_id": {
                  "type": "string"
                },
                "url": {
                  "type": "string",
                  "format": "uri"
                },
                "name": {
                  "type": "string"
                },
                "description": {
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "color": {
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "default": {
                  "type": "boolean"
                }
              }
            }
          ]
        },
        "examples": [
          "bug",
          "registration"
        ]
      },
      "assignees": {
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/simple-user"
        }
      },
      "milestone": {
        "anyOf": [
          {
            "type": "null"
          },
          {
            "$ref": "#/components/schemas/milestone"
          }
        ]
      },
      "locked": {
        "type": "boolean"
      },
      "active_lock_reason": {
        "type": [
          "string",
          "null"
        ]
      },
      "comments": {
        "type": "integer"
      },
      "pull_request": {
        "type": "object",
        "properties": {
          "merged_at": {
            "type": [
              "string",
              "null"
            ],
            "format": "date-time",
            "nullable": false
          },
          "diff_url": {
            "type": [
              "string",
              "null"
            ],
            "format": "uri",
            "nullable": false
          },
          "html_url": {
            "type": [
              "string",
              "null"
            ],
            "format": "uri",
            "nullable": false
          },
          "patch_url": {
            "type": [
              "string",
              "null"
            ],
            "format": "uri",
            "nullable": false
          },
          "url": {
            "type": [
              "string",
              "null"
            ],
            "format": "uri",
            "nullable": false
          }
        },
        "required": [
          "diff_url",
          "html_url",
          "patch_url",
          "url"
        ]
      },
      "closed_at": {
        "type": [
          "string",
          "null"
        ],
        "format": "date-time"
      },
      "created_at": {
        "type": "string",
        "format": "date-time"
      },
      "updated_at": {
        "type": "string",
        "format": "date-time"
      },
      "draft": {
        "type": "boolean"
      },
      "closed_by": {
        "anyOf": [
          {
            "type": "null"
          },
          {
            "$ref": "#/components/schemas/simple-user"
          }
        ]
      },
      "body_html": {
        "type": "string"
      },
      "body_text": {
        "type": "string"
      },
      "timeline_url": {
        "type": "string",
        "format": "uri"
      },
      "type": {
        "$ref": "#/components/schemas/issue-type"
      },
      "repository": {
        "$ref": "#/components/schemas/repository"
      },
      "performed_via_github_app": {
        "anyOf": [
          {
            "type": "null"
          },
          {
            "$ref": "#/components/schemas/integration"
          }
        ]
      },
      "author_association": {
        "$ref": "#/components/schemas/author-association"
      },
      "reactions": {
        "$ref": "#/components/schemas/reaction-rollup"
      },
      "sub_issues_summary": {
        "$ref": "#/components/schemas/sub-issues-summary"
      },
      "parent_issue_url": {
        "description": "URL to get the parent issue of this issue, if it is a sub-issue",
        "type": [
          "string",
          "null"
        ],
        "format": "uri"
      },
      "pinned_comment": {
        "anyOf": [
          {
            "type": "null"
          },
          {
            "$ref": "#/components/schemas/issue-comment"
          }
        ]
      },
      "issue_dependencies_summary": {
        "$ref": "#/components/schemas/issue-dependencies-summary"
      },
      "issue_field_values": {
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/issue-field-value"
        }
      }
    },
    "required": [
      "closed_at",
      "comments",
      "comments_url",
      "events_url",
      "html_url",
      "id",
      "node_id",
      "labels",
      "labels_url",
      "milestone",
      "number",
      "repository_url",
      "state",
      "locked",
      "title",
      "url",
      "user",
      "created_at",
      "updated_at"
    ]
  }
}
```

### Relationship manifest

```yaml
github_issues:
  user_id:
    target_table: github_users
    target_column: id
    confidence: high
    reason: 'response schema: user.id'
  repo_id:
    target_table: github_repos
    target_column: id
    confidence: high
    reason: 'response schema: repository.id'

```

### FK dependency schemas (for stub creation if needed)

```json
{
  "repos": {
    "primary_response_schema": {
      "title": "Team Repository",
      "description": "A team's access to a repository.",
      "type": "object",
      "properties": {
        "id": {
          "description": "Unique identifier of the repository",
          "type": "integer",
          "examples": [
            42
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDEwOlJlcG9zaXRvcnkxMjk2MjY5"
          ]
        },
        "name": {
          "description": "The name of the repository.",
          "type": "string",
          "examples": [
            "Team Environment"
          ]
        },
        "full_name": {
          "type": "string",
          "examples": [
            "octocat/Hello-World"
          ]
        },
        "license": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/license-simple"
            }
          ]
        },
        "forks": {
          "type": "integer"
        },
        "permissions": {
          "type": "object",
          "properties": {
            "admin": {
              "type": "boolean"
            },
            "pull": {
              "type": "boolean"
            },
            "triage": {
              "type": "boolean"
            },
            "push": {
              "type": "boolean"
            },
            "maintain": {
              "type": "boolean"
            }
          },
          "required": [
            "admin",
            "pull",
            "push"
          ]
        },
        "role_name": {
          "type": "string",
          "examples": [
            "admin"
          ]
        },
        "owner": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/simple-user"
            }
          ]
        },
        "private": {
          "description": "Whether the repository is private or public.",
          "default": false,
          "type": "boolean"
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat/Hello-World"
          ]
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "This your first repo!"
          ]
        },
        "fork": {
          "type": "boolean"
        },
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World"
          ]
        },
        "archive_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}"
          ]
        },
        "assignees_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/assignees{/user}"
          ]
        },
        "blobs_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}"
          ]
        },
        "branches_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/branches{/branch}"
          ]
        },
        "collaborators_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}"
          ]
        },
        "comments_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/comments{/number}"
          ]
        },
        "commits_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/commits{/sha}"
          ]
        },
        "compare_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}"
          ]
        },
        "contents_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/contents/{+path}"
          ]
        },
        "contributors_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/contributors"
          ]
        },
        "deployments_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/deployments"
          ]
        },
        "downloads_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/downloads"
          ]
        },
        "events_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/events"
          ]
        },
        "forks_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/forks"
          ]
        },
        "git_commits_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/commits{/sha}"
          ]
        },
        "git_refs_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/refs{/sha}"
          ]
        },
        "git_tags_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/tags{/sha}"
          ]
        },
        "git_url": {
          "type": "string",
          "examples": [
            "git:github.com/octocat/Hello-World.git"
          ]
        },
        "issue_comment_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/issues/comments{/number}"
          ]
        },
        "issue_events_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/issues/events{/number}"
          ]
        },
        "issues_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/issues{/number}"
          ]
        },
        "keys_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/keys{/key_id}"
          ]
        },
        "labels_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/labels{/name}"
          ]
        },
        "languages_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/languages"
          ]
        },
        "merges_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/merges"
          ]
        },
        "milestones_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/milestones{/number}"
          ]
        },
        "notifications_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}"
          ]
        },
        "pulls_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/pulls{/number}"
          ]
        },
        "releases_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/releases{/id}"
          ]
        },
        "ssh_url": {
          "type": "string",
          "examples": [
            "git@github.com:octocat/Hello-World.git"
          ]
        },
        "stargazers_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/stargazers"
          ]
        },
        "statuses_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/statuses/{sha}"
          ]
        },
        "subscribers_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/subscribers"
          ]
        },
        "subscription_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/subscription"
          ]
        },
        "tags_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/tags"
          ]
        },
        "teams_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/teams"
          ]
        },
        "trees_url": {
          "type": "string",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/git/trees{/sha}"
          ]
        },
        "clone_url": {
          "type": "string",
          "examples": [
            "https://github.com/octocat/Hello-World.git"
          ]
        },
        "mirror_url": {
          "type": [
            "string",
            "null"
          ],
          "format": "uri",
          "examples": [
            "git:git.example.com/octocat/Hello-World"
          ]
        },
        "hooks_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "http://api.github.com/repos/octocat/Hello-World/hooks"
          ]
        },
        "svn_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://svn.github.com/octocat/Hello-World"
          ]
        },
        "homepage": {
          "type": [
            "string",
            "null"
          ],
          "format": "uri",
          "examples": [
            "https://github.com"
          ]
        },
        "language": {
          "type": [
            "string",
            "null"
          ]
        },
        "forks_count": {
          "type": "integer",
          "examples": [
            9
          ]
        },
        "stargazers_count": {
          "type": "integer",
          "examples": [
            80
          ]
        },
        "watchers_count": {
          "type": "integer",
          "examples": [
            80
          ]
        },
        "size": {
          "type": "integer",
          "examples": [
            108
          ]
        },
        "default_branch": {
          "description": "The default branch of the repository.",
          "type": "string",
          "examples": [
            "master"
          ]
        },
        "open_issues_count": {
          "type": "integer",
          "examples": [
            0
          ]
        },
        "is_template": {
          "description": "Whether this repository acts as a template that can be used to generate new repositories.",
          "default": false,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "topics": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "has_issues": {
          "description": "Whether issues are enabled.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_projects": {
          "description": "Whether projects are enabled.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_wiki": {
          "description": "Whether the wiki is enabled.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_pages": {
          "type": "boolean"
        },
        "archived": {
          "description": "Whether the repository is archived.",
          "default": false,
          "type": "boolean"
        },
        "disabled": {
          "type": "boolean",
          "description": "Returns whether or not this repository disabled."
        },
        "visibility": {
          "description": "The repository visibility: public, private, or internal.",
          "default": "public",
          "type": "string"
        },
        "pushed_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:06:43Z"
          ]
        },
        "created_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "updated_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:14:43Z"
          ]
        },
        "allow_rebase_merge": {
          "description": "Whether to allow rebase merges for pull requests.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "temp_clone_token": {
          "type": "string"
        },
        "allow_squash_merge": {
          "description": "Whether to allow squash merges for pull requests.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "allow_auto_merge": {
          "description": "Whether to allow Auto-merge to be used on pull requests.",
          "default": false,
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "delete_branch_on_merge": {
          "description": "Whether to delete head branches when pull requests are merged",
          "default": false,
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "allow_merge_commit": {
          "description": "Whether to allow merge commits for pull requests.",
          "default": true,
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "allow_forking": {
          "description": "Whether to allow forking this repo",
          "default": false,
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "web_commit_signoff_required": {
          "description": "Whether to require contributors to sign off on web-based commits",
          "default": false,
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "subscribers_count": {
          "type": "integer"
        },
        "network_count": {
          "type": "integer"
        },
        "open_issues": {
          "type": "integer"
        },
        "watchers": {
          "type": "integer"
        },
        "master_branch": {
          "type": "string"
        }
      },
      "required": [
        "archive_url",
        "assignees_url",
        "blobs_url",
        "branches_url",
        "collaborators_url",
        "comments_url",
        "commits_url",
        "compare_url",
        "contents_url",
        "contributors_url",
        "deployments_url",
        "description",
        "downloads_url",
        "events_url",
        "fork",
        "forks_url",
        "full_name",
        "git_commits_url",
        "git_refs_url",
        "git_tags_url",
        "hooks_url",
        "html_url",
        "id",
        "node_id",
        "issue_comment_url",
        "issue_events_url",
        "issues_url",
        "keys_url",
        "labels_url",
        "languages_url",
        "merges_url",
        "milestones_url",
        "name",
        "notifications_url",
        "owner",
        "private",
        "pulls_url",
        "releases_url",
        "stargazers_url",
        "statuses_url",
        "subscribers_url",
        "subscription_url",
        "tags_url",
        "teams_url",
        "trees_url",
        "url",
        "clone_url",
        "default_branch",
        "forks",
        "forks_count",
        "git_url",
        "has_issues",
        "has_projects",
        "has_wiki",
        "has_pages",
        "homepage",
        "language",
        "archived",
        "disabled",
        "mirror_url",
        "open_issues",
        "open_issues_count",
        "license",
        "pushed_at",
        "size",
        "ssh_url",
        "stargazers_count",
        "svn_url",
        "watchers",
        "watchers_count",
        "created_at",
        "updated_at"
      ]
    }
  },
  "users": {
    "primary_response_schema": {
      "title": "Summary Stats",
      "description": "API Insights usage summary stats for an organization",
      "type": "object",
      "properties": {
        "total_request_count": {
          "description": "The total number of requests within the queried time period",
          "type": "integer",
          "format": "int64"
        },
        "rate_limited_request_count": {
          "description": "The total number of requests that were rate limited within the queried time period",
          "type": "integer",
          "format": "int64"
        }
      }
    }
  }
}
```

### ID format

Resource `issue` uses: alphabet=NUMERIC, length=2

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

Add a class `Issue(Base)` with:

- Table name: `github_issues`
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
"""ORM schema for the GitHub API replica.

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
"""Session-first CRUD operations for GitHub.

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
"""Serialization helpers for the GitHub API replica.

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
"""GitHub REST API routes.

Mounted under /api/env/{env_id}/services/github
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
