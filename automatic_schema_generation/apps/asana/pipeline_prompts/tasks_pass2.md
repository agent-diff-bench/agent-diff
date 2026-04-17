# Entity Implementation (Pass 2 — Relationships): tasks

You are adding foreign key relationships to the **tasks** resource
(`AsanaTask` in `asana_tasks`). The base model, operations,
serializers, and routes already exist from Pass 1.

The full OpenAPI spec is available at: `/Users/azh/agent-diff/automatic_schema_generation/open_api_schemas/asana_oas.json`
If any information in this prompt is unclear or seems incorrect, read the
spec directly to resolve ambiguities.

Read the existing files in the target directory first. You will modify them
to add FK columns, relationship() declarations, indexes, association tables,
and update operations/serializers to handle the new relationships.

Files to edit (all under `/Users/azh/agent-diff/backend/src/services/asana`):
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

These resources have a demonstrated relationship with **tasks**
through shared endpoints, FK-shaped property names, or schema cross-references.

Direction key:
- **outgoing** — tasks's schemas contain fields that reference
  the related resource (e.g. a `_id` field or nested object pointing there).
  **Action**: add a FK column on `asana_tasks` pointing at the related
  resource's table, plus a `relationship()` on both sides.
- **incoming** — the related resource's endpoints reference tasks
  (the subject of those endpoints is the other resource, not tasks).
  **Action**: do NOT add a FK column on `asana_tasks`. The FK lives on the
  other resource's table. Add only a `relationship()` on the tasks
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

### projects
- Table: `asana_projects`
- Primary key: `gid`
- Direction: outgoing, incoming
- **Fields referencing projects**: `data.attributable_to`, `data.memberships.project`, `data.new_project`, `data.new_task`, `data.project`, `data.projects`

These fields all point at the `asana_projects` table. Infer the correct FK relationship type and apply using the reference patterns above.

Evidence:
  - GET /tasks — query: project
  - POST /tasks — query: project
  - POST /tasks — property: data.memberships.project
  - POST /tasks — property: data.projects
  - POST /tasks — property: data.memberships.project
  - POST /tasks — property: data.projects
  - PUT /tasks/{task_gid} — property: data.memberships.project
  - PUT /tasks/{task_gid} — property: data.projects
  - PUT /tasks/{task_gid} — property: data.memberships.project
  - PUT /tasks/{task_gid} — property: data.projects
  - GET /tasks/{task_gid} — property: data.memberships.project
  - GET /tasks/{task_gid} — property: data.projects
  - POST /tasks/{task_gid}/duplicate — property: data.new_project
  - GET /projects/{project_gid}/tasks — url_segment: projects
  - GET /projects/{project_gid}/tasks — url_segment: project_gid
  - POST /tasks/{task_gid}/subtasks — property: data.memberships.project
  - POST /tasks/{task_gid}/subtasks — property: data.projects
  - POST /tasks/{task_gid}/subtasks — property: data.memberships.project
  - POST /tasks/{task_gid}/subtasks — property: data.projects
  - POST /tasks/{task_gid}/setParent — property: data.memberships.project
  - POST /tasks/{task_gid}/setParent — property: data.projects
  - POST /tasks/{task_gid}/addProject — property: data.project
  - POST /tasks/{task_gid}/removeProject — property: data.project
  - POST /tasks/{task_gid}/addFollowers — property: data.memberships.project
  - POST /tasks/{task_gid}/addFollowers — property: data.projects
  - POST /tasks/{task_gid}/removeFollowers — property: data.memberships.project
  - POST /tasks/{task_gid}/removeFollowers — property: data.projects
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.memberships.project
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.projects
  - GET /tasks/{task_gid}/time_tracking_entries — property: data.attributable_to
  - POST /tasks/{task_gid}/time_tracking_entries — property: data.attributable_to
  - POST /projects/{project_gid}/duplicate — property: data.new_task (incoming)
  - GET /tasks/{task_gid}/projects — url_segment: tasks (incoming)
  - GET /tasks/{task_gid}/projects — url_segment: task_gid (incoming)
  - POST /projects/{project_gid}/saveAsTemplate — property: data.new_task (incoming)

Key fields (PK + fields referencing tasks):
```json
{
  "ProjectCompact": {
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      }
    }
  }
}
```

### sections
- Table: `asana_sections`
- Primary key: `gid`
- Direction: outgoing, incoming
- **Fields referencing sections**: `data.assignee_section`, `data.memberships.section`, `data.section`, `data.task`

