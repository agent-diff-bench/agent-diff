# Generated Linear Test Prompts

## Test Generation #1

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 10**

### Step 2: Sample n endpoints with replacement from Linear API

Available endpoints:
- Queries: `teams`, `issues`, `issue`, `workflowStates`, `users`, `issueLabels`, `comments`
- Mutations: `issueCreate`, `issueUpdate`, `commentCreate`, `teamCreate`, `issueLabelCreate`, `commentUpdate`, `commentDelete`, `issueLabelUpdate`, `workflowStateCreate`, `workflowStateArchive`, `teamMembershipCreate`, `issueRelationCreate`

**Sampled endpoints (with replacement):**
1. `teamCreate`
2. `issueCreate`
3. `issueCreate` (duplicate)
4. `issueUpdate`
5. `issueLabelCreate`
6. `commentCreate`
7. `issueRelationCreate`
8. `workflowStateCreate`
9. `teams`
10. `users`

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 4**

**Names from different cultural traditions:**
1. **Kenji** (Japanese)
2. **Fatima** (Iranian/Persian)
3. **Bogdan** (Ukrainian)
4. **Adaeze** (Nigerian - Igbo)

---

### Step 4: Creative Theme & Task Sequence

**Theme: Fermentation Festival Coordination**

A community center is organizing a 5-day "Living Cultures Festival" celebrating traditional fermentation practices from around the world. The challenge involves coordinating fermentation timelines (which vary from 3 days to 3 weeks) with workshop schedules, ensuring demonstration pieces are ready at the right moment.

**Time Management Problem:**
- Kimchi needs 3-5 days to ferment before the tasting workshop
- Sourdough starter must be fed daily for 7 days before the bread workshop
- Miso demonstration requires showing 3-week-old vs fresh miso side-by-side
- The festival runs Feb 15-19, so fermentation must begin on staggered dates
- Kenji's miso prep blocks Fatima's koji room access until the inoculation is complete

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Query existing teams to check if a fermentation team exists |
| 2 | `teamCreate` | Create "Fermentation Guild" team for the festival |
| 3 | `users` | Find Kenji, Fatima, Bogdan, and Adaeze to assign tasks |
| 4 | `workflowStateCreate` | Add "Fermenting" state to track items in active fermentation |
| 5 | `issueLabelCreate` | Create "time-critical" label for deadline-sensitive tasks |
| 6 | `issueCreate` | Create task: "Prepare Kenji's 3-week miso base" (must start Jan 25) |
| 7 | `issueCreate` | Create task: "Inoculate koji spores for Fatima's amazake" (blocks miso) |
| 8 | `issueRelationCreate` | Set koji inoculation as blocking miso prep (shared koji room) |
| 9 | `issueUpdate` | Assign the miso task to Kenji with due date and "time-critical" label |
| 10 | `commentCreate` | Add fermentation monitoring note with keyword "CULTURE_READY_CHECK" |

---

### Generated Prompt

```
The community center is hosting the "Living Cultures Festival" from Feb 15-19. Create a new team called "Fermentation Guild" to coordinate this event. We need to track fermentation timelines carefully.

First, add a new workflow state called "Fermenting" (color: #8B4513, type: started) to the new team - this will help us track items that are actively culturing.

Create a label called "time-critical" for tasks with strict biological deadlines.

Now for the tricky scheduling: Kenji needs to start his 3-week miso base by January 25th at the latest for it to be ready for the festival tasting on Feb 18th. Create an issue titled "Prepare Kenji miso base for Feb 18 tasting" and assign it to Kenji with the time-critical label.

However, Fatima needs access to the koji room first to inoculate spores for her amazake demonstration. Create another issue "Inoculate koji spores for amazake - Fatima" and set it up so that it blocks Kenji's miso preparation (they share the temperature-controlled koji room and can't run both processes simultaneously).

Finally, add a comment to the miso task that says: "CULTURE_READY_CHECK: Verify koji colonization complete before rice inoculation. Target temp 86F for 48hrs."
```

---

### Verifiable Keywords/Assertions

1. **Team creation**: Team named "Fermentation Guild" exists
2. **Workflow state**: State "Fermenting" with color "#8B4513" in the new team
3. **Label**: "time-critical" label exists
4. **Issue 1**: Title contains "miso base" and "Feb 18", assigned to Kenji
5. **Issue 2**: Title contains "koji spores" and "Fatima"
6. **Relation**: Blocking relationship exists between the two issues
7. **Comment**: Body contains "CULTURE_READY_CHECK" and "86F"

### Metadata
```json
{
  "min_tool_calls": 10,
  "tools_required": [
    "teams",
    "teamCreate",
    "users",
    "workflowStateCreate",
    "issueLabelCreate",
    "issueCreate",
    "issueRelationCreate",
    "issueUpdate",
    "commentCreate"
  ]
}
```

---

## Test Generation #2

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 9**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `issues`
3. `users`
4. `issueLabels`
5. `issueLabelCreate`
6. `workflowStates`
7. `issueUpdate`
8. `issueUpdate` (duplicate)
9. `commentCreate`

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 3**

**Names from different cultural traditions:**
1. **Yuto** (Japanese)
2. **Nneka** (Nigerian - Igbo)
3. **Szymon** (Polish)

---

### Step 4: Creative Theme & Task Sequence

**Theme: Community Seed Library Germination Audit**

A neighborhood seed library tracks donated seed packets as issues. Each packet has a title like "Tomato - Brandywine (Yuto)" indicating variety and donor. Packets are marked with priority (1=rare heirloom, 4=common). The library needs to calculate germination success rates and apply recognition or remediation based on conditional logic.

**Math Calculation:**
- Germination rate = (packets in "Sprouted" state) / (packets in "Sprouted" + "Failed" states) × 100
- Round to nearest integer percentage

**Conditional Logic Turns:**
1. **Yuto's evaluation**: Count his packets. If germination rate ≥ 75% AND he has at least 2 varieties in "Sprouted" state → create "Seed Guardian" label and apply to ALL his packets (even failed ones, as recognition of contribution)

2. **Nneka's exception**: She has exactly one packet, and it's priority 1 (rare heirloom). REGARDLESS of its current state, move it to "Preserved Collection" status. Rare genetics must be saved even if germination failed—the library will attempt tissue culture.

3. **Szymon's remediation**: Calculate his rate. If rate < 60% → move his non-sprouted packets to "Needs Donor Review" status AND add a comment with the exact calculation: "GERMINATION_AUDIT: X sprouted / Y total = Z% - below 60% threshold"

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the "Seed Library" team |
| 2 | `issues` | Query all seed packet issues to analyze by donor |
| 3 | `users` | Look up Yuto, Nneka, Szymon by name to get their IDs |
| 4 | `issueLabels` | Check existing labels before creating new one |
| 5 | `workflowStates` | Get "Sprouted", "Failed", "Preserved Collection", "Needs Donor Review" state IDs |
| 6 | `issueLabelCreate` | Create "Seed Guardian" label for high performers |
| 7 | `issueUpdate` | Apply label to Yuto's packets; move Nneka's to Preserved |
| 8 | `issueUpdate` | Move Szymon's failing packets to review status |
| 9 | `commentCreate` | Add calculation comment to Szymon's packet |

---

### Generated Prompt

```
The Seed Library team is conducting its quarterly germination audit. We need to evaluate each donor's success rate and take appropriate action.

First, calculate Yuto's germination rate: count how many of his seed packets are in "Sprouted" status versus "Failed" status, then compute (sprouted / total) × 100. If his rate is 75% or higher AND he has at least 2 different varieties that sprouted, create a new label called "Seed Guardian" and apply it to all of his packets as recognition.

Next, handle Nneka's special case: she donated exactly one packet and it's marked as priority 1 (rare heirloom). Regardless of whether it sprouted or failed, move this packet to "Preserved Collection" status—the library will attempt tissue culture propagation on rare genetics.

Finally, evaluate Szymon's packets the same way. If his germination rate is below 60%, move all his non-sprouted packets to "Needs Donor Review" status and add a comment to each one that reads: "GERMINATION_AUDIT: X sprouted / Y total = Z% - below 60% threshold" where X, Y, Z are the actual calculated values.
```

---

### Verifiable Keywords/Assertions

1. **Label creation**: Label "Seed Guardian" exists (conditional on Yuto meeting criteria)
2. **Yuto's packets**: If rate ≥ 75% with 2+ varieties, all his packets have "Seed Guardian" label
3. **Nneka's packet**: Priority 1 packet moved to "Preserved Collection" regardless of prior state
4. **Szymon's packets**: If rate < 60%, non-sprouted packets in "Needs Donor Review" status
5. **Comment**: Body contains "GERMINATION_AUDIT:" and "below 60% threshold" with numeric values

### Key Conditional Logic Points

- **Unexpected turn 1**: Yuto's label applies to ALL packets including failed ones (recognition, not just success marking)
- **Unexpected turn 2**: Nneka's priority-based exception overrides normal germination logic entirely
- **Math verification**: The comment must contain the exact calculation, making it verifiable

### Metadata
```json
{
  "min_tool_calls": 9,
  "tools_required": [
    "teams",
    "issues",
    "users",
    "issueLabels",
    "workflowStates",
    "issueLabelCreate",
    "issueUpdate",
    "commentCreate"
  ]
}
```

---

## Test Generation #3

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 11**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `teamCreate`
3. `users`
4. `issueCreate`
5. `issueCreate` (duplicate)
6. `issueCreate` (duplicate)
7. `issueLabels`
8. `issueLabelCreate`
9. `issueUpdate`
10. `commentCreate`
11. `issueRelationCreate`

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 5**

