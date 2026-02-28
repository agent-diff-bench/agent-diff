"""
Unified Error Classifier for API Responses
Supports: Google Calendar, Box, Slack, Linear

Usage:
    from unified_error_classifier import classify_response

    result = classify_response(stdout, app_name="linear")
    # Returns: {"has_error": bool, "error_type": str, "error_code": str|None, "details": str|None}
"""

import re
import json
from typing import Optional, Dict, Any
from enum import Enum


# =============================================================================
# UNIFIED ERROR TYPES (consistent across all apps)
# =============================================================================

class ErrorType(str, Enum):
    NO_ERROR = "no_error"
    AUTHENTICATION = "authentication"      # 401, invalid auth, token issues
    PERMISSION = "permission"              # 403, forbidden, insufficient access
    NOT_FOUND = "not_found"                # 404, resource doesn't exist
    BAD_REQUEST = "bad_request"            # 400, invalid input, malformed
    RATE_LIMIT = "rate_limit"              # 429, quota exceeded, too many requests
    CONFLICT = "conflict"                  # 409, duplicate, already exists
    GONE = "gone"                          # 410, deleted, no longer available
    SERVER_ERROR = "server_error"          # 500+, internal error, backend failure
    TEMPORARY = "temporary"                # Transient errors, retry later
    UNKNOWN = "unknown"                    # Error detected but unclassified


# =============================================================================
# SHARED UTILITIES
# =============================================================================

def classify_http_code(code: int) -> ErrorType:
    """Classify error type based on HTTP status code."""
    if code == 400:
        return ErrorType.BAD_REQUEST
    elif code == 401:
        return ErrorType.AUTHENTICATION
    elif code == 403:
        return ErrorType.PERMISSION
    elif code == 404:
        return ErrorType.NOT_FOUND
    elif code == 405:
        return ErrorType.BAD_REQUEST
    elif code == 409:
        return ErrorType.CONFLICT
    elif code == 410:
        return ErrorType.GONE
    elif code == 412:
        return ErrorType.CONFLICT  # Precondition Failed (ETag mismatch)
    elif code == 429:
        return ErrorType.RATE_LIMIT
    elif 500 <= code < 600:
        return ErrorType.SERVER_ERROR
    elif 400 <= code < 500:
        return ErrorType.BAD_REQUEST
    else:
        return ErrorType.UNKNOWN


def check_raw_http_response(response: str) -> Optional[Dict[str, Any]]:
    """Check for raw HTTP responses like 'HTTP/1.1 404 Not Found' or 'HTTP/1.1 302 Found'.

    Returns:
        - Error result for 4xx/5xx status codes
        - no_error_result for 2xx/3xx status codes (success/redirect)
        - None if not an HTTP response
    """
    # Check if response starts with HTTP status line
    match = re.match(r'^HTTP/[\d.]+\s+(\d{3})\s+(.*)$', response.strip(), re.MULTILINE)
    if match:
        code = int(match.group(1))
        if code >= 400:
            status_text = match.group(2).strip()
            return error_result(classify_http_code(code), str(code), f"HTTP {code} {status_text}")
        else:
            # 2xx success or 3xx redirect - not an error
            return no_error_result()
    return None


def strip_ansi_codes(text: str) -> str:
    """Strip ANSI escape codes from text."""
    import re
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


def try_parse_json_with_noise(response: str) -> Optional[dict]:
    """Try to parse JSON that may have prefix or trailing non-JSON text, or ANSI codes."""
    # Strip ANSI color codes if present
    if '\x1b[' in response:
        response = strip_ansi_codes(response)

    # First try normal parse
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    # Try parsing just the first line (common pattern: JSON + newline + status)
    first_line = response.split('\n')[0].strip()
    if first_line.startswith('{'):
        try:
            return json.loads(first_line)
        except json.JSONDecodeError:
            pass

    # Try finding JSON object boundaries (handles trailing text)
    if response.startswith('{'):
        depth = 0
        for i, char in enumerate(response):
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(response[:i+1])
                    except json.JSONDecodeError:
                        break

    # Try finding JSON with prefix text (e.g., "Testing...\n{...}")
    json_start = response.find('{')
    if json_start > 0:
        json_part = response[json_start:]
        # Try parsing from the first { to end
        try:
            return json.loads(json_part)
        except json.JSONDecodeError:
            pass
        # Try finding the matching closing brace
        depth = 0
        for i, char in enumerate(json_part):
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(json_part[:i+1])
                    except json.JSONDecodeError:
                        break

    return None


def no_error_result() -> Dict[str, Any]:
    return {"has_error": False, "error_type": ErrorType.NO_ERROR.value, "error_code": None, "details": None}


def error_result(error_type: ErrorType, error_code: str, details: Optional[str] = None) -> Dict[str, Any]:
    return {"has_error": True, "error_type": error_type.value, "error_code": error_code, "details": details}


# =============================================================================
# GOOGLE CALENDAR CLASSIFIER
# =============================================================================

def classify_gcal_response(response: str) -> Dict[str, Any]:
    """Classify Google Calendar API response."""
    if not response or len(response) < 5:
        return no_error_result()

    # Check for raw HTTP error response
    http_error = check_raw_http_response(response)
    if http_error:
        return http_error

    # Check for batch response with HTTP errors inside
    batch_error = _check_gcal_batch_errors(response)
    if batch_error:
        return batch_error

    # Check for Gmail/Google HTML error page
    match = re.search(r'var\s+gmail_server_error\s*=\s*(\d+)', response)
    if match:
        code = match.group(1)
        http_match = re.search(r'Temporary\s+Error\s*\((\d{3})\)', response)
        http_code = int(http_match.group(1)) if http_match else None
        error_type = classify_http_code(http_code) if http_code else ErrorType.TEMPORARY
        return error_result(error_type, code, f"Gmail server error {code}" + (f" (HTTP {http_code})" if http_code else ""))

    # Check for "Temporary Error (XXX)" pattern
    match = re.search(r'Temporary\s+Error\s*\((\d{3})\)', response)
    if match:
        http_code = int(match.group(1))
        return error_result(classify_http_code(http_code), str(http_code), f"Temporary Error (HTTP {http_code})")

    # Check for Google API JSON error (with support for trailing text)
    data = try_parse_json_with_noise(response)
    if not data or not isinstance(data, dict):
        return no_error_result()

    # Handle Slack-style format: {"ok": false, "error": "..."}
    if data.get("ok") is False:
        error_msg = data.get("error", "unknown_error")
        error_type = _classify_gcal_by_message(str(error_msg))
        return error_result(error_type, str(error_msg), None)

    error_obj = data.get("error")
    if not error_obj:
        return no_error_result()

    # Handle string error: {"error": "message"}
    if isinstance(error_obj, str):
        error_type = _classify_gcal_by_message(error_obj)
        return error_result(error_type, "error", error_obj)

    if not isinstance(error_obj, dict):
        return no_error_result()

    http_code = error_obj.get("code")
    message = error_obj.get("message", "")

    # Extract reason
    reason = None
    errors_list = error_obj.get("errors", [])
    if isinstance(errors_list, list) and errors_list:
        first_error = errors_list[0]
        if isinstance(first_error, dict):
            reason = first_error.get("reason")

    # Determine error type: try reason first, then message, then HTTP code
    if reason:
        error_type = _classify_google_reason(reason)
        # If reason is unknown, try message-based classification
        if error_type == ErrorType.UNKNOWN and message:
            error_type = _classify_gcal_by_message(message)
    elif message:
        # No reason code - try message first, then HTTP code
        error_type = _classify_gcal_by_message(message)
        if error_type == ErrorType.UNKNOWN and isinstance(http_code, int) and http_code >= 400:
            error_type = classify_http_code(http_code)
    elif isinstance(http_code, int) and http_code >= 400:
        error_type = classify_http_code(http_code)
    else:
        return no_error_result()

    return error_result(error_type, reason or str(http_code) if http_code else "error", message)


