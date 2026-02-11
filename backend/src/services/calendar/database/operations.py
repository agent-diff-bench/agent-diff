# Database operations for Google Calendar API Replica
# CRUD operations for all Calendar API resources

import logging
import time
from datetime import datetime, timezone, timedelta
from typing import Any, Optional

logger = logging.getLogger(__name__)
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import select, and_, or_, func, update, delete
from sqlalchemy.exc import IntegrityError

from .schema import (
    User,
    Calendar,
    CalendarListEntry,
    Event,
    EventAttendee,
    EventReminder,
    AclRule,
    Setting,
    Channel,
    SyncToken,
    AccessRole,
    EventStatus,
    AclScopeType,
)
from ..core.utils import (
    generate_event_id,
    generate_calendar_id,
    generate_ical_uid,
    generate_acl_rule_id,
    generate_etag,
    generate_sync_token,
    extract_datetime,
    format_rfc3339,
    parse_rfc3339,
    calendar_now,
    PageToken,
    parse_instance_id,
    parse_original_start_time,
    build_original_start_time,
    format_instance_id,
    expand_recurrence,
)
from ..core.errors import (
    CalendarNotFoundError,
    EventNotFoundError,
    AclNotFoundError,
    SettingNotFoundError,
    ValidationError,
    RequiredFieldError,
    DuplicateError,
    ForbiddenError,
    SyncTokenExpiredError,
)


# ============================================================================
# USER OPERATIONS
# ============================================================================


def create_user(
    session: Session,
    email: str,
    user_id: Optional[str] = None,
    display_name: Optional[str] = None,
    create_primary_calendar: bool = True,
) -> User:
    """Create a new user with optional primary calendar."""
    if user_id is None:
        # Use email as user ID (Google-style)
        user_id = email

    user = User(
        id=user_id,
        email=email,
        display_name=display_name,
    )
    session.add(user)

    if create_primary_calendar:
        # Create primary calendar for user
        calendar = Calendar(
            id=email,  # Primary calendar ID is user's email
            summary=display_name or email,
            owner_id=user_id,
            etag=generate_etag(f"{email}:1"),
        )
        session.add(calendar)

        # Create CalendarListEntry for the primary calendar
        entry = CalendarListEntry(
            id=f"{user_id}:{email}",
            user_id=user_id,
            calendar_id=email,
            access_role=AccessRole.owner,
            primary=True,
            etag=generate_etag(f"{email}:list:1"),
        )
        session.add(entry)

        # Create owner ACL rule (include calendar_id in rule id for uniqueness)
        acl_rule = AclRule(
            id=generate_acl_rule_id("user", email, calendar_id=email),
            calendar_id=email,
            role=AccessRole.owner,
            scope_type=AclScopeType.user,
            scope_value=email,
            etag=generate_etag(f"{email}:acl:1"),
        )
        session.add(acl_rule)

        # Create default settings
        _create_default_settings(session, user_id)

    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise DuplicateError(f"User already exists: {email}")

    return user


def get_user(session: Session, user_id: str) -> Optional[User]:
    """Get a user by ID."""
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return session.execute(select(User).where(User.email == email)).scalar_one_or_none()


def _create_default_settings(session: Session, user_id: str) -> None:
    """Create default settings for a new user."""
    default_settings = {
        "timezone": "UTC",
        "locale": "en",
        "dateFieldOrder": "MDY",
        "format24HourTime": "false",
        "weekStart": "0",  # Sunday
        "defaultEventLength": "60",
        "showDeclinedEvents": "true",
        "hideInvitations": "false",
        "hideWeekends": "false",
        "useKeyboardShortcuts": "true",
        "autoAddHangouts": "true",
        "remindOnRespondedEventsOnly": "false",
    }

    for setting_id, value in default_settings.items():
        setting = Setting(
            user_id=user_id,
            setting_id=setting_id,
            value=value,
            etag=generate_etag(f"{user_id}:{setting_id}:1"),
        )
        session.add(setting)


# ============================================================================
# CALENDAR OPERATIONS
# ============================================================================


def create_calendar(
    session: Session,
    owner_id: str,
    summary: str,
    description: Optional[str] = None,
    location: Optional[str] = None,
    time_zone: Optional[str] = None,
    calendar_id: Optional[str] = None,
) -> Calendar:
    """Create a new secondary calendar."""
    owner = session.get(User, owner_id)
    if owner is None:
        raise ValidationError(f"Owner not found: {owner_id}")

    if calendar_id is None:
        calendar_id = generate_calendar_id(owner.email, is_primary=False)

    calendar = Calendar(
        id=calendar_id,
        summary=summary,
        description=description,
        location=location,
        time_zone=time_zone or "UTC",
        owner_id=owner_id,
        data_owner=owner.email,  # Read-only field for secondary calendars
        etag=generate_etag(f"{calendar_id}:1"),
    )
    session.add(calendar)

    # Create CalendarListEntry for owner
    entry = CalendarListEntry(
        id=f"{owner_id}:{calendar_id}",
        user_id=owner_id,
        calendar_id=calendar_id,
        access_role=AccessRole.owner,
        primary=False,
        etag=generate_etag(f"{calendar_id}:list:1"),
    )
    session.add(entry)

    # Create owner ACL rule
    # Include calendar_id in rule_id to make it unique per calendar
    acl_rule_id = f"{calendar_id}:{generate_acl_rule_id('user', owner.email)}"
    acl_rule = AclRule(
        id=acl_rule_id,
        calendar_id=calendar_id,
        role=AccessRole.owner,
        scope_type=AclScopeType.user,
        scope_value=owner.email,
        etag=generate_etag(f"{calendar_id}:acl:1"),
    )
    session.add(acl_rule)

    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise DuplicateError(f"Calendar already exists: {calendar_id}")

    return calendar


def get_calendar(
    session: Session,
    calendar_id: str,
    user_id: Optional[str] = None,
) -> Calendar:
    """Get a calendar by ID, optionally resolving 'primary'."""
    t_start = time.perf_counter()
    if calendar_id == "primary" and user_id:
        user = session.get(User, user_id)
        if user:
            calendar_id = user.email

    calendar = session.get(Calendar, calendar_id)
    t_ms = (time.perf_counter() - t_start) * 1000
    if t_ms > 10:
        logger.info(f"[PERF] get_calendar({calendar_id}) time={t_ms:.0f}ms")
    if calendar is None or calendar.deleted:
        raise CalendarNotFoundError(calendar_id)

    return calendar


def update_calendar(
    session: Session,
    calendar_id: str,
    user_id: str,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    time_zone: Optional[str] = None,
) -> Calendar:
    """Update a calendar's metadata."""
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar_id, user_id, AccessRole.owner)

    if summary is not None:
        calendar.summary = summary
    if description is not None:
        calendar.description = description
    if location is not None:
        calendar.location = location
    if time_zone is not None:
        calendar.time_zone = time_zone

    calendar.updated_at = calendar_now()
    calendar.etag = generate_etag(f"{calendar_id}:{calendar.updated_at.isoformat()}")

    return calendar


def delete_calendar(
    session: Session,
    calendar_id: str,
    user_id: str,
) -> None:
    """Delete a secondary calendar."""
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar_id, user_id, AccessRole.owner)

    # Check if this is a primary calendar (can't delete primary)
    user = session.get(User, user_id)
    if user and calendar_id == user.email:
        raise ValidationError("Cannot delete primary calendar")

    # Soft delete
    calendar.deleted = True
    calendar.updated_at = calendar_now()


def clear_calendar(
    session: Session,
    calendar_id: str,
    user_id: str,
) -> None:
    """Clear all events from a calendar (primary only)."""
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar_id, user_id, AccessRole.owner)

    # Mark all events as cancelled
    session.execute(
        update(Event)
        .where(Event.calendar_id == calendar.id)
        .values(
            status=EventStatus.cancelled,
            updated_at=calendar_now(),
        )
    )


# ============================================================================
# CALENDAR LIST OPERATIONS
# ============================================================================


def insert_calendar_list_entry(
    session: Session,
    user_id: str,
    calendar_id: str,
    color_id: Optional[str] = None,
    background_color: Optional[str] = None,
    foreground_color: Optional[str] = None,
    hidden: bool = False,
    selected: bool = True,
    default_reminders: Optional[list[dict[str, Any]]] = None,
    notification_settings: Optional[dict[str, Any]] = None,
    summary_override: Optional[str] = None,
) -> CalendarListEntry:
    """Add a calendar to user's calendar list."""
    # Verify calendar exists
    calendar = session.get(Calendar, calendar_id)
    if calendar is None or calendar.deleted:
        raise CalendarNotFoundError(calendar_id)

    # Check if user has read access
    access_role = _get_user_access_role(session, calendar_id, user_id)
    if access_role is None:
        raise ForbiddenError(f"No access to calendar: {calendar_id}")

    # Check if entry already exists
    existing = session.execute(
        select(CalendarListEntry).where(
            and_(
                CalendarListEntry.user_id == user_id,
                CalendarListEntry.calendar_id == calendar_id,
            )
        )
    ).scalar_one_or_none()

    if existing:
        raise DuplicateError("Calendar already in list")

    entry = CalendarListEntry(
        id=f"{user_id}:{calendar_id}",
        user_id=user_id,
        calendar_id=calendar_id,
        access_role=access_role,
        color_id=color_id,
        background_color=background_color,
        foreground_color=foreground_color,
        hidden=hidden,
        selected=selected,
        default_reminders=default_reminders,
        notification_settings=notification_settings,
        summary_override=summary_override,
        primary=False,
        etag=generate_etag(f"{user_id}:{calendar_id}:1"),
    )
    session.add(entry)

    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise DuplicateError("Calendar already in list")

    return entry


def get_calendar_list_entry(
    session: Session,
    user_id: str,
    calendar_id: str,
) -> CalendarListEntry:
    """Get a calendar list entry."""
    if calendar_id == "primary":
        user = session.get(User, user_id)
        if user:
            calendar_id = user.email

    entry = session.execute(
        select(CalendarListEntry).where(
            and_(
                CalendarListEntry.user_id == user_id,
                CalendarListEntry.calendar_id == calendar_id,
                CalendarListEntry.deleted == False,  # noqa: E712
            )
        )
    ).scalar_one_or_none()

    if entry is None:
        raise CalendarNotFoundError(calendar_id)

    return entry