**Names from different cultural traditions:**
1. **Haruki** (Japanese)
2. **Amara** (Nigerian - Yoruba)
3. **Dmitri** (Russian)
4. **Priya** (Indian)
5. **Elif** (Turkish)

---

### Step 4: Creative Theme & Task Sequence

**Theme: Amateur Mycology Club - Mushroom Foraging Expeditions**

A community mycology club tracks foraging expeditions and specimen findings. Each expedition becomes an issue, and notable specimens found during expeditions are logged as separate linked issues. The club needs to organize an upcoming foray into the Coastal Redwood Reserve.

**Scenario:**
The "Forest Mycology Collective" is planning their autumn expedition. Haruki is leading the main expedition. During planning, they need to create specimen tracking issues for anticipated finds, link dependencies between specimens that require cross-referencing for identification, and coordinate volunteer assignments.

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Check if "Forest Mycology Collective" team already exists |
| 2 | `teamCreate` | Create the mycology club team |
| 3 | `users` | Find Haruki, Amara, Dmitri, Priya, Elif to assign roles |
| 4 | `issueLabels` | Check what labels exist before creating new ones |
| 5 | `issueLabelCreate` | Create "awaiting-spore-print" label for specimens needing analysis |
| 6 | `issueCreate` | Create main expedition: "Coastal Redwood Reserve Autumn Foray" |
| 7 | `issueCreate` | Create specimen issue: "Specimen #1: Cantharellus formosus cluster - Sector 7" |
| 8 | `issueCreate` | Create specimen issue: "Specimen #2: Unknown Amanita - requires cross-reference" |
| 9 | `issueUpdate` | Assign expedition to Haruki, specimens to Priya and Dmitri |
| 10 | `issueRelationCreate` | Link Amanita specimen as blocked by Cantharellus (need spore comparison) |
| 11 | `commentCreate` | Add field notes: "FIELD_NOTE_REF: GPS coordinates 41.2132°N, found near fallen Douglas fir" |

---

### Generated Prompt

```
The Forest Mycology Collective is organizing their autumn foraging expedition. First, create a new team called "Forest Mycology Collective" to track all club activities.

Create a label called "awaiting-spore-print" for specimens that need laboratory analysis before identification can be confirmed.

Now set up the expedition: create an issue titled "Coastal Redwood Reserve Autumn Foray" and assign it to Haruki as the expedition leader.

During the planning phase, we're pre-logging anticipated specimen finds based on last year's survey. Create a specimen issue titled "Specimen #1: Cantharellus formosus cluster - Sector 7" and assign it to Priya for documentation. Create another specimen issue "Specimen #2: Unknown Amanita - requires cross-reference" and assign it to Dmitri, applying the "awaiting-spore-print" label.

The Amanita identification depends on comparing its spore print against the Cantharellus specimen first (they were found in the same microhabitat and we need to rule out look-alikes). Set up the Amanita issue as blocked by the Cantharellus issue.

Finally, add a field note comment to the Cantharellus specimen that reads: "FIELD_NOTE_REF: GPS coordinates 41.2132°N, found near fallen Douglas fir. Fruiting body golden-yellow, false gills present, apricot aroma confirmed."
```

---

### Verifiable Keywords/Assertions

1. **Team creation**: Team named "Forest Mycology Collective" exists
2. **Label creation**: Label "awaiting-spore-print" exists
3. **Expedition issue**: Title contains "Coastal Redwood Reserve" and "Foray", assigned to Haruki
4. **Specimen #1**: Title contains "Cantharellus formosus" and "Sector 7", assigned to Priya
5. **Specimen #2**: Title contains "Amanita" and "cross-reference", assigned to Dmitri, has "awaiting-spore-print" label
6. **Relation**: Blocking relationship exists (Cantharellus blocks Amanita)
7. **Comment**: Body contains "FIELD_NOTE_REF:" and "41.2132°N" and "Douglas fir"

### Metadata
```json
{
  "min_tool_calls": 11,
  "tools_required": [
    "teams",
    "teamCreate",
    "users",
    "issueLabels",
    "issueLabelCreate",
    "issueCreate",
    "issueUpdate",
    "issueRelationCreate",
    "commentCreate"
  ]
}
```

---

## Test Generation #4

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 8**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `users`
3. `issueCreate`
4. `issueCreate` (duplicate)
5. `issueUpdate`
6. `issueLabels`
7. `workflowStates`
8. `commentCreate`

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 3**

**Names from different cultural traditions:**
1. **Marcus** (Latin/Roman)
2. **Aisha** (Arabic/Swahili)
3. **Wei** (Chinese)

---

### Step 4: Theme & Task Sequence

**Theme: Mobile App Release Preparation**

A software development team is preparing for their mobile app's next release. They need to track and resolve critical bugs reported by QA before the release can proceed. This is a straightforward sprint-end scenario typical for any engineering team using Linear.

**Scenario:**
The Mobile team has received bug reports from QA testing. The team lead needs to create tickets for the reported issues, assign them to developers, apply appropriate labels, and track progress through workflow states.

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the "Mobile" team to create issues in |
| 2 | `users` | Look up Marcus, Aisha, and Wei to assign bugs |
| 3 | `issueLabels` | Check for existing "QA-reported" label |
| 4 | `workflowStates` | Get the "In Progress" state ID for status updates |
| 5 | `issueCreate` | Create bug ticket: "App crashes on login with special characters" |
| 6 | `issueCreate` | Create bug ticket: "Push notifications not working on Android 14" |
| 7 | `issueUpdate` | Assign bugs to developers and set to "In Progress" |
| 8 | `commentCreate` | Add reproduction steps comment with keyword "REPRO_STEPS" |

---

### Generated Prompt

```
The Mobile team is preparing for the v2.5 release and QA has reported some critical bugs that need to be tracked.

First, create a new issue titled "App crashes on login with special characters" in the Mobile team. This is a high priority bug. Assign it to Marcus.

Create another issue titled "Push notifications not working on Android 14" in the same team and assign it to Aisha.

Move both issues to "In Progress" status since the developers are starting work on them immediately.

Finally, add a comment to the login crash issue with the following reproduction steps: "REPRO_STEPS: 1. Open app 2. Enter username with & or % character 3. Tap login button 4. App crashes to home screen. Tested on iOS 17.2 and Android 14."
```

---

### Verifiable Keywords/Assertions

1. **Issue 1**: Title contains "crashes on login" and "special characters", assigned to Marcus
2. **Issue 2**: Title contains "Push notifications" and "Android 14", assigned to Aisha
3. **Status**: Both issues are in "In Progress" state
4. **Comment**: Body contains "REPRO_STEPS:" and "iOS 17.2" and "Android 14"

### Metadata
```json
{
  "min_tool_calls": 8,
  "tools_required": [
    "teams",
    "users",
    "issueLabels",
    "workflowStates",
    "issueCreate",
    "issueUpdate",
    "commentCreate"
  ]
}
```

---

## Test Generation #5

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 9**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `users`
3. `issueCreate`
4. `issueUpdate`
5. `issueUpdate` (duplicate)
6. `commentCreate`
7. `commentUpdate`
8. `issueLabels`
9. `issueLabelCreate`

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 4**

**Names from different cultural traditions:**
1. **Kofi** (Ghanaian - Akan)
2. **Elena** (Greek/Spanish)
3. **Tariq** (Arabic)
4. **Ingrid** (Scandinavian/Norwegian)

---

### Step 4: Theme & Task Sequence

**Theme: IT Support Ticket Workflow**

A standard IT helpdesk scenario. The creative aspect is the **chain of dependent actions** where each step builds on and modifies the results of previous steps.

**Creative Action Sequence:**
The prompt requires the agent to:
1. Create something, then immediately modify it
2. Add a comment, then update that same comment with appended information
3. Look up existing data to inform what to create next
4. Perform multiple sequential updates to the same entity

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the IT Support team |
| 2 | `users` | Look up Kofi, Elena, Tariq, Ingrid for assignment |
| 3 | `issueLabels` | Check if "hardware-failure" label already exists |
| 4 | `issueLabelCreate` | Create "hardware-failure" label since it doesn't exist |
| 5 | `issueCreate` | Create support ticket for server outage |
| 6 | `issueUpdate` | Apply the newly created label AND assign to Kofi |
| 7 | `commentCreate` | Add initial diagnostic comment with tracking code |
| 8 | `commentUpdate` | Append resolution notes to the same comment |
| 9 | `issueUpdate` | Mark ticket resolved and reassign to Elena for verification |

---

### Generated Prompt

```
The IT Support team received a critical server outage report. Here's the workflow to execute:

First, check if a label called "hardware-failure" exists. If it doesn't, create it.

Create a new issue titled "Server rack B7 unresponsive - power supply failure" in the IT Support team.

Apply the "hardware-failure" label to this ticket and assign it to Kofi for initial triage.

Add a comment to the ticket with this diagnostic entry: "DIAG_LOG_001: Initial ping test failed. Checked physical connections. PSU indicator light is off. Replacement unit requested from inventory."

Now update that same comment to append the following resolution note at the end: " || UPDATE: PSU replaced at 14:32. Server responding. Monitoring for 24hrs."

Finally, update the ticket to change the assignee from Kofi to Elena for post-incident verification, and move the ticket to "In Review" status.
```

---

### Verifiable Keywords/Assertions

1. **Label**: "hardware-failure" label exists
2. **Issue**: Title contains "Server rack B7" and "power supply failure"
3. **Issue assignment history**: Initially assigned to Kofi, then reassigned to Elena
4. **Issue status**: Ends in "In Review" state
5. **Comment**: Body contains "DIAG_LOG_001:" AND "|| UPDATE:" AND "PSU replaced at 14:32"
6. **Label applied**: Issue has "hardware-failure" label

