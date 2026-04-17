# Entity Implementation: repos

You are implementing the **repos** resource for the GitHub API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for repos

```json
{
  "paths": {
    "/orgs/{org}/repos": {
      "get": {
        "summary": "List organization repositories",
        "description": "Lists repositories for the specified organization.\n\n> [!NOTE]\n> In order to see the `security_and_analysis` block for a repository you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"",
        "tags": [
          "repos"
        ],
        "operationId": "repos/list-for-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/repos/repos#list-organization-repositories"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "name": "type",
            "description": "Specifies the types of repositories you want returned.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "all",
                "public",
                "private",
                "forks",
                "sources",
                "member"
              ],
              "default": "all"
            }
          },
          {
            "name": "sort",
            "description": "The property to sort the results by.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "created",
                "updated",
                "pushed",
                "full_name"
              ],
              "default": "created"
            }
          },
          {
            "name": "direction",
            "description": "The order to sort by. Default: `asc` when using `full_name`, otherwise `desc`.",
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
                    "$ref": "#/components/schemas/minimal-repository"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/minimal-repository-items"
                  }
                }
              }
            },
            "headers": {
              "Link": {
                "$ref": "#/components/headers/link"
              }
            }
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "repos",
          "subcategory": "repos"
        }
      },
      "post": {
        "summary": "Create an organization repository",
        "description": "Creates a new repository in the specified organization. The authenticated user must be a member of the organization.\n\nOAuth app tokens and personal access tokens (classic) need the `public_repo` or `repo` scope to create a public repository, and `repo` scope to create a private repository.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/create-in-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/repos/repos#create-an-organization-repository"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "The name of the repository."
                  },
                  "description": {
                    "type": "string",
                    "description": "A short description of the repository."
                  },
                  "homepage": {
                    "type": "string",
                    "description": "A URL with more information about the repository."
                  },
                  "private": {
                    "type": "boolean",
                    "description": "Whether the repository is private.",
                    "default": false
                  },
                  "visibility": {
                    "type": "string",
                    "description": "The visibility of the repository.",
                    "enum": [
                      "public",
                      "private"
                    ]
                  },
                  "has_issues": {
                    "type": "boolean",
                    "description": "Either `true` to enable issues for this repository or `false` to disable them.",
                    "default": true
                  },
                  "has_projects": {
                    "type": "boolean",
                    "description": "Either `true` to enable projects for this repository or `false` to disable them. **Note:** If you're creating a repository in an organization that has disabled repository projects, the default is `false`, and if you pass `true`, the API returns an error.",
                    "default": true
                  },
                  "has_wiki": {
                    "type": "boolean",
                    "description": "Either `true` to enable the wiki for this repository or `false` to disable it.",
                    "default": true
                  },
                  "has_downloads": {
                    "description": "Whether downloads are enabled.",
                    "default": true,
                    "type": "boolean",
                    "examples": [
                      true
                    ]
                  },
                  "is_template": {
                    "type": "boolean",
                    "description": "Either `true` to make this repo available as a template repository or `false` to prevent it.",
                    "default": false
                  },
                  "team_id": {
                    "type": "integer",
                    "description": "The id of the team that will be granted access to this repository. This is only valid when creating a repository in an organization."
                  },
                  "auto_init": {
                    "type": "boolean",
                    "description": "Pass `true` to create an initial commit with empty README.",
                    "default": false
                  },
                  "gitignore_template": {
                    "type": "string",
                    "description": "Desired language or platform [.gitignore template](https://github.com/github/gitignore) to apply. Use the name of the template without the extension. For example, \"Haskell\"."
                  },
                  "license_template": {
                    "type": "string",
                    "description": "Choose an [open source license template](https://choosealicense.com/) that best suits your needs, and then use the [license keyword](https://docs.github.com/articles/licensing-a-repository/#searching-github-by-license-type) as the `license_template` string. For example, \"mit\" or \"mpl-2.0\"."
                  },
                  "allow_squash_merge": {
                    "type": "boolean",
                    "description": "Either `true` to allow squash-merging pull requests, or `false` to prevent squash-merging.",
                    "default": true
                  },
                  "allow_merge_commit": {
                    "type": "boolean",
                    "description": "Either `true` to allow merging pull requests with a merge commit, or `false` to prevent merging pull requests with merge commits.",
                    "default": true
                  },
                  "allow_rebase_merge": {
                    "type": "boolean",
                    "description": "Either `true` to allow rebase-merging pull requests, or `false` to prevent rebase-merging.",
                    "default": true
                  },
                  "allow_auto_merge": {
                    "type": "boolean",
                    "description": "Either `true` to allow auto-merge on pull requests, or `false` to disallow auto-merge.",
                    "default": false
                  },
                  "delete_branch_on_merge": {
                    "type": "boolean",
                    "description": "Either `true` to allow automatically deleting head branches when pull requests are merged, or `false` to prevent automatic deletion. **The authenticated user must be an organization owner to set this property to `true`.**",
                    "default": false
                  },
                  "use_squash_pr_title_as_default": {
                    "type": "boolean",
                    "description": "Either `true` to allow squash-merge commits to use pull request title, or `false` to use commit message. **This property is closing down. Please use `squash_merge_commit_title` instead.",
                    "default": false,
                    "deprecated": true
                  },
                  "squash_merge_commit_title": {
                    "type": "string",
                    "enum": [
                      "PR_TITLE",
                      "COMMIT_OR_PR_TITLE"
                    ],
                    "description": "Required when using `squash_merge_commit_message`.\n\nThe default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit)."
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
                    "description": "Required when using `merge_commit_message`.\n\nThe default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name)."
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
                  "custom_properties": {
                    "type": "object",
                    "description": "The custom properties for the new repository. The keys are the custom property names, and the values are the corresponding custom property values.",
                    "additionalProperties": true
                  }
                },
                "required": [
                  "name"
                ]
              },
              "examples": {
                "default": {
                  "value": {
                    "name": "Hello-World",
                    "description": "This is your first repository",
                    "homepage": "https://github.com",
                    "private": false,
                    "has_issues": true,
                    "has_projects": true,
                    "has_wiki": true
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
                  "$ref": "#/components/schemas/full-repository"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/full-repository"
                  }
                }
              }
            },
            "headers": {
              "Location": {
                "example": "https://api.github.com/repos/octocat/Hello-World",
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
          },
          "451": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "repos",
          "subcategory": "repos"
        }
      }
    },
    "/orgs/{org}/teams/{team_slug}/repos": {
      "get": {
        "summary": "List team repositories",
        "description": "Lists a team's repositories visible to the authenticated user.\n\n> [!NOTE]\n> You can also specify a team by `org_id` and `team_id` using the route `GET /organizations/{org_id}/team/{team_id}/repos`.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/list-repos-in-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#list-team-repositories"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
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
                    "$ref": "#/components/schemas/minimal-repository"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/minimal-repository-items"
                  }
                }
              }
            },
            "headers": {
              "Link": {
                "$ref": "#/components/headers/link"
              }
            }
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "teams",
          "subcategory": "teams"
        }
      }
    },
    "/orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}": {
      "get": {
        "summary": "Check team permissions for a repository",
        "description": "Checks whether a team has `admin`, `push`, `maintain`, `triage`, or `pull` permission for a repository. Repositories inherited through a parent team will also be checked.\n\nYou can also get information about the specified repository, including what permissions the team grants on it, by passing the following custom [media type](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types/) via the `application/vnd.github.v3.repository+json` accept header.\n\nIf a team doesn't have permission for the repository, you will receive a `404 Not Found` response status.\n\nIf the repository is private, you must have at least `read` permission for that repository, and your token must have the `repo` or `admin:org` scope. Otherwise, you will receive a `404 Not Found` response status.\n\n> [!NOTE]\n> You can also specify a team by `org_id` and `team_id` using the route `GET /organizations/{org_id}/team/{team_id}/repos/{owner}/{repo}`.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/check-permissions-for-repo-in-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#check-team-permissions-for-a-repository"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
          },
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          }
        ],
        "responses": {
          "200": {
            "description": "Alternative response with repository permissions",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/team-repository"
                },
                "examples": {
                  "alternative-response-with-repository-permissions": {
                    "$ref": "#/components/examples/team-repository-alternative-response-with-repository-permissions"
                  }
                }
              }
            }
          },
          "204": {
            "description": "Response if team has permission for the repository. This is the response when the repository media type hasn't been provded in the Accept header."
          },
          "404": {
            "description": "Not Found if team does not have permission for the repository"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "teams",
          "subcategory": "teams"
        }
      },
      "put": {
        "summary": "Add or update team repository permissions",
        "description": "To add a repository to a team or update the team's permission on a repository, the authenticated user must have admin access to the repository, and must be able to see the team. The repository must be owned by the organization, or a direct fork of a repository owned by the organization. You will get a `422 Unprocessable Entity` status if you attempt to add a repository to a team that is not owned by the organization. Note that, if you choose not to pass any parameters, you'll need to set `Content-Length` to zero when calling out to this endpoint. For more information, see \"[HTTP method](https://docs.github.com/rest/guides/getting-started-with-the-rest-api#http-method).\"\n\n> [!NOTE]\n> You can also specify a team by `org_id` and `team_id` using the route `PUT /organizations/{org_id}/team/{team_id}/repos/{owner}/{repo}`.\n\nFor more information about the permission levels, see \"[Repository permission levels for an organization](https://docs.github.com/github/setting-up-and-managing-organizations-and-teams/repository-permission-levels-for-an-organization#permission-levels-for-repositories-owned-by-an-organization)\".",
        "tags": [
          "teams"
        ],
        "operationId": "teams/add-or-update-repo-permissions-in-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#add-or-update-team-repository-permissions"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
          },
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          }
        ],
        "requestBody": {
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "permission": {
                    "type": "string",
                    "description": "The permission to grant the team on this repository. We accept the following permissions to be set: `pull`, `triage`, `push`, `maintain`, `admin` and you can also specify a custom repository role name, if the owning organization has defined any. If no permission is specified, the team's `permission` attribute will be used to determine what permission to grant the team on this repository."
                  }
                }
              },
              "examples": {
                "default": {
                  "summary": "Adding a team to an organization repository with the write role",
                  "value": {
                    "permission": "push"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "204": {
            "description": "Response"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "teams",
          "subcategory": "teams"
        }
      },
      "delete": {
        "summary": "Remove a repository from a team",
        "description": "If the authenticated user is an organization owner or a team maintainer, they can remove any repositories from the team. To remove a repository from a team as an organization member, the authenticated user must have admin access to the repository and must be able to see the team. This does not delete the repository, it just removes it from the team.\n\n> [!NOTE]\n> You can also specify a team by `org_id` and `team_id` using the route `DELETE /organizations/{org_id}/team/{team_id}/repos/{owner}/{repo}`.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/remove-repo-in-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#remove-a-repository-from-a-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
          },
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
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
          "category": "teams",
          "subcategory": "teams"
        }
      }
    },
    "/repos/{owner}/{repo}": {
      "get": {
        "summary": "Get a repository",
        "description": "The `parent` and `source` objects are present when the repository is a fork. `parent` is the repository this repository was forked from, `source` is the ultimate source for the network.\n\n> [!NOTE]\n> - In order to see the `security_and_analysis` block for a repository you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"\n> - To view merge-related settings, you must have the `contents:read` and `contents:write` permissions.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/get",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/repos/repos#get-a-repository"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/full-repository"
                },
                "examples": {
                  "default-response": {
                    "$ref": "#/components/examples/full-repository-default-response"
                  }
                }
              }
            }
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "301": {
            "$ref": "#/components/responses/moved_permanently"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "repos",
          "subcategory": "repos"
        }
      },
      "patch": {
        "summary": "Update a repository",
        "description": "**Note**: To edit a repository's topics, use the [Replace all repository topics](https://docs.github.com/rest/repos/repos#replace-all-repository-topics) endpoint.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/update",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/repos/repos#update-a-repository"
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
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "The name of the repository."
                  },
                  "description": {
                    "type": "string",
                    "description": "A short description of the repository."
                  },
                  "homepage": {
                    "type": "string",
                    "description": "A URL with more information about the repository."
                  },
                  "private": {
                    "type": "boolean",
                    "description": "Either `true` to make the repository private or `false` to make it public. Default: `false`.  \n**Note**: You will get a `422` error if the organization restricts [changing repository visibility](https://docs.github.com/articles/repository-permission-levels-for-an-organization#changing-the-visibility-of-repositories) to organization owners and a non-owner tries to change the value of private.",
                    "default": false
                  },
                  "visibility": {
                    "type": "string",
                    "description": "The visibility of the repository.",
                    "enum": [
                      "public",
                      "private"
                    ]
                  },
                  "security_and_analysis": {
                    "type": [
                      "object",
                      "null"
                    ],
                    "description": "Specify which security and analysis features to enable or disable for the repository.\n\nTo use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"\n\nFor example, to enable GitHub Advanced Security, use this data in the body of the `PATCH` request:\n`{ \"security_and_analysis\": {\"advanced_security\": { \"status\": \"enabled\" } } }`.\n\nYou can check which security and analysis features are currently enabled by using a `GET /repos/{owner}/{repo}` request.",
                    "properties": {
                      "advanced_security": {
                        "type": "object",
                        "description": "Use the `status` property to enable or disable GitHub Advanced Security for this repository.\nFor more information, see \"[About GitHub Advanced\nSecurity](/github/getting-started-with-github/learning-about-github/about-github-advanced-security).\"\n\nFor standalone Code Scanning or Secret Protection products, this parameter cannot be used.",
                        "properties": {
                          "status": {
                            "type": "string",
                            "description": "Can be `enabled` or `disabled`."
                          }
                        }
                      },
                      "code_security": {
                        "type": "object",
                        "description": "Use the `status` property to enable or disable GitHub Code Security for this repository.",
                        "properties": {
                          "status": {
                            "type": "string",
                            "description": "Can be `enabled` or `disabled`."
                          }
                        }
                      },
                      "secret_scanning": {
                        "type": "object",
                        "description": "Use the `status` property to enable or disable secret scanning for this repository. For more information, see \"[About secret scanning](/code-security/secret-security/about-secret-scanning).\"",
                        "properties": {
                          "status": {
                            "type": "string",
                            "description": "Can be `enabled` or `disabled`."
                          }
                        }
                      },
                      "secret_scanning_push_protection": {
                        "type": "object",
                        "description": "Use the `status` property to enable or disable secret scanning push protection for this repository. For more information, see \"[Protecting pushes with secret scanning](/code-security/secret-scanning/protecting-pushes-with-secret-scanning).\"",
                        "properties": {
                          "status": {
                            "type": "string",
                            "description": "Can be `enabled` or `disabled`."
                          }
                        }
                      },
                      "secret_scanning_ai_detection": {
                        "type": "object",
                        "description": "Use the `status` property to enable or disable secret scanning AI detection for this repository. For more information, see \"[Responsible detection of generic secrets with AI](https://docs.github.com/code-security/secret-scanning/using-advanced-secret-scanning-and-push-protection-features/generic-secret-detection/responsible-ai-generic-secrets).\"",
                        "properties": {
                          "status": {
                            "type": "string",
                            "description": "Can be `enabled` or `disabled`."
                          }
                        }
                      },
                      "secret_scanning_non_provider_patterns": {
                        "type": "object",
                        "description": "Use the `status` property to enable or disable secret scanning non-provider patterns for this repository. For more information, see \"[Supported secret scanning patterns](/code-security/secret-scanning/introduction/supported-secret-scanning-patterns#supported-secrets).\"",
                        "properties": {
                          "status": {
                            "type": "string",
                            "description": "Can be `enabled` or `disabled`."
                          }
                        }
                      },
                      "secret_scanning_delegated_alert_dismissal": {
                        "type": "object",
                        "description": "Use the `status` property to enable or disable secret scanning delegated alert dismissal for this repository.",
                        "properties": {
                          "status": {
                            "type": "string",
                            "description": "Can be `enabled` or `disabled`."
                          }
                        }
                      },
                      "secret_scanning_delegated_bypass": {
                        "type": "object",
                        "description": "Use the `status` property to enable or disable secret scanning delegated bypass for this repository.",
                        "properties": {
                          "status": {
                            "type": "string",
                            "description": "Can be `enabled` or `disabled`."
                          }
                        }
                      },
                      "secret_scanning_delegated_bypass_options": {
                        "type": "object",
                        "description": "Feature options for secret scanning delegated bypass.\nThis object is only honored when `security_and_analysis.secret_scanning_delegated_bypass.status` is set to `enabled`.\nYou can send this object in the same request as `secret_scanning_delegated_bypass`, or update just the options in a separate request.",
                        "properties": {
                          "reviewers": {
                            "type": "array",
                            "description": "The bypass reviewers for secret scanning delegated bypass.\nIf you omit this field, the existing set of reviewers is unchanged.",
                            "items": {
                              "type": "object",
                              "required": [
                                "reviewer_id",
                                "reviewer_type"
                              ],
                              "properties": {
                                "reviewer_id": {
                                  "type": "integer",
                                  "description": "The ID of the team or role selected as a bypass reviewer"
                                },
                                "reviewer_type": {
                                  "type": "string",
                                  "description": "The type of the bypass reviewer",
                                  "enum": [
                                    "TEAM",
                                    "ROLE"
                                  ]
                                },
                                "mode": {
                                  "type": "string",
                                  "description": "The bypass mode for the reviewer",
                                  "enum": [
                                    "ALWAYS",
                                    "EXEMPT"
                                  ],
                                  "default": "ALWAYS"
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  },
                  "has_issues": {
                    "type": "boolean",
                    "description": "Either `true` to enable issues for this repository or `false` to disable them.",
                    "default": true
                  },
                  "has_projects": {
                    "type": "boolean",
                    "description": "Either `true` to enable projects for this repository or `false` to disable them. **Note:** If you're creating a repository in an organization that has disabled repository projects, the default is `false`, and if you pass `true`, the API returns an error.",
                    "default": true
                  },
                  "has_wiki": {
                    "type": "boolean",
                    "description": "Either `true` to enable the wiki for this repository or `false` to disable it.",
                    "default": true
                  },
                  "is_template": {
                    "type": "boolean",
                    "description": "Either `true` to make this repo available as a template repository or `false` to prevent it.",
                    "default": false
                  },
                  "default_branch": {
                    "type": "string",
                    "description": "Updates the default branch for this repository."
                  },
                  "allow_squash_merge": {
                    "type": "boolean",
                    "description": "Either `true` to allow squash-merging pull requests, or `false` to prevent squash-merging.",
                    "default": true
                  },
                  "allow_merge_commit": {
                    "type": "boolean",
                    "description": "Either `true` to allow merging pull requests with a merge commit, or `false` to prevent merging pull requests with merge commits.",
                    "default": true
                  },
                  "allow_rebase_merge": {
                    "type": "boolean",
                    "description": "Either `true` to allow rebase-merging pull requests, or `false` to prevent rebase-merging.",
                    "default": true
                  },
                  "allow_auto_merge": {
                    "type": "boolean",
                    "description": "Either `true` to allow auto-merge on pull requests, or `false` to disallow auto-merge.",
                    "default": false
                  },
                  "delete_branch_on_merge": {
                    "type": "boolean",
                    "description": "Either `true` to allow automatically deleting head branches when pull requests are merged, or `false` to prevent automatic deletion.",
                    "default": false
                  },
                  "allow_update_branch": {
                    "type": "boolean",
                    "description": "Either `true` to always allow a pull request head branch that is behind its base branch to be updated even if it is not required to be up to date before merging, or false otherwise.",
                    "default": false
                  },
                  "use_squash_pr_title_as_default": {
                    "type": "boolean",
                    "description": "Either `true` to allow squash-merge commits to use pull request title, or `false` to use commit message. **This property is closing down. Please use `squash_merge_commit_title` instead.",
                    "default": false,
                    "deprecated": true
                  },
                  "squash_merge_commit_title": {
                    "type": "string",
                    "enum": [
                      "PR_TITLE",
                      "COMMIT_OR_PR_TITLE"
                    ],
                    "description": "Required when using `squash_merge_commit_message`.\n\nThe default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit)."
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
                    "description": "Required when using `merge_commit_message`.\n\nThe default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name)."
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
                  "archived": {
                    "type": "boolean",
                    "description": "Whether to archive this repository. `false` will unarchive a previously archived repository.",
                    "default": false
                  },
                  "allow_forking": {
                    "type": "boolean",
                    "description": "Either `true` to allow private forks, or `false` to prevent private forks.",
                    "default": false
                  },
                  "web_commit_signoff_required": {
                    "type": "boolean",
                    "description": "Either `true` to require contributors to sign off on web-based commits, or `false` to not require contributors to sign off on web-based commits.",
                    "default": false
                  }
                }
              },
              "examples": {
                "default": {
                  "value": {
                    "name": "Hello-World",
                    "description": "This is your first repository",
                    "homepage": "https://github.com",
                    "private": true,
                    "has_issues": true,
                    "has_projects": true,
                    "has_wiki": true
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
                  "$ref": "#/components/schemas/full-repository"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/full-repository"
                  }
                }
              }
            }
          },
          "307": {
            "$ref": "#/components/responses/temporary_redirect"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
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
          "category": "repos",
          "subcategory": "repos"
        }
      },
      "delete": {
        "summary": "Delete a repository",
        "description": "Deleting a repository requires admin access.\n\nIf an organization owner has configured the organization to prevent members from deleting organization-owned\nrepositories, you will get a `403 Forbidden` response.\n\nOAuth app tokens and personal access tokens (classic) need the `delete_repo` scope to use this endpoint.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/delete",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/repos/repos#delete-a-repository"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
          },
          "403": {
            "description": "If an organization owner has configured the organization to prevent members from deleting organization-owned repositories, a member will get this response:",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string"
                    },
                    "documentation_url": {
                      "type": "string"
                    }
                  }
                },
                "examples": {
                  "default": {
                    "value": {
                      "message": "Organization members cannot delete repositories.",
                      "documentation_url": "https://docs.github.com/rest/repos/repos#delete-a-repository"
                    }
                  }
                }
              }
            }
          },
          "307": {
            "$ref": "#/components/responses/temporary_redirect"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "409": {
            "$ref": "#/components/responses/conflict"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "repos",
          "subcategory": "repos"
        }
      }
    },
    "/repos/{owner}/{repo}/code-scanning/codeql/variant-analyses/{codeql_variant_analysis_id}/repos/{repo_owner}/{repo_name}": {
      "get": {
        "summary": "Get the analysis status of a repository in a CodeQL variant analysis",
        "description": "Gets the analysis status of a repository in a CodeQL variant analysis.\n\nOAuth app tokens and personal access tokens (classic) need the `security_events` scope to use this endpoint with private or public repositories, or the `public_repo` scope to use this endpoint with only public repositories.",
        "tags": [
          "code-scanning"
        ],
        "operationId": "code-scanning/get-variant-analysis-repo-task",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/code-scanning/code-scanning#get-the-analysis-status-of-a-repository-in-a-codeql-variant-analysis"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "name": "repo",
            "in": "path",
            "description": "The name of the controller repository.",
            "schema": {
              "type": "string"
            },
            "required": true
          },
          {
            "name": "codeql_variant_analysis_id",
            "in": "path",
            "description": "The ID of the variant analysis.",
            "schema": {
              "type": "integer"
            },
            "required": true
          },
          {
            "name": "repo_owner",
            "in": "path",
            "description": "The account owner of the variant analysis repository. The name is not case sensitive.",
            "schema": {
              "type": "string"
            },
            "required": true
          },
          {
            "name": "repo_name",
            "in": "path",
            "description": "The name of the variant analysis repository.",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/code-scanning-variant-analysis-repo-task"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/code-scanning-variant-analysis-repo-task"
                  }
                }
              }
            }
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "503": {
            "$ref": "#/components/responses/service_unavailable"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "previews": [],
          "category": "code-scanning",
          "subcategory": "code-scanning"
        }
      }
    },
    "/teams/{team_id}/repos": {
      "get": {
        "summary": "List team repositories (Legacy)",
        "description": "> [!WARNING]\n> **Endpoint closing down notice:** This endpoint route is closing down and will be removed from the Teams API. We recommend migrating your existing code to use the new [List team repositories](https://docs.github.com/rest/teams/teams#list-team-repositories) endpoint.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/list-repos-legacy",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#list-team-repositories-legacy"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/team-id"
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
                    "$ref": "#/components/schemas/minimal-repository"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/minimal-repository-items"
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
          "enabledForGitHubApps": true,
          "removalDate": "2021-02-01",
          "deprecationDate": "2020-01-21",
          "category": "teams",
          "subcategory": "teams"
        },
        "deprecated": true
      }
    },
    "/teams/{team_id}/repos/{owner}/{repo}": {
      "get": {
        "summary": "Check team permissions for a repository (Legacy)",
        "description": "> [!WARNING]\n> **Endpoint closing down notice:** This endpoint route is closing down and will be removed from the Teams API. We recommend migrating your existing code to use the new [Check team permissions for a repository](https://docs.github.com/rest/teams/teams#check-team-permissions-for-a-repository) endpoint.\n\n> [!NOTE]\n> Repositories inherited through a parent team will also be checked.\n\nYou can also get information about the specified repository, including what permissions the team grants on it, by passing the following custom [media type](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types/) via the `Accept` header:",
        "tags": [
          "teams"
        ],
        "operationId": "teams/check-permissions-for-repo-legacy",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#check-team-permissions-for-a-repository-legacy"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/team-id"
          },
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          }
        ],
        "responses": {
          "200": {
            "description": "Alternative response with extra repository information",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/team-repository"
                },
                "examples": {
                  "alternative-response-with-extra-repository-information": {
                    "$ref": "#/components/examples/team-repository-alternative-response-with-extra-repository-information"
                  }
                }
              }
            }
          },
          "204": {
            "description": "Response if repository is managed by this team"
          },
          "404": {
            "description": "Not Found if repository is not managed by this team"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "removalDate": "2021-02-01",
          "deprecationDate": "2020-01-21",
          "category": "teams",
          "subcategory": "teams"
        },
        "deprecated": true
      },
      "put": {
        "summary": "Add or update team repository permissions (Legacy)",
        "description": "> [!WARNING]\n> **Endpoint closing down notice:** This endpoint route is closing down and will be removed from the Teams API. We recommend migrating your existing code to use the new \"[Add or update team repository permissions](https://docs.github.com/rest/teams/teams#add-or-update-team-repository-permissions)\" endpoint.\n\nTo add a repository to a team or update the team's permission on a repository, the authenticated user must have admin access to the repository, and must be able to see the team. The repository must be owned by the organization, or a direct fork of a repository owned by the organization. You will get a `422 Unprocessable Entity` status if you attempt to add a repository to a team that is not owned by the organization.\n\nNote that, if you choose not to pass any parameters, you'll need to set `Content-Length` to zero when calling out to this endpoint. For more information, see \"[HTTP method](https://docs.github.com/rest/guides/getting-started-with-the-rest-api#http-method).\"",
        "tags": [
          "teams"
        ],
        "operationId": "teams/add-or-update-repo-permissions-legacy",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#add-or-update-team-repository-permissions-legacy"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/team-id"
          },
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
          }
        ],
        "requestBody": {
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "permission": {
                    "type": "string",
                    "description": "The permission to grant the team on this repository. If no permission is specified, the team's `permission` attribute will be used to determine what permission to grant the team on this repository.",
                    "enum": [
                      "pull",
                      "push",
                      "admin"
                    ]
                  }
                }
              },
              "examples": {
                "default": {
                  "summary": "Example of setting permission to pull",
                  "value": {
                    "permission": "push"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "204": {
            "description": "Response"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "removalDate": "2021-02-01",
          "deprecationDate": "2020-01-21",
          "category": "teams",
          "subcategory": "teams"
        },
        "deprecated": true
      },
      "delete": {
        "summary": "Remove a repository from a team (Legacy)",
        "description": "> [!WARNING]\n> **Endpoint closing down notice:** This endpoint route is closing down and will be removed from the Teams API. We recommend migrating your existing code to use the new [Remove a repository from a team](https://docs.github.com/rest/teams/teams#remove-a-repository-from-a-team) endpoint.\n\nIf the authenticated user is an organization owner or a team maintainer, they can remove any repositories from the team. To remove a repository from a team as an organization member, the authenticated user must have admin access to the repository and must be able to see the team. NOTE: This does not delete the repository, it just removes it from the team.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/remove-repo-legacy",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#remove-a-repository-from-a-team-legacy"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/team-id"
          },
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
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
          "removalDate": "2021-02-01",
          "deprecationDate": "2020-01-21",
          "category": "teams",
          "subcategory": "teams"
        },
        "deprecated": true
      }
    },
    "/user/repos": {
      "get": {
        "summary": "List repositories for the authenticated user",
        "description": "Lists repositories that the authenticated user has explicit permission (`:read`, `:write`, or `:admin`) to access.\n\nThe authenticated user has explicit permission to access repositories they own, repositories where they are a collaborator, and repositories that they can access through an organization membership.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/list-for-authenticated-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/repos/repos#list-repositories-for-the-authenticated-user"
        },
        "parameters": [
          {
            "name": "visibility",
            "description": "Limit results to repositories with the specified visibility.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "all",
                "public",
                "private"
              ],
              "default": "all"
            }
          },
          {
            "name": "affiliation",
            "description": "Comma-separated list of values. Can include:  \n * `owner`: Repositories that are owned by the authenticated user.  \n * `collaborator`: Repositories that the user has been added to as a collaborator.  \n * `organization_member`: Repositories that the user has access to through being a member of an organization. This includes every repository on every team that the user is on.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "default": "owner,collaborator,organization_member"
            }
          },
          {
            "name": "type",
            "description": "Limit results to repositories of the specified type. Will cause a `422` error if used in the same request as **visibility** or **affiliation**.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "all",
                "owner",
                "public",
                "private",
                "member"
              ],
              "default": "all"
            }
          },
          {
            "name": "sort",
            "description": "The property to sort the results by.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "created",
                "updated",
                "pushed",
                "full_name"
              ],
              "default": "full_name"
            }
          },
          {
            "name": "direction",
            "description": "The order to sort by. Default: `asc` when using `full_name`, otherwise `desc`.",
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
          },
          {
            "$ref": "#/components/parameters/since-repo-date"
          },
          {
            "$ref": "#/components/parameters/before-repo-date"
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
                    "$ref": "#/components/schemas/repository"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/repository-items-default-response"
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
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "401": {
            "$ref": "#/components/responses/requires_authentication"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "repos",
          "subcategory": "repos"
        }
      },
      "post": {
        "summary": "Create a repository for the authenticated user",
        "description": "Creates a new repository for the authenticated user.\n\nOAuth app tokens and personal access tokens (classic) need the `public_repo` or `repo` scope to create a public repository, and `repo` scope to create a private repository.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/create-for-authenticated-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/repos/repos#create-a-repository-for-the-authenticated-user"
        },
        "parameters": [],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "properties": {
                  "name": {
                    "description": "The name of the repository.",
                    "type": "string",
                    "examples": [
                      "Team Environment"
                    ]
                  },
                  "description": {
                    "description": "A short description of the repository.",
                    "type": "string"
                  },
                  "homepage": {
                    "description": "A URL with more information about the repository.",
                    "type": "string"
                  },
                  "private": {
                    "description": "Whether the repository is private.",
                    "default": false,
                    "type": "boolean"
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
                  "has_discussions": {
                    "description": "Whether discussions are enabled.",
                    "default": false,
                    "type": "boolean",
                    "examples": [
                      true
                    ]
                  },
                  "team_id": {
                    "description": "The id of the team that will be granted access to this repository. This is only valid when creating a repository in an organization.",
                    "type": "integer"
                  },
                  "auto_init": {
                    "description": "Whether the repository is initialized with a minimal README.",
                    "default": false,
                    "type": "boolean"
                  },
                  "gitignore_template": {
                    "description": "The desired language or platform to apply to the .gitignore.",
                    "type": "string",
                    "examples": [
                      "Haskell"
                    ]
                  },
                  "license_template": {
                    "description": "The license keyword of the open source license for this repository.",
                    "type": "string",
                    "examples": [
                      "mit"
                    ]
                  },
                  "allow_squash_merge": {
                    "description": "Whether to allow squash merges for pull requests.",
                    "default": true,
                    "type": "boolean",
                    "examples": [
                      true
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
                  "allow_rebase_merge": {
                    "description": "Whether to allow rebase merges for pull requests.",
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
                  "squash_merge_commit_title": {
                    "type": "string",
                    "enum": [
                      "PR_TITLE",
                      "COMMIT_OR_PR_TITLE"
                    ],
                    "description": "Required when using `squash_merge_commit_message`.\n\nThe default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit)."
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
                    "description": "Required when using `merge_commit_message`.\n\nThe default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name)."
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
                  "has_downloads": {
                    "description": "Whether downloads are enabled.",
                    "default": true,
                    "type": "boolean",
                    "examples": [
                      true
                    ]
                  },
                  "is_template": {
                    "description": "Whether this repository acts as a template that can be used to generate new repositories.",
                    "default": false,
                    "type": "boolean",
                    "examples": [
                      true
                    ]
                  }
                },
                "required": [
                  "name"
                ],
                "type": "object"
              },
              "examples": {
                "default": {
                  "value": {
                    "name": "Hello-World",
                    "description": "This is your first repo!",
                    "homepage": "https://github.com",
                    "private": false,
                    "is_template": true
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
                  "$ref": "#/components/schemas/full-repository"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/full-repository"
                  }
                }
              }
            },
            "headers": {
              "Location": {
                "example": "https://api.github.com/repos/octocat/Hello-World",
                "schema": {
                  "type": "string"
                }
              }
            }
          },
          "401": {
            "$ref": "#/components/responses/requires_authentication"
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          },
          "400": {
            "$ref": "#/components/responses/bad_request"
          },
          "451": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "repos",
          "subcategory": "repos"
        }
      }
    },
    "/users/{username}/repos": {
      "get": {
        "summary": "List repositories for a user",
        "description": "Lists public repositories for the specified user.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/list-for-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/repos/repos#list-repositories-for-a-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/username"
          },
          {
            "name": "type",
            "description": "Limit results to repositories of the specified type.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "all",
                "owner",
                "member"
              ],
              "default": "owner"
            }
          },
          {
            "name": "sort",
            "description": "The property to sort the results by.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "created",
                "updated",
                "pushed",
                "full_name"
              ],
              "default": "full_name"
            }
          },
          {
            "name": "direction",
            "description": "The order to sort by. Default: `asc` when using `full_name`, otherwise `desc`.",
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
                    "$ref": "#/components/schemas/minimal-repository"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/minimal-repository-items"
                  }
                }
              }
            },
            "headers": {
              "Link": {
                "$ref": "#/components/headers/link"
              }
            }
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "repos",
          "subcategory": "repos"
        }
      }
    }
  },
  "schemas": {
    "team-repository": {
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
    "code-scanning-variant-analysis-repo-task": {
      "type": "object",
      "properties": {
        "repository": {
          "$ref": "#/components/schemas/simple-repository"
        },
        "analysis_status": {
          "$ref": "#/components/schemas/code-scanning-variant-analysis-status"
        },
        "artifact_size_in_bytes": {
          "type": "integer",
          "description": "The size of the artifact. This is only available for successful analyses."
        },
        "result_count": {
          "type": "integer",
          "description": "The number of results in the case of a successful analysis. This is only available for successful analyses."
        },
        "failure_message": {
          "type": "string",
          "description": "The reason of the failure of this repo task. This is only available if the repository task has failed."
        },
        "database_commit_sha": {
          "type": "string",
          "description": "The SHA of the commit the CodeQL database was built against. This is only available for successful analyses."
        },
        "source_location_prefix": {
          "type": "string",
          "description": "The source location prefix to use. This is only available for successful analyses."
        },
        "artifact_url": {
          "type": "string",
          "description": "The URL of the artifact. This is only available for successful analyses."
        }
      },
      "required": [
        "repository",
        "analysis_status"
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
    "code-of-conduct-simple": {
      "title": "Code Of Conduct Simple",
      "description": "Code of Conduct Simple",
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repos/github/docs/community/code_of_conduct"
          ]
        },
        "key": {
          "type": "string",
          "examples": [
            "citizen_code_of_conduct"
          ]
        },
        "name": {
          "type": "string",
          "examples": [
            "Citizen Code of Conduct"
          ]
        },
        "html_url": {
          "type": [
            "string",
            "null"
          ],
          "format": "uri",
          "examples": [
            "https://github.com/github/docs/blob/main/CODE_OF_CONDUCT.md"
          ]
        }
      },
      "required": [
        "url",
        "key",
        "name",
        "html_url"
      ]
    },
    "code-scanning-variant-analysis-status": {
      "type": "string",
      "description": "The new status of the CodeQL variant analysis repository task.",
      "enum": [
        "pending",
        "in_progress",
        "succeeded",
        "failed",
        "canceled",
        "timed_out"
      ]
    },
    "simple-repository": {
      "title": "Simple Repository",
      "description": "A GitHub repository.",
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "format": "int64",
          "description": "A unique identifier of the repository.",
          "examples": [
            1296269
          ]
        },
        "node_id": {
          "type": "string",
          "description": "The GraphQL identifier of the repository.",
          "examples": [
            "MDEwOlJlcG9zaXRvcnkxMjk2MjY5"
          ]
        },
        "name": {
          "type": "string",
          "description": "The name of the repository.",
          "examples": [
            "Hello-World"
          ]
        },
        "full_name": {
          "type": "string",
          "description": "The full, globally unique, name of the repository.",
          "examples": [
            "octocat/Hello-World"
          ]
        },
        "owner": {
          "$ref": "#/components/schemas/simple-user"
        },
        "private": {
          "type": "boolean",
          "description": "Whether the repository is private."
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "description": "The URL to view the repository on GitHub.com.",
          "examples": [
            "https://github.com/octocat/Hello-World"
          ]
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "description": "The repository description.",
          "examples": [
            "This your first repo!"
          ]
        },
        "fork": {
          "type": "boolean",
          "description": "Whether the repository is a fork."
        },
        "url": {
          "type": "string",
          "format": "uri",
          "description": "The URL to get more information about the repository from the GitHub API.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World"
          ]
        },
        "archive_url": {
          "type": "string",
          "description": "A template for the API URL to download the repository as an archive.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}"
          ]
        },
        "assignees_url": {
          "type": "string",
          "description": "A template for the API URL to list the available assignees for issues in the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/assignees{/user}"
          ]
        },
        "blobs_url": {
          "type": "string",
          "description": "A template for the API URL to create or retrieve a raw Git blob in the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}"
          ]
        },
        "branches_url": {
          "type": "string",
          "description": "A template for the API URL to get information about branches in the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/branches{/branch}"
          ]
        },
        "collaborators_url": {
          "type": "string",
          "description": "A template for the API URL to get information about collaborators of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}"
          ]
        },
        "comments_url": {
          "type": "string",
          "description": "A template for the API URL to get information about comments on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/comments{/number}"
          ]
        },
        "commits_url": {
          "type": "string",
          "description": "A template for the API URL to get information about commits on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/commits{/sha}"
          ]
        },
        "compare_url": {
          "type": "string",
          "description": "A template for the API URL to compare two commits or refs.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}"
          ]
        },
        "contents_url": {
          "type": "string",
          "description": "A template for the API URL to get the contents of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/contents/{+path}"
          ]
        },
        "contributors_url": {
          "type": "string",
          "format": "uri",
          "description": "A template for the API URL to list the contributors to the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/contributors"
          ]
        },
        "deployments_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to list the deployments of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/deployments"
          ]
        },
        "downloads_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to list the downloads on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/downloads"
          ]
        },
        "events_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to list the events of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/events"
          ]
        },
        "forks_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to list the forks of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/forks"
          ]
        },
        "git_commits_url": {
          "type": "string",
          "description": "A template for the API URL to get information about Git commits of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}"
          ]
        },
        "git_refs_url": {
          "type": "string",
          "description": "A template for the API URL to get information about Git refs of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}"
          ]
        },
        "git_tags_url": {
          "type": "string",
          "description": "A template for the API URL to get information about Git tags of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}"
          ]
        },
        "issue_comment_url": {
          "type": "string",
          "description": "A template for the API URL to get information about issue comments on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}"
          ]
        },
        "issue_events_url": {
          "type": "string",
          "description": "A template for the API URL to get information about issue events on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}"
          ]
        },
        "issues_url": {
          "type": "string",
          "description": "A template for the API URL to get information about issues on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/issues{/number}"
          ]
        },
        "keys_url": {
          "type": "string",
          "description": "A template for the API URL to get information about deploy keys on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}"
          ]
        },
        "labels_url": {
          "type": "string",
          "description": "A template for the API URL to get information about labels of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/labels{/name}"
          ]
        },
        "languages_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to get information about the languages of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/languages"
          ]
        },
        "merges_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to merge branches in the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/merges"
          ]
        },
        "milestones_url": {
          "type": "string",
          "description": "A template for the API URL to get information about milestones of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/milestones{/number}"
          ]
        },
        "notifications_url": {
          "type": "string",
          "description": "A template for the API URL to get information about notifications on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}"
          ]
        },
        "pulls_url": {
          "type": "string",
          "description": "A template for the API URL to get information about pull requests on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/pulls{/number}"
          ]
        },
        "releases_url": {
          "type": "string",
          "description": "A template for the API URL to get information about releases on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/releases{/id}"
          ]
        },
        "stargazers_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to list the stargazers on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/stargazers"
          ]
        },
        "statuses_url": {
          "type": "string",
          "description": "A template for the API URL to get information about statuses of a commit.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}"
          ]
        },
        "subscribers_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to list the subscribers on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/subscribers"
          ]
        },
        "subscription_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to subscribe to notifications for this repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/subscription"
          ]
        },
        "tags_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to get information about tags on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/tags"
          ]
        },
        "teams_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to list the teams on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/teams"
          ]
        },
        "trees_url": {
          "type": "string",
          "description": "A template for the API URL to create or retrieve a raw Git tree of the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}"
          ]
        },
        "hooks_url": {
          "type": "string",
          "format": "uri",
          "description": "The API URL to list the hooks on the repository.",
          "examples": [
            "https://api.github.com/repos/octocat/Hello-World/hooks"
          ]
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
        "url"
      ]
    },
    "full-repository": {
      "title": "Full Repository",
      "description": "Full Repository",
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "format": "int64",
          "examples": [
            1296269
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDEwOlJlcG9zaXRvcnkxMjk2MjY5"
          ]
        },
        "name": {
          "type": "string",
          "examples": [
            "Hello-World"
          ]
        },
        "full_name": {
          "type": "string",
          "examples": [
            "octocat/Hello-World"
          ]
        },
        "owner": {
          "$ref": "#/components/schemas/simple-user"
        },
        "private": {
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
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "topics": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "examples": [
            "octocat",
            "atom",
            "electron",
            "API"
          ]
        },
        "has_issues": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_projects": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_wiki": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_pages": {
          "type": "boolean"
        },
        "has_discussions": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "has_pull_requests": {
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
          "type": "boolean"
        },
        "disabled": {
          "type": "boolean",
          "description": "Returns whether or not this repository disabled."
        },
        "visibility": {
          "description": "The repository visibility: public, private, or internal.",
          "type": "string",
          "examples": [
            "public"
          ]
        },
        "pushed_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2011-01-26T19:06:43Z"
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
            "2011-01-26T19:14:43Z"
          ]
        },
        "permissions": {
          "type": "object",
          "properties": {
            "admin": {
              "type": "boolean"
            },
            "maintain": {
              "type": "boolean"
            },
            "push": {
              "type": "boolean"
            },
            "triage": {
              "type": "boolean"
            },
            "pull": {
              "type": "boolean"
            }
          },
          "required": [
            "admin",
            "pull",
            "push"
          ]
        },
        "allow_rebase_merge": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "template_repository": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/repository"
            }
          ]
        },
        "temp_clone_token": {
          "type": [
            "string",
            "null"
          ]
        },
        "allow_squash_merge": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "allow_auto_merge": {
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "delete_branch_on_merge": {
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "allow_merge_commit": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "allow_update_branch": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "squash_merge_commit_title": {
          "type": "string",
          "enum": [
            "PR_TITLE",
            "COMMIT_OR_PR_TITLE"
          ],
          "description": "The default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit).",
          "examples": [
            "PR_TITLE"
          ]
        },
        "squash_merge_commit_message": {
          "type": "string",
          "enum": [
            "PR_BODY",
            "COMMIT_MESSAGES",
            "BLANK"
          ],
          "description": "The default value for a squash merge commit message:\n\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message.",
          "examples": [
            "PR_BODY"
          ]
        },
        "merge_commit_title": {
          "type": "string",
          "enum": [
            "PR_TITLE",
            "MERGE_MESSAGE"
          ],
          "description": "The default value for a merge commit title.\n\n  - `PR_TITLE` - default to the pull request's title.\n  - `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).",
          "examples": [
            "PR_TITLE"
          ]
        },
        "merge_commit_message": {
          "type": "string",
          "enum": [
            "PR_BODY",
            "PR_TITLE",
            "BLANK"
          ],
          "description": "The default value for a merge commit message.\n\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message.",
          "examples": [
            "PR_BODY"
          ]
        },
        "allow_forking": {
          "type": "boolean",
          "examples": [
            true
          ]
        },
        "web_commit_signoff_required": {
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "subscribers_count": {
          "type": "integer",
          "examples": [
            42
          ]
        },
        "network_count": {
          "type": "integer",
          "examples": [
            0
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
        "organization": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/simple-user"
            }
          ]
        },
        "parent": {
          "$ref": "#/components/schemas/repository"
        },
        "source": {
          "$ref": "#/components/schemas/repository"
        },
        "forks": {
          "type": "integer"
        },
        "master_branch": {
          "type": "string"
        },
        "open_issues": {
          "type": "integer"
        },
        "watchers": {
          "type": "integer"
        },
        "anonymous_access_enabled": {
          "description": "Whether anonymous git access is allowed.",
          "default": true,
          "type": "boolean"
        },
        "code_of_conduct": {
          "$ref": "#/components/schemas/code-of-conduct-simple"
        },
        "security_and_analysis": {
          "$ref": "#/components/schemas/security-and-analysis"
        },
        "custom_properties": {
          "type": "object",
          "description": "The custom properties that were defined for the repository. The keys are the custom property names, and the values are the corresponding custom property values.",
          "additionalProperties": true
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
        "has_discussions",
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
        "updated_at",
        "network_count",
        "subscribers_count"
      ]
    },
    "minimal-repository": {
      "title": "Minimal Repository",
      "description": "Minimal Repository",
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "format": "int64",
          "examples": [
            1296269
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDEwOlJlcG9zaXRvcnkxMjk2MjY5"
          ]
        },
        "name": {
          "type": "string",
          "examples": [
            "Hello-World"
          ]
        },
        "full_name": {
          "type": "string",
          "examples": [
            "octocat/Hello-World"
          ]
        },
        "owner": {
          "$ref": "#/components/schemas/simple-user"
        },
        "private": {
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
          "type": "string"
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
          "type": "string"
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
          "type": "string"
        },
        "mirror_url": {
          "type": [
            "string",
            "null"
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
          "type": "string"
        },
        "homepage": {
          "type": [
            "string",
            "null"
          ]
        },
        "language": {
          "type": [
            "string",
            "null"
          ]
        },
        "forks_count": {
          "type": "integer"
        },
        "stargazers_count": {
          "type": "integer"
        },
        "watchers_count": {
          "type": "integer"
        },
        "size": {
          "description": "The size of the repository, in kilobytes. Size is calculated hourly. When a repository is initially created, the size is 0.",
          "type": "integer"
        },
        "default_branch": {
          "type": "string"
        },
        "open_issues_count": {
          "type": "integer"
        },
        "is_template": {
          "type": "boolean"
        },
        "topics": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "has_issues": {
          "type": "boolean"
        },
        "has_projects": {
          "type": "boolean"
        },
        "has_wiki": {
          "type": "boolean"
        },
        "has_pages": {
          "type": "boolean"
        },
        "has_discussions": {
          "type": "boolean"
        },
        "has_pull_requests": {
          "type": "boolean"
        },
        "pull_request_creation_policy": {
          "description": "The policy controlling who can create pull requests: all or collaborators_only.",
          "type": "string",
          "enum": [
            "all",
            "collaborators_only"
          ]
        },
        "archived": {
          "type": "boolean"
        },
        "disabled": {
          "type": "boolean"
        },
        "visibility": {
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
        "permissions": {
          "type": "object",
          "properties": {
            "admin": {
              "type": "boolean"
            },
            "maintain": {
              "type": "boolean"
            },
            "push": {
              "type": "boolean"
            },
            "triage": {
              "type": "boolean"
            },
            "pull": {
              "type": "boolean"
            }
          }
        },
        "role_name": {
          "type": "string",
          "examples": [
            "admin"
          ]
        },
        "temp_clone_token": {
          "type": "string"
        },
        "delete_branch_on_merge": {
          "type": "boolean"
        },
        "subscribers_count": {
          "type": "integer"
        },
        "network_count": {
          "type": "integer"
        },
        "code_of_conduct": {
          "$ref": "#/components/schemas/code-of-conduct"
        },
        "license": {
          "type": [
            "object",
            "null"
          ],
          "properties": {
            "key": {
              "type": "string"
            },
            "name": {
              "type": "string"
            },
            "spdx_id": {
              "type": "string"
            },
            "url": {
              "type": [
                "string",
                "null"
              ]
            },
            "node_id": {
              "type": "string"
            }
          }
        },
        "forks": {
          "type": "integer",
          "examples": [
            0
          ]
        },
        "open_issues": {
          "type": "integer",
          "examples": [
            0
          ]
        },
        "watchers": {
          "type": "integer",
          "examples": [
            0
          ]
        },
        "allow_forking": {
          "type": "boolean"
        },
        "web_commit_signoff_required": {
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "security_and_analysis": {
          "$ref": "#/components/schemas/security-and-analysis"
        },
        "custom_properties": {
          "type": "object",
          "description": "The custom properties that were defined for the repository. The keys are the custom property names, and the values are the corresponding custom property values.",
          "additionalProperties": true
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
        "url"
      ]
    },
    "code-of-conduct": {
      "title": "Code Of Conduct",
      "description": "Code Of Conduct",
      "type": "object",
      "properties": {
        "key": {
          "type": "string",
          "examples": [
            "contributor_covenant"
          ]
        },
        "name": {
          "type": "string",
          "examples": [
            "Contributor Covenant"
          ]
        },
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/codes_of_conduct/contributor_covenant"
          ]
        },
        "body": {
          "type": "string",
          "examples": [
            "# Contributor Covenant Code of Conduct\n\n## Our Pledge\n\nIn the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.\n\n## Our Standards\n\nExamples of behavior that contributes to creating a positive environment include:\n\n* Using welcoming and inclusive language\n* Being respectful of differing viewpoints and experiences\n* Gracefully accepting constructive criticism\n* Focusing on what is best for the community\n* Showing empathy towards other community members\n\nExamples of unacceptable behavior by participants include:\n\n* The use of sexualized language or imagery and unwelcome sexual attention or advances\n* Trolling, insulting/derogatory comments, and personal or political attacks\n* Public or private harassment\n* Publishing others' private information, such as a physical or electronic address, without explicit permission\n* Other conduct which could reasonably be considered inappropriate in a professional setting\n\n## Our Responsibilities\n\nProject maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response\n                  to any instances of unacceptable behavior.\n\nProject maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.\n\n## Scope\n\nThis Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project e-mail address,\n                  posting via an official social media account, or acting as an appointed representative at an online or offline event. Representation of a project may be further defined and clarified by project maintainers.\n\n## Enforcement\n\nInstances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at [EMAIL]. The project team will review and investigate all complaints, and will respond in a way that it deems appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident. Further details of specific enforcement policies may be posted separately.\n\nProject maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.\n\n## Attribution\n\nThis Code of Conduct is adapted from the [Contributor Covenant](http://contributor-covenant.org), version 1.4, available at [http://contributor-covenant.org/version/1/4](http://contributor-covenant.org/version/1/4/).\n"
          ]
        },
        "html_url": {
          "type": [
            "string",
            "null"
          ],
          "format": "uri"
        }
      },
      "required": [
        "url",
        "html_url",
        "key",
        "name"
      ]
    },
    "security-and-analysis": {
      "type": [
        "object",
        "null"
      ],
      "properties": {
        "advanced_security": {
          "description": "Enable or disable GitHub Advanced Security for the repository.\n\nFor standalone Code Scanning or Secret Protection products, this parameter cannot be used.\n",
          "type": "object",
          "properties": {
            "status": {
              "type": "string",
              "enum": [
                "enabled",
                "disabled"
              ]
            }
          }
        },
        "code_security": {
          "type": "object",
          "properties": {
            "status": {
              "type": "string",
              "enum": [
                "enabled",
                "disabled"
              ]
            }
          }
        },
        "dependabot_security_updates": {
          "description": "Enable or disable Dependabot security updates for the repository.",
          "type": "object",
          "properties": {
            "status": {
              "description": "The enablement status of Dependabot security updates for the repository.",
              "type": "string",
              "enum": [
                "enabled",
                "disabled"
              ]
            }
          }
        },
        "secret_scanning": {
          "type": "object",
          "properties": {
            "status": {
              "type": "string",
              "enum": [
                "enabled",
                "disabled"
              ]
            }
          }
        },
        "secret_scanning_push_protection": {
          "type": "object",
          "properties": {
            "status": {
              "type": "string",
              "enum": [
                "enabled",
                "disabled"
              ]
            }
          }
        },
        "secret_scanning_non_provider_patterns": {
          "type": "object",
          "properties": {
            "status": {
              "type": "string",
              "enum": [
                "enabled",
                "disabled"
              ]
            }
          }
        },
        "secret_scanning_ai_detection": {
          "type": "object",
          "properties": {
            "status": {
              "type": "string",
              "enum": [
                "enabled",
                "disabled"
              ]
            }
          }
        },
        "secret_scanning_delegated_alert_dismissal": {
          "type": "object",
          "properties": {
            "status": {
              "type": "string",
              "enum": [
                "enabled",
                "disabled"
              ]
            }
          }
        },
        "secret_scanning_delegated_bypass": {
          "type": "object",
          "properties": {
            "status": {
              "type": "string",
              "enum": [
                "enabled",
                "disabled"
              ]
            }
          }
        },
        "secret_scanning_delegated_bypass_options": {
          "type": "object",
          "properties": {
            "reviewers": {
              "type": "array",
              "description": "The bypass reviewers for secret scanning delegated bypass",
              "items": {
                "type": "object",
                "required": [
                  "reviewer_id",
                  "reviewer_type"
                ],
                "properties": {
                  "reviewer_id": {
                    "type": "integer",
                    "description": "The ID of the team or role selected as a bypass reviewer"
                  },
                  "reviewer_type": {
                    "type": "string",
                    "description": "The type of the bypass reviewer",
                    "enum": [
                      "TEAM",
                      "ROLE"
                    ]
                  },
                  "mode": {
                    "type": "string",
                    "description": "The bypass mode for the reviewer",
                    "enum": [
                      "ALWAYS",
                      "EXEMPT"
                    ],
                    "default": "ALWAYS"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
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
}
```

### Relationship manifest

```yaml
github_repos:
  team_id:
    target_table: github_teams
    target_column: id
    confidence: high
    reason: 'request body on POST /orgs/{org}/repos: team_id'

```

### FK dependency schemas (for stub creation if needed)

```json
{
  "teams": {
    "primary_response_schema": {
      "title": "Enterprise Team",
      "description": "Group of enterprise owners and/or members",
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "format": "int64"
        },
        "name": {
          "type": "string"
        },
        "description": {
          "type": "string"
        },
        "slug": {
          "type": "string"
        },
        "url": {
          "type": "string",
          "format": "uri"
        },
        "sync_to_organizations": {
          "type": "string",
          "description": "Retired: this field will not be returned with GHEC enterprise teams.",
          "examples": [
            "disabled | all"
          ]
        },
        "organization_selection_type": {
          "type": "string",
          "examples": [
            "disabled | selected | all"
          ]
        },
        "group_id": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "62ab9291-fae2-468e-974b-7e45096d5021"
          ]
        },
        "group_name": {
          "type": [
            "string",
            "null"
          ],
          "description": "Retired: this field will not be returned with GHEC enterprise teams.",
          "examples": [
            "Justice League"
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/enterprises/dc/teams/justice-league"
          ]
        },
        "members_url": {
          "type": "string"
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        }
      },
      "required": [
        "id",
        "url",
        "members_url",
        "name",
        "html_url",
        "slug",
        "created_at",
        "updated_at",
        "group_id"
      ]
    }
  }
}
```

### ID format

Resource `repo` uses: alphabet=NUMERIC, length=2

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

Add a class `Repo(Base)` with:

- Table name: `github_repos`
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