def _check_gcal_batch_errors(response: str) -> Optional[Dict[str, Any]]:
    """Check for batch response containing HTTP errors."""
    # Look for HTTP error status lines in batch responses
    # Pattern: HTTP/1.1 4xx or HTTP/1.1 5xx within the response
    if '--batch' not in response and 'Content-Type: application/http' not in response:
        return None

    # Find all HTTP status lines in the batch
    http_matches = re.findall(r'HTTP/[\d.]+\s+(\d{3})\s+([^\r\n]*)', response)
    for code_str, status_text in http_matches:
        code = int(code_str)
        if code >= 400:
            return error_result(classify_http_code(code), str(code), f"Batch HTTP {code} {status_text}")

    return None


def _classify_google_reason(reason: str) -> ErrorType:
    """Classify Google API reason code."""
    reason_lower = reason.lower()

    # Authentication
    if reason_lower in ("autherror", "invalidcredentials", "unauthorized"):
        return ErrorType.AUTHENTICATION
    if "auth" in reason_lower and "error" in reason_lower:
        return ErrorType.AUTHENTICATION

    # Permission
    if reason_lower in ("forbidden", "insufficientpermissions", "accessnotconfigured"):
        return ErrorType.PERMISSION
    if "permission" in reason_lower or "forbidden" in reason_lower:
        return ErrorType.PERMISSION

    # Gone/deleted
    if reason_lower in ("gone", "deleted", "moved", "resourcedeleted"):
        return ErrorType.GONE
    if "deleted" in reason_lower or "removed" in reason_lower:
        return ErrorType.GONE

    # Not found
    if "notfound" in reason_lower or "not_found" in reason_lower:
        return ErrorType.NOT_FOUND

    # Bad request
    if reason_lower in ("invalid", "invalidvalue", "required", "badrequest") or "invalid" in reason_lower:
        return ErrorType.BAD_REQUEST

    # Rate limit
    if "ratelimit" in reason_lower or "quota" in reason_lower:
        return ErrorType.RATE_LIMIT

    # Conflict
    if reason_lower in ("duplicate", "conflict", "conditionnotmet", "preconditionfailed") or "already" in reason_lower:
        return ErrorType.CONFLICT
    if "etag" in reason_lower or "mismatch" in reason_lower:
        return ErrorType.CONFLICT

    # Server error
    if reason_lower in ("internalerror", "backenderror", "serviceunavailable"):
        return ErrorType.SERVER_ERROR
    if "internal" in reason_lower or "server" in reason_lower or "backend" in reason_lower:
        return ErrorType.SERVER_ERROR

    return ErrorType.UNKNOWN


def _classify_gcal_by_message(message: str) -> ErrorType:
    """Classify Google Calendar error by message content."""
    msg_lower = message.lower()

    # Server/infrastructure errors (environment deleted = server-side issue)
    if "internal" in msg_lower or "server error" in msg_lower or "backend" in msg_lower:
        return ErrorType.SERVER_ERROR
    if "environment" in msg_lower and "deleted" in msg_lower:
        return ErrorType.SERVER_ERROR
    if "unavailable" in msg_lower:
        return ErrorType.TEMPORARY

    # Gone/deleted (user-deleted resources, not infrastructure)
    if "deleted" in msg_lower or "removed" in msg_lower:
        return ErrorType.GONE
    if "no longer" in msg_lower:
        return ErrorType.GONE

    # Not found
    if "not found" in msg_lower or "does not exist" in msg_lower:
        return ErrorType.NOT_FOUND

    # Permission
    if "forbidden" in msg_lower or "permission" in msg_lower or "access denied" in msg_lower:
        return ErrorType.PERMISSION

    # Authentication
    if "unauthorized" in msg_lower or "authentication" in msg_lower:
        return ErrorType.AUTHENTICATION

    # Bad request
    if "invalid" in msg_lower or "bad request" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "unsupported" in msg_lower or "unknown method" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "no" in msg_lower and "passed" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "no" in msg_lower and "specified" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "not_supplied" in msg_lower or "not supplied" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "not provided" in msg_lower or "required" in msg_lower:
        return ErrorType.BAD_REQUEST

    # Conflict
    if "already exists" in msg_lower or "duplicate" in msg_lower:
        return ErrorType.CONFLICT

    # Rate limit
    if "rate" in msg_lower and "limit" in msg_lower:
        return ErrorType.RATE_LIMIT
    if "quota" in msg_lower:
        return ErrorType.RATE_LIMIT

    return ErrorType.UNKNOWN


# =============================================================================
# BOX CLASSIFIER
# =============================================================================

BOX_ERROR_CODES = {
    # 400 Bad Request
    "bad_digest": ErrorType.BAD_REQUEST,
    "bad_request": ErrorType.BAD_REQUEST,
    "cannot_make_collaborated_subfolder_private": ErrorType.BAD_REQUEST,
    "collaborations_not_available_on_root_folder": ErrorType.BAD_REQUEST,
    "cyclical_folder_structure": ErrorType.BAD_REQUEST,
    "folder_not_empty": ErrorType.BAD_REQUEST,
    "invalid_collaboration_item": ErrorType.BAD_REQUEST,
    "invalid_grant": ErrorType.AUTHENTICATION,
    "invalid_limit": ErrorType.BAD_REQUEST,
    "invalid_offset": ErrorType.BAD_REQUEST,
    "invalid_request_parameters": ErrorType.BAD_REQUEST,
    "invalid_status": ErrorType.BAD_REQUEST,
    "invalid_upload_session_id": ErrorType.BAD_REQUEST,
    "item_name_invalid": ErrorType.BAD_REQUEST,
    "item_name_too_long": ErrorType.BAD_REQUEST,
    "metadata_after_file_contents": ErrorType.BAD_REQUEST,
    "password_reset_required": ErrorType.AUTHENTICATION,
    "requested_page_out_of_range": ErrorType.BAD_REQUEST,
    "requested_preview_unavailable": ErrorType.BAD_REQUEST,
    "sync_item_move_failure": ErrorType.BAD_REQUEST,
    "task_assignee_not_allowed": ErrorType.PERMISSION,
    "terms_of_service_required": ErrorType.BAD_REQUEST,
    "user_already_collaborator": ErrorType.CONFLICT,
    # 401 Unauthorized
    "unauthorized": ErrorType.AUTHENTICATION,
    # 403 Forbidden
    "access_denied_insufficient_permissions": ErrorType.PERMISSION,
    "insufficient_scope": ErrorType.PERMISSION,
    "access_denied_item_locked": ErrorType.PERMISSION,
    "access_from_location_blocked": ErrorType.PERMISSION,
    "file_size_limit_exceeded": ErrorType.PERMISSION,
    "forbidden": ErrorType.PERMISSION,
    "forbidden_by_policy": ErrorType.PERMISSION,
    "incorrect_shared_item_password": ErrorType.AUTHENTICATION,
    "storage_limit_exceeded": ErrorType.PERMISSION,
    "user_email_confirmation_required": ErrorType.AUTHENTICATION,
    "cors_origin_not_whitelisted": ErrorType.PERMISSION,
    # 404 Not Found
    "not_found": ErrorType.NOT_FOUND,
    "not_trashed": ErrorType.NOT_FOUND,
    "preview_cannot_be_generated": ErrorType.NOT_FOUND,
    "trashed": ErrorType.GONE,
    # 405 Method Not Allowed
    "method_not_allowed": ErrorType.BAD_REQUEST,
    # 409 Conflict
    "conflict": ErrorType.CONFLICT,
    "item_name_in_use": ErrorType.CONFLICT,
    "name_temporarily_reserved": ErrorType.CONFLICT,
    "operation_blocked_temporary": ErrorType.CONFLICT,
    "recent_similar_comment": ErrorType.CONFLICT,
    "user_login_already_used": ErrorType.CONFLICT,
    # 410 Gone
    "session_expired": ErrorType.GONE,
    "upload_failed": ErrorType.GONE,
    # 411-415
    "length_required": ErrorType.BAD_REQUEST,
    "precondition_failed": ErrorType.CONFLICT,
    "sync_state_precondition_failed": ErrorType.CONFLICT,
    "request_entity_too_large": ErrorType.BAD_REQUEST,
    "unsupported_media_type": ErrorType.BAD_REQUEST,
    # 429 Rate Limit
    "rate_limit_exceeded": ErrorType.RATE_LIMIT,
    # 500+
    "internal_server_error": ErrorType.SERVER_ERROR,
    "bad_gateway": ErrorType.SERVER_ERROR,
    "unavailable": ErrorType.SERVER_ERROR,
}


