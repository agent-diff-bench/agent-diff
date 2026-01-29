# Generated Google Calendar Benchmark Prompts

This file contains 3 prompts generated using the following procedure:
1. Sample n from range 7-13
2. Sample n endpoints with replacement from the 8 selected endpoints
3. Sample m from range 1-6 for unique names
4. Generate m names from diverse cultural traditions
5. Create action sequence with creative theme and justify each step
6. Generate natural prompt that forces all steps without revealing sequence

---

# PROMPT 1: Cosmic Voyagers Astronomy Club

## Step 1: Sample n
**n = 9** (sampled from range 7-13)

## Step 2: Sample 9 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `POST /calendars` | Calendars: insert |
| 3 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 4 | `POST /calendars/{calendarId}/events` | Events: insert |
| 5 | `POST /freeBusy` | Freebusy: query |
| 6 | `POST /calendars/{calendarId}/events` | Events: insert |
| 7 | `GET /calendars/{calendarId}/events` | Events: list |
| 8 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 9 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |

## Step 3: Sample m
**m = 3** (sampled from range 1-6)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Yuki** | Japanese |
| **Oleksandra** | Ukrainian |
| **Chidi** | Nigerian (Igbo) |

## Step 5: Action Sequence with Justification

**Theme:** Amateur astronomy club organizing stargazing events

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Check what calendars currently exist | `GET /users/me/calendarList` | Need to see if an astronomy calendar already exists before creating one |
| 2 | Create a new calendar called "Cosmic Voyagers HQ" | `POST /calendars` | The club needs a dedicated calendar for all space-related events |
| 3 | Share "Cosmic Voyagers HQ" with Yuki (yuki@test.com) as writer | `POST /calendars/{calendarId}/acl` | Yuki is the co-organizer and needs to add events too |
| 4 | Create "Perseid Meteor Shower Watch Party" on the new calendar for Saturday midnight | `POST /calendars/{calendarId}/events` | The annual meteor shower is coming up - first major event |
| 5 | Check when Oleksandra (oleksandra@test.com) is free on Saturday evening | `POST /freeBusy` | Need to find the right time for a pre-event telescope setup session |
| 6 | Create "Telescope Alignment Ceremony" at a time when Oleksandra is available | `POST /calendars/{calendarId}/events` | Someone needs to calibrate the equipment before the watch party |
| 7 | List all events on "Cosmic Voyagers HQ" to review the schedule | `GET /calendars/{calendarId}/events` | Verify both events are properly scheduled |
| 8 | Update "Perseid Meteor Shower Watch Party" location to "Hillcrest Observatory Field" | `PATCH /calendars/{calendarId}/events/{eventId}` | Location was TBD when created, now confirmed |
| 9 | Delete the old "Failed Rocket Launch Viewing (Cancelled)" from primary calendar | `DELETE /calendars/{calendarId}/events/{eventId}` | Clean up embarrassing cancelled event from last month |

## Step 6: Generated Prompt

> "Our astronomy club is getting serious and we need proper organization. First, show me what calendars I have - I want to make sure we're not duplicating anything. Create a dedicated calendar called 'Cosmic Voyagers HQ' for all our stargazing activities. Yuki (yuki@test.com) is my co-organizer, so give her write access to the new calendar. The Perseid meteor shower is this Saturday at midnight - create an event called 'Perseid Meteor Shower Watch Party' for it on our new calendar. Before the main event, we need to set up the telescopes, but it has to work with Oleksandra's schedule (oleksandra@test.com) - find when she's free Saturday evening and create a 'Telescope Alignment Ceremony' at that time. Once both events are created, show me everything on the Cosmic Voyagers calendar so I can review. Oh, I just remembered - the watch party location is confirmed as 'Hillcrest Observatory Field', so update that event. Also, there's still that embarrassing 'Failed Rocket Launch Viewing (Cancelled)' event on my main calendar from when SpaceX scrubbed last month - please delete it."

---

# PROMPT 2: Green Thumbs Urban Garden Collective

## Step 1: Sample n
**n = 11** (sampled from range 7-13)

## Step 2: Sample 11 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events` | Events: insert |
| 2 | `GET /calendars/{calendarId}/events` | Events: list |
| 3 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 4 | `POST /freeBusy` | Freebusy: query |
| 5 | `GET /users/me/calendarList` | CalendarList: list |
| 6 | `POST /calendars/{calendarId}/events` | Events: insert |
| 7 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 8 | `GET /calendars/{calendarId}/events` | Events: list |
| 9 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 10 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 11 | `POST /calendars` | Calendars: insert |

## Step 3: Sample m
**m = 4** (sampled from range 1-6)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Kenji** | Japanese |
| **Oksana** | Ukrainian |
| **Chisom** | Nigerian (Igbo) |
| **Dariush** | Iranian/Persian |

## Step 5: Action Sequence with Justification

**Theme:** Community urban garden collective coordinating planting and harvest

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create "Sacred Tomato Planting Ritual" on primary calendar for Sunday morning | `POST /calendars/{calendarId}/events` | Urgent - tomato season is starting, need to block the time immediately |
| 2 | List all events on primary calendar for this week | `GET /calendars/{calendarId}/events` | See what else is happening this week to avoid conflicts |
| 3 | Update "Sacred Tomato Planting Ritual" to add description "Bring your own seedlings and prayers" | `PATCH /calendars/{calendarId}/events/{eventId}` | Realized we need to tell people what to bring |
| 4 | Check when Kenji (kenji@test.com) and Oksana (oksana@test.com) are both free on Saturday | `POST /freeBusy` | Need to schedule a compost committee meeting with both |
| 5 | Show me all my calendars | `GET /users/me/calendarList` | Looking for the "Harvest Schedule" calendar to add events there |
| 6 | Create "Compost Communion: The Turning of the Heap" on "Harvest Schedule" at their available time | `POST /calendars/{calendarId}/events` | The sacred compost turning ceremony with both members |
| 7 | Delete "Weed Warrior Wednesday" from "Harvest Schedule" - it was rained out | `DELETE /calendars/{calendarId}/events/{eventId}` | Cancelled due to weather, need to remove it |
| 8 | List events on "Harvest Schedule" to verify deletion | `GET /calendars/{calendarId}/events` | Confirm the cancelled event is gone |
| 9 | Share "Harvest Schedule" with Chisom (chisom@test.com) as reader | `POST /calendars/{calendarId}/acl` | New member needs to see when harvests are happening |
| 10 | Update "Compost Communion" to include Dariush (dariush@test.com) as attendee | `PATCH /calendars/{calendarId}/events/{eventId}` | Forgot to invite the soil expert |
| 11 | Create a new calendar called "Greenhouse Experiments" | `POST /calendars` | Starting a new initiative for experimental growing techniques |

## Step 6: Generated Prompt

> "Tomato season waits for no one - create 'Sacred Tomato Planting Ritual' on my calendar for Sunday morning immediately. Then show me what else I have this week so we don't double-book the garden crew. That tomato event needs more details - update it to say 'Bring your own seedlings and prayers' in the description. For the compost committee, I need to find a time Saturday when both Kenji (kenji@test.com) and Oksana (oksana@test.com) can make it. Speaking of which, which of my calendars is the 'Harvest Schedule' one? Once you find it, create 'Compost Communion: The Turning of the Heap' on that calendar at whatever time works for Kenji and Oksana. Bad news - 'Weed Warrior Wednesday' got rained out, so delete it from the Harvest Schedule and confirm it's actually gone. We have a new collective member, Chisom (chisom@test.com), who needs to see the harvest calendar but shouldn't edit it - set that up. Also, I completely forgot to invite Dariush (dariush@test.com) to the compost thing - he's our soil whisperer, please add him. One last thing: we're starting a new experimental growing project and need a calendar called 'Greenhouse Experiments' for it."

---

# PROMPT 3: Dice & Dragons Tabletop Gaming Guild

## Step 1: Sample n
**n = 8** (sampled from range 7-13)

## Step 2: Sample 8 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `POST /calendars/{calendarId}/events` | Events: insert |
| 3 | `POST /freeBusy` | Freebusy: query |
| 4 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 5 | `GET /calendars/{calendarId}/events` | Events: list |
| 6 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 7 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 8 | `POST /calendars` | Calendars: insert |

## Step 3: Sample m
**m = 2** (sampled from range 1-6)

## Step 4: Generate 2 Names
| Name | Origin |
|------|--------|
| **Amara** | Nigerian (Igbo) |
| **Hiroshi** | Japanese |

## Step 5: Action Sequence with Justification

**Theme:** Tabletop gaming guild organizing D&D campaigns and board game nights

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List all calendars to find the "Dungeon Masters Guild" calendar | `GET /users/me/calendarList` | Need to locate the right calendar before adding campaign sessions |
| 2 | Create "The Curse of the Crimson Dice: Session Zero" on "Dungeon Masters Guild" for Friday 7pm | `POST /calendars/{calendarId}/events` | New campaign is starting, need to schedule character creation session |
| 3 | Check when Amara (amara@test.com) is free this weekend | `POST /freeBusy` | She's the guest DM for a one-shot, need to find her availability |
| 4 | Update "The Curse of the Crimson Dice: Session Zero" description to "Bring character concepts. Snacks provided. No phones at the table." | `PATCH /calendars/{calendarId}/events/{eventId}` | Players need to know the rules and expectations |
| 5 | List all events on "Dungeon Masters Guild" for this month | `GET /calendars/{calendarId}/events` | See the full campaign schedule and identify conflicts |
| 6 | Share "Dungeon Masters Guild" calendar with Hiroshi (hiroshi@test.com) as writer | `POST /calendars/{calendarId}/acl` | He's becoming a regular DM and needs to schedule his own sessions |
| 7 | Delete "TPK Recovery Support Group (Postponed Indefinitely)" from the guild calendar | `DELETE /calendars/{calendarId}/events/{eventId}` | The joke event is cluttering up the schedule |
| 8 | Create new calendar called "Board Game Bazaar" | `POST /calendars` | Separating board game nights from RPG sessions for clarity |

## Step 6: Generated Prompt

> "The guild needs organizing. First, remind me which calendars I have - I'm looking for our 'Dungeon Masters Guild' one. We're kicking off a new campaign called 'The Curse of the Crimson Dice' and I need to schedule Session Zero for Friday at 7pm on that calendar. Amara (amara@test.com) offered to run a one-shot this weekend but I need to find when she's actually free first. Oh, and that Session Zero event needs more info - update the description to say 'Bring character concepts. Snacks provided. No phones at the table.' I want to see all the sessions we have planned this month on the guild calendar. Hiroshi (hiroshi@test.com) has been running great sessions and deserves to schedule his own games now - give him edit access to the Dungeon Masters Guild calendar. That old 'TPK Recovery Support Group (Postponed Indefinitely)' event is still sitting there as a bad joke from when we had that campaign wipe - delete it. Finally, we've been mixing board game nights with RPG sessions and it's confusing people. Create a separate calendar called 'Board Game Bazaar' for non-RPG gaming."

---

# PROMPT 4: Celluloid Dreams International Film Festival (PAGINATION REQUIRED)

**Special Constraint:** This prompt requires handling large result sets that may overflow pagination limits.

## Step 1: Sample n
**n = 10** (sampled from range 7-13)

## Step 2: Sample 10 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `GET /calendars/{calendarId}/events` | Events: list **(PAGINATION - 200+ screenings)** |
| 3 | `POST /calendars/{calendarId}/events` | Events: insert |
| 4 | `POST /freeBusy` | Freebusy: query |
| 5 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 6 | `GET /calendars/{calendarId}/events` | Events: list **(PAGINATION - count verification)** |
| 7 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 8 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 9 | `POST /calendars` | Calendars: insert |
| 10 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |

## Step 3: Sample m
**m = 3** (sampled from range 1-6)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Takeshi** | Japanese |
| **Olena** | Ukrainian |
| **Adaeze** | Nigerian (Igbo) |

## Step 5: Action Sequence with Justification

**Theme:** International film festival with 200+ scheduled screenings across multiple venues

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List all calendars to find "Celluloid Dreams Festival 2026" | `GET /users/me/calendarList` | Festival has a dedicated calendar with all 200+ screenings |
| 2 | **List ALL events on the festival calendar and count how many screenings are scheduled in "Noir Dungeon" venue** | `GET /calendars/{calendarId}/events` | **PAGINATION REQUIRED**: The calendar has 200+ film screenings. Agent must page through all results to count events where location contains "Noir Dungeon". Expected: ~45 screenings at that venue. |
| 3 | Create "Emergency Projector Repair: The Reel Must Go On" blocking 2 hours on Saturday afternoon | `POST /calendars/{calendarId}/events` | Technical emergency - need to block time for equipment repair |
| 4 | Check when Takeshi (takeshi@test.com) is free on Saturday | `POST /freeBusy` | Takeshi is the projectionist who needs to be present for repair |
| 5 | Update "Emergency Projector Repair" to add Takeshi as attendee and note "Bring spare bulbs and prayers" | `PATCH /calendars/{calendarId}/events/{eventId}` | Need to assign the right technician and provide instructions |
| 6 | **List ALL events again and find any screening titled "The Last Samurai of Saturn" to get its exact time** | `GET /calendars/{calendarId}/events` | **PAGINATION REQUIRED**: Must search through 200+ events to find this specific film. It's somewhere in the schedule but we don't know when. |
| 7 | Delete "Intermission: Existential Crisis (15 min)" - we're cutting intermissions to fit more films | `DELETE /calendars/{calendarId}/events/{eventId}` | Schedule is tight, removing unnecessary breaks |
| 8 | Share "Celluloid Dreams Festival 2026" with Olena (olena@test.com) as reader | `POST /calendars/{calendarId}/acl` | Olena is a film critic who needs to see the full schedule for coverage planning |
| 9 | Create new calendar "Green Room Chaos" for backstage coordination | `POST /calendars` | Need separate calendar for crew logistics that shouldn't be public |
| 10 | Update "The Last Samurai of Saturn" (found in step 6) to change venue to "Grand Aurora Theater" | `PATCH /calendars/{calendarId}/events/{eventId}` | Moving the flagship screening to a larger venue due to demand |

## Step 6: Generated Prompt

> "The Celluloid Dreams Film Festival is in full swing and I'm drowning in logistics. First, find our main festival calendar - it's called 'Celluloid Dreams Festival 2026'. I need you to go through the entire screening schedule (we have over 200 films programmed) and tell me exactly how many are showing at the 'Noir Dungeon' venue - I'm worried we overbooked that theater. While you're at it, create an emergency event called 'Emergency Projector Repair: The Reel Must Go On' for Saturday afternoon, 2 hours - one of our projectors is dying. Takeshi (takeshi@test.com) is our miracle-worker projectionist, so check if he's free Saturday and add him to that repair event with a note saying 'Bring spare bulbs and prayers'. Here's a problem: we have this highly anticipated screening of 'The Last Samurai of Saturn' but I can't remember when it's scheduled - find it in our massive schedule. Also, delete all the 'Intermission: Existential Crisis (15 min)' events - we're cutting breaks to squeeze in more films. Olena (olena@test.com) from The Kyiv Film Review needs to see our complete schedule for her coverage - give her read access. Create a new private calendar called 'Green Room Chaos' for backstage crew coordination. Oh, and once you find 'The Last Samurai of Saturn', move it to the 'Grand Aurora Theater' - ticket demand is through the roof."

---

## Pagination Requirements Analysis

This prompt **explicitly requires handling pagination** because:

1. **Step 2 - Count by Venue**: The agent must iterate through ALL 200+ events to count those at "Noir Dungeon". With typical page sizes of 50-100, this requires 2-4 API calls with `pageToken` handling.

2. **Step 6 - Search by Title**: Finding "The Last Samurai of Saturn" among 200+ events requires exhaustive search. The film could be on page 1, page 3, or the last page - agent cannot shortcut.

3. **Data Dependency**: Step 10 depends on Step 6 succeeding - if pagination is handled incorrectly and the film isn't found, the final update will fail.

**Expected Agent Behavior:**
```
# Pseudo-code the agent should effectively implement:
all_events = []
page_token = None
while True:
    response = GET /calendars/{calendarId}/events?pageToken={page_token}
    all_events.extend(response.items)
    page_token = response.get('nextPageToken')
    if not page_token:
        break
# Now process all_events for counting/searching
```

---

# PROMPT 5: Symposium of Infinite Curiosity - Academic Conference (PAGINATION REQUIRED)

**Special Constraint:** This prompt requires handling large result sets that may overflow pagination limits.

## Step 1: Sample n
**n = 12** (sampled from range 7-13)

## Step 2: Sample 12 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `GET /calendars/{calendarId}/events` | Events: list **(PAGINATION - 150+ sessions)** |
| 3 | `POST /calendars/{calendarId}/events` | Events: insert |
| 4 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 5 | `POST /freeBusy` | Freebusy: query |
| 6 | `POST /calendars/{calendarId}/events` | Events: insert |
| 7 | `GET /calendars/{calendarId}/events` | Events: list **(PAGINATION - filter by speaker)** |
| 8 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 9 | `POST /calendars` | Calendars: insert |
| 10 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 11 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 12 | `GET /calendars/{calendarId}/events` | Events: list **(PAGINATION - final verification)** |

## Step 3: Sample m
**m = 5** (sampled from range 1-6)

## Step 4: Generate 5 Names
| Name | Origin |
|------|--------|
| **Mei-Lin** | Chinese |
| **Bogdan** | Ukrainian |
| **Chiamaka** | Nigerian (Igbo) |
| **Ravi** | Indian |
| **Ingrid** | Norwegian/Nordic |

## Step 5: Action Sequence with Justification

