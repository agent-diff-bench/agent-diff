# Syntactic alias classification — prompt v1

You are classifying words from an OpenAPI specification into **syntactic aliases** for a fixed list of canonical resource names.

## Definitions

A **syntactic alias** is a word that means *the same entity* as a canonical resource name, just spelled differently. Examples:
- `repo` and `repository` and `repositories` are syntactic aliases for the canonical `repos`.
- `org` and `organization` and `organizations` are syntactic aliases for the canonical `orgs`.
- `user` and `users` are syntactic aliases for each other.

A syntactic alias is **NOT**:
- A **role word** — a word that *points at* a resource without being another name for it. `assignee`, `author`, `reviewer`, `creator`, `owner`, `commenter`, `reporter` all point at users but are not aliases for `users`. Do not classify these as aliases.
- A **derived noun** — `commenter` is not an alias for `comment`, `reporter` is not an alias for `report`.
- A **related-but-distinct entity** — `comment_count` is not an alias for `comment`, `user_profile` is not an alias for `user`.
- A **schema variant** — `TaskCompact`, `UserSummary`, `ProjectMinimal` are partial/compact shapes of the same resource but should not be reported as aliases. The canonical form already covers them.
- A **parent-qualified form** — `parent_task`, `source_project` — these are qualified references, not aliases.

## Task

I will give you:

1. A list of **canonical resource names** (already in their plural form).
2. A list of **candidate words** extracted from the spec's URL segments, schema names, and response body property names.

For each canonical resource, pick the subset of candidate words that are syntactic aliases for it. A word can only be assigned to **one** canonical resource. If a word isn't an alias for any canonical resource, leave it out.

The canonical resource name itself does NOT need to appear in your output — we add it deterministically.

## Output format

Respond with ONLY a JSON object. No prose, no markdown, no code fences. The shape is:

```
{
  "aliases": {
    "<canonical_resource_name>": ["<alias1>", "<alias2>", ...],
    ...
  }
}
```

Every canonical resource must appear as a key, even if its alias list is empty. The alias list must contain only words from the candidate list — do not invent words.

## Inputs

Canonical resources:
{CANONICAL_RESOURCES_JSON}

Candidate vocabulary:
{CANDIDATE_VOCABULARY_JSON}

Respond with the JSON object only.
