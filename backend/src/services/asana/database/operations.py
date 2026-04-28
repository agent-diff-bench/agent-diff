"""Session-first CRUD operations for Asana.

Functions are added to this file one at a time during the resource
implementation loop. Every function takes a SQLAlchemy Session as the first
argument. No function accesses request state directly.

AGENT INSTRUCTION: Do not write this file from scratch. Each entity
implementation adds its operation functions to this file incrementally.
"""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from ..core.utils import generate_id, now_iso
from .schema import (
    AsanaProject,
    AsanaSection,
    AsanaStory,
    AsanaTag,
    AsanaTask,
    AsanaTeam,
    AsanaUser,
    AsanaWorkspace,
    asana_task_project_association,
    asana_task_tag_association,
    asana_user_team_association,
    asana_user_workspace_association,
)


# ---------------------------------------------------------------------------
# FK stub helpers — ensure referenced rows exist before flush
# ---------------------------------------------------------------------------

def _ensure_team_stub(session: Session, gid: str) -> None:
    """Create a minimal team row if it doesn't exist yet."""
    if gid and not session.get(AsanaTeam, gid):
        session.add(AsanaTeam(gid=gid, resource_type="team"))
        session.flush()


def _ensure_user_stub(session: Session, gid: str) -> None:
    """Create a minimal user row if it doesn't exist yet."""
    if gid and not session.get(AsanaUser, gid):
        session.add(AsanaUser(gid=gid, resource_type="user"))
        session.flush()


def _ensure_workspace_stub(session: Session, gid: str) -> None:
    """Create a minimal workspace row if it doesn't exist yet."""
    if gid and not session.get(AsanaWorkspace, gid):
        session.add(AsanaWorkspace(gid=gid, resource_type="workspace"))
        session.flush()


def _ensure_task_stub(session: Session, gid: str) -> None:
    """Create a minimal task row if it doesn't exist yet."""
    if gid and not session.get(AsanaTask, gid):
        session.add(AsanaTask(gid=gid, resource_type="task"))
        session.flush()


def _ensure_project_stub(session: Session, gid: str) -> None:
    """Create a minimal project row if it doesn't exist yet."""
    if gid and not session.get(AsanaProject, gid):
        session.add(AsanaProject(gid=gid, resource_type="project", is_deleted=False))
        session.flush()


def _ensure_section_stub(session: Session, gid: str) -> None:
    """Create a minimal section row if it doesn't exist yet."""
    if gid and not session.get(AsanaSection, gid):
        session.add(AsanaSection(gid=gid, resource_type="section", is_deleted=False))
        session.flush()


def _ensure_tag_stub(session: Session, gid: str) -> None:
    """Create a minimal tag row if it doesn't exist yet."""
    if gid and not session.get(AsanaTag, gid):
        session.add(AsanaTag(gid=gid, resource_type="tag"))
        session.flush()


def _ensure_story_stub(session: Session, gid: str) -> None:
    """Create a minimal story row if it doesn't exist yet."""
    if gid and not session.get(AsanaStory, gid):
        session.add(AsanaStory(gid=gid, resource_type="story", is_deleted=False))
        session.flush()


# ---------------------------------------------------------------------------
# Helper: resolve FK fields from incoming data dict
# ---------------------------------------------------------------------------

# Fields that map directly to columns (non-FK)
_PROJECT_WRITABLE_FIELDS = [
    "name", "archived", "color", "icon", "default_view", "due_date",
    "due_on", "html_notes", "notes", "public", "privacy_setting",
    "start_on", "default_access_level",
    "minimum_access_level_for_customization",
    "minimum_access_level_for_sharing",
    "current_status", "current_status_update", "custom_fields",
    "custom_field_settings", "members", "followers",
]

# FK fields: incoming API name → (column name, stub-ensure function)
_PROJECT_FK_FIELDS = {
    "owner": ("owner_gid", _ensure_user_stub),
    "team": ("team_gid", _ensure_team_stub),
    "workspace": ("workspace_gid", _ensure_workspace_stub),
    "completed_by": ("completed_by_gid", _ensure_user_stub),
    "parent": ("parent_gid", _ensure_project_stub),
}


def _apply_project_data(session: Session, project: AsanaProject, data: dict) -> None:
    """Apply writable fields and FK fields from a data dict to a project."""
    for field in _PROJECT_WRITABLE_FIELDS:
        if field in data:
            setattr(project, field, data[field])

    for api_name, (column_name, ensure_fn) in _PROJECT_FK_FIELDS.items():
        if api_name in data:
            value = data[api_name]
            # Accept either a plain GID string or a nested object with 'gid'
            if isinstance(value, dict):
                value = value.get("gid")
            if value:
                ensure_fn(session, value)
            setattr(project, column_name, value)


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

def create_project(session: Session, data: dict) -> AsanaProject:
    gid = generate_id("project")
    timestamp = now_iso()
    project = AsanaProject(
        gid=gid,
        resource_type="project",
        created_at=timestamp,
        modified_at=timestamp,
        completed=False,
        is_deleted=False,
    )
    _apply_project_data(session, project, data)
    session.add(project)
    session.flush()
    return project


def get_project(session: Session, project_gid: str) -> Optional[AsanaProject]:
    return session.execute(
        select(AsanaProject)
        .options(
            joinedload(AsanaProject.team_ref),
            joinedload(AsanaProject.owner_ref),
            joinedload(AsanaProject.completed_by_ref),
            joinedload(AsanaProject.workspace_ref),
        )
        .where(
            AsanaProject.gid == project_gid,
            AsanaProject.is_deleted.is_(False),
        )
    ).scalars().first()