def list_calendar_list_entries(
    session: Session,
    user_id: str,
    max_results: int = 250,
    page_token: Optional[str] = None,
    min_access_role: Optional[str] = None,
    show_deleted: bool = False,
    show_hidden: bool = False,
    sync_token: Optional[str] = None,
) -> tuple[list[CalendarListEntry], Optional[str], Optional[str]]:
    """
    List calendar list entries for a user.

    Returns: (entries, next_page_token, next_sync_token)
    """
    t_start = time.perf_counter()
    # Handle sync token
    if sync_token:
        token_record = session.execute(
            select(SyncToken).where(
                and_(
                    SyncToken.token == sync_token,
                    SyncToken.user_id == user_id,
                    SyncToken.resource_type == "calendarList",
                )
            )
        ).scalar_one_or_none()

        if token_record is None or token_record.expires_at < calendar_now():
            raise SyncTokenExpiredError()

        # Return only items updated since token was created
        query = (
            select(CalendarListEntry)
            .options(joinedload(CalendarListEntry.calendar))
            .where(
                and_(
                    CalendarListEntry.user_id == user_id,
                    CalendarListEntry.updated_at > token_record.snapshot_time,
                )
            )
        )
    else:
        query = (
            select(CalendarListEntry)
            .options(joinedload(CalendarListEntry.calendar))
            .where(CalendarListEntry.user_id == user_id)
        )

    # Apply filters
    if not show_deleted:
        query = query.where(CalendarListEntry.deleted == False)  # noqa: E712
    if not show_hidden:
        query = query.where(CalendarListEntry.hidden == False)  # noqa: E712
    if min_access_role:
        role_order = ["freeBusyReader", "reader", "writer", "owner"]
        # Validate min_access_role before using it
        if min_access_role not in role_order:
            raise ValidationError(
                f"Invalid minAccessRole value: {min_access_role}. "
                f"Must be one of: {', '.join(role_order)}"
            )
        min_idx = role_order.index(min_access_role)
        allowed_roles = role_order[min_idx:]
        query = query.where(
            CalendarListEntry.access_role.in_([AccessRole[r] for r in allowed_roles])
        )

    # Get total count for pagination
    query = query.order_by(CalendarListEntry.id)

    # Apply pagination
    offset = 0
    if page_token:
        offset, _ = PageToken.decode(page_token)
    query = query.offset(offset).limit(max_results + 1)

    entries = list(session.execute(query).unique().scalars().all())

    # Check if there are more results
    next_page_token = None
    if len(entries) > max_results:
        entries = entries[:max_results]
        next_page_token = PageToken.encode(offset + max_results)

    # Generate sync token for next incremental sync
    next_sync_token = None
    if not page_token and not sync_token:
        # Only generate sync token for initial full sync
        next_sync_token = _create_sync_token(session, user_id, "calendarList")

    t_ms = (time.perf_counter() - t_start) * 1000
    if t_ms > 10:
        logger.info(
            f"[PERF] list_calendar_list_entries({user_id}) time={t_ms:.0f}ms "
            f"entries={len(entries)}"
        )
    return entries, next_page_token, next_sync_token


def update_calendar_list_entry(
    session: Session,
    user_id: str,
    calendar_id: str,
    summary_override: Optional[str] = None,
    color_id: Optional[str] = None,
    background_color: Optional[str] = None,
    foreground_color: Optional[str] = None,
    hidden: Optional[bool] = None,
    selected: Optional[bool] = None,
    default_reminders: Optional[list[dict[str, Any]]] = None,
    notification_settings: Optional[dict[str, Any]] = None,
) -> CalendarListEntry:
    """Update a calendar list entry."""
    entry = get_calendar_list_entry(session, user_id, calendar_id)

    if summary_override is not None:
        entry.summary_override = summary_override
    if color_id is not None:
        entry.color_id = color_id
    if background_color is not None:
        entry.background_color = background_color
    if foreground_color is not None:
        entry.foreground_color = foreground_color
    if hidden is not None:
        entry.hidden = hidden
    if selected is not None:
        entry.selected = selected
    if default_reminders is not None:
        entry.default_reminders = default_reminders
    if notification_settings is not None:
        entry.notification_settings = notification_settings

    entry.updated_at = calendar_now()
    entry.etag = generate_etag(f"{entry.id}:{entry.updated_at.isoformat()}")

    return entry


def delete_calendar_list_entry(
    session: Session,
    user_id: str,
    calendar_id: str,
) -> None:
    """Remove a calendar from user's calendar list."""
    entry = get_calendar_list_entry(session, user_id, calendar_id)

    # Can't remove primary calendar
    if entry.primary:
        raise ValidationError("Cannot remove primary calendar from list")

    # Soft delete
    entry.deleted = True
    entry.updated_at = calendar_now()


# ============================================================================
# EVENT OPERATIONS
# ============================================================================


def create_event(
    session: Session,
    calendar_id: str,
    user_id: str,
    start: dict[str, Any],
    end: dict[str, Any],
    summary: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[list[dict[str, Any]]] = None,
    recurrence: Optional[list[str]] = None,
    reminders: Optional[dict[str, Any]] = None,
    event_id: Optional[str] = None,
    ical_uid: Optional[str] = None,
    **kwargs: Any,
) -> Event:
    """Create a new event."""
    t_start_perf = time.perf_counter()
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.writer)

    user = session.get(User, user_id)
    if user is None:
        raise ValidationError(f"User not found: {user_id}")

    # Generate event ID if not provided
    if event_id is None:
        event_id = generate_event_id()

    # Validate event ID format
    from ..core.utils import validate_event_id

    if not validate_event_id(event_id):
        raise ValidationError(f"Invalid event ID format: {event_id}", field="id")

    # Generate iCalUID if not provided
    if ical_uid is None:
        ical_uid = generate_ical_uid(event_id, calendar.id)

    # Extract datetime for indexing
    start_dt = extract_datetime(start)
    end_dt = extract_datetime(end)
    start_date = start.get("date")
    end_date = end.get("date")

    # Extract organizer/creator fields from kwargs to allow override (e.g., for import)
    # Use provided values if present, otherwise default to current user
    # This matches Google Calendar API behavior where imports preserve original organizer
    organizer_email = kwargs.pop("organizer_email", None) or user.email
    organizer_display_name = (
        kwargs.pop("organizer_display_name", None) or user.display_name
    )
    organizer_self = organizer_email == user.email

    event = Event(
        id=event_id,
        calendar_id=calendar.id,
        summary=summary,
        description=description,
        location=location,
        start=start,
        end=end,
        start_datetime=start_dt,
        end_datetime=end_dt,
        start_date=start_date,
        end_date=end_date,
        recurrence=recurrence,
        reminders=reminders,
        ical_uid=ical_uid,
        creator_id=user_id,
        creator_email=user.email,
        creator_display_name=user.display_name,
        creator_self=True,
        organizer_id=user_id,
        organizer_email=organizer_email,
        organizer_display_name=organizer_display_name,
        organizer_self=organizer_self,
        etag=generate_etag(f"{event_id}:1"),
        **{k: v for k, v in kwargs.items() if hasattr(Event, k)},
    )
    session.add(event)

    # Add attendees
    if attendees:
        for idx, attendee_data in enumerate(attendees):
            # Validate email is required for attendees (per Google Calendar API)
            if "email" not in attendee_data or not attendee_data["email"]:
                raise RequiredFieldError(f"attendees[{idx}].email")
            attendee = EventAttendee(
                event_id=event_id,
                email=attendee_data["email"],
                display_name=attendee_data.get("displayName"),
                organizer=attendee_data.get("organizer", False),
                self_=attendee_data.get("email") == user.email,
                optional=attendee_data.get("optional", False),
                response_status=attendee_data.get("responseStatus", "needsAction"),
                comment=attendee_data.get("comment"),
                additional_guests=attendee_data.get("additionalGuests", 0),
            )
            session.add(attendee)

    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise DuplicateError(f"Event already exists: {event_id}")

    t_ms = (time.perf_counter() - t_start_perf) * 1000
    if t_ms > 10:
        logger.info(
            f"[PERF] create_event({calendar_id}, {event_id}) time={t_ms:.0f}ms "
            f"attendees={len(attendees) if attendees else 0}"
        )
    return event


def get_event(
    session: Session,
    calendar_id: str,
    event_id: str,
    user_id: str,
    time_zone: Optional[str] = None,
) -> Event:
    """
    Get an event by ID, including recurring event instances.

    This function handles three cases:
    1. Regular event: Returns the event directly
    2. Persisted exception: Returns the exception event
    3. Virtual instance: Creates and returns a virtual Event object

    Args:
        session: Database session
        calendar_id: Calendar ID
        event_id: Event ID (may be an instance ID like "abc123_20180618T100000Z")
        user_id: User ID for access check
        time_zone: Optional timezone for response formatting

    Returns:
        Event object (may be virtual for recurring instances)

    Raises:
        EventNotFoundError: If event not found or cancelled
    """
    t_start = time.perf_counter()
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.reader)

    # First, try to find the event directly (handles regular events and exceptions)
    event = session.get(Event, event_id)
    if event is not None and event.calendar_id == calendar.id:
        if event.status == EventStatus.cancelled:
            raise EventNotFoundError(event_id)
        t_ms = (time.perf_counter() - t_start) * 1000
        if t_ms > 10:
            logger.info(
                f"[PERF] get_event({calendar_id}, {event_id}) time={t_ms:.0f}ms"
            )
        return event

    # Check if this is a recurring instance ID
    base_id, original_time_str = parse_instance_id(event_id)
    if not original_time_str:
        # Not an instance ID and not found as regular event
        raise EventNotFoundError(event_id)

    # Get the master recurring event
    master = session.get(Event, base_id)
    if master is None or master.calendar_id != calendar.id or not master.recurrence:
        raise EventNotFoundError(event_id)

    if master.status == EventStatus.cancelled:
        raise EventNotFoundError(event_id)

    # Parse the original start time
    original_dt = parse_original_start_time(original_time_str)

    # Check for a cancelled exception for this instance
    cancelled = session.execute(
        select(Event).where(
            and_(
                Event.id == event_id,
                Event.status == EventStatus.cancelled,
            )
        )
    ).scalar_one_or_none()

    if cancelled:
        raise EventNotFoundError(event_id)

    # Verify this instance exists in the recurrence
    time_min = original_dt - timedelta(minutes=1)
    time_max = original_dt + timedelta(minutes=1)

    instance_dates = expand_recurrence(
        recurrence=master.recurrence,
        start=master.start_datetime,
        time_min=time_min,
        time_max=time_max,
        max_instances=10,
    )

    # Check if the original_dt is in the expanded instances
    instance_found = False
    for inst_dt in instance_dates:
        # Normalize to UTC for comparison
        if inst_dt.tzinfo is None:
            inst_dt = inst_dt.replace(tzinfo=timezone.utc)
        else:
            inst_dt = inst_dt.astimezone(timezone.utc)

        if abs((inst_dt - original_dt).total_seconds()) < 60:  # Within 1 minute
            instance_found = True
            break

    if not instance_found:
        raise EventNotFoundError(event_id)

    # Create virtual instance with attendees inherited from master
    t_ms = (time.perf_counter() - t_start) * 1000
    if t_ms > 10:
        logger.info(
            f"[PERF] get_event({calendar_id}, {event_id}) time={t_ms:.0f}ms "
            f"(virtual instance)"
        )
    return _create_virtual_instance(master, original_dt, event_id, master.attendees)