def classify_box_response(response: str) -> Dict[str, Any]:
    """Classify Box API response."""
    if not response or len(response) < 5:
        return no_error_result()

    # Check for raw HTTP error response
    http_error = check_raw_http_response(response)
    if http_error:
        return http_error

    # Try JSON error format (with support for trailing text/concatenated JSON)
    data = try_parse_json_with_noise(response)
    if data is None:
        # Check plain text/HTML errors and classify by content
        response_lower = response.lower()

        # Skip client-side JSON parsing errors (not API errors)
        # These occur when the API returns empty response (normal for DELETE) and script tries to parse
        if "expecting value" in response_lower and "line 1 column 1" in response_lower:
            return no_error_result()
        if "jsondecodeerror" in response_lower:
            return no_error_result()
        if "error parsing response" in response_lower:
            return no_error_result()

        # Skip clear success messages
        if "✓" in response and ("success" in response_lower or "valid" in response_lower or "completed" in response_lower):
            return no_error_result()

        # Skip Git LFS pointer files (valid file content, not errors)
        # Format: "version https://git-lfs.github.com/spec/v1\noid sha256:...\nsize ..."
        if "git-lfs.github.com/spec" in response_lower or (
            response_lower.startswith("version ") and "oid sha256:" in response_lower
        ):
            return no_error_result()

        # Skip markdown/document content (file content, not API errors)
        # Markdown headers indicate this is document content
        stripped = response.strip()
        if stripped.startswith("# ") or stripped.startswith("## ") or stripped.startswith("### "):
            return no_error_result()

        # Skip text documents with separator lines (===, ---, common log/report formats)
        lines = stripped.split('\n')
        if len(lines) >= 2:
            second_line = lines[1].strip() if len(lines) > 1 else ""
            # Check for underline-style headers (Title\n====== or Title\n------)
            if second_line and (all(c == '=' for c in second_line) or all(c == '-' for c in second_line)):
                if len(second_line) >= 3:  # At least 3 chars to be a separator
                    return no_error_result()

        # Check for HTTP error codes in script output (e.g., "HTTP_CODE:401", "HTTP Status: 401", "HTTP Code: 409")
        http_code_match = re.search(r'(?:HTTP[_\s]?CODE|HTTP[_\s]?Status)[:\s]*(\d{3})', response, re.IGNORECASE)
        if http_code_match:
            code = int(http_code_match.group(1))
            if code >= 400:
                return error_result(classify_http_code(code), str(code), f"HTTP {code} in script output")

        # Detect curl verbose output (-v flag) and extract actual HTTP status
        # Curl verbose format: "< HTTP/1.1 302 Found" for response status line
        if "* Host" in response or "* Trying" in response or "Note: Unnecessary use of -X" in response:
            # This is curl verbose output - look for the actual HTTP response status
            curl_status_match = re.search(r'< HTTP/[\d.]+\s+(\d{3})\s+', response)
            if curl_status_match:
                code = int(curl_status_match.group(1))
                if code >= 400:
                    return error_result(classify_http_code(code), str(code), f"HTTP {code} in curl output")
                else:
                    # 2xx/3xx = success/redirect
                    return no_error_result()
            # If we can't find HTTP status in curl output, don't treat as error
            return no_error_result()

        # Skip script/log output that isn't an API error
        # These contain execution logs, not API error responses
        if "curl " in response_lower or "command:" in response_lower:
            # Check if it's actually reporting success
            if "return code: 0" in response_lower or "✓" in response or "success" in response_lower:
                return no_error_result()

        # Skip if it looks like shell script output (starts with === or ---)
        if response.strip().startswith("===") or response.strip().startswith("---"):
            if "error" not in response_lower[:100]:  # Only skip if no error in first 100 chars
                return no_error_result()

        # Gone/removed resources (common in Box HTML error pages)
        if "has been removed" in response_lower or "been deleted" in response_lower:
            return error_result(ErrorType.GONE, "RESOURCE_REMOVED", f"Resource removed: {response[:200]}")
        if "no longer available" in response_lower or "no longer exists" in response_lower:
            return error_result(ErrorType.GONE, "RESOURCE_GONE", f"Resource gone: {response[:200]}")

        # Not found
        if "not found" in response_lower or "does not exist" in response_lower:
            return error_result(ErrorType.NOT_FOUND, "NOT_FOUND", f"Not found: {response[:200]}")

        # Permission/auth
        if "forbidden" in response_lower or "access denied" in response_lower:
            return error_result(ErrorType.PERMISSION, "FORBIDDEN", f"Permission denied: {response[:200]}")
        if "unauthorized" in response_lower or "authentication" in response_lower:
            return error_result(ErrorType.AUTHENTICATION, "UNAUTHORIZED", f"Auth error: {response[:200]}")

        # Server errors - check for explicit error messages, not just status codes
        # (status codes might appear in URLs like /files/9979104500/)
        if "internal server error" in response_lower:
            return error_result(ErrorType.SERVER_ERROR, "SERVER_ERROR", f"Server error: {response[:200]}")
        if "service unavailable" in response_lower:
            return error_result(ErrorType.SERVER_ERROR, "SERVICE_UNAVAILABLE", f"Service unavailable: {response[:200]}")

        # Check for simple "Error: XXX" pattern where XXX is HTTP status code
        simple_error_match = re.match(r'^Error:\s*(\d{3})\s*$', response.strip(), re.IGNORECASE)
        if simple_error_match:
            code = int(simple_error_match.group(1))
            return error_result(classify_http_code(code), str(code), f"Error {code}")

        # Generic error detection
        if "error" in response_lower:
            return error_result(ErrorType.UNKNOWN, "PLAIN_TEXT_ERROR", f"Plain text error: {response[:200]}")

        return no_error_result()

    if not isinstance(data, dict):
        return no_error_result()

    # Check for batch results format: {"results":[{"status":"error",...}]}
    results = data.get("results")
    if isinstance(results, list) and results:
        for result in results:
            if isinstance(result, dict) and result.get("status") == "error":
                message = result.get("message", "")
                # Try to extract error type from message
                msg_lower = message.lower()
                if "not found" in msg_lower:
                    return error_result(ErrorType.NOT_FOUND, "batch_not_found", message)
                elif "unauthorized" in msg_lower or "authentication" in msg_lower:
                    return error_result(ErrorType.AUTHENTICATION, "batch_auth_error", message)
                elif "forbidden" in msg_lower or "permission" in msg_lower:
                    return error_result(ErrorType.PERMISSION, "batch_permission_error", message)
                elif "deleted" in msg_lower or "trashed" in msg_lower:
                    return error_result(ErrorType.GONE, "batch_gone", message)
                elif "internal" in msg_lower or "server error" in msg_lower:
                    return error_result(ErrorType.SERVER_ERROR, "batch_server_error", message)
                elif "invalid" in msg_lower or "bad request" in msg_lower:
                    return error_result(ErrorType.BAD_REQUEST, "batch_bad_request", message)
                elif "conflict" in msg_lower or "already exists" in msg_lower or "already in" in msg_lower:
                    return error_result(ErrorType.CONFLICT, "batch_conflict", message)
                else:
                    return error_result(ErrorType.UNKNOWN, "batch_error", message)

    # Box error format: {"type": "error", "status": 404, "code": "not_found", "message": "..."}
    if data.get("type") == "error":
        code = data.get("code", "").lower()
        status = data.get("status")
        message = data.get("message", "")

        if code in BOX_ERROR_CODES:
            error_type = BOX_ERROR_CODES[code]
        elif isinstance(status, int) and status >= 400:
            error_type = classify_http_code(status)
        else:
            error_type = ErrorType.UNKNOWN

        return error_result(error_type, code or str(status), message)

    # Alternative format: {"error": "...", "error_description": "..."}
    error_field = data.get("error")
    if error_field:
        code = str(error_field).lower().replace(" ", "_")
        message = data.get("error_description", data.get("message", ""))

        # Combine error and message for pattern matching
        full_text = f"{error_field} {message}".lower()

        if code in BOX_ERROR_CODES:
            error_type = BOX_ERROR_CODES[code]
        else:
            error_type = _classify_box_error_by_message(full_text)

        return error_result(error_type, code, message if message else str(error_field))

    return no_error_result()