### Creative Action Highlights

- **Create-then-modify pattern**: Label is created, then immediately used on an issue
- **Comment append pattern**: Same comment is created then updated (not a new comment)
- **Multi-field update**: Single issueUpdate changes both assignee AND status
- **Sequential dependency**: Each action depends on the result of previous actions

### Metadata
```json
{
  "min_tool_calls": 9,
  "tools_required": [
    "teams",
    "users",
    "issueLabels",
    "issueLabelCreate",
    "issueCreate",
    "issueUpdate",
    "commentCreate",
    "commentUpdate"
  ]
}
```

---

## Test Generation #6

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 10**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `issues`
3. `users`
4. `issueCreate`
5. `issueCreate` (duplicate)
6. `issueUpdate`
7. `issueUpdate` (duplicate)
8. `issueRelationCreate`
9. `commentCreate`
10. `commentDelete`

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 2**

**Names from different cultural traditions:**
1. **Olga** (Russian/Slavic)
2. **Jamal** (Arabic)

---

### Step 4: Theme & Task Sequence

**Theme: Sprint Backlog Cleanup**

A routine sprint planning session where the team reorganizes work items. The creative aspect is the **mistake-and-correction pattern** and **cross-referencing between issues**.

**Creative Action Sequence:**
The prompt requires the agent to:
1. Look up existing issues to find specific ones by description
2. Create a parent issue and a child sub-task
3. Set up a blocking dependency between unrelated issues
4. Add a comment to the wrong issue, then delete it
5. Perform corrective updates after the deletion

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the Backend team |
| 2 | `issues` | Query existing issues to find the "database migration" ticket |
| 3 | `users` | Look up Olga and Jamal for assignment |
| 4 | `issueCreate` | Create parent epic: "Q1 Infrastructure Overhaul" |
| 5 | `issueCreate` | Create sub-task: "Upgrade Redis cluster" with parent set |
| 6 | `issueRelationCreate` | Set Redis upgrade as blocked by the database migration issue |
| 7 | `commentCreate` | Add standup note to Redis issue (intentional mistake setup) |
| 8 | `commentDelete` | Delete the comment - it was added to wrong ticket |
| 9 | `issueUpdate` | Assign the Redis sub-task to Jamal |
| 10 | `issueUpdate` | Assign the parent epic to Olga and set priority to High |

---

### Generated Prompt

```
The Backend team is doing sprint cleanup. Here's what needs to happen:

First, find the existing issue about "database migration" - we'll need its ID for a dependency.

Create a new parent issue titled "Q1 Infrastructure Overhaul" in the Backend team. This will be our tracking epic.

Create a sub-issue under that epic titled "Upgrade Redis cluster to v7" - make sure to set the parent relationship to the epic you just created.

The Redis upgrade cannot start until the database migration is complete. Set up the Redis issue as blocked by the database migration issue.

Now, add a standup note comment to the Redis issue that says: "STANDUP_NOTE: Jamal will start this after migration completes. ETA next Tuesday."

Wait - that comment was supposed to go on the migration ticket, not the Redis ticket. Delete that comment.

Finally, assign the Redis sub-task to Jamal, and assign the parent epic "Q1 Infrastructure Overhaul" to Olga with High priority.
```

---

### Verifiable Keywords/Assertions

1. **Parent issue**: Title "Q1 Infrastructure Overhaul" exists in Backend team
2. **Sub-issue**: Title contains "Redis cluster" and "v7", has parent set to the epic
3. **Blocking relation**: Redis issue is blocked by database migration issue
4. **Comment deleted**: No comment containing "STANDUP_NOTE:" exists on Redis issue
5. **Assignments**: Redis assigned to Jamal, Epic assigned to Olga
6. **Priority**: Epic has High priority

### Creative Action Highlights

- **Mistake-correction pattern**: Comment is created then immediately deleted (simulates real user behavior)
- **Parent-child creation**: Two issues created with hierarchical relationship
- **Cross-issue dependency**: Blocking relationship references an existing issue found via query
- **Multi-entity updates**: Both new issues get updated with assignments

### Metadata
```json
{
  "min_tool_calls": 10,
  "tools_required": [
    "teams",
    "issues",
    "users",
    "issueCreate",
    "issueRelationCreate",
    "commentCreate",
    "commentDelete",
    "issueUpdate"
  ]
}
```

---

## Test Generation #7

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 12**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `users`
3. `workflowStates`
4. `workflowStateCreate`
5. `issueCreate`
6. `issueCreate` (duplicate)
7. `issueCreate` (duplicate)
8. `issueUpdate`
9. `issueUpdate` (duplicate)
10. `issueRelationCreate`
11. `issueRelationCreate` (duplicate)
12. `commentCreate`

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 5**

**Names from different cultural traditions:**
1. **Yuki** (Japanese)
2. **Kwame** (Ghanaian - Akan)
3. **Svetlana** (Russian)
4. **Rashid** (Arabic)
5. **Marisol** (Spanish/Latin American)

---

### Step 4: Theme & Task Sequence

**Theme: Product Launch Coordination**

A software company is coordinating a product launch scheduled for April 1st. Multiple workstreams have interdependent timing constraints that create a critical path.

**Time Management Problem:**

The launch has cascading dependencies with specific lead times:
- **Legal review** requires 5 business days and cannot begin until product documentation is finalized
- **Marketing materials** cannot be published until legal review completes
- **Support training** must complete at least 3 days before launch
- **Press embargo** lifts exactly 24 hours before launch (March 31st 9am)
- **Feature freeze** on March 20th triggers the documentation phase

The critical path is: Feature Freeze → Documentation → Legal Review → Marketing Ready → Launch

If documentation slips by even 2 days, legal review won't complete in time, which cascades to block marketing.

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the Launch Coordination team |
| 2 | `users` | Look up Yuki, Kwame, Svetlana, Rashid, Marisol |
| 3 | `workflowStates` | Get existing states to check for "Blocked" state |
| 4 | `workflowStateCreate` | Create "Awaiting Dependency" state for time-blocked items |
| 5 | `issueCreate` | Create "Complete product documentation" (due March 22) |
| 6 | `issueCreate` | Create "Legal review of launch materials" (due March 29) |
| 7 | `issueCreate` | Create "Publish marketing campaign" (due March 31) |
| 8 | `issueRelationCreate` | Documentation blocks Legal Review |
| 9 | `issueRelationCreate` | Legal Review blocks Marketing |
| 10 | `issueUpdate` | Assign documentation to Yuki, set due date March 22 |
| 11 | `issueUpdate` | Assign legal review to Svetlana, marketing to Kwame |
| 12 | `commentCreate` | Add timeline note with critical path calculation |

---

### Generated Prompt

```
The Launch Coordination team is preparing for the April 1st product release. We need to set up the critical path with proper dependencies and timing.

First, create a new workflow state called "Awaiting Dependency" (color: #FFA500, type: started) - we'll use this for tasks that are time-blocked by predecessors.

Create three issues in the Launch Coordination team:

1. "Complete product documentation for v3.0 launch" - This is the first domino. Yuki owns this. Due date must be March 22nd because legal needs 5 business days after this completes.

2. "Legal review of launch materials" - Svetlana from Legal owns this. Due date is March 29th. This CANNOT start until documentation is complete - set up the blocking relationship.

3. "Publish marketing campaign assets" - Kwame owns this. Due date is March 31st (press embargo lifts at 9am that day). This is blocked by legal review completion.

Set up the dependency chain: Documentation blocks Legal Review, and Legal Review blocks Marketing.

Finally, add a comment to the documentation issue that explains the timeline pressure: "CRITICAL_PATH_NOTE: This task has ZERO slack. If documentation slips past March 22nd, legal review (5 business days) won't complete by March 29th, which blocks marketing from the March 31st embargo lift. Launch date is immovable."
```

---

### Verifiable Keywords/Assertions

1. **Workflow state**: "Awaiting Dependency" state exists with color "#FFA500"
2. **Issue 1**: Title contains "product documentation" and "v3.0", assigned to Yuki, due March 22
3. **Issue 2**: Title contains "Legal review", assigned to Svetlana, due March 29
4. **Issue 3**: Title contains "marketing campaign", assigned to Kwame, due March 31
5. **Relation 1**: Documentation blocks Legal Review
6. **Relation 2**: Legal Review blocks Marketing
7. **Comment**: Body contains "CRITICAL_PATH_NOTE:" and "ZERO slack" and "March 22nd"

### Time Management Complexity

- **Cascading deadlines**: Each task's due date is calculated from downstream dependencies
- **Fixed external constraint**: April 1st launch and March 31st embargo are immovable
- **Lead time calculation**: 5 business days for legal review creates the March 22nd deadline
- **Zero slack critical path**: Any delay propagates through the entire chain

### Metadata
```json
{
  "min_tool_calls": 12,
  "tools_required": [
    "teams",
    "users",
    "workflowStates",
    "workflowStateCreate",
    "issueCreate",
    "issueRelationCreate",
    "issueUpdate",
    "commentCreate"
  ]
}
```

---

## Test Generation #8

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 11**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `issues`
3. `users`
4. `issueCreate`
5. `issueCreate` (duplicate)
6. `issueCreate` (duplicate)
7. `issueUpdate`
8. `issueUpdate` (duplicate)
9. `issueRelationCreate`
10. `issueRelationCreate` (duplicate)
11. `commentCreate`

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 3**

**Names from different cultural traditions:**
1. **Nadia** (Slavic/Arabic)
2. **Tomás** (Spanish/Portuguese)
3. **Chioma** (Nigerian - Igbo)