def list_events(
    session: Session,
    calendar_id: str,
    user_id: str,
    max_results: int = 250,
    page_token: Optional[str] = None,
    time_min: Optional[str] = None,
    time_max: Optional[str] = None,
    updated_min: Optional[str] = None,
    single_events: bool = False,
    order_by: Optional[str] = None,
    q: Optional[str] = None,
    show_deleted: bool = False,
    sync_token: Optional[str] = None,
    ical_uid: Optional[str] = None,
    _verified_calendar: Optional[Calendar] = None,
) -> tuple[list[Event], Optional[str], Optional[str]]:
    """
    List events from a calendar.

    Returns: (events, next_page_token, next_sync_token)

    Args:
        _verified_calendar: If the caller has already fetched and verified access
            to the calendar, pass it here to avoid redundant DB lookups.
    """
    t_start = time.perf_counter()
    if _verified_calendar is not None:
        calendar = _verified_calendar
    else:
        calendar = get_calendar(session, calendar_id, user_id)
        _check_calendar_access(session, calendar.id, user_id, AccessRole.reader)

    # Handle sync token
    if sync_token:
        token_record = session.execute(
            select(SyncToken).where(
                and_(
                    SyncToken.token == sync_token,
                    SyncToken.user_id == user_id,
                    SyncToken.resource_type == "events",
                    SyncToken.resource_id == calendar.id,
                )
            )
        ).scalar_one_or_none()

        if token_record is None or token_record.expires_at < calendar_now():
            raise SyncTokenExpiredError()

        query = (
            select(Event)
            .options(selectinload(Event.attendees))
            .where(
                and_(
                    Event.calendar_id == calendar.id,
                    Event.updated_at > token_record.snapshot_time,
                )
            )
        )
    else:
        query = (
            select(Event)
            .options(selectinload(Event.attendees))
            .where(Event.calendar_id == calendar.id)
        )

    # Apply filters
    if not show_deleted:
        query = query.where(Event.status != EventStatus.cancelled)

    if time_min:
        from ..core.utils import parse_rfc3339

        min_dt = parse_rfc3339(time_min)
        query = query.where(
            or_(
                Event.end_datetime >= min_dt,
                Event.end_date >= min_dt.strftime("%Y-%m-%d"),
            )
        )

    if time_max:
        from ..core.utils import parse_rfc3339

        max_dt = parse_rfc3339(time_max)
        query = query.where(
            or_(
                Event.start_datetime < max_dt,
                Event.start_date < max_dt.strftime("%Y-%m-%d"),
            )
        )

    if updated_min:
        from ..core.utils import parse_rfc3339

        upd_dt = parse_rfc3339(updated_min)
        query = query.where(Event.updated_at >= upd_dt)

    if ical_uid:
        query = query.where(Event.ical_uid == ical_uid)

    if q:
        # Simple text search in summary, description, location
        search_pattern = f"%{q}%"
        query = query.where(
            or_(
                Event.summary.ilike(search_pattern),
                Event.description.ilike(search_pattern),
                Event.location.ilike(search_pattern),
            )
        )

    # Handle single_events: when true, expand recurring events into instances
    # instead of returning master events
    recurring_masters = []
    if single_events:
        # Derive recurring_query from the already-filtered query so it inherits
        # all filters (q, updated_min, ical_uid, time bounds, etc.)
        # Add the recurrence predicate to get only recurring masters
        recurring_query = query.where(Event.recurrence != None)  # noqa: E711
        recurring_masters = list(session.execute(recurring_query).scalars().all())

        # Exclude recurring masters from main query (we'll merge expanded instances)
        query = query.where(Event.recurrence == None)  # noqa: E711

    # Apply ordering
    if order_by == "startTime":
        query = query.order_by(Event.start_datetime.asc(), Event.id.asc())
    elif order_by == "updated":
        query = query.order_by(Event.updated_at.desc(), Event.id.asc())
    else:
        query = query.order_by(Event.start_datetime.asc(), Event.id.asc())

    # For single_events with recurring masters, we need different pagination handling
    if single_events and recurring_masters:
        from ..core.utils import expand_recurrence, format_rfc3339, parse_rfc3339
        from datetime import timedelta

        # Parse page_token offset BEFORE expansion so we know how many instances to generate
        offset = 0
        if page_token:
            offset, _ = PageToken.decode(page_token)

        # Calculate how many instances we need: offset + max_results + 1 (for next page check)
        instances_needed = offset + max_results + 1

        # Get all non-recurring events first (no pagination yet)
        all_events = list(session.execute(query).scalars().all())

        # Determine time bounds for expansion
        now = calendar_now()
        min_dt = parse_rfc3339(time_min) if time_min else now - timedelta(days=30)
        max_dt = parse_rfc3339(time_max) if time_max else now + timedelta(days=365)

        # Ensure timezone-aware
        if min_dt.tzinfo is None:
            min_dt = min_dt.replace(tzinfo=timezone.utc)
        if max_dt.tzinfo is None:
            max_dt = max_dt.replace(tzinfo=timezone.utc)

        # Expand each recurring master into instances
        for master in recurring_masters:
            if not master.start_datetime or not master.recurrence:
                continue

            start_dt = master.start_datetime
            if start_dt.tzinfo is None:
                start_dt = start_dt.replace(tzinfo=timezone.utc)

            # Calculate duration
            duration = timedelta(hours=1)
            if master.end_datetime and master.start_datetime:
                duration = master.end_datetime - master.start_datetime

            # Get all exceptions for this master event
            exceptions_query = (
                select(Event)
                .options(selectinload(Event.attendees))
                .where(Event.recurring_event_id == master.id)
            )
            exceptions = list(session.execute(exceptions_query).scalars().all())

            # Build a set of exception original start times (for excluding from virtual instances)
            exception_times: set[str] = set()
            for exc in exceptions:
                if exc.original_start_time and exc.original_start_time.get("dateTime"):
                    # Store the time string for comparison
                    exc_dt = parse_rfc3339(exc.original_start_time["dateTime"])
                    if exc_dt.tzinfo is None:
                        exc_dt = exc_dt.replace(tzinfo=timezone.utc)
                    exception_times.add(exc_dt.strftime("%Y%m%dT%H%M%SZ"))

            # Add exception events to results (modified or cancelled if show_deleted)
            for exc in exceptions:
                if exc.status == EventStatus.cancelled and not show_deleted:
                    continue
                # Check if exception is in time range
                if exc.start_datetime:
                    exc_start = exc.start_datetime
                    if exc_start.tzinfo is None:
                        exc_start = exc_start.replace(tzinfo=timezone.utc)
                    if exc_start >= min_dt and exc_start < max_dt:
                        all_events.append(exc)

            try:
                instance_dates = expand_recurrence(
                    recurrence=master.recurrence,
                    start=start_dt,
                    time_min=min_dt,
                    time_max=max_dt,
                    max_instances=instances_needed,  # Expand enough for pagination
                )
            except Exception as e:
                # Log and skip if recurrence expansion fails
                # Keep broad exception to maintain graceful degradation (matching Google's behavior)
                logger.warning(
                    "Failed to expand recurrence for event %s: %s", master.id, e
                )
                continue

            # Get master's attendees for copying to virtual instances
            master_attendees = master.attendees

            # Create instance objects (excluding those with exceptions)
            for inst_start in instance_dates:
                # Normalize inst_start to UTC
                if inst_start.tzinfo is None:
                    inst_start = inst_start.replace(tzinfo=timezone.utc)

                # Skip if there's an exception for this instance
                inst_time_str = inst_start.strftime("%Y%m%dT%H%M%SZ")
                if inst_time_str in exception_times:
                    continue

                inst_end = inst_start + duration
                instance_id = f"{master.id}_{inst_time_str}"
                instance = Event(
                    id=instance_id,
                    calendar_id=master.calendar_id,
                    ical_uid=master.ical_uid,
                    summary=master.summary,
                    description=master.description,
                    location=master.location,
                    color_id=master.color_id,
                    status=master.status,
                    visibility=master.visibility,
                    transparency=master.transparency,
                    creator_email=master.creator_email,
                    creator_display_name=master.creator_display_name,
                    creator_profile_id=master.creator_profile_id,
                    creator_self=master.creator_self,
                    organizer_email=master.organizer_email,
                    organizer_display_name=master.organizer_display_name,
                    organizer_profile_id=master.organizer_profile_id,
                    organizer_self=master.organizer_self,
                    start={
                        "dateTime": format_rfc3339(inst_start),
                        "timeZone": master.start.get("timeZone", "UTC"),
                    },
                    end={
                        "dateTime": format_rfc3339(inst_end),
                        "timeZone": master.end.get("timeZone", "UTC"),
                    },
                    start_datetime=inst_start,
                    end_datetime=inst_end,
                    recurring_event_id=master.id,
                    original_start_time={
                        "dateTime": format_rfc3339(inst_start),
                        "timeZone": master.start.get("timeZone", "UTC"),
                    },
                    sequence=master.sequence,
                    etag=generate_etag(f"{master.id}:{inst_start.isoformat()}"),
                    html_link=master.html_link,
                    guests_can_modify=master.guests_can_modify,
                    guests_can_invite_others=master.guests_can_invite_others,
                    guests_can_see_other_guests=master.guests_can_see_other_guests,
                    anyone_can_add_self=master.anyone_can_add_self,
                    private_copy=master.private_copy,
                    locked=master.locked,
                    reminders=master.reminders,
                    event_type=master.event_type,
                    created_at=master.created_at,
                    updated_at=master.updated_at,
                )

                # Copy attendees from master to virtual instance
                for att in master_attendees:
                    virtual_attendee = EventAttendee(
                        event_id=instance_id,
                        email=att.email,
                        display_name=att.display_name,
                        organizer=att.organizer,
                        self_=att.self_,
                        optional=att.optional,
                        response_status=att.response_status,
                        comment=att.comment,
                        additional_guests=att.additional_guests,
                    )
                    instance.attendees.append(virtual_attendee)

                all_events.append(instance)

        # Helper to normalize datetime to timezone-aware for comparison
        def _normalize_dt(dt: Optional[datetime]) -> datetime:
            if dt is None:
                return datetime.min.replace(tzinfo=timezone.utc)
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt

        # Sort combined results
        if order_by == "startTime":
            all_events.sort(key=lambda e: (_normalize_dt(e.start_datetime), e.id))
        elif order_by == "updated":
            all_events.sort(
                key=lambda e: (_normalize_dt(e.updated_at), e.id), reverse=True
            )
        else:
            all_events.sort(key=lambda e: (_normalize_dt(e.start_datetime), e.id))

        # Apply pagination to combined results (offset already decoded above)
        paginated_events = all_events[offset : offset + max_results + 1]

        next_page_token = None
        if len(paginated_events) > max_results:
            paginated_events = paginated_events[:max_results]
            next_page_token = PageToken.encode(offset + max_results)

        events = paginated_events
    else:
        # Standard pagination for non-single_events queries
        offset = 0
        if page_token:
            offset, _ = PageToken.decode(page_token)
        query = query.offset(offset).limit(max_results + 1)

        events = list(session.execute(query).scalars().all())

        # Check if there are more results
        next_page_token = None
        if len(events) > max_results:
            events = events[:max_results]
            next_page_token = PageToken.encode(offset + max_results)

    # Generate sync token
    next_sync_token = None
    if not page_token and not sync_token:
        next_sync_token = _create_sync_token(
            session, user_id, "events", resource_id=calendar.id
        )

    t_ms = (time.perf_counter() - t_start) * 1000
    if t_ms > 10:
        logger.info(
            f"[PERF] list_events({calendar_id}) time={t_ms:.0f}ms "
            f"events={len(events)} single_events={single_events} q={q!r}"
        )
    return events, next_page_token, next_sync_token


