# Entity Implementation: orgs

You are implementing the **orgs** resource for the GitHub API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for orgs

```json
{
  "paths": {
    "/orgs/{org}": {
      "get": {
        "summary": "Get an organization",
        "description": "Gets information about an organization.\n\nWhen the value of `two_factor_requirement_enabled` is `true`, the organization requires all members, billing managers, outside collaborators, guest collaborators, repository collaborators, or everyone with access to any repository within the organization to enable [two-factor authentication](https://docs.github.com/articles/securing-your-account-with-two-factor-authentication-2fa/).\n\nTo see the full details about an organization, the authenticated user must be an organization owner.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` scope to see the full details about an organization.\n\nTo see information about an organization's GitHub plan, GitHub Apps need the `Organization plan` permission.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/get",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/orgs#get-an-organization"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/organization-full"
                },
                "examples": {
                  "default-response": {
                    "$ref": "#/components/examples/organization-full"
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
          "category": "orgs",
          "subcategory": "orgs"
        }
      },
      "patch": {
        "summary": "Update an organization",
        "description": "> [!WARNING]\n> **Closing down notice:** GitHub will replace and discontinue `members_allowed_repository_creation_type` in favor of more granular permissions. The new input parameters are `members_can_create_public_repositories`, `members_can_create_private_repositories` for all organizations and `members_can_create_internal_repositories` for organizations associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+. For more information, see the [blog post](https://developer.github.com/changes/2019-12-03-internal-visibility-changes).\n\n> [!WARNING]\n> **Closing down notice:** Code security product enablement for new repositories through the organization API is closing down. Please use [code security configurations](https://docs.github.com/rest/code-security/configurations#set-a-code-security-configuration-as-a-default-for-an-organization) to set defaults instead. For more information on setting a default security configuration, see the [changelog](https://github.blog/changelog/2024-07-09-sunsetting-security-settings-defaults-parameters-in-the-organizations-rest-api/).\n\nUpdates the organization's profile and member privileges.\n\nThe authenticated user must be an organization owner to use this endpoint.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` or `repo` scope to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/update",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/orgs#update-an-organization"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          }
        ],
        "requestBody": {
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "billing_email": {
                    "type": "string",
                    "description": "Billing email address. This address is not publicized."
                  },
                  "company": {
                    "type": "string",
                    "description": "The company name."
                  },
                  "email": {
                    "type": "string",
                    "description": "The publicly visible email address."
                  },
                  "twitter_username": {
                    "type": "string",
                    "description": "The Twitter username of the company."
                  },
                  "location": {
                    "type": "string",
                    "description": "The location."
                  },
                  "name": {
                    "type": "string",
                    "description": "The shorthand name of the company."
                  },
                  "description": {
                    "type": "string",
                    "description": "The description of the company. The maximum size is 160 characters."
                  },
                  "has_organization_projects": {
                    "type": "boolean",
                    "description": "Whether an organization can use organization projects."
                  },
                  "has_repository_projects": {
                    "type": "boolean",
                    "description": "Whether repositories that belong to the organization can use repository projects."
                  },
                  "default_repository_permission": {
                    "type": "string",
                    "description": "Default permission level members have for organization repositories.",
                    "enum": [
                      "read",
                      "write",
                      "admin",
                      "none"
                    ],
                    "default": "read"
                  },
                  "members_can_create_repositories": {
                    "type": "boolean",
                    "description": "Whether of non-admin organization members can create repositories. **Note:** A parameter can override this parameter. See `members_allowed_repository_creation_type` in this table for details.",
                    "default": true
                  },
                  "members_can_create_internal_repositories": {
                    "type": "boolean",
                    "description": "Whether organization members can create internal repositories, which are visible to all enterprise members. You can only allow members to create internal repositories if your organization is associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+. For more information, see \"[Restricting repository creation in your organization](https://docs.github.com/github/setting-up-and-managing-organizations-and-teams/restricting-repository-creation-in-your-organization)\" in the GitHub Help documentation."
                  },
                  "members_can_create_private_repositories": {
                    "type": "boolean",
                    "description": "Whether organization members can create private repositories, which are visible to organization members with permission. For more information, see \"[Restricting repository creation in your organization](https://docs.github.com/github/setting-up-and-managing-organizations-and-teams/restricting-repository-creation-in-your-organization)\" in the GitHub Help documentation."
                  },
                  "members_can_create_public_repositories": {
                    "type": "boolean",
                    "description": "Whether organization members can create public repositories, which are visible to anyone. For more information, see \"[Restricting repository creation in your organization](https://docs.github.com/github/setting-up-and-managing-organizations-and-teams/restricting-repository-creation-in-your-organization)\" in the GitHub Help documentation."
                  },
                  "members_allowed_repository_creation_type": {
                    "type": "string",
                    "description": "Specifies which types of repositories non-admin organization members can create. `private` is only available to repositories that are part of an organization on GitHub Enterprise Cloud. \n**Note:** This parameter is closing down and will be removed in the future. Its return value ignores internal repositories. Using this parameter overrides values set in `members_can_create_repositories`. See the parameter deprecation notice in the operation description for details.",
                    "enum": [
                      "all",
                      "private",
                      "none"
                    ]
                  },
                  "members_can_create_pages": {
                    "type": "boolean",
                    "description": "Whether organization members can create GitHub Pages sites. Existing published sites will not be impacted.",
                    "default": true
                  },
                  "members_can_create_public_pages": {
                    "type": "boolean",
                    "description": "Whether organization members can create public GitHub Pages sites. Existing published sites will not be impacted.",
                    "default": true
                  },
                  "members_can_create_private_pages": {
                    "type": "boolean",
                    "description": "Whether organization members can create private GitHub Pages sites. Existing published sites will not be impacted.",
                    "default": true
                  },
                  "members_can_fork_private_repositories": {
                    "type": "boolean",
                    "description": "Whether organization members can fork private organization repositories.",
                    "default": false
                  },
                  "web_commit_signoff_required": {
                    "type": "boolean",
                    "description": "Whether contributors to organization repositories are required to sign off on commits they make through GitHub's web interface.",
                    "default": false
                  },
                  "blog": {
                    "type": "string",
                    "examples": [
                      "\"http://github.blog\""
                    ]
                  },
                  "advanced_security_enabled_for_new_repositories": {
                    "type": "boolean",
                    "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether GitHub Advanced Security is automatically enabled for new repositories and repositories transferred to this organization.\n\nTo use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"\n\nYou can check which security and analysis features are currently enabled by using a `GET /orgs/{org}` request.",
                    "deprecated": true
                  },
                  "dependabot_alerts_enabled_for_new_repositories": {
                    "type": "boolean",
                    "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether Dependabot alerts are automatically enabled for new repositories and repositories transferred to this organization.\n\nTo use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"\n\nYou can check which security and analysis features are currently enabled by using a `GET /orgs/{org}` request.",
                    "deprecated": true
                  },
                  "dependabot_security_updates_enabled_for_new_repositories": {
                    "type": "boolean",
                    "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether Dependabot security updates are automatically enabled for new repositories and repositories transferred to this organization.\n\nTo use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"\n\nYou can check which security and analysis features are currently enabled by using a `GET /orgs/{org}` request.",
                    "deprecated": true
                  },
                  "dependency_graph_enabled_for_new_repositories": {
                    "type": "boolean",
                    "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether dependency graph is automatically enabled for new repositories and repositories transferred to this organization.\n\nTo use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"\n\nYou can check which security and analysis features are currently enabled by using a `GET /orgs/{org}` request.",
                    "deprecated": true
                  },
                  "secret_scanning_enabled_for_new_repositories": {
                    "type": "boolean",
                    "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether secret scanning is automatically enabled for new repositories and repositories transferred to this organization.\n\nTo use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"\n\nYou can check which security and analysis features are currently enabled by using a `GET /orgs/{org}` request.",
                    "deprecated": true
                  },
                  "secret_scanning_push_protection_enabled_for_new_repositories": {
                    "type": "boolean",
                    "description": "**Endpoint closing down notice.** Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead.\n\nWhether secret scanning push protection is automatically enabled for new repositories and repositories transferred to this organization.\n\nTo use this parameter, you must have admin permissions for the repository or be an owner or security manager for the organization that owns the repository. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"\n\nYou can check which security and analysis features are currently enabled by using a `GET /orgs/{org}` request.",
                    "deprecated": true
                  },
                  "secret_scanning_push_protection_custom_link": {
                    "type": "string",
                    "description": "If `secret_scanning_push_protection_custom_link_enabled` is true, the URL that will be displayed to contributors who are blocked from pushing a secret."
                  },
                  "deploy_keys_enabled_for_repositories": {
                    "type": "boolean",
                    "description": "Controls whether or not deploy keys may be added and used for repositories in the organization."
                  }
                }
              },
              "examples": {
                "default": {
                  "value": {
                    "billing_email": "mona@github.com",
                    "company": "GitHub",
                    "email": "mona@github.com",
                    "twitter_username": "github",
                    "location": "San Francisco",
                    "name": "github",
                    "description": "GitHub, the company.",
                    "default_repository_permission": "read",
                    "members_can_create_repositories": true,
                    "members_allowed_repository_creation_type": "all"
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
                  "$ref": "#/components/schemas/organization-full"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/organization-full"
                  }
                }
              }
            }
          },
          "422": {
            "description": "Validation failed",
            "content": {
              "application/json": {
                "schema": {
                  "oneOf": [
                    {
                      "$ref": "#/components/schemas/validation-error"
                    },
                    {
                      "$ref": "#/components/schemas/validation-error-simple"
                    }
                  ]
                }
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
          "category": "orgs",
          "subcategory": "orgs"
        }
      },
      "delete": {
        "summary": "Delete an organization",
        "description": "Deletes an organization and all its repositories.\n\nThe organization login will be unavailable for 90 days after deletion.\n\nPlease review the Terms of Service regarding account deletion before using this endpoint:\n\nhttps://docs.github.com/site-policy/github-terms/github-terms-of-service",
        "operationId": "orgs/delete",
        "tags": [
          "orgs"
        ],
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/orgs#delete-an-organization"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          }
        ],
        "responses": {
          "202": {
            "$ref": "#/components/responses/accepted"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "451": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "orgs"
        }
      }
    },
    "/orgs/{org}/{security_product}/{enablement}": {
      "post": {
        "summary": "Enable or disable a security feature for an organization",
        "description": "> [!WARNING]\n> **Closing down notice:** The ability to enable or disable a security feature for all eligible repositories in an organization is closing down. Please use [code security configurations](https://docs.github.com/rest/code-security/configurations) instead. For more information, see the [changelog](https://github.blog/changelog/2024-07-22-deprecation-of-api-endpoint-to-enable-or-disable-a-security-feature-for-an-organization/).\n\nEnables or disables the specified security feature for all eligible repositories in an organization. For more information, see \"[Managing security managers in your organization](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization).\"\n\nThe authenticated user must be an organization owner or be member of a team with the security manager role to use this endpoint.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org`, `write:org`, or `repo` scopes to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/enable-or-disable-security-product-on-all-org-repos",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/orgs#enable-or-disable-a-security-feature-for-an-organization"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/security-product"
          },
          {
            "$ref": "#/components/parameters/org-security-product-enablement"
          }
        ],
        "requestBody": {
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "properties": {
                  "query_suite": {
                    "description": "CodeQL query suite to be used. If you specify the `query_suite` parameter, the default setup will be configured with this query suite only on all repositories that didn't have default setup already configured. It will not change the query suite on repositories that already have default setup configured.\nIf you don't specify any `query_suite` in your request, the preferred query suite of the organization will be applied.",
                    "type": "string",
                    "enum": [
                      "default",
                      "extended"
                    ]
                  }
                }
              },
              "examples": {
                "default": {
                  "value": null
                }
              }
            }
          }
        },
        "responses": {
          "204": {
            "description": "Action started"
          },
          "422": {
            "description": "The action could not be taken due to an in progress enablement, or a policy is preventing enablement"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "previews": [],
          "category": "orgs",
          "subcategory": "orgs",
          "deprecationDate": "2024-07-22",
          "removalDate": "2025-07-22"
        },
        "deprecated": true
      }
    },
    "/user/memberships/orgs": {
      "get": {
        "summary": "List organization memberships for the authenticated user",
        "description": "Lists all of the authenticated user's organization memberships.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/list-memberships-for-authenticated-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/members#list-organization-memberships-for-the-authenticated-user"
        },
        "parameters": [
          {
            "name": "state",
            "description": "Indicates the state of the memberships to return. If not specified, the API returns both active and pending memberships.",
            "in": "query",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "active",
                "pending"
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
                    "$ref": "#/components/schemas/org-membership"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/org-membership-items"
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
          "403": {
            "$ref": "#/components/responses/forbidden"
          },
          "401": {
            "$ref": "#/components/responses/requires_authentication"
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "members"
        }
      }
    },
    "/user/memberships/orgs/{org}": {
      "get": {
        "summary": "Get an organization membership for the authenticated user",
        "description": "If the authenticated user is an active or pending member of the organization, this endpoint will return the user's membership. If the authenticated user is not affiliated with the organization, a `404` is returned. This endpoint will return a `403` if the request is made by a GitHub App that is blocked by the organization.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/get-membership-for-authenticated-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/members#get-an-organization-membership-for-the-authenticated-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/org-membership"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/org-membership"
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
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "members"
        }
      },
      "patch": {
        "summary": "Update an organization membership for the authenticated user",
        "description": "Converts the authenticated user to an active member of the organization, if that user has a pending invitation from the organization.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/update-membership-for-authenticated-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/members#update-an-organization-membership-for-the-authenticated-user"
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
                  "state": {
                    "type": "string",
                    "description": "The state that the membership should be in. Only `\"active\"` will be accepted.",
                    "enum": [
                      "active"
                    ]
                  }
                },
                "required": [
                  "state"
                ]
              },
              "examples": {
                "default": {
                  "value": {
                    "state": "active"
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
                  "$ref": "#/components/schemas/org-membership"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/org-membership-2"
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
          "422": {
            "$ref": "#/components/responses/validation_failed"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "orgs",
          "subcategory": "members"
        }
      }
    },
    "/user/orgs": {
      "get": {
        "summary": "List organizations for the authenticated user",
        "description": "List organizations for the authenticated user.\n\nFor OAuth app tokens and personal access tokens (classic), this endpoint only lists organizations that your authorization allows you to operate on in some way (e.g., you can list teams with `read:org` scope, you can publicize your organization membership with `user` scope, etc.). Therefore, this API requires at least `user` or `read:org` scope for OAuth app tokens and personal access tokens (classic). Requests with insufficient scope will receive a `403 Forbidden` response.\n\n> [!NOTE]\n> Requests using a fine-grained access token will receive a `200 Success` response with an empty list.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/list-for-authenticated-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/orgs#list-organizations-for-the-authenticated-user"
        },
        "parameters": [
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
                    "$ref": "#/components/schemas/organization-simple"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/organization-simple-items"
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
          "category": "orgs",
          "subcategory": "orgs"
        }
      }
    },
    "/users/{username}/events/orgs/{org}": {
      "get": {
        "summary": "List organization events for the authenticated user",
        "description": "This is the user's organization dashboard. You must be authenticated as the user to view this.\n\n> [!NOTE]\n> This API is not built to serve real-time use cases. Depending on the time of day, event latency can be anywhere from 30s to 6h.",
        "tags": [
          "activity"
        ],
        "operationId": "activity/list-org-events-for-authenticated-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/activity/events#list-organization-events-for-the-authenticated-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/username"
          },
          {
            "$ref": "#/components/parameters/org"
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
                    "$ref": "#/components/schemas/event"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/user-org-events-items"
                  }
                }
              }
            }
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "activity",
          "subcategory": "events"
        }
      }
    },
    "/users/{username}/orgs": {
      "get": {
        "summary": "List organizations for a user",
        "description": "List [public organization memberships](https://docs.github.com/articles/publicizing-or-concealing-organization-membership) for the specified user.\n\nThis method only lists _public_ memberships, regardless of authentication. If you need to fetch all of the organization memberships (public and private) for the authenticated user, use the [List organizations for the authenticated user](https://docs.github.com/rest/orgs/orgs#list-organizations-for-the-authenticated-user) API instead.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/list-for-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/orgs#list-organizations-for-a-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/username"
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
                    "$ref": "#/components/schemas/organization-simple"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/organization-simple-items"
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
          "category": "orgs",
          "subcategory": "orgs"
        }
      }
    }
  },
  "schemas": {
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
    "pull-request-minimal": {
      "title": "Pull Request Minimal",
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "format": "int64"
        },
        "number": {
          "type": "integer"
        },
        "url": {
          "type": "string"
        },
        "head": {
          "type": "object",
          "properties": {
            "ref": {
              "type": "string"
            },
            "sha": {
              "type": "string"
            },
            "repo": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer",
                  "format": "int64"
                },
                "url": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                }
              },
              "required": [
                "id",
                "url",
                "name"
              ]
            }
          },
          "required": [
            "ref",
            "sha",
            "repo"
          ]
        },
        "base": {
          "type": "object",
          "properties": {
            "ref": {
              "type": "string"
            },
            "sha": {
              "type": "string"
            },
            "repo": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "integer",
                  "format": "int64"
                },
                "url": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                }
              },
              "required": [
                "id",
                "url",
                "name"
              ]
            }
          },
          "required": [
            "ref",
            "sha",
            "repo"
          ]
        }
      },
      "required": [
        "id",
        "number",
        "url",
        "head",
        "base"
      ]
    },
    "pull-request-review-event": {
      "title": "PullRequestReviewEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "review": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "node_id": {
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
            },
            "body": {
              "type": "string"
            },
            "commit_id": {
              "type": "string"
            },
            "submitted_at": {
              "type": [
                "string",
                "null"
              ]
            },
            "state": {
              "type": "string"
            },
            "html_url": {
              "type": "string",
              "format": "uri"
            },
            "pull_request_url": {
              "type": "string",
              "format": "uri"
            },
            "_links": {
              "type": "object",
              "properties": {
                "html": {
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
                "pull_request": {
                  "type": "object",
                  "properties": {
                    "href": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "href"
                  ]
                }
              },
              "required": [
                "html",
                "pull_request"
              ]
            },
            "updated_at": {
              "type": "string"
            }
          }
        },
        "pull_request": {
          "$ref": "#/components/schemas/pull-request-minimal"
        }
      },
      "required": [
        "action",
        "review",
        "pull_request"
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
    "validation-error": {
      "title": "Validation Error",
      "description": "Validation Error",
      "type": "object",
      "required": [
        "message",
        "documentation_url"
      ],
      "properties": {
        "message": {
          "type": "string"
        },
        "documentation_url": {
          "type": "string"
        },
        "errors": {
          "type": "array",
          "items": {
            "type": "object",
            "required": [
              "code"
            ],
            "properties": {
              "resource": {
                "type": "string"
              },
              "field": {
                "type": "string"
              },
              "message": {
                "type": "string"
              },
              "code": {
                "type": "string"
              },
              "index": {
                "type": "integer"
              },
              "value": {
                "oneOf": [
                  {
                    "type": [
                      "string",
                      "null"
                    ]
                  },
                  {
                    "type": [
                      "integer",
                      "null"
                    ]
                  },
                  {
                    "type": [
                      "array",
                      "null"
                    ],
                    "items": {
                      "type": "string"
                    }
                  }
                ]
              }
            }
          }
        }
      }
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
    "validation-error-simple": {
      "title": "Validation Error Simple",
      "description": "Validation Error Simple",
      "type": "object",
      "required": [
        "message",
        "documentation_url"
      ],
      "properties": {
        "message": {
          "type": "string"
        },
        "documentation_url": {
          "type": "string"
        },
        "errors": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "create-event": {
      "title": "CreateEvent",
      "type": "object",
      "properties": {
        "ref": {
          "type": "string"
        },
        "ref_type": {
          "type": "string"
        },
        "full_ref": {
          "type": "string"
        },
        "master_branch": {
          "type": "string"
        },
        "description": {
          "type": [
            "string",
            "null"
          ]
        },
        "pusher_type": {
          "type": "string"
        }
      },
      "required": [
        "ref",
        "ref_type",
        "full_ref",
        "master_branch",
        "pusher_type"
      ]
    },
    "delete-event": {
      "title": "DeleteEvent",
      "type": "object",
      "properties": {
        "ref": {
          "type": "string"
        },
        "ref_type": {
          "type": "string"
        },
        "full_ref": {
          "type": "string"
        },
        "pusher_type": {
          "type": "string"
        }
      },
      "required": [
        "ref",
        "ref_type",
        "full_ref",
        "pusher_type"
      ]
    },
    "event": {
      "title": "Event",
      "description": "Event",
      "type": "object",
      "properties": {
        "id": {
          "type": "string"
        },
        "type": {
          "type": [
            "string",
            "null"
          ]
        },
        "actor": {
          "$ref": "#/components/schemas/actor"
        },
        "repo": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "url": {
              "type": "string",
              "format": "uri"
            }
          },
          "required": [
            "id",
            "name",
            "url"
          ]
        },
        "org": {
          "$ref": "#/components/schemas/actor"
        },
        "payload": {
          "oneOf": [
            {
              "$ref": "#/components/schemas/create-event"
            },
            {
              "$ref": "#/components/schemas/delete-event"
            },
            {
              "$ref": "#/components/schemas/discussion-event"
            },
            {
              "$ref": "#/components/schemas/issues-event"
            },
            {
              "$ref": "#/components/schemas/issue-comment-event"
            },
            {
              "$ref": "#/components/schemas/fork-event"
            },
            {
              "$ref": "#/components/schemas/gollum-event"
            },
            {
              "$ref": "#/components/schemas/member-event"
            },
            {
              "$ref": "#/components/schemas/public-event"
            },
            {
              "$ref": "#/components/schemas/push-event"
            },
            {
              "$ref": "#/components/schemas/pull-request-event"
            },
            {
              "$ref": "#/components/schemas/pull-request-review-comment-event"
            },
            {
              "$ref": "#/components/schemas/pull-request-review-event"
            },
            {
              "$ref": "#/components/schemas/commit-comment-event"
            },
            {
              "$ref": "#/components/schemas/release-event"
            },
            {
              "$ref": "#/components/schemas/watch-event"
            }
          ]
        },
        "public": {
          "type": "boolean"
        },
        "created_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time"
        }
      },
      "required": [
        "id",
        "type",
        "actor",
        "repo",
        "payload",
        "public",
        "created_at"
      ]
    },
    "issues-event": {
      "title": "IssuesEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "issue": {
          "$ref": "#/components/schemas/issue"
        },
        "assignee": {
          "$ref": "#/components/schemas/simple-user"
        },
        "assignees": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "label": {
          "$ref": "#/components/schemas/label"
        },
        "labels": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/label"
          }
        }
      },
      "required": [
        "action",
        "issue"
      ]
    },
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
    },
    "watch-event": {
      "title": "WatchEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        }
      },
      "required": [
        "action"
      ]
    },
    "release-asset": {
      "title": "Release Asset",
      "description": "Data related to a release.",
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri"
        },
        "browser_download_url": {
          "type": "string",
          "format": "uri"
        },
        "id": {
          "type": "integer"
        },
        "node_id": {
          "type": "string"
        },
        "name": {
          "description": "The file name of the asset.",
          "type": "string",
          "examples": [
            "Team Environment"
          ]
        },
        "label": {
          "type": [
            "string",
            "null"
          ]
        },
        "state": {
          "description": "State of the release asset.",
          "type": "string",
          "enum": [
            "uploaded",
            "open"
          ]
        },
        "content_type": {
          "type": "string"
        },
        "size": {
          "type": "integer"
        },
        "digest": {
          "type": [
            "string",
            "null"
          ]
        },
        "download_count": {
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
        "uploader": {
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
        "id",
        "name",
        "content_type",
        "size",
        "digest",
        "state",
        "url",
        "node_id",
        "download_count",
        "label",
        "uploader",
        "browser_download_url",
        "created_at",
        "updated_at"
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
    "label": {
      "title": "Label",
      "description": "Color-coded labels help you categorize and filter your issues (just like labels in Gmail).",
      "type": "object",
      "properties": {
        "id": {
          "description": "Unique identifier for the label.",
          "type": "integer",
          "format": "int64",
          "examples": [
            208045946
          ]
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDU6TGFiZWwyMDgwNDU5NDY="
          ]
        },
        "url": {
          "description": "URL for the label",
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/repositories/42/labels/bug"
          ]
        },
        "name": {
          "description": "The name of the label.",
          "type": "string",
          "examples": [
            "bug"
          ]
        },
        "description": {
          "description": "Optional description of the label, such as its purpose.",
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "Something isn't working"
          ]
        },
        "color": {
          "description": "6-character hex code, without the leading #, identifying the color",
          "type": "string",
          "examples": [
            "FFFFFF"
          ]
        },
        "default": {
          "description": "Whether this label comes by default in a new repository.",
          "type": "boolean",
          "examples": [
            true
          ]
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
    },
    "actor": {
      "title": "Actor",
      "description": "Actor",
      "type": "object",
      "properties": {
        "id": {
          "type": "integer"
        },
        "login": {
          "type": "string"
        },
        "display_login": {
          "type": "string"
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
        "avatar_url": {
          "type": "string",
          "format": "uri"
        }
      },
      "required": [
        "id",
        "login",
        "gravatar_id",
        "url",
        "avatar_url"
      ]
    },
    "issue-comment-event": {
      "title": "IssueCommentEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "issue": {
          "$ref": "#/components/schemas/issue"
        },
        "comment": {
          "$ref": "#/components/schemas/issue-comment"
        }
      },
      "required": [
        "action",
        "issue",
        "comment"
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
    "discussion-event": {
      "title": "DiscussionEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "discussion": {
          "$ref": "#/components/schemas/discussion"
        }
      },
      "required": [
        "action",
        "discussion"
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
    "org-membership": {
      "title": "Org Membership",
      "description": "Org Membership",
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/orgs/octocat/memberships/defunkt"
          ]
        },
        "state": {
          "type": "string",
          "description": "The state of the member in the organization. The `pending` state indicates the user has not yet accepted an invitation.",
          "enum": [
            "active",
            "pending"
          ],
          "examples": [
            "active"
          ]
        },
        "role": {
          "type": "string",
          "description": "The user's membership type in the organization.",
          "enum": [
            "admin",
            "member",
            "billing_manager"
          ],
          "examples": [
            "admin"
          ]
        },
        "direct_membership": {
          "type": "boolean",
          "description": "Whether the user has direct membership in the organization.",
          "examples": [
            true
          ]
        },
        "enterprise_teams_providing_indirect_membership": {
          "type": "array",
          "description": "The slugs of the enterprise teams providing the user with indirect membership in the organization.\nA limit of 100 enterprise team slugs is returned.",
          "maxItems": 100,
          "items": {
            "type": "string"
          },
          "examples": [
            "ent:team-one",
            "ent:team-two"
          ]
        },
        "organization_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/orgs/octocat"
          ]
        },
        "organization": {
          "$ref": "#/components/schemas/organization-simple"
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
        "permissions": {
          "type": "object",
          "properties": {
            "can_create_repository": {
              "type": "boolean"
            }
          },
          "required": [
            "can_create_repository"
          ]
        }
      },
      "required": [
        "state",
        "role",
        "organization_url",
        "url",
        "organization",
        "user"
      ]
    },
    "release": {
      "title": "Release",
      "description": "A release.",
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri"
        },
        "html_url": {
          "type": "string",
          "format": "uri"
        },
        "assets_url": {
          "type": "string",
          "format": "uri"
        },
        "upload_url": {
          "type": "string"
        },
        "tarball_url": {
          "type": [
            "string",
            "null"
          ],
          "format": "uri"
        },
        "zipball_url": {
          "type": [
            "string",
            "null"
          ],
          "format": "uri"
        },
        "id": {
          "type": "integer"
        },
        "node_id": {
          "type": "string"
        },
        "tag_name": {
          "description": "The name of the tag.",
          "type": "string",
          "examples": [
            "v1.0.0"
          ]
        },
        "target_commitish": {
          "description": "Specifies the commitish value that determines where the Git tag is created from.",
          "type": "string",
          "examples": [
            "master"
          ]
        },
        "name": {
          "type": [
            "string",
            "null"
          ]
        },
        "body": {
          "type": [
            "string",
            "null"
          ]
        },
        "draft": {
          "description": "true to create a draft (unpublished) release, false to create a published one.",
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "prerelease": {
          "description": "Whether to identify the release as a prerelease or a full release.",
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "immutable": {
          "description": "Whether or not the release is immutable.",
          "type": "boolean",
          "examples": [
            false
          ]
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "published_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time"
        },
        "updated_at": {
          "type": [
            "string",
            "null"
          ],
          "format": "date-time"
        },
        "author": {
          "$ref": "#/components/schemas/simple-user"
        },
        "assets": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/release-asset"
          }
        },
        "body_html": {
          "type": "string"
        },
        "body_text": {
          "type": "string"
        },
        "mentions_count": {
          "type": "integer"
        },
        "discussion_url": {
          "description": "The URL of the release discussion.",
          "type": "string",
          "format": "uri"
        },
        "reactions": {
          "$ref": "#/components/schemas/reaction-rollup"
        }
      },
      "required": [
        "assets_url",
        "upload_url",
        "tarball_url",
        "zipball_url",
        "created_at",
        "published_at",
        "draft",
        "id",
        "node_id",
        "author",
        "html_url",
        "name",
        "prerelease",
        "tag_name",
        "target_commitish",
        "assets",
        "url"
      ]
    },
    "commit-comment-event": {
      "title": "CommitCommentEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "comment": {
          "type": "object",
          "properties": {
            "html_url": {
              "type": "string",
              "format": "uri"
            },
            "url": {
              "type": "string",
              "format": "uri"
            },
            "id": {
              "type": "integer"
            },
            "node_id": {
              "type": "string"
            },
            "body": {
              "type": "string"
            },
            "path": {
              "type": [
                "string",
                "null"
              ]
            },
            "position": {
              "type": [
                "integer",
                "null"
              ]
            },
            "line": {
              "type": [
                "integer",
                "null"
              ]
            },
            "commit_id": {
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
            },
            "created_at": {
              "type": "string",
              "format": "date-time"
            },
            "updated_at": {
              "type": "string",
              "format": "date-time"
            },
            "reactions": {
              "$ref": "#/components/schemas/reaction-rollup"
            }
          }
        }
      },
      "required": [
        "action",
        "comment"
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
    "push-event": {
      "title": "PushEvent",
      "type": "object",
      "properties": {
        "repository_id": {
          "type": "integer"
        },
        "push_id": {
          "type": "integer"
        },
        "ref": {
          "type": "string"
        },
        "head": {
          "type": "string"
        },
        "before": {
          "type": "string"
        }
      },
      "required": [
        "repository_id",
        "push_id",
        "ref",
        "head",
        "before"
      ]
    },
    "public-event": {
      "title": "PublicEvent",
      "type": "object"
    },
    "organization-full": {
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
    "pull-request-event": {
      "title": "PullRequestEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "number": {
          "type": "integer"
        },
        "pull_request": {
          "$ref": "#/components/schemas/pull-request-minimal"
        },
        "assignee": {
          "$ref": "#/components/schemas/simple-user"
        },
        "assignees": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/simple-user"
          }
        },
        "label": {
          "$ref": "#/components/schemas/label"
        },
        "labels": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/label"
          }
        }
      },
      "required": [
        "action",
        "number",
        "pull_request"
      ]
    },
    "organization-simple": {
      "title": "Organization Simple",
      "description": "A GitHub organization.",
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
        "description"
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
    "pull-request-review-comment-event": {
      "title": "PullRequestReviewCommentEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "pull_request": {
          "$ref": "#/components/schemas/pull-request-minimal"
        },
        "comment": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "node_id": {
              "type": "string"
            },
            "url": {
              "type": "string",
              "format": "uri"
            },
            "pull_request_review_id": {
              "type": [
                "integer",
                "null"
              ]
            },
            "diff_hunk": {
              "type": "string"
            },
            "path": {
              "type": "string"
            },
            "position": {
              "type": [
                "integer",
                "null"
              ]
            },
            "original_position": {
              "type": "integer"
            },
            "subject_type": {
              "type": [
                "string",
                "null"
              ]
            },
            "commit_id": {
              "type": "string"
            },
            "user": {
              "title": "User",
              "type": [
                "object",
                "null"
              ],
              "properties": {
                "avatar_url": {
                  "type": "string",
                  "format": "uri"
                },
                "deleted": {
                  "type": "boolean"
                },
                "email": {
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "events_url": {
                  "type": "string",
                  "format": "uri-template"
                },
                "followers_url": {
                  "type": "string",
                  "format": "uri"
                },
                "following_url": {
                  "type": "string",
                  "format": "uri-template"
                },
                "gists_url": {
                  "type": "string",
                  "format": "uri-template"
                },
                "gravatar_id": {
                  "type": "string"
                },
                "html_url": {
                  "type": "string",
                  "format": "uri"
                },
                "id": {
                  "type": "integer",
                  "format": "int64"
                },
                "login": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "node_id": {
                  "type": "string"
                },
                "organizations_url": {
                  "type": "string",
                  "format": "uri"
                },
                "received_events_url": {
                  "type": "string",
                  "format": "uri"
                },
                "repos_url": {
                  "type": "string",
                  "format": "uri"
                },
                "site_admin": {
                  "type": "boolean"
                },
                "starred_url": {
                  "type": "string",
                  "format": "uri-template"
                },
                "subscriptions_url": {
                  "type": "string",
                  "format": "uri"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "Bot",
                    "User",
                    "Organization"
                  ]
                },
                "url": {
                  "type": "string",
                  "format": "uri"
                },
                "user_view_type": {
                  "type": "string"
                }
              }
            },
            "body": {
              "type": "string"
            },
            "created_at": {
              "type": "string",
              "format": "date-time"
            },
            "updated_at": {
              "type": "string",
              "format": "date-time"
            },
            "html_url": {
              "type": "string",
              "format": "uri"
            },
            "pull_request_url": {
              "type": "string",
              "format": "uri"
            },
            "_links": {
              "type": "object",
              "properties": {
                "html": {
                  "title": "Link",
                  "type": "object",
                  "properties": {
                    "href": {
                      "type": "string",
                      "format": "uri-template"
                    }
                  },
                  "required": [
                    "href"
                  ]
                },
                "pull_request": {
                  "title": "Link",
                  "type": "object",
                  "properties": {
                    "href": {
                      "type": "string",
                      "format": "uri-template"
                    }
                  },
                  "required": [
                    "href"
                  ]
                },
                "self": {
                  "title": "Link",
                  "type": "object",
                  "properties": {
                    "href": {
                      "type": "string",
                      "format": "uri-template"
                    }
                  },
                  "required": [
                    "href"
                  ]
                }
              },
              "required": [
                "self",
                "html",
                "pull_request"
              ]
            },
            "original_commit_id": {
              "type": "string"
            },
            "reactions": {
              "title": "Reactions",
              "type": "object",
              "properties": {
                "+1": {
                  "type": "integer"
                },
                "-1": {
                  "type": "integer"
                },
                "confused": {
                  "type": "integer"
                },
                "eyes": {
                  "type": "integer"
                },
                "heart": {
                  "type": "integer"
                },
                "hooray": {
                  "type": "integer"
                },
                "laugh": {
                  "type": "integer"
                },
                "rocket": {
                  "type": "integer"
                },
                "total_count": {
                  "type": "integer"
                },
                "url": {
                  "type": "string",
                  "format": "uri"
                }
              }
            },
            "in_reply_to_id": {
              "type": "integer"
            }
          },
          "required": [
            "url",
            "pull_request_review_id",
            "id",
            "node_id",
            "diff_hunk",
            "path",
            "position",
            "original_position",
            "commit_id",
            "original_commit_id",
            "user",
            "body",
            "created_at",
            "updated_at",
            "html_url",
            "pull_request_url",
            "_links",
            "reactions"
          ]
        }
      },
      "required": [
        "action",
        "comment",
        "pull_request"
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
    "gollum-event": {
      "title": "GollumEvent",
      "type": "object",
      "properties": {
        "pages": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "page_name": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "title": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "summary": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "action": {
                "type": "string"
              },
              "sha": {
                "type": "string"
              },
              "html_url": {
                "type": "string"
              }
            }
          }
        }
      },
      "required": [
        "pages"
      ]
    },
    "discussion": {
      "title": "Discussion",
      "description": "A Discussion in a repository.",
      "type": "object",
      "properties": {
        "active_lock_reason": {
          "type": [
            "string",
            "null"
          ]
        },
        "answer_chosen_at": {
          "type": [
            "string",
            "null"
          ]
        },
        "answer_chosen_by": {
          "title": "User",
          "type": [
            "object",
            "null"
          ],
          "properties": {
            "avatar_url": {
              "type": "string",
              "format": "uri"
            },
            "deleted": {
              "type": "boolean"
            },
            "email": {
              "type": [
                "string",
                "null"
              ]
            },
            "events_url": {
              "type": "string",
              "format": "uri-template"
            },
            "followers_url": {
              "type": "string",
              "format": "uri"
            },
            "following_url": {
              "type": "string",
              "format": "uri-template"
            },
            "gists_url": {
              "type": "string",
              "format": "uri-template"
            },
            "gravatar_id": {
              "type": "string"
            },
            "html_url": {
              "type": "string",
              "format": "uri"
            },
            "id": {
              "type": "integer"
            },
            "login": {
              "type": "string"
            },
            "name": {
              "type": "string"
            },
            "node_id": {
              "type": "string"
            },
            "organizations_url": {
              "type": "string",
              "format": "uri"
            },
            "received_events_url": {
              "type": "string",
              "format": "uri"
            },
            "repos_url": {
              "type": "string",
              "format": "uri"
            },
            "site_admin": {
              "type": "boolean"
            },
            "starred_url": {
              "type": "string",
              "format": "uri-template"
            },
            "subscriptions_url": {
              "type": "string",
              "format": "uri"
            },
            "type": {
              "type": "string",
              "enum": [
                "Bot",
                "User",
                "Organization"
              ]
            },
            "url": {
              "type": "string",
              "format": "uri"
            },
            "user_view_type": {
              "type": "string"
            }
          },
          "required": [
            "login",
            "id"
          ]
        },
        "answer_html_url": {
          "type": [
            "string",
            "null"
          ]
        },
        "author_association": {
          "title": "AuthorAssociation",
          "description": "How the author is associated with the repository.",
          "type": "string",
          "enum": [
            "COLLABORATOR",
            "CONTRIBUTOR",
            "FIRST_TIMER",
            "FIRST_TIME_CONTRIBUTOR",
            "MANNEQUIN",
            "MEMBER",
            "NONE",
            "OWNER"
          ]
        },
        "body": {
          "type": "string"
        },
        "category": {
          "type": "object",
          "properties": {
            "created_at": {
              "type": "string",
              "format": "date-time"
            },
            "description": {
              "type": "string"
            },
            "emoji": {
              "type": "string"
            },
            "id": {
              "type": "integer"
            },
            "is_answerable": {
              "type": "boolean"
            },
            "name": {
              "type": "string"
            },
            "node_id": {
              "type": "string"
            },
            "repository_id": {
              "type": "integer"
            },
            "slug": {
              "type": "string"
            },
            "updated_at": {
              "type": "string"
            }
          },
          "required": [
            "id",
            "repository_id",
            "emoji",
            "name",
            "description",
            "created_at",
            "updated_at",
            "slug",
            "is_answerable"
          ]
        },
        "comments": {
          "type": "integer"
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "html_url": {
          "type": "string"
        },
        "id": {
          "type": "integer"
        },
        "locked": {
          "type": "boolean"
        },
        "node_id": {
          "type": "string"
        },
        "number": {
          "type": "integer"
        },
        "reactions": {
          "title": "Reactions",
          "type": "object",
          "properties": {
            "+1": {
              "type": "integer"
            },
            "-1": {
              "type": "integer"
            },
            "confused": {
              "type": "integer"
            },
            "eyes": {
              "type": "integer"
            },
            "heart": {
              "type": "integer"
            },
            "hooray": {
              "type": "integer"
            },
            "laugh": {
              "type": "integer"
            },
            "rocket": {
              "type": "integer"
            },
            "total_count": {
              "type": "integer"
            },
            "url": {
              "type": "string",
              "format": "uri"
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
        "repository_url": {
          "type": "string"
        },
        "state": {
          "type": "string",
          "description": "The current state of the discussion.\n`converting` means that the discussion is being converted from an issue.\n`transferring` means that the discussion is being transferred from another repository.",
          "enum": [
            "open",
            "closed",
            "locked",
            "converting",
            "transferring"
          ]
        },
        "state_reason": {
          "description": "The reason for the current state",
          "type": [
            "string",
            "null"
          ],
          "enum": [
            "resolved",
            "outdated",
            "duplicate",
            "reopened",
            null
          ],
          "examples": [
            "resolved"
          ]
        },
        "timeline_url": {
          "type": "string"
        },
        "title": {
          "type": "string"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        },
        "user": {
          "title": "User",
          "type": [
            "object",
            "null"
          ],
          "properties": {
            "avatar_url": {
              "type": "string",
              "format": "uri"
            },
            "deleted": {
              "type": "boolean"
            },
            "email": {
              "type": [
                "string",
                "null"
              ]
            },
            "events_url": {
              "type": "string",
              "format": "uri-template"
            },
            "followers_url": {
              "type": "string",
              "format": "uri"
            },
            "following_url": {
              "type": "string",
              "format": "uri-template"
            },
            "gists_url": {
              "type": "string",
              "format": "uri-template"
            },
            "gravatar_id": {
              "type": "string"
            },
            "html_url": {
              "type": "string",
              "format": "uri"
            },
            "id": {
              "type": "integer",
              "format": "int64"
            },
            "login": {
              "type": "string"
            },
            "name": {
              "type": "string"
            },
            "node_id": {
              "type": "string"
            },
            "organizations_url": {
              "type": "string",
              "format": "uri"
            },
            "received_events_url": {
              "type": "string",
              "format": "uri"
            },
            "repos_url": {
              "type": "string",
              "format": "uri"
            },
            "site_admin": {
              "type": "boolean"
            },
            "starred_url": {
              "type": "string",
              "format": "uri-template"
            },
            "subscriptions_url": {
              "type": "string",
              "format": "uri"
            },
            "type": {
              "type": "string",
              "enum": [
                "Bot",
                "User",
                "Organization"
              ]
            },
            "url": {
              "type": "string",
              "format": "uri"
            },
            "user_view_type": {
              "type": "string"
            }
          },
          "required": [
            "login",
            "id"
          ]
        },
        "labels": {
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/label"
          }
        }
      },
      "required": [
        "repository_url",
        "category",
        "answer_html_url",
        "answer_chosen_at",
        "answer_chosen_by",
        "html_url",
        "id",
        "node_id",
        "number",
        "title",
        "user",
        "state",
        "state_reason",
        "locked",
        "comments",
        "created_at",
        "updated_at",
        "active_lock_reason",
        "body"
      ]
    },
    "fork-event": {
      "title": "ForkEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "forkee": {
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
            "full_name": {
              "type": "string"
            },
            "private": {
              "type": "boolean"
            },
            "owner": {
              "$ref": "#/components/schemas/simple-user"
            },
            "html_url": {
              "type": "string"
            },
            "description": {
              "type": [
                "string",
                "null"
              ]
            },
            "fork": {
              "type": "boolean"
            },
            "url": {
              "type": "string"
            },
            "forks_url": {
              "type": "string"
            },
            "keys_url": {
              "type": "string"
            },
            "collaborators_url": {
              "type": "string"
            },
            "teams_url": {
              "type": "string"
            },
            "hooks_url": {
              "type": "string"
            },
            "issue_events_url": {
              "type": "string"
            },
            "events_url": {
              "type": "string"
            },
            "assignees_url": {
              "type": "string"
            },
            "branches_url": {
              "type": "string"
            },
            "tags_url": {
              "type": "string"
            },
            "blobs_url": {
              "type": "string"
            },
            "git_tags_url": {
              "type": "string"
            },
            "git_refs_url": {
              "type": "string"
            },
            "trees_url": {
              "type": "string"
            },
            "statuses_url": {
              "type": "string"
            },
            "languages_url": {
              "type": "string"
            },
            "stargazers_url": {
              "type": "string"
            },
            "contributors_url": {
              "type": "string"
            },
            "subscribers_url": {
              "type": "string"
            },
            "subscription_url": {
              "type": "string"
            },
            "commits_url": {
              "type": "string"
            },
            "git_commits_url": {
              "type": "string"
            },
            "comments_url": {
              "type": "string"
            },
            "issue_comment_url": {
              "type": "string"
            },
            "contents_url": {
              "type": "string"
            },
            "compare_url": {
              "type": "string"
            },
            "merges_url": {
              "type": "string"
            },
            "archive_url": {
              "type": "string"
            },
            "downloads_url": {
              "type": "string"
            },
            "issues_url": {
              "type": "string"
            },
            "pulls_url": {
              "type": "string"
            },
            "milestones_url": {
              "type": "string"
            },
            "notifications_url": {
              "type": "string"
            },
            "labels_url": {
              "type": "string"
            },
            "releases_url": {
              "type": "string"
            },
            "deployments_url": {
              "type": "string"
            },
            "created_at": {
              "type": [
                "string",
                "null"
              ],
              "format": "date-time"
            },
            "updated_at": {
              "type": [
                "string",
                "null"
              ],
              "format": "date-time"
            },
            "pushed_at": {
              "type": [
                "string",
                "null"
              ],
              "format": "date-time"
            },
            "git_url": {
              "type": "string"
            },
            "ssh_url": {
              "type": "string"
            },
            "clone_url": {
              "type": "string"
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
            "size": {
              "type": "integer"
            },
            "stargazers_count": {
              "type": "integer"
            },
            "watchers_count": {
              "type": "integer"
            },
            "language": {
              "type": [
                "string",
                "null"
              ]
            },
            "has_issues": {
              "type": "boolean"
            },
            "has_projects": {
              "type": "boolean"
            },
            "has_downloads": {
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
            "forks_count": {
              "type": "integer"
            },
            "mirror_url": {
              "type": [
                "string",
                "null"
              ]
            },
            "archived": {
              "type": "boolean"
            },
            "disabled": {
              "type": "boolean"
            },
            "open_issues_count": {
              "type": "integer"
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
            "allow_forking": {
              "type": "boolean"
            },
            "is_template": {
              "type": "boolean"
            },
            "web_commit_signoff_required": {
              "type": "boolean"
            },
            "topics": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "visibility": {
              "type": "string"
            },
            "forks": {
              "type": "integer"
            },
            "open_issues": {
              "type": "integer"
            },
            "watchers": {
              "type": "integer"
            },
            "default_branch": {
              "type": "string"
            },
            "public": {
              "type": "boolean"
            }
          }
        }
      },
      "required": [
        "action",
        "forkee"
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
    "member-event": {
      "title": "MemberEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "member": {
          "$ref": "#/components/schemas/simple-user"
        }
      },
      "required": [
        "action",
        "member"
      ]
    },
    "release-event": {
      "title": "ReleaseEvent",
      "type": "object",
      "properties": {
        "action": {
          "type": "string"
        },
        "release": {
          "allOf": [
            {
              "$ref": "#/components/schemas/release"
            },
            {
              "type": "object",
              "properties": {
                "is_short_description_html_truncated": {
                  "type": "boolean"
                },
                "short_description_html": {
                  "type": "string"
                }
              }
            }
          ]
        }
      },
      "required": [
        "action",
        "release"
      ]
    }
  },
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

Resource `org` uses: alphabet=NUMERIC, length=1

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

Add a class `Org(Base)` with:

- Table name: `github_orgs`
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
