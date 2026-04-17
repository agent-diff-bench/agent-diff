# Entity Implementation: {{RESOURCE_NAME}}

You are implementing the **{{RESOURCE_NAME}}** resource for the {{APP_NAME}} API
replica. You will add code to four existing files. Do not create new files.

---

## Relationship Reference Patterns

The examples below are **fictional mocks** showing how each FK relationship
type maps to SQLAlchemy 2.0 models. Use them as structural guidance for
your implementation — do not copy the mock names or table names.

{{RELATIONSHIP_PATTERNS}}

---

## Section 1: This Resource — {{RESOURCE_NAME}}

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

## Section 2: Related Resources

These resources have a demonstrated relationship with **{{RESOURCE_NAME}}**
through shared endpoints, FK-shaped property names, or schema cross-references.

Direction key:
- **outgoing** — {{RESOURCE_NAME}}'s schemas contain fields that reference
  the related resource (e.g. a `_id` field or nested object pointing there)
- **incoming** — the related resource's endpoints reference {{RESOURCE_NAME}}
  (the subject of those endpoints is the other resource, not {{RESOURCE_NAME}})

For each related resource below, **infer the relationship type** from the
evidence and schema shapes:

- **One-to-Many**: this resource carries a FK column pointing at the related
  resource (e.g. `project_id` on a task), OR the related resource carries a
  FK pointing here. Look for singular ID fields and nested objects.
- **Many-to-Many**: both sides reference each other as arrays, or an endpoint
  returns a list of related entities that can independently belong to multiple
  parents. Build an association table.
- **Self-Referential**: a field like `parent_id` points at the same table.
  Use `remote_side=[id]`.

Then build the appropriate FK columns, indexes, and `relationship()`
declarations using the reference patterns above.

{{RELATED_RESOURCES}}

---

## Section 3: External Schemas

These schemas reference **{{RESOURCE_NAME}}** but belong to entities that are
**not part of this implementation**. Do NOT create FK columns, relationship
declarations, or stub models for them. They are shown only so you understand
how {{RESOURCE_NAME}} appears in the broader API.

{{EXTERNAL_SCHEMAS}}

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
  - `object` (nested, not queried) → `JSONB`
  - nullable fields → `Mapped[Optional[T]]` with `nullable=True`
- Store timestamps as `String(50)` when the API returns ISO strings
- Add `is_deleted: Mapped[bool]` with `default=False` for soft-delete support
- **Foreign keys**: use the evidence in Section 2 to identify FK relationships.
  For each related resource, determine:
  - Which fields in this resource's schemas reference the related resource
    (look for `_id` suffixed fields, nested objects with `id`, and `$ref`
    pointers to the related resource's bound schemas)
  - The relationship type: singular nested object or `_id` field → 1:N
    (`ForeignKey`), array of related entities on both sides → M:N
    (association table), self-referencing `parent_id` → self-referential
    (`remote_side=[id]`)
  - Whether the FK is required (`nullable=False`) or optional (`nullable=True`)
    based on the schema's `required` list
- Add `Index()` entries in `__table_args__` for every FK column
- For FK dependencies whose target model does not yet exist in the file,
  create a **stub** marked with `# STUB — expand when implementing this resource`

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

### Route handlers (`api/routes.py`)

- One async handler per endpoint, following the pattern in the file
- Insert Route entries **above** the `/{_unknown_path:path}` catch-all
- Fixed paths before parameterized paths
- Use `_session(request)`, `_principal_user_id(request)`, `_parse_json_body(request)`,
  `_pagination_params(request)` from the existing request helpers

### What NOT to do

- Do not modify `database/base.py`
- Do not remove or modify existing functions — only add new ones
- Do not invent API behavior not present in the endpoint definitions above
- Do not create FK columns or relationships for entities listed in Section 3
- Do not hard-delete records — use soft-delete via `is_deleted`

Read the existing files in the target directory before editing. Preserve
all existing code — add your new models, functions, and routes alongside
what is already there.