def update_event(
    session: Session,
    calendar_id: str,
    event_id: str,
    user_id: str,
    **kwargs: Any,
) -> Event:
    """Full update of an event (PUT semantics)."""
    event = get_event(session, calendar_id, event_id, user_id)
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.writer)

    # Update start/end
    if "start" in kwargs:
        event.start = kwargs["start"]
        event.start_datetime = extract_datetime(kwargs["start"])
        event.start_date = kwargs["start"].get("date")

    if "end" in kwargs:
        event.end = kwargs["end"]
        event.end_datetime = extract_datetime(kwargs["end"])
        event.end_date = kwargs["end"].get("date")

    # Update other fields
    updateable_fields = [
        "summary",
        "description",
        "location",
        "color_id",
        "recurrence",
        "transparency",
        "visibility",
        "status",
        "reminders",
        "guests_can_invite_others",
        "guests_can_modify",
        "guests_can_see_other_guests",
        "conference_data",
        "attachments",
        "extended_properties",
        "source",
    ]

    for field in updateable_fields:
        if field in kwargs and kwargs[field] is not None:
            setattr(event, field, kwargs[field])

    # Handle attendees update
    if "attendees" in kwargs and kwargs["attendees"] is not None:
        # Remove existing attendees
        session.execute(delete(EventAttendee).where(EventAttendee.event_id == event_id))
        # Add new attendees
        user = session.get(User, user_id)
        for idx, attendee_data in enumerate(kwargs["attendees"]):
            # Validate email is required for attendees (per Google Calendar API)
            if "email" not in attendee_data or not attendee_data["email"]:
                raise RequiredFieldError(f"attendees[{idx}].email")
            attendee = EventAttendee(
                event_id=event_id,
                email=attendee_data["email"],
                display_name=attendee_data.get("displayName"),
                organizer=attendee_data.get("organizer", False),
                self_=attendee_data.get("email") == (user.email if user else ""),
                optional=attendee_data.get("optional", False),
                response_status=attendee_data.get("responseStatus", "needsAction"),
            )
            session.add(attendee)

    event.sequence += 1
    event.updated_at = calendar_now()
    event.etag = generate_etag(f"{event_id}:{event.sequence}")

    return event


def patch_event(
    session: Session,
    calendar_id: str,
    event_id: str,
    user_id: str,
    **kwargs: Any,
) -> Event:
    """Partial update of an event (PATCH semantics)."""
    # PATCH is the same as PUT but only updates provided fields
    return update_event(session, calendar_id, event_id, user_id, **kwargs)


def delete_event(
    session: Session,
    calendar_id: str,
    event_id: str,
    user_id: str,
) -> None:
    """Delete (cancel) an event."""
    event = get_event(session, calendar_id, event_id, user_id)
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.writer)

    # Soft delete - mark as cancelled
    event.status = EventStatus.cancelled
    event.updated_at = calendar_now()
    event.etag = generate_etag(f"{event_id}:cancelled")


# ============================================================================
# RECURRING EVENT INSTANCE OPERATIONS
# ============================================================================


def _create_virtual_instance(
    master: Event,
    instance_start: datetime,
    instance_id: str,
    master_attendees: Optional[list[EventAttendee]] = None,
) -> Event:
    """
    Create a virtual (non-persisted) event instance from a recurring master.

    Args:
        master: The master recurring event
        instance_start: Start datetime for this instance
        instance_id: The instance ID (format: master_id_YYYYMMDDTHHMMSSZ)
        master_attendees: Optional list of master event's attendees to copy

    Returns:
        A virtual Event object representing this instance
    """
    # Calculate the duration of the master event
    if master.end_datetime and master.start_datetime:
        duration = master.end_datetime - master.start_datetime
    else:
        duration = timedelta(hours=1)

    instance_end = instance_start + duration

    # Build start/end dicts
    tz = master.start.get("timeZone", "UTC")
    instance_start_dict = {
        "dateTime": format_rfc3339(instance_start),
        "timeZone": tz,
    }
    instance_end_dict = {
        "dateTime": format_rfc3339(instance_end),
        "timeZone": master.end.get("timeZone", tz),
    }

    # Build originalStartTime
    original_start_time = build_original_start_time(instance_start, tz)

    # Create the virtual instance (not added to session)
    instance = Event(
        id=instance_id,
        calendar_id=master.calendar_id,
        recurring_event_id=master.id,
        original_start_time=original_start_time,
        ical_uid=master.ical_uid,
        summary=master.summary,
        description=master.description,
        location=master.location,
        start=instance_start_dict,
        end=instance_end_dict,
        start_datetime=instance_start,
        end_datetime=instance_end,
        creator_id=master.creator_id,
        creator_email=master.creator_email,
        creator_display_name=master.creator_display_name,
        creator_self=master.creator_self,
        organizer_id=master.organizer_id,
        organizer_email=master.organizer_email,
        organizer_display_name=master.organizer_display_name,
        organizer_self=master.organizer_self,
        status=master.status,
        visibility=master.visibility,
        transparency=master.transparency,
        color_id=master.color_id,
        html_link=master.html_link,
        hangout_link=master.hangout_link,
        conference_data=master.conference_data,
        reminders=master.reminders,
        guests_can_invite_others=master.guests_can_invite_others,
        guests_can_modify=master.guests_can_modify,
        guests_can_see_other_guests=master.guests_can_see_other_guests,
        anyone_can_add_self=master.anyone_can_add_self,
        etag=generate_etag(f"{instance_id}:virtual"),
        # Don't copy recurrence - instances don't have recurrence rules
        recurrence=None,
    )

    # Copy attendees from master (create non-persisted copies)
    if master_attendees:
        for att in master_attendees:
            virtual_attendee = EventAttendee(
                event_id=instance_id,
                email=att.email,
                display_name=att.display_name,
                organizer=att.organizer,
                self_=att.self_,
                optional=att.optional,
                response_status=att.response_status,
                comment=att.comment,
                additional_guests=att.additional_guests,
            )
            instance.attendees.append(virtual_attendee)

    return instance


def _get_master_event_for_instance(
    session: Session,
    calendar_id: str,
    instance_id: str,
    user_id: str,
) -> tuple[Optional[Event], Optional[str], Optional[datetime]]:
    """
    Get the master event for a recurring instance.

    Args:
        session: Database session
        calendar_id: Calendar ID
        instance_id: Instance ID (may include time suffix)
        user_id: User ID for access check

    Returns:
        Tuple of (master_event, original_time_str, original_datetime) or (None, None, None)
    """
    base_id, original_time_str = parse_instance_id(instance_id)

    if not original_time_str:
        return None, None, None

    # Get the master event
    master = session.get(Event, base_id)
    if master is None or master.calendar_id != calendar_id:
        return None, None, None

    if not master.recurrence:
        return None, None, None

    original_dt = parse_original_start_time(original_time_str)
    return master, original_time_str, original_dt


