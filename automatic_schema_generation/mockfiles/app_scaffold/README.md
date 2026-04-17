# App-Level Scaffold

These files are created **once per app** at the start of generation. They
establish the shared infrastructure that all entity implementations depend on.

## Customization levels

| File | Customization | What varies |
|------|--------------|-------------|
| `database/base.py` | None | Fully universal |
| `core/utils.py` | `ID_FORMATS` dict only | Alphabet + length per resource, derived from OpenAPI examples |
| `core/errors.py` | Error envelope shape | Field names and structure, derived from API docs |
| `database/schema.py` | Starts empty | Entities added one at a time by entity scaffold |
| `database/operations.py` | Starts empty | Functions added one at a time by entity scaffold |
| `core/serializers.py` | Starts empty | Functions added one at a time by entity scaffold |
| `api/routes.py` | Request helpers are universal | Route entries added one at a time by entity scaffold |

## Token placeholders

- `__APP_NAME__` — human-readable name (e.g. "Todoist")
- `__APP_SLUG__` — repo slug (e.g. "todoist")
- `__SERVICE_MOUNT_NAME__` — URL segment (e.g. "todoist")

## Generation flow

1. Copy this scaffold to `backend/src/services/__APP_SLUG__/`
2. Replace token placeholders
3. Fill in `ID_FORMATS` from contract freeze artifacts
4. Fill in error envelope from API docs / live survey
5. Proceed to entity-level scaffolding
