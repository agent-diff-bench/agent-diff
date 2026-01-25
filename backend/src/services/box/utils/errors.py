"""
Box API Error Handling - Based on validated Box SDK error schemas.
"""

from typing import Any
from starlette import status

from .enums import BoxErrorCode
from .ids import generate_request_id


# Map error codes to HTTP status codes
ERROR_STATUS_MAP: dict[BoxErrorCode, int] = {
    # Success codes
    BoxErrorCode.CREATED: status.HTTP_201_CREATED,
    BoxErrorCode.ACCEPTED: status.HTTP_202_ACCEPTED,
    BoxErrorCode.NO_CONTENT: status.HTTP_204_NO_CONTENT,
    BoxErrorCode.NOT_MODIFIED: status.HTTP_304_NOT_MODIFIED,
    # Redirect
    BoxErrorCode.REDIRECT: status.HTTP_302_FOUND,
    # Client errors
    BoxErrorCode.BAD_REQUEST: status.HTTP_400_BAD_REQUEST,
    BoxErrorCode.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
    BoxErrorCode.FORBIDDEN: status.HTTP_403_FORBIDDEN,
    BoxErrorCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    BoxErrorCode.METHOD_NOT_ALLOWED: status.HTTP_405_METHOD_NOT_ALLOWED,
    BoxErrorCode.CONFLICT: status.HTTP_409_CONFLICT,
    BoxErrorCode.PRECONDITION_FAILED: status.HTTP_412_PRECONDITION_FAILED,
    BoxErrorCode.TOO_MANY_REQUESTS: status.HTTP_429_TOO_MANY_REQUESTS,
    # Server errors
    BoxErrorCode.INTERNAL_SERVER_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    BoxErrorCode.UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
    # Box-specific codes map to their logical HTTP status
    BoxErrorCode.ITEM_NAME_INVALID: status.HTTP_400_BAD_REQUEST,
    BoxErrorCode.ITEM_NAME_TOO_LONG: status.HTTP_400_BAD_REQUEST,
    BoxErrorCode.INSUFFICIENT_SCOPE: status.HTTP_403_FORBIDDEN,
    BoxErrorCode.ACCESS_DENIED_INSUFFICIENT_PERMISSIONS: status.HTTP_403_FORBIDDEN,
    BoxErrorCode.STORAGE_LIMIT_EXCEEDED: status.HTTP_403_FORBIDDEN,
    BoxErrorCode.CYCLICAL_FOLDER_STRUCTURE: status.HTTP_400_BAD_REQUEST,
    BoxErrorCode.NAME_TEMPORARILY_RESERVED: status.HTTP_409_CONFLICT,
    BoxErrorCode.OPERATION_BLOCKED_TEMPORARY: status.HTTP_503_SERVICE_UNAVAILABLE,
}


class BoxAPIError(Exception):
    """Exception for Box API errors."""

    def __init__(
        self,
        code: BoxErrorCode,
        message: str,
        status_code: int | None = None,
        context_info: dict[str, Any] | None = None,
        request_id: str | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code or ERROR_STATUS_MAP.get(
            code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.context_info = context_info
        self.request_id = request_id or generate_request_id()
        super().__init__(message)

    def to_response(self) -> dict[str, Any]:
        """Convert exception to Box API error response format."""
        return box_error_response(
            code=self.code,
            message=self.message,
            status_code=self.status_code,
            context_info=self.context_info,
            request_id=self.request_id,
        )


def box_error_response(
    code: BoxErrorCode,
    message: str,
    status_code: int | None = None,
    context_info: dict[str, Any] | None = None,
    request_id: str | None = None,
    help_url: str | None = None,
) -> dict[str, Any]:
    """
    Create a Box-style error response.

    Based on validated Box API error format:
    {
        "type": "error",
        "status": 404,
        "code": "not_found",
        "message": "Item not found",
        "request_id": "abc123"
    }
    """
    response: dict[str, Any] = {
        "type": "error",
        "status": status_code
        or ERROR_STATUS_MAP.get(code, status.HTTP_500_INTERNAL_SERVER_ERROR),
        "code": code.value,
        "message": message,
        "request_id": request_id or generate_request_id(),
    }

    if context_info:
        response["context_info"] = context_info

    if help_url:
        response["help_url"] = help_url
    else:
        response["help_url"] = (
            "https://developer.box.com/guides/api-calls/permissions-and-errors/common-errors/"
        )

    return response


def box_conflict_error(
    message: str,
    conflicts: list[dict[str, Any]] | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """
    Create a Box conflict error response with conflicts list.

    Used when a file/folder name already exists.
    """
    response = box_error_response(
        code=BoxErrorCode.CONFLICT,
        message=message,
        status_code=status.HTTP_409_CONFLICT,
        request_id=request_id,
    )

    if conflicts:
        response["context_info"] = {"conflicts": conflicts}

    return response


# Convenience functions for common errors
def not_found_error(resource_type: str, resource_id: str) -> BoxAPIError:
    """Create a not found error."""
    return BoxAPIError(
        code=BoxErrorCode.NOT_FOUND,
        message=f"Not Found - The {resource_type} with ID '{resource_id}' was not found.",
    )


def unauthorized_error(message: str = "Unauthorized") -> BoxAPIError:
    """Create an unauthorized error."""
    return BoxAPIError(
        code=BoxErrorCode.UNAUTHORIZED,
        message=message,
    )


def forbidden_error(message: str = "Access denied") -> BoxAPIError:
    """Create a forbidden error."""
    return BoxAPIError(
        code=BoxErrorCode.FORBIDDEN,
        message=message,
    )


def bad_request_error(message: str) -> BoxAPIError:
    """Create a bad request error."""
    return BoxAPIError(
        code=BoxErrorCode.BAD_REQUEST,
        message=message,
    )


def conflict_error(
    message: str, conflicts: list[dict[str, Any]] | dict[str, Any] | None = None
) -> BoxAPIError:
    """
    Create a conflict error.

    Real Box API behavior (verified):
    - Files: conflicts is a single OBJECT
    - Folders: conflicts is an ARRAY
    """
    return BoxAPIError(
        code=BoxErrorCode.CONFLICT,
        message=message,
        context_info={"conflicts": conflicts} if conflicts else None,
    )