def update_recurring_instance(
    session: Session,
    calendar_id: str,
    instance_id: str,
    user_id: str,
    user_email: str,
    **kwargs: Any,
) -> Event:
    """
    Update a single instance of a recurring event.

    Creates a persisted exception event with the modifications.
    If an exception already exists for this instance, updates it.

    Args:
        session: Database session
        calendar_id: Calendar ID
        instance_id: Instance ID (format: master_id_YYYYMMDDTHHMMSSZ)
        user_id: User ID
        user_email: User's email address
        **kwargs: Fields to update

    Returns:
        The created/updated exception event
    """
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.writer)

    # Check if an exception already exists
    existing = session.get(Event, instance_id)
    if existing and existing.calendar_id == calendar.id:
        # Update existing exception
        return update_event(session, calendar_id, instance_id, user_id, **kwargs)

    # Get master event info
    master, original_time_str, original_dt = _get_master_event_for_instance(
        session, calendar.id, instance_id, user_id
    )

    if not master or not original_dt:
        raise EventNotFoundError(instance_id)

    # Validate that this instance date is valid for the recurrence
    # (not excluded by EXDATE and within the recurrence pattern)
    time_min = original_dt - timedelta(minutes=1)
    time_max = original_dt + timedelta(minutes=1)

    instance_dates = expand_recurrence(
        recurrence=master.recurrence,
        start=master.start_datetime,
        time_min=time_min,
        time_max=time_max,
        max_instances=10,
    )

    # Check if the original_dt is in the expanded instances
    instance_found = False
    for inst_dt in instance_dates:
        # Normalize to UTC for comparison
        if inst_dt.tzinfo is None:
            inst_dt = inst_dt.replace(tzinfo=timezone.utc)
        else:
            inst_dt = inst_dt.astimezone(timezone.utc)

        if abs((inst_dt - original_dt).total_seconds()) < 60:  # Within 1 minute
            instance_found = True
            break

    if not instance_found:
        raise EventNotFoundError(instance_id)

    # Calculate default start/end for this instance
    duration = timedelta(hours=1)
    if master.end_datetime and master.start_datetime:
        duration = master.end_datetime - master.start_datetime

    tz = master.start.get("timeZone", "UTC")

    # Use provided start/end or calculate from original
    new_start = kwargs.get(
        "start",
        {
            "dateTime": format_rfc3339(original_dt),
            "timeZone": tz,
        },
    )
    new_end = kwargs.get(
        "end",
        {
            "dateTime": format_rfc3339(original_dt + duration),
            "timeZone": master.end.get("timeZone", tz),
        },
    )

    # Build originalStartTime
    original_start_time = build_original_start_time(original_dt, tz)

    # Get user for creator info
    user = session.get(User, user_id)

    # Create exception event
    exception = Event(
        id=instance_id,
        calendar_id=calendar.id,
        recurring_event_id=master.id,
        original_start_time=original_start_time,
        ical_uid=master.ical_uid,
        # Take from kwargs or inherit from master
        summary=kwargs.get("summary", master.summary),
        description=kwargs.get("description", master.description),
        location=kwargs.get("location", master.location),
        start=new_start,
        end=new_end,
        start_datetime=extract_datetime(new_start),
        end_datetime=extract_datetime(new_end),
        # Creator/organizer from master
        creator_id=master.creator_id,
        creator_email=master.creator_email,
        creator_display_name=master.creator_display_name,
        organizer_id=master.organizer_id,
        organizer_email=master.organizer_email,
        organizer_display_name=master.organizer_display_name,
        creator_self=master.creator_email == user_email
        if master.creator_email
        else False,
        organizer_self=master.organizer_email == user_email
        if master.organizer_email
        else False,
        # Status and visibility
        status=EventStatus.confirmed,
        visibility=kwargs.get("visibility", master.visibility),
        transparency=kwargs.get("transparency", master.transparency),
        color_id=kwargs.get("color_id", master.color_id),
        # Conference and other fields
        hangout_link=kwargs.get("hangout_link", master.hangout_link),
        conference_data=kwargs.get("conference_data", master.conference_data),
        reminders=kwargs.get("reminders", master.reminders),
        extended_properties=kwargs.get(
            "extended_properties", master.extended_properties
        ),
        # Guest permissions
        guests_can_invite_others=kwargs.get(
            "guests_can_invite_others", master.guests_can_invite_others
        ),
        guests_can_modify=kwargs.get("guests_can_modify", master.guests_can_modify),
        guests_can_see_other_guests=kwargs.get(
            "guests_can_see_other_guests", master.guests_can_see_other_guests
        ),
        anyone_can_add_self=kwargs.get(
            "anyone_can_add_self", master.anyone_can_add_self
        ),
        # Generate etag
        etag=generate_etag(f"{instance_id}:{calendar_now().isoformat()}"),
    )

    session.add(exception)

    # Handle attendees - if provided use them, otherwise inherit from master
    attendees = kwargs.get("attendees")
    if attendees is not None:
        # Attendees explicitly provided (could be empty list to clear attendees)
        for attendee_data in attendees:
            attendee = EventAttendee(
                event_id=instance_id,
                email=attendee_data["email"],
                display_name=attendee_data.get("displayName"),
                organizer=attendee_data.get("organizer", False),
                self_=attendee_data.get("email") == user_email,
                optional=attendee_data.get("optional", False),
                response_status=attendee_data.get("responseStatus", "needsAction"),
                comment=attendee_data.get("comment"),
                additional_guests=attendee_data.get("additionalGuests", 0),
            )
            session.add(attendee)
    else:
        # No attendees provided - inherit from master event
        master_attendees = (
            session.execute(
                select(EventAttendee).where(EventAttendee.event_id == master.id)
            )
            .scalars()
            .all()
        )

        for master_att in master_attendees:
            attendee = EventAttendee(
                event_id=instance_id,
                email=master_att.email,
                display_name=master_att.display_name,
                organizer=master_att.organizer,
                self_=master_att.email == user_email,
                optional=master_att.optional,
                response_status=master_att.response_status,
                comment=master_att.comment,
                additional_guests=master_att.additional_guests,
            )
            session.add(attendee)

    session.flush()
    return exception


def delete_recurring_instance(
    session: Session,
    calendar_id: str,
    instance_id: str,
    user_id: str,
) -> None:
    """
    Delete a single instance of a recurring event.

    Creates a cancelled exception event. If an exception already exists,
    marks it as cancelled.

    Args:
        session: Database session
        calendar_id: Calendar ID
        instance_id: Instance ID (format: master_id_YYYYMMDDTHHMMSSZ)
        user_id: User ID
    """
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.writer)

    # Check if an exception already exists
    existing = session.get(Event, instance_id)
    if existing and existing.calendar_id == calendar.id:
        # Mark existing exception as cancelled
        existing.status = EventStatus.cancelled
        existing.updated_at = calendar_now()
        existing.etag = generate_etag(f"{instance_id}:cancelled")
        return

    # Get master event info
    master, original_time_str, original_dt = _get_master_event_for_instance(
        session, calendar.id, instance_id, user_id
    )

    if not master or not original_dt:
        raise EventNotFoundError(instance_id)

    # Validate that this instance date is valid for the recurrence
    time_min = original_dt - timedelta(minutes=1)
    time_max = original_dt + timedelta(minutes=1)

    instance_dates = expand_recurrence(
        recurrence=master.recurrence,
        start=master.start_datetime,
        time_min=time_min,
        time_max=time_max,
        max_instances=10,
    )

    # Check if the original_dt is in the expanded instances
    instance_found = False
    for inst_dt in instance_dates:
        if inst_dt.tzinfo is None:
            inst_dt = inst_dt.replace(tzinfo=timezone.utc)
        else:
            inst_dt = inst_dt.astimezone(timezone.utc)

        if abs((inst_dt - original_dt).total_seconds()) < 60:
            instance_found = True
            break

    if not instance_found:
        raise EventNotFoundError(instance_id)

    # Calculate default times for this instance
    duration = timedelta(hours=1)
    if master.end_datetime and master.start_datetime:
        duration = master.end_datetime - master.start_datetime

    tz = master.start.get("timeZone", "UTC")

    # Build originalStartTime
    original_start_time = build_original_start_time(original_dt, tz)

    # Create cancelled exception event
    exception = Event(
        id=instance_id,
        calendar_id=calendar.id,
        recurring_event_id=master.id,
        original_start_time=original_start_time,
        ical_uid=master.ical_uid,
        summary=master.summary,
        description=master.description,
        location=master.location,
        start={
            "dateTime": format_rfc3339(original_dt),
            "timeZone": tz,
        },
        end={
            "dateTime": format_rfc3339(original_dt + duration),
            "timeZone": master.end.get("timeZone", tz),
        },
        start_datetime=original_dt,
        end_datetime=original_dt + duration,
        creator_id=master.creator_id,
        creator_email=master.creator_email,
        organizer_id=master.organizer_id,
        organizer_email=master.organizer_email,
        status=EventStatus.cancelled,  # Key difference - cancelled status
        etag=generate_etag(f"{instance_id}:cancelled"),
    )

    session.add(exception)
    session.flush()


def get_or_create_instance(
    session: Session,
    calendar_id: str,
    instance_id: str,
    user_id: str,
) -> Optional[Event]:
    """
    Get an event, including virtual recurring instances.

    This function handles three cases:
    1. Regular event: Returns the event directly
    2. Persisted exception: Returns the exception event
    3. Virtual instance: Creates and returns a virtual Event object

    Args:
        session: Database session
        calendar_id: Calendar ID
        instance_id: Event or instance ID
        user_id: User ID for access check

    Returns:
        Event object (may be virtual for instances) or None if not found
    """
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.reader)

    # First, try to find the event directly (handles regular events and exceptions)
    event = session.get(Event, instance_id)
    if event and event.calendar_id == calendar.id:
        if event.status == EventStatus.cancelled:
            return None
        return event

    # Check if this is an instance ID
    base_id, original_time_str = parse_instance_id(instance_id)
    if not original_time_str:
        # Not an instance ID and not found as regular event
        return None

    # Get the master event
    master = session.get(Event, base_id)
    if not master or master.calendar_id != calendar.id or not master.recurrence:
        return None

    if master.status == EventStatus.cancelled:
        return None

    # Parse the original start time
    original_dt = parse_original_start_time(original_time_str)

    # Verify this date is valid for the recurrence (not excluded)
    # Check for a cancelled exception
    cancelled = session.execute(
        select(Event).where(
            and_(
                Event.id == instance_id,
                Event.status == EventStatus.cancelled,
            )
        )
    ).scalar_one_or_none()

    if cancelled:
        return None

    # Expand recurrence to verify this instance exists
    time_min = original_dt - timedelta(minutes=1)
    time_max = original_dt + timedelta(minutes=1)

    instance_dates = expand_recurrence(
        recurrence=master.recurrence,
        start=master.start_datetime,
        time_min=time_min,
        time_max=time_max,
        max_instances=10,
    )

    # Check if the original_dt is in the expanded instances
    instance_found = False
    for inst_dt in instance_dates:
        # Normalize to UTC for comparison
        if inst_dt.tzinfo is None:
            inst_dt = inst_dt.replace(tzinfo=timezone.utc)
        else:
            inst_dt = inst_dt.astimezone(timezone.utc)

        if abs((inst_dt - original_dt).total_seconds()) < 60:  # Within 1 minute
            instance_found = True
            break

    if not instance_found:
        return None

    # Create virtual instance with attendees inherited from master
    return _create_virtual_instance(master, original_dt, instance_id, master.attendees)


