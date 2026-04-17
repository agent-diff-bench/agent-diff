# Entity Implementation (Pass 1 — Base): {{RESOURCE_NAME}}

You are implementing the **{{RESOURCE_NAME}}** resource for the {{APP_NAME}} API
replica. Build the base model, CRUD operations, serializers, and route handlers.

**Do NOT add ForeignKey columns, relationship() declarations, or association
tables in this pass.** Those will be added in a separate step. Focus only on
the resource's own columns, operations, and endpoints.

The full OpenAPI spec is available at: `{{OPENAPI_PATH}}`
If any information in this prompt is unclear or seems incorrect, read the
spec directly to resolve ambiguities.

Files to edit (all under `{{TARGET_DIR}}`):
- `database/schema.py`
- `database/operations.py`
- `core/serializers.py`
- `api/routes.py`

---

## Section 1: {{RESOURCE_NAME}}

### Identity

- Table name: `{{TABLE_NAME}}`
- Model class: `{{MODEL_CLASS_NAME}}`
- Primary key: `{{PRIMARY_KEY}}`

### Schemas

These component schemas represent **{{RESOURCE_NAME}}** in the API. Build your
ORM model to cover the union of all fields across these schemas. Fields that
appear in only some schemas should be nullable.

```json
{{BOUND_SCHEMAS}}
```

### Endpoints

Each entry below is an endpoint that operates on **{{RESOURCE_NAME}}**. Build
one operation function and one route handler per endpoint.

{{ENDPOINTS}}

### Referenced Schemas

These schemas appear in the endpoints above (as response bodies or request
bodies) but are not direct representations of **{{RESOURCE_NAME}}**. They
define the shapes your serializers must produce and your operations must
accept.

```json
{{REFERENCED_SCHEMAS}}
```

---

## Implementation Rules

### Files you will edit

1. **`database/schema.py`** — add the ORM model class
2. **`database/operations.py`** — add CRUD functions
3. **`core/serializers.py`** — add serialization functions
4. **`api/routes.py`** — add handler functions and Route entries

### ORM model (`database/schema.py`)

- Add a class `{{MODEL_CLASS_NAME}}(Base)` with `__tablename__ = "{{TABLE_NAME}}"`
- **Primary key**: look at the `{{PRIMARY_KEY}}` field in the bound schemas —
  check its `type`, `format`, and `examples` to determine the correct column
  type. Use `Integer` for integer IDs, `String(50)` for opaque string IDs,
  `String(36)` for UUID-formatted strings, etc.
- One column per field in the schemas above. Use these type mappings:
  - `string` → `String(N)` or `Text` for long content
  - `integer` → `Integer`
  - `boolean` → `Boolean`
  - `object` (nested) → `JSONB`. Use JSONB for nested objects that represent
    settings, metadata, permissions, file maps, or any structure the API
    returns as-is without filtering on individual sub-fields
  - nullable fields → `Mapped[Optional[T]]` with `nullable=True`
- Store timestamps as `String(50)` when the API returns ISO strings
- Add `is_deleted: Mapped[bool]` with `default=False` for soft-delete support
- **Do NOT add any ForeignKey columns or relationship() declarations** — those
  will be added in Pass 2

### CRUD operations (`database/operations.py`)

- Every function takes `Session` as the first argument
- Use `generate_id("{{ENTITY_SLUG}}")` for new IDs
- Use `now_iso()` for timestamp fields
- Use `session.flush()` after mutations — never `session.commit()`
- Filter out `is_deleted` rows in all read queries
- Cursor pagination: fetch `limit + 1` rows, return next cursor from the last row

### Serializers (`core/serializers.py`)

- Return a dict matching the API response shape exactly
- Use the same key names and casing as the original API
- Include a `serialize_{{ENTITY_SLUG}}_list()` for collection endpoints
- For fields that reference other resources (e.g. `owner`, `user`), serialize
  them as the raw column value for now — Pass 2 will refine these

### Route handlers (`api/routes.py`)

- One async handler per endpoint, following the pattern in the file
- Insert Route entries **above** the `/{_unknown_path:path}` catch-all
- Fixed paths before parameterized paths
- Use `_session(request)`, `_principal_user_id(request)`, `_parse_json_body(request)`,
- **Error responses**: {{IMPLEMENTED_ERRORS}}
  `_pagination_params(request)` from the existing request helpers

### Stubs from previous implementations

Previous resource implementations may have created **stub models** for
{{RESOURCE_NAME}} in `database/schema.py`, marked with
`# STUB — expand when implementing this resource`. If you find a stub
for `{{MODEL_CLASS_NAME}}`, **replace it** with the full implementation.
Do not create a duplicate class — expand the stub in place.

### What NOT to do

- Do not modify `database/base.py`
- Do not remove or modify existing *completed* implementations for other
  resources — but DO expand any stubs that exist for {{RESOURCE_NAME}}
- Do not invent API behavior not present in the endpoint definitions above
- Do not hard-delete records — use soft-delete via `is_deleted`
- Do not add ForeignKey, relationship(), or association tables — Pass 2 handles those

Read the existing files in the target directory before editing. Preserve
all existing code for other resources — add your new models, functions,
and routes alongside what is already there.
