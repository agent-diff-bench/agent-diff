# Google Calendar API Error Handling
# Implements Google-style error responses

from typing import Any, Optional
from starlette.responses import JSONResponse


# ============================================================================
# ERROR REASONS (from discovery doc and API behavior)
# ============================================================================

# Standard error reasons
ERROR_NOT_FOUND = "notFound"
ERROR_INVALID = "invalid"
ERROR_REQUIRED = "required"
ERROR_DUPLICATE = "duplicate"
ERROR_FORBIDDEN = "forbidden"
ERROR_UNAUTHORIZED = "authError"
ERROR_RATE_LIMITED = "rateLimitExceeded"
ERROR_INTERNAL = "internalError"
ERROR_GONE = "resourceRemoved"
ERROR_CONFLICT = "conflict"
ERROR_PRECONDITION_FAILED = "conditionNotMet"

# Calendar-specific error reasons
ERROR_GROUP_TOO_BIG = "groupTooBig"
ERROR_TOO_MANY_CALENDARS = "tooManyCalendarsRequested"
ERROR_CALENDAR_NOT_FOUND = "calendarNotFound"
ERROR_EVENT_NOT_FOUND = "eventNotFound"
ERROR_ACL_NOT_FOUND = "aclNotFound"
ERROR_SETTING_NOT_FOUND = "settingNotFound"
ERROR_CHANNEL_NOT_FOUND = "channelNotFound"
ERROR_INVALID_SYNC_TOKEN = "syncTokenInvalid"
ERROR_SYNC_TOKEN_EXPIRED = "fullSyncRequired"
ERROR_INVALID_PAGE_TOKEN = "pageTokenInvalid"

# Domain
ERROR_DOMAIN_GLOBAL = "global"
ERROR_DOMAIN_CALENDAR = "calendar"


# ============================================================================
# EXCEPTION CLASSES
# ============================================================================


class CalendarAPIError(Exception):
    """Base exception for Calendar API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        reason: str = ERROR_INVALID,
        domain: str = ERROR_DOMAIN_CALENDAR,
        location: Optional[str] = None,
        location_type: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.reason = reason
        self.domain = domain
        self.location = location
        self.location_type = location_type

    def to_dict(self) -> dict[str, Any]:
        """Convert to Google-style error response dict."""
        error_detail: dict[str, Any] = {
            "domain": self.domain,
            "reason": self.reason,
            "message": self.message,
        }
        if self.location:
            error_detail["location"] = self.location
        if self.location_type:
            error_detail["locationType"] = self.location_type

        return {
            "error": {
                "code": self.status_code,
                "message": self.message,
                "errors": [error_detail],
            }
        }

    def to_response(self) -> JSONResponse:
        """Convert to Starlette JSONResponse."""
        return JSONResponse(
            content=self.to_dict(),
            status_code=self.status_code,
        )


class NotFoundError(CalendarAPIError):
    """Resource not found (404)."""

    def __init__(
        self,
        message: str = "Not Found",
        reason: str = ERROR_NOT_FOUND,
        resource_type: Optional[str] = None,
    ):
        if resource_type:
            message = f"{resource_type} not found"
        super().__init__(
            message=message,
            status_code=404,
            reason=reason,
        )


class CalendarNotFoundError(NotFoundError):
    """Calendar not found."""

    def __init__(self, calendar_id: str):
        super().__init__(
            message=f"Calendar not found: {calendar_id}",
            reason=ERROR_CALENDAR_NOT_FOUND,
            resource_type="Calendar",
        )


class EventNotFoundError(NotFoundError):
    """Event not found."""

    def __init__(self, event_id: str):
        super().__init__(
            message=f"Event not found: {event_id}",
            reason=ERROR_EVENT_NOT_FOUND,
            resource_type="Event",
        )


class AclNotFoundError(NotFoundError):
    """ACL rule not found."""

    def __init__(self, rule_id: str):
        super().__init__(
            message=f"ACL rule not found: {rule_id}",
            reason=ERROR_ACL_NOT_FOUND,
            resource_type="AclRule",
        )


class SettingNotFoundError(NotFoundError):
    """Setting not found."""

    def __init__(self, setting_id: str):
        super().__init__(
            message=f"Setting not found: {setting_id}",
            reason=ERROR_SETTING_NOT_FOUND,
            resource_type="Setting",
        )


class ChannelNotFoundError(NotFoundError):
    """Channel not found."""

    def __init__(self, channel_id: str):
        super().__init__(
            message=f"Channel not found: {channel_id}",
            reason=ERROR_CHANNEL_NOT_FOUND,
            resource_type="Channel",
        )


class ValidationError(CalendarAPIError):
    """Invalid request data (400)."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        reason: str = ERROR_INVALID,
    ):
        location = field
        location_type = "parameter" if field else None
        super().__init__(
            message=message,
            status_code=400,
            reason=reason,
            location=location,
            location_type=location_type,
        )