These fields all point at the `asana_sections` table. Infer the correct FK relationship type and apply using the reference patterns above.

Evidence:
  - GET /tasks — query: section
  - POST /tasks — query: section
  - POST /tasks — property: data.memberships.section
  - POST /tasks — property: data.memberships.section
  - POST /tasks — property: data.assignee_section
  - PUT /tasks/{task_gid} — property: data.memberships.section
  - PUT /tasks/{task_gid} — property: data.memberships.section
  - PUT /tasks/{task_gid} — property: data.assignee_section
  - GET /tasks/{task_gid} — property: data.memberships.section
  - GET /tasks/{task_gid} — property: data.assignee_section
  - GET /sections/{section_gid}/tasks — url_segment: sections
  - GET /sections/{section_gid}/tasks — url_segment: section_gid
  - POST /tasks/{task_gid}/subtasks — property: data.memberships.section
  - POST /tasks/{task_gid}/subtasks — property: data.memberships.section
  - POST /tasks/{task_gid}/subtasks — property: data.assignee_section
  - POST /tasks/{task_gid}/setParent — property: data.memberships.section
  - POST /tasks/{task_gid}/setParent — property: data.assignee_section
  - POST /tasks/{task_gid}/addProject — property: data.section
  - POST /tasks/{task_gid}/addFollowers — property: data.memberships.section
  - POST /tasks/{task_gid}/addFollowers — property: data.assignee_section
  - POST /tasks/{task_gid}/removeFollowers — property: data.memberships.section
  - POST /tasks/{task_gid}/removeFollowers — property: data.assignee_section
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.memberships.section
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.assignee_section
  - POST /sections/{section_gid}/addTask — property: data.task (incoming)

Key fields (PK + fields referencing tasks):
```json
{
  "SectionCompact": {
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      }
    }
  },
  "SectionTaskInsertRequest": {
    "properties": {
      "task": {
        "description": "The task to add to this section.",
        "type": "string",
        "example": "123456"
      }
    },
    "required": [
      "task"
    ]
  }
}
```

### stories
- Table: `asana_stories`
- Primary key: `gid`
- Direction: incoming
- **Fields referencing stories**: `data.dependency`, `data.duplicate_of`, `data.duplicated_from`, `data.target`, `data.task`

These fields all point at the `asana_stories` table. Infer the correct FK relationship type and apply using the reference patterns above.

Evidence:
  - PUT /stories/{story_gid} — property: data.task (incoming)
  - PUT /stories/{story_gid} — property: data.duplicate_of (incoming)
  - PUT /stories/{story_gid} — property: data.duplicated_from (incoming)
  - PUT /stories/{story_gid} — property: data.dependency (incoming)
  - PUT /stories/{story_gid} — property: data.target (incoming)
  - GET /stories/{story_gid} — property: data.task (incoming)
  - GET /stories/{story_gid} — property: data.duplicate_of (incoming)
  - GET /stories/{story_gid} — property: data.duplicated_from (incoming)
  - GET /stories/{story_gid} — property: data.dependency (incoming)
  - GET /stories/{story_gid} — property: data.target (incoming)
  - GET /tasks/{task_gid}/stories — url_segment: tasks (incoming)
  - GET /tasks/{task_gid}/stories — url_segment: task_gid (incoming)
  - POST /tasks/{task_gid}/stories — url_segment: tasks (incoming)
  - POST /tasks/{task_gid}/stories — url_segment: task_gid (incoming)
  - POST /tasks/{task_gid}/stories — property: data.task (incoming)
  - POST /tasks/{task_gid}/stories — property: data.duplicate_of (incoming)
  - POST /tasks/{task_gid}/stories — property: data.duplicated_from (incoming)
  - POST /tasks/{task_gid}/stories — property: data.dependency (incoming)
  - POST /tasks/{task_gid}/stories — property: data.target (incoming)
  - POST /goals/{goal_gid}/stories — property: data.task (incoming)
  - POST /goals/{goal_gid}/stories — property: data.duplicate_of (incoming)
  - POST /goals/{goal_gid}/stories — property: data.duplicated_from (incoming)
  - POST /goals/{goal_gid}/stories — property: data.dependency (incoming)
  - POST /goals/{goal_gid}/stories — property: data.target (incoming)

Key fields (PK + fields referencing tasks):
```json
{
  "StoryBase": {
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      }
    }
  },
  "StoryCompact": {
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      }
    }
  }
}
```