**Theme:** Multi-day academic conference with 150+ paper presentations, workshops, and keynotes

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List all calendars to find "Symposium of Infinite Curiosity 2026" | `GET /users/me/calendarList` | Conference has dedicated calendar with full academic program |
| 2 | **List ALL sessions and count how many are tagged as "Quantum" track in title/description** | `GET /calendars/{calendarId}/events` | **PAGINATION REQUIRED**: 150+ sessions across 5 tracks. Must page through all to count Quantum track sessions. Expected: ~32 sessions. |
| 3 | Create "Keynote: The Heresy of Obvious Conclusions" by Mei-Lin for Day 1 opening | `POST /calendars/{calendarId}/events` | Featured speaker's keynote needs to be added to the schedule |
| 4 | Update the keynote to add description "Mandatory attendance for all track chairs. Coffee will be existential." | `PATCH /calendars/{calendarId}/events/{eventId}` | Keynote details need to be specified for attendees |
| 5 | Check when Bogdan (bogdan@test.com) and Ravi (ravi@test.com) are both free on Day 2 afternoon | `POST /freeBusy` | Need to schedule an emergency program committee meeting |
| 6 | Create "Secret Tribunal of the Program Committee" at their available time | `POST /calendars/{calendarId}/events` | Emergency meeting to discuss a controversial paper submission |
| 7 | **List ALL sessions and find every presentation by Dr. Chiamaka (chiamaka@test.com) - she has 4 scattered across 3 days** | `GET /calendars/{calendarId}/events` | **PAGINATION REQUIRED**: Must search 150+ events to find all 4 of her sessions for schedule conflict checking |
| 8 | Delete "Workshop: Introduction to Procrastination (Postponed)" from the schedule | `DELETE /calendars/{calendarId}/events/{eventId}` | Ironic workshop that was postponed indefinitely |
| 9 | Create new calendar "Speakers' Green Room of Mild Panic" | `POST /calendars` | Private calendar for speaker logistics and AV setup times |
| 10 | Share "Symposium of Infinite Curiosity 2026" with Ingrid (ingrid@test.com) as writer | `POST /calendars/{calendarId}/acl` | Ingrid is the new volunteer coordinator and needs to add helper shifts |
| 11 | Update the first of Chiamaka's presentations (found in step 7) to change room to "Hall of Disputed Theories" | `PATCH /calendars/{calendarId}/events/{eventId}` | Room reassignment due to expected high attendance |
| 12 | **List ALL sessions one final time and verify total count matches expected 147 after deletion** | `GET /calendars/{calendarId}/events` | **PAGINATION REQUIRED**: Final verification that schedule integrity is maintained |

## Step 6: Generated Prompt

> "The Symposium of Infinite Curiosity is three weeks away and the program is chaos. Find our main calendar - 'Symposium of Infinite Curiosity 2026'. We have over 150 sessions scheduled and I need an exact count of how many are in the 'Quantum' track (they'll have Quantum in the title). Add Mei-Lin's opening keynote - it's called 'Keynote: The Heresy of Obvious Conclusions' and should be the first thing on Day 1 morning. Update that keynote with a description: 'Mandatory attendance for all track chairs. Coffee will be existential.' Bogdan (bogdan@test.com) and Ravi (ravi@test.com) need to meet urgently on Day 2 afternoon to discuss a problematic submission - find when they're both free and create 'Secret Tribunal of the Program Committee' at that time. Dr. Chiamaka (chiamaka@test.com) is presenting four different papers across the conference and I can't find them all - search the entire schedule and tell me when each of her sessions is. Someone finally noticed the irony: 'Workshop: Introduction to Procrastination (Postponed)' - delete it. Create a private calendar called 'Speakers' Green Room of Mild Panic' for backstage coordination. Ingrid (ingrid@test.com) just joined as volunteer coordinator - give her edit access to the main symposium calendar. Chiamaka's first presentation needs to move to 'Hall of Disputed Theories' due to popularity - update it. Finally, after all these changes, verify our total session count - we should have exactly 147 sessions remaining."

---

## Pagination Requirements Analysis (Prompt 5)

Three explicit pagination scenarios:
1. **Step 2 - Count by Track**: Count all "Quantum" sessions among 150+ events
2. **Step 7 - Find by Speaker**: Locate all 4 of Chiamaka's presentations scattered across the schedule
3. **Step 12 - Verify Total Count**: Count all remaining sessions to verify exactly 147

---

# PROMPT 6: Thunderwave Music Festival - Multi-Stage Extravaganza (PAGINATION REQUIRED)

**Special Constraint:** This prompt requires handling large result sets that may overflow pagination limits.

## Step 1: Sample n
**n = 9** (sampled from range 7-13)

## Step 2: Sample 9 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `GET /calendars/{calendarId}/events` | Events: list **(PAGINATION - 180+ performances)** |
| 3 | `POST /freeBusy` | Freebusy: query |
| 4 | `POST /calendars/{calendarId}/events` | Events: insert |
| 5 | `GET /calendars/{calendarId}/events` | Events: list **(PAGINATION - find by genre)** |
| 6 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 7 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 8 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 9 | `POST /calendars` | Calendars: insert |

## Step 3: Sample m
**m = 4** (sampled from range 1-6)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Kofi** | Ghanaian |
| **Yuna** | Korean |
| **Petro** | Ukrainian |
| **Sakura** | Japanese |

## Step 5: Action Sequence with Justification

**Theme:** 3-day outdoor music festival with 180+ performances across 6 stages

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List all calendars to find "Thunderwave Festival 2026" | `GET /users/me/calendarList` | Festival master calendar with all stage schedules |
| 2 | **List ALL performances and identify which acts are playing the "Volcano Stage" - count them** | `GET /calendars/{calendarId}/events` | **PAGINATION REQUIRED**: 180+ performances across 6 stages. Must page through all to find ~28 Volcano Stage acts. |
| 3 | Check when Kofi (kofi@test.com) the stage manager is free on Saturday afternoon | `POST /freeBusy` | Need to schedule emergency sound check for headliner |
| 4 | Create "Sacred Sound Ritual: DJ Nebula's Sunrise Set" for Sunday 5am on "Ethereal Meadow Stage" | `POST /calendars/{calendarId}/events` | Last-minute addition - secret sunrise DJ set |
| 5 | **List ALL performances and find every act tagged [METAL] in the title - there should be exactly 23** | `GET /calendars/{calendarId}/events` | **PAGINATION REQUIRED**: Must search 180+ events to verify metal lineup is complete. Festival director worried some bands were dropped. |
| 6 | Update "Sacred Sound Ritual: DJ Nebula's Sunrise Set" to add Yuna (yuna@test.com) and Petro (petro@test.com) as attendees - they're the light/sound crew | `PATCH /calendars/{calendarId}/events/{eventId}` | Crew needs to know about the secret set for logistics |
| 7 | Delete "The Amplifier Incident Investigation (Staff Only)" - issue was resolved | `DELETE /calendars/{calendarId}/events/{eventId}` | The blown amplifier mystery was solved, meeting cancelled |
| 8 | Share "Thunderwave Festival 2026" with Sakura (sakura@test.com) as reader | `POST /calendars/{calendarId}/acl` | Sakura is the photographer and needs full schedule visibility for shot planning |
| 9 | Create new calendar "Artist Hospitality: Demands & Disasters" | `POST /calendars` | Private calendar for tracking rider requests and diva moments |

## Step 6: Generated Prompt

> "Thunderwave Festival is about to explode and I need clarity on the chaos. Find the 'Thunderwave Festival 2026' calendar. We have 180+ performances booked across 6 stages and I need to know exactly how many acts are playing the 'Volcano Stage' - go through the entire schedule and count them. Kofi (kofi@test.com) is our Volcano Stage manager - check when he's free Saturday afternoon because we need an emergency sound check. We just confirmed a secret sunrise set - create 'Sacred Sound Ritual: DJ Nebula's Sunrise Set' for Sunday at 5am on 'Ethereal Meadow Stage'. Here's my panic: I'm worried we accidentally dropped some metal bands from the lineup. Search the ENTIRE schedule and find every act with [METAL] in the title - there should be exactly 23 of them, confirm this. For the sunrise set, add Yuna (yuna@test.com) and Petro (petro@test.com) as attendees - they're running lights and sound. Good news: 'The Amplifier Incident Investigation (Staff Only)' can be deleted - we found the culprit (it was a rogue beer). Sakura (sakura@test.com) is our festival photographer and needs to see the complete schedule to plan her shots - give her read access. Finally, create a private calendar called 'Artist Hospitality: Demands & Disasters' for tracking the ridiculous rider requests."

---

## Pagination Requirements Analysis (Prompt 6)

Two explicit pagination scenarios:
1. **Step 2 - Count by Stage**: Count all Volcano Stage performances among 180+ events
2. **Step 5 - Find by Tag**: Search and verify exactly 23 [METAL] tagged performances

---

# PROMPT 7: The Intergalactic Crypto-Zoology Summit

## Step 1: Sample n
**n = 10** (sampled from range 7-13)

## Step 2: Sample 10 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars` | Calendars: insert |
| 2 | `GET /users/me/calendarList` | CalendarList: list |
| 3 | `POST /calendars/{calendarId}/events` | Events: insert |
| 4 | `POST /freeBusy` | Freebusy: query |
| 5 | `POST /calendars/{calendarId}/events` | Events: insert |
| 6 | `GET /calendars/{calendarId}/events` | Events: list |
| 7 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 8 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 9 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 10 | `GET /calendars/{calendarId}/events` | Events: list |

## Step 3: Sample m
**m = 3** (sampled from range 1-6)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Zahra** | Iranian |
| **Mateusz** | Polish |
| **Aarav** | Indian |

## Step 5: Action Sequence with Justification

**Theme:** A summit for researchers of mythical creatures (Bigfoot, Yeti, Nessie, etc.)

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a new calendar called "Crypto-Zoology Summit 2026" | `POST /calendars` | Need a dedicated space for the summit schedule |
| 2 | List all calendars to get the ID of the new calendar | `GET /users/me/calendarList` | Need the ID to add events to it (simulating agent flow) |
| 3 | Create "Keynote: The Sasquatch Migration Patterns" for Day 1 at 9am | `POST /calendars/{calendarId}/events` | The opening talk of the summit |
| 4 | Check when Zahra (zahra@test.com) is free on Day 1 afternoon | `POST /freeBusy` | She's the leading expert on sea monsters, need to schedule her panel |
| 5 | Create "Panel: Nessie vs. Ogopogo - A Comparative Analysis" at Zahra's available time | `POST /calendars/{calendarId}/events` | The debate everyone is waiting for |
| 6 | List all events on the summit calendar to review the schedule | `GET /calendars/{calendarId}/events` | Checking for conflicts or missing details |
| 7 | Update "Keynote: The Sasquatch Migration Patterns" to add Mateusz (mateusz@test.com) as a speaker (attendee) | `PATCH /calendars/{calendarId}/events/{eventId}` | Mateusz just confirmed he can co-present |
| 8 | Delete "Workshop: How to Fake Bigfoot Prints (Cancelled)" | `DELETE /calendars/{calendarId}/events/{eventId}` | The ethics committee vetoed this workshop |
| 9 | Share "Crypto-Zoology Summit 2026" with Aarav (aarav@test.com) as reader | `POST /calendars/{calendarId}/acl` | Aarav is the press liaison and needs to see the schedule |
| 10 | List events again to confirm the workshop is deleted and schedule is final | `GET /calendars/{calendarId}/events` | Final verification step |

## Step 6: Generated Prompt

> "We're hosting the Intergalactic Crypto-Zoology Summit 2026 and I need you to set up the schedule. Start by creating a dedicated calendar for it. Once that's ready, schedule the opening keynote 'The Sasquatch Migration Patterns' for 9am on Day 1. I need to schedule the main debate panel, 'Nessie vs. Ogopogo - A Comparative Analysis', but it depends on Zahra's (zahra@test.com) availability in the afternoon of Day 1 - find a slot when she's free and book it. Mateusz (mateusz@test.com) just agreed to co-present the Sasquatch keynote, so please add him to that event. I think I accidentally added a workshop called 'How to Fake Bigfoot Prints' earlier - if it's there, delete it immediately, we can't have that on the official record. Aarav (aarav@test.com) from the press office needs read access to the full calendar. Finally, show me the complete, cleaned-up schedule so I can sign off on it."

---

# PROMPT 8: The Great Time-Traveler's Convention

## Step 1: Sample n
**n = 8** (sampled from range 7-13)

## Step 2: Sample 8 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `POST /calendars` | Calendars: insert |
| 3 | `POST /calendars/{calendarId}/events` | Events: insert |
| 4 | `POST /freeBusy` | Freebusy: query |
| 5 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 6 | `GET /calendars/{calendarId}/events` | Events: list |
| 7 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 8 | `POST /calendars/{calendarId}/acl` | Acl: insert |

## Step 3: Sample m
**m = 2** (sampled from range 1-6)

## Step 4: Generate 2 Names
| Name | Origin |
|------|--------|
| **Sven** | Swedish |
| **Fatima** | Arabic |

## Step 5: Action Sequence with Justification

**Theme:** A convention for time travelers (past, present, and future)

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List calendars to check for existing "Timeline Alpha" | `GET /users/me/calendarList` | Need to ensure we don't cause a paradox by duplicating the timeline |
| 2 | Create new calendar "Timeline Beta" | `POST /calendars` | Creating a safe space for temporal experiments |
| 3 | Create "Paradox Prevention Seminar" on "Timeline Beta" for next Tuesday | `POST /calendars/{calendarId}/events` | Mandatory safety briefing for all attendees |
| 4 | Check when Sven (sven@test.com) is free next Wednesday | `POST /freeBusy` | Sven is the keynote speaker from the year 2099 |
| 5 | Update "Paradox Prevention Seminar" to move it to Sven's available slot on Wednesday | `PATCH /calendars/{calendarId}/events/{eventId}` | Sven missed his original arrival window, need to reschedule |
| 6 | List events on "Timeline Beta" to verify the shift | `GET /calendars/{calendarId}/events` | Confirming the timeline has been altered successfully |
| 7 | Delete "Grandfather Paradox Demonstration" | `DELETE /calendars/{calendarId}/events/{eventId}` | Deemed too dangerous by the Time Council |
| 8 | Share "Timeline Beta" with Fatima (fatima@test.com) as writer | `POST /calendars/{calendarId}/acl` | Fatima is the archivist ensuring history is recorded correctly |

## Step 6: Generated Prompt

> "We're setting up the Time-Traveler's Convention and the timeline is fragile. First, check if 'Timeline Alpha' already exists in my calendars. Regardless, create a new calendar called 'Timeline Beta' for our experiments. Schedule the 'Paradox Prevention Seminar' for next Tuesday on this new calendar. Sven (sven@test.com) is arriving from 2099 and needs to attend, but his arrival window is fluctuating - check his availability for next Wednesday instead. Move the 'Paradox Prevention Seminar' to a time when Sven is free on Wednesday. Verify the shift by showing me the updated schedule for Timeline Beta. The Time Council has flagged the 'Grandfather Paradox Demonstration' as a Class 5 risk - if you see it on the schedule, delete it immediately. Finally, grant Fatima (fatima@test.com) write access to Timeline Beta so she can document the changes to history."

---


---

# PROMPT 9: Mirage Menagerie Caravan Festival (BATCHING REQUIRED)

## Step 1: Sample n
**n = 10** (sampled from range 7-13)

## Step 2: Sample 10 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `POST /calendars` | Calendars: insert |
| 3 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 4 | `POST /calendars/{calendarId}/events` | Events: insert |
| 5 | `POST /calendars/{calendarId}/events/quickAdd` | Events: quickAdd |
| 6 | `POST /freeBusy` | Freebusy: query |
| 7 | `POST /calendars/{calendarId}/events` | Events: insert |
| 8 | `GET /calendars/{calendarId}/events` | Events: list |
| 9 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 10 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |

## Step 3: Sample m
**m = 4** (sampled from range 1-6)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Akira** | Japanese |
| **Zainab** | Nigerian (Hausa) |
| **Ananya** | Indian |
| **Piotr** | Polish |

## Step 5: Action Sequence with Justification

**Theme:** Desert caravan festival of lanterns, puppetry, and oral myth performances

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List calendars to find the main festival calendar **"Mirage Menagerie 2026"** | `GET /users/me/calendarList` | Need the correct calendar ID before scheduling acts |
| 2 | Create a new private calendar **"Backstage Sandstorm Ops"** | `POST /calendars` | Separate internal logistics from public festival schedule |
| 3 | Share **"Backstage Sandstorm Ops"** with Piotr (piotr@test.com) as writer | `POST /calendars/{calendarId}/acl` | Piotr is the stage rigger and must add crew shifts |
| 4 | Create **eight** 15‑minute “Mirage Micro‑Acts” on **"Mirage Menagerie 2026"**: “Glass‑Dune Juggling”, “Whispering Wadi Puppets”, “Lantern Maze Overture”, “Sand‑Script Calligraphy”, “Mothlight Drummers”, “Nomad Kite Ballet”, “Oasis Echo Choir”, “Moon‑Salt Acrobatics” | `POST /calendars/{calendarId}/events` | These micro‑acts are the core program; many inserts make batching necessary |
| 5 | Quick‑add **"Starlit Tea Ceremony with Akira tomorrow 3pm"** on the festival calendar | `POST /calendars/{calendarId}/events/quickAdd` | A simple natural‑language add fits quickAdd |
| 6 | Check when Ananya (ananya@test.com) and Zainab (zainab@test.com) are both free on Saturday evening | `POST /freeBusy` | Need their availability for a joint storyteller council |
| 7 | Create **"Twilight Troupe Council"** at the time they’re both free | `POST /calendars/{calendarId}/events` | Uses the free/busy result to schedule a must‑attend meeting |
| 8 | List all events on **"Mirage Menagerie 2026"** | `GET /calendars/{calendarId}/events` | Needed to gather event IDs for bulk edits and cleanup |
| 9 | Update all eight “Mirage Micro‑Acts” to set location **"Dune Pavilion B"** and add Ananya as attendee | `PATCH /calendars/{calendarId}/events/{eventId}` | Bulk updates should be batched to avoid rate limits |
| 10 | Delete placeholder events **"Placeholder: Dust Rehearsal"** and **"Placeholder: Ghost Stage"** from the festival calendar | `DELETE /calendars/{calendarId}/events/{eventId}` | Cleanup of obsolete placeholders; multiple deletes should be batched |

## Step 6: Generated Prompt

