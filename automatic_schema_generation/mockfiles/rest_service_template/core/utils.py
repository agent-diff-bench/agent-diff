"""Shared utility helpers for __APP_NAME__ REST API."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

# BEGIN SHARED HELPERS
def generate_resource_id() -> str:
    """Deterministic-enough default ID scaffold for MVP templates."""
    return uuid4().hex


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_int_param(
    value: str | None,
    *,
    default: int,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    if value is None or value == "":
        candidate = default
    else:
        candidate = int(value)

    if minimum is not None and candidate < minimum:
        candidate = minimum
    if maximum is not None and candidate > maximum:
        candidate = maximum
    return candidate
# END SHARED HELPERS

