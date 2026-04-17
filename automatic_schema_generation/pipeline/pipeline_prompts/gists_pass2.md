# Entity Implementation (Pass 2 — Relationships): gists

You are adding foreign key relationships to the **gists** resource
(`GitHubGist` in `github_gists`). The base model, operations,
serializers, and routes already exist from Pass 1.

The full OpenAPI spec is available at: `/Users/azh/agent-diff/automatic_schema_generation/apps/github/inputs/openapi.scoped.json`
If any information in this prompt is unclear or seems incorrect, read the
spec directly to resolve ambiguities.

Read the existing files in the target directory first. You will modify them
to add FK columns, relationship() declarations, indexes, association tables,
and update operations/serializers to handle the new relationships.

Files to edit (all under `/Users/azh/backend/src/services/github`):
- `database/schema.py`
- `database/operations.py`
- `core/serializers.py`
- `api/routes.py`

---

## Relationship Reference Patterns

The examples below are **fictional mocks** showing how each FK relationship
type maps to SQLAlchemy 2.0 models. Use them as structural guidance — do not
copy the mock names or table names.

### Many To Many
```python
"""Pattern: Many-to-Many (M:N) — REFERENCE MOCK, not real code.

These models are fictional examples showing how to implement an M:N
relationship via an association table. Do not reuse these names —
build your own models based on the actual resource schemas provided
in the prompt.

Use an association Table when both sides carry a list and no extra
metadata is needed on the link itself. If the link needs extra
columns (e.g. joined_at, role), use an explicit mapped class with
a composite primary key instead of a bare Table.
"""

from sqlalchemy import Boolean, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# Association table — bare Table, not a mapped class.
# Composite primary key prevents duplicate links.
example_item_tag_association = Table(
    "mock_item_tag_association",
    Base.metadata,
    Column("item_id", ForeignKey("mock_items.id"), primary_key=True),
    Column("tag_id", ForeignKey("mock_tags.id"), primary_key=True),
)


class ExampleItem(Base):
    __tablename__ = "mock_items"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # secondary= points at the association table.
    # Both sides use back_populates to keep the ORM in sync.
    tags: Mapped[list["ExampleTag"]] = relationship(
        secondary=example_item_tag_association, back_populates="items"
    )


class ExampleTag(Base):
    __tablename__ = "mock_tags"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    items: Mapped[list["ExampleItem"]] = relationship(
        secondary=example_item_tag_association, back_populates="tags"
    )


# --- Operations (key patterns) ---
#
# Adding / removing links operates on the relationship list directly.
# SQLAlchemy handles the association table inserts and deletes.
#
# def add_tag_to_item(session, item_id, tag_id):
#     item = session.get(ExampleItem, item_id)
#     tag = session.get(ExampleTag, tag_id)
#     if tag not in item.tags:
#         item.tags.append(tag)
#     session.flush()
#
# def remove_tag_from_item(session, item_id, tag_id):
#     item = session.get(ExampleItem, item_id)
#     tag = session.get(ExampleTag, tag_id)
#     if tag in item.tags:
#         item.tags.remove(tag)
#     session.flush()
#
# Querying items by tag:
#
# def list_items_by_tag(session, tag_id):
#     return session.execute(
#         select(ExampleItem)
#         .join(ExampleItem.tags)
#         .where(ExampleTag.id == tag_id,
#                ExampleItem.is_deleted.is_(False))
#     ).scalars().all()
```

### Multiple Fks Same Target
```python
"""Pattern: Multiple FKs to the Same Target — REFERENCE MOCK, not real code.

These models are fictional examples showing how to disambiguate
when two or more FK columns reference the same table. Do not reuse
these names — build your own models based on the actual resource
schemas provided in the prompt.

When multiple FK columns point at the same target, SQLAlchemy
cannot infer which relationship uses which column. Disambiguate
with the foreign_keys= argument. Each relationship on the target
side also needs its own back_populates name.
"""

from typing import Optional

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ExamplePerson(Base):
    __tablename__ = "mock_persons"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # One back_populates list per FK role on the referencing side.
    created_tickets: Mapped[list["ExampleTicket"]] = relationship(
        back_populates="creator", foreign_keys="ExampleTicket.creator_id"
    )
    assigned_tickets: Mapped[list["ExampleTicket"]] = relationship(
        back_populates="assignee", foreign_keys="ExampleTicket.assignee_id"
    )


class ExampleTicket(Base):
    __tablename__ = "mock_tickets"
    __table_args__ = (
        Index("ix_mock_tickets_creator", "creator_id"),
        Index("ix_mock_tickets_assignee", "assignee_id"),
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)

    # Two FK columns to the same table.
    creator_id: Mapped[str] = mapped_column(
        ForeignKey("mock_persons.id"), nullable=False
    )
    assignee_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("mock_persons.id"), nullable=True
    )

    # foreign_keys= resolves the ambiguity. Without it, SQLAlchemy
    # raises AmbiguousForeignKeysError at mapper configuration time.
    creator: Mapped["ExamplePerson"] = relationship(
        back_populates="created_tickets", foreign_keys=[creator_id]
    )
    assignee: Mapped[Optional["ExamplePerson"]] = relationship(
        back_populates="assigned_tickets", foreign_keys=[assignee_id]
    )


# --- Serializer hint ---
#
# def serialize_ticket(ticket: ExampleTicket) -> dict:
#     return {
#         "id": ticket.id,
#         "title": ticket.title,
#         "creator_id": ticket.creator_id,
#         "assignee_id": ticket.assignee_id,
#     }
```