---

### Step 4: Theme & Task Sequence

**Theme: Research Grant Application Pipeline**

A university research team is setting up their grant application workflow. The pipeline has strict sequential dependencies mandated by the funding agency.

**Dependency Chain (as requested in prompt):**
```
IRB Ethics Approval → Data Collection Protocol → Pilot Study Design → Grant Submission Draft
```

**HIDDEN CONFLICT (in seed data, NOT mentioned in prompt):**

The seed will contain a pre-existing issue relation where **"Grant Submission Draft" blocks "IRB Ethics Approval"**. This was incorrectly entered by a previous team member who misunderstood the workflow direction.

When the agent attempts to set up the forward dependency chain (Ethics → ... → Grant), they will create a **circular dependency**:
```
Ethics → Data → Pilot → Grant → Ethics (CYCLE!)
```

A capable agent should:
1. Discover this conflict when querying existing relations or when the relation creation fails/warns
2. Leave a comment flagging the circular dependency issue
3. Potentially suggest removing the incorrect relation

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the Research team |
| 2 | `issues` | Query existing issues to find "IRB Ethics Approval" and check current state |
| 3 | `users` | Look up Nadia, Tomás, Chioma for assignment |
| 4 | `issueCreate` | Create "Data Collection Protocol" issue |
| 5 | `issueCreate` | Create "Pilot Study Design" issue |
| 6 | `issueCreate` | Create "Grant Submission Draft" issue |
| 7 | `issueRelationCreate` | Set Ethics Approval → blocks Data Collection |
| 8 | `issueRelationCreate` | Set Data Collection → blocks Pilot Study |
| 9 | `issueUpdate` | Assign issues to team members |
| 10 | `issueUpdate` | Set due dates based on submission deadline |
| 11 | `commentCreate` | Add pipeline overview OR flag dependency conflict |

---

### Generated Prompt

```
The Research team needs to set up the grant application pipeline for the upcoming NIH submission deadline (June 15th).

First, find the existing "IRB Ethics Approval" issue - this is our starting point and is already in progress.

Create three new issues in the Research team to complete the pipeline:

1. "Data Collection Protocol v2" - Nadia will own this. It cannot begin until ethics approval is complete.

2. "Pilot Study Design - 50 participant cohort" - Tomás will lead this. It depends on having the data collection protocol finalized.

3. "Grant Submission Draft - R01 mechanism" - Chioma will compile the final submission. This is the last step and depends on pilot study results.

Set up the blocking relationships to enforce the sequential workflow:
- IRB Ethics Approval blocks Data Collection Protocol
- Data Collection Protocol blocks Pilot Study Design
- Pilot Study Design blocks Grant Submission Draft

After setting up the dependencies, add a comment to the Grant Submission issue summarizing the critical path: "PIPELINE_STATUS: This submission depends on completion chain: Ethics (in progress) → Data Protocol (Nadia) → Pilot Study (Tomás) → This draft. Target: June 15th deadline."
```

---

### Verifiable Keywords/Assertions

**Standard assertions (always true):**
1. **Issue 1**: Title contains "Data Collection Protocol", assigned to Nadia
2. **Issue 2**: Title contains "Pilot Study" and "50 participant", assigned to Tomás
3. **Issue 3**: Title contains "Grant Submission" and "R01", assigned to Chioma
4. **Relations**: At least 2 blocking relationships exist in the forward direction

**Conflict detection assertions (if agent discovers the cycle):**
5. **Comment on conflict**: If agent detects cycle, comment contains "circular" OR "cycle" OR "conflict" OR "dependency issue"
6. **Conflict flagged**: Comment exists on Ethics Approval OR Grant Submission issue mentioning the problematic relation

### Hidden Seed Conflict Details

**Pre-existing relation in seed data:**
```json
{
  "type": "blocks",
  "issueId": "<grant_submission_id>",
  "relatedIssueId": "<ethics_approval_id>"
}
```

This means "Grant Submission blocks Ethics Approval" - the REVERSE of the correct flow. When the agent creates the forward chain, this forms a cycle.

**Expected agent behavior:**
- **Minimum**: Complete the requested setup (may not notice conflict)
- **Better**: Notice something is wrong when relations are created
- **Best**: Explicitly identify the circular dependency and comment about it

### Metadata
```json
{
  "min_tool_calls": 11,
  "tools_required": [
    "teams",
    "issues",
    "users",
    "issueCreate",
    "issueRelationCreate",
    "issueUpdate",
    "commentCreate"
  ],
  "seed_contains_conflict": true,
  "conflict_type": "circular_dependency",
  "conflict_description": "Grant Submission incorrectly blocks Ethics Approval, creating cycle when forward chain is added"
}
```

---

## Test Generation #9

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 10**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `issues`
3. `users`
4. `issueCreate`
5. `issueCreate` (duplicate)
6. `issueRelationCreate`
7. `issueRelationCreate` (duplicate)
8. `issueRelationCreate` (duplicate)
9. `issueUpdate`
10. `commentCreate`

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 4**

**Names from different cultural traditions:**
1. **Kenji** (Japanese)
2. **Amara** (West African - Ethiopian/Amharic)
3. **Dmitri** (Russian)
4. **Paloma** (Spanish)

---

### Step 4: Theme & Task Sequence

**Theme: Film Post-Production Pipeline**

A film production company is managing their post-production workflow in Linear. The scenario involves multiple editing phases with complex interdependencies that form a directed acyclic graph (DAG).

**Dependency Counting Challenge:**

The seed data contains a "Master Edit Lock" issue that blocks EXACTLY 4 other issues. The agent must:
1. Query to find the Master Edit Lock issue
2. Count how many issues are directly blocked by it
3. Create new issues and add them to the dependency chain
4. Report the exact count in a comment (this allows verification)

**Seed Data Structure:**
```
Master Edit Lock (blocks exactly 4 issues):
├── blocks → Color Grading Phase 1
├── blocks → Sound Design Draft
├── blocks → VFX Shot Compositing
└── blocks → Subtitle Localization

Color Grading Phase 1:
└── blocks → Color Grading Phase 2 (pre-existing secondary dependency)
```

This creates a verifiable scenario: the agent MUST correctly count "4" direct blockers to pass.

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the "Post-Production" team |
| 2 | `users` | Look up Kenji, Amara, Dmitri, Paloma for assignments |
| 3 | `issues` | Query to find "Master Edit Lock" and examine its blocking relations |
| 4 | `issueCreate` | Create "Final Color Grade" issue |
| 5 | `issueCreate` | Create "Audio Mix Master" issue |
| 6 | `issueRelationCreate` | Set "Color Grading Phase 1" blocks "Final Color Grade" |
| 7 | `issueRelationCreate` | Set "Sound Design Draft" blocks "Audio Mix Master" |
| 8 | `issueRelationCreate` | Set "Final Color Grade" blocks "Audio Mix Master" (cross-stream dependency) |
| 9 | `issueUpdate` | Assign new issues to Kenji and Amara |
| 10 | `commentCreate` | Add dependency audit comment with the counted value |

---

### Generated Prompt

```
The Post-Production team is managing the editing pipeline for "Project Aurora". Here's what needs to happen:

First, find the "Master Edit Lock" issue - this is the critical gate that must complete before downstream work can proceed.

Count how many issues are directly blocked by "Master Edit Lock" (i.e., issues that have a "blocked by" relationship pointing to Master Edit Lock). You'll need this exact number for your report.

Create two new issues in the Post-Production team:
1. "Final Color Grade - DCI-P3 Mastering" - Kenji will handle this. It cannot start until "Color Grading Phase 1" is complete, so set up that blocking relationship.
2. "Audio Mix Master - Dolby Atmos" - Amara will handle this. It depends on "Sound Design Draft" being finished.

Additionally, the colorist needs to lock the final look before audio can be mixed to picture. Set up "Final Color Grade" as blocking "Audio Mix Master".

After setting up all the new dependencies, add a comment to the "Master Edit Lock" issue with a dependency audit in this exact format:

"DEPENDENCY_AUDIT: Master Edit Lock directly blocks [X] downstream issues. New dependencies added: Final Color Grade (Kenji), Audio Mix Master (Amara). Cross-stream link established between color and audio pipelines."

Replace [X] with the actual count of issues directly blocked by Master Edit Lock.
```

---

### Verifiable Keywords/Assertions

1. **Issue 1**: Title contains "Final Color Grade" and "DCI-P3", assigned to Kenji
2. **Issue 2**: Title contains "Audio Mix Master" and "Dolby Atmos", assigned to Amara
3. **Relation 1**: "Color Grading Phase 1" blocks "Final Color Grade" (new relation)
4. **Relation 2**: "Sound Design Draft" blocks "Audio Mix Master" (new relation)
5. **Relation 3**: "Final Color Grade" blocks "Audio Mix Master" (cross-stream)
6. **Comment contains correct count**: Body contains "directly blocks 4 downstream issues"
7. **Comment format**: Body contains "DEPENDENCY_AUDIT:" AND "Kenji" AND "Amara" AND "Cross-stream"

### Verification Logic

**The critical assertion is #6**: The seed will have exactly 4 issues blocked by Master Edit Lock:
- Color Grading Phase 1
- Sound Design Draft
- VFX Shot Compositing
- Subtitle Localization

If the agent reports any number other than 4, the test fails. This verifies:
- The agent correctly queried the issue relations
- The agent correctly filtered for "blocks" relationship type
- The agent correctly counted the results

### Metadata
```json
{
  "min_tool_calls": 10,
  "tools_required": [
    "teams",
    "issues",
    "users",
    "issueCreate",
    "issueRelationCreate",
    "issueUpdate",
    "commentCreate"
  ],
  "requires_counting": true,
  "counting_target": "issues blocked by Master Edit Lock",
  "expected_count": 4
}
```