### tags
- Table: `asana_tags`
- Primary key: `gid`
- Direction: outgoing, incoming
- **Fields referencing tags**: `data.tag`, `data.tags`

These fields all point at the `asana_tags` table. Infer the correct FK relationship type and apply using the reference patterns above.

Evidence:
  - POST /tasks — property: data.tags
  - POST /tasks — property: data.tags
  - PUT /tasks/{task_gid} — property: data.tags
  - PUT /tasks/{task_gid} — property: data.tags
  - GET /tasks/{task_gid} — property: data.tags
  - GET /tags/{tag_gid}/tasks — url_segment: tags
  - GET /tags/{tag_gid}/tasks — url_segment: tag_gid
  - POST /tasks/{task_gid}/subtasks — property: data.tags
  - POST /tasks/{task_gid}/subtasks — property: data.tags
  - POST /tasks/{task_gid}/setParent — property: data.tags
  - POST /tasks/{task_gid}/addTag — property: data.tag
  - POST /tasks/{task_gid}/removeTag — property: data.tag
  - POST /tasks/{task_gid}/addFollowers — property: data.tags
  - POST /tasks/{task_gid}/removeFollowers — property: data.tags
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.tags
  - GET /tasks/{task_gid}/tags — url_segment: tasks (incoming)
  - GET /tasks/{task_gid}/tags — url_segment: task_gid (incoming)

Key fields (PK + fields referencing tasks):
```json
{
  "TagCompact": {
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      }
    }
  }
}
```

### tasks
- **SELF-REFERENTIAL** — this resource references itself
- Use the Self Referential pattern: nullable FK to own table,
  `remote_side=[id]` on the parent relationship
- Table: `asana_tasks`
- Primary key: `gid`
- Direction: outgoing
- **Fields referencing tasks**: `data`

These fields create a self-referential hierarchy. Add a nullable FK column (e.g. `parent_id`) pointing at `asana_tasks.gid` with `remote_side=[gid]`.

