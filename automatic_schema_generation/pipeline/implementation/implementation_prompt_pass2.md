# Entity Implementation (Pass 2 — Relationships): {{RESOURCE_NAME}}

You are adding foreign key relationships to the **{{RESOURCE_NAME}}** resource
(`{{MODEL_CLASS_NAME}}` in `{{TABLE_NAME}}`). The base model, operations,
serializers, and routes already exist from Pass 1.

The full OpenAPI spec is available at: `{{OPENAPI_PATH}}`
If any information in this prompt is unclear or seems incorrect, read the
spec directly to resolve ambiguities.

Read the existing files in the target directory first. You will modify them
to add FK columns, relationship() declarations, indexes, association tables,
and update operations/serializers to handle the new relationships.

Files to edit (all under `{{TARGET_DIR}}`):
- `database/schema.py`
- `database/operations.py`
- `core/serializers.py`
- `api/routes.py`

---

## Relationship Reference Patterns

The examples below are **fictional mocks** showing how each FK relationship
type maps to SQLAlchemy 2.0 models. Use them as structural guidance — do not
copy the mock names or table names.

{{RELATIONSHIP_PATTERNS}}

---

## Related Resources

These resources have a demonstrated relationship with **{{RESOURCE_NAME}}**
through shared endpoints, FK-shaped property names, or schema cross-references.

Direction key:
- **outgoing** — {{RESOURCE_NAME}}'s schemas contain fields that reference
  the related resource (e.g. a `_id` field or nested object pointing there).
  **Action**: add a FK column on `{{TABLE_NAME}}` pointing at the related
  resource's table, plus a `relationship()` on both sides.
- **incoming** — the related resource's endpoints reference {{RESOURCE_NAME}}
  (the subject of those endpoints is the other resource, not {{RESOURCE_NAME}}).
  **Action**: do NOT add a FK column on `{{TABLE_NAME}}`. The FK lives on the
  other resource's table. Add only a `relationship()` on the {{RESOURCE_NAME}}
  side (the "many" side) if the other resource's model already exists or will
  be created as a stub. If the incoming evidence is only URL segments (no
  property-level field), it may just be endpoint nesting — no FK needed.

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

## External Schemas

These schemas reference **{{RESOURCE_NAME}}** but belong to entities that are
**not part of this implementation**. Do NOT create FK columns, relationship
declarations, or stub models for them. They are shown only so you understand
how {{RESOURCE_NAME}} appears in the broader API.

{{EXTERNAL_SCHEMAS}}

---

## Implementation Rules for Pass 2

### What to add

- **FK columns** in `database/schema.py`: add `mapped_column(ForeignKey(...))`
  for each identified relationship. Use the evidence and schema shapes above
  to determine:
  - Which fields become FK columns (look for `_id` suffixed fields, nested
    objects with `id`, and `$ref` pointers to related resource schemas)
  - Whether `nullable=False` (required) or `nullable=True` (optional),
    based on the schema's `required` list
  - The correct column type (must match the target table's PK type)
- **Indexes** in `__table_args__`: add `Index()` for every new FK column
- **relationship() declarations**: add on both sides (this model and the
  target model). Use `foreign_keys=[col]` when multiple FKs point at the
  same table. Use `remote_side=[id]` for self-referential relationships.
- **Association tables**: for M:N relationships, add a `Table()` with
  composite primary key above the model classes
- **Stub models**: if a FK target model does not yet exist in schema.py,
  create a minimal stub marked with `# STUB — expand when implementing this resource`.
  If a stub already exists for the target model, leave it as-is — it will be
  expanded when that resource is implemented
- **Update operations**: for every create/update function that sets a FK
  column, ensure the FK target row exists before flushing. Add a helper
  (e.g. `_ensure_<entity>_stub(session, gid)`) that creates a minimal stub
  row if the target doesn't exist, and call it before assigning the FK
  value. Without this, `session.flush()` will raise a ForeignKeyViolation.
  Also add eager loading (`joinedload`/`selectinload`) where FK-related
  queries need it.
- **Update serializers**: where the API response includes nested related
  objects (not just an ID), update the serializer to include them

### What NOT to do

- Do not modify the base columns, CRUD logic, or route handlers from Pass 1
  unless necessary for FK support
- Do not create FK columns or relationships for entities listed in
  External Schemas — those are context only
- Do not guess relationships that aren't supported by the evidence above
