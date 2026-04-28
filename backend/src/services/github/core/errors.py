"""Error primitives for the GitHub API replica.

GitHub error envelope (basic-error):
  {"message": "...", "documentation_url": "...", "url": "...", "status": "..."}

Validation errors add an `errors` array with structured field-level details.
Service-unavailable uses a slightly different shape with a `code` field.
"""

from __future__ import annotations

from typing import Any

from starlette import status
from starlette.responses import JSONResponse


DOCS_URL = "https://docs.github.com/rest"


# ---------------------------------------------------------------------------
# Base error class — returns GitHub's basic-error envelope
# ---------------------------------------------------------------------------

class AppAPIError(Exception):
    """GitHub-shaped API error."""

    def __init__(
        self,
        message: str,
        *,
        http_code: int = status.HTTP_400_BAD_REQUEST,
        documentation_url: str = DOCS_URL,
        status_text: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.http_code = http_code
        self.documentation_url = documentation_url
        self.status_text = status_text

    def to_dict(self) -> dict:
        body: dict[str, Any] = {
            "message": self.message,
            "documentation_url": self.documentation_url,
        }
        if self.status_text is not None:
            body["status"] = self.status_text
        return body

    def to_response(self) -> JSONResponse:
        return JSONResponse(content=self.to_dict(), status_code=self.http_code)


# ---------------------------------------------------------------------------
# Validation error — includes structured field-level error details
# Schema: validation-error
# ---------------------------------------------------------------------------

class ValidationError(AppAPIError):
    """GitHub validation error with structured field-level details."""

    def __init__(
        self,
        message: str = "Validation Failed",
        *,
        documentation_url: str = DOCS_URL,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            message,
            http_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            documentation_url=documentation_url,
        )
        self.errors = errors

    def to_dict(self) -> dict:
        body: dict[str, Any] = {
            "message": self.message,
            "documentation_url": self.documentation_url,
        }
        if self.errors is not None:
            body["errors"] = self.errors
        return body


# ---------------------------------------------------------------------------
# Simple validation error — errors array is just strings
# Schema: validation-error-simple
# ---------------------------------------------------------------------------

class ValidationErrorSimple(AppAPIError):
    """GitHub validation error with simple string error list."""

    def __init__(
        self,
        message: str = "Validation Failed",
        *,
        documentation_url: str = DOCS_URL,
        errors: list[str] | None = None,
    ) -> None:
        super().__init__(
            message,
            http_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            documentation_url=documentation_url,
        )
        self.errors = errors

    def to_dict(self) -> dict:
        body: dict[str, Any] = {
            "message": self.message,
            "documentation_url": self.documentation_url,
        }
        if self.errors is not None:
            body["errors"] = self.errors
        return body


# ---------------------------------------------------------------------------
# Service-unavailable error — uses {code, message, documentation_url} shape
# ---------------------------------------------------------------------------

class ServiceUnavailableError(AppAPIError):
    """GitHub service-unavailable error with a code field."""

    def __init__(
        self,
        message: str = "Service unavailable",
        *,
        code: str | None = None,
        documentation_url: str = DOCS_URL,
    ) -> None:
        super().__init__(
            message,
            http_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            documentation_url=documentation_url,
        )
        self.code = code

    def to_dict(self) -> dict:
        body: dict[str, Any] = {
            "message": self.message,
            "documentation_url": self.documentation_url,
        }
        if self.code is not None:
            body["code"] = self.code
        return body


# ---------------------------------------------------------------------------
# Convenience constructors — one per standard HTTP error in the GitHub spec.
# All basic-error responses share the same {message, documentation_url, status}
# shape and only differ in HTTP status code.
# ---------------------------------------------------------------------------

def bad_request(message: str = "Bad Request") -> AppAPIError:
    return AppAPIError(
        message=message,
        http_code=status.HTTP_400_BAD_REQUEST,
        status_text="400",
    )


def unauthorized(message: str = "Requires authentication") -> AppAPIError:
    return AppAPIError(
        message=message,
        http_code=status.HTTP_401_UNAUTHORIZED,
        status_text="401",
    )


def forbidden(message: str = "Forbidden") -> AppAPIError:
    return AppAPIError(
        message=message,
        http_code=status.HTTP_403_FORBIDDEN,
        status_text="403",
    )


def not_found(message: str = "Not Found") -> AppAPIError:
    return AppAPIError(
        message=message,
        http_code=status.HTTP_404_NOT_FOUND,
        status_text="404",
    )


def conflict(message: str = "Conflict") -> AppAPIError:
    return AppAPIError(
        message=message,
        http_code=status.HTTP_409_CONFLICT,
        status_text="409",
    )


def gone(message: str = "Gone") -> AppAPIError:
    return AppAPIError(
        message=message,
        http_code=status.HTTP_410_GONE,
        status_text="410",
    )


def unprocessable_entity(
    message: str = "Validation Failed",
    errors: list[dict[str, Any]] | None = None,
) -> ValidationError:
    return ValidationError(message=message, errors=errors)


def unprocessable_entity_simple(
    message: str = "Validation Failed",
    errors: list[str] | None = None,
) -> ValidationErrorSimple:
    return ValidationErrorSimple(message=message, errors=errors)


def internal_server_error(message: str = "Internal Server Error") -> AppAPIError:
    return AppAPIError(
        message=message,
        http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        status_text="500",
    )


def service_unavailable(
    message: str = "Service unavailable",
    code: str | None = None,
) -> ServiceUnavailableError:
    return ServiceUnavailableError(message=message, code=code)


# ---------------------------------------------------------------------------
# Catch-all — universal across apps
# ---------------------------------------------------------------------------

def handle_exception(exc: Exception) -> JSONResponse:
    """Convert unhandled exceptions into a GitHub-shaped error response."""
    if isinstance(exc, AppAPIError):
        return exc.to_response()
    fallback = internal_server_error(message=f"Internal server error: {exc}")
    return fallback.to_response()
