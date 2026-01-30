# Schema for Google Calendar API Replica
# Based on https://developers.google.com/calendar/api/v3/reference

from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Optional
from sqlalchemy import (
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


# ============================================================================
# ENUMS
# ============================================================================


class AccessRole(PyEnum):
    """Calendar access roles."""

    none = "none"  # Used for deleted ACLs
    freeBusyReader = "freeBusyReader"
    reader = "reader"
    writer = "writer"
    owner = "owner"


class EventStatus(PyEnum):
    """Event status values."""

    confirmed = "confirmed"
    tentative = "tentative"
    cancelled = "cancelled"


class EventTransparency(PyEnum):
    """Event transparency (affects free/busy)."""

    opaque = "opaque"
    transparent = "transparent"


class EventVisibility(PyEnum):
    """Event visibility levels."""

    default = "default"
    public = "public"
    private = "private"
    confidential = "confidential"


class EventType(PyEnum):
    """Event type classification."""

    default = "default"
    outOfOffice = "outOfOffice"
    focusTime = "focusTime"
    workingLocation = "workingLocation"
    fromGmail = "fromGmail"
    birthday = "birthday"


class AttendeeResponseStatus(PyEnum):
    """Attendee RSVP status."""

    needsAction = "needsAction"
    declined = "declined"
    tentative = "tentative"
    accepted = "accepted"


class AclScopeType(PyEnum):
    """ACL scope type values."""

    default = "default"
    user = "user"
    group = "group"
    domain = "domain"


class ReminderMethod(PyEnum):
    """Reminder delivery method."""

    email = "email"
    popup = "popup"


# ============================================================================
# MODELS
# ============================================================================


class User(Base):
    """
    User/Principal entity.
    Represents a Google account that can own calendars and attend events.
    """

    __tablename__ = "calendar_users"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    self_: Mapped[bool] = mapped_column(
        "self", Boolean, default=False, server_default="false"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    owned_calendars: Mapped[list["Calendar"]] = relationship(
        back_populates="owner", cascade="all,delete-orphan"
    )
    calendar_list_entries: Mapped[list["CalendarListEntry"]] = relationship(
        back_populates="user", cascade="all,delete-orphan"
    )
    settings: Mapped[list["Setting"]] = relationship(
        back_populates="user", cascade="all,delete-orphan"
    )
    created_events: Mapped[list["Event"]] = relationship(
        back_populates="creator", foreign_keys="Event.creator_id"
    )
    organized_events: Mapped[list["Event"]] = relationship(
        back_populates="organizer", foreign_keys="Event.organizer_id"
    )


class Calendar(Base):
    """
    Calendar resource.
    Represents a calendar that can contain events.
    kind = "calendar#calendar"
    """

    __tablename__ = "calendars"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    time_zone: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    etag: Mapped[str] = mapped_column(String(100), nullable=False)
    conference_properties: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    # Whether this calendar automatically accepts invitations (resource calendars only)
    auto_accept_invitations: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    owner_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_users.id"), nullable=False
    )
    # Read-only: Email of the owner (for secondary calendars)
    data_owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    # Relationships
    owner: Mapped["User"] = relationship(back_populates="owned_calendars")
    events: Mapped[list["Event"]] = relationship(
        back_populates="calendar", cascade="all,delete-orphan"
    )
    acl_rules: Mapped[list["AclRule"]] = relationship(
        back_populates="calendar", cascade="all,delete-orphan"
    )
    calendar_list_entries: Mapped[list["CalendarListEntry"]] = relationship(
        back_populates="calendar", cascade="all,delete-orphan"
    )

    @property
    def kind(self) -> str:
        return "calendar#calendar"


class CalendarListEntry(Base):
    """
    Calendar list entry.
    Represents a user's subscription to a calendar with personalized settings.
    kind = "calendar#calendarListEntry"
    """

    __tablename__ = "calendar_list_entries"
    __table_args__ = (
        UniqueConstraint("user_id", "calendar_id", name="uq_user_calendar"),
        Index("ix_calendar_list_user", "user_id"),
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_users.id"), nullable=False
    )
    calendar_id: Mapped[str] = mapped_column(
        ForeignKey("calendars.id"), nullable=False
    )
    etag: Mapped[str] = mapped_column(String(100), nullable=False)

    # Access role
    access_role: Mapped[AccessRole] = mapped_column(
        Enum(AccessRole, name="access_role_enum", native_enum=True, schema="public"),
        nullable=False,
    )

    # Display settings (can override calendar defaults)
    summary_override: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description_override: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    color_id: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    background_color: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    foreground_color: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Visibility settings
    hidden: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    selected: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    primary: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    # Reminders and notifications
    default_reminders: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(
        JSONB, nullable=True
    )
    notification_settings: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="calendar_list_entries")
    calendar: Mapped["Calendar"] = relationship(back_populates="calendar_list_entries")

    @property
    def kind(self) -> str:
        return "calendar#calendarListEntry"


