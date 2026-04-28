"""Error primitives for the Asana API replica.

Asana error envelope shape (ErrorResponse):
  {"errors": [{"message": "...", "help": "...", "phrase": "..."}]}

The `errors` array contains Error objects. Each has a required `message` field
and optional `help` (documentation link) and `phrase` (incident lookup key for
server errors).
"""

from __future__ import annotations

from starlette import status
from starlette.responses import JSONResponse


# ---------------------------------------------------------------------------
# Base error class — returns Asana's ErrorResponse envelope
# ---------------------------------------------------------------------------

class AppAPIError(Exception):
    """Asana-shaped API error."""

    def __init__(
        self,
        message: str,
        *,
        http_code: int = status.HTTP_400_BAD_REQUEST,
        help_url: str | None = None,
        phrase: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.http_code = http_code
        self.help_url = help_url
        self.phrase = phrase

    def to_dict(self) -> dict:
        error_object: dict = {"message": self.message}
        if self.help_url is not None:
            error_object["help"] = self.help_url
        if self.phrase is not None:
            error_object["phrase"] = self.phrase
        return {"errors": [error_object]}

    def to_response(self) -> JSONResponse:
        return JSONResponse(content=self.to_dict(), status_code=self.http_code)


# ---------------------------------------------------------------------------
# Convenience constructors — one per standard HTTP error in the Asana spec
# ---------------------------------------------------------------------------

def bad_request(message: str = "Bad Request") -> AppAPIError:
    return AppAPIError(message=message, http_code=status.HTTP_400_BAD_REQUEST)


def unauthorized(message: str = "Unauthorized") -> AppAPIError:
    return AppAPIError(message=message, http_code=status.HTTP_401_UNAUTHORIZED)


def payment_required(message: str = "Payment Required") -> AppAPIError:
    return AppAPIError(message=message, http_code=status.HTTP_402_PAYMENT_REQUIRED)


def forbidden(message: str = "Forbidden") -> AppAPIError:
    return AppAPIError(message=message, http_code=status.HTTP_403_FORBIDDEN)


def not_found(message: str = "Not Found") -> AppAPIError:
    return AppAPIError(message=message, http_code=status.HTTP_404_NOT_FOUND)


def internal_server_error(
    message: str = "Internal Server Error",
    phrase: str | None = None,
) -> AppAPIError:
    return AppAPIError(
        message=message,
        http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        phrase=phrase,
    )


# ---------------------------------------------------------------------------
# Catch-all — universal across apps
# ---------------------------------------------------------------------------

def handle_exception(exc: Exception) -> JSONResponse:
    """Convert unhandled exceptions into an Asana-shaped error response."""
    if isinstance(exc, AppAPIError):
        return exc.to_response()
    fallback = internal_server_error(message=f"Internal server error: {exc}")
    return fallback.to_response()