---

## Test Generation #10

### Step 1: Sample n (number of endpoints)
**Random selection from range [7-13]: n = 11**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `issues`
3. `users`
4. `issueRelationCreate`
5. `issueRelationDelete`
6. `issueUpdate`
7. `issueUpdate` (duplicate)
8. `commentCreate`
9. `workflowStates`
10. `issueCreate`
11. `issueRelationCreate` (duplicate)

### Step 3: Sample m unique names (m from [1-6])
**Random selection: m = 3**

**Names from different cultural traditions:**
1. **Ximena** (Spanish/Mexican)
2. **Okonkwo** (Nigerian - Igbo)
3. **Søren** (Danish/Scandinavian)

---

### Step 4: Theme & Task Sequence

**Theme: Archaeological Dig Site Coordination**

An archaeological research team is managing their excavation workflow in Linear. The dig has strict procedural dependencies mandated by preservation protocols.

**Conflicting Dependency Challenge:**

The seed data contains a **mutual blocking conflict** (deadlock) between two issues:
- "Artifact Photography Documentation" blocks "Lab Sample Analysis" ✓ (correct - need in-situ photos before extraction)
- "Lab Sample Analysis" blocks "Artifact Photography Documentation" ✗ (incorrect - added by mistake)

This creates a deadlock where neither task can proceed. The agent must:
1. Query issues and discover the mutual block
2. Identify which relation is incorrect based on domain logic
3. Delete the erroneous relation
4. Set up additional workflow dependencies
5. Document the fix

**Seed Data Structure:**
```
Artifact Photography Documentation ←→ Lab Sample Analysis (MUTUAL BLOCK - deadlock!)
     ↑                                      ↑
     └── both are stuck, neither can start ─┘

Site Grid Mapping (independent, in progress)
Stratigraphy Recording (independent, completed)
```

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the "Archaeology" team |
| 2 | `issues` | Query issues to find the conflicting pair and examine their relations |
| 3 | `users` | Look up Ximena, Okonkwo, Søren for assignments |
| 4 | `workflowStates` | Get states to update blocked issues |
| 5 | `issueRelationDelete` | Remove the incorrect "Lab blocks Photography" relation |
| 6 | `issueCreate` | Create "Final Site Report Compilation" issue |
| 7 | `issueRelationCreate` | Set Photography blocks new Report issue |
| 8 | `issueRelationCreate` | Set Lab Analysis blocks new Report issue |
| 9 | `issueUpdate` | Move unblocked Photography to "In Progress", assign to Ximena |
| 10 | `issueUpdate` | Assign Lab Analysis to Okonkwo, Report to Søren |
| 11 | `commentCreate` | Document the conflict resolution with audit trail |

---

### Generated Prompt

```
The Archaeology team is managing the Season 3 excavation at Site Karnak-West. There's a workflow problem blocking progress.

Examine the issues "Artifact Photography Documentation" and "Lab Sample Analysis". These two issues are in a dependency deadlock - each one is marked as blocking the other, which means neither can proceed.

Determine which blocking relationship is incorrect. The correct archaeological workflow is: Photography must complete BEFORE samples can go to the lab (you need photos of artifacts in situ before extraction for the record). The reverse relationship (lab blocking photography) was added by mistake and makes no sense.

Delete the incorrect blocking relationship to resolve the deadlock.

Now extend the workflow. Create a new issue called "Final Site Report Compilation - Season 3" in the Archaeology team. This report cannot be written until BOTH the photography documentation AND the lab analysis are complete. Set up both as blockers for the report.

Assign the work: Ximena handles photography, Okonkwo handles lab analysis, and Søren compiles the final report.

Move the photography issue to "In Progress" now that it's unblocked.

After fixing everything, add a comment to the "Lab Sample Analysis" issue documenting the fix: "WORKFLOW_FIX: Removed erroneous blocking relation where Lab was blocking Photography. Correct flow is Photography → Lab (need in-situ photos before extraction). Deadlock resolved. Current chain: Photography → Lab Analysis → Final Report."
```

---

### Verifiable Keywords/Assertions

1. **Relation deleted**: The "Lab Sample Analysis blocks Artifact Photography Documentation" relation no longer exists
2. **Correct relation preserved**: "Artifact Photography Documentation blocks Lab Sample Analysis" still exists
3. **New issue**: Title contains "Final Site Report" and "Season 3"
4. **New relation 1**: Photography Documentation blocks Final Report
5. **New relation 2**: Lab Sample Analysis blocks Final Report
6. **Photography status**: "Artifact Photography Documentation" is in "In Progress" state
7. **Assignments**: Photography → Ximena, Lab Analysis → Okonkwo, Report → Søren
8. **Comment**: Body contains "WORKFLOW_FIX:" AND "Deadlock resolved" AND "Photography → Lab"

### Conflict Resolution Verification

**Critical assertions are #1 and #2**:
- The seed contains TWO relations creating a mutual block (A blocks B, B blocks A)
- The agent must delete ONLY the incorrect one (Lab → Photography)
- The agent must preserve the correct one (Photography → Lab)

**Failure modes:**
- Deletes both relations → fails assertion #2
- Deletes wrong relation → fails both #1 and #2
- Deletes nothing → fails assertion #1
- Creates new relations without deleting → issues remain deadlocked

### Seed Data Requirements

```json
{
  "issues": [
    {"title": "Artifact Photography Documentation", "state": "Blocked"},
    {"title": "Lab Sample Analysis", "state": "Blocked"},
    {"title": "Site Grid Mapping", "state": "In Progress"},
    {"title": "Stratigraphy Recording", "state": "Done"}
  ],
  "issue_relations": [
    {"type": "blocks", "issue": "Artifact Photography Documentation", "relatedIssue": "Lab Sample Analysis"},
    {"type": "blocks", "issue": "Lab Sample Analysis", "relatedIssue": "Artifact Photography Documentation"}
  ]
}
```

### Metadata
```json
{
  "min_tool_calls": 11,
  "tools_required": [
    "teams",
    "issues",
    "users",
    "workflowStates",
    "issueRelationDelete",
    "issueCreate",
    "issueRelationCreate",
    "issueUpdate",
    "commentCreate"
  ],
  "requires_conflict_resolution": true,
  "conflict_type": "mutual_blocking_deadlock",
  "relation_to_delete": "Lab Sample Analysis blocks Artifact Photography Documentation",
  "relation_to_preserve": "Artifact Photography Documentation blocks Lab Sample Analysis"
}
```

---

## Test Generation #11

**New Generation Pattern:**
1. Randomly sample n from range [3-7]
2. Sample with replacement n endpoints from Linear
3. Sample m from range [0-3] unique names from different cultural traditions
4. Create a creative, non-corporate scenario using original themes

### Step 1: Sample n (number of endpoints)
**Random selection from range [3-7]: n = 5**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `issueLabels`
3. `issueCreate`
4. `issueUpdate`
5. `commentCreate`

### Step 3: Sample m unique names (m from [0-3])
**Random selection: m = 2**

**Names from different cultural traditions:**
1. **Priya** (Indian)
2. **Bogdan** (Ukrainian)

---

### Step 4: Theme & Task Sequence

**Theme: Amateur Astronomy Club - Celestial Event Planning**

The Stargazers astronomy club tracks their observation sessions, telescope time slots, and celestial events through Linear. Spring brings prime conditions for meteor shower viewing parties.

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the "Stargazers" astronomy club team |
| 2 | `issueLabels` | Check for existing "public-event" label to apply |
| 3 | `issueCreate` | Create observation event for the Lyrid meteor shower peak |
| 4 | `issueUpdate` | Assign Priya as event coordinator and apply the label |
| 5 | `commentCreate` | Add viewing logistics, equipment setup, and photography tips |

---

### Generated Prompt

```
The Stargazers astronomy club needs to set up their spring celestial events schedule.

Create a new issue in the Stargazers team titled "Lyrid Meteor Shower Viewing Party - Peak Night April 22nd" with description "Annual club gathering at Dark Sky Preserve. Expected rate: 18 meteors/hour. Radiant rises after midnight in Perseus."

Assign this event to Priya as the event coordinator.

Apply the "public-event" label to this issue since non-members are welcome to attend.

Add a comment with the viewing logistics: "OBSERVATION_DETAILS: Meet at Ridgeline Observatory parking lot at 10pm. Bring red flashlights only - no white light. Bogdan will set up the 12-inch Dobsonian for Saturn viewing while we wait for the radiant to rise. Best meteor photography settings: ISO 3200, f/2.8, 20-second exposures pointed northeast."
```

---

### Verifiable Keywords/Assertions

1. **Issue**: Title contains "Lyrid Meteor Shower" and "April 22"
2. **Issue description**: Contains "Dark Sky Preserve" and "18 meteors/hour"
3. **Assignment**: Issue assigned to Priya
4. **Label**: Issue has "public-event" label applied
5. **Comment**: Body contains "OBSERVATION_DETAILS:" AND "Ridgeline Observatory" AND "Bogdan" AND "12-inch Dobsonian"

### Metadata
```json
{
  "min_tool_calls": 5,
  "tools_required": [
    "teams",
    "issueLabels",
    "issueCreate",
    "issueUpdate",
    "commentCreate"
  ]
}
```

---

## Test Generation #12

### Step 1: Sample n (number of endpoints)
**Random selection from range [3-7]: n = 6**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `issues`
2. `workflowStates`
3. `issueUpdate`
4. `issueUpdate` (duplicate)
5. `issueLabelCreate`
6. `commentCreate`

