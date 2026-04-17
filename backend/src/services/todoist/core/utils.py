"""Shared utilities for the Todoist API replica.

ID generation uses a universal pattern: a config dict maps resource names to
their format (alphabet + length), and a single generate_id() function handles
all resources. This pattern is intended to be reusable across generated apps —
only ID_FORMATS changes per app.
"""

import random
import string
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# ID generation — format derived from OpenAPI spec examples
# ---------------------------------------------------------------------------

ALPHANUMERIC = string.ascii_letters + string.digits  # a-zA-Z0-9
NUMERIC = string.digits                               # 0-9

ID_FORMATS: dict[str, dict] = {
    "project": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgm6PHrGgMpCFX
    "section": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgm6PHrGgMpCFX
    "task": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFVcrG5RRjVr
    "comment": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFQrx44wfGHr
    "label": {"alphabet": NUMERIC, "length": 10},  # example: (override)
    "user": {"alphabet": NUMERIC, "length": 10},  # example: (override)
},  # example: 6XGgm6PHrGgMpCFX
    "section": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgm6PHrGgMpCFX
    "task": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFVcrG5RRjVr
    "comment": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFQrx44wfGHr
    "label": {"alphabet": NUMERIC, "length": 10},  # example: (override)
    "user": {"alphabet": NUMERIC, "length": 10},  # example: (override)
},  # example: 6XGgm6PHrGgMpCFX
    "section": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgm6PHrGgMpCFX
    "task": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFVcrG5RRjVr
    "comment": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFQrx44wfGHr
    "label": {"alphabet": NUMERIC, "length": 10},  # example: (override)
    "user": {"alphabet": NUMERIC, "length": 10},  # example: (override)
},  # example: 6XGgm6PHrGgMpCFX
    "section": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgm6PHrGgMpCFX
    "task": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFVcrG5RRjVr
    "comment": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFQrx44wfGHr
    "label": {"alphabet": NUMERIC, "length": 10},  # example: (override)
    "user": {"alphabet": NUMERIC, "length": 10},  # example: (override)
},  # example: 6XGgm6PHrGgMpCFX
    "section": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgm6PHrGgMpCFX
    "task": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFVcrG5RRjVr
    "comment": {"alphabet": ALPHANUMERIC, "length": 16},  # example: 6XGgmFQrx44wfGHr
    "label": {"alphabet": NUMERIC, "length": 10},  # example: (override)
    "user": {"alphabet": NUMERIC, "length": 10},  # example: (override)
},
    "section": {"alphabet": ALPHANUMERIC, "length": 16},
    "task": {"alphabet": ALPHANUMERIC, "length": 16},
    "comment": {"alphabet": ALPHANUMERIC, "length": 16},
    "label": {"alphabet": NUMERIC, "length": 10},  # example: (override)
    "user": {"alphabet": NUMERIC, "length": 10},  # example: (override)
},
    "section": {"alphabet": ALPHANUMERIC, "length": 16},
    "task": {"alphabet": ALPHANUMERIC, "length": 16},
    "comment": {"alphabet": ALPHANUMERIC, "length": 16},
    "label": {"alphabet": NUMERIC, "length": 10},  # example: (override)
    "user": {"alphabet": NUMERIC, "length": 10},  # example: (override)
},
    "task":    {"alphabet": ALPHANUMERIC, "length": 16},
    "section": {"alphabet": ALPHANUMERIC, "length": 16},
    "comment": {"alphabet": ALPHANUMERIC, "length": 16},
    "label":   {"alphabet": NUMERIC,      "length": 10},
    "user":    {"alphabet": NUMERIC,      "length": 10},
    "folder":  {"alphabet": ALPHANUMERIC, "length": 16},
}


def generate_id(resource: str) -> str:
    """Generate an ID matching the source app's format for the given resource."""
    fmt = ID_FORMATS[resource]
    return "".join(random.choices(fmt["alphabet"], k=fmt["length"]))


# ---------------------------------------------------------------------------
# Timestamps
# ---------------------------------------------------------------------------

def now_iso() -> str:
    """Current UTC time as an ISO 8601 string matching Todoist's format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