Evidence:
  - GET /tasks — url_segment: tasks
  - GET /tasks — property: data
  - POST /tasks — url_segment: tasks
  - POST /tasks — property: data
  - POST /tasks — property: data
  - POST /tasks — property: data.parent
  - PUT /tasks/{task_gid} — url_segment: tasks
  - PUT /tasks/{task_gid} — url_segment: task_gid
  - PUT /tasks/{task_gid} — property: data
  - PUT /tasks/{task_gid} — property: data
  - PUT /tasks/{task_gid} — property: data.parent
  - GET /tasks/{task_gid} — url_segment: tasks
  - GET /tasks/{task_gid} — url_segment: task_gid
  - GET /tasks/{task_gid} — property: data
  - GET /tasks/{task_gid} — property: data.parent
  - DELETE /tasks/{task_gid} — url_segment: tasks
  - DELETE /tasks/{task_gid} — url_segment: task_gid
  - POST /tasks/{task_gid}/duplicate — url_segment: tasks
  - POST /tasks/{task_gid}/duplicate — url_segment: task_gid
  - POST /tasks/{task_gid}/duplicate — property: data.new_task
  - GET /projects/{project_gid}/tasks — url_segment: tasks
  - GET /projects/{project_gid}/tasks — property: data
  - GET /sections/{section_gid}/tasks — url_segment: tasks
  - GET /sections/{section_gid}/tasks — property: data
  - GET /tags/{tag_gid}/tasks — url_segment: tasks
  - GET /tags/{tag_gid}/tasks — property: data
  - GET /user_task_lists/{user_task_list_gid}/tasks — url_segment: tasks
  - GET /user_task_lists/{user_task_list_gid}/tasks — property: data
  - GET /tasks/{task_gid}/subtasks — url_segment: tasks
  - GET /tasks/{task_gid}/subtasks — url_segment: task_gid
  - GET /tasks/{task_gid}/subtasks — property: data
  - POST /tasks/{task_gid}/subtasks — url_segment: tasks
  - POST /tasks/{task_gid}/subtasks — url_segment: task_gid
  - POST /tasks/{task_gid}/subtasks — property: data
  - POST /tasks/{task_gid}/subtasks — property: data
  - POST /tasks/{task_gid}/subtasks — property: data.parent
  - POST /tasks/{task_gid}/setParent — url_segment: tasks
  - POST /tasks/{task_gid}/setParent — url_segment: task_gid
  - POST /tasks/{task_gid}/setParent — property: data
  - POST /tasks/{task_gid}/setParent — property: data.parent
  - GET /tasks/{task_gid}/dependencies — url_segment: tasks
  - GET /tasks/{task_gid}/dependencies — url_segment: task_gid
  - GET /tasks/{task_gid}/dependencies — property: data
  - POST /tasks/{task_gid}/addDependencies — url_segment: tasks
  - POST /tasks/{task_gid}/addDependencies — url_segment: task_gid
  - POST /tasks/{task_gid}/removeDependencies — url_segment: tasks
  - POST /tasks/{task_gid}/removeDependencies — url_segment: task_gid
  - GET /tasks/{task_gid}/dependents — url_segment: tasks
  - GET /tasks/{task_gid}/dependents — url_segment: task_gid
  - GET /tasks/{task_gid}/dependents — property: data
  - POST /tasks/{task_gid}/addDependents — url_segment: tasks
  - POST /tasks/{task_gid}/addDependents — url_segment: task_gid
  - POST /tasks/{task_gid}/removeDependents — url_segment: tasks
  - POST /tasks/{task_gid}/removeDependents — url_segment: task_gid
  - POST /tasks/{task_gid}/addProject — url_segment: tasks
  - POST /tasks/{task_gid}/addProject — url_segment: task_gid
  - POST /tasks/{task_gid}/removeProject — url_segment: tasks
  - POST /tasks/{task_gid}/removeProject — url_segment: task_gid
  - POST /tasks/{task_gid}/addTag — url_segment: tasks
  - POST /tasks/{task_gid}/addTag — url_segment: task_gid
  - POST /tasks/{task_gid}/removeTag — url_segment: tasks
  - POST /tasks/{task_gid}/removeTag — url_segment: task_gid
  - POST /tasks/{task_gid}/addFollowers — url_segment: tasks
  - POST /tasks/{task_gid}/addFollowers — url_segment: task_gid
  - POST /tasks/{task_gid}/addFollowers — property: data
  - POST /tasks/{task_gid}/addFollowers — property: data.parent
  - POST /tasks/{task_gid}/removeFollowers — url_segment: tasks
  - POST /tasks/{task_gid}/removeFollowers — url_segment: task_gid
  - POST /tasks/{task_gid}/removeFollowers — property: data
  - POST /tasks/{task_gid}/removeFollowers — property: data.parent
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — url_segment: tasks
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.parent
  - GET /workspaces/{workspace_gid}/tasks/search — url_segment: tasks
  - GET /workspaces/{workspace_gid}/tasks/search — property: data
  - GET /tasks/{task_gid}/time_tracking_entries — url_segment: tasks
  - GET /tasks/{task_gid}/time_tracking_entries — url_segment: task_gid
  - POST /tasks/{task_gid}/time_tracking_entries — url_segment: tasks
  - POST /tasks/{task_gid}/time_tracking_entries — url_segment: task_gid
  - POST /tasks/{task_gid}/time_tracking_entries — property: data.task

Key fields (PK + fields referencing tasks):
```json
{
  "TaskCompact": {
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      }
    }
  }
}
```

### users
- Table: `asana_users`
- Primary key: `gid`
- Direction: outgoing
- **Fields referencing users**: `data`

These fields all point at the `asana_users` table. Infer the correct FK relationship type and apply using the reference patterns above.

