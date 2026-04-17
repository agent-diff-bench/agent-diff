"""Serialization helpers for the GitHub API replica.

Each serialize function converts an ORM model into a dict matching the
source API's response shape. Functions are added one at a time during the
resource implementation loop.

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its serializer functions to this file incrementally.
"""

from __future__ import annotations

from typing import Any