class RequiredFieldError(ValidationError):
    """Required field missing (400)."""

    def __init__(self, field: str):
        super().__init__(
            message=f"Required field missing: {field}",
            field=field,
            reason=ERROR_REQUIRED,
        )


class InvalidFieldError(ValidationError):
    """Invalid field value (400)."""

    def __init__(self, field: str, message: Optional[str] = None):
        msg = message or f"Invalid value for field: {field}"
        super().__init__(
            message=msg,
            field=field,
            reason=ERROR_INVALID,
        )


class DuplicateError(CalendarAPIError):
    """Duplicate resource (409)."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            message=message,
            status_code=409,
            reason=ERROR_DUPLICATE,
        )


class ForbiddenError(CalendarAPIError):
    """Access forbidden (403)."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            status_code=403,
            reason=ERROR_FORBIDDEN,
        )


class UnauthorizedError(CalendarAPIError):
    """Unauthorized access (401)."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            status_code=401,
            reason=ERROR_UNAUTHORIZED,
            domain=ERROR_DOMAIN_GLOBAL,
        )


class PreconditionFailedError(CalendarAPIError):
    """Precondition failed / ETag mismatch (412)."""

    def __init__(self, message: str = "Precondition Failed"):
        super().__init__(
            message=message,
            status_code=412,
            reason=ERROR_PRECONDITION_FAILED,
        )


class GoneError(CalendarAPIError):
    """Resource gone / sync token expired (410)."""

    def __init__(self, message: str = "Resource is no longer available"):
        super().__init__(
            message=message,
            status_code=410,
            reason=ERROR_GONE,
        )


class SyncTokenExpiredError(GoneError):
    """Sync token expired, full sync required (410)."""

    def __init__(self):
        super().__init__(message="Sync token is no longer valid. Full sync required.")
        self.reason = ERROR_SYNC_TOKEN_EXPIRED


class RateLimitedError(CalendarAPIError):
    """Rate limited (429)."""

    def __init__(self, message: str = "Rate Limit Exceeded"):
        super().__init__(
            message=message,
            status_code=429,
            reason=ERROR_RATE_LIMITED,
            domain=ERROR_DOMAIN_GLOBAL,
        )


class InternalError(CalendarAPIError):
    """Internal server error (500)."""

    def __init__(self, message: str = "Internal Server Error"):
        super().__init__(
            message=message,
            status_code=500,
            reason=ERROR_INTERNAL,
        )


class TooManyCalendarsError(CalendarAPIError):
    """Too many calendars in request (400)."""

    def __init__(self):
        super().__init__(
            message="The number of calendars requested is too large for a single query",
            status_code=400,
            reason=ERROR_TOO_MANY_CALENDARS,
        )


class GroupTooBigError(CalendarAPIError):
    """Group too big for query (400)."""

    def __init__(self):
        super().__init__(
            message="The group of users requested is too large for a single query",
            status_code=400,
            reason=ERROR_GROUP_TOO_BIG,
        )


# ============================================================================
# ERROR RESPONSE BUILDERS
# ============================================================================


def error_response(
    status_code: int,
    message: str,
    reason: str = ERROR_INVALID,
    domain: str = ERROR_DOMAIN_CALENDAR,
) -> JSONResponse:
    """Build a Google-style error response."""
    error = CalendarAPIError(
        message=message,
        status_code=status_code,
        reason=reason,
        domain=domain,
    )
    return error.to_response()


def validation_error_response(
    message: str,
    field: Optional[str] = None,
) -> JSONResponse:
    """Build a validation error response."""
    error = ValidationError(message=message, field=field)
    return error.to_response()


def not_found_response(
    resource_type: str,
    resource_id: str,
) -> JSONResponse:
    """Build a not found error response."""
    error = NotFoundError(
        message=f"{resource_type} not found: {resource_id}",
        reason=ERROR_NOT_FOUND,
    )
    return error.to_response()


# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================


def handle_exception(exc: Exception) -> JSONResponse:
    """Convert an exception to a JSONResponse."""
    if isinstance(exc, CalendarAPIError):
        return exc.to_response()

    # Log unexpected exceptions
    import logging

    logging.error(f"Unexpected exception: {exc}", exc_info=True)

    return InternalError().to_response()