Evidence:
  - GET /tasks — query: assignee
  - GET /tasks — property: data.created_by
  - POST /tasks — query: assignee
  - POST /tasks — property: data.created_by
  - POST /tasks — property: data.assigned_by
  - POST /tasks — property: data.completed_by
  - POST /tasks — property: data.hearts.user
  - POST /tasks — property: data.assignee
  - POST /tasks — property: data.followers
  - POST /tasks — property: data.created_by
  - POST /tasks — property: data.assigned_by
  - POST /tasks — property: data.completed_by
  - POST /tasks — property: data.hearts.user
  - POST /tasks — property: data.assignee
  - POST /tasks — property: data.custom_fields.created_by
  - POST /tasks — property: data.custom_fields.people_value
  - POST /tasks — property: data.followers
  - PUT /tasks/{task_gid} — property: data.created_by
  - PUT /tasks/{task_gid} — property: data.assigned_by
  - PUT /tasks/{task_gid} — property: data.completed_by
  - PUT /tasks/{task_gid} — property: data.hearts.user
  - PUT /tasks/{task_gid} — property: data.assignee
  - PUT /tasks/{task_gid} — property: data.followers
  - PUT /tasks/{task_gid} — property: data.created_by
  - PUT /tasks/{task_gid} — property: data.assigned_by
  - PUT /tasks/{task_gid} — property: data.completed_by
  - PUT /tasks/{task_gid} — property: data.hearts.user
  - PUT /tasks/{task_gid} — property: data.assignee
  - PUT /tasks/{task_gid} — property: data.custom_fields.created_by
  - PUT /tasks/{task_gid} — property: data.custom_fields.people_value
  - PUT /tasks/{task_gid} — property: data.followers
  - GET /tasks/{task_gid} — property: data.created_by
  - GET /tasks/{task_gid} — property: data.assigned_by
  - GET /tasks/{task_gid} — property: data.completed_by
  - GET /tasks/{task_gid} — property: data.hearts.user
  - GET /tasks/{task_gid} — property: data.assignee
  - GET /tasks/{task_gid} — property: data.custom_fields.created_by
  - GET /tasks/{task_gid} — property: data.custom_fields.people_value
  - GET /tasks/{task_gid} — property: data.followers
  - POST /tasks/{task_gid}/duplicate — property: data.new_task.created_by
  - GET /projects/{project_gid}/tasks — property: data.created_by
  - GET /sections/{section_gid}/tasks — property: data.created_by
  - GET /tags/{tag_gid}/tasks — property: data.created_by
  - GET /user_task_lists/{user_task_list_gid}/tasks — property: data.created_by
  - GET /tasks/{task_gid}/subtasks — property: data.created_by
  - POST /tasks/{task_gid}/subtasks — property: data.created_by
  - POST /tasks/{task_gid}/subtasks — property: data.assigned_by
  - POST /tasks/{task_gid}/subtasks — property: data.completed_by
  - POST /tasks/{task_gid}/subtasks — property: data.hearts.user
  - POST /tasks/{task_gid}/subtasks — property: data.assignee
  - POST /tasks/{task_gid}/subtasks — property: data.followers
  - POST /tasks/{task_gid}/subtasks — property: data.created_by
  - POST /tasks/{task_gid}/subtasks — property: data.assigned_by
  - POST /tasks/{task_gid}/subtasks — property: data.completed_by
  - POST /tasks/{task_gid}/subtasks — property: data.hearts.user
  - POST /tasks/{task_gid}/subtasks — property: data.assignee
  - POST /tasks/{task_gid}/subtasks — property: data.custom_fields.created_by
  - POST /tasks/{task_gid}/subtasks — property: data.custom_fields.people_value
  - POST /tasks/{task_gid}/subtasks — property: data.followers
  - POST /tasks/{task_gid}/setParent — property: data.created_by
  - POST /tasks/{task_gid}/setParent — property: data.assigned_by
  - POST /tasks/{task_gid}/setParent — property: data.completed_by
  - POST /tasks/{task_gid}/setParent — property: data.hearts.user
  - POST /tasks/{task_gid}/setParent — property: data.assignee
  - POST /tasks/{task_gid}/setParent — property: data.custom_fields.created_by
  - POST /tasks/{task_gid}/setParent — property: data.custom_fields.people_value
  - POST /tasks/{task_gid}/setParent — property: data.followers
  - GET /tasks/{task_gid}/dependencies — property: data.created_by
  - GET /tasks/{task_gid}/dependents — property: data.created_by
  - POST /tasks/{task_gid}/addFollowers — property: data
  - POST /tasks/{task_gid}/addFollowers — property: data.followers
  - POST /tasks/{task_gid}/addFollowers — property: data.created_by
  - POST /tasks/{task_gid}/addFollowers — property: data.assigned_by
  - POST /tasks/{task_gid}/addFollowers — property: data.completed_by
  - POST /tasks/{task_gid}/addFollowers — property: data.hearts.user
  - POST /tasks/{task_gid}/addFollowers — property: data.assignee
  - POST /tasks/{task_gid}/addFollowers — property: data.custom_fields.created_by
  - POST /tasks/{task_gid}/addFollowers — property: data.custom_fields.people_value
  - POST /tasks/{task_gid}/addFollowers — property: data.followers
  - POST /tasks/{task_gid}/removeFollowers — property: data
  - POST /tasks/{task_gid}/removeFollowers — property: data.followers
  - POST /tasks/{task_gid}/removeFollowers — property: data.created_by
  - POST /tasks/{task_gid}/removeFollowers — property: data.assigned_by
  - POST /tasks/{task_gid}/removeFollowers — property: data.completed_by
  - POST /tasks/{task_gid}/removeFollowers — property: data.hearts.user
  - POST /tasks/{task_gid}/removeFollowers — property: data.assignee
  - POST /tasks/{task_gid}/removeFollowers — property: data.custom_fields.created_by
  - POST /tasks/{task_gid}/removeFollowers — property: data.custom_fields.people_value
  - POST /tasks/{task_gid}/removeFollowers — property: data.followers
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.created_by
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.assigned_by
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.completed_by
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.hearts.user
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.assignee
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.custom_fields.created_by
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.custom_fields.people_value
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.followers
  - GET /workspaces/{workspace_gid}/tasks/search — property: data.created_by
  - GET /tasks/{task_gid}/time_tracking_entries — property: data.created_by
  - POST /tasks/{task_gid}/time_tracking_entries — property: data.created_by
  - POST /tasks/{task_gid}/time_tracking_entries — property: data.task.created_by