> "I’m drowning in festival logistics for **Mirage Menagerie 2026**. Find that calendar first. We also need a private crew calendar called **Backstage Sandstorm Ops** and Piotr (piotr@test.com) must be able to edit it. On the main festival calendar, schedule our eight 15‑minute micro‑acts: Glass‑Dune Juggling, Whispering Wadi Puppets, Lantern Maze Overture, Sand‑Script Calligraphy, Mothlight Drummers, Nomad Kite Ballet, Oasis Echo Choir, and Moon‑Salt Acrobatics. Add a quick note‑style event: ‘Starlit Tea Ceremony with Akira tomorrow 3pm’. I also need a **Twilight Troupe Council** on Saturday evening when both Ananya (ananya@test.com) and Zainab (zainab@test.com) can attend—check their availability first. Then update all the micro‑acts to be at **Dune Pavilion B** and include Ananya. Finally, remove the placeholders ‘Placeholder: Dust Rehearsal’ and ‘Placeholder: Ghost Stage’. Please batch the repeated edits/inserts/deletes so we don’t trip our API rate limits."

---

# PROMPT 10: Museum of Whispered Relics (BATCHING REQUIRED)

## Step 1: Sample n
**n = 11** (sampled from range 7-13)

## Step 2: Sample 11 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `GET /colors` | Colors: get |
| 3 | `POST /calendars` | Calendars: insert |
| 4 | `POST /calendars` | Calendars: insert |
| 5 | `GET /calendars/{calendarId}` | Calendars: get |
| 6 | `PATCH /calendars/{calendarId}` | Calendars: patch |
| 7 | `POST /users/me/calendarList` | CalendarList: insert |
| 8 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |
| 9 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 10 | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Acl: patch |
| 11 | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Acl: delete |

## Step 3: Sample m
**m = 5** (sampled from range 1-6)

## Step 4: Generate 5 Names
| Name | Origin |
|------|--------|
| **Haruka** | Japanese |
| **Farid** | Iranian |
| **Niamh** | Irish |
| **Olena** | Ukrainian |
| **Kofi** | Ghanaian |

## Step 5: Action Sequence with Justification

**Theme:** Traveling museum coordinating relic transport routes and curator access

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List all calendars to find the existing **"Whispered Relics Mainline"** and **"Embargoed Vault"** calendars | `GET /users/me/calendarList` | Need the correct IDs before modifying subscriptions and permissions |
| 2 | Fetch the color palette to choose distinct colors for new route calendars | `GET /colors` | Prevents confusing similar colors for route tracking |
| 3 | Create a new calendar **"Relic Transit - Northern Route"** | `POST /calendars` | The caravan needs a dedicated calendar for the northern itinerary |
| 4 | Create a new calendar **"Relic Transit - Coastal Route"** | `POST /calendars` | Coastal transport schedule must be separated from the northern route |
| 5 | Get the metadata of **"Whispered Relics Mainline"** | `GET /calendars/{calendarId}` | Confirm timezone/metadata before aligning the new route calendars |
| 6 | Patch both new route calendars with descriptions and chosen colors | `PATCH /calendars/{calendarId}` | Branding and clarity; multiple metadata updates should be batched |
| 7 | Subscribe to the external calendar **"City Archives Access Windows"** | `POST /users/me/calendarList` | The museum needs visibility into archive entry slots |
| 8 | Update calendar list entries: hide **"Embargoed Vault"**, and pin both route calendars as visible with their colors | `PATCH /users/me/calendarList/{calendarId}` | Bulk visibility/color changes should be batched to avoid rate limits |
| 9 | Share both route calendars with Niamh (niamh@test.com) as writer and Farid (farid@test.com) as reader | `POST /calendars/{calendarId}/acl` | Curator coordination needs proper access across both routes |
| 10 | Upgrade Niamh to **owner** on both route calendars | `PATCH /calendars/{calendarId}/acl/{ruleId}` | She is taking over transport logistics; multiple role changes should be batched |
| 11 | Remove Olena's (olena@test.com) access from **"Embargoed Vault"** | `DELETE /calendars/{calendarId}/acl/{ruleId}` | She is no longer on the restricted archive rotation |

## Step 6: Generated Prompt

> "We are reorganizing the Traveling Museum of Whispered Relics. Find the main calendar called **Whispered Relics Mainline** and the old **Embargoed Vault** calendar first. I need two new route calendars: **Relic Transit - Northern Route** and **Relic Transit - Coastal Route**. Use distinct colors from the calendar palette and give them clear descriptions so nobody confuses the routes. Also, subscribe me to the external calendar called **City Archives Access Windows**. In my calendar list, hide the Embargoed Vault from view and make sure both route calendars are visible and color-coded.
>
> Access needs a cleanup too: Niamh (niamh@test.com) should be a writer on both route calendars, Farid (farid@test.com) should be a reader on both, and then promote Niamh to owner on both routes. Remove Olena (olena@test.com) from the Embargoed Vault entirely. Please batch the calendar-list updates and permission changes so we don’t hit quota limits."

---

# PROMPT 11: Emberline Embassy Network (BATCHING REQUIRED)

## Step 1: Sample n
**n = 12** (sampled from range 7-13)

## Step 2: Sample 12 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `POST /users/me/settings/watch` | Settings: watch |
| 3 | `POST /calendars` | Calendars: insert |
| 4 | `POST /calendars` | Calendars: insert |
| 5 | `POST /users/me/calendarList` | CalendarList: insert |
| 6 | `GET /users/me/settings` | Settings: list |
| 7 | `PATCH /calendars/{calendarId}` | Calendars: patch |
| 8 | `PATCH /calendars/{calendarId}` | Calendars: patch |
| 9 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |
| 10 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |
| 11 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 12 | `DELETE /users/me/calendarList/{calendarId}` | CalendarList: delete |

## Step 3: Sample m
**m = 6** (sampled from range 1-6)

## Step 4: Generate 6 Names
| Name | Origin |
|------|--------|
| **Sora** | Japanese |
| **Priya** | Indian |
| **Hassan** | Iranian |
| **Agnieszka** | Polish |
| **Oksana** | Ukrainian |
| **Liam** | Irish |

## Step 5: Action Sequence with Justification

**Theme:** Diplomatic courier network managing embassy calendars and visibility

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List all calendars to locate **"Emberline Embassy Roster"** and legacy **"Old Courier Shifts"** | `GET /users/me/calendarList` | Need IDs for visibility changes and cleanups |
| 2 | Start a watch on user settings updates for audit compliance | `POST /users/me/settings/watch` | Embassy operations require change tracking |
| 3 | Create calendar **"Emberline Courier North Circuit"** | `POST /calendars` | New route for northern embassies needs its own calendar |
| 4 | Create calendar **"Emberline Courier South Circuit"** | `POST /calendars` | Southern route must be isolated for security |
| 5 | Subscribe to **"Consular Blackout Windows"** calendar | `POST /users/me/calendarList` | Must avoid scheduling during consular blackouts |
| 6 | List user settings to confirm locale/timezone format | `GET /users/me/settings` | Ensures calendar metadata is aligned with required time format |
| 7 | Patch **North Circuit** with description and timezone "Europe/Warsaw" | `PATCH /calendars/{calendarId}` | Northern route runs on Warsaw time for cross-border handoffs |
| 8 | Patch **South Circuit** with description and timezone "Asia/Kolkata" | `PATCH /calendars/{calendarId}` | Southern route uses Kolkata time due to regional hubs |
| 9 | Update calendar list entry for North Circuit to be visible and colored | `PATCH /users/me/calendarList/{calendarId}` | Bulk list updates should be batched |
| 10 | Update calendar list entry for South Circuit to be visible and colored | `PATCH /users/me/calendarList/{calendarId}` | Batch with previous list update to reduce API calls |
| 11 | Share both route calendars with Priya (priya@test.com) as writer and Hassan (hassan@test.com) as reader | `POST /calendars/{calendarId}/acl` | Needed for operational access across both routes |
| 12 | Remove **"Old Courier Shifts"** from my calendar list | `DELETE /users/me/calendarList/{calendarId}` | Legacy schedule is obsolete and should be unsubscribed |

## Step 6: Generated Prompt

> "We’re reorganizing the Emberline Embassy courier network. Find the **Emberline Embassy Roster** calendar and the legacy **Old Courier Shifts** entry. I need two new route calendars: **Emberline Courier North Circuit** and **Emberline Courier South Circuit**. Also subscribe me to **Consular Blackout Windows** so we can avoid those times. For compliance, set up a watch on my settings and then confirm my current locale/timezone preferences.
>
> Update the North Circuit to use timezone **Europe/Warsaw** with a clear description, and the South Circuit to use **Asia/Kolkata** with its own description. Make both route calendars visible in my list with distinct colors. Share both routes with Priya (priya@test.com) as a writer and Hassan (hassan@test.com) as a reader. Finally, remove **Old Courier Shifts** from my calendar list. Please batch the calendar-list updates and permission changes to reduce API calls."

---

# PROMPT 12: Skyward Observatory Access Passes (BATCHING REQUIRED)

## Step 1: Sample n
**n = 10** (sampled from range 7-13)

## Step 2: Sample 10 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `GET /colors` | Colors: get |
| 3 | `POST /calendars` | Calendars: insert |
| 4 | `POST /calendars` | Calendars: insert |
| 5 | `POST /users/me/calendarList` | CalendarList: insert |
| 6 | `PATCH /calendars/{calendarId}` | Calendars: patch |
| 7 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |
| 8 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 9 | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Acl: patch |
| 10 | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Acl: delete |

## Step 3: Sample m
**m = 4** (sampled from range 1-6)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Mei** | Chinese |
| **Tomasz** | Polish |
| **Amina** | Nigerian (Hausa) |
| **Leila** | Iranian |

## Step 5: Action Sequence with Justification

**Theme:** Mountain observatory coordinating telescope access, patrols, and weather windows

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List calendars to find **"Skyward Observatory Access"** and the legacy **"Dormant Telescopes"** calendar | `GET /users/me/calendarList` | Need IDs for updates and access cleanup |
| 2 | Fetch available calendar colors to assign distinct hues | `GET /colors` | Prevents confusion between patrol and research schedules |
| 3 | Create calendar **"Meteor Patrol Rotation"** | `POST /calendars` | New rotation schedule for night patrols |
| 4 | Create calendar **"Aurora Research Slots"** | `POST /calendars` | Separate calendar for research telescope bookings |
| 5 | Subscribe to external calendar **"Mountain Weather Alerts"** | `POST /users/me/calendarList` | Weather windows determine which nights are usable |
| 6 | Patch both new calendars with descriptions and timezones | `PATCH /calendars/{calendarId}` | Clarifies scope and aligns schedules to local mountain time |
| 7 | Update calendar list entries: make both new calendars visible and color‑coded | `PATCH /users/me/calendarList/{calendarId}` | Multiple list updates should be batched |
| 8 | Share both new calendars with Mei (mei@test.com) as writer and Tomasz (tomasz@test.com) as reader | `POST /calendars/{calendarId}/acl` | Research lead needs write access; visitor gets read‑only |
| 9 | Promote Mei to **owner** on both new calendars | `PATCH /calendars/{calendarId}/acl/{ruleId}` | She is taking over observatory scheduling, multiple ACL updates should be batched |
| 10 | Remove Leila (leila@test.com) from **"Dormant Telescopes"** | `DELETE /calendars/{calendarId}/acl/{ruleId}` | She no longer has clearance for the legacy archive |

## Step 6: Generated Prompt

> "We’re reorganizing the mountain observatory. First, find **Skyward Observatory Access** and the legacy **Dormant Telescopes** calendar. Create two new calendars: **Meteor Patrol Rotation** and **Aurora Research Slots**. Subscribe me to **Mountain Weather Alerts** so we can coordinate around storms. Use distinct colors from the palette and add clear descriptions with the correct local timezone. Make sure both new calendars are visible in my list and color‑coded.
>
> Access changes: Mei (mei@test.com) should be a writer on both new calendars, Tomasz (tomasz@test.com) should be a reader on both, and then promote Mei to owner on both. Remove Leila (leila@test.com) from Dormant Telescopes. Please batch the calendar‑list updates and ACL changes to stay under quota limits."

---

# PROMPT 13: Firefly Conservatory - Recurring Patrols Required

## Step 1: Sample n
**n = 9** (sampled from range 7-13)

## Step 2: Sample 9 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `POST /calendars` | Calendars: insert |
| 3 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 4 | `POST /calendars/{calendarId}/events` | Events: insert |
| 5 | `POST /freeBusy` | Freebusy: query |
| 6 | `POST /calendars/{calendarId}/events` | Events: insert |
| 7 | `GET /calendars/{calendarId}/events` | Events: list |
| 8 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 9 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |

## Step 3: Sample m
**m = 3** (sampled from range 1-6)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Haruto** | Japanese |
| **Farid** | Iranian |
| **Zanele** | South African |

## Step 5: Action Sequence with Justification

**Theme:** Firefly conservatory running recurring lantern patrols and research sessions

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List calendars to confirm whether a conservatory calendar already exists | `GET /users/me/calendarList` | Need to avoid duplicating an existing conservatory schedule |
| 2 | Create a new calendar called "Firefly Conservatory 2018" | `POST /calendars` | Dedicated calendar for all conservation work |
| 3 | Share the new calendar with Haruto (haruto@test.com) as writer | `POST /calendars/{calendarId}/acl` | Haruto manages field notes and needs edit access |
| 4 | Create a **recurring event** "Lantern Patrol" every Tuesday at 7:00pm for 6 weeks starting June 19, 2018 | `POST /calendars/{calendarId}/events` | Patrols are weekly and must be set up as a recurrence rather than six separate events |
| 5 | Check when Zanele (zanele@test.com) is free on Saturday evening, June 23 | `POST /freeBusy` | Need her availability for a special microscope workshop |
| 6 | Create "Bioluminescent Microscopy Workshop" at the time Zanele is free | `POST /calendars/{calendarId}/events` | Workshop timing depends on Zanele's availability |
| 7 | List all events on "Firefly Conservatory 2018" | `GET /calendars/{calendarId}/events` | Verify the recurring patrols and workshop were added |
| 8 | Update "Lantern Patrol" to add location "Willow Glade Observation Ring" | `PATCH /calendars/{calendarId}/events/{eventId}` | The patrol route location was finalized after creation |
| 9 | Delete the old "Broken Jar Ceremony" event from the primary calendar | `DELETE /calendars/{calendarId}/events/{eventId}` | That event was canceled and should not remain on the main calendar |

## Step 6: Generated Prompt

> "We are starting a serious conservation push for the firefly habitat. First, show me all my calendars so I can see whether I already have a conservatory calendar. If not, create a new calendar called 'Firefly Conservatory 2018' and share it with Haruto (haruto@test.com) so he can edit. The weekly Lantern Patrols need to happen every Tuesday at 7:00pm for indefinite time six weeks starting June 19, 2018 - set that up as a **recurring event**. Zanele (zanele@test.com) can only do the Bioluminescent Microscopy Workshop on next Saturday evening, so check her availability and schedule it when she is free. Then list the events on the Firefly Conservatory calendar so I can confirm everything looks right. Once the patrol route is final, update the Lantern Patrol to use the location 'Willow Glade Observation Ring'. Finally, delete the old 'Broken Jar Ceremony' event from my primary calendar."

---

# PROMPT 14: Clockwork Tinkerers Guild - Recurring Series Exceptions

## Step 1: Sample n
**n = 9** (sampled from range 7-13)

## Step 2: Sample 9 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `POST /calendars` | Calendars: insert |
| 3 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 4 | `POST /calendars/{calendarId}/events` | Events: insert |
| 5 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 6 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 7 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 8 | `GET /calendars/{calendarId}/events` | Events: list |
| 9 | `POST /calendars/{calendarId}/events` | Events: insert |

## Step 3: Sample m
**m = 3** (sampled from range 1-6)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Aiko** | Japanese |
| **Dariusz** | Polish |
| **Asha** | Indian |

## Step 5: Action Sequence with Justification

**Theme:** Clockwork tinkerers guild running recurring workshops with exceptions

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List calendars to check if a guild calendar already exists | `GET /users/me/calendarList` | Need to avoid duplicate calendars before creating a new one |
| 2 | Create a new calendar called "Clockwork Tinkerers Guild" | `POST /calendars` | Dedicated calendar for guild events |
| 3 | Share the guild calendar with Aiko (aiko@test.com) as writer | `POST /calendars/{calendarId}/acl` | Aiko co-runs the workshops and needs edit access |
| 4 | Create a **recurring event** "Gear & Ember Workshop" every Friday at 6:00pm for 8 weeks starting June 22, 2018 | `POST /calendars/{calendarId}/events` | Weekly workshops must be set up as a series |
| 5 | Get all instances of "Gear & Ember Workshop" | `GET /calendars/{calendarId}/events/{eventId}/instances` | Need concrete instance IDs to update/delete specific occurrences |
| 6 | Update the instance that falls on Friday June 29 to start at 7:00pm and add note "Late start due to forge maintenance" | `PATCH /calendars/{calendarId}/events/{eventId}` | This week's session is shifted later, but only for that one instance |
| 7 | Delete the instance that falls on Friday July 6 (festival blackout) | `DELETE /calendars/{calendarId}/events/{eventId}` | That specific occurrence must be cancelled, not the whole series |
| 8 | List all events on the guild calendar to verify the exception changes | `GET /calendars/{calendarId}/events` | Ensure the updated and deleted instances are reflected |
| 9 | Create a one-off "Brass Beetle Showcase" on Saturday July 7 at noon | `POST /calendars/{calendarId}/events` | A standalone exhibition tied to the workshop series |

## Step 6: Generated Prompt

> "I’m setting up the Clockwork Tinkerers Guild calendar. First, show me my calendars so I don’t duplicate anything; if we don’t already have it, create a calendar called **Clockwork Tinkerers Guild** and give Aiko (aiko@test.com) write access. Our **Gear & Ember Workshop** needs to run every Friday at 6:00pm starting June 22, 2018—set it up as a recurring series. However, we need two exceptions: the June 29 session should start at 7:00pm and include the note ‘Late start due to forge maintenance,’ and the July 6 session must be cancelled entirely (festival blackout). After applying those exceptions, show me the guild calendar so I can confirm the series looks right. Then add a one-off event called **Brass Beetle Showcase** on Saturday July 7 at noon."

---

# PROMPT 15: Tidal Library Keeper's Routines - Recurring Series Lifecycle