### One To Many
```python
"""Pattern: One-to-Many (1:N) — REFERENCE MOCK, not real code.

These models are fictional examples showing how to implement a 1:N
FK relationship. Do not reuse these names — build your own models
based on the actual resource schemas provided in the prompt.

Use this pattern when one entity "belongs to" another and the child
carries the FK column.
"""

from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ExampleParent(Base):
    __tablename__ = "mock_parents"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Parent side: list relationship, no FK column on this table.
    # cascade="all,delete-orphan" ensures children are removed when
    # the parent is deleted.
    children: Mapped[list["ExampleChild"]] = relationship(
        back_populates="parent", cascade="all,delete-orphan"
    )


class ExampleChild(Base):
    __tablename__ = "mock_children"
    __table_args__ = (
        Index("ix_mock_children_parent", "parent_id"),
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Child side: FK column + scalar relationship.
    # nullable=False means every child must belong to a parent.
    # Use nullable=True when the parent is optional.
    parent_id: Mapped[str] = mapped_column(
        ForeignKey("mock_parents.id"), nullable=False
    )
    parent: Mapped["ExampleParent"] = relationship(back_populates="children")


# --- Operations (key patterns) ---
#
# def create_child(session, *, parent_id, title):
#     child = ExampleChild(
#         id=generate_id("child"),
#         parent_id=parent_id,             # FK set at creation
#         title=title,
#     )
#     session.add(child)
#     session.flush()
#     return child
#
# def list_children_by_parent(session, parent_id):
#     return session.execute(
#         select(ExampleChild)
#         .where(ExampleChild.parent_id == parent_id,
#                ExampleChild.is_deleted.is_(False))
#     ).scalars().all()
```

### Self Referential
```python
"""Pattern: Self-Referential FK — REFERENCE MOCK, not real code.

These models are fictional examples showing how to implement a
self-referential tree hierarchy. Do not reuse these names — build
your own models based on the actual resource schemas provided in
the prompt.

Use this pattern for any entity that nests within itself: folders,
comments, org units, task subtasks, etc. The FK is nullable because
root nodes have parent_id = NULL.
"""

from typing import Optional

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ExampleNode(Base):
    __tablename__ = "mock_nodes"
    __table_args__ = (
        Index("ix_mock_nodes_parent", "parent_id"),
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)

    # FK to own table. Nullable because root nodes have no parent.
    parent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("mock_nodes.id"), nullable=True
    )

    # remote_side=[id] tells SQLAlchemy which column is the "one"
    # side. Without it, SQLAlchemy can't distinguish parent from
    # children since both reference the same table.
    parent: Mapped[Optional["ExampleNode"]] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list["ExampleNode"]] = relationship(
        back_populates="parent"
    )


# --- Operations (key patterns) ---
#
# def get_root_nodes(session):
#     return session.execute(
#         select(ExampleNode).where(ExampleNode.parent_id.is_(None))
#     ).scalars().all()
#
# def get_children(session, node_id):
#     return session.execute(
#         select(ExampleNode)
#         .where(ExampleNode.parent_id == node_id)
#     ).scalars().all()
#
# def move_node(session, node_id, new_parent_id):
#     node = session.get(ExampleNode, node_id)
#     node.parent_id = new_parent_id
#     session.flush()
```


---

## Related Resources

These resources have a demonstrated relationship with **gists**
through shared endpoints, FK-shaped property names, or schema cross-references.

Direction key:
- **outgoing** — gists's schemas contain fields that reference
  the related resource (e.g. a `_id` field or nested object pointing there).
  **Action**: add a FK column on `github_gists` pointing at the related
  resource's table, plus a `relationship()` on both sides.
