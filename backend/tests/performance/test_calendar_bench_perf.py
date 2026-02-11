"""
Performance tests for Calendar API - mimicking real calendar_bench operations.

These tests create an isolated Calendar environment (calendar_default template),
then run the same API call patterns that appear in the calendar_bench test suite
to measure response times and identify bottlenecks.

Usage:
    # Run via docker exec (from ops/ directory):
    docker exec ops-backend-1 python -m pytest tests/performance/test_calendar_bench_perf.py -v -s

    # Run with timing threshold (skip assertions under N ms):
    docker exec ops-backend-1 sh -c "PERF_THRESHOLD_MS=100 python -m pytest tests/performance/test_calendar_bench_perf.py -v -s"

Environment setup:
    1. The calendar_default template must be seeded in the database.
    2. Tests use core_isolation_engine.create_environment(template_schema="calendar_default")
       to create an isolated copy of the template.
    3. The impersonate_user_id "user_agent" matches the bench's default user (test.user@test.com).
    4. All environments are auto-cleaned after the test session.
"""

import asyncio
import logging
import os
import time

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from starlette.applications import Starlette

from src.services.calendar.api import routes as calendar_routes

logger = logging.getLogger(__name__)

# Default user from calendar_bench.json
CALENDAR_IMPERSONATE_USER_ID = "user_agent"
CALENDAR_IMPERSONATE_EMAIL = "test.user@test.com"

# Well-known IDs from calendar_default seed data
PRIMARY_CALENDAR_ID = "test.user@test.com"
HARVEST_CALENDAR_ID = "cal_harvest_schedule"
DUNGEON_MASTERS_CALENDAR_ID = "cal_dungeon_masters"
TIMELINE_ALPHA_CALENDAR_ID = "cal_timeline_alpha"
EVENT_FAILED_ROCKET_ID = "event_failed_rocket"
EVENT_WEED_WARRIOR_ID = "event_weed_warrior"

