"""Error primitives for the Todoist API replica.

Todoist errors use:
  - error_tag: machine-readable identifier (e.g. "ITEM_NOT_FOUND")
  - error_code: numeric code
  - error: human-readable message
  - http_code: HTTP status
"""

from __future__ import annotations

from starlette import status
from starlette.responses import JSONResponse


class TodoistAPIError(Exception):
    """Base Todoist-shaped API error."""

    def __init__(
        self,
        message: str,
        *,
        error_tag: str = "UNKNOWN_ERROR",
        error_code: int = 0,
        http_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_tag = error_tag
        self.error_code = error_code
        self.http_code = http_code

    def to_dict(self) -> dict:
        return {
            "error_tag": self.error_tag,
            "error_code": self.error_code,
            "error": self.message,
            "http_code": self.http_code,
        }

    def to_response(self) -> JSONResponse:
        return JSONResponse(content=self.to_dict(), status_code=self.http_code)


def bad_request(message: str = "Bad Request") -> TodoistAPIError:
    return TodoistAPIError(
        message=message,
        error_tag="INVALID_REQUEST",
        error_code=20,
        http_code=status.HTTP_400_BAD_REQUEST,
    )


def unauthorized(message: str = "Unauthorized") -> TodoistAPIError:
    return TodoistAPIError(
        message=message,
        error_tag="AUTH_INVALID_TOKEN",
        error_code=1,
        http_code=status.HTTP_401_UNAUTHORIZED,
    )


def forbidden(message: str = "Forbidden") -> TodoistAPIError:
    return TodoistAPIError(
        message=message,
        error_tag="FORBIDDEN",
        error_code=3,
        http_code=status.HTTP_403_FORBIDDEN,
    )


def not_found(message: str = "Not Found") -> TodoistAPIError:
    return TodoistAPIError(
        message=message,
        error_tag="ITEM_NOT_FOUND",
        error_code=40,
        http_code=status.HTTP_404_NOT_FOUND,
    )


def handle_exception(exc: Exception) -> JSONResponse:
    """Convert unhandled exceptions into a Todoist-shaped error response."""
    if isinstance(exc, TodoistAPIError):
        return exc.to_response()
    fallback = TodoistAPIError(
        message=f"Internal server error: {exc}",
        error_tag="INTERNAL_ERROR",
        error_code=0,
        http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    return fallback.to_response()