- **incoming** — the related resource's endpoints reference gists
  (the subject of those endpoints is the other resource, not gists).
  **Action**: do NOT add a FK column on `github_gists`. The FK lives on the
  other resource's table. Add only a `relationship()` on the gists
  side (the "many" side) if the other resource's model already exists or will
  be created as a stub. If the incoming evidence is only URL segments (no
  property-level field), it may just be endpoint nesting — no FK needed.

For each related resource below, **infer the relationship type** from the
evidence and schema shapes:

- **One-to-Many**: this resource carries a FK column pointing at the related
  resource (e.g. `project_id` on a task), OR the related resource carries a
  FK pointing here. Look for singular ID fields and nested objects.
- **Many-to-Many**: both sides reference each other as arrays, or an endpoint
  returns a list of related entities that can independently belong to multiple
  parents. Build an association table.
- **Self-Referential**: a field like `parent_id` points at the same table.
  Use `remote_side=[id]`.

Then build the appropriate FK columns, indexes, and `relationship()`
declarations using the reference patterns above.

### commits
- Table: `github_commits`
- Primary key: `sha`
- Direction: incoming

Evidence:
  - GET /gists/{gist_id}/commits — url_segment: gists (incoming)
  - GET /gists/{gist_id}/commits — url_segment: gist_id (incoming)

Key fields (PK + fields referencing gists):
```json
{
  "commit": {
    "properties": {
      "sha": {
        "type": "string",
        "examples": [
          "6dcb09b5b57875f334f61aebed695e2e4193db5e"
        ]
      }
    },
    "required": [
      "sha"
    ]
  },
  "commit-search-result-item": {
    "properties": {
      "sha": {
        "type": "string"
      }
    },
    "required": [
      "sha"
    ]
  },
  "git-commit": {
    "properties": {
      "sha": {
        "description": "SHA for the commit",
        "type": "string",
        "examples": [
          "7638417db6d59f3c431d3e1f261cc637155684cd"
        ]
      }
    },
    "required": [
      "sha"
    ]
  }
}
```

### gists
- **SELF-REFERENTIAL** — this resource references itself
- Use the Self Referential pattern: nullable FK to own table,
  `remote_side=[id]` on the parent relationship
- Table: `github_gists`
- Primary key: `id`
- Direction: outgoing

Evidence:
  - POST /gists — url_segment: gists
  - POST /gists — body_response: application/json:gist-simple
  - GET /gists — url_segment: gists
  - GET /gists — body_response: application/json:base-gist
  - GET /gists/public — url_segment: gists
  - GET /gists/public — body_response: application/json:base-gist
  - GET /gists/starred — url_segment: gists
  - GET /gists/starred — body_response: application/json:base-gist
  - PATCH /gists/{gist_id} — url_segment: gists
  - PATCH /gists/{gist_id} — url_segment: gist_id
  - PATCH /gists/{gist_id} — body_response: application/json:gist-simple
  - GET /gists/{gist_id} — url_segment: gists
  - GET /gists/{gist_id} — url_segment: gist_id
  - GET /gists/{gist_id} — body_response: application/json:gist-simple
  - DELETE /gists/{gist_id} — url_segment: gists
  - DELETE /gists/{gist_id} — url_segment: gist_id
  - POST /gists/{gist_id}/comments — url_segment: gists
  - POST /gists/{gist_id}/comments — url_segment: gist_id
  - GET /gists/{gist_id}/comments — url_segment: gists
  - GET /gists/{gist_id}/comments — url_segment: gist_id
  - PATCH /gists/{gist_id}/comments/{comment_id} — url_segment: gists
  - PATCH /gists/{gist_id}/comments/{comment_id} — url_segment: gist_id
  - GET /gists/{gist_id}/comments/{comment_id} — url_segment: gists
  - GET /gists/{gist_id}/comments/{comment_id} — url_segment: gist_id
  - DELETE /gists/{gist_id}/comments/{comment_id} — url_segment: gists
  - DELETE /gists/{gist_id}/comments/{comment_id} — url_segment: gist_id
  - POST /gists/{gist_id}/forks — url_segment: gists
  - POST /gists/{gist_id}/forks — url_segment: gist_id
  - POST /gists/{gist_id}/forks — body_response: application/json:base-gist
  - GET /gists/{gist_id}/forks — url_segment: gists
  - GET /gists/{gist_id}/forks — url_segment: gist_id
  - GET /gists/{gist_id}/forks — body_response: application/json:gist-simple
  - PUT /gists/{gist_id}/star — url_segment: gists
  - PUT /gists/{gist_id}/star — url_segment: gist_id
  - GET /gists/{gist_id}/star — url_segment: gists
  - GET /gists/{gist_id}/star — url_segment: gist_id
  - DELETE /gists/{gist_id}/star — url_segment: gists
  - DELETE /gists/{gist_id}/star — url_segment: gist_id
  - GET /gists/{gist_id}/{sha} — url_segment: gists
  - GET /gists/{gist_id}/{sha} — url_segment: gist_id
  - GET /gists/{gist_id}/{sha} — body_response: application/json:gist-simple
  - GET /users/{username}/gists — url_segment: gists
  - GET /users/{username}/gists — body_response: application/json:base-gist

