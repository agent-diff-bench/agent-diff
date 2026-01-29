# Google Calendar Agent Scenarios

## 1. Event Management (Basic)
- Create a simple event ("Meeting with John tomorrow at 2pm")
- Create an event with duration ("2 hour brainstorming session")
- Create an event with location and description
- Update an event's time ("Move the team meeting to 3pm")
- Update an event's title/description
- Delete an event ("Cancel the 1:1 with Sarah")
- Get event details ("Where is the offsite happening?")

## 2. Scheduling & Querying
- List events for a specific day ("What's on my calendar for Monday?")
- Find free time ("Am I free between 2pm and 4pm?")
- Check specific availability ("Do I have any conflicts on Wednesday afternoon?")
- Summarize schedule ("Give me a briefing of my meetings today")

## 3. Recurring Events
- Create a daily recurring event ("Standup every weekday at 10am")
- Create a weekly recurring event
- Create a monthly recurring event
- Delete a specific instance of a recurring series ("Cancel standup for this Friday only")
- Update a specific instance ("Move this week's 1:1 to Tuesday")
- Delete the entire series

## 4. Attendees & Invitations
- Create event with attendees
- Add an attendee to an existing meeting ("Invite alice@example.com to the project review")
- Remove an attendee
- Check attendee status (accepted/declined/tentative)

## 5. Calendar Management
- Create a new secondary calendar ("Create a 'Fitness' calendar")
- List all calendars
- Update calendar summary/color
- Delete a calendar
- Clear a calendar (remove all events)

## 6. Access Control (ACL)
- Share calendar with a user ("Give bob@example.com reader access to my primary calendar")
- Update sharing permissions ("Make Bob a writer")
- Remove sharing permissions ("Stop sharing with Bob")
- List who has access

## 7. CalendarList (Subscription)
- Subscribe to a calendar
- Hide/Show a calendar from the list
- Change the color of a calendar in the list

## 8. Free/Busy
- Query free/busy information for a set of users ("When are Alice and Bob both free?")

## 9. Complex/Compound Tasks
- "Find the next available 30-minute slot where both Alice and I are free, and schedule a 'Sync' meeting"
- "Reschedule all my morning meetings to the afternoon"
- "Find the meeting about 'Project X' and add the 'Marketing' team to it"
- "If I have more than 3 meetings today, block out the rest of the day as 'Focus Time'"