## Step 1: Sample n
**n = 10** (sampled from range 7-13)

## Step 2: Sample 10 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `POST /calendars` | Calendars: insert |
| 3 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 4 | `POST /calendars/{calendarId}/events` | Events: insert |
| 5 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 6 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 7 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 8 | `POST /calendars/{calendarId}/events` | Events: insert |
| 9 | `GET /calendars/{calendarId}/events` | Events: list |
| 10 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |

## Step 3: Sample m
**m = 3** (sampled from range 1-6)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Fumiko** | Japanese |
| **Agnieszka** | Polish |
| **Tariq** | North African |

## Step 5: Action Sequence with Justification

**Theme:** Moonlit tidal library scheduling a perpetual monthly ritual with exceptions

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List calendars to see if a tidal library calendar already exists | `GET /users/me/calendarList` | Avoid duplicating a specialized calendar |
| 2 | Create a new calendar called "Tidal Library Rotations" | `POST /calendars` | Dedicated calendar for coastal archives and rituals |
| 3 | Share the calendar with Fumiko (fumiko@test.com) as writer | `POST /calendars/{calendarId}/acl` | Fumiko coordinates archive access and needs edit rights |
| 4 | Create a **monthly recurring event** "Moon-Shell Rebinding" on the first Tuesday at 9:00am, starting July 3, 2018 (recurs indefinitely until cancelled) | `POST /calendars/{calendarId}/events` | This is a long-term monthly ritual, not a fixed-length series |
| 5 | Fetch all instances of "Moon-Shell Rebinding" | `GET /calendars/{calendarId}/events/{eventId}/instances` | Need instance IDs for exception handling |
| 6 | Update the August 7, 2018 instance to start at 11:00am and add note "Storm-surge delay" | `PATCH /calendars/{calendarId}/events/{eventId}` | Single-instance change without altering the full series |
| 7 | Delete the September 4, 2018 instance only | `DELETE /calendars/{calendarId}/events/{eventId}` | That occurrence is cancelled due to dock repairs |
| 8 | Add a one-off event "Ink Tide Inventory" on July 15, 2018 at 4:00pm | `POST /calendars/{calendarId}/events` | A separate task unrelated to the series |
| 9 | List all events on "Tidal Library Rotations" to verify exceptions are visible | `GET /calendars/{calendarId}/events` | Confirms the instance update and deletion appear correctly |
| 10 | Delete the entire "Moon-Shell Rebinding" recurring series after the inventory is finished | `DELETE /calendars/{calendarId}/events/{eventId}` | The ritual is being retired, so the whole series should be removed |

## Step 6: Generated Prompt

> "We’re setting up the tidal library’s long-term calendar. First, show me my calendars and create **Tidal Library Rotations** if it doesn’t already exist. Share it with Fumiko (fumiko@test.com) so she can edit. The **Moon-Shell Rebinding** ritual needs to recur **monthly on the first Tuesday at 9:00am**, starting July 3, 2018, and should continue indefinitely until we cancel it. We also need two exceptions: the August 7, 2018 occurrence should start at 11:00am with a note ‘Storm-surge delay,’ and the September 4, 2018 occurrence should be cancelled entirely. Add a separate one-off event called **Ink Tide Inventory** on July 15, 2018 at 4:00pm. After confirming the schedule looks right, delete the entire **Moon-Shell Rebinding** series."

---

# PROMPT 16: Monastery of Echoing Bells - Daily Recurring Series Lifecycle

## Step 1: Sample n
**n = 11** (sampled from range 7-13)

## Step 2: Sample 11 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList` | CalendarList: list |
| 2 | `POST /calendars` | Calendars: insert |
| 3 | `GET /colors` | Colors: get |
| 4 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 5 | `POST /calendars/{calendarId}/events` | Events: insert |
| 6 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 7 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 8 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 9 | `POST /freeBusy` | Freebusy: query |
| 10 | `GET /calendars/{calendarId}/events` | Events: list |
| 11 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |

## Step 3: Sample m
**m = 4** (sampled from range 1-6)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Linh** | Vietnamese |
| **Kwame** | Ghanaian |
| **Agnieszka** | Polish |
| **Arash** | Iranian |

## Step 5: Action Sequence with Justification

**Theme:** Mountain monastery running daily bell rituals with exceptions and a final retirement

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List calendars to see if a monastery calendar already exists | `GET /users/me/calendarList` | Avoid duplicate calendars before creation |
| 2 | Create a new calendar called "Monastery of Echoing Bells" | `POST /calendars` | Dedicated schedule for rituals and maintenance |
| 3 | Fetch colors to choose a distinct monastery calendar color | `GET /colors` | Helps visually separate the monastery calendar |
| 4 | Share the calendar with Linh (linh@test.com) as writer | `POST /calendars/{calendarId}/acl` | Linh logs the rituals and needs edit access |
| 5 | Create a **daily recurring event** "Dawn Bell Rite" at 5:30am starting June 18, 2018 (recurs indefinitely until cancelled) | `POST /calendars/{calendarId}/events` | Daily ritual without a fixed end date |
| 6 | Fetch all instances of "Dawn Bell Rite" | `GET /calendars/{calendarId}/events/{eventId}/instances` | Need instance IDs for specific exceptions |
| 7 | Update the June 20, 2018 instance to start at 6:30am with note "Storm quiet hours" | `PATCH /calendars/{calendarId}/events/{eventId}` | One-off change without altering the series |
| 8 | Delete the June 23, 2018 instance only | `DELETE /calendars/{calendarId}/events/{eventId}` | That day's rite is canceled due to lantern repairs |
| 9 | Check when Kwame (kwame@test.com) is free on June 24 evening | `POST /freeBusy` | Confirm availability for a guest chant workshop |
| 10 | List all events on the monastery calendar to verify the exceptions | `GET /calendars/{calendarId}/events` | Confirms the updated/deleted instances are reflected |
| 11 | Delete the entire "Dawn Bell Rite" recurring series after the workshop | `DELETE /calendars/{calendarId}/events/{eventId}` | The ritual is being retired, remove the full series |

## Step 6: Generated Prompt

> "We’re setting up a proper schedule for the **Monastery of Echoing Bells**. First, show me my calendars so I don’t duplicate anything, and create a calendar with that name if needed. Give Linh (linh@test.com) edit access. The **Dawn Bell Rite** must recur **daily at 5:30am**, starting June 18, 2018, and it should continue indefinitely until we cancel it. I need two exceptions: the June 20, 2018 occurrence should start at 6:30am with the note ‘Storm quiet hours,’ and the June 23, 2018 occurrence should be cancelled entirely. Also, check when Kwame (kwame@test.com) is free on the evening of June 24. After you confirm the schedule, delete the entire **Dawn Bell Rite** series."

---

# PROMPT 17: Glassmoth Conservatory - Single Event + Settings Watch

## Step 1: Sample n
**n = 3** (sampled from range 1-3)

## Step 2: Sample 3 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events` | Events: insert |
| 2 | `PUT /calendars/{calendarId}/events/{eventId}` | Events: update |
| 3 | `POST /users/me/settings/watch` | Settings: watch |

## Step 3: Sample m
**m = 1** (sampled from range 0-2)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Ngozi** | Nigerian |

## Step 5: Action Sequence with Justification

**Theme:** Small conservatory kickoff with a single event that gets corrected

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a one-off event called "Glassmoth Conservatory Candle-Lighting" on the primary calendar and include Ngozi (ngozi@test.com) | `POST /calendars/{calendarId}/events` | Establish the kickoff event so the team has a placeholder on the schedule |
| 2 | Update that same event to move it one hour later and add the location "Hothouse Lantern Atrium" | `PUT /calendars/{calendarId}/events/{eventId}` | The timing and location were confirmed after the initial hold |
| 3 | Start watching user settings changes | `POST /users/me/settings/watch` | We want notifications if timezone/formatting settings change |

## Step 6: Generated Prompt

> "Please put a hold on my primary calendar for **Glassmoth Conservatory Candle-Lighting** and invite Ngozi (ngozi@test.com). After you add it, move it one hour later and set the location to **Hothouse Lantern Atrium**. Also, set up a watch so I get notified whenever my calendar settings change."

---

# PROMPT 18: Sandglass Aviary - Import + Access Revoke

## Step 1: Sample n
**n = 2** (sampled from range 1-3)

## Step 2: Sample 2 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events/import` | Events: import |
| 2 | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Acl: delete |

## Step 3: Sample m
**m = 1** (sampled from range 0-2)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Salma** | Egyptian |

## Step 5: Action Sequence with Justification

**Theme:** A desert aviary logbook needing an imported record and a permission cleanup

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Import an event record named "Saffron Dusk Feather-Mending" into the primary calendar using an iCal import payload | `POST /calendars/{calendarId}/events/import` | The record is coming from a legacy system and must be imported, not retyped |
| 2 | Revoke Salma’s access to the "Sandglass Aviary" calendar (rule ID: `user:salma@test.com`) | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Her access must be removed immediately after the logbook entry is imported |

## Step 6: Generated Prompt

> "Please **import** the following legacy entry into my **primary calendar** (not a manual create): ‘Saffron Dusk Feather-Mending’ on June 22, 2018 from 6:00pm–7:00pm, location ‘Windglass Roost,’ iCalUID `saffron-dusk-20180622@aviary`. Also, remove Salma’s access to the **Sandglass Aviary** calendar — her ACL rule is `user:salma@test.com`."

---

# PROMPT 19: Quartzloom Herbarium - Event Create + Access Revoke

## Step 1: Sample n
**n = 2** (sampled from range 1-3)

## Step 2: Sample 2 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Acl: delete |
| 2 | `POST /calendars/{calendarId}/events` | Events: insert |

## Step 3: Sample m
**m = 1** (sampled from range 0-2)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Mina** | Iranian |

## Step 5: Action Sequence with Justification

**Theme:** A crystal herbarium filing a single ritual and tightening access

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a one-off event called "Quartzloom Spore Cataloging" on the primary calendar for June 21, 2018, 9:00am–10:00am | `POST /calendars/{calendarId}/events` | The cataloging session must be logged immediately on the main schedule |
| 2 | Revoke Mina’s access to the Quartzloom Herbarium calendar (calendar ID `cal_quartzloom_herbarium`, rule ID `user:mina@test.com`) | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Her access should be removed now that the catalog is sealed |

## Step 6: Generated Prompt

> "On my **primary calendar**, add a one-hour event called **Quartzloom Spore Cataloging** on June 21, 2018 from 9:00am–10:00am. Also, remove Mina’s access from the **Quartzloom Herbarium** calendar (calendar ID `cal_quartzloom_herbarium`, rule ID `user:mina@test.com`)."

---

# PROMPT 20: Starfen Observatory - ACL Review, Event Replace, Calendar Delete

## Step 1: Sample n
**n = 3** (sampled from range 1-3)

## Step 2: Sample 3 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `DELETE /calendars/{calendarId}` | Calendars: delete |
| 2 | `GET /calendars/{calendarId}/acl` | Acl: list |
| 3 | `PUT /calendars/{calendarId}/events/{eventId}` | Events: update |

## Step 3: Sample m
**m = 2** (sampled from range 0-2)

## Step 4: Generate 2 Names
| Name | Origin |
|------|--------|
| **Ewa** | Polish |
| **Yara** | Brazilian |

## Step 5: Action Sequence with Justification

**Theme:** Observatory housekeeping with a strict event replacement and a retired calendar

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List ACL rules on the "Starfen Observatory" calendar to verify who can edit | `GET /calendars/{calendarId}/acl` | Confirms access before making sensitive changes |
| 2 | Fully replace the "Comet Scribe Session" event on that calendar to move it to June 24, 2018, 2:00pm–3:00pm and set location "Dome 3" | `PUT /calendars/{calendarId}/events/{eventId}` | A full replacement is needed to ensure all fields are explicit and correct |
| 3 | Permanently delete the "Dust Ledger" calendar because it is retired | `DELETE /calendars/{calendarId}` | The obsolete calendar should be removed entirely |

## Step 6: Generated Prompt

> "On the **Starfen Observatory** calendar, please review who has access, then fully replace the **Comet Scribe Session** so it is on June 24, 2018 from 2:00pm–3:00pm at **Dome 3** (treat this as a full replace, not a patch). Also, delete the **Dust Ledger** calendar entirely."

---

# PROMPT 21: Emberglass Atelier - Single Event Create

## Step 1: Sample n
**n = 1** (sampled from range 1-3)

## Step 2: Sample 1 Endpoint (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events` | Events: insert |

## Step 3: Sample m
**m = 0** (sampled from range 0-2)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** A single artisan workshop entry

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a one-off event called "Emberglass Kiln Glow" on the primary calendar for June 25, 2018, 7:00pm–8:30pm | `POST /calendars/{calendarId}/events` | The schedule only needs a single new entry |

## Step 6: Generated Prompt

> "Add a one-off event on my **primary calendar** called **Emberglass Kiln Glow** on June 25, 2018 from 7:00pm–8:30pm."

---

# PROMPT 22: Fogloom Archive - QuickAdd + Get + Settings Watch

## Step 1: Sample n
**n = 3** (sampled from range 1-3)

## Step 2: Sample 3 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events/quickAdd` | Events: quickAdd |
| 2 | `GET /calendars/{calendarId}/events/{eventId}` | Events: get |
| 3 | `POST /users/me/settings/watch` | Settings: watch |

## Step 3: Sample m
**m = 0** (sampled from range 0-2)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** A fogbound archive with a quick entry and a verification pull

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Quick-add a one-off event using natural language: "Fogloom Archive Lantern Check on June 26, 2018 at 8:00pm for 45 minutes" on the primary calendar | `POST /calendars/{calendarId}/events/quickAdd` | The request arrives as plain text and should be captured quickly |
| 2 | Retrieve the newly created event by ID to confirm its parsed fields | `GET /calendars/{calendarId}/events/{eventId}` | Ensures the quick-add parsed the time correctly |
| 3 | Start watching user settings changes | `POST /users/me/settings/watch` | We want notifications if user settings change |

## Step 6: Generated Prompt

> "Please **quick-add** this to my **primary calendar**: ‘Fogloom Archive Lantern Check on June 26, 2018 at 8:00pm for 45 minutes.’ After it’s created, fetch that event by ID so we can verify the parsed details. Also, set up a watch for changes to my calendar settings."

---

# PROMPT 23: Lumenfjord Scriptorium - ACL Check, Event Replace, Event List

## Step 1: Sample n
**n = 3** (sampled from range 1-3)

## Step 2: Sample 3 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /calendars/{calendarId}/acl/{ruleId}` | Acl: get |
| 2 | `PUT /calendars/{calendarId}/events/{eventId}` | Events: update |
| 3 | `GET /calendars/{calendarId}/events` | Events: list |

## Step 3: Sample m
**m = 0** (sampled from range 0-2)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** A fjord scriptorium that needs a strict event replacement and a final review

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Retrieve the ACL rule `user:scribe@lumenfjord.example` on the Lumenfjord Scriptorium calendar to verify its current role | `GET /calendars/{calendarId}/acl/{ruleId}` | Confirm the permission details before changing the schedule |
| 2 | Fully replace the "Aurora Ink Drying" event to move it to June 27, 2018, 3:00pm–4:00pm and set location "North Alcove" | `PUT /calendars/{calendarId}/events/{eventId}` | A full replacement ensures all fields are explicitly corrected |
| 3 | List the calendar’s events to verify the updated entry appears correctly | `GET /calendars/{calendarId}/events` | Confirms the replacement took effect on the schedule |

## Step 6: Generated Prompt

> "On the **Lumenfjord Scriptorium** calendar, check the ACL rule `user:scribe@lumenfjord.example` and tell me what role it has. Then fully replace the **Aurora Ink Drying** event so it’s on June 27, 2018 from 3:00pm–4:00pm at **North Alcove**. Afterward, list the events on that calendar so I can verify the update."

---

# PROMPT 24: Sunthread Archive - Delete Event + List Settings

## Step 1: Sample n
**n = 2** (sampled from range 1-2)

## Step 2: Sample 2 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 2 | `GET /users/me/settings` | Settings: list |

## Step 3: Sample m
**m = 1** (sampled from range 0-2)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Adebayo** | Nigerian |

## Step 5: Action Sequence with Justification

**Theme:** A single cleanup in a textile archive with a settings check

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Delete the event "Sunthread Loom Blessing" from the primary calendar (event ID `evt_sunthread_loom_001`) | `DELETE /calendars/{calendarId}/events/{eventId}` | The event is cancelled and must be removed from the schedule |
| 2 | List all user settings to confirm the current timezone before informing Adebayo | `GET /users/me/settings` | Ensures any follow-up messaging uses the correct settings |

## Step 6: Generated Prompt

> "Please remove the **Sunthread Loom Blessing** event from my **primary calendar** (event ID `evt_sunthread_loom_001`). After that, list all my calendar settings so I can confirm my current timezone before I update Adebayo (adebayo@test.com)."

---

# PROMPT 25: Emberpine Cartography - Create Calendar Only

## Step 1: Sample n
**n = 1** (sampled from range 1-3)

## Step 2: Sample 1 Endpoint (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars` | Calendars: insert |

## Step 3: Sample m
**m = 2** (sampled from range 0-2)

## Step 4: Generate 2 Names
| Name | Origin |
|------|--------|
| **Mateusz** | Polish |
| **Ewa** | Polish |

## Step 5: Action Sequence with Justification

**Theme:** A cartographers’ archive getting its own calendar

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a new calendar named "Emberpine Cartography Ledger" | `POST /calendars` | A dedicated calendar is needed for mapmaking rituals and field logs |

## Step 6: Generated Prompt

> "Create a new calendar called **Emberpine Cartography Ledger**."

---

# PROMPT 26: Mistforge Observatory - Settings Check Only

## Step 1: Sample n
**n = 1** (sampled from range 1-2)

## Step 2: Sample 1 Endpoint (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/settings` | Settings: list |

## Step 3: Sample m
**m = 1** (sampled from range 0-2)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Sana** | Pakistani |

## Step 5: Action Sequence with Justification

**Theme:** Checking preferences before coordinating a niche observatory task

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List all user settings to confirm timezone and formatting | `GET /users/me/settings` | Needed before relaying schedule details to Sana |

