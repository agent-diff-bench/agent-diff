"""Error primitives for the Asana API replica.

Asana errors use the ErrorResponse envelope:
  {"errors": [{"message": "...", "help": "...", "phrase": "..."}]}

The `help` field is optional and provides links to documentation.
The `phrase` field is only present on 500 errors (used by Asana support
to look up specific incidents).
"""

from __future__ import annotations

from starlette import status
from starlette.responses import JSONResponse


class AsanaAPIError(Exception):
    """Base Asana-shaped API error."""

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
        error: dict = {"message": self.message}
        if self.help_url is not None:
            error["help"] = self.help_url
        if self.phrase is not None:
            error["phrase"] = self.phrase
        return {"errors": [error]}

    def to_response(self) -> JSONResponse:
        return JSONResponse(content=self.to_dict(), status_code=self.http_code)


# ---------------------------------------------------------------------------
# Convenience constructors — one per standard HTTP error in the Asana spec
# ---------------------------------------------------------------------------

def bad_request(message: str = "Bad request") -> AsanaAPIError:
    return AsanaAPIError(message=message, http_code=status.HTTP_400_BAD_REQUEST)


def unauthorized(message: str = "Not authorized") -> AsanaAPIError:
    return AsanaAPIError(message=message, http_code=status.HTTP_401_UNAUTHORIZED)


def payment_required(message: str = "Payment required") -> AsanaAPIError:
    return AsanaAPIError(message=message, http_code=status.HTTP_402_PAYMENT_REQUIRED)


def forbidden(message: str = "Forbidden") -> AsanaAPIError:
    return AsanaAPIError(message=message, http_code=status.HTTP_403_FORBIDDEN)


def not_found(message: str = "Not found") -> AsanaAPIError:
    return AsanaAPIError(message=message, http_code=status.HTTP_404_NOT_FOUND)


def internal_server_error(
    message: str = "Server error", phrase: str | None = None
) -> AsanaAPIError:
    return AsanaAPIError(
        message=message,
        http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        phrase=phrase,
    )


# ---------------------------------------------------------------------------
# Catch-all handler
# ---------------------------------------------------------------------------

def handle_exception(exception: Exception) -> JSONResponse:
    """Convert unhandled exceptions into an Asana-shaped error response."""
    if isinstance(exception, AsanaAPIError):
        return exception.to_response()
    fallback = internal_server_error(message=f"Server error: {exception}")
    return fallback.to_response()