### Step 3: Sample m unique names (m from [0-3])
**Random selection: m = 1**

**Names from different cultural traditions:**
1. **Fatou** (Senegalese/West African - Wolof)

---

### Step 4: Theme & Task Sequence

**Theme: Pottery Studio - Kiln Firing Schedule**

A community pottery studio tracks their kiln firing queue through Linear. Each piece in the queue is an issue that moves through workflow states as it progresses from wet clay to finished ceramic.

**Unique Action Pattern:**
- Query-first workflow (find existing issues before modifying)
- Multiple status transitions on different items in same batch
- Label creation without immediate application
- Technical process logging

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `issues` | Find existing pieces: "Fatou's Celadon Vase" and "Stoneware Bowl Set" |
| 2 | `workflowStates` | Get "Firing" and "Cooling" workflow states for the studio |
| 3 | `issueUpdate` | Move "Fatou's Celadon Vase" from "Queued" to "Firing" |
| 4 | `issueUpdate` | Move "Stoneware Bowl Set" from "Firing" to "Cooling" |
| 5 | `issueLabelCreate` | Create "raku-firing" label for special rapid-cool technique |
| 6 | `commentCreate` | Add kiln temperature log entry to the vase issue |

---

### Generated Prompt

```
The Clay & Fire pottery studio tracks their kiln schedule. Help update the firing queue.

First, find the existing issues "Fatou's Celadon Vase" and "Stoneware Bowl Set" in the Ceramics team.

The celadon vase is ready to go in the kiln - move it to "Firing" status.

The stoneware bowls have finished their cone 10 firing and need to cool down - move them to "Cooling" status.

Create a new label called "raku-firing" for pieces that will use the rapid-cooling technique (we'll apply it to future items).

Finally, add a kiln log comment to the celadon vase issue: "KILN_LOG: Loaded into kiln #2 at 9:15am. Target: Cone 9 oxidation (~2300°F). Fatou requested slow cooling for crystal development. Do not open kiln door until temp drops below 400°F."
```

---

### Verifiable Keywords/Assertions

1. **Vase status**: "Fatou's Celadon Vase" is in "Firing" state
2. **Bowls status**: "Stoneware Bowl Set" is in "Cooling" state
3. **Label created**: "raku-firing" label exists
4. **Comment**: Body contains "KILN_LOG:" AND "Cone 9" AND "2300°F" AND "crystal development"

### Seed Data Requirements

```json
{
  "team": {"name": "Ceramics"},
  "workflow_states": [
    {"name": "Queued", "type": "backlog"},
    {"name": "Firing", "type": "started"},
    {"name": "Cooling", "type": "started"},
    {"name": "Complete", "type": "completed"}
  ],
  "issues": [
    {"title": "Fatou's Celadon Vase", "state": "Queued"},
    {"title": "Stoneware Bowl Set", "state": "Firing"}
  ]
}
```

### Metadata
```json
{
  "min_tool_calls": 6,
  "tools_required": [
    "issues",
    "workflowStates",
    "issueUpdate",
    "issueLabelCreate",
    "commentCreate"
  ]
}
```

---

## Test Generation #13

### Step 1: Sample n (number of endpoints)
**Random selection from range [3-7]: n = 7**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `issues`
3. `users`
4. `issueCreate`
5. `issueUpdate`
6. `issueUpdate` (duplicate)
7. `issueUpdate` (duplicate)

### Step 3: Sample m unique names (m from [0-3])
**Random selection: m = 2**

**Names from different cultural traditions:**
1. **Ines** (Portuguese/Spanish)
2. **Rashida** (Swahili/Arabic)

---

### Step 4: Theme & Task Sequence

**Theme: Community Garden Plot Management**

A community garden cooperative tracks their seasonal plot assignments and maintenance tasks through Linear. Spring is plot reassignment season, and several gardeners are swapping plots or taking over abandoned ones.

**Unique Action Pattern:**
- Query-first pattern with heavy update emphasis (3 separate issueUpdates)
- Multiple existing tickets get moved/reassigned
- One new ticket created to track the overall reassignment
- Focus on status changes AND assignee changes across multiple issues

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Find the "Garden Plots" team |
| 2 | `issues` | Query existing plot tickets: "Plot A7 - Tomatoes", "Plot B3 - Herbs", "Plot C1 - Squash" |
| 3 | `users` | Look up Ines and Rashida for reassignments |
| 4 | `issueCreate` | Create "Spring 2025 Plot Reassignment Tracker" to document all changes |
| 5 | `issueUpdate` | Reassign "Plot A7 - Tomatoes" from previous owner to Ines, move to "Active" |
| 6 | `issueUpdate` | Reassign "Plot B3 - Herbs" from Ines to Rashida (plot swap), keep status |
| 7 | `issueUpdate` | Move "Plot C1 - Squash" to "Dormant" status (owner left the co-op) |

---

### Generated Prompt

```
The Garden Plots team manages our community garden cooperative. It's spring reassignment season and we need to shuffle some plots around.

First, find the existing plot issues: "Plot A7 - Tomatoes", "Plot B3 - Herbs", and "Plot C1 - Squash".

Look up gardeners Ines and Rashida - they're involved in this season's reassignments.

Create a new tracking issue titled "Spring 2025 Plot Reassignment Tracker" in the Garden Plots team with description "Documenting all plot changes for the growing season. Reassignments finalized at March board meeting."

Now process the reassignments:

1. Plot A7 (tomatoes) was abandoned when Marcus moved away. Reassign it to Ines and change its status to "Active" since she's starting immediately.

2. Ines and Rashida agreed to swap their herb plots. Reassign "Plot B3 - Herbs" from Ines to Rashida. Keep the current status unchanged.

3. The squash plot (C1) owner has left the cooperative entirely. Move it to "Dormant" status but don't assign anyone yet - we'll offer it at the next meeting.
```

---

### Verifiable Keywords/Assertions

1. **Tracker issue**: Title contains "Spring 2025" and "Plot Reassignment", description contains "March board meeting"
2. **Plot A7**: Assigned to Ines, status is "Active"
3. **Plot B3**: Assigned to Rashida (changed from Ines)
4. **Plot C1**: Status is "Dormant", assignee unchanged or null

### Seed Data Requirements

```json
{
  "team": {"name": "Garden Plots"},
  "workflow_states": [
    {"name": "Dormant", "type": "backlog"},
    {"name": "Planned", "type": "unstarted"},
    {"name": "Active", "type": "started"},
    {"name": "Harvested", "type": "completed"}
  ],
  "users": [
    {"name": "Ines"},
    {"name": "Rashida"},
    {"name": "Marcus"}
  ],
  "issues": [
    {"title": "Plot A7 - Tomatoes", "state": "Dormant", "assignee": "Marcus"},
    {"title": "Plot B3 - Herbs", "state": "Active", "assignee": "Ines"},
    {"title": "Plot C1 - Squash", "state": "Active", "assignee": null}
  ]
}
```

### Unique Sequence Characteristics

- **Triple update pattern**: Three separate issueUpdate calls modifying different tickets
- **Mixed update types**: Combines status changes with assignee changes
- **Swap operation**: Plot B3 demonstrates reassignment from one user to another
- **Null assignment handling**: Plot C1 tests leaving assignee empty while changing status

### Metadata
```json
{
  "min_tool_calls": 7,
  "tools_required": [
    "teams",
    "issues",
    "users",
    "issueCreate",
    "issueUpdate"
  ]
}
```

---

## Test Generation #14

### Step 1: Sample n (number of endpoints)
**Random selection from range [3-7]: n = 6**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `issues`
2. `users`
3. `issueUpdate`
4. `issueUpdate` (duplicate)
5. `issueUpdate` (duplicate)
6. `commentCreate`

### Step 3: Sample m unique names (m from [0-3])
**Random selection: m = 3**

**Names from different cultural traditions:**
1. **Yuto** (Japanese)
2. **Adaeze** (Nigerian - Igbo)
3. **Henrik** (Swedish/Scandinavian)

---

### Step 4: Theme & Task Sequence

**Theme: Board Game Café - Tournament Rescheduling Crisis**

A board game café tracks their tournament schedule through Linear. A venue double-booking forces a cascade of date changes across multiple linked events, plus a last-minute organizer swap.

**Time Management Challenge:**

The Regional Championship was scheduled for **March 15th**, but the venue is now unavailable. Everything must shift by **exactly 8 days** to March 23rd. The cascading timeline constraints are:

```
Registration Deadline: must close 5 days before Qualifying Round
Qualifying Round: must be 7 days before Championship
Regional Championship: March 23rd (rescheduled from March 15th)
```

Working backwards from March 23rd:
- Championship: March 23rd
- Qualifying Round: March 23rd - 7 days = March 16th
- Registration Deadline: March 16th - 5 days = March 11th

Additionally, Yuto (original championship organizer) has a conflict on the new date and must hand off to Adaeze.

**Unique Action Pattern:**
- Pure update-focused workflow (no issue creation)
- Cascading date calculations with explicit constraints
- Combined date change + reassignment in one flow
- Time arithmetic verification through comment

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `issues` | Find tournament tickets: "Regional Championship", "Qualifying Round", "Registration Deadline" |
| 2 | `users` | Look up Yuto, Adaeze, Henrik for the organizer handoff |
| 3 | `issueUpdate` | Update "Regional Championship": new due date March 23rd, reassign from Yuto to Adaeze |
| 4 | `issueUpdate` | Update "Qualifying Round": new due date March 16th (7 days before championship) |
| 5 | `issueUpdate` | Update "Registration Deadline": new due date March 11th (5 days before qualifiers) |
| 6 | `commentCreate` | Add scheduling audit to championship issue with date calculations |