## Step 6: Generated Prompt

> "Please list my calendar settings so I can confirm my timezone and date/time formats before I reply to Sana (sana@test.com)."

---

# PROMPT 27: Lattice Observatory - CalendarList Patch + Recurring Event Replace

## Step 1: Sample n
**n = 2** (sampled from range 1-2)

## Step 2: Sample 2 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |
| 2 | `PUT /calendars/{calendarId}/events/{eventId}` | Events: update |

## Step 3: Sample m
**m = 1** (sampled from range 0-2)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Ewa** | Polish |

## Step 5: Action Sequence with Justification

**Theme:** A telescope maintenance series that must be fully replaced, plus a visibility tweak

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Patch the calendar list entry for "Lattice Observatory" to set `hidden=true` | `PATCH /users/me/calendarList/{calendarId}` | The calendar should no longer clutter the main view |
| 2 | Fully replace the recurring event "Prism-Lens Alignment" (event ID `evt_prism_lens_004`) on the Lattice Observatory calendar so it repeats weekly on Thursdays at 6:00am, starting June 28, 2018, lasting 45 minutes, location "Pier 7 Scope" | `PUT /calendars/{calendarId}/events/{eventId}` | The maintenance series needs a full replacement to reset its schedule |

## Step 6: Generated Prompt

> "Please hide the **Lattice Observatory** calendar in my calendar list (calendar ID `cal_lattice_observatory`). Also, fully replace the recurring **Prism-Lens Alignment** event (event ID `evt_prism_lens_004`) on that calendar so it runs **weekly on Thursdays at 6:00am**, starting June 28, 2018, for **45 minutes** at **Pier 7 Scope**. Ewa asked me to confirm the updated series today."

---

# PROMPT 28: Copperseed Archive - QuickAdd + Events Watch

## Step 1: Sample n
**n = 2** (sampled from range 1-2)

## Step 2: Sample 2 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events/quickAdd` | Events: quickAdd |
| 2 | `POST /calendars/{calendarId}/events/watch` | Events: watch |

## Step 3: Sample m
**m = 1** (sampled from range 0-2)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Fatima** | Moroccan |

## Step 5: Action Sequence with Justification

**Theme:** A tiny archive needs a quick entry and notifications

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Quick-add an event using natural language: "Copperseed Archive dusting on June 28, 2018 at 9:30am for 30 minutes" on the primary calendar | `POST /calendars/{calendarId}/events/quickAdd` | The request is a short plain-text note that should be captured quickly |
| 2 | Start watching event changes on the primary calendar | `POST /calendars/{calendarId}/events/watch` | We want alerts if the entry is altered after creation |

## Step 6: Generated Prompt

> "Quick-add this to my **primary calendar**: ‘Copperseed Archive dusting on June 28, 2018 at 9:30am for 30 minutes.’ Then start watching my primary calendar for event changes so I can notify Fatima (fatima@test.com) if anything shifts."

---

# PROMPT 29: Aurora Loom - CalendarList Check + Recurring Series Delete

## Step 1: Sample n
**n = 2** (sampled from range 1-2)

## Step 2: Sample 2 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /users/me/calendarList/{calendarId}` | CalendarList: get |
| 2 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |

## Step 3: Sample m
**m = 0** (sampled from range 0-2)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** A recurring ritual is being retired after verifying the subscription

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Fetch the calendar list entry for "Aurora Loom" (calendar ID `cal_aurora_loom`) to confirm it’s subscribed | `GET /users/me/calendarList/{calendarId}` | Ensure the calendar is actually in the user’s list before acting on it |
| 2 | Delete the entire recurring series "Starlit Weave Circle" (event ID `evt_starlit_weave_series`) from that calendar | `DELETE /calendars/{calendarId}/events/{eventId}` | The weekly ritual is ending, so the whole series should be removed |

## Step 6: Generated Prompt

> "Check that I’m subscribed to the **Aurora Loom** calendar (ID `cal_aurora_loom`). Then remove the entire recurring series **Starlit Weave Circle** (event ID `evt_starlit_weave_series`) from that calendar."

---

# PROMPT 30: Cinderflock Choir - Delete Recurring Series Only

## Step 1: Sample n
**n = 1** (sampled from range 1-2)

## Step 2: Sample 1 Endpoint (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |

## Step 3: Sample m
**m = 0** (sampled from range 0-2)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** Retiring a recurring rehearsal series

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Delete the entire recurring series "Cinderflock Vesper Choir" (event ID `evt_cinderflock_vespers`) from the Cinderflock Choir calendar (ID `cal_cinderflock_choir`) | `DELETE /calendars/{calendarId}/events/{eventId}` | The weekly rehearsal series is ending and should be removed in full |

## Step 6: Generated Prompt

> "Please delete the entire recurring **Cinderflock Vesper Choir** series (event ID `evt_cinderflock_vespers`) from the **Cinderflock Choir** calendar (ID `cal_cinderflock_choir`)."

---

# PROMPT 31: Driftglass Archives - List + Move Event

## Step 1: Sample n
**n = 2** (sampled from range 1-2)

## Step 2: Sample 2 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /calendars/{calendarId}/events` | Events: list |
| 2 | `POST /calendars/{calendarId}/events/{eventId}/move` | Events: move |

## Step 3: Sample m
**m = 0** (sampled from range 0-2)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** A workshop event needs to be moved after reviewing a calendar

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List events on the "Driftglass Studio" calendar to locate the event ID for "Tide-Polish Lesson" | `GET /calendars/{calendarId}/events` | We need the event ID before moving it |
| 2 | Move "Tide-Polish Lesson" from the Driftglass Studio calendar to the "Mariner Annex" calendar | `POST /calendars/{calendarId}/events/{eventId}/move` | The lesson belongs on the annex calendar now |

## Step 6: Generated Prompt

> "Please list events on my **Driftglass Studio** calendar so you can find the event ID for **Tide-Polish Lesson**, then move that event to the **Mariner Annex** calendar."

---

# PROMPT 32: Emberwharf Ledger - Import Event Only

## Step 1: Sample n
**n = 1** (sampled from range 1-3)

## Step 2: Sample 1 Endpoint (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events/import` | Events: import |

## Step 3: Sample m
**m = 0** (sampled from range 0-2)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** A single legacy record imported into the main ledger

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Import a legacy event called "Emberwharf Tide Log" into the primary calendar using an iCal import payload | `POST /calendars/{calendarId}/events/import` | The record comes from a legacy system and should be imported, not recreated |

## Step 6: Generated Prompt

> "Please **import** this legacy entry into my **primary calendar** (do not recreate it manually): ‘Emberwharf Tide Log’ on June 29, 2018 from 5:00pm–5:30pm, location ‘Pier Lantern Desk,’ iCalUID `emberwharf-tide-20180629@ledger`."

---

# PROMPT 33: Latticewren Survey - CalendarList Get/Put + Create Calendar

## Step 1: Sample n
**n = 3** (sampled from range 2-3)

## Step 2: Sample 3 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `PUT /users/me/calendarList/{calendarId}` | CalendarList: update |
| 2 | `GET /users/me/calendarList/{calendarId}` | CalendarList: get |
| 3 | `POST /calendars` | Calendars: insert |

## Step 3: Sample m
**m = 1** (sampled from range 0-2)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Salma** | Egyptian |

## Step 5: Action Sequence with Justification

**Theme:** New survey calendar with a strict calendar-list update

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a new calendar named "Latticewren Survey Log" | `POST /calendars` | A dedicated calendar is needed for field notes and survey windows |
| 2 | Retrieve the calendar list entry for the new calendar to see its current properties | `GET /users/me/calendarList/{calendarId}` | We need the existing entry before doing a full replacement |
| 3 | Fully replace the calendar list entry to set `selected=false` and `hidden=true` | `PUT /users/me/calendarList/{calendarId}` | The calendar should be created but not shown by default |

## Step 6: Generated Prompt

> "Create a new calendar called **Latticewren Survey Log**. Then fetch its calendar-list entry and fully replace that entry so the calendar is **hidden** and **not selected** in my list. I want it out of sight until Salma (salma@test.com) asks for it."

---

# PROMPT 34: Icefern Annex - Move Event + Events Watch

## Step 1: Sample n
**n = 2** (sampled from range 2-3)

## Step 2: Sample 2 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events/{eventId}/move` | Events: move |
| 2 | `POST /calendars/{calendarId}/events/watch` | Events: watch |

## Step 3: Sample m
**m = 2** (sampled from range 0-2)

## Step 4: Generate 2 Names
| Name | Origin |
|------|--------|
| **Hana** | Korean |
| **Sven** | Swedish |

## Step 5: Action Sequence with Justification

**Theme:** A classroom event is relocated and monitored

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Move "Icefern Map Workshop" (event ID `evt_icefern_maps_07`) from the Icefern Annex calendar to the Boreal Classroom calendar (ID `cal_boreal_classroom`) | `POST /calendars/{calendarId}/events/{eventId}/move` | The workshop was reassigned to a different space |
| 2 | Start watching event changes on the Boreal Classroom calendar | `POST /calendars/{calendarId}/events/watch` | We need alerts if the moved event changes before Hana or Sven arrive |

## Step 6: Generated Prompt

> "Please move **Icefern Map Workshop** (event ID `evt_icefern_maps_07`) from the **Icefern Annex** calendar to the **Boreal Classroom** calendar (ID `cal_boreal_classroom`). Then start watching the Boreal Classroom calendar for event changes so I can notify Hana (hana@test.com) and Sven (sven@test.com) if anything shifts."

---

# PROMPT 35: Nightglass Repository - Clear Calendar + CalendarList Patch

## Step 1: Sample n
**n = 2** (sampled from range 2-3)

## Step 2: Sample 2 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/clear` | Calendars: clear |
| 2 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |

## Step 3: Sample m
**m = 2** (sampled from range 0-2)

## Step 4: Generate 2 Names
| Name | Origin |
|------|--------|
| **Ewa** | Polish |
| **Hana** | Korean |

## Step 5: Action Sequence with Justification

**Theme:** Purging a repository calendar and hiding it

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Clear all events from the "Nightglass Repository" calendar (ID `cal_nightglass_repository`) | `POST /calendars/{calendarId}/clear` | The repository is resetting but the calendar itself must remain |
| 2 | Patch the calendar list entry to set `hidden=true` for that calendar | `PATCH /users/me/calendarList/{calendarId}` | After clearing, it should be hidden from the main view |

## Step 6: Generated Prompt

> "Please clear all events from my **Nightglass Repository** calendar (ID `cal_nightglass_repository`) but keep the calendar. Then hide that calendar in my list. I’ll let Ewa (ewa@test.com) and Hana (hana@test.com) know once it’s done."

---

# PROMPT 36: Brasswillow Registry - Create, Share, Delete Calendar

## Step 1: Sample n
**n = 3** (fixed to 3)

## Step 2: Sample 3 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 2 | `DELETE /calendars/{calendarId}` | Calendars: delete |
| 3 | `POST /calendars` | Calendars: insert |

## Step 3: Sample m
**m = 1** (sampled from range 0-2)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Ewa** | Polish |

## Step 5: Action Sequence with Justification

**Theme:** Creating a registry calendar, sharing it briefly, then removing it

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a new calendar named "Brasswillow Registry" | `POST /calendars` | A temporary registry needs its own calendar |
| 2 | Share the calendar with Ewa (ewa@test.com) as a writer | `POST /calendars/{calendarId}/acl` | Ewa must verify the registry contents |
| 3 | Delete the Brasswillow Registry calendar after verification | `DELETE /calendars/{calendarId}` | The registry is temporary and should be removed |

## Step 6: Generated Prompt

> "Create a new calendar called **Brasswillow Registry** and share it with Ewa (ewa@test.com) with edit access. After she’s had a look, delete the Brasswillow Registry calendar entirely."

---

# PROMPT 37: Kiteglass Survey Log - Multi-Check Coordination

## Step 1: Sample n
**n = 6** (sampled from range 4-6)

## Step 2: Sample 6 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Acl: patch |
| 2 | `POST /channels/stop` | Channels: stop |
| 3 | `POST /calendars` | Calendars: insert |
| 4 | `GET /colors` | Colors: get |
| 5 | `POST /freeBusy` | Freebusy: query |
| 6 | `GET /calendars/{calendarId}/events/{eventId}` | Events: get |

## Step 3: Sample m
**m = 1** (sampled from range 0-4)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Sven** | Swedish |

## Step 5: Action Sequence with Justification

**Theme:** A small survey log with access tweaks and a tight multi-calendar coordination

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Fetch the color palette and use **color ID 9** for the new survey calendar | `GET /colors` | We need a color ID before assigning a visual style |
| 2 | Create a new calendar called "Kiteglass Survey Log" | `POST /calendars` | The survey work needs a dedicated calendar |
| 3 | Patch Sven’s ACL rule on the "Harbor Signalboard" calendar (ID `cal_harbor_signalboard`, rule ID `user:sven@test.com`) to writer | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Sven must be able to edit that shared calendar going forward |
| 4 | Use free/busy across my primary calendar and Sven’s calendar to find the earliest 45-minute overlap between June 27–28, 2018 | `POST /freeBusy` | We need a joint window that works for both of us |
| 5 | Retrieve the event with ID `evt_horizon_shim_02` on my primary calendar to confirm its exact timing before finalizing the slot | `GET /calendars/{calendarId}/events/{eventId}` | Prevents scheduling on top of a fixed commitment |
| 6 | Stop the old settings watch channel (id `chan_settings_204`, resourceId `res_settings_204`) | `POST /channels/stop` | The prior notification channel is obsolete and should be closed |

## Step 6: Generated Prompt

> "Create a new calendar named **Kiteglass Survey Log**. Before you do anything else, pull the **calendar color palette** and set the new calendar to **color ID 9**. Sven needs editor access on the **Harbor Signalboard** calendar (ID `cal_harbor_signalboard`)—his ACL rule is `user:sven@test.com`, please update it. Then find the **earliest 45-minute overlap** between **my primary calendar** and **Sven’s calendar** across June 27–28, 2018. Also, fetch the event **evt_horizon_shim_02** on my primary calendar to confirm its exact time so the overlap you pick doesn’t collide. Finally, stop the old settings watch channel with id `chan_settings_204` and resourceId `res_settings_204`."

---

# PROMPT 38: Driftweave Annex - Access Tweak, Watch, Unsubscribe, Stop Channel

## Step 1: Sample n
**n = 4** (sampled from range 4-6)

## Step 2: Sample 4 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /channels/stop` | Channels: stop |
| 2 | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Acl: patch |
| 3 | `POST /calendars/{calendarId}/events/watch` | Events: watch |
| 4 | `DELETE /users/me/calendarList/{calendarId}` | CalendarList: delete |

## Step 3: Sample m
**m = 1** (sampled from range 0-4)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Iryna** | Ukrainian |

## Step 5: Action Sequence with Justification

**Theme:** A small annex cleanup with permissions, watch, and subscription pruning

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Patch Iryna’s ACL rule on the "Driftweave Annex" calendar (ID `cal_driftweave_annex`, rule `user:iryna@test.com`) to writer | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Iryna is now coordinating edits and needs write access |
| 2 | Start watching event changes on the Driftweave Annex calendar | `POST /calendars/{calendarId}/events/watch` | We want notifications if the annex schedule changes |
| 3 | Unsubscribe me from the "Old Aster Lodge" calendar (ID `cal_old_aster_lodge`) | `DELETE /users/me/calendarList/{calendarId}` | That calendar is no longer relevant to the annex |
| 4 | Stop the old events watch channel (id `chan_annex_77`, resourceId `res_annex_77`) | `POST /channels/stop` | The old channel should be closed to avoid duplicate notifications |

## Step 6: Generated Prompt

> "Please update Iryna’s access on the **Driftweave Annex** calendar (ID `cal_driftweave_annex`) to **writer** — her ACL rule is `user:iryna@test.com`. Then set up an **events watch** on that calendar. Also, unsubscribe me from the **Old Aster Lodge** calendar (ID `cal_old_aster_lodge`). Finally, stop the old events watch channel with id `chan_annex_77` and resourceId `res_annex_77`."

---

# PROMPT 39: Mossquill Archive - Clear, Patch Calendar, Replace ACL, Replace Event, Settings Checks

## Step 1: Sample n
**n = 6** (sampled from range 4-6)

## Step 2: Sample 6 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/clear` | Calendars: clear |
| 2 | `PATCH /calendars/{calendarId}` | Calendars: patch |
| 3 | `PUT /calendars/{calendarId}/acl/{ruleId}` | Acl: update |
| 4 | `GET /users/me/settings/{setting}` | Settings: get |
| 5 | `PUT /calendars/{calendarId}/events/{eventId}` | Events: update |
| 6 | `GET /users/me/settings/{setting}` | Settings: get |

## Step 3: Sample m
**m = 3** (sampled from range 0-4)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Ngozi** | Nigerian |
| **Iryna** | Ukrainian |
| **Salma** | Egyptian |

## Step 5: Action Sequence with Justification

**Theme:** A restored archive that needs a clean slate, metadata tweaks, and strict access rules

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Clear all events from the "Mossquill Archive" calendar (ID `cal_mossquill_archive`) | `POST /calendars/{calendarId}/clear` | The archive is resetting and must start with an empty schedule |
| 2 | Patch the Mossquill Archive calendar to set description "Restoration ledger and vault access" | `PATCH /calendars/{calendarId}` | Metadata needs to reflect the new scope |
| 3 | Fully replace Salma’s ACL rule on Mossquill Archive (rule `user:salma@test.com`) to role **reader** | `PUT /calendars/{calendarId}/acl/{ruleId}` | Access must be redefined with a full replacement |
| 4 | Fetch the user setting `timezone` | `GET /users/me/settings/{setting}` | Ensure we’re using the correct timezone for the updated event |
| 5 | Fully replace the event `evt_mossquill_vault_check` on that calendar to June 29, 2018, 4:00pm–5:00pm, location "Lower Vault Door" | `PUT /calendars/{calendarId}/events/{eventId}` | The inspection slot must be rewritten with explicit fields |
| 6 | Fetch the user setting `dateFieldOrder` | `GET /users/me/settings/{setting}` | Confirm date formatting preference for the archive log |

