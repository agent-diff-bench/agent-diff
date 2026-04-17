# Entity Implementation: users

You are implementing the **users** resource for the GitHub API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for users

```json
{
  "paths": {
    "/orgs/{org}/insights/api/summary-stats/users/{user_id}": {
      "get": {
        "summary": "Get summary stats by user",
        "description": "Get overall statistics of API requests within the organization for a user.",
        "tags": [
          "orgs"
        ],
        "operationId": "api-insights/get-summary-stats-by-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/api-insights#get-summary-stats-by-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/api-insights-user-id"
          },
          {
            "$ref": "#/components/parameters/api-insights-min-timestamp"
          },
          {
            "$ref": "#/components/parameters/api-insights-max-timestamp"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/api-insights-summary-stats"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/api-insights-summary-stats"
                  }
                }
              }
            }
          }
        },
        "x-github": {
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "api-insights"
        }
      }
    },
    "/orgs/{org}/insights/api/time-stats/users/{user_id}": {
      "get": {
        "summary": "Get time stats by user",
        "description": "Get the number of API requests and rate-limited requests made within an organization by a specific user over a specified time period.",
        "tags": [
          "orgs"
        ],
        "operationId": "api-insights/get-time-stats-by-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/api-insights#get-time-stats-by-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/api-insights-user-id"
          },
          {
            "$ref": "#/components/parameters/api-insights-min-timestamp"
          },
          {
            "$ref": "#/components/parameters/api-insights-max-timestamp"
          },
          {
            "$ref": "#/components/parameters/api-insights-timestamp-increment"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/api-insights-time-stats"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/api-insights-time-stats"
                  }
                }
              }
            }
          }
        },
        "x-github": {
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "api-insights"
        }
      }
    },
    "/orgs/{org}/organization-roles/users/{username}": {
      "delete": {
        "summary": "Remove all organization roles for a user",
        "description": "Revokes all assigned organization roles from a user. For more information on organization roles, see \"[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles).\"\n\nThe authenticated user must be an administrator for the organization to use this endpoint.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/revoke-all-org-roles-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/organization-roles#remove-all-organization-roles-for-a-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/username"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "organization-roles"
        }
      }
    },
    "/orgs/{org}/organization-roles/users/{username}/{role_id}": {
      "put": {
        "summary": "Assign an organization role to a user",
        "description": "Assigns an organization role to a member of an organization. For more information on organization roles, see \"[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles).\"\n\nThe authenticated user must be an administrator for the organization to use this endpoint.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/assign-user-to-org-role",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/organization-roles#assign-an-organization-role-to-a-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/username"
          },
          {
            "$ref": "#/components/parameters/role-id"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
          },
          "404": {
            "description": "Response if the organization, user or role does not exist."
          },
          "422": {
            "description": "Response if the organization roles feature is not enabled enabled for the organization, the validation failed, or the user is not an organization member."
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "organization-roles"
        }
      },
      "delete": {
        "summary": "Remove an organization role from a user",
        "description": "Remove an organization role from a user. For more information on organization roles, see \"[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles).\"\n\nThe authenticated user must be an administrator for the organization to use this endpoint.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/revoke-org-role-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/organization-roles#remove-an-organization-role-from-a-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/username"
          },
          {
            "$ref": "#/components/parameters/role-id"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "organization-roles"
        }
      }
    },
    "/orgs/{org}/organization-roles/{role_id}/users": {
      "get": {
        "summary": "List users that are assigned to an organization role",
        "description": "Lists organization members that are assigned to an organization role. For more information on organization roles, see \"[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles).\"\n\nTo use this endpoint, you must be an administrator for the organization.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/list-org-role-users",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/organization-roles#list-users-that-are-assigned-to-an-organization-role"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/role-id"
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
            "description": "Response - List of assigned users",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "description": "List of users assigned to the organization role",
                  "items": {
                    "$ref": "#/components/schemas/user-role-assignment"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/simple-user-items"
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
            "description": "Response if the organization or role does not exist."
          },
          "422": {
            "description": "Response if the organization roles feature is not enabled or validation failed."
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "organization-roles"
        }
      }
    },
    "/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users": {
      "get": {
        "summary": "Get users with access to the protected branch",
        "description": "Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nLists the people who have push access to this branch.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/get-users-with-access-to-protected-branch",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/branches/branch-protection#get-users-with-access-to-the-protected-branch"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "$ref": "#/components/parameters/branch"
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
                    "$ref": "#/components/schemas/simple-user"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/simple-user-items"
                  }
                }
              }
            }
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "branches",
          "subcategory": "branch-protection"
        }
      },
      "post": {
        "summary": "Add user access restrictions",
        "description": "Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nGrants the specified people push access for this branch.\n\n| Type    | Description                                                                                                                   |\n| ------- | ----------------------------------------------------------------------------------------------------------------------------- |\n| `array` | Usernames for people who can have push access. **Note**: The list of users, apps, and teams in total is limited to 100 items. |",
        "tags": [
          "repos"
        ],
        "operationId": "repos/add-user-access-restrictions",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/branches/branch-protection#add-user-access-restrictions"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "$ref": "#/components/parameters/branch"
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "users": {
                    "type": "array",
                    "description": "The username for users",
                    "items": {
                      "type": "string"
                    }
                  }
                },
                "required": [
                  "users"
                ],
                "example": {
                  "users": [
                    "mona"
                  ]
                }
              },
              "examples": {
                "default": {
                  "summary": "Example adding a user in a branch protection rule",
                  "value": {
                    "users": [
                      "octocat"
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
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/simple-user"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/simple-user-items"
                  }
                }
              }
            }
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "requestBodyParameterName": "users",
          "category": "branches",
          "subcategory": "branch-protection"
        }
      },
      "put": {
        "summary": "Set user access restrictions",
        "description": "Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nReplaces the list of people that have push access to this branch. This removes all people that previously had push access and grants push access to the new list of people.\n\n| Type    | Description                                                                                                                   |\n| ------- | ----------------------------------------------------------------------------------------------------------------------------- |\n| `array` | Usernames for people who can have push access. **Note**: The list of users, apps, and teams in total is limited to 100 items. |",
        "tags": [
          "repos"
        ],
        "operationId": "repos/set-user-access-restrictions",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/branches/branch-protection#set-user-access-restrictions"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "$ref": "#/components/parameters/branch"
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "users": {
                    "type": "array",
                    "description": "The username for users",
                    "items": {
                      "type": "string"
                    }
                  }
                },
                "required": [
                  "users"
                ],
                "example": {
                  "users": [
                    "mona"
                  ]
                }
              },
              "examples": {
                "default": {
                  "summary": "Example replacing a user in a branch protection rule",
                  "value": {
                    "users": [
                      "octocat"
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
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/simple-user"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/simple-user-items"
                  }
                }
              }
            }
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "requestBodyParameterName": "users",
          "category": "branches",
          "subcategory": "branch-protection"
        }
      },
      "delete": {
        "summary": "Remove user access restrictions",
        "description": "Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nRemoves the ability of a user to push to this branch.\n\n| Type    | Description                                                                                                                                   |\n| ------- | --------------------------------------------------------------------------------------------------------------------------------------------- |\n| `array` | Usernames of the people who should no longer have push access. **Note**: The list of users, apps, and teams in total is limited to 100 items. |",
        "tags": [
          "repos"
        ],
        "operationId": "repos/remove-user-access-restrictions",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/branches/branch-protection#remove-user-access-restrictions"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          },
          {
            "$ref": "#/components/parameters/branch"
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "users": {
                    "type": "array",
                    "description": "The username for users",
                    "items": {
                      "type": "string"
                    }
                  }
                },
                "required": [
                  "users"
                ],
                "example": {
                  "users": [
                    "mona"
                  ]
                }
              },
              "examples": {
                "default": {
                  "summary": "Example removing a user in a branch protection rule",
                  "value": {
                    "users": [
                      "octocat"
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
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/simple-user"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/simple-user-items"
                  }
                }
              }
            }
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "requestBodyParameterName": "users",
          "category": "branches",
          "subcategory": "branch-protection"
        }
      }
    },
    "/search/users": {
      "get": {
        "summary": "Search users",
        "description": "Find users via various criteria. This method returns up to 100 results [per page](https://docs.github.com/rest/guides/using-pagination-in-the-rest-api).\n\nWhen searching for users, you can get text match metadata for the issue **login**, public **email**, and **name** fields when you pass the `text-match` media type. For more details about highlighting search results, see [Text match metadata](https://docs.github.com/rest/search/search#text-match-metadata). For more details about how to receive highlighted search results, see [Text match metadata](https://docs.github.com/rest/search/search#text-match-metadata).\n\nFor example, if you're looking for a list of popular users, you might try this query:\n\n`q=tom+repos:%3E42+followers:%3E1000`\n\nThis query searches for users with the name `tom`. The results are restricted to users with more than 42 repositories and over 1,000 followers.\n\nThis endpoint does not accept authentication and will only include publicly visible users. As an alternative, you can use the GraphQL API. The GraphQL API requires authentication and will return private users, including Enterprise Managed Users (EMUs), that you are authorized to view. For more information, see \"[GraphQL Queries](https://docs.github.com/graphql/reference/queries#search).\"",
        "tags": [
          "search"
        ],
        "operationId": "search/users",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/search/search#search-users"
        },
        "parameters": [
          {
            "name": "q",
            "description": "The query contains one or more search keywords and qualifiers. Qualifiers allow you to limit your search to specific areas of GitHub. The REST API supports the same qualifiers as the web interface for GitHub. To learn more about the format of the query, see [Constructing a search query](https://docs.github.com/rest/search/search#constructing-a-search-query). See \"[Searching users](https://docs.github.com/search-github/searching-on-github/searching-users)\" for a detailed list of qualifiers.",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "sort",
            "description": "Sorts the results of your query by number of `followers` or `repositories`, or when the person `joined` GitHub. Default: [best match](https://docs.github.com/rest/search/search#ranking-search-results)",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "followers",
                "repositories",
                "joined"
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
                    "items"
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
                        "$ref": "#/components/schemas/user-search-result-item"
                      }
                    }
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/user-search-result-item-paginated"
                  }
                }
              }
            }
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          },
          "503": {
            "$ref": "#/components/responses/service_unavailable"
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
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
    "/users": {
      "get": {
        "summary": "List users",
        "description": "Lists all users, in the order that they signed up on GitHub. This list includes personal user accounts and organization accounts.\n\nNote: Pagination is powered exclusively by the `since` parameter. Use the [Link header](https://docs.github.com/rest/guides/using-pagination-in-the-rest-api#using-link-headers) to get the URL for the next page of users.",
        "tags": [
          "users"
        ],
        "operationId": "users/list",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/users/users#list-users"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/since-user"
          },
          {
            "$ref": "#/components/parameters/per-page"
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
                    "$ref": "#/components/schemas/simple-user"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/simple-user-items"
                  }
                }
              }
            },
            "headers": {
              "Link": {
                "example": "<https://api.github.com/users?since=135>; rel=\"next\"",
                "schema": {
                  "type": "string"
                }
              }
            }
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "users",
          "subcategory": "users"
        }
      }
    },
    "/users/{username}": {
      "get": {
        "summary": "Get a user",
        "description": "Provides publicly available information about someone with a GitHub account.\n\nIf you are requesting information about an [Enterprise Managed User](https://docs.github.com/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/about-enterprise-managed-users), or a GitHub App bot that is installed in an organization that uses Enterprise Managed Users, your requests must be authenticated as a user or GitHub App that has access to the organization to view that account's information. If you are not authorized, the request will return a `404 Not Found` status.\n\nThe `email` key in the following response is the publicly visible email address from your GitHub [profile page](https://github.com/settings/profile). When setting up your profile, you can select a primary email address to be public which provides an email entry for this endpoint. If you do not set a public email address for `email`, then it will have a value of `null`. You only see publicly visible email addresses when authenticated with GitHub. For more information, see [Authentication](https://docs.github.com/rest/guides/getting-started-with-the-rest-api#authentication).\n\nThe Emails API enables you to list all of your email addresses, and toggle a primary email to be visible publicly. For more information, see [Emails API](https://docs.github.com/rest/users/emails).",
        "tags": [
          "users"
        ],
        "operationId": "users/get-by-username",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/users/users#get-a-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/username"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "oneOf": [
                    {
                      "$ref": "#/components/schemas/private-user"
                    },
                    {
                      "$ref": "#/components/schemas/public-user"
                    }
                  ],
                  "discriminator": {
                    "propertyName": "user_view_type",
                    "mapping": {
                      "public": "#/components/schemas/public-user",
                      "private": "#/components/schemas/private-user"
                    }
                  }
                },
                "examples": {
                  "default-response": {
                    "$ref": "#/components/examples/public-user-default-response"
                  },
                  "response-with-git-hub-plan-information": {
                    "$ref": "#/components/examples/public-user-response-with-git-hub-plan-information"
                  }
                }
              }
            }
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "users",
          "subcategory": "users"
        }
      }
    }
  },
  "schemas": {
    "api-insights-summary-stats": {
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
    },
    "api-insights-time-stats": {
      "title": "Time Stats",
      "description": "API Insights usage time stats for an organization",
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "timestamp": {
            "type": "string"
          },
          "total_request_count": {
            "type": "integer",
            "format": "int64"
          },
          "rate_limited_request_count": {
            "type": "integer",
            "format": "int64"
          }
        }
      }
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
    "user-search-result-item": {
      "title": "User Search Result Item",
      "description": "User Search Result Item",
      "type": "object",
      "properties": {
        "login": {
          "type": "string"
        },
        "id": {
          "type": "integer",
          "format": "int64"
        },
        "node_id": {
          "type": "string"
        },
        "avatar_url": {
          "type": "string",
          "format": "uri"
        },
        "gravatar_id": {
          "type": [
            "string",
            "null"
          ]
        },
        "url": {
          "type": "string",
          "format": "uri"
        },
        "html_url": {
          "type": "string",
          "format": "uri"
        },
        "followers_url": {
          "type": "string",
          "format": "uri"
        },
        "subscriptions_url": {
          "type": "string",
          "format": "uri"
        },
        "organizations_url": {
          "type": "string",
          "format": "uri"
        },
        "repos_url": {
          "type": "string",
          "format": "uri"
        },
        "received_events_url": {
          "type": "string",
          "format": "uri"
        },
        "type": {
          "type": "string"
        },
        "score": {
          "type": "number"
        },
        "following_url": {
          "type": "string"
        },
        "gists_url": {
          "type": "string"
        },
        "starred_url": {
          "type": "string"
        },
        "events_url": {
          "type": "string"
        },
        "public_repos": {
          "type": "integer"
        },
        "public_gists": {
          "type": "integer"
        },
        "followers": {
          "type": "integer"
        },
        "following": {
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
        "name": {
          "type": [
            "string",
            "null"
          ]
        },
        "bio": {
          "type": [
            "string",
            "null"
          ]
        },
        "email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email"
        },
        "location": {
          "type": [
            "string",
            "null"
          ]
        },
        "site_admin": {
          "type": "boolean"
        },
        "hireable": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "text_matches": {
          "$ref": "#/components/schemas/search-result-text-matches"
        },
        "blog": {
          "type": [
            "string",
            "null"
          ]
        },
        "company": {
          "type": [
            "string",
            "null"
          ]
        },
        "suspended_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time"
        },
        "user_view_type": {
          "type": "string"
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
        "url",
        "score"
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
    "user-role-assignment": {
      "title": "A Role Assignment for a User",
      "description": "The Relationship a User has with a role.",
      "type": "object",
      "properties": {
        "assignment": {
          "type": "string",
          "description": "Determines if the user has a direct, indirect, or mixed relationship to a role",
          "enum": [
            "direct",
            "indirect",
            "mixed"
          ],
          "examples": [
            "direct"
          ]
        },
        "inherited_from": {
          "description": "Team the user has gotten the role through",
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/team-simple"
          }
        },
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
    "private-user": {
      "title": "Private User",
      "description": "Private User",
      "type": "object",
      "properties": {
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
        "user_view_type": {
          "type": "string"
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
        "name": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "monalisa octocat"
          ]
        },
        "company": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "GitHub"
          ]
        },
        "blog": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "https://github.com/blog"
          ]
        },
        "location": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "San Francisco"
          ]
        },
        "email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email",
          "examples": [
            "octocat@github.com"
          ]
        },
        "notification_email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email",
          "examples": [
            "octocat@github.com"
          ]
        },
        "hireable": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "bio": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "There once was..."
          ]
        },
        "twitter_username": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "monalisa"
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
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2008-01-14T04:33:35Z"
          ]
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2008-01-14T04:33:35Z"
          ]
        },
        "private_gists": {
          "type": "integer",
          "examples": [
            81
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
        "disk_usage": {
          "type": "integer",
          "examples": [
            10000
          ]
        },
        "collaborators": {
          "type": "integer",
          "examples": [
            8
          ]
        },
        "two_factor_authentication": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "plan": {
          "type": "object",
          "properties": {
            "collaborators": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "space": {
              "type": "integer"
            },
            "private_repos": {
              "type": "integer"
            }
          },
          "required": [
            "collaborators",
            "name",
            "space",
            "private_repos"
          ]
        },
        "business_plus": {
          "type": "boolean"
        },
        "ldap_dn": {
          "type": "string"
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
        "url",
        "bio",
        "blog",
        "company",
        "email",
        "followers",
        "following",
        "hireable",
        "location",
        "name",
        "public_gists",
        "public_repos",
        "created_at",
        "updated_at",
        "collaborators",
        "disk_usage",
        "owned_private_repos",
        "private_gists",
        "total_private_repos",
        "two_factor_authentication"
      ]
    },
    "public-user": {
      "title": "Public User",
      "description": "Public User",
      "type": "object",
      "properties": {
        "login": {
          "type": "string"
        },
        "id": {
          "type": "integer",
          "format": "int64"
        },
        "user_view_type": {
          "type": "string"
        },
        "node_id": {
          "type": "string"
        },
        "avatar_url": {
          "type": "string",
          "format": "uri"
        },
        "gravatar_id": {
          "type": [
            "string",
            "null"
          ]
        },
        "url": {
          "type": "string",
          "format": "uri"
        },
        "html_url": {
          "type": "string",
          "format": "uri"
        },
        "followers_url": {
          "type": "string",
          "format": "uri"
        },
        "following_url": {
          "type": "string"
        },
        "gists_url": {
          "type": "string"
        },
        "starred_url": {
          "type": "string"
        },
        "subscriptions_url": {
          "type": "string",
          "format": "uri"
        },
        "organizations_url": {
          "type": "string",
          "format": "uri"
        },
        "repos_url": {
          "type": "string",
          "format": "uri"
        },
        "events_url": {
          "type": "string"
        },
        "received_events_url": {
          "type": "string",
          "format": "uri"
        },
        "type": {
          "type": "string"
        },
        "site_admin": {
          "type": "boolean"
        },
        "name": {
          "type": [
            "string",
            "null"
          ]
        },
        "company": {
          "type": [
            "string",
            "null"
          ]
        },
        "blog": {
          "type": [
            "string",
            "null"
          ]
        },
        "location": {
          "type": [
            "string",
            "null"
          ]
        },
        "email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email"
        },
        "notification_email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email"
        },
        "hireable": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "bio": {
          "type": [
            "string",
            "null"
          ]
        },
        "twitter_username": {
          "type": [
            "string",
            "null"
          ]
        },
        "public_repos": {
          "type": "integer"
        },
        "public_gists": {
          "type": "integer"
        },
        "followers": {
          "type": "integer"
        },
        "following": {
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
        "plan": {
          "type": "object",
          "properties": {
            "collaborators": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "space": {
              "type": "integer"
            },
            "private_repos": {
              "type": "integer"
            }
          },
          "required": [
            "collaborators",
            "name",
            "space",
            "private_repos"
          ]
        },
        "private_gists": {
          "type": "integer",
          "examples": [
            1
          ]
        },
        "total_private_repos": {
          "type": "integer",
          "examples": [
            2
          ]
        },
        "owned_private_repos": {
          "type": "integer",
          "examples": [
            2
          ]
        },
        "disk_usage": {
          "type": "integer",
          "examples": [
            1
          ]
        },
        "collaborators": {
          "type": "integer",
          "examples": [
            3
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
        "url",
        "bio",
        "blog",
        "company",
        "email",
        "followers",
        "following",
        "hireable",
        "location",
        "name",
        "public_gists",
        "public_repos",
        "created_at",
        "updated_at"
      ],
      "additionalProperties": false
    }
  },
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

Resource `user` uses: alphabet=NUMERIC, length=1

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

- Table name: `github_users`
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
