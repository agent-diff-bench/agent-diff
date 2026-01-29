# Calendar Bench Determinism + Seed Audit (2026-01-23)

Scope: `examples/calendar/testsuites/calendar_bench.json` vs `examples/calendar/seeds/calendar_default.json`.

## Summary
- Tests reviewed: 16
- Deterministic as-is: **test_12, test_15, test_16**
- Conditional / at-risk: **test_1–test_11, test_13, test_14** (see per-test notes)

## Global observations (affect determinism)
1) **FreeBusy ACL gaps**
   - `POST /freeBusy` requires access via CalendarListEntry or ACL. In seed, `test.user@test.com` only has `freeBusyReader` for **Ananya, Zainab, Kwame, Zanele**.
   - Tests requiring availability checks for other users are under-provisioned (see per-test notes).

2) **Relative date anchor required**
   - Tests 1–4 and 9 contain relative date language ("this Saturday", "Sunday morning", "this weekend", "tomorrow").
   - Assertions assume the system prompt sets **today = 2018-06-17 (Sunday)**. Without this, results can drift.

3) **Update-vs-create ambiguity**
   - Several tests assert `diff_type: "changed"` on events or calendars that are **created in the same test**. If an agent sets those fields at creation instead of PATCHing later, there will be no `changed` diff and the test fails.
   - Affected tests: **1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14** (details below).

4) **Soft-delete behavior vs assertions**
   - `events_delete` sets `status = cancelled` (soft delete) and keeps the row. `diff_type: "removed"` would not match unless rows are physically deleted.
   - Several tests use `diff_type: "removed"` for events (e.g., tests 1–9, 13). This may cause deterministic failures even when the agent follows the prompt.
   - `acl_delete` is also soft-delete; **test_10** expects `diff_type: "removed"` for an ACL rule.

5) **Recurring series representation**
   - Tests 13 and 14 require `COUNT` in recurrence, and test 14 requires `EXDATE`. If an agent uses `UNTIL` or cancels an instance instead of `EXDATE`, the assertions fail.

## Per-test checks

### test_1 – Cosmic Voyagers Astronomy Club
- Seed infra: OK (Yuki, Oleksandra, `event_failed_rocket` exist; Oleksandra has a unique free slot on 2018-06-23 19:30–21:00).
- Gaps: **freeBusy ACL missing** for `oleksandra@test.com`.
- Determinism risks:
  - Relative date dependency ("this Saturday").
  - `changed` assertion on newly created watch-party event (location update).

### test_2 – Green Thumbs Urban Garden Collective
- Seed infra: OK (`cal_harvest_schedule`, `event_weed_warrior`, Kenji/Oksana schedules).
- Gaps: **freeBusy ACL missing** for `kenji@test.com` and `oksana@test.com`.
- Determinism risks:
  - Relative date dependency (Sunday/Saturday).
  - `changed` assertions for description and attendees on newly created events.

### test_3 – Dice & Dragons Tabletop Gaming Guild
- Seed infra: OK (`cal_dungeon_masters`, `event_tpk_recovery`, Amara schedule).
- Gaps: **freeBusy ACL missing** for `amara@test.com`.
- Determinism risks:
  - Relative date dependency (Friday/this weekend).
  - `changed` assertion for description on newly created event.

### test_4 – Celluloid Dreams Film Festival
- Seed infra: OK (`cal_celluloid_dreams`, `event_film_022`, intermission events, Takeshi schedule).
- Gaps: **freeBusy ACL missing** for `takeshi@test.com`.
- Determinism risks:
  - Relative date dependency (Saturday afternoon).
  - `changed` assertion for description/attendees on newly created event.

### test_5 – Symposium of Infinite Curiosity
- Seed infra: OK (`cal_symposium_curiosity`, `event_procrastination_workshop`, `event_chiamaka_pres_1`, Bogdan/Ravi schedules).
- Gaps: **freeBusy ACL missing** for `bogdan@test.com` and `ravi@test.com`.
- Determinism risks:
  - `changed` assertion for description on newly created keynote event.

### test_6 – Thunderwave Music Festival
- Seed infra: OK (`cal_thunderwave_festival`, `event_amplifier_incident`, Kofi schedule).
- Gaps: **freeBusy ACL missing** for `kofi@test.com`.
- Determinism risks:
  - `changed` assertions for attendees on newly created DJ Nebula event.

### test_7 – Crypto-Zoology Summit
- Seed infra: OK (`cal_cryptozoology_summit`, `event_bigfoot_workshop`, Zahra schedule).
- Gaps: **freeBusy ACL missing** for `zahra@test.com`.
- Determinism risks:
  - `changed` assertion for attendees on newly created Sasquatch event.

### test_8 – Time-Traveler's Convention
- Seed infra: OK (`cal_timeline_alpha`, `event_grandfather_paradox`, Sven schedule).
- Gaps: **freeBusy ACL missing** for `sven@test.com`.
- Determinism risks:
  - Time choice depends on Sven’s availability but freeBusy access is missing.

### test_9 – Mirage Menagerie Caravan Festival
- Seed infra: OK (`cal_mirage_menagerie`, placeholder events, Ananya/Zainab calendars and freeBusy ACLs, deterministic busy slots for June 23).
- Determinism risks:
  - Relative date dependency (tomorrow = 2018-06-18 per system prompt).
  - `changed` assertions on micro-acts (location + attendee updates) if agent sets these at creation.

### test_10 – Museum of Whispered Relics
- Seed infra: OK (`cal_whispered_relics_mainline`, `cal_embargoed_vault`, `cal_city_archives_access`, ACL for Olena).
- Determinism risks:
  - `changed` assertions for new route calendars if fields are set at creation.
  - **ACL deletion uses `diff_type: removed` but API soft-deletes** (likely `changed`).

### test_11 – Emberline Embassy Network
- Seed infra: OK (`cal_emberline_roster`, `cal_old_courier_shifts`, `cal_consular_blackout`).
- Determinism risks:
  - `changed` assertions for new route calendars if fields are set at creation.

### test_12 – Skyward Observatory Access Passes
- Seed infra: OK (`cal_skyward_observatory`, `cal_dormant_telescopes`, `cal_mountain_weather`, Leila).
- Determinism: **OK** (no relative dates, no freeBusy dependency, no update-vs-create ambiguity).

### test_13 – Firefly Conservatory
- Seed infra: OK (Zanele calendar + freeBusy ACL, `event_broken_jar`).
- Determinism risks:
  - `changed` assertion for Lantern Patrol location if set at creation.
  - Recurrence requires `COUNT=6` (agent might use `UNTIL`).

### test_14 – Clockwork Tinkerers Guild
- Seed infra: OK (pre-seeded `cal_clockwork_tinkerers_guild`).
- Determinism risks:
  - Recurrence requires `COUNT=8` and `EXDATE` (agent may use `UNTIL` or cancelled instance instead).

### test_15 – Tidal Library Rotations
- Seed infra: OK (Fumiko exists; calendar is created in-test).
- Determinism: **OK** (no relative dates, no freeBusy, exceptions allow either EXDATE or cancelled instance; master deletion asserted via status).

### test_16 – Monastery of Echoing Bells
- Seed infra: OK (pre-seeded `cal_monastery_echoing_bells`, Kwame calendar + freeBusy ACL).
- Determinism: **OK** (no relative dates; cancellation allows EXDATE or cancelled instance; uses seeded calendar via `unchanged`).