## Step 6: Generated Prompt

> "Please clear all events from the **Mossquill Archive** calendar (ID `cal_mossquill_archive`). Then patch that calendar’s description to **‘Restoration ledger and vault access.’** Update Salma’s ACL on the Mossquill Archive calendar (rule `user:salma@test.com`) to **reader** using a full replacement. Before changing the inspection slot, check my **timezone** setting. Then fully replace the event **evt_mossquill_vault_check** so it’s on **June 29, 2018 from 4:00pm–5:00pm** at **Lower Vault Door**. Finally, fetch my **dateFieldOrder** setting."

---

# PROMPT 40: Glimmerforge Atlas - Create Calendar, Share, ACL Patch, Settings Check

## Step 1: Sample n
**n = 4** (sampled from range 4-6)

## Step 2: Sample 4 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Acl: patch |
| 2 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 3 | `POST /calendars` | Calendars: insert |
| 4 | `GET /users/me/settings/{setting}` | Settings: get |

## Step 3: Sample m
**m = 3** (sampled from range 0-4)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Adebayo** | Nigerian |
| **Sven** | Swedish |
| **Mina** | Iranian |

## Step 5: Action Sequence with Justification

**Theme:** A fresh atlas calendar with curated access levels

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a new calendar named "Glimmerforge Atlas" | `POST /calendars` | A dedicated atlas calendar is required for the project |
| 2 | Share the calendar with Mina (mina@test.com) as writer | `POST /calendars/{calendarId}/acl` | Mina is the primary editor |
| 3 | Patch Sven’s ACL on the same calendar (rule `user:sven@test.com`) to writer | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Sven should have edit access |
| 4 | Fetch the user setting `timezone` | `GET /users/me/settings/{setting}` | Confirm timezone before sending the access details |

## Step 6: Generated Prompt

> "Create a new calendar called **Glimmerforge Atlas**. Share it with Mina (mina@test.com) as **writer**. Then update Sven’s access on that same calendar (rule `user:sven@test.com`) to **writer**. Finally, fetch my **timezone** setting so I can include it in the access note to Adebayo (adebayo@test.com)."

---

# PROMPT 41: Tidemire Conservatory - Inspect, Clear, Settings Check

## Step 1: Sample n
**n = 4** (sampled from range 4-6)

## Step 2: Sample 4 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 2 | `POST /calendars/{calendarId}/clear` | Calendars: clear |
| 3 | `GET /users/me/settings` | Settings: list |
| 4 | `GET /calendars/{calendarId}/events/{eventId}` | Events: get |

## Step 3: Sample m
**m = 1** (sampled from range 0-4)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Yara** | Brazilian |

## Step 5: Action Sequence with Justification

**Theme:** Clearing a conservatory calendar after a final inspection

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Retrieve the recurring event `evt_tidemire_orchid_rounds` on the Tidemire Conservatory calendar (ID `cal_tidemire_conservatory`) | `GET /calendars/{calendarId}/events/{eventId}` | Confirm the series exists before touching the calendar |
| 2 | Fetch all instances of that recurring event | `GET /calendars/{calendarId}/events/{eventId}/instances` | We need to see upcoming occurrences before clearing |
| 3 | List all user settings | `GET /users/me/settings` | Confirm current preferences for the final report |
| 4 | Clear all events from the Tidemire Conservatory calendar | `POST /calendars/{calendarId}/clear` | The conservatory is being reset and should be emptied |

## Step 6: Generated Prompt

> "On the **Tidemire Conservatory** calendar (ID `cal_tidemire_conservatory`), first fetch the event **evt_tidemire_orchid_rounds**, then list its **instances** so I can review upcoming rounds. After that, list my **calendar settings** for the record. Once I confirm, **clear all events** from the Tidemire Conservatory calendar. Yara (yara@test.com) needs the final report after the reset."

---

# PROMPT 42: Lanternbraid Pavilion - Get Event, Unsubscribe, ACL Watch, Patch Calendar

## Step 1: Sample n
**n = 4** (sampled from range 4-6)

## Step 2: Sample 4 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /calendars/{calendarId}/events/{eventId}` | Events: get |
| 2 | `DELETE /users/me/calendarList/{calendarId}` | CalendarList: delete |
| 3 | `POST /calendars/{calendarId}/acl/watch` | Acl: watch |
| 4 | `PATCH /calendars/{calendarId}` | Calendars: patch |

## Step 3: Sample m
**m = 4** (sampled from range 0-4)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Sana** | Pakistani |
| **Hiro** | Japanese |
| **Tariq** | North African |
| **Lucia** | Mexican |

## Step 5: Action Sequence with Justification

**Theme:** Pavilion admin cleanup with a quick check and metadata tweak

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Fetch the event `evt_lanternbraid_opening` on the Lanternbraid Pavilion calendar (ID `cal_lanternbraid_pavilion`) | `GET /calendars/{calendarId}/events/{eventId}` | Confirm the opening event details before editing the calendar |
| 2 | Patch the Lanternbraid Pavilion calendar to set location "Harborline Rotunda" | `PATCH /calendars/{calendarId}` | The venue address has been finalized |
| 3 | Start an ACL watch on the Lanternbraid Pavilion calendar | `POST /calendars/{calendarId}/acl/watch` | We need notifications when access changes |
| 4 | Unsubscribe me from the "Old Copper Annex" calendar (ID `cal_old_copper_annex`) | `DELETE /users/me/calendarList/{calendarId}` | That calendar is no longer needed |

## Step 6: Generated Prompt

> "On the **Lanternbraid Pavilion** calendar (ID `cal_lanternbraid_pavilion`), fetch the event **evt_lanternbraid_opening** first. Then update the calendar’s **location** to **Harborline Rotunda**. Also start an **ACL watch** on the Lanternbraid Pavilion calendar. Finally, unsubscribe me from the **Old Copper Annex** calendar (ID `cal_old_copper_annex`). I need Sana, Hiro, Tariq, and Lucia copied on the final note once this is done."

---

# PROMPT 43: Meridian Drift Folio - Subscribe, List Entry Replace, Event Patch, ACL Watch

## Step 1: Sample n
**n = 4** (sampled from range 4-6)

## Step 2: Sample 4 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/acl/watch` | Acl: watch |
| 2 | `PUT /users/me/calendarList/{calendarId}` | CalendarList: update |
| 3 | `POST /users/me/calendarList` | CalendarList: insert |
| 4 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |

## Step 3: Sample m
**m = 1** (sampled from range 0-4)

## Step 4: Generate 1 Name
| Name | Origin |
|------|--------|
| **Ewa** | Polish |

## Step 5: Action Sequence with Justification

**Theme:** A folio calendar is subscribed, tuned, and monitored

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Subscribe me to the external calendar with ID `cal_meridian_drift_folio` | `POST /users/me/calendarList` | The folio is external and must be added to my list |
| 2 | Fully replace that calendar list entry to set `selected=false`, `hidden=true`, and color ID 7 | `PUT /users/me/calendarList/{calendarId}` | We want it present but out of the main view |
| 3 | Patch the event `evt_meridian_index` on that calendar to add description "Catalog spine check" | `PATCH /calendars/{calendarId}/events/{eventId}` | The event needs a note without changing other fields |
| 4 | **(Extra to satisfy constraint)** Start ACL watches on **all calendars** that have at least one event with "coolcoolcool" in the **name** | `POST /calendars/{calendarId}/acl/watch` | We need notifications for any calendar flagged by the keyword scan |

## Step 6: Generated Prompt

> "Subscribe me to the external calendar **cal_meridian_drift_folio**. Then fully replace that calendar list entry so it’s **hidden**, **not selected**, and uses **color ID 7**. On that same calendar, patch the event **evt_meridian_index** to add the description **‘Catalog spine check.’** Finally, start **ACL watches on every calendar** that has at least one event whose **name contains ‘coolcoolcool.’**"

---

# PROMPT 44: Ashline Relay Commons - Availability Triangulation

## Step 1: Sample n
**n = 5** (sampled from range 4-6)

## Step 2: Sample 5 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 2 | `PUT /users/me/calendarList/{calendarId}` | CalendarList: update |
| 3 | `POST /freeBusy` | Freebusy: query |
| 4 | `GET /calendars/{calendarId}/acl/{ruleId}` | Acl: get |
| 5 | `POST /calendars/{calendarId}/acl` | Acl: insert |

## Step 3: Sample m
**m = 3** (sampled from range 0-4)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Hana** | Korean |
| **Chinedu** | Nigerian |
| **Noah** | American |

## Step 5: Action Sequence with Justification

**Theme:** A relay commons coordinating a tight window across three people

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Get the ACL rule `user:hana@test.com` on the Ashline Relay Commons calendar (ID `cal_ashline_relay_commons`) | `GET /calendars/{calendarId}/acl/{ruleId}` | Verify Hana’s current access before adding others |
| 2 | Add Chinedu (chinedu@test.com) as a writer on that calendar | `POST /calendars/{calendarId}/acl` | Chinedu will edit the relay schedule |
| 3 | Add Noah (noah@test.com) as a reader on that calendar | `POST /calendars/{calendarId}/acl` | Noah needs view access only |
| 4 | Query free/busy for Hana, Chinedu, and Noah to find the earliest **60‑minute overlap** between June 28–29, 2018, then schedule a new event on my primary calendar at that time called "Ashline Relay Briefing" | `POST /freeBusy` + `POST /calendars/{calendarId}/events` | The relay briefing must happen when all three are free |
| 5 | Fully replace the calendar list entry for Ashline Relay Commons to set `hidden=true` and `selected=false` | `PUT /users/me/calendarList/{calendarId}` | Keep the calendar available but out of the main view |

## Step 6: Generated Prompt

> "On the **Ashline Relay Commons** calendar (ID `cal_ashline_relay_commons`), check the ACL rule **user:hana@test.com** first. Then grant **Chinedu** (chinedu@test.com) **writer** access and **Noah** (noah@test.com) **reader** access. After that, use free/busy to find the **earliest 60‑minute overlap** for **Hana, Chinedu, and Noah** between **June 28–29, 2018**, and schedule a new event on my primary calendar called **Ashline Relay Briefing** at that overlap (use my timezone). Finally, update the calendar list entry so this calendar is **hidden** and **not selected**."

---

# PROMPT 45: Silverroot Observatory - Event Replace + Instances + Dual Watches

## Step 1: Sample n
**n = 6** (sampled from range 4-6)

## Step 2: Sample 6 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/acl/watch` | Acl: watch |
| 2 | `PATCH /calendars/{calendarId}` | Calendars: patch |
| 3 | `GET /calendars/{calendarId}/acl/{ruleId}` | Acl: get |
| 4 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 5 | `PUT /calendars/{calendarId}/events/{eventId}` | Events: update |
| 6 | `POST /calendars/{calendarId}/events/watch` | Events: watch |

## Step 3: Sample m
**m = 4** (sampled from range 0-4)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Zahra** | Persian |
| **Chinedu** | Nigerian |
| **Yara** | Brazilian |
| **Hana** | Korean |

## Step 5: Action Sequence with Justification

**Theme:** Observatory upkeep with a series review and strict replacement

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Get the ACL rule `user:zahra@test.com` on the Silverroot Observatory calendar (ID `cal_silverroot_observatory`) | `GET /calendars/{calendarId}/acl/{ruleId}` | Confirm Zahra’s access before watches are enabled |
| 2 | Patch the Silverroot Observatory calendar to set description "Lens rotation and night ledger" | `PATCH /calendars/{calendarId}` | Metadata needs to reflect the revised program |
| 3 | Fetch all instances of the recurring event `evt_silverroot_rotation` | `GET /calendars/{calendarId}/events/{eventId}/instances` | Review upcoming instances before making a full replacement |
| 4 | Fully replace the event `evt_silverroot_rotation` so it runs **weekly on Mondays at 7:00pm**, starting July 2, 2018, for 1 hour at "West Dome" | `PUT /calendars/{calendarId}/events/{eventId}` | The series schedule must be rewritten in full |
| 5 | Start an events watch on the Silverroot Observatory calendar | `POST /calendars/{calendarId}/events/watch` | We want change notifications on the schedule |
| 6 | Start an ACL watch on the Silverroot Observatory calendar | `POST /calendars/{calendarId}/acl/watch` | We want notifications when access changes |

## Step 6: Generated Prompt

> "On the **Silverroot Observatory** calendar (ID `cal_silverroot_observatory`), first check the ACL rule **user:zahra@test.com**. Then update the calendar description to **‘Lens rotation and night ledger.’** Next, list instances of the recurring event **evt_silverroot_rotation**, and then fully replace that event so it runs **weekly on Mondays at 7:00pm**, starting **July 2, 2018**, for **1 hour** at **West Dome**. After that, enable both an **events watch** and an **ACL watch** on this calendar. Chinedu, Yara, and Hana will be following the updates."

---

# PROMPT 46: Brineglass Works - Move, FreeBusy, Create, ACL Replace, Settings Watch

## Step 1: Sample n
**n = 6** (sampled from range 4-6)

## Step 2: Sample 6 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events/{eventId}/move` | Events: move |
| 2 | `POST /freeBusy` | Freebusy: query |
| 3 | `GET /calendars/{calendarId}/events/{eventId}` | Events: get |
| 4 | `POST /calendars/{calendarId}/events` | Events: insert |
| 5 | `PUT /calendars/{calendarId}/acl/{ruleId}` | Acl: update |
| 6 | `POST /users/me/settings/watch` | Settings: watch |

## Step 3: Sample m
**m = 2** (sampled from range 0-4)

## Step 4: Generate 2 Names
| Name | Origin |
|------|--------|
| **Lucia** | Mexican |
| **Noah** | American |

## Step 5: Action Sequence with Justification

**Theme:** Workshop logistics with a move, a new slot, and access updates

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Get the event `evt_brineglass_forge_demo` on the Brineglass Works calendar (ID `cal_brineglass_works`) | `GET /calendars/{calendarId}/events/{eventId}` | Confirm its details before moving it |
| 2 | Move that event to the "Harbor Kiln Hall" calendar (ID `cal_harbor_kiln_hall`) | `POST /calendars/{calendarId}/events/{eventId}/move` | The demo has been reassigned to a different venue calendar |
| 3 | Query free/busy for Lucia and Noah to find the earliest 30‑minute overlap on June 30, 2018 | `POST /freeBusy` | We need a quick check-in slot that works for both |
| 4 | Create a new event "Saltglass Alignment" on Brineglass Works at that overlap time | `POST /calendars/{calendarId}/events` | The alignment session must be scheduled once a slot is found |
| 5 | Fully replace Lucia’s ACL rule on Brineglass Works (rule `user:lucia@test.com`) to writer | `PUT /calendars/{calendarId}/acl/{ruleId}` | Lucia should be able to edit the workshop schedule |
| 6 | Start a settings watch for my account | `POST /users/me/settings/watch` | We want notifications if settings change |

## Step 6: Generated Prompt

> "On the **Brineglass Works** calendar (ID `cal_brineglass_works`), first fetch the event **evt_brineglass_forge_demo**, then move it to the **Harbor Kiln Hall** calendar (ID `cal_harbor_kiln_hall`). Next, use free/busy to find the **earliest 30‑minute overlap** for **Lucia** (lucia@test.com) and **Noah** (noah@test.com) on **June 30, 2018**, and create a new event **Saltglass Alignment** on Brineglass Works at that time. Then fully replace Lucia’s ACL rule (`user:lucia@test.com`) on Brineglass Works to **writer**. Finally, set up a **settings watch** for my account."

---

# PROMPT 47: Quillshore Annex - Import, ACL Check, List Entry Review, Dual Watches

## Step 1: Sample n
**n = 6** (sampled from range 4-6)

## Step 2: Sample 6 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/acl/watch` | Acl: watch |
| 2 | `GET /calendars/{calendarId}/acl/{ruleId}` | Acl: get |
| 3 | `POST /calendars/{calendarId}/events/import` | Events: import |
| 4 | `GET /users/me/calendarList/{calendarId}` | CalendarList: get |
| 5 | `POST /users/me/calendarList/watch` | CalendarList: watch |
| 6 | `GET /colors` | Colors: get |

## Step 3: Sample m
**m = 4** (sampled from range 0-4)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Tariq** | North African |
| **Linh** | Vietnamese |
| **Priya** | Indian |
| **Salma** | Egyptian |

## Step 5: Action Sequence with Justification

**Theme:** Annex setup with an import, access review, and monitoring

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Fetch the color palette and set the annex calendar to **color ID 8** | `GET /colors` | We need a known color ID for the annex |
| 2 | Import a legacy event "Quillshore Salt Index" into the Quillshore Annex calendar (ID `cal_quillshore_annex`) with iCalUID `quillshore-salt-20180630@annex` | `POST /calendars/{calendarId}/events/import` | The entry must be imported from a legacy system |
| 3 | Get the ACL rule `user:linh@test.com` on Quillshore Annex | `GET /calendars/{calendarId}/acl/{ruleId}` | Verify Linh’s current access before announcing the change |
| 4 | Retrieve the calendar list entry for Quillshore Annex | `GET /users/me/calendarList/{calendarId}` | Confirm the subscription settings before monitoring |
| 5 | Start an ACL watch on Quillshore Annex | `POST /calendars/{calendarId}/acl/watch` | We want notifications if access changes |
| 6 | Start a calendar list watch for my calendar list | `POST /users/me/calendarList/watch` | We want notifications if subscriptions change |

## Step 6: Generated Prompt

> "Pull the **calendar color palette** and set **Quillshore Annex** (ID `cal_quillshore_annex`) to **color ID 8**. Then **import** the legacy entry **Quillshore Salt Index** into that calendar for June 30, 2018 from 2:00pm–3:00pm, location **Brine Archive Hall**, iCalUID `quillshore-salt-20180630@annex`. After that, check the ACL rule **user:linh@test.com** on Quillshore Annex and show me the calendar list entry for that calendar. Finally, start an **ACL watch** on Quillshore Annex and a **calendar list watch** for my account."

---

# PROMPT 48: Vellumwind Pavilion - Access Audit + Settings Watch

## Step 1: Sample n
**n = 5** (sampled from range 4-6)

