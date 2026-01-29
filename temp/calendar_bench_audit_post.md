# Calendar Bench Determinism Re‑Audit (Post‑Changes)

Date: 2026-01-23

## Result
All protocol issues (3–5) are resolved in the current `calendar_bench.json` and seed. No remaining `removed` assertions, no update‑vs‑create ambiguity, and recurrence expectations are tolerant to alternative encodings.

## Checks Performed
- **Removed vs soft‑delete:** No `diff_type: "removed"` assertions remain.
- **Update‑vs‑create:** All `diff_type: "changed"` assertions target seeded entities only.
- **Recurrence drift:** `COUNT` is no longer required; `EXDATE` assertions are optional (min 0, max 1) in tests 14–16.
- **Calendar ID references:** All `calendar_id: {eq: ...}` targets exist in the seed.
- **FreeBusy access:** `freeBusyReader` ACLs exist for all users referenced in availability checks.

## Notes
- Optional EXDATE assertions appear in tests **14, 15, 16** (all use `{min: 0, max: 1}`).
- Relative date anchor remains consistent with system prompt: **today = June 17, 2018 (Sunday)**.

## Artifacts
- Machine audit data: `temp/calendar_bench_audit_post.json`