# Threshold in ms - tests log warnings above this
PERF_THRESHOLD_MS = int(os.environ.get("PERF_THRESHOLD_MS", "500"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _timed(label: str):
    """Context manager that logs elapsed time."""

    class Timer:
        def __init__(self):
            self.elapsed_ms = 0.0

        def __enter__(self):
            self._start = time.perf_counter()
            return self

        def __exit__(self, *exc):
            self.elapsed_ms = (time.perf_counter() - self._start) * 1000
            marker = "SLOW" if self.elapsed_ms > PERF_THRESHOLD_MS else "OK"
            logger.info(f"[PERF {marker}] {label}: {self.elapsed_ms:.0f}ms")

    return Timer()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def _cal_env(
    test_user_id,
    core_isolation_engine,
    session_manager,
    environment_handler,
):
    """
    Create ONE isolated calendar_default environment for the entire test session.
    Cloning the large calendar_default seed (~12k lines) per test is ~2-3s each;
    doing it once drops total wall-clock from ~95s to <15s.
    """
    env_result = core_isolation_engine.create_environment(
        template_schema="calendar_default",
        ttl_seconds=3600,
        created_by=test_user_id,
        impersonate_user_id=CALENDAR_IMPERSONATE_USER_ID,
        impersonate_email=CALENDAR_IMPERSONATE_EMAIL,
    )
    yield env_result
    environment_handler.drop_schema(env_result.schema_name)


@pytest_asyncio.fixture
async def cal_client(_cal_env, session_manager):
    """
    Lightweight per-test fixture: reuses the session-scoped environment,
    only creates a fresh AsyncClient + Starlette app (sub-millisecond).
    """
    env_result = _cal_env

    async def add_db_session(request, call_next):
        with session_manager.with_session_for_environment(
            env_result.environment_id
        ) as session:
            request.state.db_session = session
            request.state.db = session
            request.state.environment_id = env_result.environment_id
            request.state.impersonate_user_id = CALENDAR_IMPERSONATE_USER_ID
            request.state.impersonate_email = CALENDAR_IMPERSONATE_EMAIL
            response = await call_next(request)
            return response

    app = Starlette(routes=calendar_routes)
    app.middleware("http")(add_db_session)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# ---------------------------------------------------------------------------
# Test: GET /users/me/calendarList (bench: calendarList.list)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_calendar_list(cal_client: AsyncClient):
    """GET /users/me/calendarList — list user's calendars (very common operation)."""
    with _timed("GET /users/me/calendarList") as t:
        resp = await cal_client.get("/users/me/calendarList")

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#calendarList"
    assert len(data["items"]) >= 1
    logger.info(f"  CalendarList returned {len(data['items'])} entries")
    assert t.elapsed_ms < 5000, f"calendarList.list took {t.elapsed_ms:.0f}ms (>5s)"


# ---------------------------------------------------------------------------
# Test: GET /calendars/{calendarId} (bench: calendars.get)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_primary_calendar(cal_client: AsyncClient):
    """GET /calendars/primary — get primary calendar."""
    with _timed("GET /calendars/primary") as t:
        resp = await cal_client.get("/calendars/primary")

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#calendar"
    assert data["id"] == PRIMARY_CALENDAR_ID
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_get_secondary_calendar(cal_client: AsyncClient):
    """GET /calendars/{calendarId} — get Harvest Schedule calendar."""
    with _timed(f"GET /calendars/{HARVEST_CALENDAR_ID}") as t:
        resp = await cal_client.get(f"/calendars/{HARVEST_CALENDAR_ID}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#calendar"
    assert "Harvest" in data["summary"]
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: POST /calendars (bench: calendars.insert — bench test_1, test_2, ...)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_calendar(cal_client: AsyncClient):
    """POST /calendars — create a new secondary calendar (bench test_1)."""
    with _timed("POST /calendars") as t:
        resp = await cal_client.post(
            "/calendars",
            json={
                "summary": "Cosmic Voyagers HQ",
                "description": "Stargazing activities",
                "timeZone": "America/Los_Angeles",
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#calendar"
    assert data["summary"] == "Cosmic Voyagers HQ"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: PATCH /calendars/{calendarId} (bench: calendars.patch)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_patch_calendar(cal_client: AsyncClient):
    """PATCH /calendars/{calendarId} — update calendar description (bench test_5)."""
    with _timed(f"PATCH /calendars/{HARVEST_CALENDAR_ID}") as t:
        resp = await cal_client.patch(
            f"/calendars/{HARVEST_CALENDAR_ID}",
            json={"description": "Updated harvest calendar"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["description"] == "Updated harvest calendar"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: GET /calendars/{calendarId}/events (bench: events.list)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_events_primary(cal_client: AsyncClient):
    """GET /calendars/primary/events — list events on primary calendar."""
    with _timed("GET /calendars/primary/events") as t:
        resp = await cal_client.get(
            "/calendars/primary/events",
            params={"timeMin": "2018-01-01T00:00:00Z", "maxResults": 250},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#events"
    logger.info(f"  Primary calendar has {len(data.get('items', []))} events")
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_list_events_secondary(cal_client: AsyncClient):
    """GET /calendars/{calendarId}/events — list events on Harvest Schedule."""
    with _timed(f"GET /calendars/{HARVEST_CALENDAR_ID}/events") as t:
        resp = await cal_client.get(
            f"/calendars/{HARVEST_CALENDAR_ID}/events",
            params={"timeMin": "2018-01-01T00:00:00Z"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#events"
    logger.info(f"  Harvest calendar has {len(data.get('items', []))} events")
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_list_events_with_search(cal_client: AsyncClient):
    """GET /calendars/{calendarId}/events?q=... — search events (bench test_4, 5, 6)."""
    with _timed("GET events?q=Weed") as t:
        resp = await cal_client.get(
            f"/calendars/{HARVEST_CALENDAR_ID}/events",
            params={"q": "Weed", "timeMin": "2017-01-01T00:00:00Z"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#events"
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_list_events_single_events(cal_client: AsyncClient):
    """GET events?singleEvents=true&orderBy=startTime — expand recurring (common agent pattern)."""
    with _timed("GET events?singleEvents=true") as t:
        resp = await cal_client.get(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events",
            params={
                "singleEvents": "true",
                "orderBy": "startTime",
                "timeMin": "2018-06-01T00:00:00Z",
                "timeMax": "2018-07-01T00:00:00Z",
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#events"
    logger.info(f"  singleEvents returned {len(data.get('items', []))} events")
    assert t.elapsed_ms < 10000, f"singleEvents took {t.elapsed_ms:.0f}ms (>10s)"


# ---------------------------------------------------------------------------
# Test: GET /calendars/{calendarId}/events/{eventId} (bench: events.get)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_event_by_id(cal_client: AsyncClient):
    """GET /calendars/{calendarId}/events/{eventId} — get a specific event."""
    with _timed(f"GET events/{EVENT_FAILED_ROCKET_ID}") as t:
        resp = await cal_client.get(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events/{EVENT_FAILED_ROCKET_ID}"
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#event"
    assert data["id"] == EVENT_FAILED_ROCKET_ID
    assert "Failed Rocket" in data["summary"]
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: POST /calendars/{calendarId}/events (bench: events.insert — test_1..test_9)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_event(cal_client: AsyncClient):
    """POST /calendars/{calendarId}/events — create event (bench test_1)."""
    with _timed("POST events (basic)") as t:
        resp = await cal_client.post(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events",
            json={
                "summary": "Perseid Meteor Shower Watch Party",
                "location": "Hillcrest Observatory Field",
                "start": {
                    "dateTime": "2018-06-24T00:00:00-07:00",
                    "timeZone": "America/Los_Angeles",
                },
                "end": {
                    "dateTime": "2018-06-24T03:00:00-07:00",
                    "timeZone": "America/Los_Angeles",
                },
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#event"
    assert data["summary"] == "Perseid Meteor Shower Watch Party"
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_create_event_with_attendees(cal_client: AsyncClient):
    """POST events with attendees (bench test_2, test_6)."""
    with _timed("POST events (with attendees)") as t:
        resp = await cal_client.post(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events",
            json={
                "summary": "Telescope Alignment Ceremony",
                "start": {
                    "dateTime": "2018-06-23T19:30:00+03:00",
                    "timeZone": "Europe/Kyiv",
                },
                "end": {
                    "dateTime": "2018-06-23T21:00:00+03:00",
                    "timeZone": "Europe/Kyiv",
                },
                "attendees": [
                    {"email": "oleksandra@test.com"},
                    {"email": "yuki@test.com"},
                ],
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert len(data.get("attendees", [])) >= 2
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: PATCH /calendars/{calendarId}/events/{eventId} (bench: events.patch)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_patch_event(cal_client: AsyncClient):
    """PATCH /events/{eventId} — update event details (bench test_1, test_2)."""
    with _timed(f"PATCH events/{EVENT_FAILED_ROCKET_ID}") as t:
        resp = await cal_client.patch(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events/{EVENT_FAILED_ROCKET_ID}",
            json={"description": "Updated: SpaceX launch rescheduled"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["description"] == "Updated: SpaceX launch rescheduled"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: DELETE /calendars/{calendarId}/events/{eventId} (bench: events.delete)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_delete_event(cal_client: AsyncClient):
    """DELETE /events/{eventId} — delete event (bench test_1, test_2, test_3)."""
    # Create a throwaway event to delete (don't mutate shared seed data)
    create_resp = await cal_client.post(
        f"/calendars/{PRIMARY_CALENDAR_ID}/events",
        json={
            "summary": "Throwaway event for delete test",
            "start": {"dateTime": "2018-07-10T10:00:00Z", "timeZone": "UTC"},
            "end": {"dateTime": "2018-07-10T11:00:00Z", "timeZone": "UTC"},
        },
    )
    assert create_resp.status_code == 200
    event_id = create_resp.json()["id"]

    with _timed(f"DELETE events/{event_id}") as t:
        resp = await cal_client.delete(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events/{event_id}"
        )

    assert resp.status_code == 204 or resp.status_code == 200
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: POST /freeBusy (bench: freeBusy.query — test_1..test_8)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_freebusy_single_calendar(cal_client: AsyncClient):
    """POST /freeBusy — query single calendar (bench test_1)."""
    with _timed("POST /freeBusy (1 calendar)") as t:
        resp = await cal_client.post(
            "/freeBusy",
            json={
                "timeMin": "2018-06-23T00:00:00Z",
                "timeMax": "2018-06-24T00:00:00Z",
                "items": [{"id": "oleksandra@test.com"}],
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#freeBusy"
    assert "oleksandra@test.com" in data["calendars"]
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_freebusy_multiple_calendars(cal_client: AsyncClient):
    """POST /freeBusy — query multiple calendars (bench test_2, test_5)."""
    with _timed("POST /freeBusy (3 calendars)") as t:
        resp = await cal_client.post(
            "/freeBusy",
            json={
                "timeMin": "2018-06-18T00:00:00Z",
                "timeMax": "2018-06-25T00:00:00Z",
                "items": [
                    {"id": "kenji@test.com"},
                    {"id": "oksana@test.com"},
                    {"id": "amara@test.com"},
                ],
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["calendars"]) == 3
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: POST /calendars/{calendarId}/acl (bench: acl.insert — test_1..test_8)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_acl_rule(cal_client: AsyncClient):
    """POST /calendars/{calendarId}/acl — grant access (bench test_1)."""
    # First create a calendar to grant access to
    create_resp = await cal_client.post(
        "/calendars",
        json={"summary": "ACL Test Calendar"},
    )
    assert create_resp.status_code == 200
    cal_id = create_resp.json()["id"]

    with _timed(f"POST /calendars/{cal_id}/acl") as t:
        resp = await cal_client.post(
            f"/calendars/{cal_id}/acl",
            json={
                "role": "writer",
                "scope": {
                    "type": "user",
                    "value": "yuki@test.com",
                },
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "writer"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: GET /calendars/{calendarId}/acl (bench: acl.list)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_acl_rules(cal_client: AsyncClient):
    """GET /calendars/{calendarId}/acl — list ACL rules."""
    with _timed(f"GET /calendars/{PRIMARY_CALENDAR_ID}/acl") as t:
        resp = await cal_client.get(f"/calendars/{PRIMARY_CALENDAR_ID}/acl")

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#acl"
    assert len(data["items"]) >= 1
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: GET /colors (bench: colors.get)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_colors(cal_client: AsyncClient):
    """GET /colors — get color definitions."""
    with _timed("GET /colors") as t:
        resp = await cal_client.get("/colors")

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#colors"
    assert "calendar" in data
    assert "event" in data
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: GET /users/me/settings (bench: settings.list)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_settings(cal_client: AsyncClient):
    """GET /users/me/settings — list user settings."""
    with _timed("GET /users/me/settings") as t:
        resp = await cal_client.get("/users/me/settings")

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#settings"
    assert len(data["items"]) >= 1
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_get_setting(cal_client: AsyncClient):
    """GET /users/me/settings/{setting} — get a specific setting."""
    with _timed("GET /users/me/settings/timezone") as t:
        resp = await cal_client.get("/users/me/settings/timezone")

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#setting"
    assert data["id"] == "timezone"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: POST /calendars/{calendarId}/events/quickAdd (bench: events.quickAdd)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_quick_add_event(cal_client: AsyncClient):
    """POST /events/quickAdd — quick add via natural language (bench test_2)."""
    with _timed("POST events/quickAdd") as t:
        resp = await cal_client.post(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events/quickAdd",
            params={"text": "Starlit Tea Ceremony with Akira tomorrow 3pm"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#event"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: POST /calendars/{calendarId}/events/{eventId}/move (bench: events.move)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_move_event(cal_client: AsyncClient):
    """POST /events/{eventId}/move — move event to another calendar (bench test_8)."""
    # First create an event to move
    create_resp = await cal_client.post(
        f"/calendars/{PRIMARY_CALENDAR_ID}/events",
        json={
            "summary": "Event To Move",
            "start": {
                "dateTime": "2018-06-20T10:00:00-07:00",
                "timeZone": "America/Los_Angeles",
            },
            "end": {
                "dateTime": "2018-06-20T11:00:00-07:00",
                "timeZone": "America/Los_Angeles",
            },
        },
    )
    assert create_resp.status_code == 200
    event_id = create_resp.json()["id"]

    with _timed(f"POST events/{event_id}/move") as t:
        resp = await cal_client.post(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events/{event_id}/move",
            params={"destination": HARVEST_CALENDAR_ID},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["kind"] == "calendar#event"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: Multi-step flows mimicking real bench scenarios
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_bench_flow_list_calendars_then_create_and_event(cal_client: AsyncClient):
    """
    Mimics bench test_1: List calendars, create a new one, add an event to it.
    Measures the combined latency of a typical 3-step agent operation.
    """
    with _timed("FLOW: list calendars + create + event") as t_total:
        # Step 1: List calendars
        with _timed("  step1: calendarList.list") as t1:
            list_resp = await cal_client.get("/users/me/calendarList")
        assert list_resp.status_code == 200

        # Step 2: Create new calendar
        with _timed("  step2: calendars.insert") as t2:
            create_resp = await cal_client.post(
                "/calendars",
                json={"summary": "Flow Test Calendar"},
            )
        assert create_resp.status_code == 200
        new_cal_id = create_resp.json()["id"]

        # Step 3: Create event on new calendar
        with _timed("  step3: events.insert") as t3:
            event_resp = await cal_client.post(
                f"/calendars/{new_cal_id}/events",
                json={
                    "summary": "Test Event",
                    "start": {
                        "dateTime": "2018-06-20T10:00:00Z",
                        "timeZone": "UTC",
                    },
                    "end": {
                        "dateTime": "2018-06-20T11:00:00Z",
                        "timeZone": "UTC",
                    },
                },
            )
        assert event_resp.status_code == 200

    logger.info(
        f"  FLOW total={t_total.elapsed_ms:.0f}ms "
        f"(list={t1.elapsed_ms:.0f}ms + create_cal={t2.elapsed_ms:.0f}ms "
        f"+ create_event={t3.elapsed_ms:.0f}ms)"
    )
    assert t_total.elapsed_ms < 15000


@pytest.mark.asyncio
async def test_bench_flow_freebusy_then_create_event(cal_client: AsyncClient):
    """
    Mimics bench test_1/test_2: Check free/busy, then create event at free time.
    This is the most common 2-step pattern in the calendar bench.
    """
    with _timed("FLOW: freeBusy + create event") as t_total:
        # Step 1: Check free/busy
        with _timed("  step1: freeBusy.query") as t1:
            fb_resp = await cal_client.post(
                "/freeBusy",
                json={
                    "timeMin": "2018-06-23T00:00:00Z",
                    "timeMax": "2018-06-24T00:00:00Z",
                    "items": [{"id": "oleksandra@test.com"}],
                },
            )
        assert fb_resp.status_code == 200

        # Step 2: Create event
        with _timed("  step2: events.insert") as t2:
            event_resp = await cal_client.post(
                f"/calendars/{PRIMARY_CALENDAR_ID}/events",
                json={
                    "summary": "Telescope Alignment",
                    "start": {
                        "dateTime": "2018-06-23T19:30:00+03:00",
                        "timeZone": "Europe/Kyiv",
                    },
                    "end": {
                        "dateTime": "2018-06-23T21:00:00+03:00",
                        "timeZone": "Europe/Kyiv",
                    },
                },
            )
        assert event_resp.status_code == 200

    logger.info(
        f"  FLOW total={t_total.elapsed_ms:.0f}ms "
        f"(freeBusy={t1.elapsed_ms:.0f}ms + create={t2.elapsed_ms:.0f}ms)"
    )
    assert t_total.elapsed_ms < 10000


@pytest.mark.asyncio
async def test_bench_flow_search_patch_delete(cal_client: AsyncClient):
    """
    Mimics bench test_2: List events (search), patch one, delete another.
    """
    with _timed("FLOW: search + patch + delete") as t_total:
        # Step 1: Search events on harvest calendar
        with _timed("  step1: events.list (search)") as t1:
            list_resp = await cal_client.get(
                f"/calendars/{HARVEST_CALENDAR_ID}/events",
                params={"q": "Weed", "timeMin": "2017-01-01T00:00:00Z"},
            )
        assert list_resp.status_code == 200
        items = list_resp.json().get("items", [])

        # Step 2: Patch the failed rocket event (different calendar)
        with _timed("  step2: events.patch") as t2:
            patch_resp = await cal_client.patch(
                f"/calendars/{PRIMARY_CALENDAR_ID}/events/{EVENT_FAILED_ROCKET_ID}",
                json={"location": "Cape Canaveral"},
            )
        assert patch_resp.status_code == 200

        # Step 3: Create then delete a throwaway event (don't mutate seed data)
        tmp_resp = await cal_client.post(
            f"/calendars/{HARVEST_CALENDAR_ID}/events",
            json={
                "summary": "Throwaway for flow delete",
                "start": {"dateTime": "2018-07-10T09:00:00Z", "timeZone": "UTC"},
                "end": {"dateTime": "2018-07-10T10:00:00Z", "timeZone": "UTC"},
            },
        )
        assert tmp_resp.status_code == 200
        tmp_event_id = tmp_resp.json()["id"]

        with _timed("  step3: events.delete") as t3:
            delete_resp = await cal_client.delete(
                f"/calendars/{HARVEST_CALENDAR_ID}/events/{tmp_event_id}"
            )
        assert delete_resp.status_code in (200, 204)

    logger.info(
        f"  FLOW total={t_total.elapsed_ms:.0f}ms "
        f"(search={t1.elapsed_ms:.0f}ms + patch={t2.elapsed_ms:.0f}ms "
        f"+ delete={t3.elapsed_ms:.0f}ms)"
    )
    assert t_total.elapsed_ms < 10000


@pytest.mark.asyncio
async def test_bench_flow_create_cal_acl_events(cal_client: AsyncClient):
    """
    Mimics bench test_1 full scenario: Create calendar, grant ACL, create event,
    free/busy check, patch event, delete event. A 6-step agent operation.
    """
    with _timed(
        "FLOW: create_cal + acl + create_event + freebusy + patch + delete"
    ) as t_total:
        # Step 1: Create calendar
        with _timed("  step1: calendars.insert"):
            cal_resp = await cal_client.post(
                "/calendars",
                json={"summary": "Full Flow Calendar"},
            )
        assert cal_resp.status_code == 200
        cal_id = cal_resp.json()["id"]

        # Step 2: Grant ACL
        with _timed("  step2: acl.insert"):
            acl_resp = await cal_client.post(
                f"/calendars/{cal_id}/acl",
                json={
                    "role": "writer",
                    "scope": {"type": "user", "value": "yuki@test.com"},
                },
            )
        assert acl_resp.status_code == 200

        # Step 3: Create event
        with _timed("  step3: events.insert"):
            event_resp = await cal_client.post(
                f"/calendars/{cal_id}/events",
                json={
                    "summary": "Watch Party",
                    "start": {
                        "dateTime": "2018-06-24T00:00:00-07:00",
                        "timeZone": "America/Los_Angeles",
                    },
                    "end": {
                        "dateTime": "2018-06-24T03:00:00-07:00",
                        "timeZone": "America/Los_Angeles",
                    },
                },
            )
        assert event_resp.status_code == 200
        event_id = event_resp.json()["id"]

        # Step 4: FreeBusy check
        with _timed("  step4: freeBusy.query"):
            fb_resp = await cal_client.post(
                "/freeBusy",
                json={
                    "timeMin": "2018-06-23T00:00:00Z",
                    "timeMax": "2018-06-25T00:00:00Z",
                    "items": [{"id": "oleksandra@test.com"}],
                },
            )
        assert fb_resp.status_code == 200

        # Step 5: Patch event
        with _timed("  step5: events.patch"):
            patch_resp = await cal_client.patch(
                f"/calendars/{cal_id}/events/{event_id}",
                json={"location": "Hillcrest Observatory Field"},
            )
        assert patch_resp.status_code == 200

        # Step 6: Delete the event we just created
        with _timed("  step6: events.delete"):
            del_resp = await cal_client.delete(f"/calendars/{cal_id}/events/{event_id}")
        assert del_resp.status_code in (200, 204)

    logger.info(f"  FLOW total={t_total.elapsed_ms:.0f}ms")
    assert t_total.elapsed_ms < 20000


# ---------------------------------------------------------------------------
# Test: Repeated event listing (simulates an agent retrying/iterating)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_repeated_event_listings(cal_client: AsyncClient):
    """
    Run 10 sequential event list requests to measure consistency.
    """
    search_terms = [
        "Meeting",
        "Party",
        "Review",
        "Ritual",
        "Workshop",
        "Yoga",
        "Lunch",
        "Shopping",
        "Concert",
        "Festival",
    ]

    times = []
    for term in search_terms:
        with _timed(f"  events search '{term}'") as t:
            resp = await cal_client.get(
                f"/calendars/{PRIMARY_CALENDAR_ID}/events",
                params={"q": term, "timeMin": "2017-01-01T00:00:00Z"},
            )
        assert resp.status_code == 200
        times.append(t.elapsed_ms)

    avg_ms = sum(times) / len(times)
    p50 = sorted(times)[len(times) // 2]
    max_ms = max(times)

    logger.info(
        f"  10 event searches: avg={avg_ms:.0f}ms p50={p50:.0f}ms max={max_ms:.0f}ms"
    )
    assert max_ms < 10000, f"Worst event search took {max_ms:.0f}ms (>10s)"


# ---------------------------------------------------------------------------
# Tests: Parallel requests (4 concurrent) — simulates real agent bench load
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_parallel_4_event_listings(cal_client: AsyncClient):
    """
    Fire 4 event list requests in parallel and measure wall-clock time.
    """
    calendars = [
        PRIMARY_CALENDAR_ID,
        HARVEST_CALENDAR_ID,
        DUNGEON_MASTERS_CALENDAR_ID,
        TIMELINE_ALPHA_CALENDAR_ID,
    ]

    async def do_list(cal_id: str) -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await cal_client.get(
            f"/calendars/{cal_id}/events",
            params={"timeMin": "2018-01-01T00:00:00Z"},
        )
        elapsed = (time.perf_counter() - t0) * 1000
        return cal_id, elapsed, resp.status_code

    with _timed("PARALLEL: 4 event listings") as wall:
        results = await asyncio.gather(*(do_list(c) for c in calendars))

    for cal_id, ms, code in results:
        logger.info(f"  parallel events.list '{cal_id}': {ms:.0f}ms status={code}")
        assert code == 200

    max_individual = max(ms for _, ms, _ in results)
    logger.info(
        f"  wall_clock={wall.elapsed_ms:.0f}ms  max_individual={max_individual:.0f}ms"
    )
    assert wall.elapsed_ms < 10000, (
        f"4 parallel event listings took {wall.elapsed_ms:.0f}ms wall-clock (>10s)"
    )


@pytest.mark.asyncio
async def test_parallel_4_mixed_operations(cal_client: AsyncClient):
    """
    Fire 4 different operation types in parallel — calendarList, events.list,
    freeBusy, colors — simulating a realistic agent burst.
    """

    async def list_calendars() -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await cal_client.get("/users/me/calendarList")
        return "calendarList", (time.perf_counter() - t0) * 1000, resp.status_code

    async def list_events() -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await cal_client.get(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events",
            params={"timeMin": "2018-06-01T00:00:00Z"},
        )
        return "events.list", (time.perf_counter() - t0) * 1000, resp.status_code

    async def freebusy() -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await cal_client.post(
            "/freeBusy",
            json={
                "timeMin": "2018-06-23T00:00:00Z",
                "timeMax": "2018-06-24T00:00:00Z",
                "items": [{"id": "kenji@test.com"}],
            },
        )
        return "freeBusy", (time.perf_counter() - t0) * 1000, resp.status_code

    async def colors() -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await cal_client.get("/colors")
        return "colors", (time.perf_counter() - t0) * 1000, resp.status_code

    with _timed("PARALLEL: 4 mixed ops") as wall:
        results = await asyncio.gather(
            list_calendars(), list_events(), freebusy(), colors()
        )

    for op, ms, code in results:
        logger.info(f"  parallel {op}: {ms:.0f}ms status={code}")
        assert code == 200

    max_individual = max(ms for _, ms, _ in results)
    logger.info(
        f"  wall_clock={wall.elapsed_ms:.0f}ms  max_individual={max_individual:.0f}ms"
    )
    assert wall.elapsed_ms < 10000, (
        f"4 parallel mixed ops took {wall.elapsed_ms:.0f}ms wall-clock (>10s)"
    )


@pytest.mark.asyncio
async def test_parallel_4_writes(cal_client: AsyncClient):
    """
    Fire 4 write operations in parallel — create events simultaneously.
    Tests DB write contention under concurrent load.
    """

    async def create_event(name: str) -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await cal_client.post(
            f"/calendars/{PRIMARY_CALENDAR_ID}/events",
            json={
                "summary": name,
                "start": {
                    "dateTime": "2018-07-01T10:00:00-07:00",
                    "timeZone": "America/Los_Angeles",
                },
                "end": {
                    "dateTime": "2018-07-01T11:00:00-07:00",
                    "timeZone": "America/Los_Angeles",
                },
            },
        )
        return name, (time.perf_counter() - t0) * 1000, resp.status_code

    names = ["Parallel_A", "Parallel_B", "Parallel_C", "Parallel_D"]

    with _timed("PARALLEL: 4 event creates") as wall:
        results = await asyncio.gather(*(create_event(n) for n in names))

    for name, ms, code in results:
        logger.info(f"  parallel POST events '{name}': {ms:.0f}ms status={code}")
        assert code == 200

    max_individual = max(ms for _, ms, _ in results)
    logger.info(
        f"  wall_clock={wall.elapsed_ms:.0f}ms  max_individual={max_individual:.0f}ms"
    )
    assert wall.elapsed_ms < 10000, (
        f"4 parallel event creates took {wall.elapsed_ms:.0f}ms wall-clock (>10s)"
    )


@pytest.mark.asyncio
async def test_parallel_4_freebusy_queries(cal_client: AsyncClient):
    """
    Fire 4 free/busy queries in parallel with different calendars.
    FreeBusy is one of the most common calendar bench operations.
    """

    async def do_freebusy(email: str) -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await cal_client.post(
            "/freeBusy",
            json={
                "timeMin": "2018-06-18T00:00:00Z",
                "timeMax": "2018-06-25T00:00:00Z",
                "items": [{"id": email}],
            },
        )
        elapsed = (time.perf_counter() - t0) * 1000
        return email, elapsed, resp.status_code

    emails = [
        "oleksandra@test.com",
        "kenji@test.com",
        "amara@test.com",
        "takeshi@test.com",
    ]

    with _timed("PARALLEL: 4 freeBusy queries") as wall:
        results = await asyncio.gather(*(do_freebusy(e) for e in emails))

    for email, ms, code in results:
        logger.info(f"  parallel freeBusy '{email}': {ms:.0f}ms status={code}")
        assert code == 200

    max_individual = max(ms for _, ms, _ in results)
    logger.info(
        f"  wall_clock={wall.elapsed_ms:.0f}ms  max_individual={max_individual:.0f}ms"
    )
    assert wall.elapsed_ms < 10000, (
        f"4 parallel freeBusy queries took {wall.elapsed_ms:.0f}ms wall-clock (>10s)"
    )