def _classify_box_error_by_message(message: str) -> ErrorType:
    """Classify Box error by message content when no explicit code."""
    msg_lower = message.lower()

    # Server/infrastructure errors (environment deleted = server-side issue)
    if "internal" in msg_lower or "server error" in msg_lower:
        return ErrorType.SERVER_ERROR
    if "environment" in msg_lower and "deleted" in msg_lower:
        return ErrorType.SERVER_ERROR
    if "unavailable" in msg_lower or "temporarily" in msg_lower:
        return ErrorType.TEMPORARY

    # Gone/deleted (user-deleted resources, not infrastructure)
    if "deleted" in msg_lower or "trashed" in msg_lower or "removed" in msg_lower:
        return ErrorType.GONE
    if "no longer" in msg_lower or "expired" in msg_lower:
        return ErrorType.GONE

    # Not found
    if "not found" in msg_lower or "does not exist" in msg_lower:
        return ErrorType.NOT_FOUND
    if "no such" in msg_lower or "doesn't exist" in msg_lower:
        return ErrorType.NOT_FOUND

    # Permission
    if "forbidden" in msg_lower or "permission" in msg_lower or "access denied" in msg_lower:
        return ErrorType.PERMISSION
    if "not allowed" in msg_lower:
        return ErrorType.PERMISSION

    # Authentication
    if "unauthorized" in msg_lower or "authentication" in msg_lower:
        return ErrorType.AUTHENTICATION
    if "invalid token" in msg_lower or "token expired" in msg_lower:
        return ErrorType.AUTHENTICATION

    # Bad request
    if "invalid" in msg_lower or "bad request" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "malformed" in msg_lower or "missing" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "unsupported" in msg_lower or "unknown method" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "no" in msg_lower and "passed" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "no" in msg_lower and "specified" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "not_supplied" in msg_lower or "not supplied" in msg_lower:
        return ErrorType.BAD_REQUEST
    if "not provided" in msg_lower or "required" in msg_lower:
        return ErrorType.BAD_REQUEST

    # Conflict
    if "already exists" in msg_lower or "duplicate" in msg_lower:
        return ErrorType.CONFLICT
    if "conflict" in msg_lower:
        return ErrorType.CONFLICT

    # Rate limit
    if "rate" in msg_lower and "limit" in msg_lower:
        return ErrorType.RATE_LIMIT
    if "too many" in msg_lower:
        return ErrorType.RATE_LIMIT

    return ErrorType.UNKNOWN


# =============================================================================
# SLACK CLASSIFIER
# =============================================================================

