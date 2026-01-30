"""
Google Calendar API Batch Request Parser

Parses multipart/mixed batch requests into individual request parts.
Implements Google's batch request format as documented at:
https://developers.google.com/workspace/calendar/api/guides/batch
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qs, urlparse


# Line endings
CRLF = b"\r\n"
LF = b"\n"
DOUBLE_CRLF = b"\r\n\r\n"
DOUBLE_LF = b"\n\n"


class BatchParseError(Exception):
    """Error parsing a batch request."""
    pass


@dataclass
class BatchPart:
    """Represents a single part of a batch request."""
    content_id: Optional[str]       # e.g., "item1:12930812@example.com" (without <>)
    method: str                     # GET, POST, PUT, PATCH, DELETE
    path: str                       # /calendar/v3/calendars/primary (without query)
    query_params: dict[str, list[str]]  # Parsed query parameters
    headers: dict[str, str]         # Inner request headers
    body: Optional[bytes]           # Request body (for POST/PUT/PATCH)


@dataclass
class ParsedBatchRequest:
    """Represents the complete parsed batch request."""
    boundary: str
    parts: list[BatchPart]
    outer_headers: dict[str, str]   # For inheritance
    outer_query_params: dict[str, list[str]]  # For inheritance


def extract_boundary(content_type: str) -> str:
    """
    Extract boundary string from Content-Type header.
    
    Handles both quoted and unquoted boundary values:
    - multipart/mixed; boundary=batch_foobarbaz
    - multipart/mixed; boundary="batch_foobarbaz"
    
    Raises: BatchParseError if boundary not found
    """
    if "multipart/mixed" not in content_type.lower():
        raise BatchParseError("Content-Type must be multipart/mixed")
    
    # Look for boundary parameter
    match = re.search(r'boundary\s*=\s*"?([^";,\s]+)"?', content_type, re.IGNORECASE)
    if not match:
        raise BatchParseError("Missing boundary in Content-Type header")
    
    return match.group(1)


def parse_content_id(raw: str) -> Optional[str]:
    """
    Extract Content-ID value, stripping angle brackets if present.
    
    Input: "<item1:12930812@barnyard.example.com>"
    Output: "item1:12930812@barnyard.example.com"
    
    Input: "item1"
    Output: "item1"
    """
    if not raw:
        return None
    
    raw = raw.strip()
    if raw.startswith("<") and raw.endswith(">"):
        return raw[1:-1]
    return raw


def normalize_line_endings(data: bytes) -> bytes:
    """
    Normalize line endings to CRLF.
    Accept both LF and CRLF on input.
    """
    # First normalize CRLF to LF, then convert all LF to CRLF
    data = data.replace(CRLF, LF)
    data = data.replace(LF, CRLF)
    return data


def parse_batch_request(
    body: bytes,
    boundary: str,
    outer_headers: dict[str, str],
    outer_query_params: dict[str, list[str]]
) -> ParsedBatchRequest:
    """
    Parse multipart/mixed body into individual BatchParts.
    
    Steps:
    1. Split body by boundary delimiter
    2. For each part:
       a. Extract part headers (Content-Type, Content-ID)
       b. Parse inner HTTP request (method, path, headers, body)
       c. Merge outer query params with inner query params
    3. Return ParsedBatchRequest with all parts
    
    Raises: BatchParseError for malformed requests
    """
    # Normalize line endings
    body = normalize_line_endings(body)
    
    # Create boundary markers
    boundary_bytes = f"--{boundary}".encode("utf-8")
    end_boundary_bytes = f"--{boundary}--".encode("utf-8")
    
    # Split by boundary
    parts_raw = body.split(boundary_bytes)
    
    # First part is preamble (empty or whitespace), skip it
    # Last element after split by end boundary should be epilogue
    
    parts: list[BatchPart] = []
    
    for i, part_raw in enumerate(parts_raw):
        # Skip empty preamble
        if i == 0:
            continue
        
        # Check if this is the end boundary
        part_raw = part_raw.strip()
        if part_raw == b"--" or part_raw.startswith(b"--"):
            # This is the closing boundary marker
            break
        
        if not part_raw:
            continue
        
        # Parse the part
        try:
            batch_part = _parse_single_part(part_raw, outer_headers, outer_query_params, i)
            parts.append(batch_part)
        except Exception as e:
            raise BatchParseError(f"Invalid HTTP request in part {i}: {e}")
    
    return ParsedBatchRequest(
        boundary=boundary,
        parts=parts,
        outer_headers=outer_headers,
        outer_query_params=outer_query_params,
    )


def _parse_single_part(
    part_raw: bytes,
    outer_headers: dict[str, str],
    outer_query_params: dict[str, list[str]],
    part_index: int,
) -> BatchPart:
    """Parse a single part of the batch request."""
    
    # Split part headers from inner request
    # Part structure:
    # Content-Type: application/http
    # Content-ID: <item1>
    #
    # GET /calendar/v3/calendars/primary HTTP/1.1
    # ...
    
    if DOUBLE_CRLF in part_raw:
        part_headers_raw, inner_request_raw = part_raw.split(DOUBLE_CRLF, 1)
    else:
        raise BatchParseError(f"Missing blank line between part headers and request in part {part_index}")
    
    # Parse part headers
    part_headers = _parse_headers(part_headers_raw)
    
    # Validate Content-Type is application/http
    part_content_type = part_headers.get("content-type", "").lower()
    if "application/http" not in part_content_type:
        raise BatchParseError(
            f"Part {part_index} Content-Type must be application/http, got: {part_content_type}"
        )
    
    # Extract Content-ID
    content_id = parse_content_id(part_headers.get("content-id", ""))
    
    # Parse inner HTTP request
    method, path, query_params, inner_headers, body = parse_inner_http_request(inner_request_raw)
    
    # Merge query params (inner overrides outer)
    merged_query_params = merge_query_params(outer_query_params, query_params)
    
    # Merge headers (inner overrides outer, skip Content-* from outer)
    merged_headers = merge_headers(outer_headers, inner_headers)
    
    return BatchPart(
        content_id=content_id,
        method=method,
        path=path,
        query_params=merged_query_params,
        headers=merged_headers,
        body=body if body else None,
    )


def _parse_headers(headers_raw: bytes) -> dict[str, str]:
    """Parse HTTP headers from raw bytes."""
    headers: dict[str, str] = {}
    
    lines = headers_raw.split(CRLF)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip if no colon
        if b":" not in line:
            continue
        
        key, _, value = line.partition(b":")
        key = key.decode("utf-8", errors="replace").strip().lower()
        value = value.decode("utf-8", errors="replace").strip()
        headers[key] = value
    
    return headers


def parse_inner_http_request(
    raw: bytes
) -> tuple[str, str, dict[str, list[str]], dict[str, str], bytes]:
    """
    Parse a raw HTTP request string into components.
    
    Input: b"GET /calendar/v3/calendars/primary?fields=id\\r\\nIf-None-Match: \\"etag\\"\\r\\n\\r\\n"
    Output: (
        "GET",                                    # method
        "/calendar/v3/calendars/primary",         # path (without query)
        {"fields": ["id"]},                       # query params
        {"if-none-match": "\\"etag\\""},          # headers (lowercase keys)
        b""                                       # body
    )
    
    Note: Must handle both "GET /path" and "GET /path HTTP/1.1" formats
    """
    # Split headers and body
    if DOUBLE_CRLF in raw:
        headers_section, body = raw.split(DOUBLE_CRLF, 1)
    else:
        headers_section = raw
        body = b""
    
    lines = headers_section.split(CRLF)
    
    if not lines:
        raise BatchParseError("Empty inner request")
    
    # Parse request line
    request_line = lines[0].decode("utf-8", errors="replace").strip()
    if not request_line:
        raise BatchParseError("Empty request line")
    
    # Parse: METHOD PATH [HTTP/1.1]
    parts = request_line.split()
    if len(parts) < 2:
        raise BatchParseError(f"Invalid request line: {request_line}")
    
    method = parts[0].upper()
    full_path = parts[1]
    # Ignore HTTP version if present (parts[2] would be "HTTP/1.1")
    
    # Parse path and query params
    parsed_url = urlparse(full_path)
    path = parsed_url.path
    query_params = parse_qs(parsed_url.query, keep_blank_values=True)
    
    # Parse headers (remaining lines)
    headers: dict[str, str] = {}
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        if b":" not in line:
            continue
        
        key, _, value = line.partition(b":")
        key = key.decode("utf-8", errors="replace").strip().lower()
        value = value.decode("utf-8", errors="replace").strip()
        headers[key] = value
    
    return method, path, query_params, headers, body


def merge_query_params(
    outer: dict[str, list[str]],
    inner: dict[str, list[str]]
) -> dict[str, list[str]]:
    """
    Merge outer and inner query parameters.
    Inner params override outer for same key.
    """
    merged = dict(outer)  # Copy outer
    merged.update(inner)  # Inner overrides
    return merged


def merge_headers(
    outer: dict[str, str],
    inner: dict[str, str]
) -> dict[str, str]:
    """
    Merge outer and inner headers.
    - Skip Content-* headers from outer
    - Inner overrides outer for same key (case-insensitive)
    """
    merged: dict[str, str] = {}
    
    # Add outer headers (skip Content-*)
    for key, value in outer.items():
        key_lower = key.lower()
        if not key_lower.startswith("content-"):
            merged[key_lower] = value
    
    # Add/override with inner headers
    for key, value in inner.items():
        key_lower = key.lower()
        merged[key_lower] = value
    
    return merged