Key fields (PK + fields referencing gists):
```json
{
  "base-gist": {
    "properties": {
      "id": {
        "type": "string"
      }
    },
    "required": [
      "id"
    ]
  },
  "gist-simple": {
    "properties": {
      "id": {
        "type": "string"
      }
    }
  }
}
```

### users
- Table: `github_users`
- Primary key: `id`
- Direction: outgoing
- **Fields referencing users**: `fork_of.owner`, `fork_of.user`, `owner`, `user`

These fields all point at the `github_users` table. Infer the correct FK relationship type and apply using the reference patterns above.

Evidence:
  - POST /gists — property: fork_of.user
  - POST /gists — property: fork_of.user.login
  - POST /gists — property: fork_of.owner
  - POST /gists — property: user
  - POST /gists — property: owner
  - GET /gists — property: owner
  - GET /gists — property: owner.login
  - GET /gists/public — property: owner
  - GET /gists/public — property: owner.login
  - GET /gists/starred — property: owner
  - GET /gists/starred — property: owner.login
  - PATCH /gists/{gist_id} — property: fork_of.user
  - PATCH /gists/{gist_id} — property: fork_of.user.login
  - PATCH /gists/{gist_id} — property: fork_of.owner
  - PATCH /gists/{gist_id} — property: user
  - PATCH /gists/{gist_id} — property: owner
  - GET /gists/{gist_id} — property: fork_of.user
  - GET /gists/{gist_id} — property: fork_of.user.login
  - GET /gists/{gist_id} — property: fork_of.owner
  - GET /gists/{gist_id} — property: user
  - GET /gists/{gist_id} — property: owner
  - POST /gists/{gist_id}/comments — property: user
  - POST /gists/{gist_id}/comments — property: user.login
  - GET /gists/{gist_id}/comments — property: user
  - GET /gists/{gist_id}/comments — property: user.login
  - PATCH /gists/{gist_id}/comments/{comment_id} — property: user
  - PATCH /gists/{gist_id}/comments/{comment_id} — property: user.login
  - GET /gists/{gist_id}/comments/{comment_id} — property: user
  - GET /gists/{gist_id}/comments/{comment_id} — property: user.login
  - POST /gists/{gist_id}/forks — property: owner
  - POST /gists/{gist_id}/forks — property: owner.login
  - GET /gists/{gist_id}/forks — property: fork_of.user
  - GET /gists/{gist_id}/forks — property: fork_of.user.login
  - GET /gists/{gist_id}/forks — property: fork_of.owner
  - GET /gists/{gist_id}/forks — property: user
  - GET /gists/{gist_id}/forks — property: owner
  - GET /gists/{gist_id}/{sha} — property: fork_of.user
  - GET /gists/{gist_id}/{sha} — property: fork_of.user.login
  - GET /gists/{gist_id}/{sha} — property: fork_of.owner
  - GET /gists/{gist_id}/{sha} — property: user
  - GET /gists/{gist_id}/{sha} — property: owner
  - GET /users/{username}/gists — url_segment: users
  - GET /users/{username}/gists — url_segment: username
  - GET /users/{username}/gists — property: owner
  - GET /users/{username}/gists — property: owner.login