---

### Generated Prompt

```
The Meeple & Brew board game café has a scheduling emergency. The venue for our Catan Regional Championship double-booked us, so we need to reschedule the entire tournament pipeline.

Find the three tournament issues: "Catan Regional Championship - Spring 2025", "Qualifying Round - Top 16 Bracket", and "Tournament Registration Deadline".

The championship was originally March 15th but must move to March 23rd (8-day delay).

Here's the critical part - the dates are interdependent:
- The Qualifying Round must happen exactly 7 days before the Championship
- The Registration Deadline must close exactly 5 days before the Qualifying Round

Calculate and update all three due dates accordingly.

Also, Yuto was organizing the championship but has a work trip conflict on the new date. Reassign the championship to Adaeze. Keep Henrik on the qualifying round.

After updating all dates, add a comment to the championship issue documenting the changes:

"RESCHEDULE_AUDIT: Venue conflict forced 8-day delay. New timeline calculated:
- Registration closes: March 11th (was March 3rd)
- Qualifiers: March 16th (was March 8th)
- Championship: March 23rd (was March 15th)
Organizer handoff: Yuto → Adaeze due to travel conflict."
```

---

### Verifiable Keywords/Assertions

1. **Championship due date**: "Catan Regional Championship" has due date March 23rd (or 2025-03-23)
2. **Championship assignee**: Assigned to Adaeze (changed from Yuto)
3. **Qualifying due date**: "Qualifying Round" has due date March 16th
4. **Registration due date**: "Tournament Registration Deadline" has due date March 11th
5. **Comment**: Body contains "RESCHEDULE_AUDIT:" AND "March 11th" AND "March 16th" AND "March 23rd" AND "Yuto → Adaeze"

### Time Calculation Verification

The agent must perform correct date arithmetic:
- Start with championship: March 23rd
- Qualifiers = Championship - 7 days = March 16th
- Registration = Qualifiers - 5 days = March 11th

**Failure modes:**
- Uses wrong offset (e.g., 8 days for all instead of calculated)
- Calculates from original dates instead of new championship date
- Forgets to update one of the three issues
- Doesn't reassign the championship organizer

### Seed Data Requirements

```json
{
  "team": {"name": "Meeple & Brew Events"},
  "users": [
    {"name": "Yuto"},
    {"name": "Adaeze"},
    {"name": "Henrik"}
  ],
  "issues": [
    {
      "title": "Catan Regional Championship - Spring 2025",
      "dueDate": "2025-03-15",
      "assignee": "Yuto"
    },
    {
      "title": "Qualifying Round - Top 16 Bracket",
      "dueDate": "2025-03-08",
      "assignee": "Henrik"
    },
    {
      "title": "Tournament Registration Deadline",
      "dueDate": "2025-03-03",
      "assignee": "Yuto"
    }
  ]
}
```

### Unique Sequence Characteristics

- **No issue creation**: Pure update workflow operating on existing tickets
- **Cascading date dependencies**: Each date is calculated relative to others
- **Combined field updates**: Due date + assignee changed together on championship
- **Arithmetic verification**: Comment must contain correctly calculated dates
- **Backwards calculation**: Agent must work from championship date backwards

### Metadata
```json
{
  "min_tool_calls": 6,
  "tools_required": [
    "issues",
    "users",
    "issueUpdate",
    "commentCreate"
  ],
  "requires_date_arithmetic": true,
  "date_constraints": {
    "championship": "2025-03-23",
    "qualifying": "championship - 7 days",
    "registration": "qualifying - 5 days"
  }
}
```

---

## Test Generation #15

### Step 1: Sample n (number of endpoints)
**Random selection from range [3-7]: n = 7**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `teams`
2. `issues`
3. `issueUpdate`
4. `issueCreate`
5. `issueCreate` (duplicate)
6. `issueCreate` (duplicate)
7. `commentCreate`

### Step 3: Sample m unique names (m from [0-3])
**Random selection: m = 0**

(No personal names - this test uses team names only)

---

### Step 4: Theme & Task Sequence

**Theme: Quarterly Resource Allocation Review**

A standard corporate scenario: the PMO is conducting a quarterly review of team staffing levels and needs to rebalance work and flag understaffed teams.

**Unique Computational Challenge:**

The agent must:
1. Query all teams and count their members
2. Identify the team with the MAXIMUM member count
3. For each team with FEWER members than the max, calculate the gap
4. Create a staffing request issue in each understaffed team with the exact gap number
5. Move a misrouted issue between teams
6. Document the analysis in a comment

**Seed Data Structure:**
```
Teams and member counts:
├── Engineering: 5 members (MAX)
├── Product: 3 members (gap = 2)
├── Design: 2 members (gap = 3)
└── QA: 4 members (gap = 1)
```

This requires:
- Aggregation (count members per team)
- Max finding (identify largest team)
- Arithmetic (calculate gaps)
- Conditional issue creation (only for teams below max)

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `teams` | Query all teams with their member counts |
| 2 | `issues` | Find "API Documentation Update" issue that was misrouted to Design |
| 3 | `issueUpdate` | Move the misrouted issue from Design team to Engineering team |
| 4 | `issueCreate` | Create staffing issue in Product team: "Need 2 more members" |
| 5 | `issueCreate` | Create staffing issue in Design team: "Need 3 more members" |
| 6 | `issueCreate` | Create staffing issue in QA team: "Need 1 more member" |
| 7 | `commentCreate` | Add analysis summary to Engineering team's backlog |

---

### Generated Prompt

```
The PMO is conducting a Q1 resource allocation review. Here's what needs to happen:

First, look at all teams and count how many members each team has.

Find the team with the most members - this is our "fully staffed" benchmark.

For every team that has FEWER members than the benchmark team, create a new issue in that team titled "Q1 Staffing Request - Need [X] additional team members" where [X] is the exact difference between that team's member count and the benchmark team's count. Set priority to High for these issues.

Also, there's a misrouted issue: "API Documentation Update" was accidentally created in the Design team but belongs in Engineering. Move it to the Engineering team.

Finally, add a comment to any issue in the Engineering team summarizing the analysis:

"RESOURCE_AUDIT: Q1 staffing review complete. Engineering has [MAX] members (benchmark). Staffing gaps identified: Product needs [A], Design needs [B], QA needs [C]. Total headcount gap across org: [TOTAL]. Staffing request issues created in all understaffed teams."

Replace the bracketed values with the actual numbers from your analysis.
```

---

### Verifiable Keywords/Assertions