SLACK_ERROR_CODES = {
    # Authentication
    "invalid_auth": ErrorType.AUTHENTICATION,
    "not_authed": ErrorType.AUTHENTICATION,
    "account_inactive": ErrorType.AUTHENTICATION,
    "token_revoked": ErrorType.AUTHENTICATION,
    "token_expired": ErrorType.AUTHENTICATION,
    "not_allowed_token_type": ErrorType.AUTHENTICATION,
    "org_login_required": ErrorType.AUTHENTICATION,
    "invalid_token": ErrorType.AUTHENTICATION,
    "team_access_not_granted": ErrorType.AUTHENTICATION,
    # Permission
    "no_permission": ErrorType.PERMISSION,
    "missing_scope": ErrorType.PERMISSION,
    "ekm_access_denied": ErrorType.PERMISSION,
    "enterprise_is_restricted": ErrorType.PERMISSION,
    "not_in_channel": ErrorType.PERMISSION,
    "is_archived": ErrorType.PERMISSION,
    "channel_is_archived": ErrorType.PERMISSION,
    "restricted_action": ErrorType.PERMISSION,
    "restricted_action_read_only_channel": ErrorType.PERMISSION,
    "restricted_action_thread_only_channel": ErrorType.PERMISSION,
    "restricted_action_non_threadable_channel": ErrorType.PERMISSION,
    "not_allowed": ErrorType.PERMISSION,
    "posting_to_general_channel_denied": ErrorType.PERMISSION,
    "as_user_not_supported": ErrorType.PERMISSION,
    "cannot_dm_bot": ErrorType.PERMISSION,
    "cant_update_message": ErrorType.PERMISSION,
    "cant_delete_message": ErrorType.PERMISSION,
    "cant_invite": ErrorType.PERMISSION,
    "cant_kick_from_general": ErrorType.PERMISSION,
    "cant_kick_from_last_channel": ErrorType.PERMISSION,
    "cant_archive_general": ErrorType.PERMISSION,
    "cant_leave_general": ErrorType.PERMISSION,
    "last_member": ErrorType.PERMISSION,
    "access_denied": ErrorType.PERMISSION,
    "user_is_restricted": ErrorType.PERMISSION,
    "user_is_ultra_restricted": ErrorType.PERMISSION,
    "user_is_bot": ErrorType.PERMISSION,
    "channel_not_allowed": ErrorType.PERMISSION,
    "compliance_exports_prevent_deletion": ErrorType.PERMISSION,
    # Not Found
    "channel_not_found": ErrorType.NOT_FOUND,
    "user_not_found": ErrorType.NOT_FOUND,
    "users_not_found": ErrorType.NOT_FOUND,
    "no_user": ErrorType.NOT_FOUND,
    "message_not_found": ErrorType.NOT_FOUND,
    "file_not_found": ErrorType.NOT_FOUND,
    "team_not_found": ErrorType.NOT_FOUND,
    "thread_not_found": ErrorType.NOT_FOUND,
    "app_not_found": ErrorType.NOT_FOUND,
    "bot_not_found": ErrorType.NOT_FOUND,
    "view_not_found": ErrorType.NOT_FOUND,
    "trigger_not_found": ErrorType.NOT_FOUND,
    "workflow_not_found": ErrorType.NOT_FOUND,
    "no_reaction": ErrorType.NOT_FOUND,
    "emoji_not_found": ErrorType.NOT_FOUND,
    "pin_not_found": ErrorType.NOT_FOUND,
    "bookmark_not_found": ErrorType.NOT_FOUND,
    "reminder_not_found": ErrorType.NOT_FOUND,
    "conversation_not_found": ErrorType.NOT_FOUND,
    # Bad Request
    "invalid_arguments": ErrorType.BAD_REQUEST,
    "invalid_arg_name": ErrorType.BAD_REQUEST,
    "invalid_array_arg": ErrorType.BAD_REQUEST,
    "invalid_charset": ErrorType.BAD_REQUEST,
    "invalid_form_data": ErrorType.BAD_REQUEST,
    "invalid_post_type": ErrorType.BAD_REQUEST,
    "invalid_json": ErrorType.BAD_REQUEST,
    "invalid_name": ErrorType.BAD_REQUEST,
    "invalid_name_specials": ErrorType.BAD_REQUEST,
    "invalid_name_maxlength": ErrorType.BAD_REQUEST,
    "invalid_name_punctuation": ErrorType.BAD_REQUEST,
    "invalid_name_required": ErrorType.BAD_REQUEST,
    "invalid_cursor": ErrorType.BAD_REQUEST,
    "invalid_limit": ErrorType.BAD_REQUEST,
    "invalid_ts_latest": ErrorType.BAD_REQUEST,
    "invalid_ts_oldest": ErrorType.BAD_REQUEST,
    "invalid_timestamp": ErrorType.BAD_REQUEST,
    "invalid_blocks": ErrorType.BAD_REQUEST,
    "invalid_blocks_format": ErrorType.BAD_REQUEST,
    "invalid_attachments": ErrorType.BAD_REQUEST,
    "invalid_metadata_format": ErrorType.BAD_REQUEST,
    "invalid_metadata_schema": ErrorType.BAD_REQUEST,
    "too_many_attachments": ErrorType.BAD_REQUEST,
    "too_many_blocks": ErrorType.BAD_REQUEST,
    "too_many_users": ErrorType.BAD_REQUEST,
    "msg_too_long": ErrorType.BAD_REQUEST,
    "no_text": ErrorType.BAD_REQUEST,
    "missing_argument": ErrorType.BAD_REQUEST,
    "missing_channel": ErrorType.BAD_REQUEST,
    "missing_ts": ErrorType.BAD_REQUEST,
    "missing_user": ErrorType.BAD_REQUEST,
    "missing_message": ErrorType.BAD_REQUEST,
    "bad_timestamp": ErrorType.BAD_REQUEST,
    "method_not_supported_for_channel_type": ErrorType.BAD_REQUEST,
    "request_timeout": ErrorType.BAD_REQUEST,
    "unsupported_endpoint": ErrorType.BAD_REQUEST,
    "unknown_method": ErrorType.BAD_REQUEST,
    # Conflict
    "name_taken": ErrorType.CONFLICT,
    "already_reacted": ErrorType.CONFLICT,
    "already_pinned": ErrorType.CONFLICT,
    "already_starred": ErrorType.CONFLICT,
    "already_in_channel": ErrorType.CONFLICT,
    "already_archived": ErrorType.CONFLICT,
    "user_already_team_member": ErrorType.CONFLICT,
    "channel_already_exists": ErrorType.CONFLICT,
    "message_limit_exceeded": ErrorType.CONFLICT,
    "duplicate_channel_not_allowed": ErrorType.CONFLICT,
    "duplicate_message": ErrorType.CONFLICT,
    "edit_window_closed": ErrorType.CONFLICT,
    # Rate Limit
    "ratelimited": ErrorType.RATE_LIMIT,
    "rate_limited": ErrorType.RATE_LIMIT,
    "too_many_requests": ErrorType.RATE_LIMIT,
    # Server Error
    "internal_error": ErrorType.SERVER_ERROR,
    "fatal_error": ErrorType.SERVER_ERROR,
    "service_unavailable": ErrorType.SERVER_ERROR,
    # Temporary
    "temporarily_disabled": ErrorType.TEMPORARY,
    "team_added_to_org": ErrorType.TEMPORARY,
}


def classify_slack_response(response: str) -> Dict[str, Any]:
    """Classify Slack API response."""
    if not response or len(response) < 5:
        return no_error_result()

    # Check for raw HTTP error response
    http_error = check_raw_http_response(response)
    if http_error:
        return http_error

    # Strip ANSI color codes if present
    if '\x1b[' in response:
        response = strip_ansi_codes(response)

    # Try JSON
    try:
        data = json.loads(response)
    except (json.JSONDecodeError, TypeError):
        return no_error_result()

    if not isinstance(data, dict):
        return no_error_result()

    # Slack format: {"ok": false, "error": "error_code"}
    # Some errors use boolean flags instead: {"ok": false, "not_in_channel": true}
    if data.get("ok") is False:
        # Handle buggy test data: ok:false but message indicates success
        msg = data.get("message", "").lower()
        if "deleted" in msg and "error" not in data:
            return no_error_result()  # "Lunch message deleted" etc.
        error_code = data.get("error")

        # Check for boolean error indicators if no explicit error field
        if not error_code:
            boolean_error_fields = {
                "not_in_channel": ("not_in_channel", ErrorType.PERMISSION),
                "is_archived": ("channel_is_archived", ErrorType.PERMISSION),
                "channel_not_found": ("channel_not_found", ErrorType.NOT_FOUND),
                "user_not_found": ("user_not_found", ErrorType.NOT_FOUND),
                "already_reacted": ("already_reacted", ErrorType.CONFLICT),
                "no_reaction": ("no_reaction", ErrorType.NOT_FOUND),
                "cant_update_message": ("cant_update_message", ErrorType.PERMISSION),
                "cant_delete_message": ("cant_delete_message", ErrorType.PERMISSION),
            }
            for field, (code, err_type) in boolean_error_fields.items():
                if data.get(field) is True:
                    return error_result(err_type, code, None)
            error_code = "unknown_error"

        if error_code in SLACK_ERROR_CODES:
            error_type = SLACK_ERROR_CODES[error_code]
        else:
            error_type = _classify_unknown_slack_error(error_code)

        # Get additional details
        details = data.get("response_metadata", {}).get("messages", [])
        details_str = "; ".join(details) if details else data.get("needed", data.get("provided", None))

        return error_result(error_type, error_code, details_str)

    return no_error_result()


