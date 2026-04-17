# Entity Implementation: teams

You are implementing the **teams** resource for the GitHub API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for teams

```json
{
  "paths": {
    "/enterprises/{enterprise}/teams": {
      "get": {
        "summary": "List enterprise teams",
        "description": "List all teams in the enterprise for the authenticated user",
        "tags": [
          "enterprise-teams"
        ],
        "operationId": "enterprise-teams/list",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/enterprise-teams/enterprise-teams#list-enterprise-teams"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/enterprise"
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
                    "$ref": "#/components/schemas/enterprise-team"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/enterprise-teams-items"
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
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "enterprise-teams",
          "subcategory": "enterprise-teams"
        }
      },
      "post": {
        "summary": "Create an enterprise team",
        "description": "To create an enterprise team, the authenticated user must be an owner of the enterprise.",
        "tags": [
          "enterprise-teams"
        ],
        "operationId": "enterprise-teams/create",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/enterprise-teams/enterprise-teams#create-an-enterprise-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/enterprise"
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
                    "description": "The name of the team."
                  },
                  "description": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "description": "A description of the team."
                  },
                  "sync_to_organizations": {
                    "type": "string",
                    "description": "Retired: this field is no longer supported.\nWhether the enterprise team should be reflected in each organization.\nThis value cannot be set.\n",
                    "enum": [
                      "all",
                      "disabled"
                    ],
                    "default": "disabled"
                  },
                  "organization_selection_type": {
                    "type": "string",
                    "description": "Specifies which organizations in the enterprise should have access to this team. Can be one of `disabled`, `selected`, or `all`.\n`disabled`: The team is not assigned to any organizations. This is the default when you create a new team.\n`selected`: The team is assigned to specific organizations. You can then use the [add organization assignments API](https://docs.github.com/rest/enterprise-teams/enterprise-team-organizations#add-organization-assignments) endpoint.\n`all`: The team is assigned to all current and future organizations in the enterprise.\n",
                    "enum": [
                      "disabled",
                      "selected",
                      "all"
                    ],
                    "default": "disabled"
                  },
                  "group_id": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "description": "The ID of the IdP group to assign team membership with. You can get this value from the [REST API endpoints for SCIM](https://docs.github.com/rest/scim#list-provisioned-scim-groups-for-an-enterprise)."
                  }
                },
                "required": [
                  "name"
                ]
              },
              "examples": {
                "default": {
                  "value": {
                    "name": "Justice League",
                    "description": "A great team.",
                    "group_id": "62ab9291-fae2-468e-974b-7e45096d5021"
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
                  "$ref": "#/components/schemas/enterprise-team"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/enterprise-teams-item"
                  }
                }
              }
            }
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "enterprise-teams",
          "subcategory": "enterprise-teams"
        }
      }
    },
    "/enterprises/{enterprise}/teams/{team_slug}": {
      "get": {
        "summary": "Get an enterprise team",
        "description": "Gets a team using the team's slug. To create the slug, GitHub replaces special characters in the name string, changes all words to lowercase, and replaces spaces with a `-` separator and adds the \"ent:\" prefix. For example, \"My TEam N\u00e4me\" would become `ent:my-team-name`.",
        "tags": [
          "enterprise-teams"
        ],
        "operationId": "enterprise-teams/get",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/enterprise-teams/enterprise-teams#get-an-enterprise-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/enterprise"
          },
          {
            "$ref": "#/components/parameters/team-slug"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/enterprise-team"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/enterprise-teams-item"
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
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "enterprise-teams",
          "subcategory": "enterprise-teams"
        }
      },
      "patch": {
        "summary": "Update an enterprise team",
        "description": "To edit a team, the authenticated user must be an enterprise owner.",
        "tags": [
          "enterprise-teams"
        ],
        "operationId": "enterprise-teams/update",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/enterprise-teams/enterprise-teams#update-an-enterprise-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/enterprise"
          },
          {
            "$ref": "#/components/parameters/team-slug"
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
                    "type": [
                      "string",
                      "null"
                    ],
                    "description": "A new name for the team."
                  },
                  "description": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "description": "A new description for the team."
                  },
                  "sync_to_organizations": {
                    "type": "string",
                    "description": "Retired: this field is no longer supported.\nWhether the enterprise team should be reflected in each organization.\nThis value cannot be changed.\n",
                    "enum": [
                      "all",
                      "disabled"
                    ],
                    "default": "disabled"
                  },
                  "organization_selection_type": {
                    "type": "string",
                    "description": "Specifies which organizations in the enterprise should have access to this team. Can be one of `disabled`, `selected`, or `all`.\n`disabled`: The team is not assigned to any organizations. This is the default when you create a new team.\n`selected`: The team is assigned to specific organizations. You can then use the [add organization assignments API](https://docs.github.com/rest/enterprise-teams/enterprise-team-organizations#add-organization-assignments).\n`all`: The team is assigned to all current and future organizations in the enterprise.\n",
                    "enum": [
                      "disabled",
                      "selected",
                      "all"
                    ],
                    "default": "disabled"
                  },
                  "group_id": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "description": "The ID of the IdP group to assign team membership with. The new IdP group will replace the existing one, or replace existing direct members if the team isn't currently linked to an IdP group."
                  }
                }
              },
              "examples": {
                "default": {
                  "value": {
                    "name": "Justice League",
                    "description": "A great team.",
                    "group_id": "62ab9291-fae2-468e-974b-7e45096d5021"
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
                  "$ref": "#/components/schemas/enterprise-team"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/enterprise-teams-item"
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
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "enterprise-teams",
          "subcategory": "enterprise-teams"
        }
      },
      "delete": {
        "summary": "Delete an enterprise team",
        "description": "To delete an enterprise team, the authenticated user must be an enterprise owner.\n\nIf you are an enterprise owner, deleting an enterprise team will delete all of its IdP mappings as well.",
        "tags": [
          "enterprise-teams"
        ],
        "operationId": "enterprise-teams/delete",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/enterprise-teams/enterprise-teams#delete-an-enterprise-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/enterprise"
          },
          {
            "$ref": "#/components/parameters/team-slug"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "enterprise-teams",
          "subcategory": "enterprise-teams"
        }
      }
    },
    "/orgs/{org}/invitations/{invitation_id}/teams": {
      "get": {
        "summary": "List organization invitation teams",
        "description": "List all teams associated with an invitation. In order to see invitations in an organization, the authenticated user must be an organization owner.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/list-invitation-teams",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/members#list-organization-invitation-teams"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/invitation-id"
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
                    "$ref": "#/components/schemas/team"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-items"
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
          "category": "orgs",
          "subcategory": "members"
        }
      }
    },
    "/orgs/{org}/organization-roles/teams/{team_slug}": {
      "delete": {
        "summary": "Remove all organization roles for a team",
        "description": "Removes all assigned organization roles from a team. For more information on organization roles, see \"[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles).\"\n\nThe authenticated user must be an administrator for the organization to use this endpoint.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/revoke-all-org-roles-team",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/organization-roles#remove-all-organization-roles-for-a-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
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
    "/orgs/{org}/organization-roles/teams/{team_slug}/{role_id}": {
      "put": {
        "summary": "Assign an organization role to a team",
        "description": "Assigns an organization role to a team in an organization. For more information on organization roles, see \"[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles).\"\n\nThe authenticated user must be an administrator for the organization to use this endpoint.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/assign-team-to-org-role",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/organization-roles#assign-an-organization-role-to-a-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
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
            "description": "Response if the organization, team or role does not exist."
          },
          "422": {
            "description": "Response if the organization roles feature is not enabled for the organization, or validation failed."
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
        "summary": "Remove an organization role from a team",
        "description": "Removes an organization role from a team. For more information on organization roles, see \"[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles).\"\n\nThe authenticated user must be an administrator for the organization to use this endpoint.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/revoke-org-role-team",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/organization-roles#remove-an-organization-role-from-a-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
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
    "/orgs/{org}/organization-roles/{role_id}/teams": {
      "get": {
        "summary": "List teams that are assigned to an organization role",
        "description": "Lists the teams that are assigned to an organization role. For more information on organization roles, see \"[Using organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles).\"\n\nTo use this endpoint, you must be an administrator for the organization.\n\nOAuth app tokens and personal access tokens (classic) need the `admin:org` scope to use this endpoint.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/list-org-role-teams",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/organization-roles#list-teams-that-are-assigned-to-an-organization-role"
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
            "description": "Response - List of assigned teams",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "description": "List of teams assigned to the organization role",
                  "items": {
                    "$ref": "#/components/schemas/team-role-assignment"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-items"
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
    "/orgs/{org}/security-managers/teams/{team_slug}": {
      "put": {
        "summary": "Add a security manager team",
        "description": "> [!WARNING]\n> **Closing down notice:** This operation is closing down and will be removed starting January 1, 2026. Please use the \"[Organization Roles](https://docs.github.com/rest/orgs/organization-roles)\" endpoints instead.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/add-security-manager-team",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/security-managers#add-a-security-manager-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
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
          "previews": [],
          "category": "orgs",
          "subcategory": "security-managers",
          "deprecationDate": "2024-12-01",
          "removalDate": "2026-01-01"
        },
        "deprecated": true
      },
      "delete": {
        "summary": "Remove a security manager team",
        "description": "> [!WARNING]\n> **Closing down notice:** This operation is closing down and will be removed starting January 1, 2026. Please use the \"[Organization Roles](https://docs.github.com/rest/orgs/organization-roles)\" endpoints instead.",
        "tags": [
          "orgs"
        ],
        "operationId": "orgs/remove-security-manager-team",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/orgs/security-managers#remove-a-security-manager-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
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
          "previews": [],
          "category": "orgs",
          "subcategory": "security-managers",
          "deprecationDate": "2024-12-01",
          "removalDate": "2026-01-01"
        },
        "deprecated": true
      }
    },
    "/orgs/{org}/teams": {
      "get": {
        "summary": "List teams",
        "description": "Lists all teams in an organization that are visible to the authenticated user.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/list",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#list-teams"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/per-page"
          },
          {
            "$ref": "#/components/parameters/page"
          },
          {
            "$ref": "#/components/parameters/team-type"
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
                    "$ref": "#/components/schemas/team"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-items"
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
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": true,
          "category": "teams",
          "subcategory": "teams"
        }
      },
      "post": {
        "summary": "Create a team",
        "description": "To create a team, the authenticated user must be a member or owner of `{org}`. By default, organization members can create teams. Organization owners can limit team creation to organization owners. For more information, see \"[Setting team creation permissions](https://docs.github.com/articles/setting-team-creation-permissions-in-your-organization).\"\n\nWhen you create a new team, you automatically become a team maintainer without explicitly adding yourself to the optional array of `maintainers`. For more information, see \"[About teams](https://docs.github.com/github/setting-up-and-managing-organizations-and-teams/about-teams)\".",
        "tags": [
          "teams"
        ],
        "operationId": "teams/create",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#create-a-team"
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
                    "description": "The name of the team."
                  },
                  "description": {
                    "type": "string",
                    "description": "The description of the team."
                  },
                  "maintainers": {
                    "type": "array",
                    "description": "List GitHub usernames for organization members who will become team maintainers.",
                    "items": {
                      "type": "string"
                    }
                  },
                  "repo_names": {
                    "type": "array",
                    "description": "The full name (e.g., \"organization-name/repository-name\") of repositories to add the team to.",
                    "items": {
                      "type": "string"
                    }
                  },
                  "privacy": {
                    "type": "string",
                    "description": "The level of privacy this team should have. The options are:  \n**For a non-nested team:**  \n * `secret` - only visible to organization owners and members of this team.  \n * `closed` - visible to all members of this organization.  \nDefault: `secret`  \n**For a parent or child team:**  \n * `closed` - visible to all members of this organization.  \nDefault for child team: `closed`",
                    "enum": [
                      "secret",
                      "closed"
                    ]
                  },
                  "notification_setting": {
                    "type": "string",
                    "description": "The notification setting the team has chosen. The options are:  \n * `notifications_enabled` - team members receive notifications when the team is @mentioned.  \n * `notifications_disabled` - no one receives notifications.  \nDefault: `notifications_enabled`",
                    "enum": [
                      "notifications_enabled",
                      "notifications_disabled"
                    ]
                  },
                  "parent_team_id": {
                    "type": "integer",
                    "description": "The ID of a team to set as the parent team."
                  }
                },
                "required": [
                  "name"
                ]
              },
              "examples": {
                "default": {
                  "value": {
                    "name": "Justice League",
                    "description": "A great team",
                    "permission": "push",
                    "notification_setting": "notifications_enabled",
                    "privacy": "closed"
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
                  "$ref": "#/components/schemas/team-full"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-full"
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
          "category": "teams",
          "subcategory": "teams"
        }
      }
    },
    "/orgs/{org}/teams/{team_slug}": {
      "get": {
        "summary": "Get a team by name",
        "description": "Gets a team using the team's `slug`. To create the `slug`, GitHub replaces special characters in the `name` string, changes all words to lowercase, and replaces spaces with a `-` separator. For example, `\"My TEam N\u00e4me\"` would become `my-team-name`.\n\n> [!NOTE]\n> You can also specify a team by `org_id` and `team_id` using the route `GET /organizations/{org_id}/team/{team_id}`.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/get-by-name",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#get-a-team-by-name"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/team-full"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-full"
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
          "category": "teams",
          "subcategory": "teams"
        }
      },
      "patch": {
        "summary": "Update a team",
        "description": "To edit a team, the authenticated user must either be an organization owner or a team maintainer.\n\n> [!NOTE]\n> You can also specify a team by `org_id` and `team_id` using the route `PATCH /organizations/{org_id}/team/{team_id}`.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/update-in-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#update-a-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
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
                    "description": "The name of the team."
                  },
                  "description": {
                    "type": "string",
                    "description": "The description of the team."
                  },
                  "privacy": {
                    "type": "string",
                    "description": "The level of privacy this team should have. Editing teams without specifying this parameter leaves `privacy` intact. When a team is nested, the `privacy` for parent teams cannot be `secret`. The options are:  \n**For a non-nested team:**  \n * `secret` - only visible to organization owners and members of this team.  \n * `closed` - visible to all members of this organization.  \n**For a parent or child team:**  \n * `closed` - visible to all members of this organization.",
                    "enum": [
                      "secret",
                      "closed"
                    ]
                  },
                  "notification_setting": {
                    "type": "string",
                    "description": "The notification setting the team has chosen. Editing teams without specifying this parameter leaves `notification_setting` intact. The options are: \n * `notifications_enabled` - team members receive notifications when the team is @mentioned.  \n * `notifications_disabled` - no one receives notifications.",
                    "enum": [
                      "notifications_enabled",
                      "notifications_disabled"
                    ]
                  },
                  "permission": {
                    "type": "string",
                    "description": "**Closing down notice**. The permission that new repositories will be added to the team with when none is specified.",
                    "enum": [
                      "pull",
                      "push",
                      "admin"
                    ],
                    "default": "pull"
                  },
                  "parent_team_id": {
                    "type": [
                      "integer",
                      "null"
                    ],
                    "description": "The ID of a team to set as the parent team."
                  }
                }
              },
              "examples": {
                "default": {
                  "value": {
                    "name": "new team name",
                    "description": "new team description",
                    "privacy": "closed",
                    "notification_setting": "notifications_enabled"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Response when the updated information already exists",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/team-full"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-full"
                  }
                }
              }
            }
          },
          "201": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/team-full"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-full"
                  }
                }
              }
            }
          },
          "404": {
            "$ref": "#/components/responses/not_found"
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
          "category": "teams",
          "subcategory": "teams"
        }
      },
      "delete": {
        "summary": "Delete a team",
        "description": "To delete a team, the authenticated user must be an organization owner or team maintainer.\n\nIf you are an organization owner, deleting a parent team will delete all of its child teams as well.\n\n> [!NOTE]\n> You can also specify a team by `org_id` and `team_id` using the route `DELETE /organizations/{org_id}/team/{team_id}`.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/delete-in-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#delete-a-team"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/org"
          },
          {
            "$ref": "#/components/parameters/team-slug"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
          },
          "422": {
            "$ref": "#/components/responses/enterprise_team_unsupported"
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
    "/orgs/{org}/teams/{team_slug}/teams": {
      "get": {
        "summary": "List child teams",
        "description": "Lists the child teams of the team specified by `{team_slug}`.\n\n> [!NOTE]\n> You can also specify a team by `org_id` and `team_id` using the route `GET /organizations/{org_id}/team/{team_id}/teams`.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/list-child-in-org",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#list-child-teams"
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
            "description": "if child teams exist",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/team"
                  }
                },
                "examples": {
                  "response-if-child-teams-exist": {
                    "$ref": "#/components/examples/team-items-response-if-child-teams-exist"
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
    "/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams": {
      "get": {
        "summary": "Get teams with access to the protected branch",
        "description": "Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nLists the teams who have push access to this branch. The list includes child teams.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/get-teams-with-access-to-protected-branch",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/branches/branch-protection#get-teams-with-access-to-the-protected-branch"
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
                    "$ref": "#/components/schemas/team"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-items"
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
        "summary": "Add team access restrictions",
        "description": "Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nGrants the specified teams push access for this branch. You can also give push access to child teams.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/add-team-access-restrictions",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/branches/branch-protection#add-team-access-restrictions"
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
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "oneOf": [
                  {
                    "type": "object",
                    "properties": {
                      "teams": {
                        "type": "array",
                        "description": "The slug values for teams",
                        "items": {
                          "type": "string"
                        }
                      }
                    },
                    "required": [
                      "teams"
                    ],
                    "example": {
                      "teams": [
                        "my-team"
                      ]
                    }
                  },
                  {
                    "type": "array",
                    "description": "The slug values for teams",
                    "items": {
                      "type": "string"
                    }
                  }
                ]
              },
              "examples": {
                "default": {
                  "summary": "Example adding a team in a branch protection rule",
                  "value": {
                    "teams": [
                      "justice-league"
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
                    "$ref": "#/components/schemas/team"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-items"
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
          "requestBodyParameterName": "teams",
          "category": "branches",
          "subcategory": "branch-protection"
        }
      },
      "put": {
        "summary": "Set team access restrictions",
        "description": "Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nReplaces the list of teams that have push access to this branch. This removes all teams that previously had push access and grants push access to the new list of teams. Team restrictions include child teams.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/set-team-access-restrictions",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/branches/branch-protection#set-team-access-restrictions"
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
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "oneOf": [
                  {
                    "type": "object",
                    "properties": {
                      "teams": {
                        "type": "array",
                        "description": "The slug values for teams",
                        "items": {
                          "type": "string"
                        }
                      }
                    },
                    "required": [
                      "teams"
                    ],
                    "example": {
                      "teams": [
                        "justice-league"
                      ]
                    }
                  },
                  {
                    "type": "array",
                    "description": "The slug values for teams",
                    "items": {
                      "type": "string"
                    }
                  }
                ]
              },
              "examples": {
                "default": {
                  "summary": "Example replacing a team in a branch protection rule",
                  "value": {
                    "teams": [
                      "justice-league"
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
                    "$ref": "#/components/schemas/team"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-items"
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
          "requestBodyParameterName": "teams",
          "category": "branches",
          "subcategory": "branch-protection"
        }
      },
      "delete": {
        "summary": "Remove team access restrictions",
        "description": "Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server. For more information, see [GitHub's products](https://docs.github.com/github/getting-started-with-github/githubs-products) in the GitHub Help documentation.\n\nRemoves the ability of a team to push to this branch. You can also remove push access for child teams.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/remove-team-access-restrictions",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/branches/branch-protection#remove-team-access-restrictions"
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
          "content": {
            "application/json": {
              "schema": {
                "oneOf": [
                  {
                    "type": "object",
                    "properties": {
                      "teams": {
                        "type": "array",
                        "description": "The slug values for teams",
                        "items": {
                          "type": "string"
                        }
                      }
                    },
                    "required": [
                      "teams"
                    ],
                    "example": {
                      "teams": [
                        "my-team"
                      ]
                    }
                  },
                  {
                    "type": "array",
                    "description": "The slug values for teams",
                    "items": {
                      "type": "string"
                    }
                  }
                ]
              },
              "examples": {
                "default": {
                  "summary": "Example removing a team in a branch protection rule",
                  "value": {
                    "teams": [
                      "octocats"
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
                    "$ref": "#/components/schemas/team"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-items"
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
          "requestBodyParameterName": "teams",
          "category": "branches",
          "subcategory": "branch-protection"
        }
      }
    },
    "/repos/{owner}/{repo}/teams": {
      "get": {
        "summary": "List repository teams",
        "description": "Lists the teams that have access to the specified repository and that are also visible to the authenticated user.\n\nFor a public repository, a team is listed only if that team added the public repository explicitly.\n\nOAuth app tokens and personal access tokens (classic) need the `public_repo` or `repo` scope to use this endpoint with a public repository, and `repo` scope to use this endpoint with a private repository.",
        "tags": [
          "repos"
        ],
        "operationId": "repos/list-teams",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/repos/repos#list-repository-teams"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/owner"
          },
          {
            "$ref": "#/components/parameters/repo"
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
                    "$ref": "#/components/schemas/team"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-items"
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
          "category": "repos",
          "subcategory": "repos"
        }
      }
    },
    "/teams/{team_id}": {
      "get": {
        "summary": "Get a team (Legacy)",
        "description": "> [!WARNING]\n> **Endpoint closing down notice:** This endpoint route is closing down and will be removed from the Teams API. We recommend migrating your existing code to use the [Get a team by name](https://docs.github.com/rest/teams/teams#get-a-team-by-name) endpoint.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/get-legacy",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#get-a-team-legacy"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/team-id"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/team-full"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-full"
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
          "removalDate": "2021-02-01",
          "deprecationDate": "2020-01-21",
          "category": "teams",
          "subcategory": "teams"
        },
        "deprecated": true
      },
      "patch": {
        "summary": "Update a team (Legacy)",
        "description": "> [!WARNING]\n> **Endpoint closing down notice:** This endpoint route is closing down and will be removed from the Teams API. We recommend migrating your existing code to use the new [Update a team](https://docs.github.com/rest/teams/teams#update-a-team) endpoint.\n\nTo edit a team, the authenticated user must either be an organization owner or a team maintainer.\n\n> [!NOTE]\n> With nested teams, the `privacy` for parent teams cannot be `secret`.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/update-legacy",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#update-a-team-legacy"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/team-id"
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
                    "description": "The name of the team."
                  },
                  "description": {
                    "type": "string",
                    "description": "The description of the team."
                  },
                  "privacy": {
                    "type": "string",
                    "description": "The level of privacy this team should have. Editing teams without specifying this parameter leaves `privacy` intact. The options are:  \n**For a non-nested team:**  \n * `secret` - only visible to organization owners and members of this team.  \n * `closed` - visible to all members of this organization.  \n**For a parent or child team:**  \n * `closed` - visible to all members of this organization.",
                    "enum": [
                      "secret",
                      "closed"
                    ]
                  },
                  "notification_setting": {
                    "type": "string",
                    "description": "The notification setting the team has chosen. Editing teams without specifying this parameter leaves `notification_setting` intact. The options are: \n * `notifications_enabled` - team members receive notifications when the team is @mentioned.  \n * `notifications_disabled` - no one receives notifications.",
                    "enum": [
                      "notifications_enabled",
                      "notifications_disabled"
                    ]
                  },
                  "permission": {
                    "type": "string",
                    "description": "**Closing down notice**. The permission that new repositories will be added to the team with when none is specified.",
                    "enum": [
                      "pull",
                      "push",
                      "admin"
                    ],
                    "default": "pull"
                  },
                  "parent_team_id": {
                    "type": [
                      "integer",
                      "null"
                    ],
                    "description": "The ID of a team to set as the parent team."
                  }
                },
                "required": [
                  "name"
                ]
              },
              "examples": {
                "default": {
                  "value": {
                    "name": "new team name",
                    "description": "new team description",
                    "privacy": "closed",
                    "notification_setting": "notifications_enabled"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Response when the updated information already exists",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/team-full"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-full"
                  }
                }
              }
            }
          },
          "201": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/team-full"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-full"
                  }
                }
              }
            }
          },
          "404": {
            "$ref": "#/components/responses/not_found"
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
          "removalDate": "2021-02-01",
          "deprecationDate": "2020-01-21",
          "category": "teams",
          "subcategory": "teams"
        },
        "deprecated": true
      },
      "delete": {
        "summary": "Delete a team (Legacy)",
        "description": "> [!WARNING]\n> **Endpoint closing down notice:** This endpoint route is closing down and will be removed from the Teams API. We recommend migrating your existing code to use the new [Delete a team](https://docs.github.com/rest/teams/teams#delete-a-team) endpoint.\n\nTo delete a team, the authenticated user must be an organization owner or team maintainer.\n\nIf you are an organization owner, deleting a parent team will delete all of its child teams as well.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/delete-legacy",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#delete-a-team-legacy"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/team-id"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
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
          "removalDate": "2021-02-01",
          "deprecationDate": "2020-01-21",
          "category": "teams",
          "subcategory": "teams"
        },
        "deprecated": true
      }
    },
    "/teams/{team_id}/teams": {
      "get": {
        "summary": "List child teams (Legacy)",
        "description": "> [!WARNING]\n> **Endpoint closing down notice:** This endpoint route is closing down and will be removed from the Teams API. We recommend migrating your existing code to use the new [`List child teams`](https://docs.github.com/rest/teams/teams#list-child-teams) endpoint.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/list-child-legacy",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#list-child-teams-legacy"
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
            "description": "if child teams exist",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/team"
                  }
                },
                "examples": {
                  "response-if-child-teams-exist": {
                    "$ref": "#/components/examples/team-items-response-if-child-teams-exist"
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
      }
    },
    "/user/teams": {
      "get": {
        "summary": "List teams for the authenticated user",
        "description": "List all of the teams across all of the organizations to which the authenticated\nuser belongs.\n\nOAuth app tokens and personal access tokens (classic) need the `user`, `repo`, or `read:org` scope to use this endpoint.\n\nWhen using a fine-grained personal access token, the resource owner of the token must be a single organization, and the response will only include the teams from that organization.",
        "tags": [
          "teams"
        ],
        "operationId": "teams/list-for-authenticated-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/teams/teams#list-teams-for-the-authenticated-user"
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
                    "$ref": "#/components/schemas/team-full"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/team-full-items"
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
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "teams",
          "subcategory": "teams"
        }
      }
    }
  },
  "schemas": {
    "team-organization": {
      "title": "Team Organization",
      "description": "Team Organization",
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
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2008-01-14T04:33:35Z"
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
    "team-role-assignment": {
      "title": "A Role Assignment for a Team",
      "description": "The Relationship a Team has with a role.",
      "type": "object",
      "properties": {
        "assignment": {
          "type": "string",
          "description": "Determines if the team has a direct, indirect, or mixed relationship to a role",
          "enum": [
            "direct",
            "indirect",
            "mixed"
          ],
          "examples": [
            "direct"
          ]
        },
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
        "parent": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "$ref": "#/components/schemas/team-simple"
            }
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
        "type",
        "parent"
      ]
    },
    "team-full": {
      "title": "Full Team",
      "description": "Groups of organization members that gives permissions on specified repositories.",
      "type": "object",
      "properties": {
        "id": {
          "description": "Unique identifier of the team",
          "type": "integer",
          "examples": [
            42
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
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/orgs/rails/teams/core"
          ]
        },
        "name": {
          "description": "Name of the team",
          "type": "string",
          "examples": [
            "Developers"
          ]
        },
        "slug": {
          "type": "string",
          "examples": [
            "justice-league"
          ]
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "A great team."
          ]
        },
        "privacy": {
          "description": "The level of privacy this team should have",
          "type": "string",
          "enum": [
            "closed",
            "secret"
          ],
          "examples": [
            "closed"
          ]
        },
        "notification_setting": {
          "description": "The notification setting the team has set",
          "type": "string",
          "enum": [
            "notifications_enabled",
            "notifications_disabled"
          ],
          "examples": [
            "notifications_enabled"
          ]
        },
        "permission": {
          "description": "Permission that the team will have for its repositories",
          "type": "string",
          "examples": [
            "push"
          ]
        },
        "members_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/organizations/1/team/1/members{/member}"
          ]
        },
        "repositories_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/organizations/1/team/1/repos"
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
        },
        "members_count": {
          "type": "integer",
          "examples": [
            3
          ]
        },
        "repos_count": {
          "type": "integer",
          "examples": [
            10
          ]
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2017-07-14T16:53:42Z"
          ]
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2017-08-17T12:37:15Z"
          ]
        },
        "organization": {
          "$ref": "#/components/schemas/team-organization"
        },
        "ldap_dn": {
          "$ref": "#/components/schemas/ldap-dn"
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
        "type",
        "created_at",
        "updated_at",
        "members_count",
        "repos_count",
        "organization"
      ]
    },
    "ldap-dn": {
      "type": "string",
      "description": "The [distinguished name](https://www.ldap.com/ldap-dns-and-rdns) (DN) of the LDAP entry to map to a team.",
      "examples": [
        "cn=Enterprise Ops,ou=teams,dc=github,dc=com"
      ]
    },
    "enterprise-team": {
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
  },
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
```

### Relationship manifest

```yaml
github_teams:
  parent_team_id:
    target_table: github_teams
    target_column: id
    confidence: high
    reason: 'request body on POST /orgs/{org}/teams: parent_team_id'

```

### FK dependency schemas (for stub creation if needed)

```json
{}
```

### ID format

Resource `team` uses: alphabet=NUMERIC, length=1

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

Add a class `Team(Base)` with:

- Table name: `github_teams`
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
