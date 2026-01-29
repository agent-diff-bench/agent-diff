# Google Calendar API v3 - Complete Endpoint Reference

Base URL: `https://www.googleapis.com/calendar/v3`

---

## Acl (Access Control List)
Manage sharing permissions for calendars.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/calendars/{calendarId}/acl` | List all ACL rules for a calendar |
| GET | `/calendars/{calendarId}/acl/{ruleId}` | Get a specific ACL rule |
| POST | `/calendars/{calendarId}/acl` | Create/insert a new ACL rule (share calendar) |
| PUT | `/calendars/{calendarId}/acl/{ruleId}` | Update an ACL rule (full replacement) |
| PATCH | `/calendars/{calendarId}/acl/{ruleId}` | Update an ACL rule (partial update) |
| DELETE | `/calendars/{calendarId}/acl/{ruleId}` | Delete an ACL rule (revoke access) |
| POST | `/calendars/{calendarId}/acl/watch` | Watch for changes to ACL rules |

---

## CalendarList
Manage the list of calendars shown in the user's calendar UI (subscriptions).

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me/calendarList` | List all calendars in user's calendar list |
| GET | `/users/me/calendarList/{calendarId}` | Get a specific calendar list entry |
| POST | `/users/me/calendarList` | Add an existing calendar to user's list (subscribe) |
| PUT | `/users/me/calendarList/{calendarId}` | Update a calendar list entry (full replacement) |
| PATCH | `/users/me/calendarList/{calendarId}` | Update a calendar list entry (partial - e.g., color, hidden) |
| DELETE | `/users/me/calendarList/{calendarId}` | Remove a calendar from user's list (unsubscribe) |
| POST | `/users/me/calendarList/watch` | Watch for changes to calendar list entries |

---

## Calendars
Manage calendar resources (metadata, creation, deletion).

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/calendars/{calendarId}` | Get calendar metadata (summary, timezone, etc.) |
| POST | `/calendars` | Create a new secondary calendar |
| PUT | `/calendars/{calendarId}` | Update calendar metadata (full replacement) |
| PATCH | `/calendars/{calendarId}` | Update calendar metadata (partial update) |
| DELETE | `/calendars/{calendarId}` | Delete a secondary calendar permanently |
| POST | `/calendars/{calendarId}/clear` | Clear all events from a calendar (keeps the calendar) |

---

## Channels
Manage push notification channels.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/channels/stop` | Stop receiving push notifications for a channel |

### Channel Resource (for watch requests)
All `*.watch` endpoints require a **Channel** request body with at least:
- `id` (string, unique channel ID)
- `type` (string, usually `web_hook`)
- `address` (string, webhook callback URL)

Example body:
```json
{
  "id": "settings-watch-123",
  "type": "web_hook",
  "address": "https://example.com/webhook",
  "token": "optional-token",
  "params": {"ttl": "86400"},
  "payload": false,
  "expiration": 1711929600000
}
```

---

## Colors
Get color definitions for calendars and events.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/colors` | Get the color palette (IDs and hex values) for calendars/events |

---

## Events
Core event management - create, read, update, delete, and special operations.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/calendars/{calendarId}/events` | List events on a calendar (supports filtering, pagination, sync) |
| GET | `/calendars/{calendarId}/events/{eventId}` | Get a specific event by ID |
| POST | `/calendars/{calendarId}/events` | Create a new event |
| PUT | `/calendars/{calendarId}/events/{eventId}` | Update an event (full replacement) |
| PATCH | `/calendars/{calendarId}/events/{eventId}` | Update an event (partial - e.g., just description) |
| DELETE | `/calendars/{calendarId}/events/{eventId}` | Delete an event |
| POST | `/calendars/{calendarId}/events/quickAdd` | Create event from natural language text (e.g., "Lunch with Priya tomorrow at noon") |
| POST | `/calendars/{calendarId}/events/import` | Import an event (creates a private copy with a new iCalUID) |
| POST | `/calendars/{calendarId}/events/{eventId}/move` | Move an event to a different calendar |
| GET | `/calendars/{calendarId}/events/{eventId}/instances` | Get all instances of a recurring event |
| POST | `/calendars/{calendarId}/events/watch` | Watch for changes to events on a calendar |

---

## Freebusy
Query availability across calendars.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/freeBusy` | Query free/busy information for one or more calendars in a time range |

---

## Settings
Read user-level settings (read-only via API).

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me/settings` | List all user settings |
| GET | `/users/me/settings/{setting}` | Get a specific setting (e.g., timezone, dateFieldOrder) |
| POST | `/users/me/settings/watch` | Watch for changes to user settings |

**Note:** Settings watch is **`/users/me/settings/watch`** (not a calendar-scoped endpoint). Use the Channel body above.

---

## Summary by Resource

| Resource | Total Endpoints | CRUD Methods | Watch Method |
|----------|-----------------|--------------|--------------|
| Acl | 7 | list, get, insert, update, patch, delete | Yes |
| CalendarList | 7 | list, get, insert, update, patch, delete | Yes |
| Calendars | 6 | get, insert, update, patch, delete, clear | No |
| Channels | 1 | stop | N/A |
| Colors | 1 | get | No |
| Events | 11 | list, get, insert, update, patch, delete, quickAdd, import, move, instances | Yes |
| Freebusy | 1 | query | No |
| Settings | 3 | list, get | Yes |

**Total: 37 endpoints**

---

## Common Query Parameters

Many endpoints support these common parameters:

| Parameter | Description |
|-----------|-------------|
| `fields` | Partial response - specify which fields to include |
| `key` | API key (for public data only) |
| `oauth_token` | OAuth 2.0 token |
| `prettyPrint` | Returns response with indentations (default: true) |
| `quotaUser` | Quota enforcement identifier |
| `maxResults` | Maximum number of entries to return |
| `pageToken` | Token for pagination |
| `syncToken` | Token for incremental sync |
| `timeMin` / `timeMax` | Filter events by time range (RFC3339) |
| `singleEvents` | Expand recurring events into instances |
| `orderBy` | Sort order (startTime, updated) |
| `showDeleted` | Include deleted events (for sync) |
| `showHiddenInvitations` | Include hidden invitations |