def _classify_unknown_slack_error(error_code: str) -> ErrorType:
    """Classify unknown Slack error by pattern."""
    code_lower = error_code.lower()

    # Server/infrastructure errors (environment deleted = server-side issue)
    if "internal" in code_lower or "server" in code_lower or "fatal" in code_lower:
        return ErrorType.SERVER_ERROR
    if "environment" in code_lower and "deleted" in code_lower:
        return ErrorType.SERVER_ERROR
    if "unavailable" in code_lower or "temporarily" in code_lower:
        return ErrorType.TEMPORARY

    # Gone/deleted resources (user-deleted resources, not infrastructure)
    if "deleted" in code_lower or "removed" in code_lower or "archived" in code_lower:
        return ErrorType.GONE

    # Not found
    if "not_found" in code_lower or code_lower.endswith("_not_found") or "not found" in code_lower:
        return ErrorType.NOT_FOUND
    if "no such" in code_lower or "does not exist" in code_lower or "doesn't exist" in code_lower:
        return ErrorType.NOT_FOUND

    # Bad request
    if code_lower.startswith("invalid_") or "invalid" in code_lower:
        return ErrorType.BAD_REQUEST
    if code_lower.startswith("missing_") or "missing" in code_lower:
        return ErrorType.BAD_REQUEST
    if "bad" in code_lower or "malformed" in code_lower:
        return ErrorType.BAD_REQUEST
    if "unsupported" in code_lower or "unknown_method" in code_lower:
        return ErrorType.BAD_REQUEST
    if "no" in code_lower and "passed" in code_lower:  # "No query passed", etc.
        return ErrorType.BAD_REQUEST
    if "no" in code_lower and "specified" in code_lower:  # "no_item_specified", etc.
        return ErrorType.BAD_REQUEST
    if "not_supplied" in code_lower or "not supplied" in code_lower:
        return ErrorType.BAD_REQUEST
    if "not provided" in code_lower or "required" in code_lower:
        return ErrorType.BAD_REQUEST

    # Conflict
    if "already_" in code_lower or "duplicate" in code_lower or "already exists" in code_lower:
        return ErrorType.CONFLICT

    # Rate limit
    if "rate" in code_lower or "limit" in code_lower or "throttl" in code_lower:
        return ErrorType.RATE_LIMIT

    # Permission
    if "permission" in code_lower or "denied" in code_lower or code_lower.startswith("cant_"):
        return ErrorType.PERMISSION
    if "forbidden" in code_lower or "not allowed" in code_lower:
        return ErrorType.PERMISSION

    # Authentication
    if "auth" in code_lower or "token" in code_lower or "credential" in code_lower:
        return ErrorType.AUTHENTICATION

    return ErrorType.UNKNOWN


# =============================================================================
# LINEAR CLASSIFIER
# =============================================================================

LINEAR_ERROR_CODES = {
    # Authentication
    "UNAUTHENTICATED": ErrorType.AUTHENTICATION,
    "UNAUTHORIZED": ErrorType.AUTHENTICATION,
    "INVALID_API_KEY": ErrorType.AUTHENTICATION,
    "API_KEY_EXPIRED": ErrorType.AUTHENTICATION,
    "TOKEN_EXPIRED": ErrorType.AUTHENTICATION,
    "INVALID_TOKEN": ErrorType.AUTHENTICATION,
    "AUTHENTICATION_ERROR": ErrorType.AUTHENTICATION,
    "AuthenticationError": ErrorType.AUTHENTICATION,
    # Permission
    "FORBIDDEN": ErrorType.PERMISSION,
    "ACCESS_DENIED": ErrorType.PERMISSION,
    "PERMISSION_DENIED": ErrorType.PERMISSION,
    "INSUFFICIENT_PERMISSIONS": ErrorType.PERMISSION,
    "ORGANIZATION_ACCESS_DENIED": ErrorType.PERMISSION,
    "TEAM_ACCESS_DENIED": ErrorType.PERMISSION,
    "FEATURE_NOT_ENABLED": ErrorType.PERMISSION,
    # Not Found
    "NOT_FOUND": ErrorType.NOT_FOUND,
    "ENTITY_NOT_FOUND": ErrorType.NOT_FOUND,
    "ISSUE_NOT_FOUND": ErrorType.NOT_FOUND,
    "PROJECT_NOT_FOUND": ErrorType.NOT_FOUND,
    "TEAM_NOT_FOUND": ErrorType.NOT_FOUND,
    "USER_NOT_FOUND": ErrorType.NOT_FOUND,
    "CYCLE_NOT_FOUND": ErrorType.NOT_FOUND,
    "LABEL_NOT_FOUND": ErrorType.NOT_FOUND,
    "COMMENT_NOT_FOUND": ErrorType.NOT_FOUND,
    "ATTACHMENT_NOT_FOUND": ErrorType.NOT_FOUND,
    "WORKFLOW_STATE_NOT_FOUND": ErrorType.NOT_FOUND,
    "MILESTONE_NOT_FOUND": ErrorType.NOT_FOUND,
    "ROADMAP_NOT_FOUND": ErrorType.NOT_FOUND,
    "INITIATIVE_NOT_FOUND": ErrorType.NOT_FOUND,
    "INTEGRATION_NOT_FOUND": ErrorType.NOT_FOUND,
    "WEBHOOK_NOT_FOUND": ErrorType.NOT_FOUND,
    # Bad Request
    "BAD_REQUEST": ErrorType.BAD_REQUEST,
    "INVALID_INPUT": ErrorType.BAD_REQUEST,
    "VALIDATION_ERROR": ErrorType.BAD_REQUEST,
    "GRAPHQL_VALIDATION_FAILED": ErrorType.BAD_REQUEST,
    "GRAPHQL_PARSE_FAILED": ErrorType.BAD_REQUEST,
    "GRAPHQL_ERROR": ErrorType.BAD_REQUEST,
    "INVALID_QUERY": ErrorType.BAD_REQUEST,
    "INVALID_MUTATION": ErrorType.BAD_REQUEST,
    "INVALID_ARGUMENT": ErrorType.BAD_REQUEST,
    "MISSING_ARGUMENT": ErrorType.BAD_REQUEST,
    "MISSING_REQUIRED_FIELD": ErrorType.BAD_REQUEST,
    "INVALID_FIELD_VALUE": ErrorType.BAD_REQUEST,
    "INVALID_ID": ErrorType.BAD_REQUEST,
    "INVALID_UUID": ErrorType.BAD_REQUEST,
    "INVALID_DATE": ErrorType.BAD_REQUEST,
    "INVALID_FILTER": ErrorType.BAD_REQUEST,
    "INVALID_SORT": ErrorType.BAD_REQUEST,
    "QUERY_TOO_COMPLEX": ErrorType.BAD_REQUEST,
    "VARIABLES_ERROR": ErrorType.BAD_REQUEST,
    # Conflict
    "CONFLICT": ErrorType.CONFLICT,
    "ALREADY_EXISTS": ErrorType.CONFLICT,
    "DUPLICATE": ErrorType.CONFLICT,
    "DUPLICATE_KEY": ErrorType.CONFLICT,
    "VERSION_CONFLICT": ErrorType.CONFLICT,
    "OPTIMISTIC_LOCK_ERROR": ErrorType.CONFLICT,
    "STATE_CONFLICT": ErrorType.CONFLICT,
    "ISSUE_ALREADY_ASSIGNED": ErrorType.CONFLICT,
    "LABEL_ALREADY_EXISTS": ErrorType.CONFLICT,
    # Rate Limit
    "RATE_LIMITED": ErrorType.RATE_LIMIT,
    "RATE_LIMIT_EXCEEDED": ErrorType.RATE_LIMIT,
    "TOO_MANY_REQUESTS": ErrorType.RATE_LIMIT,
    "COMPLEXITY_LIMIT_EXCEEDED": ErrorType.RATE_LIMIT,
    "QUERY_DEPTH_LIMIT_EXCEEDED": ErrorType.RATE_LIMIT,
    # Server Error
    "INTERNAL_ERROR": ErrorType.SERVER_ERROR,
    "INTERNAL_SERVER_ERROR": ErrorType.SERVER_ERROR,
    "SERVER_ERROR": ErrorType.SERVER_ERROR,
    "SERVICE_UNAVAILABLE": ErrorType.SERVER_ERROR,
    "TIMEOUT": ErrorType.SERVER_ERROR,
    "DATABASE_ERROR": ErrorType.SERVER_ERROR,
    "UNEXPECTED_ERROR": ErrorType.SERVER_ERROR,
    # Gone
    "ENTITY_DELETED": ErrorType.GONE,
    "ARCHIVED": ErrorType.GONE,
    "ISSUE_ARCHIVED": ErrorType.GONE,
    "PROJECT_ARCHIVED": ErrorType.GONE,
    # Temporary
    "NETWORK_ERROR": ErrorType.TEMPORARY,
    "CONNECTION_ERROR": ErrorType.TEMPORARY,
    "RETRY_LATER": ErrorType.TEMPORARY,
}


