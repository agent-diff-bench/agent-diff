"""Error primitives for the __APP_NAME__ API replica.

AGENT INSTRUCTION: The error envelope shape varies per app. Fill in the
structure below based on the API's documented error format.

Common patterns seen across apps:
  - Todoist: {"error_tag": "...", "error_code": N, "error": "...", "http_code": N}
  - Box:     {"type": "error", "status": N, "code": "...", "message": "..."}
  - Google:  {"error": {"code": N, "message": "...", "errors": [...]}}

Adapt the TodoistAPIError class, to_dict(), and convenience constructors to
match the target app. The structure (base class + constructors + handle_exception)
stays the same across all apps.
"""

from __future__ import annotations

from starlette import status
from starlette.responses import JSONResponse


# ---------------------------------------------------------------------------
# Base error class — adapt to_dict() to match the target app's error envelope
# ---------------------------------------------------------------------------

class AppAPIError(Exception):
    """Base app-shaped API error."""

    def __init__(
        self,
        message: str,
        *,
        http_code: int = status.HTTP_400_BAD_REQUEST,
        # AGENT INSTRUCTION: Add app-specific error fields here
        # (e.g. error_tag, error_code, reason, etc.)
    ) -> None:
        super().__init__(message)
        self.message = message
        self.http_code = http_code

    def to_dict(self) -> dict:
        # AGENT INSTRUCTION: Return the app-specific error envelope shape
        return {
            "error": self.message,
            "http_code": self.http_code,
        }

    def to_response(self) -> JSONResponse:
        return JSONResponse(content=self.to_dict(), status_code=self.http_code)


# ---------------------------------------------------------------------------
# Convenience constructors — one per HTTP error the app uses.
# These stay the same across apps; only the internal fields change.
# ---------------------------------------------------------------------------

def bad_request(message: str = "Bad Request") -> AppAPIError:
    return AppAPIError(message=message, http_code=status.HTTP_400_BAD_REQUEST)


def unauthorized(message: str = "Unauthorized") -> AppAPIError:
    return AppAPIError(message=message, http_code=status.HTTP_401_UNAUTHORIZED)


def forbidden(message: str = "Forbidden") -> AppAPIError:
    return AppAPIError(message=message, http_code=status.HTTP_403_FORBIDDEN)


def not_found(message: str = "Not Found") -> AppAPIError:
    return AppAPIError(message=message, http_code=status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------------------------
# Catch-all — universal across apps
# ---------------------------------------------------------------------------

def handle_exception(exc: Exception) -> JSONResponse:
    """Convert unhandled exceptions into an app-shaped error response."""
    if isinstance(exc, AppAPIError):
        return exc.to_response()
    fallback = AppAPIError(
        message=f"Internal server error: {exc}",
        http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    return fallback.to_response()
