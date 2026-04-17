"""Shared utilities for the Asana API replica.

ID generation uses a universal pattern: a config dict maps resource names to
their format (alphabet + length), and a single generate_id() function handles
all resources. Only ID_FORMATS changes per app — derived from OpenAPI spec
examples during contract freeze.
"""

import random
import string
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# ID generation
# ---------------------------------------------------------------------------

ALPHANUMERIC = string.ascii_letters + string.digits  # a-zA-Z0-9
NUMERIC = string.digits                               # 0-9
HEX_LOWER = string.digits + "abcdef"                  # 0-9a-f

ID_FORMATS: dict[str, dict] = {
    "project": {"alphabet": ALPHANUMERIC, "length": 16},
    "section": {"alphabet": ALPHANUMERIC, "length": 16},
    "tag": {"alphabet": ALPHANUMERIC, "length": 16},
    "task": {"alphabet": ALPHANUMERIC, "length": 16},
    "team": {"alphabet": ALPHANUMERIC, "length": 16},
    "time_tracking_entry": {"alphabet": ALPHANUMERIC, "length": 16},
    "job": {"alphabet": ALPHANUMERIC, "length": 16},
    "user_task_list": {"alphabet": ALPHANUMERIC, "length": 16},
    "user": {"alphabet": ALPHANUMERIC, "length": 16},
    "workspace": {"alphabet": ALPHANUMERIC, "length": 16},
}


def generate_id(resource: str) -> str:
    """Generate an ID matching the source app's format for the given resource."""
    fmt = ID_FORMATS[resource]
    return "".join(random.choices(fmt["alphabet"], k=fmt["length"]))


# ---------------------------------------------------------------------------
# Timestamps
# ---------------------------------------------------------------------------

def now_iso() -> str:
    """Current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