def classify_linear_response(response: str) -> Dict[str, Any]:
    """Classify Linear API response (GraphQL or REST)."""
    if not response or len(response) < 5:
        return no_error_result()

    # Check for raw HTTP error response
    http_error = check_raw_http_response(response)
    if http_error:
        return http_error

    # Strip ANSI color codes if present
    if '\x1b[' in response:
        response = strip_ansi_codes(response)

    # Try JSON
    try:
        data = json.loads(response)
    except (json.JSONDecodeError, TypeError):
        return no_error_result()

    if not isinstance(data, dict):
        return no_error_result()

    # GraphQL format: {"errors": [...]}
    errors = data.get("errors")
    if errors and isinstance(errors, list) and len(errors) > 0:
        first_error = errors[0]
        if isinstance(first_error, dict):
            message = first_error.get("message", "")
            extensions = first_error.get("extensions", {})

            # Get error code from extensions or infer from message
            error_code = None
            if isinstance(extensions, dict):
                error_code = extensions.get("code")

            if not error_code and message:
                error_code = _infer_linear_error_code(message)

            if not error_code:
                error_code = "GRAPHQL_ERROR"

            # Classify
            if error_code in LINEAR_ERROR_CODES:
                error_type = LINEAR_ERROR_CODES[error_code]
            else:
                error_type = _classify_unknown_linear_error(error_code, message)

            return error_result(error_type, error_code, message)

    # Handle Slack-style format: {"ok": false, "error": "..."}
    if data.get("ok") is False:
        error_msg = data.get("error", "unknown_error")
        if isinstance(error_msg, str):
            inferred_code = _infer_linear_error_code(error_msg)
            if inferred_code:
                error_type = LINEAR_ERROR_CODES.get(inferred_code, _classify_unknown_linear_error(inferred_code, error_msg))
                return error_result(error_type, inferred_code, error_msg)
            else:
                error_type = _classify_unknown_linear_error(error_msg, error_msg)
                return error_result(error_type, error_msg.upper().replace(" ", "_"), error_msg)

    # REST format: {"error": "..."}
    error_field = data.get("error")
    if error_field:
        if data.get("success") is True or (data.get("data") is not None and "errors" not in data):
            return no_error_result()

        message = data.get("message", "")
        status = data.get("status")

        if isinstance(error_field, str):
            error_code = error_field.upper().replace(" ", "_")
        elif isinstance(error_field, dict):
            # Dict error: {"code": "...", "message": "..."} or just {"message": "..."}
            if "code" in error_field:
                error_code = str(error_field["code"]).upper()
            elif "message" in error_field:
                # No code, use message for inference
                err_msg = error_field.get("message", "")
                inferred_code = _infer_linear_error_code(err_msg)
                if inferred_code:
                    error_type = LINEAR_ERROR_CODES.get(inferred_code, _classify_unknown_linear_error(inferred_code, err_msg))
                    return error_result(error_type, inferred_code, err_msg)
                else:
                    error_type = _classify_unknown_linear_error("", err_msg)
                    return error_result(error_type, "ERROR", err_msg)
            else:
                error_code = "UNKNOWN_ERROR"
                message = str(error_field)
        else:
            error_code = str(error_field).upper()

        # Combine message sources
        if not message and isinstance(error_field, str):
            message = error_field

        if error_code in LINEAR_ERROR_CODES:
            error_type = LINEAR_ERROR_CODES[error_code]
        elif isinstance(status, int) and status >= 400:
            error_type = classify_http_code(status)
        else:
            error_type = _classify_unknown_linear_error(error_code, message)

        return error_result(error_type, error_code, message)

    return no_error_result()