def import_event(
    session: Session,
    calendar_id: str,
    user_id: str,
    ical_uid: str,
    start: dict[str, Any],
    end: dict[str, Any],
    **kwargs: Any,
) -> Event:
    """Import an event using iCalUID."""
    if not ical_uid:
        raise RequiredFieldError("iCalUID")

    # Check if event with this iCalUID already exists
    calendar = get_calendar(session, calendar_id, user_id)
    existing = session.execute(
        select(Event).where(
            and_(
                Event.calendar_id == calendar.id,
                Event.ical_uid == ical_uid,
            )
        )
    ).scalar_one_or_none()

    if existing:
        # Update existing event
        return update_event(
            session,
            calendar_id,
            existing.id,
            user_id,
            start=start,
            end=end,
            **kwargs,
        )

    # Create new event
    return create_event(
        session,
        calendar_id,
        user_id,
        start=start,
        end=end,
        ical_uid=ical_uid,
        **kwargs,
    )


def move_event(
    session: Session,
    source_calendar_id: str,
    event_id: str,
    destination_calendar_id: str,
    user_id: str,
) -> Event:
    """Move an event to another calendar."""
    event = get_event(session, source_calendar_id, event_id, user_id)
    source_calendar = get_calendar(session, source_calendar_id, user_id)
    dest_calendar = get_calendar(session, destination_calendar_id, user_id)

    # Check access to both calendars
    _check_calendar_access(session, source_calendar.id, user_id, AccessRole.writer)
    _check_calendar_access(session, dest_calendar.id, user_id, AccessRole.writer)

    # Move the event
    event.calendar_id = dest_calendar.id
    event.updated_at = calendar_now()
    event.etag = generate_etag(f"{event_id}:moved:{dest_calendar.id}")

    return event


def quick_add_event(
    session: Session,
    calendar_id: str,
    user_id: str,
    user_email: str,
    text: str,
) -> Event:
    """
    Create an event from quick add text.

    This is a simplified implementation - real Google Calendar uses NLP.
    Format expected: "Meeting tomorrow at 3pm"
    """
    from dateutil import parser as date_parser
    from zoneinfo import ZoneInfo
    import re

    # Try to parse the text - simplified implementation
    summary = text
    now = calendar_now()
    calendar = get_calendar(session, calendar_id, user_id)
    tz_name = calendar.time_zone or "UTC"
    try:
        tzinfo = ZoneInfo(tz_name)
    except Exception:
        tzinfo = timezone.utc
        tz_name = "UTC"
    now_local = now.astimezone(tzinfo)

    # Default to 1 hour meeting starting now
    start_dt = now_local + timedelta(hours=1)
    duration = timedelta(hours=1)

    def _extract_duration(raw_text: str) -> tuple[str, timedelta]:
        pattern = re.compile(
            r"\bfor\s+(\d+(?:\.\d+)?)\s*(minutes?|mins?|hours?|hrs?)\b",
            re.IGNORECASE,
        )
        match = pattern.search(raw_text)
        if not match:
            return raw_text, timedelta(hours=1)
        value = float(match.group(1))
        unit = match.group(2).lower()
        if unit.startswith("hour") or unit.startswith("hr"):
            delta = timedelta(hours=value)
        else:
            delta = timedelta(minutes=value)
        cleaned = pattern.sub("", raw_text).strip()
        return cleaned, delta

    def _has_explicit_date(text_value: str) -> bool:
        return bool(
            re.search(
                r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}(?:,\s*\d{4})?|\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b",
                text_value,
            )
        )

    def _has_explicit_time(text_value: str) -> bool:
        return bool(
            re.search(
                r"\b\d{1,2}(?::\d{2})?\s*(am|pm)\b|\b\d{1,2}:\d{2}\b",
                text_value,
            )
        )

    def _extract_time(text_value: str) -> tuple[int, int] | None:
        match = re.search(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b", text_value)
        if not match:
            return None
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        meridiem = match.group(3).lower()
        if meridiem == "pm" and hour != 12:
            hour += 12
        if meridiem == "am" and hour == 12:
            hour = 0
        return hour, minute

    # Try to find time references (very simplified)
    text_lower = text.lower()
    cleaned_text, duration = _extract_duration(text)
    explicit_date = _has_explicit_date(text_lower)
    explicit_time = _has_explicit_time(text_lower)

    if ("tomorrow" in text_lower or "today" in text_lower) and not explicit_date:
        base_date = now_local.date()
        if "tomorrow" in text_lower:
            base_date = (now_local + timedelta(days=1)).date()
        time_parts = _extract_time(text_lower)
        if time_parts:
            hour, minute = time_parts
            start_dt = datetime(
                base_date.year,
                base_date.month,
                base_date.day,
                hour,
                minute,
                tzinfo=tzinfo,
            )
        elif "tomorrow" in text_lower:
            start_dt = datetime(
                base_date.year,
                base_date.month,
                base_date.day,
                9,
                0,
                tzinfo=tzinfo,
            )
        else:
            start_dt = now_local.replace(minute=0, second=0, microsecond=0) + timedelta(
                hours=1
            )
    elif explicit_date or explicit_time:
        try:
            parsed_dt = date_parser.parse(cleaned_text, fuzzy=True, default=now_local)
            if parsed_dt.tzinfo is None:
                parsed_dt = parsed_dt.replace(tzinfo=tzinfo)
            else:
                parsed_dt = parsed_dt.astimezone(tzinfo)
            start_dt = parsed_dt
        except ValueError, TypeError:
            start_dt = now_local.replace(minute=0, second=0, microsecond=0) + timedelta(
                hours=1
            )
    else:
        start_dt = now_local.replace(minute=0, second=0, microsecond=0) + timedelta(
            hours=1
        )

    end_dt = start_dt + duration

    start = {"dateTime": format_rfc3339(start_dt), "timeZone": tz_name}
    end = {"dateTime": format_rfc3339(end_dt), "timeZone": tz_name}

    return create_event(
        session,
        calendar_id,
        user_id,
        user_email=user_email,
        summary=summary,
        start=start,
        end=end,
    )


def get_event_instances(
    session: Session,
    calendar_id: str,
    event_id: str,
    user_id: str,
    max_results: int = 250,
    time_min: Optional[str] = None,
    time_max: Optional[str] = None,
    show_deleted: bool = False,
    original_start: Optional[str] = None,
) -> tuple[list[Event], Optional[str], Optional[str]]:
    """
    Get instances of a recurring event.

    Returns a tuple of (instances, next_page_token, next_sync_token).
    Each instance has recurringEventId and originalStartTime set.

    This function merges:
    - Virtual instances expanded from recurrence rules
    - Persisted exception events (modified instances)
    - Cancelled exceptions (only if show_deleted=True)

    Args:
        original_start: If provided, returns only the instance with this original start time.

    Note: page_token is not used as instances are computed dynamically
    from recurrence rules rather than paginated from stored data.
    """
    from ..core.utils import expand_recurrence, format_rfc3339, parse_rfc3339
    from datetime import datetime, timedelta, timezone

    master = get_event(session, calendar_id, event_id, user_id)

    if not master.recurrence:
        # Not a recurring event - return empty
        return [], None, None

    # Parse time bounds
    now = calendar_now()
    if time_min:
        min_dt = parse_rfc3339(time_min)
    else:
        min_dt = now - timedelta(days=30)  # Default to last 30 days

    if time_max:
        max_dt = parse_rfc3339(time_max)
    else:
        max_dt = now + timedelta(days=365)  # Default to next year

    # Get the master event's start time
    start_dt = master.start_datetime
    if not start_dt:
        # All-day event - use start_date
        return [master], None, None

    # Ensure start_dt is timezone-aware (convert naive to UTC)
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone.utc)

    # Ensure min_dt and max_dt are also timezone-aware
    if min_dt.tzinfo is None:
        min_dt = min_dt.replace(tzinfo=timezone.utc)
    if max_dt.tzinfo is None:
        max_dt = max_dt.replace(tzinfo=timezone.utc)

    # Query for persisted exception events (modified or cancelled instances)
    exceptions_query = select(Event).where(Event.recurring_event_id == master.id)
    exceptions = list(session.execute(exceptions_query).scalars().all())

    # Build a set of exception original start times (to exclude from virtual instances)
    exception_times: set[str] = set()
    for exc in exceptions:
        if exc.original_start_time and exc.original_start_time.get("dateTime"):
            exc_dt = parse_rfc3339(exc.original_start_time["dateTime"])
            if exc_dt.tzinfo is None:
                exc_dt = exc_dt.replace(tzinfo=timezone.utc)
            exception_times.add(exc_dt.strftime("%Y%m%dT%H%M%SZ"))

    # Collect all instances (virtual + exceptions)
    all_instances = []

    # Add exception events to results (if in time range)
    for exc in exceptions:
        # Skip cancelled unless show_deleted is True
        if exc.status == EventStatus.cancelled and not show_deleted:
            continue
        # Check if exception is in time range
        if exc.start_datetime:
            exc_start = exc.start_datetime
            if exc_start.tzinfo is None:
                exc_start = exc_start.replace(tzinfo=timezone.utc)
            if exc_start >= min_dt and exc_start < max_dt:
                all_instances.append(exc)

    # Expand recurrence rules to get instance dates
    try:
        instance_dates = expand_recurrence(
            recurrence=master.recurrence,
            start=start_dt,
            time_min=min_dt,
            time_max=max_dt,
            max_instances=max_results,
        )
    except Exception as e:
        # Log and return empty if recurrence expansion fails
        # Keep broad exception to maintain graceful degradation (matching Google's behavior)
        logger.warning(
            "Failed to expand recurrence for event %s in get_instances: %s",
            master.id,
            e,
        )
        return [], None, None

    # Calculate event duration
    duration = timedelta(hours=1)  # Default
    if master.end_datetime and master.start_datetime:
        duration = master.end_datetime - master.start_datetime

    # Get master's attendees for copying to virtual instances
    master_attendees = master.attendees

    # Create virtual instance objects (excluding those with persisted exceptions)
    for inst_start in instance_dates:
        # Normalize to UTC
        if inst_start.tzinfo is None:
            inst_start = inst_start.replace(tzinfo=timezone.utc)

        # Skip if there's a persisted exception for this instance
        inst_time_str = inst_start.strftime("%Y%m%dT%H%M%SZ")
        if inst_time_str in exception_times:
            continue

        inst_end = inst_start + duration
        instance_id = f"{master.id}_{inst_time_str}"

        # Create virtual instance with inherited attendees
        instance = Event(
            id=instance_id,
            calendar_id=master.calendar_id,
            ical_uid=master.ical_uid,
            summary=master.summary,
            description=master.description,
            location=master.location,
            color_id=master.color_id,
            status=master.status,
            visibility=master.visibility,
            transparency=master.transparency,
            creator_email=master.creator_email,
            creator_display_name=master.creator_display_name,
            creator_profile_id=master.creator_profile_id,
            creator_self=master.creator_self,
            organizer_email=master.organizer_email,
            organizer_display_name=master.organizer_display_name,
            organizer_profile_id=master.organizer_profile_id,
            organizer_self=master.organizer_self,
            start={
                "dateTime": format_rfc3339(inst_start),
                "timeZone": master.start.get("timeZone", "UTC"),
            },
            end={
                "dateTime": format_rfc3339(inst_end),
                "timeZone": master.end.get("timeZone", "UTC"),
            },
            start_datetime=inst_start,
            end_datetime=inst_end,
            recurring_event_id=master.id,
            original_start_time={
                "dateTime": format_rfc3339(inst_start),
                "timeZone": master.start.get("timeZone", "UTC"),
            },
            sequence=master.sequence,
            etag=generate_etag(f"{master.id}:{inst_start.isoformat()}"),
            html_link=master.html_link,
            guests_can_modify=master.guests_can_modify,
            guests_can_invite_others=master.guests_can_invite_others,
            guests_can_see_other_guests=master.guests_can_see_other_guests,
            anyone_can_add_self=master.anyone_can_add_self,
            private_copy=master.private_copy,
            locked=master.locked,
            reminders=master.reminders,
            event_type=master.event_type,
            created_at=master.created_at,
            updated_at=master.updated_at,
        )

        # Copy attendees from master to virtual instance
        for att in master_attendees:
            virtual_attendee = EventAttendee(
                event_id=instance_id,
                email=att.email,
                display_name=att.display_name,
                organizer=att.organizer,
                self_=att.self_,
                optional=att.optional,
                response_status=att.response_status,
                comment=att.comment,
                additional_guests=att.additional_guests,
            )
            instance.attendees.append(virtual_attendee)

        all_instances.append(instance)

    # Filter by original_start if specified
    if original_start:
        target_dt = parse_rfc3339(original_start)
        if target_dt.tzinfo is None:
            target_dt = target_dt.replace(tzinfo=timezone.utc)
        target_str = target_dt.strftime("%Y%m%dT%H%M%SZ")

        filtered_instances = []
        for inst in all_instances:
            if inst.original_start_time and inst.original_start_time.get("dateTime"):
                inst_dt = parse_rfc3339(inst.original_start_time["dateTime"])
                if inst_dt.tzinfo is None:
                    inst_dt = inst_dt.replace(tzinfo=timezone.utc)
                if inst_dt.strftime("%Y%m%dT%H%M%SZ") == target_str:
                    filtered_instances.append(inst)
        all_instances = filtered_instances

    # Sort by start time
    all_instances.sort(
        key=lambda e: (
            e.start_datetime or datetime.min.replace(tzinfo=timezone.utc),
            e.id,
        )
    )

    # Limit to max_results
    if len(all_instances) > max_results:
        all_instances = all_instances[:max_results]

    # Persist sync token for incremental sync support
    sync_token = _create_sync_token(
        session=session,
        user_id=user_id,
        resource_type="event_instances",
        resource_id=event_id,
    )

    return all_instances, None, sync_token


