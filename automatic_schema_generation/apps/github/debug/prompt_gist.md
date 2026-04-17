# Entity Implementation: gists

You are implementing the **gists** resource for the GitHub API
replica. You will add code to four existing files. Do not create new files.

## Context provided

### OpenAPI excerpt for gists

```json
{
  "paths": {
    "/gists": {
      "get": {
        "summary": "List gists for the authenticated user",
        "description": "Lists the authenticated user's gists or if called anonymously, this endpoint returns all public gists:",
        "tags": [
          "gists"
        ],
        "operationId": "gists/list",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#list-gists-for-the-authenticated-user"
        },
        "parameters": [
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
                    "$ref": "#/components/schemas/base-gist"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/base-gist-items"
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
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "gists",
          "subcategory": "gists"
        }
      },
      "post": {
        "summary": "Create a gist",
        "description": "Allows you to add a new gist with one or more files.\n\n> [!NOTE]\n> Don't name your files \"gistfile\" with a numerical suffix. This is the format of the automatic naming scheme that Gist uses internally.",
        "operationId": "gists/create",
        "tags": [
          "gists"
        ],
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#create-a-gist"
        },
        "parameters": [],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "properties": {
                  "description": {
                    "description": "Description of the gist",
                    "type": "string",
                    "examples": [
                      "Example Ruby script"
                    ]
                  },
                  "files": {
                    "description": "Names and content for the files that make up the gist",
                    "type": "object",
                    "additionalProperties": {
                      "type": "object",
                      "properties": {
                        "content": {
                          "description": "Content of the file",
                          "readOnly": false,
                          "type": "string"
                        }
                      },
                      "required": [
                        "content"
                      ]
                    },
                    "examples": [
                      {
                        "hello.rb": {
                          "content": "puts \"Hello, World!\""
                        }
                      }
                    ]
                  },
                  "public": {
                    "oneOf": [
                      {
                        "description": "Flag indicating whether the gist is public",
                        "type": "boolean",
                        "default": false,
                        "examples": [
                          true
                        ]
                      },
                      {
                        "type": "string",
                        "default": "false",
                        "enum": [
                          "true",
                          "false"
                        ],
                        "examples": [
                          "true"
                        ]
                      }
                    ]
                  }
                },
                "required": [
                  "files"
                ],
                "type": "object"
              },
              "examples": {
                "default": {
                  "summary": "Creating a gist",
                  "value": {
                    "description": "Example of a gist",
                    "public": false,
                    "files": {
                      "README.md": {
                        "content": "Hello World"
                      }
                    }
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
                  "$ref": "#/components/schemas/gist-simple"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/gist"
                  }
                }
              }
            },
            "headers": {
              "Location": {
                "example": "https://api.github.com/gists/aa5a315d61ae9438b18d",
                "schema": {
                  "type": "string"
                }
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
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "gists",
          "subcategory": "gists"
        }
      }
    },
    "/gists/{gist_id}": {
      "get": {
        "summary": "Get a gist",
        "description": "Gets a specified gist.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown. This is the default if you do not pass any specific media type.",
        "tags": [
          "gists"
        ],
        "operationId": "gists/get",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#get-a-gist"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/gist-id"
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/gist-simple"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/gist"
                  }
                }
              }
            }
          },
          "403": {
            "$ref": "#/components/responses/forbidden_gist"
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
          "category": "gists",
          "subcategory": "gists"
        }
      },
      "patch": {
        "summary": "Update a gist",
        "description": "Allows you to update a gist's description and to update, delete, or rename gist files. Files\nfrom the previous version of the gist that aren't explicitly changed during an edit\nare unchanged.\n\nAt least one of `description` or `files` is required.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown. This is the default if you do not pass any specific media type.",
        "tags": [
          "gists"
        ],
        "operationId": "gists/update",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#update-a-gist"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/gist-id"
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "properties": {
                  "description": {
                    "description": "The description of the gist.",
                    "type": "string",
                    "examples": [
                      "Example Ruby script"
                    ]
                  },
                  "files": {
                    "description": "The gist files to be updated, renamed, or deleted. Each `key` must match the current filename\n(including extension) of the targeted gist file. For example: `hello.py`.\n\nTo delete a file, set the whole file to null. For example: `hello.py : null`. The file will also be\ndeleted if the specified object does not contain at least one of `content` or `filename`.",
                    "type": "object",
                    "additionalProperties": {
                      "type": [
                        "object",
                        "null"
                      ],
                      "properties": {
                        "content": {
                          "description": "The new content of the file.",
                          "type": "string"
                        },
                        "filename": {
                          "description": "The new filename for the file.",
                          "type": [
                            "string",
                            "null"
                          ]
                        }
                      }
                    },
                    "examples": [
                      {
                        "hello.rb": {
                          "content": "blah",
                          "filename": "goodbye.rb"
                        }
                      }
                    ]
                  }
                },
                "type": [
                  "object",
                  "null"
                ]
              },
              "examples": {
                "updateGist": {
                  "summary": "Updating a gist",
                  "value": {
                    "description": "An updated gist description",
                    "files": {
                      "README.md": {
                        "content": "Hello World from GitHub"
                      }
                    }
                  }
                },
                "deleteFile": {
                  "summary": "Deleting a gist file",
                  "value": {
                    "files": {
                      "hello.py": null
                    }
                  }
                },
                "renameFile": {
                  "summary": "Renaming a gist file",
                  "value": {
                    "files": {
                      "hello.py": {
                        "filename": "goodbye.py"
                      }
                    }
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
                  "$ref": "#/components/schemas/gist-simple"
                },
                "examples": {
                  "updateGist": {
                    "$ref": "#/components/examples/gist"
                  },
                  "deleteFile": {
                    "$ref": "#/components/examples/delete-gist-file"
                  },
                  "renameFile": {
                    "$ref": "#/components/examples/rename-gist-file"
                  }
                }
              }
            }
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
          "enabledForGitHubApps": false,
          "category": "gists",
          "subcategory": "gists"
        }
      },
      "delete": {
        "summary": "Delete a gist",
        "description": "",
        "tags": [
          "gists"
        ],
        "operationId": "gists/delete",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#delete-a-gist"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/gist-id"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "gists",
          "subcategory": "gists"
        }
      }
    },
    "/gists/{gist_id}/star": {
      "get": {
        "summary": "Check if a gist is starred",
        "description": "",
        "tags": [
          "gists"
        ],
        "operationId": "gists/check-is-starred",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#check-if-a-gist-is-starred"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/gist-id"
          }
        ],
        "responses": {
          "204": {
            "description": "Response if gist is starred"
          },
          "404": {
            "description": "Not Found if gist is not starred",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {},
                  "additionalProperties": false
                }
              }
            }
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "gists",
          "subcategory": "gists"
        }
      },
      "put": {
        "summary": "Star a gist",
        "description": "Note that you'll need to set `Content-Length` to zero when calling out to this endpoint. For more information, see \"[HTTP method](https://docs.github.com/rest/guides/getting-started-with-the-rest-api#http-method).\"",
        "tags": [
          "gists"
        ],
        "operationId": "gists/star",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#star-a-gist"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/gist-id"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
          },
          "404": {
            "$ref": "#/components/responses/not_found"
          },
          "304": {
            "$ref": "#/components/responses/not_modified"
          },
          "403": {
            "$ref": "#/components/responses/forbidden"
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "gists",
          "subcategory": "gists"
        }
      },
      "delete": {
        "summary": "Unstar a gist",
        "description": "",
        "tags": [
          "gists"
        ],
        "operationId": "gists/unstar",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#unstar-a-gist"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/gist-id"
          }
        ],
        "responses": {
          "204": {
            "description": "Response"
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
          "category": "gists",
          "subcategory": "gists"
        }
      }
    },
    "/gists/{gist_id}/{sha}": {
      "get": {
        "summary": "Get a gist revision",
        "description": "Gets a specified gist revision.\n\nThis endpoint supports the following custom media types. For more information, see \"[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types).\"\n\n- **`application/vnd.github.raw+json`**: Returns the raw markdown. This is the default if you do not pass any specific media type.",
        "tags": [
          "gists"
        ],
        "operationId": "gists/get-revision",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#get-a-gist-revision"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/gist-id"
          },
          {
            "name": "sha",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/gist-simple"
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/gist"
                  }
                }
              }
            }
          },
          "422": {
            "$ref": "#/components/responses/validation_failed"
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
          "category": "gists",
          "subcategory": "gists"
        }
      }
    },
    "/users/{username}/gists": {
      "get": {
        "summary": "List gists for a user",
        "description": "Lists public gists for the specified user:",
        "tags": [
          "gists"
        ],
        "operationId": "gists/list-for-user",
        "externalDocs": {
          "description": "API method documentation",
          "url": "https://docs.github.com/rest/gists/gists#list-gists-for-a-user"
        },
        "parameters": [
          {
            "$ref": "#/components/parameters/username"
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
                    "$ref": "#/components/schemas/base-gist"
                  }
                },
                "examples": {
                  "default": {
                    "$ref": "#/components/examples/base-gist-items"
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
          }
        },
        "x-github": {
          "githubCloudOnly": false,
          "enabledForGitHubApps": false,
          "category": "gists",
          "subcategory": "gists"
        }
      }
    }
  },
  "schemas": {
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
    "gist-simple": {
      "title": "Gist Simple",
      "description": "Gist Simple",
      "type": "object",
      "properties": {
        "fork_of": {
          "title": "Gist",
          "description": "Gist",
          "type": [
            "object",
            "null"
          ],
          "properties": {
            "url": {
              "type": "string",
              "format": "uri"
            },
            "forks_url": {
              "type": "string",
              "format": "uri"
            },
            "commits_url": {
              "type": "string",
              "format": "uri"
            },
            "id": {
              "type": "string"
            },
            "node_id": {
              "type": "string"
            },
            "git_pull_url": {
              "type": "string",
              "format": "uri"
            },
            "git_push_url": {
              "type": "string",
              "format": "uri"
            },
            "html_url": {
              "type": "string",
              "format": "uri"
            },
            "files": {
              "type": "object",
              "additionalProperties": {
                "type": "object",
                "properties": {
                  "filename": {
                    "type": "string"
                  },
                  "type": {
                    "type": "string"
                  },
                  "language": {
                    "type": "string"
                  },
                  "raw_url": {
                    "type": "string"
                  },
                  "size": {
                    "type": "integer"
                  }
                }
              }
            },
            "public": {
              "type": "boolean"
            },
            "created_at": {
              "type": "string",
              "format": "date-time"
            },
            "updated_at": {
              "type": "string",
              "format": "date-time"
            },
            "description": {
              "type": [
                "string",
                "null"
              ]
            },
            "comments": {
              "type": "integer"
            },
            "comments_enabled": {
              "type": "boolean"
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
            "comments_url": {
              "type": "string",
              "format": "uri"
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
            "truncated": {
              "type": "boolean"
            },
            "forks": {
              "type": "array",
              "items": {}
            },
            "history": {
              "type": "array",
              "items": {}
            }
          },
          "required": [
            "id",
            "node_id",
            "url",
            "forks_url",
            "commits_url",
            "git_pull_url",
            "git_push_url",
            "html_url",
            "comments_url",
            "public",
            "description",
            "comments",
            "user",
            "files",
            "created_at",
            "updated_at"
          ]
        },
        "url": {
          "type": "string"
        },
        "forks_url": {
          "type": "string"
        },
        "commits_url": {
          "type": "string"
        },
        "id": {
          "type": "string"
        },
        "node_id": {
          "type": "string"
        },
        "git_pull_url": {
          "type": "string"
        },
        "git_push_url": {
          "type": "string"
        },
        "html_url": {
          "type": "string"
        },
        "files": {
          "type": "object",
          "additionalProperties": {
            "type": [
              "object",
              "null"
            ],
            "properties": {
              "filename": {
                "type": "string"
              },
              "type": {
                "type": "string"
              },
              "language": {
                "type": "string"
              },
              "raw_url": {
                "type": "string"
              },
              "size": {
                "type": "integer"
              },
              "truncated": {
                "type": "boolean"
              },
              "content": {
                "type": "string"
              },
              "encoding": {
                "type": "string",
                "description": "The encoding used for `content`. Currently, `\"utf-8\"` and `\"base64\"` are supported.",
                "default": "utf-8"
              }
            }
          }
        },
        "public": {
          "type": "boolean"
        },
        "created_at": {
          "type": "string"
        },
        "updated_at": {
          "type": "string"
        },
        "description": {
          "type": [
            "string",
            "null"
          ]
        },
        "comments": {
          "type": "integer"
        },
        "comments_enabled": {
          "type": "boolean"
        },
        "user": {
          "type": [
            "string",
            "null"
          ]
        },
        "comments_url": {
          "type": "string"
        },
        "owner": {
          "$ref": "#/components/schemas/simple-user"
        },
        "truncated": {
          "type": "boolean"
        }
      }
    },
    "base-gist": {
      "title": "Base Gist",
      "description": "Base Gist",
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri"
        },
        "forks_url": {
          "type": "string",
          "format": "uri"
        },
        "commits_url": {
          "type": "string",
          "format": "uri"
        },
        "id": {
          "type": "string"
        },
        "node_id": {
          "type": "string"
        },
        "git_pull_url": {
          "type": "string",
          "format": "uri"
        },
        "git_push_url": {
          "type": "string",
          "format": "uri"
        },
        "html_url": {
          "type": "string",
          "format": "uri"
        },
        "files": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string"
              },
              "type": {
                "type": "string"
              },
              "language": {
                "type": "string"
              },
              "raw_url": {
                "type": "string"
              },
              "size": {
                "type": "integer"
              },
              "encoding": {
                "type": "string",
                "description": "The encoding used for `content`. Currently, `\"utf-8\"` and `\"base64\"` are supported.",
                "default": "utf-8"
              }
            }
          }
        },
        "public": {
          "type": "boolean"
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        },
        "description": {
          "type": [
            "string",
            "null"
          ]
        },
        "comments": {
          "type": "integer"
        },
        "comments_enabled": {
          "type": "boolean"
        },
        "comments_url": {
          "type": "string",
          "format": "uri"
        },
        "owner": {
          "$ref": "#/components/schemas/simple-user"
        },
        "truncated": {
          "type": "boolean"
        }
      },
      "required": [
        "id",
        "node_id",
        "url",
        "forks_url",
        "commits_url",
        "git_pull_url",
        "git_push_url",
        "html_url",
        "comments_url",
        "public",
        "description",
        "comments",
        "files",
        "created_at",
        "updated_at"
      ]
    }
  },
  "primary_response_schema": {
    "title": "Gist Simple",
    "description": "Gist Simple",
    "type": "object",
    "properties": {
      "fork_of": {
        "title": "Gist",
        "description": "Gist",
        "type": [
          "object",
          "null"
        ],
        "properties": {
          "url": {
            "type": "string",
            "format": "uri"
          },
          "forks_url": {
            "type": "string",
            "format": "uri"
          },
          "commits_url": {
            "type": "string",
            "format": "uri"
          },
          "id": {
            "type": "string"
          },
          "node_id": {
            "type": "string"
          },
          "git_pull_url": {
            "type": "string",
            "format": "uri"
          },
          "git_push_url": {
            "type": "string",
            "format": "uri"
          },
          "html_url": {
            "type": "string",
            "format": "uri"
          },
          "files": {
            "type": "object",
            "additionalProperties": {
              "type": "object",
              "properties": {
                "filename": {
                  "type": "string"
                },
                "type": {
                  "type": "string"
                },
                "language": {
                  "type": "string"
                },
                "raw_url": {
                  "type": "string"
                },
                "size": {
                  "type": "integer"
                }
              }
            }
          },
          "public": {
            "type": "boolean"
          },
          "created_at": {
            "type": "string",
            "format": "date-time"
          },
          "updated_at": {
            "type": "string",
            "format": "date-time"
          },
          "description": {
            "type": [
              "string",
              "null"
            ]
          },
          "comments": {
            "type": "integer"
          },
          "comments_enabled": {
            "type": "boolean"
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
          "comments_url": {
            "type": "string",
            "format": "uri"
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
          "truncated": {
            "type": "boolean"
          },
          "forks": {
            "type": "array",
            "items": {}
          },
          "history": {
            "type": "array",
            "items": {}
          }
        },
        "required": [
          "id",
          "node_id",
          "url",
          "forks_url",
          "commits_url",
          "git_pull_url",
          "git_push_url",
          "html_url",
          "comments_url",
          "public",
          "description",
          "comments",
          "user",
          "files",
          "created_at",
          "updated_at"
        ]
      },
      "url": {
        "type": "string"
      },
      "forks_url": {
        "type": "string"
      },
      "commits_url": {
        "type": "string"
      },
      "id": {
        "type": "string"
      },
      "node_id": {
        "type": "string"
      },
      "git_pull_url": {
        "type": "string"
      },
      "git_push_url": {
        "type": "string"
      },
      "html_url": {
        "type": "string"
      },
      "files": {
        "type": "object",
        "additionalProperties": {
          "type": [
            "object",
            "null"
          ],
          "properties": {
            "filename": {
              "type": "string"
            },
            "type": {
              "type": "string"
            },
            "language": {
              "type": "string"
            },
            "raw_url": {
              "type": "string"
            },
            "size": {
              "type": "integer"
            },
            "truncated": {
              "type": "boolean"
            },
            "content": {
              "type": "string"
            },
            "encoding": {
              "type": "string",
              "description": "The encoding used for `content`. Currently, `\"utf-8\"` and `\"base64\"` are supported.",
              "default": "utf-8"
            }
          }
        }
      },
      "public": {
        "type": "boolean"
      },
      "created_at": {
        "type": "string"
      },
      "updated_at": {
        "type": "string"
      },
      "description": {
        "type": [
          "string",
          "null"
        ]
      },
      "comments": {
        "type": "integer"
      },
      "comments_enabled": {
        "type": "boolean"
      },
      "user": {
        "type": [
          "string",
          "null"
        ]
      },
      "comments_url": {
        "type": "string"
      },
      "owner": {
        "$ref": "#/components/schemas/simple-user"
      },
      "truncated": {
        "type": "boolean"
      }
    }
  }
}
```

### Relationship manifest

```yaml
github_gists:
  user_id:
    target_table: github_users
    target_column: id
    confidence: high
    reason: 'response schema: fork_of.user.id'

```

### FK dependency schemas (for stub creation if needed)

```json
{
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

Resource `gist` uses: alphabet=NUMERIC, length=1

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

Add a class `Gist(Base)` with:

- Table name: `github_gists`
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