class Event(Base):
    """
    Event resource.
    Represents a calendar event.
    kind = "calendar#event"
    """

    __tablename__ = "calendar_events"
    __table_args__ = (
        Index("ix_event_calendar", "calendar_id"),
        Index("ix_event_start", "start_datetime"),
        Index("ix_event_end", "end_datetime"),
        Index("ix_event_ical_uid", "ical_uid"),
        Index("ix_event_recurring", "recurring_event_id"),
        Index("ix_event_updated", "updated_at"),
    )

    id: Mapped[str] = mapped_column(String(1024), primary_key=True)
    calendar_id: Mapped[str] = mapped_column(
        ForeignKey("calendars.id"), nullable=False
    )
    etag: Mapped[str] = mapped_column(String(100), nullable=False)

    # Basic info
    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus, name="event_status_enum", native_enum=True, schema="public"),
        default=EventStatus.confirmed,
    )
    html_link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    color_id: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Creator and organizer
    creator_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("calendar_users.id"), nullable=True
    )
    organizer_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("calendar_users.id"), nullable=True
    )
    # Store creator/organizer info directly for cases where user doesn't exist
    creator_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organizer_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    creator_display_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    organizer_display_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    # Google Profile IDs (different from internal user_id)
    creator_profile_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organizer_profile_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    creator_self: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    organizer_self: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    # Date/Time - stored as JSON for flexibility (date vs dateTime vs timeZone)
    start: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    end: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    # Denormalized datetime for indexing/querying
    start_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    start_date: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True
    )  # YYYY-MM-DD for all-day
    end_date: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    end_time_unspecified: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    # Recurrence
    recurrence: Mapped[Optional[list[str]]] = mapped_column(JSONB, nullable=True)
    recurring_event_id: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    original_start_time: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )

    # Visibility and transparency
    transparency: Mapped[EventTransparency] = mapped_column(
        Enum(
            EventTransparency,
            name="event_transparency_enum",
            native_enum=True,
            schema="public",
        ),
        default=EventTransparency.opaque,
    )
    visibility: Mapped[EventVisibility] = mapped_column(
        Enum(
            EventVisibility,
            name="event_visibility_enum",
            native_enum=True,
            schema="public",
        ),
        default=EventVisibility.default,
    )

    # iCalendar UID
    ical_uid: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    sequence: Mapped[int] = mapped_column(Integer, default=0)

    # Guest permissions
    guests_can_invite_others: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    guests_can_modify: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    guests_can_see_other_guests: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    anyone_can_add_self: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    # Special flags
    private_copy: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    locked: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    attendees_omitted: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    # Conferencing
    hangout_link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    conference_data: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )

    # Attachments
    attachments: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(
        JSONB, nullable=True
    )

    # Extended properties
    extended_properties: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )

    # Source
    source: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Gadget
    gadget: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Reminders (event-specific override)
    reminders: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Event type and related properties
    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType, name="event_type_enum", native_enum=True, schema="public"),
        default=EventType.default,
    )
    working_location_properties: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    out_of_office_properties: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    focus_time_properties: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    birthday_properties: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    calendar: Mapped["Calendar"] = relationship(back_populates="events")
    creator: Mapped[Optional["User"]] = relationship(
        back_populates="created_events", foreign_keys=[creator_id]
    )
    organizer: Mapped[Optional["User"]] = relationship(
        back_populates="organized_events", foreign_keys=[organizer_id]
    )
    attendees: Mapped[list["EventAttendee"]] = relationship(
        back_populates="event", cascade="all,delete-orphan"
    )
    reminders_list: Mapped[list["EventReminder"]] = relationship(
        back_populates="event", cascade="all,delete-orphan"
    )

    @property
    def kind(self) -> str:
        return "calendar#event"


