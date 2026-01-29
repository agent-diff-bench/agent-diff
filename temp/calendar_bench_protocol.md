# Calendar Bench Protocol for Issues 3–5

Scope: This protocol standardizes how we avoid (3) update-vs-create ambiguity, (4) soft-delete vs removed mismatches, and (5) recurrence representation drift in calendar bench tests. Apply for current fixes and all future test additions/edits.

## Issue 3 — Update-vs-Create Ambiguity
Problem: Assertions expect `diff_type: "changed"` on resources that could be created with the final values, resulting in no update diff.

Protocol:
1) If the prompt implies a **two-step change** (create then update), prefer **asserting the final state only** and avoid `changed` unless the seed already contains the object.
2) Use `diff_type: "added"` with the final values in `where` for new resources (events/calendars) whenever possible.
3) Only use `diff_type: "changed"` when:
   - The object **exists in seed**, or
   - The prompt explicitly requires an update to a **pre-existing** object (by ID or deterministic lookup).
4) If the prompt must test update behavior on a newly created entity:
   - Add a **seeded placeholder** instance, then update it.
   - Or split into two explicit objects: create one, update the other (seeded).

## Issue 4 — Soft-Delete vs Removed Mismatch
Problem: Calendar delete operations soft-delete (e.g., events set `status = cancelled`, ACL `deleted = true`), so `diff_type: "removed"` can fail.

Protocol:
1) For events, default to asserting **`status: "cancelled"`** on the event row (diff_type `changed`) rather than `removed`.
2) For ACL or calendar list deletions, assert **`deleted: true`** (diff_type `changed`) rather than `removed`.
3) Only use `diff_type: "removed"` when the API truly deletes rows (confirm in code).
4) If test needs to accept either hard-delete or soft-delete, allow both using **optional assertions** (`expected_count: {min: 0, max: 1}`) for each method.

## Issue 5 — Recurrence Representation Drift
Problem: Agents may use `COUNT` vs `UNTIL`, or cancel instances via `EXDATE` vs cancelled instance events.

Protocol:
1) For **series length**, avoid forcing one representation unless required by prompt or product spec:
   - Prefer asserting `FREQ=...` only.
   - If length must be enforced, allow **either** `COUNT` or `UNTIL` using optional assertions.
2) For **cancelled instances**, allow **either**:
   - `EXDATE` in the master recurrence, or
   - a cancelled instance event (status `cancelled` with matching date).
3) For **moved instances**, assert presence of a rescheduled instance event; do not require recurrence changes unless explicit.

## Future Test Review Checklist
- Does the test rely on a two-step create+update? If yes, either seed the object or assert only the final “added” state.
- Are any deletions asserted as `removed`? If yes, confirm the API hard-deletes; otherwise assert soft-delete fields.
- Does recurrence allow multiple valid encodings? If yes, allow both via optional assertions.