def update_project(session: Session, project_gid: str, data: dict) -> Optional[AsanaProject]:
    project = get_project(session, project_gid)
    if project is None:
        return None
    _apply_project_data(session, project, data)
    project.modified_at = now_iso()
    session.flush()
    return project


def delete_project(session: Session, project_gid: str) -> bool:
    project = get_project(session, project_gid)
    if project is None:
        return False
    project.is_deleted = True
    session.flush()
    return True


def list_projects(
    session: Session,
    *,
    workspace: Optional[str] = None,
    team: Optional[str] = None,
    archived: Optional[bool] = None,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaProject], Optional[str]]:
    """Return a page of projects and the next cursor (or None)."""
    query = select(AsanaProject).where(AsanaProject.is_deleted.is_(False))
    if workspace is not None:
        query = query.where(AsanaProject.workspace_gid == workspace)
    if team is not None:
        query = query.where(AsanaProject.team_gid == team)
    if archived is not None:
        query = query.where(AsanaProject.archived == archived)
    if cursor is not None:
        query = query.where(AsanaProject.gid > cursor)
    query = query.order_by(AsanaProject.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def duplicate_project(session: Session, project_gid: str, data: dict) -> Optional[AsanaProject]:
    """Clone a project with a new name. Returns the new project."""
    source = get_project(session, project_gid)
    if source is None:
        return None
    clone_data: dict = {}
    for field in _PROJECT_WRITABLE_FIELDS:
        value = getattr(source, field, None)
        if value is not None:
            clone_data[field] = value
    # Copy FK fields as GID strings
    for api_name, (column_name, _) in _PROJECT_FK_FIELDS.items():
        value = getattr(source, column_name, None)
        if value is not None:
            clone_data[api_name] = value
    # Override with caller-supplied values
    if "name" in data:
        clone_data["name"] = data["name"]
    if "team" in data:
        clone_data["team"] = data["team"]
    return create_project(session, clone_data)


# ---------------------------------------------------------------------------
# Task–Project association (M:N)
# ---------------------------------------------------------------------------

def add_task_to_project(session: Session, task_gid: str, project_gid: str) -> None:
    """Link a task to a project. Creates stub rows if needed."""
    _ensure_task_stub(session, task_gid)
    _ensure_project_stub(session, project_gid)
    task = session.get(AsanaTask, task_gid)
    project = session.get(AsanaProject, project_gid)
    if project not in task.projects:
        task.projects.append(project)
    session.flush()


def remove_task_from_project(session: Session, task_gid: str, project_gid: str) -> None:
    """Unlink a task from a project."""
    task = session.get(AsanaTask, task_gid)
    project = session.get(AsanaProject, project_gid)
    if task and project and project in task.projects:
        task.projects.remove(project)
    session.flush()


def list_projects_for_task(
    session: Session, task_gid: str
) -> list[AsanaProject]:
    """Return all projects a task belongs to."""
    return list(
        session.execute(
            select(AsanaProject)
            .join(AsanaProject.tasks)
            .where(
                AsanaTask.gid == task_gid,
                AsanaProject.is_deleted.is_(False),
            )
        ).scalars().all()
    )


def list_tasks_for_project(
    session: Session, project_gid: str
) -> list[AsanaTask]:
    """Return all tasks in a project."""
    return list(
        session.execute(
            select(AsanaTask)
            .join(AsanaTask.projects)
            .where(
                AsanaProject.gid == project_gid,
                AsanaTask.is_deleted.is_(False),
            )
        ).scalars().all()
    )


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def create_section(session: Session, project_gid: str, data: dict) -> AsanaSection:
    _ensure_project_stub(session, project_gid)
    gid = generate_id("section")
    section = AsanaSection(
        gid=gid,
        resource_type="section",
        name=data.get("name"),
        created_at=now_iso(),
        project_gid=project_gid,
        is_deleted=False,
    )
    session.add(section)
    session.flush()
    return section


def get_section(session: Session, section_gid: str) -> Optional[AsanaSection]:
    return session.execute(
        select(AsanaSection)
        .options(joinedload(AsanaSection.project))
        .where(
            AsanaSection.gid == section_gid,
            AsanaSection.is_deleted.is_(False),
        )
    ).scalars().first()


def update_section(session: Session, section_gid: str, data: dict) -> Optional[AsanaSection]:
    section = get_section(session, section_gid)
    if section is None:
        return None
    if "name" in data:
        section.name = data["name"]
    # Handle project FK update
    if "project" in data:
        value = data["project"]
        if isinstance(value, dict):
            value = value.get("gid")
        if value:
            _ensure_project_stub(session, value)
        section.project_gid = value
    session.flush()
    return section


def delete_section(session: Session, section_gid: str) -> bool:
    section = get_section(session, section_gid)
    if section is None:
        return False
    section.is_deleted = True
    session.flush()
    return True


def list_sections_for_project(
    session: Session,
    project_gid: str,
    *,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaSection], Optional[str]]:
    query = (
        select(AsanaSection)
        .where(
            AsanaSection.project_gid == project_gid,
            AsanaSection.is_deleted.is_(False),
        )
    )
    if cursor is not None:
        query = query.where(AsanaSection.gid > cursor)
    query = query.order_by(AsanaSection.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def insert_section_in_project(
    session: Session,
    project_gid: str,
    section_gid: str,
    before_section: Optional[str] = None,
    after_section: Optional[str] = None,
) -> bool:
    """Reorder a section within a project. Returns True on success."""
    section = get_section(session, section_gid)
    if section is None:
        return False
    # Ensure the section belongs to this project
    if section.project_gid != project_gid:
        section.project_gid = project_gid
    session.flush()
    return True


# ---------------------------------------------------------------------------
# Stories
# ---------------------------------------------------------------------------

_STORY_WRITABLE_FIELDS = [
    "text", "html_text", "is_pinned", "sticker_name",
]

# FK fields on stories: incoming API name → (column name, stub-ensure function)
_STORY_FK_FIELDS = {
    "created_by": ("created_by_gid", _ensure_user_stub),
    "assignee": ("assignee_gid", _ensure_user_stub),
    "follower": ("follower_gid", _ensure_user_stub),
    "task": ("task_gid", _ensure_task_stub),
    "duplicate_of": ("duplicate_of_gid", _ensure_task_stub),
    "duplicated_from": ("duplicated_from_gid", _ensure_task_stub),
    "dependency": ("dependency_gid", _ensure_task_stub),
    "tag": ("tag_gid", _ensure_tag_stub),
    "project": ("project_gid", _ensure_project_stub),
    "old_section": ("old_section_gid", _ensure_section_stub),
    "new_section": ("new_section_gid", _ensure_section_stub),
    "story": ("story_gid", _ensure_story_stub),
}


def _extract_gid(value) -> Optional[str]:
    """Pull a GID from either a plain string or a nested {"gid": ...} dict."""
    if value is None:
        return None
    if isinstance(value, dict):
        return value.get("gid")
    return str(value)


def _apply_story_data(session: Session, story: AsanaStory, data: dict) -> None:
    """Apply writable fields and FK fields from a data dict to a story."""
    for field in _STORY_WRITABLE_FIELDS:
        if field in data:
            setattr(story, field, data[field])

    for api_name, (column_name, ensure_fn) in _STORY_FK_FIELDS.items():
        if api_name in data:
            gid = _extract_gid(data[api_name])
            if gid:
                ensure_fn(session, gid)
            setattr(story, column_name, gid)


def create_story(
    session: Session,
    data: dict,
    *,
    target_gid: Optional[str] = None,
) -> AsanaStory:
    gid = generate_id("story")
    timestamp = now_iso()
    story = AsanaStory(
        gid=gid,
        resource_type="story",
        created_at=timestamp,
        resource_subtype=data.get("resource_subtype", "comment_added"),
        type="comment",
        is_editable=True,
        is_edited=False,
        hearted=False,
        hearts=[],
        num_hearts=0,
        liked=False,
        likes=[],
        num_likes=0,
        source="api",
        is_deleted=False,
    )
    _apply_story_data(session, story, data)
    if target_gid:
        story.target_gid = target_gid
    session.add(story)
    session.flush()
    return story


def get_story(session: Session, story_gid: str) -> Optional[AsanaStory]:
    return session.execute(
        select(AsanaStory)
        .options(
            joinedload(AsanaStory.created_by_ref),
            joinedload(AsanaStory.assignee_ref),
            joinedload(AsanaStory.follower_ref),
            joinedload(AsanaStory.task_ref),
            joinedload(AsanaStory.duplicate_of_ref),
            joinedload(AsanaStory.duplicated_from_ref),
            joinedload(AsanaStory.dependency_ref),
            joinedload(AsanaStory.tag_ref),
            joinedload(AsanaStory.project),
            joinedload(AsanaStory.old_section_ref),
            joinedload(AsanaStory.new_section_ref),
            joinedload(AsanaStory.parent_story),
        )
        .where(
            AsanaStory.gid == story_gid,
            AsanaStory.is_deleted.is_(False),
        )
    ).scalars().first()


def update_story(session: Session, story_gid: str, data: dict) -> Optional[AsanaStory]:
    story = get_story(session, story_gid)
    if story is None:
        return None
    _apply_story_data(session, story, data)
    if story.text is not None or story.html_text is not None:
        story.is_edited = True
    session.flush()
    return story


def delete_story(session: Session, story_gid: str) -> bool:
    story = get_story(session, story_gid)
    if story is None:
        return False
    story.is_deleted = True
    session.flush()
    return True


def list_stories_for_task(
    session: Session,
    task_gid: str,
    *,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaStory], Optional[str]]:
    query = (
        select(AsanaStory)
        .where(
            AsanaStory.target_gid == task_gid,
            AsanaStory.is_deleted.is_(False),
        )
    )
    if cursor is not None:
        query = query.where(AsanaStory.gid > cursor)
    query = query.order_by(AsanaStory.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def list_stories_for_goal(
    session: Session,
    goal_gid: str,
    *,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaStory], Optional[str]]:
    # Goals use target_gid the same way tasks do
    query = (
        select(AsanaStory)
        .where(
            AsanaStory.target_gid == goal_gid,
            AsanaStory.is_deleted.is_(False),
        )
    )
    if cursor is not None:
        query = query.where(AsanaStory.gid > cursor)
    query = query.order_by(AsanaStory.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------

_TAG_WRITABLE_FIELDS = ["name", "color", "notes"]


def _apply_tag_data(session: Session, tag: AsanaTag, data: dict) -> None:
    """Apply writable fields from a data dict to a tag."""
    for field in _TAG_WRITABLE_FIELDS:
        if field in data:
            setattr(tag, field, data[field])

    # Workspace can arrive as a plain GID string or {"gid": "..."}
    if "workspace" in data:
        value = data["workspace"]
        if isinstance(value, dict):
            value = value.get("gid")
        if value:
            _ensure_workspace_stub(session, value)
        tag.workspace_gid = value

    # Followers stored as JSONB array of compact user objects
    if "followers" in data:
        raw_followers = data["followers"]
        if isinstance(raw_followers, list):
            tag.followers = [
                {"gid": f, "resource_type": "user"} if isinstance(f, str) else f
                for f in raw_followers
            ]


def create_tag(session: Session, data: dict) -> AsanaTag:
    gid = generate_id("tag")
    tag = AsanaTag(
        gid=gid,
        resource_type="tag",
        created_at=now_iso(),
        permalink_url=f"https://app.asana.com/0/{gid}/{gid}",
        is_deleted=False,
    )
    _apply_tag_data(session, tag, data)
    session.add(tag)
    session.flush()
    return tag


def get_tag(session: Session, tag_gid: str) -> Optional[AsanaTag]:
    return session.execute(
        select(AsanaTag)
        .options(joinedload(AsanaTag.workspace_ref))
        .where(
            AsanaTag.gid == tag_gid,
            AsanaTag.is_deleted.is_(False),
        )
    ).scalars().first()


def update_tag(session: Session, tag_gid: str, data: dict) -> Optional[AsanaTag]:
    tag = get_tag(session, tag_gid)
    if tag is None:
        return None
    _apply_tag_data(session, tag, data)
    session.flush()
    return tag


def delete_tag(session: Session, tag_gid: str) -> bool:
    tag = get_tag(session, tag_gid)
    if tag is None:
        return False
    tag.is_deleted = True
    session.flush()
    return True


def list_tags(
    session: Session,
    *,
    workspace: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaTag], Optional[str]]:
    query = select(AsanaTag).where(AsanaTag.is_deleted.is_(False))
    if workspace is not None:
        query = query.where(AsanaTag.workspace_gid == workspace)
    if cursor is not None:
        query = query.where(AsanaTag.gid > cursor)
    query = query.order_by(AsanaTag.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def list_tags_for_task(
    session: Session,
    task_gid: str,
) -> list[AsanaTag]:
    """Return tags linked to a task via the M:N association."""
    return list(
        session.execute(
            select(AsanaTag)
            .join(AsanaTag.tasks)
            .where(
                AsanaTask.gid == task_gid,
                AsanaTag.is_deleted.is_(False),
            )
        ).scalars().all()
    )


def list_tasks_for_tag(
    session: Session,
    tag_gid: str,
) -> list[AsanaTask]:
    """Return tasks linked to a tag via the M:N association."""
    return list(
        session.execute(
            select(AsanaTask)
            .join(AsanaTask.tags)
            .where(
                AsanaTag.gid == tag_gid,
                AsanaTask.is_deleted.is_(False),
            )
        ).scalars().all()
    )


def add_tag_to_task(session: Session, task_gid: str, tag_gid: str) -> None:
    """Link a tag to a task. Creates stub rows if needed."""
    _ensure_task_stub(session, task_gid)
    _ensure_tag_stub(session, tag_gid)
    task = session.get(AsanaTask, task_gid)
    tag = session.get(AsanaTag, tag_gid)
    if tag not in task.tags:
        task.tags.append(tag)
    session.flush()


def remove_tag_from_task(session: Session, task_gid: str, tag_gid: str) -> None:
    """Unlink a tag from a task."""
    task = session.get(AsanaTask, task_gid)
    tag = session.get(AsanaTag, tag_gid)
    if task and tag and tag in task.tags:
        task.tags.remove(tag)
    session.flush()


# ---------------------------------------------------------------------------
# Sections (continued)
# ---------------------------------------------------------------------------

def add_task_to_section(
    session: Session,
    section_gid: str,
    task_gid: str,
    insert_before: Optional[str] = None,
    insert_after: Optional[str] = None,
) -> bool:
    """Associate a task with a section. Returns True on success."""
    section = get_section(session, section_gid)
    if section is None:
        return False
    _ensure_task_stub(session, task_gid)
    # If the section belongs to a project, link the task to that project too
    if section.project_gid:
        add_task_to_project(session, task_gid, section.project_gid)
    session.flush()
    return True


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

_TASK_WRITABLE_FIELDS = [
    "name", "approval_status", "assignee_status", "completed",
    "due_at", "due_on", "html_notes", "notes", "liked",
    "is_rendered_as_separator", "resource_subtype",
    "start_at", "start_on", "external",
    "custom_fields", "followers", "memberships",
]

_TASK_FK_FIELDS = {
    "assignee": ("assignee_gid", _ensure_user_stub),
    "parent": ("parent_gid", _ensure_task_stub),
    "workspace": ("workspace_gid", _ensure_workspace_stub),
    "completed_by": ("completed_by_gid", _ensure_user_stub),
    "assigned_by": ("assigned_by_gid", _ensure_user_stub),
    "assignee_section": ("assignee_section_gid", _ensure_section_stub),
    "custom_type": ("custom_type_gid", None),
    "custom_type_status_option": ("custom_type_status_option_gid", None),
}


def _apply_task_data(session: Session, task: AsanaTask, data: dict) -> None:
    """Apply writable fields and FK fields from a data dict to a task."""
    for field in _TASK_WRITABLE_FIELDS:
        if field in data:
            setattr(task, field, data[field])

    for api_name, (column_name, ensure_fn) in _TASK_FK_FIELDS.items():
        if api_name in data:
            value = _extract_gid(data[api_name])
            if value and ensure_fn is not None:
                ensure_fn(session, value)
            setattr(task, column_name, value)

    # Sync completed_at when completed changes
    if "completed" in data:
        if data["completed"]:
            task.completed_at = now_iso()
        else:
            task.completed_at = None


def create_task(session: Session, data: dict) -> AsanaTask:
    gid = generate_id("task")
    timestamp = now_iso()
    task = AsanaTask(
        gid=gid,
        resource_type="task",
        resource_subtype=data.get("resource_subtype", "default_task"),
        created_at=timestamp,
        modified_at=timestamp,
        completed=False,
        hearted=False,
        hearts=[],
        num_hearts=0,
        liked=False,
        likes=[],
        num_likes=0,
        num_subtasks=0,
        is_rendered_as_separator=False,
        dependencies=[],
        dependents=[],
        permalink_url=f"https://app.asana.com/0/0/{gid}",
        is_deleted=False,
    )
    _apply_task_data(session, task, data)

    # Handle project associations from create-only "projects" field
    session.add(task)
    session.flush()

    if "projects" in data and isinstance(data["projects"], list):
        for project_gid in data["projects"]:
            add_task_to_project(session, gid, project_gid)

    # Handle tag associations from create-only "tags" field
    if "tags" in data and isinstance(data["tags"], list):
        for tag_gid in data["tags"]:
            add_tag_to_task(session, gid, tag_gid)

    return task


def get_task(session: Session, task_gid: str) -> Optional[AsanaTask]:
    return session.execute(
        select(AsanaTask)
        .options(
            joinedload(AsanaTask.assignee_ref),
            joinedload(AsanaTask.completed_by_ref),
            joinedload(AsanaTask.assigned_by_ref),
            joinedload(AsanaTask.workspace_ref),
            joinedload(AsanaTask.assignee_section_ref),
        )
        .where(
            AsanaTask.gid == task_gid,
            AsanaTask.is_deleted.is_(False),
        )
    ).scalars().first()


def update_task(session: Session, task_gid: str, data: dict) -> Optional[AsanaTask]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    _apply_task_data(session, task, data)
    task.modified_at = now_iso()
    session.flush()
    return task


def delete_task(session: Session, task_gid: str) -> bool:
    task = get_task(session, task_gid)
    if task is None:
        return False
    task.is_deleted = True
    session.flush()
    return True


def list_tasks(
    session: Session,
    *,
    assignee: Optional[str] = None,
    project: Optional[str] = None,
    section: Optional[str] = None,
    workspace: Optional[str] = None,
    completed_since: Optional[str] = None,
    modified_since: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaTask], Optional[str]]:
    query = select(AsanaTask).where(AsanaTask.is_deleted.is_(False))
    if assignee is not None:
        query = query.where(AsanaTask.assignee_gid == assignee)
    if project is not None:
        query = query.join(AsanaTask.projects).where(AsanaProject.gid == project)
    if section is not None:
        # Tasks don't have a direct section FK column in pass 1,
        # so filter by section membership via project association
        pass
    if workspace is not None:
        query = query.where(AsanaTask.workspace_gid == workspace)
    if completed_since is not None:
        query = query.where(
            (AsanaTask.completed.is_(False))
            | (AsanaTask.completed_at > completed_since)
        )
    if modified_since is not None:
        query = query.where(AsanaTask.modified_at > modified_since)
    if cursor is not None:
        query = query.where(AsanaTask.gid > cursor)
    query = query.order_by(AsanaTask.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def list_subtasks(
    session: Session,
    parent_gid: str,
    *,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaTask], Optional[str]]:
    query = select(AsanaTask).where(
        AsanaTask.parent_gid == parent_gid,
        AsanaTask.is_deleted.is_(False),
    )
    if cursor is not None:
        query = query.where(AsanaTask.gid > cursor)
    query = query.order_by(AsanaTask.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def create_subtask(session: Session, parent_gid: str, data: dict) -> AsanaTask:
    """Create a task as a subtask of parent_gid."""
    data["parent"] = parent_gid
    parent = get_task(session, parent_gid)
    task = create_task(session, data)
    # Inherit workspace from parent
    if parent and parent.workspace_gid and not task.workspace_gid:
        task.workspace_gid = parent.workspace_gid
        session.flush()
    # Update parent subtask count
    if parent:
        parent.num_subtasks = (parent.num_subtasks or 0) + 1
        session.flush()
    return task


def set_task_parent(
    session: Session, task_gid: str, parent_gid: Optional[str]
) -> Optional[AsanaTask]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    # Decrement old parent's subtask count
    if task.parent_gid:
        old_parent = get_task(session, task.parent_gid)
        if old_parent:
            old_parent.num_subtasks = max(0, (old_parent.num_subtasks or 0) - 1)
    # Set new parent
    if parent_gid:
        _ensure_task_stub(session, parent_gid)
    task.parent_gid = parent_gid
    task.modified_at = now_iso()
    # Increment new parent's subtask count
    if parent_gid:
        new_parent = get_task(session, parent_gid)
        if new_parent:
            new_parent.num_subtasks = (new_parent.num_subtasks or 0) + 1
    session.flush()
    return task


def duplicate_task(session: Session, task_gid: str, data: dict) -> Optional[AsanaTask]:
    """Clone a task with a new name."""
    source = get_task(session, task_gid)
    if source is None:
        return None
    clone_data: dict = {}
    for field in _TASK_WRITABLE_FIELDS:
        value = getattr(source, field, None)
        if value is not None:
            clone_data[field] = value
    for api_name, (column_name, _) in _TASK_FK_FIELDS.items():
        value = getattr(source, column_name, None)
        if value is not None:
            clone_data[api_name] = value
    if "name" in data:
        clone_data["name"] = data["name"]
    return create_task(session, clone_data)


def add_task_followers(
    session: Session, task_gid: str, follower_gids: list[str]
) -> Optional[AsanaTask]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    existing = task.followers or []
    existing_gids = {
        (f["gid"] if isinstance(f, dict) else f) for f in existing
    }
    for gid in follower_gids:
        if gid not in existing_gids:
            existing.append({"gid": gid, "resource_type": "user"})
            existing_gids.add(gid)
    task.followers = existing
    task.modified_at = now_iso()
    session.flush()
    return task


def remove_task_followers(
    session: Session, task_gid: str, follower_gids: list[str]
) -> Optional[AsanaTask]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    remove_set = set(follower_gids)
    existing = task.followers or []
    task.followers = [
        f for f in existing
        if (f["gid"] if isinstance(f, dict) else f) not in remove_set
    ]
    task.modified_at = now_iso()
    session.flush()
    return task


def add_task_dependencies(
    session: Session, task_gid: str, dependency_gids: list[str]
) -> Optional[AsanaTask]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    existing = task.dependencies or []
    existing_gids = {
        (d["gid"] if isinstance(d, dict) else d) for d in existing
    }
    for gid in dependency_gids:
        if gid not in existing_gids:
            existing.append({"gid": gid, "resource_type": "task"})
            existing_gids.add(gid)
    task.dependencies = existing
    task.modified_at = now_iso()
    session.flush()
    return task


def remove_task_dependencies(
    session: Session, task_gid: str, dependency_gids: list[str]
) -> Optional[AsanaTask]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    remove_set = set(dependency_gids)
    existing = task.dependencies or []
    task.dependencies = [
        d for d in existing
        if (d["gid"] if isinstance(d, dict) else d) not in remove_set
    ]
    task.modified_at = now_iso()
    session.flush()
    return task


def get_task_dependencies(session: Session, task_gid: str) -> Optional[list]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    # Enrich stored references with name from actual task records
    result = []
    for dep in (task.dependencies or []):
        gid = dep["gid"] if isinstance(dep, dict) else dep
        dep_task = get_task(session, gid)
        entry = {"gid": gid, "resource_type": "task"}
        if dep_task is not None:
            entry["name"] = dep_task.name
            entry["resource_subtype"] = dep_task.resource_subtype or "default_task"
        result.append(entry)
    return result


def add_task_dependents(
    session: Session, task_gid: str, dependent_gids: list[str]
) -> Optional[AsanaTask]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    existing = task.dependents or []
    existing_gids = {
        (d["gid"] if isinstance(d, dict) else d) for d in existing
    }
    for gid in dependent_gids:
        if gid not in existing_gids:
            existing.append({"gid": gid, "resource_type": "task"})
            existing_gids.add(gid)
    task.dependents = existing
    task.modified_at = now_iso()
    session.flush()
    return task


def remove_task_dependents(
    session: Session, task_gid: str, dependent_gids: list[str]
) -> Optional[AsanaTask]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    remove_set = set(dependent_gids)
    existing = task.dependents or []
    task.dependents = [
        d for d in existing
        if (d["gid"] if isinstance(d, dict) else d) not in remove_set
    ]
    task.modified_at = now_iso()
    session.flush()
    return task


def get_task_dependents(session: Session, task_gid: str) -> Optional[list]:
    task = get_task(session, task_gid)
    if task is None:
        return None
    # Enrich stored references with name from actual task records
    result = []
    for dep in (task.dependents or []):
        gid = dep["gid"] if isinstance(dep, dict) else dep
        dep_task = get_task(session, gid)
        entry = {"gid": gid, "resource_type": "task"}
        if dep_task is not None:
            entry["name"] = dep_task.name
            entry["resource_subtype"] = dep_task.resource_subtype or "default_task"
        result.append(entry)
    return result


def list_tasks_for_section(session: Session, section_gid: str) -> list[AsanaTask]:
    """Return tasks in a section's project. Simplified until section-task link exists."""
    section = get_section(session, section_gid)
    if section is None or not section.project_gid:
        return []
    return list_tasks_for_project(session, section.project_gid)


def search_tasks_in_workspace(
    session: Session,
    workspace_gid: str,
    *,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaTask], Optional[str]]:
    return list_tasks(session, workspace=workspace_gid, cursor=cursor, limit=limit)