## Step 2: Sample 5 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /users/me/settings/watch` | Settings: watch |
| 2 | `GET /users/me/calendarList/{calendarId}` | CalendarList: get |
| 3 | `GET /calendars/{calendarId}/acl/{ruleId}` | Acl: get |
| 4 | `GET /calendars/{calendarId}/acl` | Acl: list |
| 5 | `GET /calendars/{calendarId}/acl` | Acl: list |

## Step 3: Sample m
**m = 0** (sampled from range 0-4)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** Pavilion access audit with a settings watch for future alerts

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Retrieve the calendar list entry for Vellumwind Pavilion (ID `cal_vellumwind_pavilion`) | `GET /users/me/calendarList/{calendarId}` | Confirm subscription details before auditing access |
| 2 | List all ACL rules on Vellumwind Pavilion | `GET /calendars/{calendarId}/acl` | Review everyone who currently has access |
| 3 | Fetch the ACL rule `user:archive@vellumwind.example` on Vellumwind Pavilion | `GET /calendars/{calendarId}/acl/{ruleId}` | Check a specific rule’s details after the list |
| 4 | List all ACL rules again to confirm no changes during the audit | `GET /calendars/{calendarId}/acl` | Ensures the access list is stable |
| 5 | Start a settings watch for my account | `POST /users/me/settings/watch` | We want notifications if settings change after the audit |

## Step 6: Generated Prompt

> "Please pull the calendar list entry for **Vellumwind Pavilion** (ID `cal_vellumwind_pavilion`), then list **all ACL rules** on that calendar. After that, fetch the specific ACL rule **user:archive@vellumwind.example** and list the ACLs once more to confirm nothing changed during the audit. Finally, set up a **settings watch** for my account."

---

# PROMPT 49: Thistlewire Workshop - Instances Review, Create Event, List Watch, Calendar Delete

## Step 1: Sample n
**n = 5** (sampled from range 4-6)

## Step 2: Sample 5 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 2 | `DELETE /calendars/{calendarId}` | Calendars: delete |
| 3 | `POST /calendars/{calendarId}/events` | Events: insert |
| 4 | `POST /users/me/calendarList/watch` | CalendarList: watch |
| 5 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |

## Step 3: Sample m
**m = 2** (sampled from range 0-4)

## Step 4: Generate 2 Names
| Name | Origin |
|------|--------|
| **Ewa** | Polish |
| **Kofi** | Ghanaian |

## Step 5: Action Sequence with Justification

**Theme:** Workshop planning with a series review, a new event, and cleanup

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List instances of the recurring event `evt_thistlewire_cycles` on the Thistlewire Workshop calendar (ID `cal_thistlewire_workshop`) | `GET /calendars/{calendarId}/events/{eventId}/instances` | We need to see the upcoming cycle before adding a new session |
| 2 | Create a one‑off event "Bronze Fret Alignment" on that calendar for June 30, 2018, 10:00am–11:00am | `POST /calendars/{calendarId}/events` | The workshop needs a standalone session |
| 3 | Patch the calendar list entry for Thistlewire Workshop to set `hidden=true` | `PATCH /users/me/calendarList/{calendarId}` | It should be out of the main view afterward |
| 4 | Start a calendar list watch for my account | `POST /users/me/calendarList/watch` | We want alerts if subscriptions change |
| 5 | Delete the obsolete "Copperwind Annex" calendar (ID `cal_copperwind_annex`) | `DELETE /calendars/{calendarId}` | The annex calendar should be retired |

## Step 6: Generated Prompt

> "On the **Thistlewire Workshop** calendar (ID `cal_thistlewire_workshop`), list instances of the recurring event **evt_thistlewire_cycles** first. Then add a one‑off event **Bronze Fret Alignment** on June 30, 2018 from 10:00am–11:00am. After that, hide the Thistlewire Workshop calendar in my list and start a **calendar list watch** for my account. Finally, delete the obsolete **Copperwind Annex** calendar (ID `cal_copperwind_annex`). Ewa and Kofi will need the final confirmation."

---

# PROMPT 50: Emberveil Rookery - Subscribe, Watch, Revoke, Delete Calendar

## Step 1: Sample n
**n = 5** (sampled from range 4-6)

## Step 2: Sample 5 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events/watch` | Events: watch |
| 2 | `DELETE /calendars/{calendarId}` | Calendars: delete |
| 3 | `POST /users/me/calendarList` | CalendarList: insert |
| 4 | `POST /users/me/settings/watch` | Settings: watch |
| 5 | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Acl: delete |

## Step 3: Sample m
**m = 3** (sampled from range 0-4)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Hiro** | Japanese |
| **Sana** | Pakistani |
| **Salma** | Egyptian |

## Step 5: Action Sequence with Justification

**Theme:** Rookery operations with subscription, monitoring, and cleanup

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Subscribe me to the external calendar `cal_emberveil_rookery` | `POST /users/me/calendarList` | The rookery calendar is external and must be added |
| 2 | Start an events watch on the Emberveil Rookery calendar | `POST /calendars/{calendarId}/events/watch` | We need notifications for schedule changes |
| 3 | Revoke Salma’s access on Emberveil Rookery (rule `user:salma@test.com`) | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Her access should be removed immediately |
| 4 | Start a settings watch for my account | `POST /users/me/settings/watch` | We want alerts if settings change during the rollout |
| 5 | Delete the obsolete "Ashfeather Annex" calendar (ID `cal_ashfeather_annex`) | `DELETE /calendars/{calendarId}` | The annex calendar is being retired |

## Step 6: Generated Prompt

> "Subscribe me to the external calendar **cal_emberveil_rookery**. Then start an **events watch** on that calendar. Remove **Salma’s** access from Emberveil Rookery (rule `user:salma@test.com`). Also, set up a **settings watch** for my account. Finally, delete the obsolete **Ashfeather Annex** calendar (ID `cal_ashfeather_annex`). Hiro and Sana should be kept in the loop once it’s done."

---

# PROMPT 51: Windchord Cartotheca - Create Calendar, Color, Metadata, ACL Replace

## Step 1: Sample n
**n = 6** (sampled from range 4-6)

## Step 2: Sample 6 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |
| 2 | `GET /users/me/calendarList/{calendarId}` | CalendarList: get |
| 3 | `POST /calendars` | Calendars: insert |
| 4 | `GET /colors` | Colors: get |
| 5 | `PUT /calendars/{calendarId}/acl/{ruleId}` | Acl: update |
| 6 | `PATCH /calendars/{calendarId}` | Calendars: patch |

## Step 3: Sample m
**m = 4** (sampled from range 0-4)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Lucia** | Mexican |
| **Zahra** | Persian |
| **Adebayo** | Nigerian |
| **Aiko** | Japanese |

## Step 5: Action Sequence with Justification

**Theme:** A cartotheca calendar with visual tuning and strict access control

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Fetch the color palette and set the new calendar to **color ID 11** | `GET /colors` | We need a known color ID for the calendar list entry |
| 2 | Create a new calendar called "Windchord Cartotheca" | `POST /calendars` | The cartotheca needs its own schedule |
| 3 | Retrieve the calendar list entry for Windchord Cartotheca | `GET /users/me/calendarList/{calendarId}` | We need the current entry before patching it |
| 4 | Patch the calendar list entry to set `hidden=false` and `selected=true` | `PATCH /users/me/calendarList/{calendarId}` | The calendar should be visible by default |
| 5 | Patch the calendar metadata to set description "Atlas repair bays" | `PATCH /calendars/{calendarId}` | Add a concise purpose for the calendar |
| 6 | Fully replace Aiko’s ACL rule on Windchord Cartotheca (rule `user:aiko@test.com`) to **writer** | `PUT /calendars/{calendarId}/acl/{ruleId}` | Aiko needs edit access to manage the atlas work |

## Step 6: Generated Prompt

> "Create a new calendar named **Windchord Cartotheca**. Pull the **calendar color palette** and set it to **color ID 11**. Then fetch its calendar list entry and patch it so the calendar is **visible** and **selected**. Also update the calendar description to **‘Atlas repair bays.’** Finally, fully replace **Aiko’s** ACL rule (`user:aiko@test.com`) on this calendar to **writer**. Lucia, Zahra, and Adebayo need to be informed once it’s ready."

---

# PROMPT 52: Stoneglow Depot - Clear, Calendar Replace, ACL Replace, Move Event, Settings Watch

## Step 1: Sample n
**n = 6** (sampled from range 4-6)

## Step 2: Sample 6 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `PUT /calendars/{calendarId}` | Calendars: update |
| 2 | `POST /users/me/settings/watch` | Settings: watch |
| 3 | `POST /calendars/{calendarId}/clear` | Calendars: clear |
| 4 | `GET /users/me/calendarList/{calendarId}` | CalendarList: get |
| 5 | `PUT /calendars/{calendarId}/acl/{ruleId}` | Acl: update |
| 6 | `POST /calendars/{calendarId}/events/{eventId}/move` | Events: move |

## Step 3: Sample m
**m = 0** (sampled from range 0-4)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** Depot reset with a strict calendar replacement and an event relocation

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Retrieve the calendar list entry for Stoneglow Depot (ID `cal_stoneglow_depot`) | `GET /users/me/calendarList/{calendarId}` | Confirm subscription status before changes |
| 2 | Clear all events from Stoneglow Depot | `POST /calendars/{calendarId}/clear` | The depot is being reset |
| 3 | Fully replace the Stoneglow Depot calendar metadata to summary "Stoneglow Depot", description "Crate intake ledger", and timezone America/Los_Angeles | `PUT /calendars/{calendarId}` | Full replacement ensures all fields are explicitly set |
| 4 | Fully replace the ACL rule `user:clerk@stoneglow.example` on Stoneglow Depot to **reader** | `PUT /calendars/{calendarId}/acl/{ruleId}` | The clerk should be view‑only after the reset |
| 5 | Move event `evt_stoneglow_manifest` from Stoneglow Depot to the "Harbor Ledger" calendar (ID `cal_harbor_ledger`) | `POST /calendars/{calendarId}/events/{eventId}/move` | The manifest must live on the shared ledger calendar |
| 6 | Start a settings watch for my account | `POST /users/me/settings/watch` | We want notifications if settings change |

## Step 6: Generated Prompt

> "Check my calendar list entry for **Stoneglow Depot** (ID `cal_stoneglow_depot`) first. Then **clear all events** from that calendar. After that, fully replace the calendar metadata with summary **Stoneglow Depot**, description **‘Crate intake ledger’**, and timezone **America/Los_Angeles**. Fully replace the ACL rule **user:clerk@stoneglow.example** to **reader**. Move **evt_stoneglow_manifest** from Stoneglow Depot to **Harbor Ledger** (ID `cal_harbor_ledger`). Finally, set up a **settings watch** for my account."

---

# PROMPT 53: Crystalfold Foundry - Replace + Delete Events, Unsubscribe

## Step 1: Sample n
**n = 4** (sampled from range 4-6)

## Step 2: Sample 4 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 2 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 3 | `DELETE /users/me/calendarList/{calendarId}` | CalendarList: delete |
| 4 | `PUT /calendars/{calendarId}/events/{eventId}` | Events: update |

## Step 3: Sample m
**m = 4** (sampled from range 0-4)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Fatima** | Moroccan |
| **Mateusz** | Polish |
| **Noah** | American |
| **Kofi** | Ghanaian |

## Step 5: Action Sequence with Justification

**Theme:** Foundry cleanup with a strict replacement and two removals

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Fully replace the event `evt_crystalfold_quench` on the Crystalfold Foundry calendar (ID `cal_crystalfold_foundry`) to July 1, 2018, 9:00am–10:30am at "Forge Bay 2" | `PUT /calendars/{calendarId}/events/{eventId}` | The session timing and location were revised |
| 2 | Delete the event `evt_crystalfold_slag` from Crystalfold Foundry | `DELETE /calendars/{calendarId}/events/{eventId}` | The slag briefing is canceled |
| 3 | Delete the event `evt_crystalfold_mold` from Crystalfold Foundry | `DELETE /calendars/{calendarId}/events/{eventId}` | The mold prep session is canceled |
| 4 | Unsubscribe me from the "Old Lattice Mill" calendar (ID `cal_old_lattice_mill`) | `DELETE /users/me/calendarList/{calendarId}` | That calendar is no longer needed |

## Step 6: Generated Prompt

> "On the **Crystalfold Foundry** calendar (ID `cal_crystalfold_foundry`), fully replace **evt_crystalfold_quench** so it’s on **July 1, 2018 from 9:00am–10:30am** at **Forge Bay 2**. Then delete **evt_crystalfold_slag** and **evt_crystalfold_mold**. Finally, unsubscribe me from the **Old Lattice Mill** calendar (ID `cal_old_lattice_mill`). Let Fatima, Mateusz, Noah, and Kofi know when it’s done."

---

# PROMPT 54: Sablewind Archive - Create Calendar, Share, Revoke, List Entry Patch, Settings Watch

## Step 1: Sample n
**n = 6** (sampled from range 4-6)

## Step 2: Sample 6 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars` | Calendars: insert |
| 2 | `GET /users/me/calendarList/{calendarId}` | CalendarList: get |
| 3 | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Acl: delete |
| 4 | `POST /users/me/settings/watch` | Settings: watch |
| 5 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 6 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |

## Step 3: Sample m
**m = 4** (sampled from range 0-4)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Sana** | Pakistani |
| **Salma** | Egyptian |
| **Keiko** | Japanese |
| **Ewa** | Polish |

## Step 5: Action Sequence with Justification

**Theme:** Archive setup with a share, a revoke, and list tuning

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a new calendar named "Sablewind Archive" | `POST /calendars` | The archive needs a dedicated calendar |
| 2 | Retrieve the calendar list entry for Sablewind Archive | `GET /users/me/calendarList/{calendarId}` | We need the current entry before patching it |
| 3 | Patch the calendar list entry to set `hidden=false` and color ID 5 | `PATCH /users/me/calendarList/{calendarId}` | The archive should be visible with a defined color |
| 4 | Share Sablewind Archive with Keiko (keiko@test.com) as writer | `POST /calendars/{calendarId}/acl` | Keiko will edit the archive schedule |
| 5 | Revoke Salma’s access on Sablewind Archive (rule `user:salma@test.com`) | `DELETE /calendars/{calendarId}/acl/{ruleId}` | Salma should be removed from access |
| 6 | Start a settings watch for my account | `POST /users/me/settings/watch` | We want notifications if settings change |

## Step 6: Generated Prompt

> "Create a new calendar called **Sablewind Archive**. Then fetch its calendar list entry and set it to **visible** (not hidden) with **color ID 5**. Share the calendar with **Keiko** (keiko@test.com) as **writer**, and remove **Salma’s** access (rule `user:salma@test.com`). Finally, set up a **settings watch** for my account. Sana and Ewa should be notified once this is done."

---

# PROMPT 55: Skyloom Observatory - Event Replace, ACL Replace, Events Watch

## Step 1: Sample n
**n = 5** (sampled from range 4-6)

## Step 2: Sample 5 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `PUT /calendars/{calendarId}/events/{eventId}` | Events: update |
| 2 | `GET /calendars/{calendarId}/events` | Events: list |
| 3 | `PUT /calendars/{calendarId}/acl/{ruleId}` | Acl: update |
| 4 | `POST /calendars/{calendarId}/events/watch` | Events: watch |
| 5 | `GET /calendars/{calendarId}/events` | Events: list |

## Step 3: Sample m
**m = 0** (sampled from range 0-4)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** Observatory maintenance with a strict event replacement and monitoring

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List events on the Skyloom Observatory calendar (ID `cal_skyloom_observatory`) to confirm the target event is present | `GET /calendars/{calendarId}/events` | Establish current schedule before replacement |
| 2 | Fully replace the event `evt_skyloom_alignment` to July 2, 2018, 8:00pm–9:00pm at "Upper Ring" | `PUT /calendars/{calendarId}/events/{eventId}` | The alignment slot must be rewritten in full |
| 3 | Fully replace the ACL rule `user:mechanic@skyloom.example` to **reader** | `PUT /calendars/{calendarId}/acl/{ruleId}` | Access should be view‑only after the update |
| 4 | Start an events watch on the Skyloom Observatory calendar | `POST /calendars/{calendarId}/events/watch` | We want notifications if the schedule changes |
| 5 | List events again to confirm the replacement appears | `GET /calendars/{calendarId}/events` | Verifies the new slot is visible |

## Step 6: Generated Prompt

> "On the **Skyloom Observatory** calendar (ID `cal_skyloom_observatory`), list events first. Then fully replace **evt_skyloom_alignment** so it’s on **July 2, 2018 from 8:00pm–9:00pm** at **Upper Ring**. Also fully replace the ACL rule **user:mechanic@skyloom.example** to **reader**. After that, start an **events watch** on the Skyloom Observatory calendar and list events again to confirm the change."

---

# PROMPT 56: Ironlace Conservatory - Clear, Replace Event, Instances, ACL Patch, Delete Calendar

## Step 1: Sample n
**n = 6** (sampled from range 4-6)

## Step 2: Sample 6 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `DELETE /calendars/{calendarId}` | Calendars: delete |
| 2 | `POST /channels/stop` | Channels: stop |
| 3 | `POST /calendars/{calendarId}/clear` | Calendars: clear |
| 4 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 5 | `PUT /calendars/{calendarId}/events/{eventId}` | Events: update |
| 6 | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Acl: patch |

## Step 3: Sample m
**m = 3** (sampled from range 0-4)

## Step 4: Generate 3 Names
| Name | Origin |
|------|--------|
| **Kofi** | Ghanaian |
| **Ewa** | Polish |
| **Mina** | Iranian |

## Step 5: Action Sequence with Justification

