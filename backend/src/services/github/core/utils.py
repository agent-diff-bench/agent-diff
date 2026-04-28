"""Shared utilities for the GitHub API replica.

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
# AGENT INSTRUCTION: Fill in ID_FORMATS from the contract freeze artifacts.
# Each entry is derived from OpenAPI example IDs for that resource:
#   - Analyze the example string to determine alphabet (alphanumeric, numeric,
#     hex, etc.) and length.
#   - Example: "6XGgm6PHrGgMpCFX" -> alphabet=ALPHANUMERIC, length=16
#   - Example: "2147509004"        -> alphabet=NUMERIC, length=10
# ---------------------------------------------------------------------------

ALPHANUMERIC = string.ascii_letters + string.digits  # a-zA-Z0-9
NUMERIC = string.digits                               # 0-9
HEX_LOWER = string.digits + "abcdef"                  # 0-9a-f

ID_FORMATS: dict[str, dict] = {
    "gist": {"alphabet": HEX_LOWER, "length": 20},
    "issue": {"alphabet": NUMERIC, "length": 10},
    "issue_comment": {"alphabet": NUMERIC, "length": 10},
    "issue_event": {"alphabet": NUMERIC, "length": 10},
    "issue_reaction": {"alphabet": NUMERIC, "length": 10},
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