def _infer_linear_error_code(message: str) -> Optional[str]:
    """Infer error code from Linear GraphQL error message."""
    msg_lower = message.lower()

    # Server/infrastructure errors (check early - high priority)
    if "internal" in msg_lower or "server error" in msg_lower:
        return "INTERNAL_SERVER_ERROR"
    if "environment" in msg_lower and "deleted" in msg_lower:
        return "INTERNAL_SERVER_ERROR"  # Environment deleted = infrastructure issue
    if "timeout" in msg_lower:
        return "TIMEOUT"
    if "unavailable" in msg_lower:
        return "SERVICE_UNAVAILABLE"
    # Server-side data integrity issues (not client's fault)
    if "cannot return null for non-nullable" in msg_lower:
        return "INTERNAL_SERVER_ERROR"  # Schema/resolver returning unexpected null
    if "should be created automatically" in msg_lower:
        return "INTERNAL_SERVER_ERROR"  # Missing auto-created data (e.g., workflow states)

    # Gone/deleted/archived resources (user-deleted, not infrastructure)
    if "deleted" in msg_lower or "has been removed" in msg_lower:
        return "ENTITY_DELETED"
    if "archived" in msg_lower:
        return "ARCHIVED"
    if "no longer" in msg_lower:  # "no longer available", "no longer exists"
        return "ENTITY_DELETED"

    # GraphQL syntax/validation errors
    if "syntax error" in msg_lower:
        return "GRAPHQL_PARSE_FAILED"
    if "enum" in msg_lower and "cannot represent" in msg_lower:
        return "GRAPHQL_VALIDATION_FAILED"
    if "expected value of type" in msg_lower:
        return "GRAPHQL_VALIDATION_FAILED"
    if "type" in msg_lower and "is required" in msg_lower:
        return "GRAPHQL_VALIDATION_FAILED"
    if "was not provided" in msg_lower:
        return "GRAPHQL_VALIDATION_FAILED"
    if "is not defined" in msg_lower:
        return "GRAPHQL_VALIDATION_FAILED"
    if "unknown type" in msg_lower:
        return "GRAPHQL_VALIDATION_FAILED"
    if "cannot query field" in msg_lower:
        return "GRAPHQL_VALIDATION_FAILED"
    if "cannot represent" in msg_lower:
        return "GRAPHQL_VALIDATION_FAILED"
    if "validation" in msg_lower or ("field" in msg_lower and "argument" in msg_lower):
        return "GRAPHQL_VALIDATION_FAILED"
    # Additional validation patterns
    if "is never used" in msg_lower:  # Unused variable
        return "GRAPHQL_VALIDATION_FAILED"
    if "used in position expecting" in msg_lower:  # Type mismatch
        return "GRAPHQL_VALIDATION_FAILED"
    if "must have a selection of subfields" in msg_lower:
        return "GRAPHQL_VALIDATION_FAILED"
    if "does not exist in" in msg_lower and "enum" in msg_lower:  # Invalid enum value
        return "GRAPHQL_VALIDATION_FAILED"
    if "invalid input" in msg_lower or "invalid value" in msg_lower:
        return "INVALID_INPUT"

    # Not found
    if "not found" in msg_lower:
        return "NOT_FOUND"
    if "does not exist" in msg_lower or "doesn't exist" in msg_lower:
        return "NOT_FOUND"
    if "no such" in msg_lower:
        return "NOT_FOUND"

    # Auth/permission
    if "unauthorized" in msg_lower or "unauthenticated" in msg_lower:
        return "UNAUTHENTICATED"
    if "forbidden" in msg_lower or "permission" in msg_lower or "access denied" in msg_lower:
        return "FORBIDDEN"

    # Conflict
    if "already exists" in msg_lower or "duplicate" in msg_lower:
        return "ALREADY_EXISTS"
    if "conflict" in msg_lower:
        return "CONFLICT"

    # Rate limiting
    if "rate" in msg_lower and "limit" in msg_lower:
        return "RATE_LIMITED"
    if "too many" in msg_lower:
        return "TOO_MANY_REQUESTS"

    return None


def _classify_unknown_linear_error(error_code: str, message: str = "") -> ErrorType:
    """Classify unknown Linear error by pattern."""
    code_lower = error_code.lower()
    msg_lower = message.lower() if message else ""

    if "not_found" in code_lower or "notfound" in code_lower:
        return ErrorType.NOT_FOUND
    if code_lower.startswith("invalid_") or code_lower.startswith("bad_"):
        return ErrorType.BAD_REQUEST
    if code_lower.startswith("missing_"):
        return ErrorType.BAD_REQUEST
    if "_denied" in code_lower or "forbidden" in code_lower:
        return ErrorType.PERMISSION
    if "_expired" in code_lower or "_revoked" in code_lower:
        return ErrorType.AUTHENTICATION
    if code_lower.startswith("already_") or code_lower.startswith("duplicate_") or "_exists" in code_lower:
        return ErrorType.CONFLICT
    if "rate_" in code_lower or "_limit_" in code_lower:
        return ErrorType.RATE_LIMIT
    if code_lower.startswith("internal_") or code_lower.startswith("server_"):
        return ErrorType.SERVER_ERROR
    if "_archived" in code_lower or "_deleted" in code_lower:
        return ErrorType.GONE

    # Check message as fallback
    if msg_lower:
        if "not found" in msg_lower:
            return ErrorType.NOT_FOUND
        if "permission" in msg_lower or "access" in msg_lower:
            return ErrorType.PERMISSION
        if "authentication" in msg_lower or "unauthorized" in msg_lower:
            return ErrorType.AUTHENTICATION
        if "invalid" in msg_lower or "required" in msg_lower:
            return ErrorType.BAD_REQUEST
        if "unsupported" in msg_lower or "unknown method" in msg_lower:
            return ErrorType.BAD_REQUEST
        if "no" in msg_lower and "passed" in msg_lower:
            return ErrorType.BAD_REQUEST
        if "no" in msg_lower and "specified" in msg_lower:
            return ErrorType.BAD_REQUEST
        if "not_supplied" in msg_lower or "not supplied" in msg_lower:
            return ErrorType.BAD_REQUEST
        if "not provided" in msg_lower:
            return ErrorType.BAD_REQUEST
        if "already exists" in msg_lower or "duplicate" in msg_lower:
            return ErrorType.CONFLICT

    return ErrorType.UNKNOWN


# =============================================================================
# MAIN UNIFIED CLASSIFIER
# =============================================================================

# App name aliases
APP_ALIASES = {
    "calendar": "gcal",
    "google_calendar": "gcal",
    "google-calendar": "gcal",
    "gcal": "gcal",
    "box": "box",
    "slack": "slack",
    "linear": "linear",
}

CLASSIFIERS = {
    "gcal": classify_gcal_response,
    "box": classify_box_response,
    "slack": classify_slack_response,
    "linear": classify_linear_response,
}


def classify_response(stdout: str, app_name: str) -> Dict[str, Any]:
    """
    Unified error classifier for API responses.

    Args:
        stdout: Raw response string (JSON, HTML, or text)
        app_name: Name of the app ("calendar", "gcal", "box", "slack", "linear")

    Returns:
        {
            "has_error": bool,
            "error_type": str (one of ErrorType values),
            "error_code": str or None,
            "details": str or None
        }
    """
    # Normalize app name
    app_key = APP_ALIASES.get(app_name.lower().replace("-", "_").replace(" ", "_"))

    if not app_key:
        raise ValueError(f"Unknown app: {app_name}. Supported: {list(APP_ALIASES.keys())}")

    classifier = CLASSIFIERS[app_key]
    return classifier(stdout)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def has_error(stdout: str, app_name: str) -> bool:
    """Quick check if response contains an error."""
    return classify_response(stdout, app_name)["has_error"]


def get_error_type(stdout: str, app_name: str) -> str:
    """Get just the error type (or 'no_error')."""
    return classify_response(stdout, app_name)["error_type"]


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("UNIFIED ERROR CLASSIFIER")
    print("=" * 70)
    print(f"Supported apps: {list(APP_ALIASES.keys())}")
    print(f"Error types: {[e.value for e in ErrorType]}")
    print()

    # Test cases
    tests = [
        ("gcal", '{"error": {"code": 404, "message": "Not Found", "errors": [{"reason": "notFound"}]}}'),
        ("box", '{"type": "error", "status": 401, "code": "unauthorized", "message": "Invalid token"}'),
        ("slack", '{"ok": false, "error": "channel_not_found"}'),
        ("linear", '{"errors": [{"message": "Issue with id \'123\' not found"}]}'),
        ("linear", '{"errors": [{"message": "Syntax Error: Unexpected character"}]}'),
        ("linear", '{"data": {"issue": {"id": "123"}}}'),  # No error
    ]

    print("Test cases:")
    for app, response in tests:
        result = classify_response(response, app)
        print(f"  [{app}] has_error={result['has_error']}, type={result['error_type']}, code={result['error_code']}")

    print()
    print("Function: classify_response(stdout, app_name)")
