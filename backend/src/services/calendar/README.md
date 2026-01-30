# Google Calendar API Replica

A 1:1 replica of the Google Calendar API v3 for testing and development purposes.

## Overview

This service implements a faithful replica of the [Google Calendar API v3](https://developers.google.com/calendar/api/v3/reference), following the same patterns as our Slack and Linear replicas.

## Architecture

```
services/calendar/
├── api/
│   └── methods.py          # REST endpoint handlers (to be implemented)
├── core/
│   ├── errors.py           # Google-style error responses
│   └── utils.py            # ID generation, ETag, datetime, pagination utilities
├── database/
│   ├── base.py             # SQLAlchemy Base class
│   ├── operations.py       # Database CRUD operations
│   └── schema.py           # SQLAlchemy ORM models
└── README.md
```

## Database Schema

### Core Entities

| Table | Description |
|-------|-------------|
| `calendar_users` | User/Principal entities |
| `calendars` | Calendar resources |
| `calendar_list_entries` | User's subscriptions to calendars |
| `calendar_events` | Event resources |
| `calendar_event_attendees` | Event attendees |
| `calendar_event_reminders` | Event reminder overrides |
| `calendar_acl_rules` | Access Control List rules |
| `calendar_settings` | User settings |
| `calendar_channels` | Push notification channels (stub) |
| `calendar_sync_tokens` | Sync tokens for incremental sync |

### Enums

- `AccessRole`: freeBusyReader, reader, writer, owner
- `EventStatus`: confirmed, tentative, cancelled
- `EventTransparency`: opaque, transparent
- `EventVisibility`: default, public, private, confidential
- `EventType`: default, outOfOffice, focusTime, workingLocation, fromGmail, birthday
- `AttendeeResponseStatus`: needsAction, declined, tentative, accepted
- `AclScopeType`: default, user, group, domain
- `ReminderMethod`: email, popup

## API Endpoints (38 total)

### Phase 1 - Core (Implemented in DB Layer)

| Resource | Endpoints |
|----------|-----------|
| `calendars` | get, insert, update, patch, delete, clear |
| `calendarList` | list, get, insert, update, patch, delete |
| `events` | list, get, insert, update, patch, delete, quickAdd, import, move, instances |

### Phase 2 - ACL (Implemented in DB Layer)

| Resource | Endpoints |
|----------|-----------|
| `acl` | list, get, insert, update, patch, delete |

### Phase 3 - Utility (Implemented in DB Layer)

| Resource | Endpoints |
|----------|-----------|
| `settings` | list, get |
| `freebusy` | query |
| `colors` | get (static response) |

### Phase 4 - Watch (Stub)

| Resource | Endpoints |
|----------|-----------|
| `*.watch` | All watch endpoints (stub) |
| `channels` | stop (stub) |

## ID Formats

### Event ID
- Characters: `a-v` (lowercase) and `0-9` (base32hex encoding)
- Length: 5-1024 characters
- Generated using UUID v4 → base32hex encoding

### Calendar ID
- Primary calendar: User's email address
- Secondary calendar: `c_{random}@group.calendar.google.com`

### ACL Rule ID
- Format: `{scope_type}:{scope_value}` (e.g., `user:john@example.com`)
- Default scope: `default`

### iCalUID
- Format: `{event_id}@{domain}` (RFC5545 compliant)

## Error Handling

Errors follow Google's standard format:

```json
{
  "error": {
    "code": 404,
    "message": "Calendar not found: xyz",
    "errors": [
      {
        "domain": "calendar",
        "reason": "notFound",
        "message": "Calendar not found: xyz"
      }
    ]
  }
}
```

### Error Reasons

| Reason | HTTP Status | Description |
|--------|-------------|-------------|
| `notFound` | 404 | Resource not found |
| `invalid` | 400 | Invalid request |
| `required` | 400 | Required field missing |
| `duplicate` | 409 | Resource already exists |
| `forbidden` | 403 | Insufficient permissions |
| `authError` | 401 | Authentication required |
| `preconditionFailed` | 412 | ETag mismatch |
| `fullSyncRequired` | 410 | Sync token expired |

## Session & Auth Pattern

```python
def _session(request: Request):
    session = getattr(request.state, "db_session", None)
    if session is None:
        raise CalendarAPIError("Database session not available", 500)
    return session

def _authenticated_user(request: Request) -> str:
    """Get the authenticated user ID (handles impersonation)."""
    session = _session(request)
    impersonate_user_id = getattr(request.state, "impersonate_user_id", None)
    impersonate_email = getattr(request.state, "impersonate_email", None)
    
    if impersonate_user_id:
        return impersonate_user_id
    
    if impersonate_email:
        user = session.query(User).filter(User.email == impersonate_email).first()
        if user:
            return user.id
    
    raise UnauthorizedError()
```

## Usage Examples

### Create a user with primary calendar

```python
from services.calendar.database import create_user, get_calendar

user = create_user(
    session,
    email="john@example.com",
    display_name="John Doe",
)
# Primary calendar is automatically created
calendar = get_calendar(session, "primary", user.id)
```

### Create an event

```python
from services.calendar.database import create_event

event = create_event(
    session,
    calendar_id="primary",
    user_id=user.id,
    summary="Team Meeting",
    start={"dateTime": "2024-01-15T10:00:00Z", "timeZone": "UTC"},
    end={"dateTime": "2024-01-15T11:00:00Z", "timeZone": "UTC"},
    attendees=[
        {"email": "jane@example.com"},
        {"email": "bob@example.com"},
    ],
)
```

### List events with pagination

```python
from services.calendar.database import list_events

events, next_page_token, sync_token = list_events(
    session,
    calendar_id="primary",
    user_id=user.id,
    max_results=100,
    time_min="2024-01-01T00:00:00Z",
    time_max="2024-12-31T23:59:59Z",
)

# For subsequent incremental sync
events, _, new_sync_token = list_events(
    session,
    calendar_id="primary",
    user_id=user.id,
    sync_token=sync_token,
)
```

## Dependencies

- SQLAlchemy (ORM)
- python-dateutil (datetime parsing, recurrence expansion)
- Starlette (HTTP responses)

## Implementation Status

- [x] Database schema (all models)
- [x] Core utilities (ID generation, ETag, pagination)
- [x] Error handling (Google-style)
- [x] Database operations (CRUD for all resources)
- [ ] REST API endpoints (`api/methods.py`)
- [ ] Batch request support
- [ ] Watch/Push notifications (stub only)
- [ ] Recurring event expansion

## Next Steps

1. Implement REST API endpoint handlers in `api/methods.py`
2. Add response serializers to convert ORM models to JSON
3. Integrate with the isolation middleware
4. Write integration tests
5. Add batch request support