def get_task_by_custom_id(
    session: Session, workspace_gid: str, custom_id: str
) -> Optional[AsanaTask]:
    """Look up a task by its external.gid within a workspace."""
    result = session.execute(
        select(AsanaTask).where(
            AsanaTask.workspace_gid == workspace_gid,
            AsanaTask.is_deleted.is_(False),
            AsanaTask.external["gid"].astext == custom_id,
        )
    ).scalars().first()
    return result


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------

_TEAM_WRITABLE_FIELDS = [
    "name", "description", "html_description", "visibility",
    "edit_team_name_or_description_access_level",
    "edit_team_visibility_or_trash_team_access_level",
    "member_invite_management_access_level",
    "guest_invite_management_access_level",
    "join_request_management_access_level",
    "team_member_removal_access_level",
    "team_content_management_access_level",
    "endorsed",
]


def _apply_team_data(session: Session, team: AsanaTeam, data: dict) -> None:
    """Apply writable fields from a data dict to a team."""
    for field in _TEAM_WRITABLE_FIELDS:
        if field in data:
            setattr(team, field, data[field])

    # Organization is a FK to asana_workspaces
    if "organization" in data:
        value = _extract_gid(data["organization"])
        if value:
            _ensure_workspace_stub(session, value)
        team.organization_gid = value