1. **Issue moved**: "API Documentation Update" is now in Engineering team (was in Design)
2. **Product staffing issue**: Title contains "Staffing Request" and "2 additional", team is Product, priority is High
3. **Design staffing issue**: Title contains "Staffing Request" and "3 additional", team is Design, priority is High
4. **QA staffing issue**: Title contains "Staffing Request" and "1 additional", team is QA, priority is High
5. **No Engineering staffing issue**: Engineering team has NO new staffing request issue (it's the benchmark)
6. **Comment contains correct numbers**: Body contains "RESOURCE_AUDIT:" AND "5 members" AND "Product needs 2" AND "Design needs 3" AND "QA needs 1" AND "Total headcount gap across org: 6"

### Computational Verification

The agent must correctly calculate:
- Engineering: 5 members (MAX - no issue created)
- Product: 5 - 3 = **2** gap
- Design: 5 - 2 = **3** gap
- QA: 5 - 4 = **1** gap
- Total gap: 2 + 3 + 1 = **6**

**Failure modes:**
- Creates staffing issue for Engineering (wrong - it's the benchmark)
- Wrong gap calculations in issue titles
- Wrong totals in comment
- Forgets to move the misrouted issue
- Creates issues in wrong teams

### Seed Data Requirements

```json
{
  "teams": [
    {"name": "Engineering", "members": ["user1", "user2", "user3", "user4", "user5"]},
    {"name": "Product", "members": ["user6", "user7", "user8"]},
    {"name": "Design", "members": ["user9", "user10"]},
    {"name": "QA", "members": ["user11", "user12", "user13", "user14"]}
  ],
  "issues": [
    {"title": "API Documentation Update", "team": "Design", "description": "Update API docs for v2 endpoints"}
  ]
}
```

### Unique Sequence Characteristics

- **Aggregation-first pattern**: Must count team members before any action
- **Max-finding logic**: Must identify the largest team as benchmark
- **Conditional creation**: Only creates issues for teams BELOW max (not equal)
- **Dynamic content**: Issue titles contain calculated values, not static text
- **Cross-team migration**: Issue movement combined with issue creation
- **Summary with computed values**: Comment must contain multiple calculated numbers

### Metadata
```json
{
  "min_tool_calls": 7,
  "tools_required": [
    "teams",
    "issues",
    "issueUpdate",
    "issueCreate",
    "commentCreate"
  ],
  "requires_aggregation": true,
  "requires_max_finding": true,
  "requires_arithmetic": true,
  "expected_calculations": {
    "max_team": "Engineering",
    "max_count": 5,
    "gaps": {
      "Product": 2,
      "Design": 3,
      "QA": 1
    },
    "total_gap": 6
  }
}
```

---

## Test Generation #17

### Step 1: Sample n (number of endpoints)
**Random selection from range [2-5]: n = 4**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `comments`
2. `users`
3. `issueCreate`
4. `commentCreate`

### Step 3: Sample m unique names (m from [0-3])
**Random selection: m = 1**

**Names from different cultural traditions:**
1. **Saoirse** (Irish - meaning "freedom")

---

### Step 4: Theme & Task Sequence

**Theme: Community Guidelines Enforcement - Profanity Audit**

A moderation team needs to find all comments containing a specific flagged word, document them for cleanup, and warn the authors.

**Unique Action Pattern:**
- Query-first with aggregation (find and count matching comments)
- Data extraction (collect comment IDs for the cleanup ticket)
- Notification pattern (warn authors via reply comments)
- Compact but requires multi-entity coordination

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `comments` | Query all comments to find ones containing "YOLO_BAD" |
| 2 | `users` | Look up Saoirse to assign the cleanup task |
| 3 | `issueCreate` | Create "Content Cleanup Required" ticket with count and comment IDs |
| 4 | `commentCreate` | Add warning replies to issues where violations occurred |

---

### Generated Prompt

```
The moderation team has flagged the word "YOLO_BAD" as inappropriate for our workspace. We need to audit and address any comments containing this term.

First, search through all comments to find any that contain "YOLO_BAD". Count how many comments contain this word and note their IDs.

Create a new issue in the Moderation team titled "Content Cleanup Required - YOLO_BAD audit" assigned to Saoirse. In the description, include:
- The exact count of comments found containing "YOLO_BAD"
- A list of the comment IDs that need to be reviewed
- Use this format: "AUDIT_RESULT: Found [X] comments containing flagged content. Comment IDs: [id1, id2, ...]"

For each issue that has a comment containing "YOLO_BAD", add a warning comment: "MODERATION_NOTICE: A comment on this issue contains content that violates community guidelines. Please review and edit your comment to remove inappropriate language. Ref: YOLO_BAD audit."
```

---

### Verifiable Keywords/Assertions

1. **Cleanup issue created**: Title contains "Content Cleanup" and "YOLO_BAD", assigned to Saoirse
2. **Issue description contains count**: Description contains "AUDIT_RESULT:" AND "Found 3 comments" (seed will have exactly 3)
3. **Issue description contains IDs**: Description contains all 3 comment IDs from seed
4. **Warning comments added**: At least 2 comments containing "MODERATION_NOTICE:" exist (2 issues have bad comments, one has 2 bad comments)

### Seed Data Requirements

```json
{
  "team": {"name": "Moderation"},
  "users": [
    {"name": "Saoirse"},
    {"name": "Derek"},
    {"name": "Mila"}
  ],
  "issues": [
    {"title": "Feature request - dark mode", "team": "Engineering"},
    {"title": "Bug in checkout flow", "team": "Engineering"},
    {"title": "Update landing page", "team": "Product"}
  ],
  "comments": [
    {
      "id": "comment-bad-001",
      "issueTitle": "Feature request - dark mode",
      "body": "This is taking forever YOLO_BAD just ship it already",
      "author": "Derek"
    },
    {
      "id": "comment-bad-002",
      "issueTitle": "Feature request - dark mode",
      "body": "YOLO_BAD I agree this is ridiculous",
      "author": "Mila"
    },
    {
      "id": "comment-bad-003",
      "issueTitle": "Bug in checkout flow",
      "body": "Who wrote this YOLO_BAD code anyway",
      "author": "Derek"
    },
    {
      "id": "comment-clean-001",
      "issueTitle": "Update landing page",
      "body": "Looks great, approved!",
      "author": "Saoirse"
    }
  ]
}
```

### Computational Verification

The agent must correctly:
- Find exactly **3** comments containing "YOLO_BAD"
- Identify that they span **2** unique issues (dark mode has 2, checkout has 1)
- Include all 3 comment IDs in the cleanup ticket
- Add warning comments to the 2 affected issues (NOT to the clean "landing page" issue)

**Failure modes:**
- Wrong count in the ticket description
- Missing comment IDs
- Adds warning to issues without violations
- Doesn't add warning to all affected issues
- Assigns to wrong person

### Unique Sequence Characteristics

- **Search-aggregate-act pattern**: Must search, count, and collect before creating
- **Data inclusion in creation**: Created issue must contain computed values (count + IDs)
- **Selective commenting**: Only comments on issues with violations, not all issues
- **Cross-entity correlation**: Links comments → issues → new comments

### Metadata
```json
{
  "min_tool_calls": 4,
  "tools_required": [
    "comments",
    "users",
    "issueCreate",
    "commentCreate"
  ],
  "requires_counting": true,
  "requires_id_collection": true,
  "expected_count": 3,
  "affected_issues": 2
}
```

---

## Test Generation #18

### Step 1: Sample n (number of endpoints)
**Random selection from range [2-5]: n = 4**

### Step 2: Sample n endpoints with replacement from Linear API

**Sampled endpoints (with replacement):**
1. `issues`
2. `issueCreate`
3. `issueUpdate`
4. `commentCreate`

### Step 3: Sample m unique names (m from [0-3])
**Random selection: m = 2**

**Names from different cultural traditions:**
1. **Amadi** (Nigerian - Igbo, meaning "free man")
2. **Liora** (Hebrew, meaning "light for me")

---

### Step 4: Theme & Task Sequence

**Theme: Competitive Pigeon Racing Club - Storm Emergency Protocol**

A competitive pigeon racing club uses Linear to track their birds, races, and flight logistics. An unexpected storm system is approaching the region where several birds are mid-flight during a weekend race. The race coordinator must execute emergency protocols.

**Unique Action Pattern:**
- Query-first to identify at-risk birds (issues in specific state)
- Create an emergency coordination ticket
- Update existing bird tracking issues with diversion instructions
- Add official weather advisory comment with coordinates

---

### Endpoint Usage Justification

| Step | Endpoint | Justification |
|------|----------|---------------|
| 1 | `issues` | Find all bird tracking issues currently in "In Flight" status for the weekend race |
| 2 | `issueCreate` | Create storm emergency coordination ticket with weather severity |
| 3 | `issueUpdate` | Update the in-flight bird "Stormchaser" with diversion loft coordinates |
| 4 | `commentCreate` | Add official weather advisory to emergency ticket with timestamp and GPS |

---

### Generated Prompt

```
The Wing & Wind pigeon racing club has an emergency. A fast-moving storm system is approaching the race corridor and we need to execute safety protocols.

First, find all birds currently marked as "In Flight" in the Racing Operations team - these are the ones at risk.

Create an emergency coordination issue in the Racing Operations team titled "WEATHER ALERT: Storm cell approaching sector 7 - All birds at risk" with description "NWS severe thunderstorm warning issued 14:32 UTC. Wind gusts to 60mph expected. Initiating emergency diversion protocol."

Find the bird tracking issue for "Stormchaser" (Liora's champion racer, band #2847). Update it to add this to the description: "DIVERSION ACTIVE: Rerouted to backup loft at coordinates 41.8781° N, 87.6298° W. Amadi's loft confirmed ready to receive."

Finally, add a weather advisory comment to the emergency coordination issue:
"WEATHER_LOG: Storm tracking update at 14:45 UTC. Cell moving NNE at 35mph. ETA to race corridor: 47 minutes. All handlers notified via SMS. GPS tracking shows 3 birds diverted successfully. Amadi confirming visual on Stormchaser approaching backup loft."
```

---

### Verifiable Keywords/Assertions

1. **Emergency issue created**: Title contains "WEATHER ALERT" and "sector 7", description contains "NWS" and "60mph"
2. **Stormchaser updated**: Issue containing "Stormchaser" has description with "DIVERSION ACTIVE" and "41.8781° N, 87.6298° W"
3. **Comment format**: Body contains "WEATHER_LOG:" AND "14:45 UTC" AND "35mph" AND "Amadi confirming"
4. **Names present**: Liora mentioned in context of Stormchaser, Amadi mentioned in diversion coordinates AND weather log

### Seed Data Requirements

```json
{
  "team": {"name": "Racing Operations"},
  "workflow_states": [
    {"name": "Registered", "type": "backlog"},
    {"name": "Pre-Flight", "type": "unstarted"},
    {"name": "In Flight", "type": "started"},
    {"name": "Landed", "type": "completed"}
  ],
  "users": [
    {"name": "Liora"},
    {"name": "Amadi"},
    {"name": "Viktor"}
  ],
  "issues": [
    {
      "title": "Bird #2847 - Stormchaser",
      "description": "Liora's championship racer. Band: 2847. Breed: Racing Homer. Released 09:15 UTC from checkpoint Alpha.",
      "state": "In Flight",
      "assignee": "Liora"
    },
    {
      "title": "Bird #3102 - Quicksilver",
      "description": "Viktor's veteran racer. Band: 3102. Released 09:18 UTC from checkpoint Alpha.",
      "state": "In Flight",
      "assignee": "Viktor"
    },
    {
      "title": "Bird #2956 - Nightwing",
      "description": "Amadi's young prospect. Band: 2956. Released 09:12 UTC from checkpoint Alpha.",
      "state": "In Flight",
      "assignee": "Amadi"
    },
    {
      "title": "Bird #2201 - Cloudrunner",
      "description": "Club reserve bird. Resting after last week's race.",
      "state": "Registered",
      "assignee": null
    }
  ]
}
```

### Unique Sequence Characteristics

- **Emergency response pattern**: Time-sensitive scenario requiring quick coordination
- **GPS coordinate inclusion**: Tests ability to handle precise location data in updates
- **Multi-entity reference**: Emergency ticket references birds, handlers, and locations
- **Append-to-description pattern**: Update adds to existing description rather than replacing
- **Timestamp verification**: Comment must include specific times for audit trail

### Metadata
```json
{
  "min_tool_calls": 4,
  "tools_required": [
    "issues",
    "issueCreate",
    "issueUpdate",
    "commentCreate"
  ],
  "requires_state_filtering": true,
  "expected_in_flight_birds": 3,
  "coordinate_precision_test": true
}
```