# ============================================================================
# ACL OPERATIONS
# ============================================================================


def create_acl_rule(
    session: Session,
    calendar_id: str,
    user_id: str,
    role: str,
    scope_type: str,
    scope_value: Optional[str] = None,
) -> AclRule:
    """Create an ACL rule on a calendar."""
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.owner)

    # Include calendar_id in rule_id to ensure uniqueness per calendar
    rule_id = generate_acl_rule_id(scope_type, scope_value, calendar_id=calendar.id)

    # Check if rule already exists
    existing = session.get(AclRule, rule_id)
    if existing:
        raise DuplicateError(f"ACL rule already exists: {rule_id}")

    rule = AclRule(
        id=rule_id,
        calendar_id=calendar.id,
        role=AccessRole[role],
        scope_type=AclScopeType[scope_type],
        scope_value=scope_value,
        etag=generate_etag(f"{rule_id}:1"),
    )
    session.add(rule)

    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise DuplicateError(f"ACL rule already exists: {rule_id}")

    return rule


def get_acl_rule(
    session: Session,
    calendar_id: str,
    rule_id: str,
    user_id: str,
) -> AclRule:
    """Get an ACL rule."""
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.owner)

    rule = session.get(AclRule, rule_id)
    if rule is None or rule.calendar_id != calendar.id or rule.deleted:
        raise AclNotFoundError(rule_id)

    return rule


def list_acl_rules(
    session: Session,
    calendar_id: str,
    user_id: str,
    max_results: int = 250,
    page_token: Optional[str] = None,
    show_deleted: bool = False,
    sync_token: Optional[str] = None,
) -> tuple[list[AclRule], Optional[str], Optional[str]]:
    """List ACL rules for a calendar."""
    calendar = get_calendar(session, calendar_id, user_id)
    _check_calendar_access(session, calendar.id, user_id, AccessRole.owner)

    # Handle sync token
    if sync_token:
        token_record = session.execute(
            select(SyncToken).where(
                and_(
                    SyncToken.token == sync_token,
                    SyncToken.user_id == user_id,
                    SyncToken.resource_type == "acl",
                    SyncToken.resource_id == calendar.id,
                )
            )
        ).scalar_one_or_none()

        if token_record is None or token_record.expires_at < calendar_now():
            raise SyncTokenExpiredError()

        query = select(AclRule).where(
            and_(
                AclRule.calendar_id == calendar.id,
                AclRule.updated_at > token_record.snapshot_time,
            )
        )
    else:
        query = select(AclRule).where(AclRule.calendar_id == calendar.id)

    if not show_deleted:
        query = query.where(AclRule.deleted == False)  # noqa: E712

    query = query.order_by(AclRule.id)

    # Apply pagination
    offset = 0
    if page_token:
        offset, _ = PageToken.decode(page_token)
    query = query.offset(offset).limit(max_results + 1)

    rules = list(session.execute(query).scalars().all())

    next_page_token = None
    if len(rules) > max_results:
        rules = rules[:max_results]
        next_page_token = PageToken.encode(offset + max_results)

    next_sync_token = None
    if not page_token and not sync_token:
        next_sync_token = _create_sync_token(
            session, user_id, "acl", resource_id=calendar.id
        )

    return rules, next_page_token, next_sync_token


def update_acl_rule(
    session: Session,
    calendar_id: str,
    rule_id: str,
    user_id: str,
    role: str,
) -> AclRule:
    """Update an ACL rule."""
    rule = get_acl_rule(session, calendar_id, rule_id, user_id)

    rule.role = AccessRole[role]
    rule.updated_at = calendar_now()
    rule.etag = generate_etag(f"{rule_id}:{rule.updated_at.isoformat()}")

    return rule


def delete_acl_rule(
    session: Session,
    calendar_id: str,
    rule_id: str,
    user_id: str,
) -> None:
    """Delete an ACL rule."""
    rule = get_acl_rule(session, calendar_id, rule_id, user_id)

    # Soft delete
    rule.deleted = True
    rule.updated_at = calendar_now()


# ============================================================================
# SETTINGS OPERATIONS
# ============================================================================


def get_setting(
    session: Session,
    user_id: str,
    setting_id: str,
) -> Setting:
    """Get a user setting."""
    setting = session.execute(
        select(Setting).where(
            and_(
                Setting.user_id == user_id,
                Setting.setting_id == setting_id,
            )
        )
    ).scalar_one_or_none()

    if setting is None:
        raise SettingNotFoundError(setting_id)

    return setting


def list_settings(
    session: Session,
    user_id: str,
    max_results: int = 250,
    page_token: Optional[str] = None,
    sync_token: Optional[str] = None,
) -> tuple[list[Setting], Optional[str], Optional[str]]:
    """List all user settings."""
    # Handle sync token
    if sync_token:
        token_record = session.execute(
            select(SyncToken).where(
                and_(
                    SyncToken.token == sync_token,
                    SyncToken.user_id == user_id,
                    SyncToken.resource_type == "settings",
                )
            )
        ).scalar_one_or_none()

        if token_record is None or token_record.expires_at < calendar_now():
            raise SyncTokenExpiredError()

        query = select(Setting).where(Setting.user_id == user_id)
    else:
        query = select(Setting).where(Setting.user_id == user_id)

    query = query.order_by(Setting.setting_id)

    # Apply pagination
    offset = 0
    if page_token:
        offset, _ = PageToken.decode(page_token)
    query = query.offset(offset).limit(max_results + 1)

    settings = list(session.execute(query).scalars().all())

    next_page_token = None
    if len(settings) > max_results:
        settings = settings[:max_results]
        next_page_token = PageToken.encode(offset + max_results)

    next_sync_token = None
    if not page_token and not sync_token:
        next_sync_token = _create_sync_token(session, user_id, "settings")

    return settings, next_page_token, next_sync_token


# ============================================================================
# CHANNEL OPERATIONS
# ============================================================================


def get_channel(
    session: Session,
    channel_id: str,
    resource_id: str,
) -> Optional[Channel]:
    """Get a channel by ID and resource ID."""
    return session.execute(
        select(Channel).where(
            and_(
                Channel.id == channel_id,
                Channel.resource_id == resource_id,
            )
        )
    ).scalar_one_or_none()


def delete_channel(
    session: Session,
    channel_id: str,
    resource_id: str,
) -> bool:
    """Delete (stop) a channel."""
    channel = get_channel(session, channel_id, resource_id)
    if channel is None:
        return False
    session.delete(channel)
    session.flush()
    return True


# ============================================================================
# FREEBUSY OPERATIONS
# ============================================================================