**Theme:** Conservatory reset with a series review and a hard retirement

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List instances of the recurring event `evt_ironlace_orchid` on the Ironlace Conservatory calendar (ID `cal_ironlace_conservatory`) | `GET /calendars/{calendarId}/events/{eventId}/instances` | Review remaining occurrences before the reset |
| 2 | Clear all events from Ironlace Conservatory | `POST /calendars/{calendarId}/clear` | The conservatory is being wiped for a new season |
| 3 | Fully replace the event `evt_ironlace_orchid` to July 3, 2018, 10:00am–11:00am at "Glassbed Hall" | `PUT /calendars/{calendarId}/events/{eventId}` | The first post‑reset inspection needs a clean replacement |
| 4 | Patch the ACL rule `user:mina@test.com` on Ironlace Conservatory to **reader** | `PATCH /calendars/{calendarId}/acl/{ruleId}` | Mina’s access should be view‑only after reset |
| 5 | Stop the old channel with id `chan_ironlace_12` and resourceId `res_ironlace_12` | `POST /channels/stop` | The previous watch is obsolete |
| 6 | Delete the retired "Old Driftgreen" calendar (ID `cal_old_driftgreen`) | `DELETE /calendars/{calendarId}` | The old calendar should be removed entirely |

## Step 6: Generated Prompt

> "On the **Ironlace Conservatory** calendar (ID `cal_ironlace_conservatory`), list instances of **evt_ironlace_orchid** first. Then **clear all events** from that calendar. After the reset, fully replace **evt_ironlace_orchid** so it’s on **July 3, 2018 from 10:00am–11:00am** at **Glassbed Hall**. Patch Mina’s ACL rule (`user:mina@test.com`) to **reader**. Then stop the old channel with id `chan_ironlace_12` and resourceId `res_ironlace_12`. Finally, delete the **Old Driftgreen** calendar (ID `cal_old_driftgreen`)."

---

# PROMPT 57: Tideglass Registry - Subscribe, List, Patch Entry, Import Event

## Step 1: Sample n
**n = 4** (sampled from range 4-6)

## Step 2: Sample 4 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars/{calendarId}/events/import` | Events: import |
| 2 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |
| 3 | `GET /users/me/calendarList` | CalendarList: list |
| 4 | `POST /users/me/calendarList` | CalendarList: insert |

## Step 3: Sample m
**m = 4** (sampled from range 0-4)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Salma** | Egyptian |
| **Linh** | Vietnamese |
| **Sven** | Swedish |
| **Mateusz** | Polish |

## Step 5: Action Sequence with Justification

**Theme:** Registry onboarding with a subscription and a legacy import

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List my calendar list to confirm whether Tideglass Registry is already present | `GET /users/me/calendarList` | Avoid duplicate subscriptions |
| 2 | Subscribe me to the external calendar `cal_tideglass_registry` | `POST /users/me/calendarList` | The registry is external and must be added |
| 3 | Patch the Tideglass Registry calendar list entry to set `hidden=true` and color ID 4 | `PATCH /users/me/calendarList/{calendarId}` | Keep it out of the main view but visually distinct |
| 4 | Import the legacy event "Tideglass Ledger Seal" into Tideglass Registry for July 4, 2018, 1:00pm–2:00pm, location "Seawick Vault", iCalUID `tideglass-seal-20180704@registry` | `POST /calendars/{calendarId}/events/import` | The event must be imported from a legacy log |

## Step 6: Generated Prompt

> "List my calendars first so we don’t duplicate anything. Then subscribe me to the external **Tideglass Registry** calendar (ID `cal_tideglass_registry`). After that, hide that calendar in my list and set it to **color ID 4**. Finally, **import** the legacy entry **Tideglass Ledger Seal** into the Tideglass Registry calendar for **July 4, 2018 from 1:00pm–2:00pm** at **Seawick Vault**, iCalUID `tideglass-seal-20180704@registry`. Salma, Linh, Sven, and Mateusz are the stakeholders to keep in the loop."

---

# PROMPT 58: Glassreef Codex - Count, Move, Patch, Watch, Clear

## Step 1: Sample n
**n = 7** (sampled from range 7-13)

## Step 2: Sample 7 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `GET /calendars/{calendarId}/acl/{ruleId}` | Acl: get |
| 2 | `PATCH /calendars/{calendarId}/events/{eventId}` | Events: patch |
| 3 | `POST /calendars/{calendarId}/events/{eventId}/move` | Events: move |
| 4 | `POST /calendars/{calendarId}/clear` | Calendars: clear |
| 5 | `GET /users/me/settings/{setting}` | Settings: get |
| 6 | `GET /colors` | Colors: get |
| 7 | `POST /calendars/{calendarId}/acl/watch` | Acl: watch |

## Step 3: Sample m
**m = 0** (sampled from range 0-6)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** Glassreef archive tally with a moved log entry and access monitoring

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Fetch the calendar color palette so we can reference a color ID in the new log entry | `GET /colors` | We need a palette reference before annotating the log |
| 2 | Get my `timezone` setting | `GET /users/me/settings/{setting}` | Ensures the tally event uses my correct timezone |
| 3 | List events on **Glassreef Codex** (ID `cal_glassreef_codex`) for July 1-31, 2018 and **count how many** have "Tide-loom" in the summary | `GET /calendars/{calendarId}/events` | Required to compute the count used in the new event description |
| 4 | Move the template event `evt_kelp_murmur_template` from `cal_kelpshade_staging` into **Glassreef Codex** | `POST /calendars/{calendarId}/events/{eventId}/move` | Creates the tally log entry in the correct calendar |
| 5 | Patch the moved event to set summary "Tide-loom Count Ledger", location "Pearlwork Desk", and **description including the count** | `PATCH /calendars/{calendarId}/events/{eventId}` | Records the computed count in the event description |
| 6 | Fetch the ACL rule `user:archivist@glassreef.example` on **Glassreef Codex** | `GET /calendars/{calendarId}/acl/{ruleId}` | Confirm current access before enabling monitoring |
| 7 | Start an ACL watch on **Glassreef Codex** | `POST /calendars/{calendarId}/acl/watch` | We want alerts if access changes after the update |
| 8 | Clear all events from the **Barnacle Practice** calendar (ID `cal_barnacle_practice`) | `POST /calendars/{calendarId}/clear` | Retires the old practice calendar after the tally is logged |

## Step 6: Generated Prompt

> "For the **Glassreef Codex** calendar (ID `cal_glassreef_codex`), I need a tally log. First, check the **calendar color palette** and confirm my **timezone** setting. Then list **July 1-31, 2018** events on Glassreef Codex and **count how many** include **\"Tide-loom\"** in the summary. Move the template event **evt_kelp_murmur_template** from **cal_kelpshade_staging** into Glassreef Codex and update it to **Tide-loom Count Ledger** at **Pearlwork Desk**, with a description that explicitly includes that count. Also fetch the ACL rule **user:archivist@glassreef.example** on Glassreef Codex, start an **ACL watch** for that calendar, and finally **clear** the old **Barnacle Practice** calendar (ID `cal_barnacle_practice`)."

---

# PROMPT 59: Seabriar Leave Ledger - Count, Book, Clear Conflicts, Pigeon Check

## Step 1: Sample n
**n = 11** (sampled from range 7-13)

## Step 2: Sample 11 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /channels/stop` | Channels: stop |
| 2 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 3 | `GET /calendars/{calendarId}` | Calendars: get |
| 4 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 5 | `POST /calendars/{calendarId}/acl` | Acl: insert |
| 6 | `POST /calendars/{calendarId}/events/quickAdd` | Events: quickAdd |
| 7 | `PATCH /users/me/calendarList/{calendarId}` | CalendarList: patch |
| 8 | `PUT /calendars/{calendarId}` | Calendars: update |
| 9 | `GET /calendars/{calendarId}/events/{eventId}/instances` | Events: instances |
| 10 | `GET /users/me/calendarList` | CalendarList: list |
| 11 | `POST /calendars/{calendarId}/events` | Events: insert |

## Step 3: Sample m
**m = 2** (sampled from range 0-6)

## Step 4: Generate 2 Names
| Name | Origin |
|------|--------|
| **Aiko** | Japanese |
| **Priya** | Indian |

## Step 5: Action Sequence with Justification

**Theme:** Leave planning with a tally-driven vacation block, conflict cleanup, and a pigeon-timed reschedule

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | List my calendar list to confirm the **Seabriar Leave Ledger** calendar is present (ID `cal_seabriar_leave`) | `GET /users/me/calendarList` | Avoids using the wrong calendar for leave accounting |
| 2 | Get the Seabriar Leave Ledger calendar metadata | `GET /calendars/{calendarId}` | Confirms timezone/summary before scheduling |
| 3 | List instances of the recurring event `evt_used_vacation_day` on Seabriar Leave Ledger for Jan 1–Aug 9, 2018 and **count the total days used** | `GET /calendars/{calendarId}/events/{eventId}/instances` | Provides the used-days count needed to compute the remaining leave |
| 4 | List instances of the recurring event `evt_company_blackout` to verify any blackout days that might overlap the new leave | `GET /calendars/{calendarId}/events/{eventId}/instances` | Ensures the planned leave respects existing blackout rules |
| 5 | List instances of the recurring event `evt_weekend_silence` as a reminder that **no events can occur on weekends** | `GET /calendars/{calendarId}/events/{eventId}/instances` | Reinforces the weekend restriction before rescheduling |
| 6 | Update the Seabriar Leave Ledger calendar description to "Leave ledger and tally-based booking" | `PUT /calendars/{calendarId}` | Keeps the calendar metadata aligned with its purpose |
| 7 | Share Seabriar Leave Ledger with Aiko (aiko@test.com) as **reader** | `POST /calendars/{calendarId}/acl` | Aiko needs visibility into the leave tally |
| 8 | Patch the calendar list entry for Seabriar Leave Ledger to set `hidden=false` and color ID 10 | `PATCH /users/me/calendarList/{calendarId}` | Keeps the ledger visible and easily distinguishable |
| 9 | Create a new vacation event starting **August 10, 2018** that lasts **(20 - used_days)** business days, summary "Seabriar Leave Block" | `POST /calendars/{calendarId}/events` | Books the vacation period based on the computed count |
| 10 | Quick-add a reminder: "Send pigeon letter Aug 10, 2018 9am" | `POST /calendars/{calendarId}/events/quickAdd` | Ensures the pigeon dispatch is scheduled |
| 11 | Stop the old channel `chan_leave_09` / `res_leave_09` | `POST /channels/stop` | Cleans up an obsolete watch |
| 12 | **(Extra to satisfy constraints)** List events on my primary calendar during the leave window and **delete any events that overlap** | `GET /calendars/{calendarId}/events` + `DELETE /calendars/{calendarId}/events/{eventId}` | Required to cancel interfering events during the vacation |
| 13 | **(Extra to satisfy constraints)** Check whether a pigeon sent Aug 10 arrives before **Aug 15, 2018** (arrival = Aug 16). If not, move event `evt_cliffside_pact` to the **earliest weekday** after Aug 15 that doesn't overlap the vacation and add a note "Cannot occur on weekends" | `PATCH /calendars/{calendarId}/events/{eventId}` | Meets the delivery constraint and weekday-only requirement |

## Step 6: Generated Prompt

> "Please help me plan leave using the **Seabriar Leave Ledger** calendar (ID `cal_seabriar_leave`). First list my calendar list to confirm the ledger is there, and fetch that calendar’s metadata. Then count how many vacation days I’ve already used by listing instances of **evt_used_vacation_day** from **Jan 1 to Aug 9, 2018**. Use that count to book my vacation **starting Aug 10, 2018** for the remaining days (assume the annual allowance is **20 days**). Before you lock it in, check instances of **evt_company_blackout** and **evt_weekend_silence** so you don’t place anything on weekends. Update the ledger description to "Leave ledger and tally-based booking," share the ledger with **Aiko (aiko@test.com)** as a **reader**, and set its calendar list entry to **visible** with **color ID 10**. Create the vacation block event on the ledger, and quick-add a reminder: "Send pigeon letter Aug 10, 2018 9am." Also stop the old channel **chan_leave_09** / **res_leave_09**.
>
> Next, cancel **all events on my primary calendar** that overlap the vacation window. Finally, I want to know if a pigeon letter sent on **Aug 10** (it takes **6 days**) would arrive before when the "Clilffside Pact" (**evt_cliffside_pact**) is scheduled. If it would not, move it to the **earliest weekday** after the arrival of the pigeon mail that doesn’t overlap my vacation.

---

# PROMPT 60: Ivory Loom Archive - Purge "blood" Events

## Step 1: Sample n
**n = 4** (sampled from range 4-6)

## Step 2: Sample 4 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 2 | `GET /calendars/{calendarId}/acl` | Acl: list |
| 3 | `GET /calendars/{calendarId}/events` | Events: list |
| 4 | `GET /users/me/settings/{setting}` | Settings: get |

## Step 3: Sample m
**m = 0** (sampled from range 0-4)

## Step 4: Generate 0 Names
*(none)*

## Step 5: Action Sequence with Justification

**Theme:** Archive cleanup to purge sensitive "blood" references

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Fetch my `timezone` setting | `GET /users/me/settings/{setting}` | Ensures the cleanup report references the correct timezone if needed |
| 2 | **(Extra to satisfy constraint)** Update the **Ivory Loom Archive** calendar timezone to match **Ewa’s** (Europe/Warsaw) because her pierogi timer is “more accurate than my wristwatch” | `PATCH /calendars/{calendarId}` | Meets the request to switch to another user’s timezone, with a playful reason |
| 3 | List ACL rules on the **Ivory Loom Archive** calendar (ID `cal_ivory_loom_archive`) | `GET /calendars/{calendarId}/acl` | Confirms access before deletions |
| 4 | List events on Ivory Loom Archive and identify any events whose **title or description contains "blood"** | `GET /calendars/{calendarId}/events` | We must find all offending events before removal |
| 5 | Delete every event on Ivory Loom Archive that contains "blood" in the title or description | `DELETE /calendars/{calendarId}/events/{eventId}` | Removes all prohibited content from the calendar |

## Step 6: Generated Prompt

> "On the **Ivory Loom Archive** calendar (ID `cal_ivory_loom_archive`), I need a cleanup. First, switch my calendar’s timezone to match **Ewa’s** — her pierogi timer is somehow more reliable than my wristwatch. Next, list the calendar’s **ACL rules** so we confirm access. After that, list events on Ivory Loom Archive and identify every event whose **title or description contains the word \"blood\"**. **Delete all of those events**."

---

# PROMPT 61: Wavelock Guest Sweep - Purge Attendee Events

## Step 1: Sample n
**n = 9** (sampled from range 7-13)

## Step 2: Sample 9 Endpoints (with replacement)
| # | Endpoint | Resource:Method |
|---|----------|-----------------|
| 1 | `POST /calendars` | Calendars: insert |
| 2 | `PUT /calendars/{calendarId}` | Calendars: update |
| 3 | `DELETE /calendars/{calendarId}/events/{eventId}` | Events: delete |
| 4 | `POST /freeBusy` | Freebusy: query |
| 5 | `DELETE /users/me/calendarList/{calendarId}` | CalendarList: delete |
| 6 | `GET /calendars/{calendarId}/events` | Events: list |
| 7 | `POST /freeBusy` | Freebusy: query |
| 8 | `POST /users/me/calendarList/watch` | CalendarList: watch |
| 9 | `POST /users/me/settings/watch` | Settings: watch |

## Step 3: Sample m
**m = 4** (sampled from range 0-6)

## Step 4: Generate 4 Names
| Name | Origin |
|------|--------|
| **Aiko** | Japanese |
| **Farid** | Iranian |
| **Lucia** | Mexican |
| **Oksana** | Ukrainian |

## Step 5: Action Sequence with Justification

**Theme:** A guest-sweep cleanup with a comedic embargo on certain attendees

| Step | Action | Endpoint | Justification |
|------|--------|----------|---------------|
| 1 | Create a new calendar called **Wavelock Guest Sweep** | `POST /calendars` | A dedicated ledger for the cleanup is needed |
| 2 | Fully update that calendar to set timezone **Europe/Berlin** and description "Guest sweep log and embargo notes" | `PUT /calendars/{calendarId}` | Makes the ledger explicit and consistent |
| 3 | List events on my **primary calendar** and identify all events where **Aiko, Farid, Lucia, or Oksana** appear in the attendee list | `GET /calendars/{calendarId}/events` | We must find all affected events before deleting them |
| 4 | Delete every event on my primary calendar that lists **Aiko, Farid, Lucia, or Oksana** as attendees | `DELETE /calendars/{calendarId}/events/{eventId}` | Purges the unwanted events |
| 5 | Run a free/busy query for those four across Aug 1–7, 2018 | `POST /freeBusy` | Confirms they’re busy so we don’t try to reschedule |
| 6 | Run another free/busy query for Aug 8–14, 2018 to double‑check there’s no easy replacement slot | `POST /freeBusy` | Reinforces the decision to cancel instead of reschedule |
| 7 | **(Extra to satisfy constraint)** Schedule a **weekly** 30‑minute event on my primary calendar at the **earliest** time that doesn’t conflict with any of those four attendees | `POST /calendars/{calendarId}/events` | Uses free/busy results to set a conflict‑free weekly slot |
| 8 | Unsubscribe me from the legacy calendar **cal_wavelock_legacy** | `DELETE /users/me/calendarList/{calendarId}` | Keeps my calendar list tidy after the sweep |
| 9 | Start a watch on my calendar list | `POST /users/me/calendarList/watch` | We want notifications if subscriptions change |
| 10 | Start a watch on my settings | `POST /users/me/settings/watch` | We want notifications if settings change during the cleanup |

## Step 6: Generated Prompt

> "I need a cleanup sweep. Create a new calendar named **Wavelock Guest Sweep** and update its details so the timezone is **Europe/Berlin** with the description ‘Guest sweep log and embargo notes.’ Then, on my **primary calendar**, find **every event** where **Aiko, Farid, Lucia, or Oksana** are listed as attendees and **cancel/delete** those events — they keep trying to book my calendar for their midnight ghost‑parade rehearsals. Before you finish, run two **free/busy** checks for those four (Aug 1–7 and Aug 8–14, 2018) just to confirm we shouldn’t reschedule. Using those free/busy results, schedule a **weekly 30‑minute event** on my primary calendar at the **earliest** time that doesn’t conflict with any of their schedules (start it the week of Aug 20). Add them as attendees there and make sure that the location is set as "The Hall of the Mountain King". Also remove me from **cal_wavelock_legacy**, and set up watches on **my calendar list** and **my settings** so we catch any surprise changes."

---