Key fields (PK + fields referencing tasks):
```json
{
  "UserCompact": {
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      }
    }
  }
}
```

### workspaces
- Table: `asana_workspaces`
- Primary key: `gid`
- Direction: outgoing
- **Fields referencing workspaces**: `data.workspace`

These fields all point at the `asana_workspaces` table. Infer the correct FK relationship type and apply using the reference patterns above.

Evidence:
  - GET /tasks — query: workspace
  - POST /tasks — query: workspace
  - POST /tasks — property: data.workspace
  - POST /tasks — property: data.workspace
  - PUT /tasks/{task_gid} — property: data.workspace
  - PUT /tasks/{task_gid} — property: data.workspace
  - GET /tasks/{task_gid} — property: data.workspace
  - POST /tasks/{task_gid}/subtasks — property: data.workspace
  - POST /tasks/{task_gid}/subtasks — property: data.workspace
  - POST /tasks/{task_gid}/setParent — property: data.workspace
  - POST /tasks/{task_gid}/addFollowers — property: data.workspace
  - POST /tasks/{task_gid}/removeFollowers — property: data.workspace
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — url_segment: workspaces
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — url_segment: workspace_gid
  - GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id} — property: data.workspace
  - GET /workspaces/{workspace_gid}/tasks/search — url_segment: workspaces
  - GET /workspaces/{workspace_gid}/tasks/search — url_segment: workspace_gid

Key fields (PK + fields referencing tasks):
```json
{
  "WorkspaceCompact": {
    "properties": {
      "gid": {
        "description": "Globally unique identifier of the resource, as a string.",
        "type": "string",
        "readOnly": true,
        "example": "12345",
        "x-insert-after": false
      }
    }
  }
}
```


---

## External Schemas

These schemas reference **tasks** but belong to entities that are
**not part of this implementation**. Do NOT create FK columns, relationship
declarations, or stub models for them. They are shown only so you understand
how tasks appears in the broader API.

### TaskAddProjectRequest
```json
{
  "type": "object",
  "properties": {
    "project": {
      "description": "The project to add the task to.",
      "type": "string",
      "example": "13579"
    },
    "insert_after": {
      "description": "A task in the project to insert the task after, or `null` to insert at the beginning of the list. When used with `section`, `null` will insert at the beginning of the specified section, otherwise the task must be in the specified section.",
      "type": "string",
      "nullable": true,
      "example": "124816"
    },
    "insert_before": {
      "description": "A task in the project to insert the task before, or `null` to insert at the end of the list. When used with `section`, `null` will insert at the end of the specified section, otherwise the task must be in the specified section.",
      "type": "string",
      "nullable": true,
      "example": "432134"
    },
    "section": {
      "description": "A section in the project to insert the task into. The task will be inserted at the bottom of the section unless combined with `insert_before: null` (end of section) or `insert_after: null` (beginning of section). Can also be combined with non-null `insert_before` or `insert_after` to position relative to a task within the section.",
      "type": "string",
      "nullable": true,
      "example": "987654"
    }
  },
  "required": [
    "project"
  ]
}
```

### TaskAddTagRequest
```json
{
  "type": "object",
  "properties": {
    "tag": {
      "description": "The tag's gid to add to the task.",
      "type": "string",
      "example": "13579"
    }
  },
  "required": [
    "tag"
  ]
}
```