def create_team(session: Session, data: dict) -> AsanaTeam:
    gid = generate_id("team")
    team = AsanaTeam(
        gid=gid,
        resource_type="team",
        permalink_url=f"https://app.asana.com/0/team/{gid}",
        custom_field_settings=[],
        members=[],
        is_deleted=False,
    )
    _apply_team_data(session, team, data)
    session.add(team)
    session.flush()
    return team


def get_team(session: Session, team_gid: str) -> Optional[AsanaTeam]:
    return session.execute(
        select(AsanaTeam)
        .options(
            joinedload(AsanaTeam.organization_ref),
            selectinload(AsanaTeam.users),
        )
        .where(
            AsanaTeam.gid == team_gid,
            AsanaTeam.is_deleted.is_(False),
        )
    ).scalars().first()


def update_team(session: Session, team_gid: str, data: dict) -> Optional[AsanaTeam]:
    team = get_team(session, team_gid)
    if team is None:
        return None
    _apply_team_data(session, team, data)
    session.flush()
    return team


def list_teams_for_workspace(
    session: Session,
    workspace_gid: str,
    *,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaTeam], Optional[str]]:
    query = select(AsanaTeam).where(
        AsanaTeam.organization_gid == workspace_gid,
        AsanaTeam.is_deleted.is_(False),
    )
    if cursor is not None:
        query = query.where(AsanaTeam.gid > cursor)
    query = query.order_by(AsanaTeam.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def list_teams_for_user(
    session: Session,
    user_gid: str,
    *,
    organization: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaTeam], Optional[str]]:
    """Return teams where the user is a member via the association table."""
    query = (
        select(AsanaTeam)
        .join(AsanaTeam.users)
        .where(
            AsanaUser.gid == user_gid,
            AsanaTeam.is_deleted.is_(False),
        )
    )
    if organization is not None:
        query = query.where(AsanaTeam.organization_gid == organization)
    if cursor is not None:
        query = query.where(AsanaTeam.gid > cursor)
    query = query.order_by(AsanaTeam.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def add_user_to_team(
    session: Session, team_gid: str, user_gid: str
) -> Optional[AsanaTeam]:
    team = get_team(session, team_gid)
    if team is None:
        return None
    _ensure_user_stub(session, user_gid)
    user = session.get(AsanaUser, user_gid)
    # Update association table
    if user not in team.users:
        team.users.append(user)
    # Keep JSONB members in sync for backwards compatibility
    # Copy the list so SQLAlchemy detects the JSONB column change
    existing = list(team.members or [])
    existing_gids = {
        (m["gid"] if isinstance(m, dict) else m) for m in existing
    }
    if user_gid not in existing_gids:
        existing.append({"gid": user_gid, "resource_type": "user"})
        team.members = existing
    session.flush()
    return team


def remove_user_from_team(
    session: Session, team_gid: str, user_gid: str
) -> Optional[AsanaTeam]:
    team = get_team(session, team_gid)
    if team is None:
        return None
    user = session.get(AsanaUser, user_gid)
    # Update association table
    if user and user in team.users:
        team.users.remove(user)
    # Keep JSONB members in sync
    existing = team.members or []
    team.members = [
        m for m in existing
        if (m["gid"] if isinstance(m, dict) else m) != user_gid
    ]
    session.flush()
    return team


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

_USER_WRITABLE_FIELDS = ["name"]


def _apply_user_data(session: Session, user: AsanaUser, data: dict) -> None:
    """Apply writable fields from a data dict to a user."""
    for field in _USER_WRITABLE_FIELDS:
        if field in data:
            setattr(user, field, data[field])

    # custom_fields arrives as a dict of {gid: value} on update;
    # store it as JSONB directly
    if "custom_fields" in data:
        user.custom_fields = data["custom_fields"]

    # workspaces: sync to both JSONB and association table
    if "workspaces" in data:
        raw_workspaces = data["workspaces"]
        if isinstance(raw_workspaces, list):
            user.workspaces = [
                w if isinstance(w, dict) else {"gid": w, "resource_type": "workspace"}
                for w in raw_workspaces
            ]
            # Sync association table
            user.workspace_refs.clear()
            for workspace in raw_workspaces:
                workspace_gid = workspace["gid"] if isinstance(workspace, dict) else workspace
                if workspace_gid:
                    _ensure_workspace_stub(session, workspace_gid)
                    workspace_obj = session.get(AsanaWorkspace, workspace_gid)
                    if workspace_obj and workspace_obj not in user.workspace_refs:
                        user.workspace_refs.append(workspace_obj)


def get_user(session: Session, user_gid: str) -> Optional[AsanaUser]:
    return session.execute(
        select(AsanaUser)
        .options(
            selectinload(AsanaUser.workspace_refs),
            selectinload(AsanaUser.teams),
        )
        .where(
            AsanaUser.gid == user_gid,
            AsanaUser.is_deleted.is_(False),
        )
    ).scalars().first()


def update_user(session: Session, user_gid: str, data: dict) -> Optional[AsanaUser]:
    user = get_user(session, user_gid)
    if user is None:
        return None
    _apply_user_data(session, user, data)
    session.flush()
    return user


def list_users(
    session: Session,
    *,
    workspace: Optional[str] = None,
    team: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaUser], Optional[str]]:
    """Return a page of users and the next cursor (or None).

    When workspace is provided, filter via the user↔workspace association
    table. When team is provided, filter via the user↔team association table.
    """
    query = select(AsanaUser).where(AsanaUser.is_deleted.is_(False))
    if workspace is not None:
        query = query.join(AsanaUser.workspace_refs).where(
            AsanaWorkspace.gid == workspace
        )
    if team is not None:
        query = query.join(AsanaUser.teams).where(
            AsanaTeam.gid == team
        )
    if cursor is not None:
        query = query.where(AsanaUser.gid > cursor)
    query = query.order_by(AsanaUser.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def add_user_to_workspace(
    session: Session, workspace_gid: str, user_gid: str
) -> Optional[AsanaUser]:
    """Add a user to a workspace via the association table and JSONB."""
    _ensure_workspace_stub(session, workspace_gid)
    _ensure_user_stub(session, user_gid)
    user = session.get(AsanaUser, user_gid)
    workspace = session.get(AsanaWorkspace, workspace_gid)
    if user is None:
        return None
    # Update association table
    if workspace not in user.workspace_refs:
        user.workspace_refs.append(workspace)
    # Keep JSONB in sync
    existing = user.workspaces or []
    existing_gids = {
        (w["gid"] if isinstance(w, dict) else w) for w in existing
    }
    if workspace_gid not in existing_gids:
        existing.append({"gid": workspace_gid, "resource_type": "workspace", "name": workspace.name})
        user.workspaces = existing
    session.flush()
    return user


def remove_user_from_workspace(
    session: Session, workspace_gid: str, user_gid: str
) -> Optional[AsanaUser]:
    """Remove a user from a workspace via the association table and JSONB."""
    user = session.get(AsanaUser, user_gid)
    workspace = session.get(AsanaWorkspace, workspace_gid)
    if user is None:
        return None
    # Update association table
    if workspace and workspace in user.workspace_refs:
        user.workspace_refs.remove(workspace)
    # Keep JSONB in sync
    existing = user.workspaces or []
    user.workspaces = [
        w for w in existing
        if (w["gid"] if isinstance(w, dict) else w) != workspace_gid
    ]
    session.flush()
    return user


# ---------------------------------------------------------------------------
# Workspaces
# ---------------------------------------------------------------------------

_WORKSPACE_WRITABLE_FIELDS = ["name", "email_domains", "is_organization"]


def _apply_workspace_data(session: Session, workspace: AsanaWorkspace, data: dict) -> None:
    """Apply writable fields from a data dict to a workspace."""
    for field in _WORKSPACE_WRITABLE_FIELDS:
        if field in data:
            setattr(workspace, field, data[field])


def get_workspace(session: Session, workspace_gid: str) -> Optional[AsanaWorkspace]:
    return session.execute(
        select(AsanaWorkspace).where(
            AsanaWorkspace.gid == workspace_gid,
            AsanaWorkspace.is_deleted.is_(False),
        )
    ).scalars().first()


def update_workspace(session: Session, workspace_gid: str, data: dict) -> Optional[AsanaWorkspace]:
    workspace = get_workspace(session, workspace_gid)
    if workspace is None:
        return None
    _apply_workspace_data(session, workspace, data)
    session.flush()
    return workspace


def list_workspaces(
    session: Session,
    *,
    cursor: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[AsanaWorkspace], Optional[str]]:
    query = select(AsanaWorkspace).where(AsanaWorkspace.is_deleted.is_(False))
    if cursor is not None:
        query = query.where(AsanaWorkspace.gid > cursor)
    query = query.order_by(AsanaWorkspace.gid).limit(limit + 1)
    rows = list(session.execute(query).scalars().all())
    if len(rows) > limit:
        next_cursor = rows[limit - 1].gid
        rows = rows[:limit]
    else:
        next_cursor = None
    return rows, next_cursor


def _get_env_schema(session: Session) -> str:
    """Extract the target schema from the session's schema_translate_map."""
    bind = session.get_bind()
    translate_map = bind._execution_options.get("schema_translate_map", {})
    return translate_map.get(None, "public")


def _ensure_time_tracking_column(session: Session) -> None:
    """Add time_tracking_entries JSONB column if it doesn't exist yet."""
    from sqlalchemy import text
    schema = _get_env_schema(session)
    session.execute(text(
        f'ALTER TABLE "{schema}".asana_tasks '
        f"ADD COLUMN IF NOT EXISTS time_tracking_entries JSONB"
    ))
    session.flush()


def _get_time_tracking_raw(session: Session, task_gid: str) -> Optional[list]:
    """Read time_tracking_entries via raw SQL to bypass ORM column mapping."""
    from sqlalchemy import text
    schema = _get_env_schema(session)
    _ensure_time_tracking_column(session)
    row = session.execute(
        text(f'SELECT time_tracking_entries FROM "{schema}".asana_tasks WHERE gid = :gid AND NOT is_deleted'),
        {"gid": task_gid},
    ).first()
    if row is None:
        return None
    return row[0] or []


def _set_time_tracking_raw(session: Session, task_gid: str, entries: list) -> None:
    """Write time_tracking_entries via raw SQL to bypass ORM column mapping."""
    import json
    from sqlalchemy import text
    schema = _get_env_schema(session)
    session.execute(
        text(f'UPDATE "{schema}".asana_tasks SET time_tracking_entries = :entries WHERE gid = :gid'),
        {"gid": task_gid, "entries": json.dumps(entries)},
    )
    session.flush()


def create_time_tracking_entry(
    session: Session, task_gid: str, data: dict
) -> Optional[dict]:
    """Create a time tracking entry on a task, persisted in JSONB list."""
    task = get_task(session, task_gid)
    if task is None:
        return None
    entry_gid = generate_id("time_tracking_entry")
    entry = {
        "gid": entry_gid,
        "resource_type": "time_tracking_entry",
        "duration_minutes": data.get("duration_minutes", 0),
        "entered_on": data.get("entered_on", now_iso()[:10]),
        "created_at": now_iso(),
        "task": {"gid": task.gid, "resource_type": "task", "name": task.name},
    }
    if "description" in data:
        entry["description"] = data["description"]
    if "billable_status" in data:
        entry["billable_status"] = data["billable_status"]
    if "categories" in data:
        entry["categories"] = data["categories"]
    # Persist the entry in the JSONB list via raw SQL
    existing_entries = _get_time_tracking_raw(session, task_gid) or []
    existing_entries.append(entry)
    _set_time_tracking_raw(session, task_gid, existing_entries)
    # Update actual_time_minutes on the task
    task.actual_time_minutes = (task.actual_time_minutes or 0) + entry["duration_minutes"]
    task.modified_at = now_iso()
    session.flush()
    return entry


def get_time_tracking_entries(session: Session, task_gid: str) -> Optional[list]:
    """Return persisted time tracking entries for a task."""
    task = get_task(session, task_gid)
    if task is None:
        return None
    return _get_time_tracking_raw(session, task_gid)
