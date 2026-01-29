# Google Calendar Benchmark Prompts

## Easy Tasks (1-2 Tool Calls)
Expected to require simple CRUD operations or direct queries.

1.  **Create simple event**: "Schedule a 'Team Lunch' for tomorrow at 12pm."
2.  **List daily events**: "What is on my agenda for today?"
3.  **Get event details**: "Show me the details for the 'Project Kickoff' meeting."
4.  **Delete specific event**: "Cancel the meeting with ID 'evt_12345'."
5.  **Create calendar**: "Create a new secondary calendar named 'Gym Schedule'."
6.  **Quick add**: "Add 'Dentist appointment' to my calendar for next Monday at 9am."
7.  **Update description**: "Update the description of the 'Weekly Sync' meeting to include 'Review Q3 goals'."
8.  **Update location**: "Change the location of the 'Board Meeting' to 'Conference Room A'."
9.  **List calendars**: "List all the calendars I have access to."
10. **Subscribe to calendar**: "Subscribe to the public holiday calendar for US."

## Medium Tasks (3-4 Tool Calls)
Expected to require retrieval followed by action, basic conditional logic, or multi-step configuration.

11. **Reschedule specific meeting**: "Find the meeting with 'Priya' regarding 'Design' and move it to 3pm."
12. **Conditional booking**: "Check if I'm free tomorrow at 2pm. If I am, schedule a 'Client Call'."
13. **Invite attendee to existing**: "Find the 'Budget Review' meeting and invite 'finance@example.com'."
14. **Create with attendees**: "Schedule a 'Product Sync' next Tuesday at 10am and invite 'wei.zhang@test.com', 'fatima@test.com', and 'newuser@external.com'."
15. **Manage permissions**: "Share my 'Work' calendar with 'intern@example.com' giving them read-only access."
16. **Handle conflict**: "I have two meetings at 10am tomorrow. Decline the one titled 'Optional Training'."
17. **Update recurrence exception**: "Move just this Friday's 'Standup' meeting to 11am."
18. **Add virtual location**: "Add a Google Meet link (description) and set location to 'Virtual' for all my meetings tomorrow."
19. **RSVP**: "Find the invitation for the 'All Hands' meeting and accept it."
20. **Copy event**: "Duplicate the 'Client Intro' meeting to next Tuesday at the same time."

## Hard Tasks (5+ Tool Calls)
Expected to require complex reasoning, iteration, batch processing, or multi-user coordination.

21. **Multi-timezone scheduling**: "Find a 1-hour slot where Yara (Buenos Aires), Raj (India Standard Time), and Luka (US Eastern) can all meet. The meeting must be after 9am UTC. Schedule it for the earliest possible slot and invite them."
22. **Vacation mode**: "I'm out next week. Decline all my accepted meetings for that week and create an 'Out of Office' event for the whole week with the description 'Contact Wei for emergencies'."
23. **Smart reschedule**: "Reschedule the 'Product Review' to the next time slot that works for all current attendees."
24. **Batch description update**: "Update the description of all 'Interview' events next week to include 'Please read the candidate's resume beforehand'."
25. **Complex invite management**: "Find the 'Q4 Planning' meeting. If 'dmitri@test.com' is not invited, invite him. If 'priya@test.com' is invited, remove her."
26. **Calendar migration**: "Copy all my meetings from my 'Personal' calendar to my 'Work' calendar for today, marking them as 'Private'."
27. **Rotation setup**: "Schedule a daily 'Triage' task for next week, alternating the assignee between Fatima (Mon/Wed/Fri) and Wei (Tue/Thu) in the description."
28. **Conflict audit**: "Analyze my schedule for next week. List all time slots where I am double-booked."
29. **Re-organize day**: "Clear my morning schedule for tomorrow (until 12pm) by moving all existing meetings to the afternoon (after 1pm)."
30. **Project setup**: "Create a new 'Project X' calendar, share it with the team (fatima@test.com, wei@test.com), and schedule a 'Kickoff' meeting on it for next Monday at 10am."