class EventAttendee(Base):
    """
    Event attendee.
    Represents a person attending an event.
    """

    __tablename__ = "calendar_event_attendees"
    __table_args__ = (
        UniqueConstraint("event_id", "email", name="uq_event_attendee"),
        Index("ix_attendee_event", "event_id"),
        Index("ix_attendee_email", "email"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_events.id"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organizer: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    self_: Mapped[bool] = mapped_column(
        "self", Boolean, default=False, server_default="false"
    )
    resource: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    optional: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    response_status: Mapped[AttendeeResponseStatus] = mapped_column(
        Enum(
            AttendeeResponseStatus,
            name="attendee_response_enum",
            native_enum=True,
            schema="public",
        ),
        default=AttendeeResponseStatus.needsAction,
    )
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    additional_guests: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    # Profile ID (if available)
    profile_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationship
    event: Mapped["Event"] = relationship(back_populates="attendees")


class EventReminder(Base):
    """
    Event reminder override.
    Represents a reminder setting for an event.
    """

    __tablename__ = "calendar_event_reminders"
    __table_args__ = (Index("ix_reminder_event", "event_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_events.id"), nullable=False
    )
    method: Mapped[ReminderMethod] = mapped_column(
        Enum(
            ReminderMethod,
            name="reminder_method_enum",
            native_enum=True,
            schema="public",
        ),
        nullable=False,
    )
    minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationship
    event: Mapped["Event"] = relationship(back_populates="reminders_list")


class AclRule(Base):
    """
    Access Control List rule.
    Represents a permission grant on a calendar.
    kind = "calendar#aclRule"
    """

    __tablename__ = "calendar_acl_rules"
    __table_args__ = (
        UniqueConstraint("calendar_id", "scope_type", "scope_value", name="uq_acl_rule"),
        Index("ix_acl_calendar", "calendar_id"),
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    calendar_id: Mapped[str] = mapped_column(
        ForeignKey("calendars.id"), nullable=False
    )
    etag: Mapped[str] = mapped_column(String(100), nullable=False)

    role: Mapped[AccessRole] = mapped_column(
        Enum(AccessRole, name="acl_role_enum", native_enum=True, schema="public"),
        nullable=False,
    )
    scope_type: Mapped[AclScopeType] = mapped_column(
        Enum(
            AclScopeType, name="acl_scope_type_enum", native_enum=True, schema="public"
        ),
        nullable=False,
    )
    scope_value: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )  # email or domain

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    # Relationship
    calendar: Mapped["Calendar"] = relationship(back_populates="acl_rules")

    @property
    def kind(self) -> str:
        return "calendar#aclRule"


class Setting(Base):
    """
    User setting.
    Represents a user's calendar settings.
    kind = "calendar#setting"
    """

    __tablename__ = "calendar_settings"
    __table_args__ = (
        UniqueConstraint("user_id", "setting_id", name="uq_user_setting"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_users.id"), nullable=False
    )
    setting_id: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    etag: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationship
    user: Mapped["User"] = relationship(back_populates="settings")

    @property
    def kind(self) -> str:
        return "calendar#setting"


class Channel(Base):
    """
    Push notification channel.
    Represents a watch channel for push notifications.
    kind = "api#channel"

    Note: This is largely stubbed - full push notification support is Phase 5.
    """

    __tablename__ = "calendar_channels"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_uri: Mapped[str] = mapped_column(String(1000), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # Usually "web_hook"
    address: Mapped[str] = mapped_column(
        String(1000), nullable=False
    )  # Webhook callback URL
    expiration: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )  # Unix timestamp ms
    token: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    params: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    # Whether payload is wanted for notifications
    payload: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    # User who created the channel (for ownership validation)
    user_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    @property
    def kind(self) -> str:
        return "api#channel"


class SyncToken(Base):
    """
    Sync token tracking.
    Used for incremental sync support in list operations.
    """

    __tablename__ = "calendar_sync_tokens"
    __table_args__ = (
        Index("ix_sync_token_resource", "resource_type", "resource_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_users.id"), nullable=False
    )
    resource_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # 'events', 'calendarList', 'acl', 'settings'
    resource_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )  # calendar_id for events/acl
    snapshot_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
