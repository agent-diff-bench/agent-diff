# FK candidate resolution — prompt v1

You are classifying **foreign-key candidates** extracted from an OpenAPI specification. The walker that produced these candidates was deliberately loose: it proposed every field that *might* be a FK and punted the semantic decision to you. Your job is to decide, for each candidate, whether it actually points at one of a fixed list of canonical resources — and if so, which one, and with what cardinality.

## Definitions

A **candidate** is one field (or path/query parameter) on a *source resource*. The walker has already told you:
- which resource owns the field (`source_resource`),
- where inside that resource the field lives (`source_path`),
- what stem the walker tried to resolve (`raw_target`),
- what shape the candidate has (`candidate_type`),
- and a minimal JSON schema fragment for the field itself and, when available, for the target schema it points at.

A **canonical resource** is a plural name from the fixed list I give you. These are the ONLY valid targets. You cannot invent new resources — if a candidate doesn't point at one of these, reject it.

## Decisions

Pick exactly one decision per candidate:

- `linked` — the candidate points at one of the canonical resources. You must provide `target_resource` (one of the canonical names) and `cardinality` (`ONE_TO_MANY` or `MANY_TO_MANY`).
- `rejected` — the walker was wrong: this field is not a reference to any canonical resource. Examples: a free-form label, an enum, a cached denormalized value, a structural ID that names something outside the resource model. Provide a one-line `reason`.
- `cardinality_only` — the candidate is already linked to a target, but the walker couldn't infer the cardinality from shape alone. You must provide `cardinality`. Leave `target_resource` unchanged.

### Cardinality rules

- `ONE_TO_MANY` — the source row points at exactly one (or zero) target rows. Scalar IDs, single `$ref` objects, and single-valued path/query params are all ONE_TO_MANY.
- `MANY_TO_MANY` — the source row points at a collection of target rows. Arrays of `$ref`s, arrays of inline objects with an id field, and plural-name scalar arrays are MANY_TO_MANY.

### Rejection heuristics (when to say `rejected`)

- The field is a free-text name, label, title, or description.
- The field is a status/kind/type enum whose values are strings, not IDs.
- The field is a hash, token, or opaque identifier unrelated to any canonical resource (e.g. a session token, a git sha, a signing key).
- The target the walker proposed (a schema name or field stem) has no canonical resource that matches it, not even by looser semantic matching. For example, `tag_name` is probably not a reference to a `tags` resource if `tags` isn't in the canonical list.
- The field is a counter or aggregate (`comment_count`, `star_count`).

**Trust the walker's shape signal.** If `candidate_type` is `NESTED_REF` and the target schema clearly represents an entity in the canonical list, link it. Don't second-guess obvious cases.

### Self-references

If a candidate's most natural target is the source resource itself (e.g. `User.manager: $ref User`, `Task.parent_task_id`), mark it `linked` with `target_resource` equal to the source resource. Self-references are valid.

## Inputs

Canonical resources (the only valid `target_resource` values):
{CANONICAL_RESOURCES_JSON}

Known syntactic aliases (each canonical resource and the words that already map to it):
{RESOURCE_ALIASES_JSON}

Candidates to resolve:
{CANDIDATES_JSON}

## Output format

Respond with ONLY a JSON object. No prose, no markdown, no code fences. The shape is:

```
{
  "resolutions": [
    {
      "id": <integer — the id from the candidate input>,
      "decision": "linked" | "rejected" | "cardinality_only",
      "target_resource": "<canonical_resource_name>" | null,
      "cardinality": "ONE_TO_MANY" | "MANY_TO_MANY" | null,
      "reason": "<one-line justification>"
    },
    ...
  ]
}
```

Every candidate id in the input must appear exactly once in your `resolutions` array. `target_resource` must be either `null` (for `rejected`) or one of the canonical resources — do not invent names. `cardinality` must be non-null when `decision` is `linked` or `cardinality_only`.

Respond with the JSON object only.