### TaskCountResponse
```json
{
  "description": "A response object returned from the task count endpoint.",
  "type": "object",
  "properties": {
    "num_tasks": {
      "description": "The number of tasks in a project.",
      "type": "integer",
      "example": 200
    },
    "num_incomplete_tasks": {
      "description": "The number of incomplete tasks in a project.",
      "type": "integer",
      "example": 50
    },
    "num_completed_tasks": {
      "description": "The number of completed tasks in a project.",
      "type": "integer",
      "example": 150
    },
    "num_milestones": {
      "description": "The number of milestones in a project.",
      "type": "integer",
      "example": 10
    },
    "num_incomplete_milestones": {
      "description": "The number of incomplete milestones in a project.",
      "type": "integer",
      "example": 7
    },
    "num_completed_milestones": {
      "description": "The number of completed milestones in a project.",
      "type": "integer",
      "example": 3
    }
  }
}
```

### TaskDuplicateRequest
```json
{
  "type": "object",
  "properties": {
    "name": {
      "description": "The name of the new task.",
      "type": "string",
      "example": "New Task Name"
    },
    "include": {
      "description": "A comma-separated list of fields that will be duplicated to the new task.\n##### Fields\n- assignee\n- attachments\n- dates\n- dependencies\n- followers\n- notes\n- parent\n- projects\n- subtasks\n- tags",
      "type": "string",
      "pattern": "([notes|assignee|subtasks|attachments|tags|followers|projects|dates|dependencies|parent])(,\\1)*",
      "example": [
        "notes,assignee,subtasks,attachments,tags,followers,projects,dates,dependencies,parent"
      ]
    }
  }
}
```

### TaskRemoveProjectRequest
```json
{
  "type": "object",
  "properties": {
    "project": {
      "description": "The project to remove the task from.",
      "type": "string",
      "example": "13579"
    }
  },
  "required": [
    "project"
  ]
}
```

### TaskRemoveTagRequest
```json
{
  "type": "object",
  "properties": {
    "tag": {
      "description": "The tag's gid to remove from the task.",
      "type": "string",
      "example": "13579"
    }
  },
  "required": [
    "tag"
  ]
}
```

### TaskSetParentRequest
```json
{
  "type": "object",
  "properties": {
    "parent": {
      "description": "The new parent of the task, or `null` for no parent.",
      "type": "string",
      "example": "987654"
    },
    "insert_after": {
      "description": "A subtask of the parent to insert the task after, or `null` to insert at the beginning of the list.",
      "type": "string",
      "example": "null"
    },
    "insert_before": {
      "description": "A subtask of the parent to insert the task before, or `null` to insert at the end of the list.",
      "type": "string",
      "example": "124816"
    }
  },
  "required": [
    "parent"
  ]
}
```

### TaskTemplateBase
```json
{
  "allOf": [
    {
      "$ref": "#/components/schemas/TaskTemplateCompact"
    }
  ]
}
```

### TaskTemplateCompact
```json
{
  "description": "A *task template* is an object that allows new tasks to be created with a predefined setup.",
  "type": "object",
  "properties": {
    "gid": {
      "description": "Globally unique identifier of the resource, as a string.",
      "type": "string",
      "readOnly": true,
      "example": "12345",
      "x-insert-after": false
    },
    "resource_type": {
      "description": "The base type of this resource.",
      "type": "string",
      "readOnly": true,
      "example": "task_template",
      "x-insert-after": "gid"
    },
    "name": {
      "description": "Name of the task template.",
      "type": "string",
      "example": "Packing list"
    }
  }
}
```

### TaskTemplateInstantiateTaskRequest
```json
{
  "type": "object",
  "properties": {
    "name": {
      "description": "The name of the new task. If not provided, the name of the task template will be used.",
      "type": "string",
      "example": "New Task"
    }
  }
}
```

### TaskTemplateRecipe
```json
{
  "allOf": [
    {
      "$ref": "#/components/schemas/TaskTemplateRecipeCompact"
    },
    {
      "type": "object",
      "properties": {
        "description": {
          "description": "Description of the task that will be created from this template.",
          "type": "string",
          "example": "Please describe the bug you found and how to reproduce it."
        },
        "html_description": {
          "description": "HTML description of the task that will be created from this template.",
          "type": "string",
          "example": "Please describe the bug you found and how to reproduce it."
        },
        "memberships": {
          "description": "Array of projects that the task created from this template will be added to",
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/ProjectCompact"
          }
        },
        "relative_start_on": {
          "nullable": true,
          "description": "The number of days after the task has been instantiated on which that the task will start",
          "type": "integer",
          "example": 1
        },
        "relative_due_on": {
          "nullable": true,
          "description": "The number of days after the task has been instantiated on which that the task will be due",
          "type": "integer",
          "example": 2
        },
        "due_time": {
          "nullable": true,
          "description": "The time of day that the task will be due",
          "type": "string",
          "example": "13:15:00.000Z"
        },
        "dependencies": {
          "description": "Array of task templates that the task created from this template will depend on",
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/TaskTemplateRecipeCompact"
          }
        },
        "dependents": {
          "description": "Array of task templates that will depend on the task created from this template",
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/TaskTemplateRecipeCompact"
          }
        },
        "followers": {
          "description": "Array of users that will be added as followers to the task created from this template",
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/UserCompact"
          }
        },
        "attachments": {
          "description": "Array of attachments that will be added to the task created from this template",
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/AttachmentCompact"
          }
        },
        "subtasks": {
          "description": "Array of subtasks that will be added to the task created from this template",
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/TaskTemplateRecipeCompact"
          }
        },
        "custom_fields": {
          "description": "Array of custom fields that will be added to the task created from this template",
          "type": "array",
          "items": {
            "$ref": "#/components/schemas/CustomFieldCompact"
          }
        }
      }
    }
  ]
}
```

