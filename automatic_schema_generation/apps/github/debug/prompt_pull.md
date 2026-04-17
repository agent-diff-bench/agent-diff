# Entity Implementation: pulls

You are implementing the **pulls** resource for the GitHub API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for pulls

```json
{
  "paths": {
    "/repos/{owner}/{repo}/commits/{commit_sha}/pulls": {
      "get": {
        "summary": "List pull requests associated with a commit",
        "description": "Lists the merged pull request that introduced the commit to the repository. If the commit is not present in the default branch, it will return merged and open pull requests associated with the commit.\n\nTo list the open or merged pull requests associated with a branch, you can set the `commit_sha` parameter to the branch name.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/list-pull-requests-associated-with-commit",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/commits/commits#list-pull-requests-associated-with-a-commit"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "$ref": "#/components/parameters/commit-sha"
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
                    "$ref": "#/components/schemas/pull-request-simple"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/pull-request-simple-items"
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
          "409": {
            "$ref": "#/components/responses/conflict"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "commits",
          "subcategory": "commits"
        }
      }
    },
    "/repos/{owner}/{repo}/pulls": {
      "get": {
        "summary": "List pull requests",
        "description": "Lists pull requests in a specified repository.\n\nDraft pull requests are available in public repositories with GitHub\nFree and GitHub Free for organizations, GitHub Pro, and legacy per-repository billing\nplans, and in public and private repositories with GitHub Team and GitHub Enterprise\nCloud. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products)\nin the GitHub Help documentation.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "pulls"
        ],
        "operationId": "pulls/list",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/pulls/pulls#list-pull-requests"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "name": "state",
            "description": "Either `open`, `closed`, or `all` to filter by state.",
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
            "name": "head",
            "description": "Filter pulls by head user or head organization and branch name in the format of `user:ref-name` or `organization:ref-name`. For example: `github:new-script-format` or `octocat:test-branch`.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "base",
            "description": "Filter pulls by base branch name. Example: `gh-pages`.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "sort",
            "description": "What to sort results by. `popularity` will sort by the number of comments. `long-running` will sort by date created and will limit the results to pull requests that have been open for more than a month and have had activity within the past month.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "created",
                "updated",
                "popularity",
                "long-running"
              ],
              "default": "created"
            }
          },
          {
            "name": "direction",
            "description": "The direction of the sort. Default: `desc` when sort is `created` or sort is not specified, otherwise `asc`.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "asc",
                "desc"
              ]
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
                    "$ref": "#/components/schemas/pull-request-simple"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/pull-request-simple-items"
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
          "304": {
            "$ref": "#/components/responses/not_modified"
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "pulls",
          "subcategory": "pulls"
        }
      },
      "post": {
        "summary": "Create a pull request",
        "description": "Draft pull requests are available in public repositories with GitHub Free and GitHub Free for organizations, GitHub Pro, and legacy per-repository billing plans, and in public and private repositories with GitHub Team and GitHub Enterprise Cloud. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nTo open or update a pull request in a public repository, you must have write access to the head or the source branch. For organization-owned repositories, you must be a member of the organization that owns the repository to open or update a pull request.\n\nThis endpoint triggers [notifications](https://docs.github.com/github/managing-subscriptions-and-notifications-on-github/about-notifications). Creating content too quickly using this endpoint may result in secondary rate limiting. For more information, see \"[Rate limits for the API](https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api#about-secondary-rate-limits)\" and \"[Best practices for using the REST API](https://docs.github.com/rest/guides/best-practices-for-using-the-rest-api).\"\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "pulls"
        ],
        "operationId": "pulls/create",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/pulls/pulls#create-a-pull-request"
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
                    "type": "string",
                    "description": "The title of the new pull request. Required unless `issue` is specified."
                  },
                  "head": {
                    "type": "string",
                    "description": "The name of the branch where your changes are implemented. For cross-repository pull requests in the same network, namespace `head` with a user like this: `username:branch`."
                  },
                  "head_repo": {
                    "type": "string",
                    "description": "The name of the repository where the changes in the pull request were made. This field is required for cross-repository pull requests if both repositories are owned by the same organization.",
                    "format": "repo.nwo",
                    "examples": [
                      "octo-org/octo-repo"
                    ]
                  },
                  "base": {
                    "type": "string",
                    "description": "The name of the branch you want the changes pulled into. This should be an existing branch on the current repository. You cannot submit a pull request to one repository that requests a merge to a base of another repository."
                  },
                  "body": {
                    "type": "string",
                    "description": "The contents of the pull request."
                  },
                  "maintainer_can_modify": {
                    "type": "boolean",
                    "description": "Indicates whether [maintainers can modify](https://docs.github.com/articles/allowing-changes-to-a-pull-request-branch-created-from-a-fork/) the pull request."
                  },
                  "draft": {
                    "type": "boolean",
                    "description": "Indicates whether the pull request is a draft. See \"[Draft Pull Requests](https://docs.github.com/articles/about-pull-requests#draft-pull-requests)\" in the GitHub Help documentation to learn more."
                  },
                  "issue": {
                    "type": "integer",
                    "format": "int64",
                    "description": "An issue in the repository to convert to a pull request. The issue title, body, and comments will become the title, body, and comments on the new pull request. Required unless `title` is specified.",
                    "examples": [
                      1
                    ]
                  }
                },
                "required": [
                  "head",
                  "base"
                ]
              },
              "examples": {
                "default": {
                  "value": {
                    "title": "Amazing new feature",
                    "body": "Please pull these awesome changes in!",
                    "head": "octocat:new-feature",
                    "base": "master"
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
                  "$ref": "#/components/schemas/pull-request"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/pull-request"
                  }
                }
              }
            },
            "headers": {
              "Location": {
                "example": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
                "schema": {
                  "type": "string"
                }
              }
            }
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "triggersNotification": true,
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "pulls",
          "subcategory": "pulls"
        }
      }
    },
    "/repos/{owner}/{repo}/pulls/{pull_number}": {
      "get": {
        "summary": "Get a pull request",
        "description": "Draft pull requests are available in public repositories with GitHub Free and GitHub Free for organizations, GitHub Pro, and legacy per-repository billing plans, and in public and private repositories with GitHub Team and GitHub Enterprise Cloud. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nLists details of a pull request by providing its number.\n\nWhen you get, [create](https://docs.github.com/rest/pulls/pulls/#create-a-pull-request), or [edit](https://docs.github.com/rest/pulls/pulls#update-a-pull-request) a pull request, GitHub creates a merge commit to test whether the pull request can be automatically merged into the base branch. This test commit is not added to the base branch or the head branch. You can review the status of the test commit using the `mergeable` key. For more information, see \"[Checking mergeability of pull requests](https://docs.github.com/rest/guides/getting-started-with-the-git-database-api#checking-mergeability-of-pull-requests)\".\n\nThe value of the `mergeable` attribute can be `true`, `false`, or `null`. If the value is `null`, then GitHub has started a background job to compute the mergeability. After giving the job time to complete, resubmit the request. When the job finishes, you will see a non-`null` value for the `mergeable` attribute in the response. If `mergeable` is `true`, then `merge_commit_sha` will be the SHA of the _test_ merge commit.\n\nThe value of the `merge_commit_sha` attribute changes depending on the state of the pull request. Before merging a pull request, the `merge_commit_sha` attribute holds the SHA of the _test_ merge commit. After merging a pull request, the `merge_commit_sha` attribute changes depending on how you merged the pull request:\n\n*   If merged as a [merge commit](https://docs.github.com/articles/about-merge-methods-on-github/), `merge_commit_sha` represents the SHA of the merge commit.\n*   If merged via a [squash](https://docs.github.com/articles/about-merge-methods-on-github/#squashing-your-merge-commits), `merge_commit_sha` represents the SHA of the squashed commit on the base branch.\n*   If [rebased](https://docs.github.com/articles/about-merge-methods-on-github/#rebasing-and-merging-your-commits), `merge_commit_sha` represents the commit that the base branch was updated to.\n\nPass the appropriate [media type](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types) to fetch diff and patch formats.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.\n- **`application/vnd.github.diff`**: For more information, see \"[git-diff](https://git-scm.com/docs/git-diff)\" in the Git documentation. If a diff is corrupt, contact us through the [GitHub Support portal](https://support.github.com/). Include the repository name and pull request ID in your message.",
        "tags": [
          "pulls"
        ],
        "operationId": "pulls/get",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/pulls/pulls#get-a-pull-request"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "$ref": "#/components/parameters/pull-number"
          }
        ],
        "responses": {
          "200": {
            "description": "Pass the appropriate [media type](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types) to fetch diff and patch formats.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/pull-request"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/pull-request"
                  }
                }
              }
            }
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "406": {
            "$ref": "#/components/responses/unacceptable"
          },
          "500": {
            "$ref": "#/components/responses/internal_error"
          },
          "503": {
            "$ref": "#/components/responses/service_unavailable"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "pulls",
          "subcategory": "pulls"
        }
      },
      "patch": {
        "summary": "Update a pull request",
        "description": "Draft pull requests are available in public repositories with GitHub Free and GitHub Free for organizations, GitHub Pro, and legacy per-repository billing plans, and in public and private repositories with GitHub Team and GitHub Enterprise Cloud. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nTo open or update a pull request in a public repository, you must have write access to the head or the source branch. For organization-owned repositories, you must be a member of the organization that owns the repository to open or update a pull request.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown body. Response will include `body`. This is the default if you do not pass any specific media type.\n- **`application/vnd.github.text+json`**: Returns a text only representation of the markdown body. Response will include `body_text`.\n- **`application/vnd.github.html+json`**: Returns HTML rendered from the body's markdown. Response will include `body_html`.\n- **`application/vnd.github.full+json`**: Returns raw, text, and HTML representations. Response will include `body`, `body_text`, and `body_html`.",
        "tags": [
          "pulls"
        ],
        "operationId": "pulls/update",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/pulls/pulls#update-a-pull-request"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "$ref": "#/components/parameters/pull-number"
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
                    "type": "string",
                    "description": "The title of the pull request."
                  },
                  "body": {
                    "type": "string",
                    "description": "The contents of the pull request."
                  },
                  "state": {
                    "type": "string",
                    "description": "State of this Pull Request. Either `open` or `closed`.",
                    "enum": [
                      "open",
                      "closed"
                    ]
                  },
                  "base": {
                    "type": "string",
                    "description": "The name of the branch you want your changes pulled into. This should be an existing branch on the current repository. You cannot update the base branch on a pull request to point to another repository."
                  },
                  "maintainer_can_modify": {
                    "type": "boolean",
                    "description": "Indicates whether [maintainers can modify](https://docs.github.com/articles/allowing-changes-to-a-pull-request-branch-created-from-a-fork/) the pull request."
                  }
                }
              },
              "examples": {
                "default": {
                  "value": {
                    "title": "new title",
                    "body": "updated body",
                    "state": "open",
                    "base": "master"
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
                  "$ref": "#/components/schemas/pull-request"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/pull-request"
                  }
                }
              }
            }
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "pulls",
          "subcategory": "pulls"
        }
      }
    }
  },
  "schemas": {
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
    "team": {
      "title": "Team",
      "description": "Groups of organization members that gives permissions on specified repositories.",
      "type": "object",
      "properties": {
        "id": {
          "type": "integer"
        },
        "node_id": {
          "type": "string"
        },
        "name": {
          "type": "string"
        },
        "slug": {
          "type": "string"
        },
        "description": {
          "type": [
            "string",
            "null"
          ]
        },
        "privacy": {
          "type": "string"
        },
        "notification_setting": {
          "type": "string"
        },
        "permission": {
          "type": "string"
        },
        "permissions": {
          "type": "object",
          "properties": {
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
            },
            "admin": {
              "type": "boolean"
            }
          },
          "required": [
            "pull",
            "triage",
            "push",
            "maintain",
            "admin"
          ]
        },
        "url": {
          "type": "string",
          "format": "uri"
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/orgs/rails/teams/core"
          ]
        },
        "members_url": {
          "type": "string"
        },
        "repositories_url": {
          "type": "string",
          "format": "uri"
        },
        "type": {
          "description": "The ownership type of the team",
          "type": "string",
          "enum": [
            "enterprise",
            "organization"
          ]
        },
        "organization_id": {
          "type": "integer",
          "description": "Unique identifier of the organization to which this team belongs",
          "examples": [
            37
          ]
        },
        "enterprise_id": {
          "type": "integer",
          "description": "Unique identifier of the enterprise to which this team belongs",
          "examples": [
            42
          ]
        },
        "parent": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/team-simple"
            }
          ]
        }
      },
      "required": [
        "id",
        "node_id",
        "url",
        "members_url",
        "name",
        "description",
        "permission",
        "html_url",
        "repositories_url",
        "slug",
        "parent",
        "type"
      ]
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
    "auto-merge": {
      "title": "Auto merge",
      "description": "The status of auto merging a pull request.",
      "type": [
        "object",
        "null"
      ],
      "properties": {
        "enabled_by": {
          "$ref": "#/components/schemas/simple-user"
        },
        "merge_method": {
          "type": "string",
          "description": "The merge method to use.",
          "enum": [
            "merge",
            "squash",
            "rebase"
          ]
        },
        "commit_title": {
          "type": "string",
          "description": "Title for the merge commit message."
        },
        "commit_message": {
          "type": "string",
          "description": "Commit message for the merge commit."
        }
      },
      "required": [
        "enabled_by",
        "merge_method",
        "commit_title",
        "commit_message"
      ]
    },
    "team-simple": {
      "title": "Team Simple",
      "description": "Groups of organization members that gives permissions on specified repositories.",
      "type": "object",
      "properties": {
        "id": {
          "description": "Unique identifier of the team",
          "type": "integer",
          "examples": [
            1
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDQ6VGVhbTE="
          ]
        },
        "url": {
          "description": "URL for the team",
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/organizations/1/team/1"
          ]
        },
        "members_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/organizations/1/team/1/members{/member}"
          ]
        },
        "name": {
          "description": "Name of the team",
          "type": "string",
          "examples": [
            "Justice League"
          ]
        },
        "description": {
          "description": "Description of the team",
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "A great team."
          ]
        },
        "permission": {
          "description": "Permission that the team will have for its repositories",
          "type": "string",
          "examples": [
            "admin"
          ]
        },
        "privacy": {
          "description": "The level of privacy this team should have",
          "type": "string",
          "examples": [
            "closed"
          ]
        },
        "notification_setting": {
          "description": "The notification setting the team has set",
          "type": "string",
          "examples": [
            "notifications_enabled"
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/orgs/rails/teams/core"
          ]
        },
        "repositories_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/organizations/1/team/1/repos"
          ]
        },
        "slug": {
          "type": "string",
          "examples": [
            "justice-league"
          ]
        },
        "ldap_dn": {
          "description": "Distinguished Name (DN) that team maps to within LDAP environment",
          "type": "string",
          "examples": [
            "uid=example,ou=users,dc=github,dc=com"
          ]
        },
        "type": {
          "description": "The ownership type of the team",
          "type": "string",
          "enum": [
            "enterprise",
            "organization"
          ]
        },
        "organization_id": {
          "type": "integer",
          "description": "Unique identifier of the organization to which this team belongs",
          "examples": [
            37
          ]
        },
        "enterprise_id": {
          "type": "integer",
          "description": "Unique identifier of the enterprise to which this team belongs",
          "examples": [
            42
          ]
        }
      },
      "required": [
        "id",
        "node_id",
        "url",
        "members_url",
        "name",
        "description",
        "permission",
        "html_url",
        "repositories_url",
        "slug",
        "type"
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
    "pull-request-simple": {
      "title": "Pull Request Simple",
      "description": "Pull Request Simple",
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/pulls/1347"
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
            "MDExOlB1bGxSZXF1ZXN0MQ=="
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat/Hello-World/pull/1347"
          ]
        },
        "diff_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat/Hello-World/pull/1347.diff"
          ]
        },
        "patch_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat/Hello-World/pull/1347.patch"
          ]
        },
        "issue_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/issues/1347"
          ]
        },
        "commits_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits"
          ]
        },
        "review_comments_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments"
          ]
        },
        "review_comment_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}"
          ]
        },
        "comments_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments"
          ]
        },
        "statuses_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e"
          ]
        },
        "number": {
          "type": "integer",
          "examples": [
            1347
          ]
        },
        "state": {
          "type": "string",
          "examples": [
            "open"
          ]
        },
        "locked": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "title": {
          "type": "string",
          "examples": [
            "new-feature"
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
        "body": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "Please pull these awesome changes"
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
              "description": {
                "type": "string"
              },
              "color": {
                "type": "string"
              },
              "default": {
                "type": "boolean"
              }
            },
            "required": [
              "id",
              "node_id",
              "url",
              "name",
              "description",
              "color",
              "default"
            ]
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
        "active_lock_reason": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "too heated"
          ]
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "closed_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "merged_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "assignees": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "requested_reviewers": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "requested_teams": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/team"
          }
        },
        "head": {
          "type": "object",
          "properties": {
            "label": {
              "type": "string"
            },
            "ref": {
              "type": "string"
            },
            "repo": {
              "$ref": "#/components/schemas/repository"
            },
            "sha": {
              "type": "string"
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
            }
          },
          "required": [
            "label",
            "ref",
            "repo",
            "sha",
            "user"
          ]
        },
        "base": {
          "type": "object",
          "properties": {
            "label": {
              "type": "string"
            },
            "ref": {
              "type": "string"
            },
            "repo": {
              "$ref": "#/components/schemas/repository"
            },
            "sha": {
              "type": "string"
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
            }
          },
          "required": [
            "label",
            "ref",
            "repo",
            "sha",
            "user"
          ]
        },
        "_links": {
          "type": "object",
          "properties": {
            "comments": {
              "$ref": "#/components/schemas/link"
            },
            "commits": {
              "$ref": "#/components/schemas/link"
            },
            "statuses": {
              "$ref": "#/components/schemas/link"
            },
            "html": {
              "$ref": "#/components/schemas/link"
            },
            "issue": {
              "$ref": "#/components/schemas/link"
            },
            "review_comments": {
              "$ref": "#/components/schemas/link"
            },
            "review_comment": {
              "$ref": "#/components/schemas/link"
            },
            "self": {
              "$ref": "#/components/schemas/link"
            }
          },
          "required": [
            "comments",
            "commits",
            "statuses",
            "html",
            "issue",
            "review_comments",
            "review_comment",
            "self"
          ]
        },
        "author_association": {
          "$ref": "#/components/schemas/author-association"
        },
        "auto_merge": {
          "$ref": "#/components/schemas/auto-merge"
        },
        "draft": {
          "description": "Indicates whether or not the pull request is a draft.",
          "type": "boolean",
          "examples": [
            false
          ]
        }
      },
      "required": [
        "_links",
        "labels",
        "base",
        "body",
        "closed_at",
        "comments_url",
        "commits_url",
        "created_at",
        "diff_url",
        "head",
        "html_url",
        "id",
        "node_id",
        "issue_url",
        "merged_at",
        "milestone",
        "number",
        "patch_url",
        "review_comment_url",
        "review_comments_url",
        "statuses_url",
        "state",
        "locked",
        "title",
        "updated_at",
        "url",
        "user",
        "author_association",
        "auto_merge"
      ]
    },
    "link": {
      "title": "Link",
      "description": "Hypermedia Link",
      "type": "object",
      "properties": {
        "href": {
          "type": "string"
        }
      },
      "required": [
        "href"
      ]
    },
    "pull-request": {
      "type": "object",
      "title": "Pull Request",
      "description": "Pull requests let you tell others about changes you've pushed to a repository on GitHub. Once a pull request is sent, interested parties can review the set of changes, discuss potential modifications, and even push follow-up commits if necessary.",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/pulls/1347"
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
            "MDExOlB1bGxSZXF1ZXN0MQ=="
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat/Hello-World/pull/1347"
          ]
        },
        "diff_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat/Hello-World/pull/1347.diff"
          ]
        },
        "patch_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat/Hello-World/pull/1347.patch"
          ]
        },
        "issue_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/issues/1347"
          ]
        },
        "commits_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits"
          ]
        },
        "review_comments_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments"
          ]
        },
        "review_comment_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}"
          ]
        },
        "comments_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments"
          ]
        },
        "statuses_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e"
          ]
        },
        "number": {
          "description": "Number uniquely identifying the pull request within its repository.",
          "type": "integer",
          "examples": [
            42
          ]
        },
        "state": {
          "description": "State of this Pull Request. Either `open` or `closed`.",
          "enum": [
            "open",
            "closed"
          ],
          "type": "string",
          "examples": [
            "open"
          ]
        },
        "locked": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "title": {
          "description": "The title of the pull request.",
          "type": "string",
          "examples": [
            "Amazing new feature"
          ]
        },
        "user": {
          "$ref": "#/components/schemas/simple-user"
        },
        "body": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "Please pull these awesome changes"
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
              "description": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "color": {
                "type": "string"
              },
              "default": {
                "type": "boolean"
              }
            },
            "required": [
              "id",
              "node_id",
              "url",
              "name",
              "description",
              "color",
              "default"
            ]
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
        "active_lock_reason": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "too heated"
          ]
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "closed_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "merged_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time",
          "examples": [
            "2011-01-26T19:01:12Z"
          ]
        },
        "assignees": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "requested_reviewers": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "requested_teams": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/team-simple"
          }
        },
        "head": {
          "type": "object",
          "properties": {
            "label": {
              "type": "string"
            },
            "ref": {
              "type": "string"
            },
            "repo": {
              "$ref": "#/components/schemas/repository"
            },
            "sha": {
              "type": "string"
            },
            "user": {
              "$ref": "#/components/schemas/simple-user"
            }
          },
          "required": [
            "label",
            "ref",
            "repo",
            "sha",
            "user"
          ]
        },
        "base": {
          "type": "object",
          "properties": {
            "label": {
              "type": "string"
            },
            "ref": {
              "type": "string"
            },
            "repo": {
              "$ref": "#/components/schemas/repository"
            },
            "sha": {
              "type": "string"
            },
            "user": {
              "$ref": "#/components/schemas/simple-user"
            }
          },
          "required": [
            "label",
            "ref",
            "repo",
            "sha",
            "user"
          ]
        },
        "_links": {
          "type": "object",
          "properties": {
            "comments": {
              "$ref": "#/components/schemas/link"
            },
            "commits": {
              "$ref": "#/components/schemas/link"
            },
            "statuses": {
              "$ref": "#/components/schemas/link"
            },
            "html": {
              "$ref": "#/components/schemas/link"
            },
            "issue": {
              "$ref": "#/components/schemas/link"
            },
            "review_comments": {
              "$ref": "#/components/schemas/link"
            },
            "review_comment": {
              "$ref": "#/components/schemas/link"
            },
            "self": {
              "$ref": "#/components/schemas/link"
            }
          },
          "required": [
            "comments",
            "commits",
            "statuses",
            "html",
            "issue",
            "review_comments",
            "review_comment",
            "self"
          ]
        },
        "author_association": {
          "$ref": "#/components/schemas/author-association"
        },
        "auto_merge": {
          "$ref": "#/components/schemas/auto-merge"
        },
        "draft": {
          "description": "Indicates whether or not the pull request is a draft.",
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "merged": {
          "type": "boolean"
        },
        "mergeable": {
          "type": [
            "boolean",
            "null"
          ],
          "examples": [
            true
          ]
        },
        "rebaseable": {
          "type": [
            "boolean",
            "null"
          ],
          "examples": [
            true
          ]
        },
        "mergeable_state": {
          "type": "string",
          "examples": [
            "clean"
          ]
        },
        "merged_by": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/simple-user"
            }
          ]
        },
        "comments": {
          "type": "integer",
          "examples": [
            10
          ]
        },
        "review_comments": {
          "type": "integer",
          "examples": [
            0
          ]
        },
        "maintainer_can_modify": {
          "description": "Indicates whether maintainers can modify the pull request.",
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "commits": {
          "type": "integer",
          "examples": [
            3
          ]
        },
        "additions": {
          "type": "integer",
          "examples": [
            100
          ]
        },
        "deletions": {
          "type": "integer",
          "examples": [
            3
          ]
        },
        "changed_files": {
          "type": "integer",
          "examples": [
            5
          ]
        }
      },
      "required": [
        "_links",
        "labels",
        "base",
        "body",
        "closed_at",
        "comments_url",
        "commits_url",
        "created_at",
        "diff_url",
        "head",
        "html_url",
        "id",
        "node_id",
        "issue_url",
        "merged_at",
        "milestone",
        "number",
        "patch_url",
        "review_comment_url",
        "review_comments_url",
        "statuses_url",
        "state",
        "locked",
        "title",
        "updated_at",
        "url",
        "user",
        "author_association",
        "auto_merge",
        "additions",
        "changed_files",
        "comments",
        "commits",
        "deletions",
        "mergeable",
        "mergeable_state",
        "merged",
        "maintainer_can_modify",
        "merged_by",
        "review_comments"
      ]
    }
  },
  "primary_response_schema": {
    "type": "object",
    "title": "Pull Request",
    "description": "Pull requests let you tell others about changes you've pushed to a repository on GitHub. Once a pull request is sent, interested parties can review the set of changes, discuss potential modifications, and even push follow-up commits if necessary.",
    "properties": {
      "url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/repos/octocat/Hello-World/pulls/1347"
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
          "MDExOlB1bGxSZXF1ZXN0MQ=="
        ]
      },
      "html_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://github.com/octocat/Hello-World/pull/1347"
        ]
      },
      "diff_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://github.com/octocat/Hello-World/pull/1347.diff"
        ]
      },
      "patch_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://github.com/octocat/Hello-World/pull/1347.patch"
        ]
      },
      "issue_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/repos/octocat/Hello-World/issues/1347"
        ]
      },
      "commits_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/repos/octocat/Hello-World/pulls/1347/commits"
        ]
      },
      "review_comments_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/repos/octocat/Hello-World/pulls/1347/comments"
        ]
      },
      "review_comment_url": {
        "type": "string",
        "examples": [
          "https://api.github.com/repos/octocat/Hello-World/pulls/comments{/number}"
        ]
      },
      "comments_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments"
        ]
      },
      "statuses_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/repos/octocat/Hello-World/statuses/6dcb09b5b57875f334f61aebed695e2e4193db5e"
        ]
      },
      "number": {
        "description": "Number uniquely identifying the pull request within its repository.",
        "type": "integer",
        "examples": [
          42
        ]
      },
      "state": {
        "description": "State of this Pull Request. Either `open` or `closed`.",
        "enum": [
          "open",
          "closed"
        ],
        "type": "string",
        "examples": [
          "open"
        ]
      },
      "locked": {
        "type": "boolean",
        "examples": [
          true
        ]
      },
      "title": {
        "description": "The title of the pull request.",
        "type": "string",
        "examples": [
          "Amazing new feature"
        ]
      },
      "user": {
        "$ref": "#/components/schemas/simple-user"
      },
      "body": {
        "type": [
          "string",
          "null"
        ],
        "examples": [
          "Please pull these awesome changes"
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
            "description": {
              "type": [
                "string",
                "null"
              ]
            },
            "color": {
              "type": "string"
            },
            "default": {
              "type": "boolean"
            }
          },
          "required": [
            "id",
            "node_id",
            "url",
            "name",
            "description",
            "color",
            "default"
          ]
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
      "active_lock_reason": {
        "type": [
          "string",
          "null"
        ],
        "examples": [
          "too heated"
        ]
      },
      "created_at": {
        "type": "string",
        "format": "date-time",
        "examples": [
          "2011-01-26T19:01:12Z"
        ]
      },
      "updated_at": {
        "type": "string",
        "format": "date-time",
        "examples": [
          "2011-01-26T19:01:12Z"
        ]
      },
      "closed_at": {
        "type": [
          "string",
          "null"
        ],
        "format": "date-time",
        "examples": [
          "2011-01-26T19:01:12Z"
        ]
      },
      "merged_at": {
        "type": [
          "string",
          "null"
        ],
        "format": "date-time",
        "examples": [
          "2011-01-26T19:01:12Z"
        ]
      },
      "assignees": {
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/simple-user"
        }
      },
      "requested_reviewers": {
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/simple-user"
        }
      },
      "requested_teams": {
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/team-simple"
        }
      },
      "head": {
        "type": "object",
        "properties": {
          "label": {
            "type": "string"
          },
          "ref": {
            "type": "string"
          },
          "repo": {
            "$ref": "#/components/schemas/repository"
          },
          "sha": {
            "type": "string"
          },
          "user": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "required": [
          "label",
          "ref",
          "repo",
          "sha",
          "user"
        ]
      },
      "base": {
        "type": "object",
        "properties": {
          "label": {
            "type": "string"
          },
          "ref": {
            "type": "string"
          },
          "repo": {
            "$ref": "#/components/schemas/repository"
          },
          "sha": {
            "type": "string"
          },
          "user": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "required": [
          "label",
          "ref",
          "repo",
          "sha",
          "user"
        ]
      },
      "_links": {
        "type": "object",
        "properties": {
          "comments": {
            "$ref": "#/components/schemas/link"
          },
          "commits": {
            "$ref": "#/components/schemas/link"
          },
          "statuses": {
            "$ref": "#/components/schemas/link"
          },
          "html": {
            "$ref": "#/components/schemas/link"
          },
          "issue": {
            "$ref": "#/components/schemas/link"
          },
          "review_comments": {
            "$ref": "#/components/schemas/link"
          },
          "review_comment": {
            "$ref": "#/components/schemas/link"
          },
          "self": {
            "$ref": "#/components/schemas/link"
          }
        },
        "required": [
          "comments",
          "commits",
          "statuses",
          "html",
          "issue",
          "review_comments",
          "review_comment",
          "self"
        ]
      },
      "author_association": {
        "$ref": "#/components/schemas/author-association"
      },
      "auto_merge": {
        "$ref": "#/components/schemas/auto-merge"
      },
      "draft": {
        "description": "Indicates whether or not the pull request is a draft.",
        "type": "boolean",
        "examples": [
          false
        ]
      },
      "merged": {
        "type": "boolean"
      },
      "mergeable": {
        "type": [
          "boolean",
          "null"
        ],
        "examples": [
          true
        ]
      },
      "rebaseable": {
        "type": [
          "boolean",
          "null"
        ],
        "examples": [
          true
        ]
      },
      "mergeable_state": {
        "type": "string",
        "examples": [
          "clean"
        ]
      },
      "merged_by": {
        "anyOf": [
          {
            "type": "null"
          },
          {
            "$ref": "#/components/schemas/simple-user"
          }
        ]
      },
      "comments": {
        "type": "integer",
        "examples": [
          10
        ]
      },
      "review_comments": {
        "type": "integer",
        "examples": [
          0
        ]
      },
      "maintainer_can_modify": {
        "description": "Indicates whether maintainers can modify the pull request.",
        "type": "boolean",
        "examples": [
          true
        ]
      },
      "commits": {
        "type": "integer",
        "examples": [
          3
        ]
      },
      "additions": {
        "type": "integer",
        "examples": [
          100
        ]
      },
      "deletions": {
        "type": "integer",
        "examples": [
          3
        ]
      },
      "changed_files": {
        "type": "integer",
        "examples": [
          5
        ]
      }
    },
    "required": [
      "_links",
      "labels",
      "base",
      "body",
      "closed_at",
      "comments_url",
      "commits_url",
      "created_at",
      "diff_url",
      "head",
      "html_url",
      "id",
      "node_id",
      "issue_url",
      "merged_at",
      "milestone",
      "number",
      "patch_url",
      "review_comment_url",
      "review_comments_url",
      "statuses_url",
      "state",
      "locked",
      "title",
      "updated_at",
      "url",
      "user",
      "author_association",
      "auto_merge",
      "additions",
      "changed_files",
      "comments",
      "commits",
      "deletions",
      "mergeable",
      "mergeable_state",
      "merged",
      "maintainer_can_modify",
      "merged_by",
      "review_comments"
    ]
  }
}
```