Key fields (PK + fields referencing gists):
```json
{
  "collaborator": {
    "properties": {
      "id": {
        "type": "integer",
        "format": "int64",
        "examples": [
          1
        ]
      },
      "gists_url": {
        "type": "string",
        "examples": [
          "https://api.github.com/users/octocat/gists{/gist_id}"
        ]
      }
    },
    "required": [
      "gists_url",
      "id"
    ]
  },
  "private-user": {
    "properties": {
      "id": {
        "type": "integer",
        "format": "int64",
        "examples": [
          1
        ]
      },
      "gists_url": {
        "type": "string",
        "examples": [
          "https://api.github.com/users/octocat/gists{/gist_id}"
        ]
      },
      "public_gists": {
        "type": "integer",
        "examples": [
          1
        ]
      },
      "private_gists": {
        "type": "integer",
        "examples": [
          81
        ]
      }
    },
    "required": [
      "gists_url",
      "id",
      "public_gists",
      "private_gists"
    ]
  },
  "public-user": {
    "properties": {
      "id": {
        "type": "integer",
        "format": "int64"
      },
      "gists_url": {
        "type": "string"
      },
      "public_gists": {
        "type": "integer"
      },
      "private_gists": {
        "type": "integer",
        "examples": [
          1
        ]
      }
    },
    "required": [
      "gists_url",
      "id",
      "public_gists"
    ]
  },
  "simple-classroom-user": {
    "properties": {
      "id": {
        "type": "integer",
        "examples": [
          1
        ]
      }
    },
    "required": [
      "id"
    ]
  },
  "simple-user": {
    "properties": {
      "id": {
        "type": "integer",
        "format": "int64",
        "examples": [
          1
        ]
      },
      "gists_url": {
        "type": "string",
        "examples": [
          "https://api.github.com/users/octocat/gists{/gist_id}"
        ]
      }
    },
    "required": [
      "gists_url",
      "id"
    ]
  },
  "user-role-assignment": {
    "properties": {
      "id": {
        "type": "integer",
        "examples": [
          1
        ]
      },
      "gists_url": {
        "type": "string",
        "examples": [
          "https://api.github.com/users/octocat/gists{/gist_id}"
        ]
      }
    },
    "required": [
      "gists_url",
      "id"
    ]
  },
  "user-search-result-item": {
    "properties": {
      "id": {
        "type": "integer",
        "format": "int64"
      },
      "gists_url": {
        "type": "string"
      },
      "public_gists": {
        "type": "integer"
      }
    },
    "required": [
      "gists_url",
      "id"
    ]
  }
}
```


---

## External Schemas

These schemas reference **gists** but belong to entities that are
**not part of this implementation**. Do NOT create FK columns, relationship
declarations, or stub models for them. They are shown only so you understand
how gists appears in the broader API.

### gist-comment
```json
{
  "title": "Gist Comment",
  "description": "A comment made to a gist.",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "examples": [
        1
      ]
    },
    "node_id": {
      "type": "string",
      "examples": [
        "MDExOkdpc3RDb21tZW50MQ=="
      ]
    },
    "url": {
      "type": "string",
      "format": "uri",
      "examples": [
        "https://api.github.com/gists/a6db0bec360bb87e9418/comments/1"
      ]
    },
    "body": {
      "description": "The comment text.",
      "type": "string",
      "maxLength": 65535,
      "examples": [
        "Body of the attachment"
      ]
    },
    "user": {
      "anyOf": [
        {
          "type": "null"
        },
        {
          "$ref": "#/components/schemas/simple-user"
        }
      ]
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "examples": [
        "2011-04-18T23:23:56Z"
      ]
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "examples": [
        "2011-04-18T23:23:56Z"
      ]
    },
    "author_association": {
      "$ref": "#/components/schemas/author-association"
    }
  },
  "required": [
    "url",
    "id",
    "node_id",
    "user",
    "body",
    "author_association",
    "created_at",
    "updated_at"
  ]
}
```


---

## Implementation Rules for Pass 2

### What to add

- **FK columns** in `database/schema.py`: add `mapped_column(ForeignKey(...))`
  for each identified relationship. Use the evidence and schema shapes above
  to determine:
  - Which fields become FK columns (look for `_id` suffixed fields, nested
    objects with `id`, and `$ref` pointers to related resource schemas)
  - Whether `nullable=False` (required) or `nullable=True` (optional),
    based on the schema's `required` list
  - The correct column type (must match the target table's PK type)
- **Indexes** in `__table_args__`: add `Index()` for every new FK column
- **relationship() declarations**: add on both sides (this model and the
  target model). Use `foreign_keys=[col]` when multiple FKs point at the
  same table. Use `remote_side=[id]` for self-referential relationships.
- **Association tables**: for M:N relationships, add a `Table()` with
  composite primary key above the model classes
- **Stub models**: if a FK target model does not yet exist in schema.py,
  create a minimal stub marked with `# STUB — expand when implementing this resource`
- **Update operations**: add eager loading (`joinedload`/`selectinload`)
  where FK-related queries need it
- **Update serializers**: where the API response includes nested related
  objects (not just an ID), update the serializer to include them

### What NOT to do

- Do not modify the base columns, CRUD logic, or route handlers from Pass 1
  unless necessary for FK support
- Do not create FK columns or relationships for entities listed in
  External Schemas — those are context only
- Do not guess relationships that aren't supported by the evidence above
