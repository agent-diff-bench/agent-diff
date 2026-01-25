"""
Box API Enums - Based on validated Box SDK and OpenAPI specifications.
"""

from enum import Enum


class BoxItemType(str, Enum):
    """Type discriminators for Box items."""

    FILE = "file"
    FOLDER = "folder"
    USER = "user"
    COMMENT = "comment"
    TASK = "task"
    HUB = "hubs"  # Note: Box uses "hubs" not "hub"
    WEB_LINK = "web_link"
    ERROR = "error"
    FILE_VERSION = "file_version"
    TASK_ASSIGNMENT = "task_assignment"


class BoxErrorCode(str, Enum):
    """
    Box API error codes - from SDK ClientErrorCodeField enum.
    """

    # Success codes (not errors, but part of code enum)
    CREATED = "created"
    ACCEPTED = "accepted"
    NO_CONTENT = "no_content"
    REDIRECT = "redirect"
    NOT_MODIFIED = "not_modified"

    # Client errors (4xx)
    BAD_REQUEST = "bad_request"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    METHOD_NOT_ALLOWED = "method_not_allowed"
    CONFLICT = "conflict"
    PRECONDITION_FAILED = "precondition_failed"
    TOO_MANY_REQUESTS = "too_many_requests"

    # Server errors (5xx)
    INTERNAL_SERVER_ERROR = "internal_server_error"
    UNAVAILABLE = "unavailable"

    # Box-specific error codes
    ITEM_NAME_INVALID = "item_name_invalid"
    ITEM_NAME_IN_USE = "item_name_in_use"
    ITEM_NAME_TOO_LONG = "item_name_too_long"
    INSUFFICIENT_SCOPE = "insufficient_scope"
    ACCESS_DENIED_INSUFFICIENT_PERMISSIONS = "access_denied_insufficient_permissions"
    STORAGE_LIMIT_EXCEEDED = "storage_limit_exceeded"
    CYCLICAL_FOLDER_STRUCTURE = "cyclical_folder_structure"
    NAME_TEMPORARILY_RESERVED = "name_temporarily_reserved"
    OPERATION_BLOCKED_TEMPORARY = "operation_blocked_temporary"


class BoxItemStatus(str, Enum):
    """Status for files and folders."""

    ACTIVE = "active"
    TRASHED = "trashed"
    DELETED = "deleted"


class BoxUserStatus(str, Enum):
    """Status for users."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    CANNOT_DELETE_EDIT = "cannot_delete_edit"
    CANNOT_DELETE_EDIT_UPLOAD = "cannot_delete_edit_upload"


class BoxTaskAction(str, Enum):
    """Task action types."""

    REVIEW = "review"
    COMPLETE = "complete"


class BoxTaskCompletionRule(str, Enum):
    """Task completion rule."""

    ALL_ASSIGNEES = "all_assignees"
    ANY_ASSIGNEE = "any_assignee"


class BoxSharedLinkAccess(str, Enum):
    """Shared link access levels."""

    OPEN = "open"
    COMPANY = "company"
    COLLABORATORS = "collaborators"


class BoxSortDirection(str, Enum):
    """Sort direction for collections."""

    ASC = "ASC"
    DESC = "DESC"