### TaskTemplateRecipeCompact
```json
{
  "type": "object",
  "properties": {
    "name": {
      "description": "Name of the task that will be created from this template.",
      "type": "string",
      "example": "Bug Report"
    },
    "task_resource_subtype": {
      "type": "string",
      "description": "The subtype of the task that will be created from this template.",
      "enum": [
        "default_task",
        "milestone_task",
        "approval_task"
      ],
      "example": "default_task"
    }
  }
}
```

### TaskTemplateResponse
```json
{
  "allOf": [
    {
      "$ref": "#/components/schemas/TaskTemplateBase"
    },
    {
      "type": "object",
      "properties": {
        "name": {
          "description": "Name of the task template.",
          "type": "string",
          "example": "Bug Report Template"
        },
        "project": {
          "description": "The project that this task template belongs to.",
          "nullable": true,
          "allOf": [
            {
              "$ref": "#/components/schemas/ProjectCompact"
            }
          ]
        },
        "template": {
          "description": "The configuration for the task that will be created from this template.",
          "allOf": [
            {
              "$ref": "#/components/schemas/TaskTemplateRecipe"
            }
          ]
        },
        "created_by": {
          "description": "The user who created this task template.",
          "allOf": [
            {
              "$ref": "#/components/schemas/UserCompact"
            }
          ]
        },
        "created_at": {
          "description": "The time at which this task template was created.",
          "type": "string",
          "format": "date-time",
          "example": "2019-01-01T00:00:00.000Z"
        }
      }
    }
  ]
}
```

### UserTaskListBase
```json
{
  "$ref": "#/components/schemas/UserTaskListCompact"
}
```

### UserTaskListCompact
```json
{
  "description": "A user task list represents the tasks assigned to a particular user. It provides API access to a user\u2019s [My tasks](https://asana.com/guide/help/fundamentals/my-tasks) view in Asana.",
  "type": "object",
  "properties": {
    "gid": {
      "description": "Globally unique identifier of the resource, as a string.",
      "type": "string",
      "readOnly": true,
      "example": "12345",
      "x-insert-after": false
    },
    "resource_type": {
      "description": "The base type of this resource.",
      "type": "string",
      "readOnly": true,
      "example": "user_task_list",
      "x-insert-after": "gid"
    },
    "name": {
      "description": "The name of the user task list.",
      "type": "string",
      "example": "My tasks in My Workspace"
    },
    "owner": {
      "description": "The owner of the user task list, i.e. the person whose My Tasks is represented by this resource.",
      "readOnly": true,
      "allOf": [
        {
          "$ref": "#/components/schemas/UserCompact"
        }
      ]
    },
    "workspace": {
      "description": "The workspace in which the user task list is located.",
      "readOnly": true,
      "allOf": [
        {
          "$ref": "#/components/schemas/WorkspaceCompact"
        }
      ]
    }
  }
}
```

### UserTaskListRequest
```json
{
  "$ref": "#/components/schemas/UserTaskListBase"
}
```

### UserTaskListResponse
```json
{
  "$ref": "#/components/schemas/UserTaskListBase"
}
```

Other schemas that reference this resource (context only):
- `AttachmentResponse` (refs: TaskCompact)
- `JobCompact` (refs: TaskCompact)
- `TimeTrackingEntryBase` (refs: TaskCompact)

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
  create a minimal stub marked with `# STUB — expand when implementing this resource`.
  If a stub already exists for the target model, leave it as-is — it will be
  expanded when that resource is implemented
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