### Relationship manifest

```yaml
github_pulls:
  user_id:
    target_table: github_users
    target_column: id
    confidence: high
    reason: 'response schema: user.id'
  organization_id:
    target_table: github_orgs
    target_column: id
    confidence: high
    reason: 'response schema: requested_teams[].organization_id'
  repo_id:
    target_table: github_repos
    target_column: id
    confidence: high
    reason: 'response schema: head.repo.id'

```

### FK dependency schemas (for stub creation if needed)

```json
{
  "orgs": {
    "primary_response_schema": {
      "title": "Organization Full",
      "description": "Organization Full",
      "type": "object",
      "properties": {
        "login": {
          "type": "string",
          "examples": [
            "github"
          ]
        },
        "id": {
          "type": "integer",
          "examples": [
            1
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDEyOk9yZ2FuaXphdGlvbjE="
          ]
        },
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/orgs/github"
          ]
        },
        "repos_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/orgs/github/repos"
          ]
        },
        "events_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/orgs/github/events"
          ]
        },
        "hooks_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/orgs/github/hooks"
          ]
        },
        "issues_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/orgs/github/issues"
          ]
        },
        "members_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/orgs/github/members{/member}"
          ]
        },
        "public_members_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/orgs/github/public_members{/member}"
          ]
        },
        "avatar_url": {
          "type": "string",
          "examples": [
            "https://github.com/images/error/octocat_happy.gif"
          ]
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "A great organization"
          ]
        },
        "name": {
          "type": "string",
          "examples": [
            "github"
          ]
        },
        "company": {
          "type": "string",
          "examples": [
            "GitHub"
          ]
        },
        "blog": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/blog"
          ]
        },
        "location": {
          "type": "string",
          "examples": [
            "San Francisco"
          ]
        },
        "email": {
          "type": "string",
          "format": "email",
          "examples": [
            "octocat@github.com"
          ]
        },
        "twitter_username": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "github"
          ]
        },
        "is_verified": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_organization_projects": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_repository_projects": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "public_repos": {
          "type": "integer",
          "examples": [
            2
          ]
        },
        "public_gists": {
          "type": "integer",
          "examples": [
            1
          ]
        },
        "followers": {
          "type": "integer",
          "examples": [
            20
          ]
        },
        "following": {
          "type": "integer",
          "examples": [
            0
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat"
          ]
        },
        "type": {
          "type": "string",
          "examples": [
            "Organization"
          ]
        },
        "total_private_repos": {
          "type": "integer",
          "examples": [
            100
          ]
        },
        "owned_private_repos": {
          "type": "integer",
          "examples": [
            100
          ]
        },
        "private_gists": {
          "type": [
            "integer",
            "null"
          ],
          "examples": [
            81
          ]
        },
        "disk_usage": {
          "type": [
            "integer",
            "null"
          ],
          "examples": [
            10000
          ]
        },
        "collaborators": {
          "type": [
            "integer",
            "null"
          ],
          "description": "The number of collaborators on private repositories.\n\nThis field may be null if the number of private repositories is over 50,000.",
          "examples": [
            8
          ]
        },
        "billing_email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email",
          "examples": [
            "org@example.com"
          ]
        },
        "plan": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "space": {
              "type": "integer"
            },
            "private_repos": {
              "type": "integer"
            },
            "filled_seats": {
              "type": "integer"
            },
            "seats": {
              "type": "integer"
            }
          },
          "required": [
            "name",
            "space",
            "private_repos"
          ]
        },
        "default_repository_permission": {
          "type": [
            "string",
            "null"
          ]
        },
        "default_repository_branch": {
          "type": [
            "string",
            "null"
          ],
          "description": "The default branch for repositories created in this organization.",
          "examples": [
            "main"
          ]
        },
        "members_can_create_repositories": {
          "type": [
            "boolean",
            "null"
          ],
          "examples": [
            true
          ]
        },
        "two_factor_requirement_enabled": {
          "type": [
            "boolean",
            "null"
          ],
          "examples": [
            true
          ]
        },
        "members_allowed_repository_creation_type": {
          "type": "string",
          "examples": [
            "all"
          ]
        },
        "members_can_create_public_repositories": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_create_private_repositories": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_create_internal_repositories": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_create_pages": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_create_public_pages": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_create_private_pages": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_delete_repositories": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_change_repo_visibility": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_invite_outside_collaborators": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_delete_issues": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "display_commenter_full_name_setting_enabled": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "readers_can_create_discussions": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_create_teams": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_view_dependency_insights": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "members_can_fork_private_repositories": {
          "type": [
            "boolean",
            "null"
          ],
          "examples": [
            false
          ]
        },
        "web_commit_signoff_required": {
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "advanced_security_enabled_for_new_repositories": {
          "type": "boolean",
          "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether GitHub Advanced Security is enabled for new repositories and repositories transferred to this organization.\n\nThis field is only visible to organization owners or members of a team with the security manager role.",
          "examples": [
            false
          ],
          "deprecated": true
        },
        "dependabot_alerts_enabled_for_new_repositories": {
          "type": "boolean",
          "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether Dependabot alerts are automatically enabled for new repositories and repositories transferred to this organization.\n\nThis field is only visible to organization owners or members of a team with the security manager role.",
          "examples": [
            false
          ],
          "deprecated": true
        },
        "dependabot_security_updates_enabled_for_new_repositories": {
          "type": "boolean",
          "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether Dependabot security updates are automatically enabled for new repositories and repositories transferred to this organization.\n\nThis field is only visible to organization owners or members of a team with the security manager role.",
          "examples": [
            false
          ],
          "deprecated": true
        },
        "dependency_graph_enabled_for_new_repositories": {
          "type": "boolean",
          "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether dependency graph is automatically enabled for new repositories and repositories transferred to this organization.\n\nThis field is only visible to organization owners or members of a team with the security manager role.",
          "examples": [
            false
          ],
          "deprecated": true
        },
        "secret_scanning_enabled_for_new_repositories": {
          "type": "boolean",
          "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether secret scanning is automatically enabled for new repositories and repositories transferred to this organization.\n\nThis field is only visible to organization owners or members of a team with the security manager role.",
          "examples": [
            false
          ],
          "deprecated": true
        },
        "secret_scanning_push_protection_enabled_for_new_repositories": {
          "type": "boolean",
          "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether secret scanning push protection is automatically enabled for new repositories and repositories transferred to this organization.\n\nThis field is only visible to organization owners or members of a team with the security manager role.",
          "examples": [
            false
          ],
          "deprecated": true
        },
        "secret_scanning_push_protection_custom_link": {
          "type": [
            "string",
            "null"
          ],
          "description": "An optional URL string to display to contributors who are blocked from pushing a secret.",
          "examples": [
            "https://github.com/test-org/test-repo/blob/main/README.md"
          ]
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2008-01-14T04:33:35Z"
          ]
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        },
        "archived_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time"
        },
        "deploy_keys_enabled_for_repositories": {
          "type": "boolean",
          "description": "Controls whether or not deploy keys may be added and used for repositories in the organization.",
          "examples": [
            false
          ]
        }
      },
      "required": [
        "login",
        "url",
        "id",
        "node_id",
        "repos_url",
        "events_url",
        "hooks_url",
        "issues_url",
        "members_url",
        "public_members_url",
        "avatar_url",
        "description",
        "html_url",
        "has_organization_projects",
        "has_repository_projects",
        "public_repos",
        "public_gists",
        "followers",
        "following",
        "type",
        "created_at",
        "updated_at",
        "archived_at"
      ]
    }
  },
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

Resource `pull` uses: alphabet=NUMERIC, length=1

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

Add a class `Pull(Base)` with:

- Table name: `github_pulls`
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