def query_free_busy(
    session: Session,
    user_id: str,
    time_min: str,
    time_max: str,
    calendar_ids: list[str],
    time_zone: Optional[str] = None,
) -> dict[str, Any]:
    """
    Query free/busy information for calendars.

    Following Google Calendar API behavior:
    - If timeZone is not provided, times are returned in UTC (with Z suffix)
    - If timeZone is provided, times are converted to that timezone (with offset like -08:00)
    """
    t_start = time.perf_counter()
    from ..core.utils import parse_rfc3339, format_rfc3339
    from zoneinfo import ZoneInfo
    from datetime import timezone as dt_timezone

    min_dt = parse_rfc3339(time_min)
    max_dt = parse_rfc3339(time_max)

    # Determine target timezone for output
    target_tz = None
    if time_zone:
        try:
            target_tz = ZoneInfo(time_zone)
        except KeyError, ValueError:
            # Invalid timezone - fall back to UTC
            pass

    calendars_result: dict[str, dict[str, Any]] = {}

    # --- Phase 1: Resolve calendar IDs and batch-check access ---
    # Resolve "primary" once
    user = session.get(User, user_id)
    resolved_map: dict[str, str] = {}  # original_id -> resolved_id
    for cal_id in calendar_ids:
        if cal_id == "primary" and user:
            resolved_map[cal_id] = user.email
        else:
            resolved_map[cal_id] = cal_id

    # Batch access check: get all CalendarListEntry rows for this user + these calendars
    resolved_ids = list(set(resolved_map.values()))
    accessible_entries = {
        row.calendar_id: row.access_role
        for row in session.execute(
            select(CalendarListEntry.calendar_id, CalendarListEntry.access_role).where(
                and_(
                    CalendarListEntry.user_id == user_id,
                    CalendarListEntry.calendar_id.in_(resolved_ids),
                    CalendarListEntry.deleted == False,  # noqa: E712
                )
            )
        ).all()
    }

    # For calendars not in CalendarListEntry, do a single batched ACL check
    missing_ids = [cid for cid in resolved_ids if cid not in accessible_entries]
    acl_access: dict[str, AccessRole] = {}
    if missing_ids and user:
        acl_conditions = [
            and_(
                AclRule.scope_type == AclScopeType.user,
                AclRule.scope_value == user.email,
            ),
            and_(
                AclRule.scope_type == AclScopeType.default,
            ),
        ]
        if "@" in user.email:
            domain = user.email.split("@")[1]
            acl_conditions.append(
                and_(
                    AclRule.scope_type == AclScopeType.domain,
                    AclRule.scope_value == domain,
                )
            )
        acl_rules = list(
            session.execute(
                select(AclRule).where(
                    and_(
                        AclRule.calendar_id.in_(missing_ids),
                        AclRule.deleted == False,  # noqa: E712
                        or_(*acl_conditions),
                    )
                )
            )
            .scalars()
            .all()
        )
        # Group by calendar_id, pick highest-priority scope per calendar
        scope_priority = {
            AclScopeType.user: 3,
            AclScopeType.domain: 2,
            AclScopeType.default: 1,
        }
        acl_best_scope: dict[str, AclScopeType] = {}  # track scope of best rule
        for rule in acl_rules:
            existing_scope = acl_best_scope.get(rule.calendar_id)
            if existing_scope is None or scope_priority.get(
                rule.scope_type, 0
            ) > scope_priority.get(existing_scope, 0):
                acl_access[rule.calendar_id] = rule.role
                acl_best_scope[rule.calendar_id] = rule.scope_type

    # Determine which calendars are accessible
    accessible_cal_ids: list[str] = []
    for original_id, resolved_id in resolved_map.items():
        if resolved_id in accessible_entries or resolved_id in acl_access:
            accessible_cal_ids.append(resolved_id)
        else:
            calendars_result[original_id] = {
                "errors": [
                    {
                        "domain": "calendar",
                        "reason": "notFound",
                    }
                ]
            }

    # --- Phase 2: Batch fetch all events across accessible calendars ---
    if accessible_cal_ids:
        all_events = list(
            session.execute(
                select(Event).where(
                    and_(
                        Event.calendar_id.in_(accessible_cal_ids),
                        Event.status != EventStatus.cancelled,
                        Event.transparency == "opaque",
                        or_(
                            and_(
                                Event.start_datetime >= min_dt,
                                Event.start_datetime < max_dt,
                            ),
                            and_(
                                Event.end_datetime > min_dt,
                                Event.end_datetime <= max_dt,
                            ),
                            and_(
                                Event.start_datetime < min_dt,
                                Event.end_datetime > max_dt,
                            ),
                        ),
                    )
                )
            )
            .scalars()
            .all()
        )

        # Group events by calendar_id
        events_by_cal: dict[str, list[Event]] = {cid: [] for cid in accessible_cal_ids}
        for event in all_events:
            if event.calendar_id in events_by_cal:
                events_by_cal[event.calendar_id].append(event)
    else:
        events_by_cal = {}

    # --- Phase 3: Build busy periods ---
    for original_id, resolved_id in resolved_map.items():
        if original_id in calendars_result:
            # Already set as error
            continue

        try:
            events = events_by_cal.get(resolved_id, [])
            busy = []
            for event in events:
                if event.start_datetime and event.end_datetime:
                    start_dt = event.start_datetime
                    end_dt = event.end_datetime

                    # Get the event's timezone from the JSONB start/end fields
                    event_tz_name = None
                    if event.start and isinstance(event.start, dict):
                        event_tz_name = event.start.get("timeZone")

                    if event_tz_name and start_dt.tzinfo is None:
                        try:
                            event_tz = ZoneInfo(event_tz_name)
                            start_dt = start_dt.replace(tzinfo=event_tz)
                        except KeyError, ValueError:
                            start_dt = start_dt.replace(tzinfo=dt_timezone.utc)
                    elif start_dt.tzinfo is None:
                        start_dt = start_dt.replace(tzinfo=dt_timezone.utc)

                    end_tz_name = None
                    if event.end and isinstance(event.end, dict):
                        end_tz_name = event.end.get("timeZone")

                    if end_tz_name and end_dt.tzinfo is None:
                        try:
                            end_tz = ZoneInfo(end_tz_name)
                            end_dt = end_dt.replace(tzinfo=end_tz)
                        except KeyError, ValueError:
                            end_dt = end_dt.replace(tzinfo=dt_timezone.utc)
                    elif end_dt.tzinfo is None:
                        end_dt = end_dt.replace(tzinfo=dt_timezone.utc)

                    if target_tz:
                        start_dt = start_dt.astimezone(target_tz)
                        end_dt = end_dt.astimezone(target_tz)
                        busy.append(
                            {
                                "start": start_dt.isoformat(),
                                "end": end_dt.isoformat(),
                            }
                        )
                    else:
                        start_utc = start_dt.astimezone(dt_timezone.utc)
                        end_utc = end_dt.astimezone(dt_timezone.utc)
                        busy.append(
                            {
                                "start": start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "end": end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            }
                        )

            calendars_result[original_id] = {"busy": busy}

        except Exception as e:
            logger.exception("Error querying free/busy for calendar %s", original_id)
            calendars_result[original_id] = {
                "errors": [
                    {
                        "domain": "calendar",
                        "reason": "internalError",
                    }
                ]
            }

    t_ms = (time.perf_counter() - t_start) * 1000
    if t_ms > 10:
        logger.info(
            f"[PERF] query_free_busy() time={t_ms:.0f}ms calendars={len(calendar_ids)}"
        )
    return {
        "kind": "calendar#freeBusy",
        "timeMin": time_min,
        "timeMax": time_max,
        "calendars": calendars_result,
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _get_user_access_role(
    session: Session,
    calendar_id: str,
    user_id: str,
) -> Optional[AccessRole]:
    """Get user's access role to a calendar.

    Optimized: checks CalendarListEntry first (single query), then falls back
    to a single consolidated ACL query covering user/domain/default scopes.
    """
    user = session.get(User, user_id)
    if user is None:
        return None

    # Check CalendarListEntry first (most common path, indexed on user_id)
    entry = session.execute(
        select(CalendarListEntry.access_role).where(
            and_(
                CalendarListEntry.user_id == user_id,
                CalendarListEntry.calendar_id == calendar_id,
                CalendarListEntry.deleted == False,  # noqa: E712
            )
        )
    ).scalar_one_or_none()

    if entry:
        return entry

    # Consolidated ACL check: fetch all matching rules in a single query
    # instead of 3 separate queries for user/domain/default scopes
    acl_conditions = [
        # User scope
        and_(
            AclRule.scope_type == AclScopeType.user,
            AclRule.scope_value == user.email,
        ),
        # Default scope (public)
        and_(
            AclRule.scope_type == AclScopeType.default,
        ),
    ]

    # Domain scope (only if email has a domain)
    domain = None
    if "@" in user.email:
        domain = user.email.split("@")[1]
        acl_conditions.append(
            and_(
                AclRule.scope_type == AclScopeType.domain,
                AclRule.scope_value == domain,
            )
        )

    rules = list(
        session.execute(
            select(AclRule).where(
                and_(
                    AclRule.calendar_id == calendar_id,
                    AclRule.deleted == False,  # noqa: E712
                    or_(*acl_conditions),
                )
            )
        )
        .scalars()
        .all()
    )

    if not rules:
        return None

    # Return the highest-privilege role found
    # Priority: user scope > domain scope > default scope
    scope_priority = {
        AclScopeType.user: 3,
        AclScopeType.domain: 2,
        AclScopeType.default: 1,
    }
    best_rule = max(rules, key=lambda r: scope_priority.get(r.scope_type, 0))
    return best_rule.role


def _check_calendar_access(
    session: Session,
    calendar_id: str,
    user_id: str,
    required_role: AccessRole,
) -> None:
    """Check if user has required access to calendar."""
    role = _get_user_access_role(session, calendar_id, user_id)

    if role is None:
        raise ForbiddenError(f"No access to calendar: {calendar_id}")

    # Role hierarchy: owner > writer > reader > freeBusyReader
    role_hierarchy = {
        AccessRole.freeBusyReader: 0,
        AccessRole.reader: 1,
        AccessRole.writer: 2,
        AccessRole.owner: 3,
    }

    if role_hierarchy.get(role, 0) < role_hierarchy.get(required_role, 0):
        raise ForbiddenError(f"Insufficient permissions for calendar: {calendar_id}")


def _create_sync_token(
    session: Session,
    user_id: str,
    resource_type: str,
    resource_id: Optional[str] = None,
) -> str:
    """Create a new sync token for incremental sync."""
    token = generate_sync_token()
    now = calendar_now()

    sync_token = SyncToken(
        token=token,
        user_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        snapshot_time=now,
        expires_at=now + timedelta(days=7),  # Tokens expire after 7 days
    )
    session.add(sync_token)

    return token
