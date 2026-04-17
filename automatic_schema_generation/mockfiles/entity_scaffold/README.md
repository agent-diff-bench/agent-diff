# Entity-Level Scaffold

This directory contains the **prompt template** used when asking an AI agent to
implement a single resource. It is not a code template — it is a structured
instruction set that the pipeline fills in with resource-specific context and
sends to the agent.

## How it works

For each resource in the implementation loop, the pipeline:

1. Reads `entity_implementation_prompt.md`
2. Substitutes the placeholders with resource-specific data:
   - OpenAPI excerpt for this entity
   - Relationship manifest entries for this entity
   - OpenAPI excerpts for FK dependencies
   - Current state of schema.py, operations.py, serializers.py, routes.py
3. Sends the filled prompt to the AI agent
4. Agent returns code edits for the four files
5. Pipeline applies the edits and validates

## What the agent receives

- The entity prompt (this template, filled in)
- The current file contents it may edit
- The OpenAPI excerpt for the entity being implemented
- The relationship manifest entries
- The ID format config for this resource

## What the agent produces

Additions to these existing files (not new files):

- `database/schema.py` — new ORM model class (or expand a STUB)
- `database/operations.py` — new CRUD functions for this entity
- `core/serializers.py` — new serialize functions for this entity
- `api/routes.py` — new handler functions + Route entries

## Operation categories

The agent is instructed to implement only the operations that exist in the
OpenAPI excerpt. Common categories:

| Category | Pattern | Example |
|----------|---------|---------|
| list | `GET /<entities>` | `GET /projects` |
| get | `GET /<entities>/{id}` | `GET /projects/{project_id}` |
| create | `POST /<entities>` | `POST /projects` |
| update | `POST/PATCH/PUT /<entities>/{id}` | `POST /projects/{project_id}` |
| delete | `DELETE /<entities>/{id}` | `DELETE /projects/{project_id}` |
| action | `POST /<entities>/{id}/<action>` | `POST /projects/{project_id}/archive` |
| search | `GET /<entities>/search` | `GET /projects/search` |
| nested list | `GET /<entities>/{id}/<sub>` | `GET /projects/{project_id}/collaborators` |
