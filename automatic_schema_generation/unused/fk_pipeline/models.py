"""Data model for the resource ↔ endpoint bucketing output.

Three dataclasses:

  * ``Edge`` — one resource-endpoint relationship, tagged with a role.
  * ``EndpointRecord`` — one operation, with its metadata and the set
    of resource edges attached to it.
  * ``ResourceEndpointMap`` — the full bidirectional artifact.

The two views (``resources`` and ``endpoints``) are both derived from
the same canonical edge list. Downstream steps can read either one
without worrying about consistency: a mutation to the canonical list
invalidates both views until they're rebuilt.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EdgeRole(str, Enum):
    """The controlled vocabulary of edge role tags.

    Ownership roles (at most one per endpoint):
      * ``OWNER_COLLECTION`` — endpoint acts on the resource's collection
        root. Examples: ``GET /projects``, ``POST /projects``.
      * ``OWNER_ITEM`` — endpoint acts on a single item of the resource.
        Examples: ``GET /projects/{project_id}``, ``DELETE /tasks/{id}``.
      * ``OWNER_ACTION`` — POST (or occasionally PUT) that mutates a
        single item via a verb-style sub-path. Example:
        ``POST /projects/{project_id}/archive``.
      * ``SUB_COLLECTION`` — resource is the terminal segment of a
        nested path scoped by a parent. Example: the ``tasks`` resource
        under ``GET /projects/{project_id}/tasks``.

    Reference roles (any number per endpoint, including zero):
      * ``PARENT`` — resource is referenced by a path parameter but
        does not own the endpoint. Example: ``projects`` for
        ``POST /projects/{project_id}/tasks``.
      * ``QUERY_REFERENCED`` — resource is mentioned only via a query
        parameter. Example: ``projects`` for ``GET /tasks?project_id=...``.
      * ``BODY_REFERENCED`` — resource is mentioned only in response
        or request body schemas (via ``$ref`` to a matching component
        schema). Example: ``users`` for ``GET /issues/{id}`` when the
        response contains ``user: $ref: #/components/schemas/User``.

    The ordering of roles in this enum is load-bearing: it encodes the
    strength ordering used to suppress weaker roles when a stronger
    one is already present for the same (resource, endpoint) pair.
    Strongest first.
    """

    OWNER_ITEM = "OWNER_ITEM"
    OWNER_COLLECTION = "OWNER_COLLECTION"
    OWNER_ACTION = "OWNER_ACTION"
    SUB_COLLECTION = "SUB_COLLECTION"
    PARENT = "PARENT"
    QUERY_REFERENCED = "QUERY_REFERENCED"
    BODY_REFERENCED = "BODY_REFERENCED"


# Strength ordering for dedup — lower index = stronger.
_ROLE_STRENGTH: dict[EdgeRole, int] = {
    role: idx for idx, role in enumerate(list(EdgeRole))
}


def role_is_stronger(a: EdgeRole, b: EdgeRole) -> bool:
    """True if role ``a`` is strictly stronger than ``b``."""
    return _ROLE_STRENGTH[a] < _ROLE_STRENGTH[b]


@dataclass
class Edge:
    """One (resource, endpoint) relationship with role + provenance."""

    resource: str
    endpoint_key: str  # "METHOD /path"
    role: EdgeRole
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "resource": self.resource,
            "endpoint": self.endpoint_key,
            "role": self.role.value,
            "evidence": self.evidence,
        }


@dataclass
class EndpointRecord:
    """Full operation metadata plus its attached edges.

    ``raw_operation`` is the full OpenAPI operation dict verbatim so
    later steps can walk schemas, parameters, responses without re-
    reading the spec. This is why unbucketed endpoints keep their full
    metadata too — they may still be useful for manual triage.
    """

    method: str
    path: str
    operation_id: str
    raw_operation: dict[str, Any]
    # Attached by the map — each edge references this endpoint's key.
    resource_edges: list[Edge] = field(default_factory=list)

    @property
    def key(self) -> str:
        return f"{self.method} {self.path}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "path": self.path,
            "operation_id": self.operation_id,
            "resource_edges": [
                {"resource": e.resource, "role": e.role.value, "evidence": e.evidence}
                for e in self.resource_edges
            ],
            "raw_operation": self.raw_operation,
        }


@dataclass
class ResourceEndpointMap:
    """Bidirectional resource ↔ endpoint map.

    Canonical data is the flat ``edges`` list. ``endpoints`` holds the
    full operation metadata (one entry per operation). ``resources``
    is derived from ``edges`` grouped by resource name.

    ``unbucketed_endpoints`` holds operations that matched zero
    resources — useful for debugging missing coverage and for deciding
    whether to expand scope.
    """

    edges: list[Edge]
    endpoints: dict[str, EndpointRecord]
    unbucketed_endpoints: list[EndpointRecord]
    resource_aliases: dict[str, list[str]]  # canonical → full alias list

    def resources_view(self) -> dict[str, list[Edge]]:
        """Group edges by resource name."""
        out: dict[str, list[Edge]] = {r: [] for r in self.resource_aliases}
        for edge in self.edges:
            out.setdefault(edge.resource, []).append(edge)
        return out
