"""Error primitives for __APP_NAME__ REST API."""

from __future__ import annotations

from typing import Any

from starlette import status
from starlette.responses import JSONResponse

# BEGIN SHARED HELPERS
ERROR_DOMAIN = "__SERVICE_MOUNT_NAME__"


class AppAPIError(Exception):
    """Base app-shaped API error."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        reason: str = "invalid",
        location: str | None = None,
        location_type: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.reason = reason
        self.location = location
        self.location_type = location_type

    def to_dict(self) -> dict[str, Any]:
        error_detail: dict[str, Any] = {
            "domain": ERROR_DOMAIN,
            "reason": self.reason,
            "message": self.message,
        }
        if self.location is not None:
            error_detail["location"] = self.location
        if self.location_type is not None:
            error_detail["locationType"] = self.location_type

        return {
            "error": {
                "code": self.status_code,
                "message": self.message,
                "errors": [error_detail],
            }
        }

    def to_response(self) -> JSONResponse:
        return JSONResponse(content=self.to_dict(), status_code=self.status_code)


def bad_request(message: str) -> AppAPIError:
    return AppAPIError(
        message=message,
        status_code=status.HTTP_400_BAD_REQUEST,
        reason="invalid",
    )


def unauthorized(message: str = "Unauthorized") -> AppAPIError:
    return AppAPIError(
        message=message,
        status_code=status.HTTP_401_UNAUTHORIZED,
        reason="authError",
    )


def forbidden(message: str = "Forbidden") -> AppAPIError:
    return AppAPIError(
        message=message,
        status_code=status.HTTP_403_FORBIDDEN,
        reason="forbidden",
    )


def not_found(message: str = "Not found") -> AppAPIError:
    return AppAPIError(
        message=message,
        status_code=status.HTTP_404_NOT_FOUND,
        reason="notFound",
    )


def conflict(message: str = "Conflict") -> AppAPIError:
    return AppAPIError(
        message=message,
        status_code=status.HTTP_409_CONFLICT,
        reason="conflict",
    )


def handle_exception(exc: Exception) -> JSONResponse:
    """Convert unhandled exceptions into deterministic API responses."""
    if isinstance(exc, AppAPIError):
        return exc.to_response()
    fallback = AppAPIError(
        message=f"Internal server error: {exc}",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        reason="internalError",
    )
    return fallback.to_response()
# END SHARED HELPERS

