"""
Performance tests for Box API - mimicking real box_bench operations.

These tests create an isolated Box environment (box_default template),
then run the same API call patterns that appear in the box_bench test suite
to measure response times and identify bottlenecks.

Usage:
    # Run from backend/ directory (requires DATABASE_URL in .env or env):



    # Run with timing threshold (skip assertions under N ms):
    PERF_THRESHOLD_MS=100 pytest tests/performance/test_box_bench_perf.py -v -s

Environment setup:
    1. The box_default template must be seeded in the database.
    2. Tests use core_isolation_engine.create_environment(template_schema="box_default")
       to create an isolated copy of the template.
    3. The impersonate_user_id "27512847635" matches the bench's default user (Admin User).
    4. All environments are auto-cleaned after the test session.
"""

import asyncio
import logging
import os
import time

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from starlette.applications import Starlette

from src.services.box.api.routes import routes as box_routes

logger = logging.getLogger(__name__)

# Default user from box_bench.json
BOX_IMPERSONATE_USER_ID = "27512847635"

# Threshold in ms - tests log warnings above this
PERF_THRESHOLD_MS = int(os.environ.get("PERF_THRESHOLD_MS", "500"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _timed(label: str):
    """Context manager that logs elapsed time."""

    class Timer:
        def __init__(self):
            self.elapsed_ms = 0.0

        def __enter__(self):
            self._start = time.perf_counter()
            return self

        def __exit__(self, *exc):
            self.elapsed_ms = (time.perf_counter() - self._start) * 1000
            marker = "SLOW" if self.elapsed_ms > PERF_THRESHOLD_MS else "OK"
            logger.info(f"[PERF {marker}] {label}: {self.elapsed_ms:.0f}ms")

    return Timer()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def box_client(
    test_user_id,
    core_isolation_engine,
    session_manager,
    environment_handler,
):
    """
    Create an isolated box_default environment and return an AsyncClient
    wired to the Box API routes, just like the real bench does.

    The flow mirrors environment.py setup_state:
      1. core_isolation_engine.create_environment(template_schema="box_default", ...)
      2. Wire session + impersonate_user_id into request.state
      3. Mount box routes
    """
    env_result = core_isolation_engine.create_environment(
        template_schema="box_default",
        ttl_seconds=3600,
        created_by=test_user_id,
        impersonate_user_id=BOX_IMPERSONATE_USER_ID,
    )

    async def add_db_session(request, call_next):
        with session_manager.with_session_for_environment(
            env_result.environment_id
        ) as session:
            request.state.db_session = session
            request.state.environment_id = env_result.environment_id
            request.state.impersonate_user_id = BOX_IMPERSONATE_USER_ID
            request.state.impersonate_email = None
            response = await call_next(request)
            return response

    app = Starlette(routes=box_routes)
    app.middleware("http")(add_db_session)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    environment_handler.drop_schema(env_result.schema_name)


# ---------------------------------------------------------------------------
# Test: GET /users/me (bench test_1)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_current_user(box_client: AsyncClient):
    """GET /users/me — identify the logged-in user."""
    with _timed("GET /users/me") as t:
        resp = await box_client.get("/users/me")

    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "user"
    assert data["id"] == BOX_IMPERSONATE_USER_ID
    assert t.elapsed_ms < 5000, f"GET /users/me took {t.elapsed_ms:.0f}ms (>5s)"


# ---------------------------------------------------------------------------
# Test: GET /search (bench test_2, test_3, test_4, test_5, test_6, ...)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_search_by_name(box_client: AsyncClient):
    """GET /search?query=investments — find folder by name (very common operation)."""
    with _timed("GET /search?query=investments") as t:
        resp = await box_client.get("/search", params={"query": "investments"})

    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "search_results_items"
    assert data["total_count"] >= 1
    assert t.elapsed_ms < 5000, f"search 'investments' took {t.elapsed_ms:.0f}ms (>5s)"


@pytest.mark.asyncio
async def test_search_fomc(box_client: AsyncClient):
    """GET /search?query=fomc — search for FOMC files (bench test_3)."""
    with _timed("GET /search?query=fomc") as t:
        resp = await box_client.get("/search", params={"query": "fomc"})

    assert resp.status_code == 200
    data = resp.json()
    assert data["total_count"] >= 1
    assert t.elapsed_ms < 5000, f"search 'fomc' took {t.elapsed_ms:.0f}ms (>5s)"


@pytest.mark.asyncio
async def test_search_broad_query(box_client: AsyncClient):
    """GET /search?query=a — broad search that returns many results (stress test)."""
    with _timed("GET /search?query=a (broad)") as t:
        resp = await box_client.get("/search", params={"query": "a", "limit": 200})

    assert resp.status_code == 200
    data = resp.json()
    logger.info(
        f"  Broad search returned {data['total_count']} total, "
        f"{len(data['entries'])} entries"
    )
    assert t.elapsed_ms < 10000, f"broad search took {t.elapsed_ms:.0f}ms (>10s)"


@pytest.mark.asyncio
async def test_search_file_type_filter(box_client: AsyncClient):
    """GET /search?query=report&type=file — search with type filter."""
    with _timed("GET /search?query=report&type=file") as t:
        resp = await box_client.get(
            "/search", params={"query": "report", "type": "file"}
        )

    assert resp.status_code == 200
    data = resp.json()
    # All results should be files
    for entry in data["entries"]:
        assert entry["type"] == "file"
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_search_folder_type_filter(box_client: AsyncClient):
    """GET /search?query=macro&type=folder — folder search (bench test_5)."""
    with _timed("GET /search?query=macro&type=folder") as t:
        resp = await box_client.get(
            "/search", params={"query": "macro", "type": "folder"}
        )

    assert resp.status_code == 200
    data = resp.json()
    for entry in data["entries"]:
        assert entry["type"] == "folder"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: GET /folders/{id} (bench test_9, test_12)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_root_folder(box_client: AsyncClient):
    """GET /folders/0 — get root folder (always ID "0")."""
    with _timed("GET /folders/0") as t:
        resp = await box_client.get("/folders/0")

    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "folder"
    assert data["id"] == "0"
    assert "item_collection" in data
    assert t.elapsed_ms < 5000, f"GET /folders/0 took {t.elapsed_ms:.0f}ms (>5s)"


@pytest.mark.asyncio
async def test_get_investments_folder(box_client: AsyncClient):
    """GET /folders/5610825569 — get the investments folder (bench test_9)."""
    with _timed("GET /folders/5610825569") as t:
        resp = await box_client.get("/folders/5610825569")

    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "folder"
    assert data["name"] == "investments"
    assert "path_collection" in data
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: GET /folders/{id}/items (bench test_12)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_root_folder_items(box_client: AsyncClient):
    """GET /folders/0/items — list items in root folder."""
    with _timed("GET /folders/0/items") as t:
        resp = await box_client.get("/folders/0/items")

    assert resp.status_code == 200
    data = resp.json()
    assert "entries" in data
    assert "total_count" in data
    logger.info(f"  Root folder has {data['total_count']} items")
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_list_investments_folder_items(box_client: AsyncClient):
    """GET /folders/5610825569/items — list items in investments folder (bench test_12)."""
    with _timed("GET /folders/5610825569/items") as t:
        resp = await box_client.get("/folders/5610825569/items")

    assert resp.status_code == 200
    data = resp.json()
    assert "entries" in data
    logger.info(f"  investments folder has {data['total_count']} items")
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: GET /files/{id} (bench test_4 needs file lookup before comment)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_file_by_id(box_client: AsyncClient):
    """GET /files/{file_id} — get a specific file's details."""
    # First find a file via search
    search_resp = await box_client.get(
        "/search", params={"query": "fomc", "type": "file"}
    )
    assert search_resp.status_code == 200
    entries = search_resp.json()["entries"]
    if not entries:
        pytest.skip("No fomc files found in seed data")

    file_id = entries[0]["id"]

    with _timed(f"GET /files/{file_id}") as t:
        resp = await box_client.get(f"/files/{file_id}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "file"
    assert data["id"] == file_id
    assert "path_collection" in data
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: POST /comments (bench test_3, test_4, test_10)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_add_comment_to_file(box_client: AsyncClient):
    """POST /comments — add a comment to a file (bench test_3, test_4)."""
    # Find a file
    search_resp = await box_client.get(
        "/search", params={"query": "fomc", "type": "file"}
    )
    entries = search_resp.json().get("entries", [])
    if not entries:
        pytest.skip("No fomc files found")

    file_id = entries[0]["id"]

    with _timed(f"POST /comments on file {file_id}") as t:
        resp = await box_client.post(
            "/comments",
            json={
                "item": {"type": "file", "id": file_id},
                "message": "Relevant",
            },
        )

    assert resp.status_code == 201
    data = resp.json()
    assert data["type"] == "comment"
    assert data["message"] == "Relevant"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: POST /folders (bench test_1, test_2, test_11)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_folder_in_root(box_client: AsyncClient):
    """POST /folders — create folder in root (bench test_1)."""
    with _timed("POST /folders (root)") as t:
        resp = await box_client.post(
            "/folders",
            json={"name": "Admin User", "parent": {"id": "0"}},
        )

    assert resp.status_code == 201
    data = resp.json()
    assert data["type"] == "folder"
    assert data["name"] == "Admin User"
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_create_folder_in_subfolder(box_client: AsyncClient):
    """POST /folders — create folder inside investments (bench test_2)."""
    with _timed("POST /folders (investments)") as t:
        resp = await box_client.post(
            "/folders",
            json={"name": "Analysis_2026", "parent": {"id": "5610825569"}},
        )

    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Analysis_2026"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: PUT /folders/{id} (bench test_5, test_8, test_9)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_rename_folder(box_client: AsyncClient):
    """PUT /folders/{id} — rename folder (bench test_5)."""
    # macroeconomics folder ID from bench
    folder_id = "1973339758"

    with _timed(f"PUT /folders/{folder_id}") as t:
        resp = await box_client.put(
            f"/folders/{folder_id}",
            json={"name": "Global Economics"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Global Economics"
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_update_folder_tags(box_client: AsyncClient):
    """PUT /folders/{id} — update tags (bench test_8)."""
    folder_id = "5610825569"  # investments

    with _timed(f"PUT /folders/{folder_id} (tags)") as t:
        resp = await box_client.put(
            f"/folders/{folder_id}",
            json={"tags": ["finance", "investments", "quarterly"]},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert "finance" in data.get("tags", [])
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: PUT /files/{id} (bench test_6 — move file)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_move_file(box_client: AsyncClient):
    """PUT /files/{id} — move file to different folder (bench test_6)."""
    file_id = "1421498350"  # transport-april-2025-csv.csv
    target_folder_id = "5610825569"  # investments

    with _timed(f"PUT /files/{file_id} (move)") as t:
        resp = await box_client.put(
            f"/files/{file_id}",
            json={"parent": {"id": target_folder_id}},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["parent"]["id"] == target_folder_id
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: GET /files/{id}/comments (needed for checking existing comments)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_file_comments(box_client: AsyncClient):
    """GET /files/{id}/comments — list comments on a file."""
    # Find a file
    search_resp = await box_client.get(
        "/search", params={"query": "fomc", "type": "file"}
    )
    entries = search_resp.json().get("entries", [])
    if not entries:
        pytest.skip("No fomc files found")

    file_id = entries[0]["id"]

    with _timed(f"GET /files/{file_id}/comments") as t:
        resp = await box_client.get(f"/files/{file_id}/comments")

    assert resp.status_code == 200
    data = resp.json()
    assert "entries" in data
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: POST /tasks (bench test_10)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_task(box_client: AsyncClient):
    """POST /tasks — create task on a file (bench test_10)."""
    # Find a file
    search_resp = await box_client.get(
        "/search", params={"query": "fomc", "type": "file"}
    )
    entries = search_resp.json().get("entries", [])
    if not entries:
        pytest.skip("No fomc files found")

    file_id = entries[0]["id"]

    with _timed(f"POST /tasks on file {file_id}") as t:
        resp = await box_client.post(
            "/tasks",
            json={
                "item": {"type": "file", "id": file_id},
                "message": "Review content",
                "action": "review",
            },
        )

    assert resp.status_code == 201
    data = resp.json()
    assert data["type"] == "task"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: Hubs (bench test_7, test_13)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_hubs(box_client: AsyncClient):
    """GET /hubs — list all hubs (bench test_13)."""
    with _timed("GET /hubs") as t:
        resp = await box_client.get("/hubs", headers={"box-version": "2025.0"})

    assert resp.status_code == 200
    data = resp.json()
    assert "entries" in data
    assert t.elapsed_ms < 5000


@pytest.mark.asyncio
async def test_create_hub(box_client: AsyncClient):
    """POST /hubs — create a hub (bench test_7)."""
    with _timed("POST /hubs") as t:
        resp = await box_client.post(
            "/hubs",
            json={"title": "Research Center", "description": "Research hub"},
            headers={"box-version": "2025.0"},
        )

    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Research Center"
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: Collections (bench test_15+)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_collections(box_client: AsyncClient):
    """GET /collections — list available collections."""
    with _timed("GET /collections") as t:
        resp = await box_client.get("/collections")

    assert resp.status_code == 200
    data = resp.json()
    assert "entries" in data
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Test: Multi-step flows mimicking real bench scenarios
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_bench_flow_search_then_comment(box_client: AsyncClient):
    """
    Mimics bench test_3: Search for 'fomc', then add comment to first result.
    Measures the combined latency of a typical 2-step agent operation.
    """
    with _timed("FLOW: search + comment") as t_total:
        # Step 1: Search
        with _timed("  step1: search fomc") as t1:
            search_resp = await box_client.get(
                "/search", params={"query": "fomc", "type": "file"}
            )
        assert search_resp.status_code == 200
        entries = search_resp.json()["entries"]
        assert len(entries) >= 1

        file_id = entries[0]["id"]

        # Step 2: Comment
        with _timed(f"  step2: comment on {file_id}") as t2:
            comment_resp = await box_client.post(
                "/comments",
                json={"item": {"type": "file", "id": file_id}, "message": "Relevant"},
            )
        assert comment_resp.status_code == 201

    logger.info(
        f"  FLOW total={t_total.elapsed_ms:.0f}ms "
        f"(search={t1.elapsed_ms:.0f}ms + comment={t2.elapsed_ms:.0f}ms)"
    )
    assert t_total.elapsed_ms < 10000


@pytest.mark.asyncio
async def test_bench_flow_search_rename_folder(box_client: AsyncClient):
    """
    Mimics bench test_5: Search for folder, then rename it.
    """
    with _timed("FLOW: search + rename folder") as t_total:
        # Step 1: Search for macroeconomics folder
        with _timed("  step1: search macroeconomics") as t1:
            search_resp = await box_client.get(
                "/search", params={"query": "macroeconomics", "type": "folder"}
            )
        assert search_resp.status_code == 200
        entries = search_resp.json()["entries"]
        assert len(entries) >= 1

        folder_id = entries[0]["id"]

        # Step 2: Rename
        with _timed(f"  step2: rename folder {folder_id}") as t2:
            rename_resp = await box_client.put(
                f"/folders/{folder_id}",
                json={"name": "Global Economics"},
            )
        assert rename_resp.status_code == 200

    logger.info(
        f"  FLOW total={t_total.elapsed_ms:.0f}ms "
        f"(search={t1.elapsed_ms:.0f}ms + rename={t2.elapsed_ms:.0f}ms)"
    )
    assert t_total.elapsed_ms < 10000


@pytest.mark.asyncio
async def test_bench_flow_create_nested_folders_and_move(box_client: AsyncClient):
    """
    Mimics bench test_11: Create Project_Beta in root, create Docs inside it,
    then move a file into Docs. Measures a 4-step agent operation.
    """
    with _timed("FLOW: create nested + search + move") as t_total:
        # Step 1: Create Project_Beta in root
        with _timed("  step1: create Project_Beta"):
            resp1 = await box_client.post(
                "/folders",
                json={"name": "Project_Beta", "parent": {"id": "0"}},
            )
        assert resp1.status_code == 201
        project_beta_id = resp1.json()["id"]

        # Step 2: Create Docs inside Project_Beta
        with _timed("  step2: create Docs"):
            resp2 = await box_client.post(
                "/folders",
                json={"name": "Docs", "parent": {"id": project_beta_id}},
            )
        assert resp2.status_code == 201
        docs_id = resp2.json()["id"]

        # Step 3: Search for the file
        with _timed("  step3: search for file"):
            search_resp = await box_client.get(
                "/search", params={"query": "interviewing tips", "type": "file"}
            )
        assert search_resp.status_code == 200
        entries = search_resp.json()["entries"]
        assert len(entries) >= 1
        file_id = entries[0]["id"]

        # Step 4: Move file
        with _timed(f"  step4: move file {file_id} to Docs"):
            move_resp = await box_client.put(
                f"/files/{file_id}",
                json={"parent": {"id": docs_id}},
            )
        assert move_resp.status_code == 200

    logger.info(f"  FLOW total={t_total.elapsed_ms:.0f}ms")
    assert t_total.elapsed_ms < 15000


@pytest.mark.asyncio
async def test_bench_flow_count_items_and_update_description(box_client: AsyncClient):
    """
    Mimics bench test_12: Count files in investments, set description to the count.
    """
    with _timed("FLOW: search + list items + update") as t_total:
        # Step 1: Search for investments folder
        with _timed("  step1: search investments"):
            search_resp = await box_client.get(
                "/search", params={"query": "investments", "type": "folder"}
            )
        assert search_resp.status_code == 200
        entries = search_resp.json()["entries"]
        assert len(entries) >= 1
        folder_id = entries[0]["id"]

        # Step 2: List folder items to count
        with _timed(f"  step2: list items in {folder_id}"):
            items_resp = await box_client.get(f"/folders/{folder_id}/items")
        assert items_resp.status_code == 200
        item_count = items_resp.json()["total_count"]

        # Step 3: Update folder description
        with _timed("  step3: update description"):
            update_resp = await box_client.put(
                f"/folders/{folder_id}",
                json={"description": str(item_count)},
            )
        assert update_resp.status_code == 200

    logger.info(f"  FLOW total={t_total.elapsed_ms:.0f}ms, items counted={item_count}")
    assert t_total.elapsed_ms < 10000


# ---------------------------------------------------------------------------
# Test: Repeated searches (simulates an agent retrying/iterating)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_repeated_searches(box_client: AsyncClient):
    """
    Run 10 sequential searches to measure consistency and detect degradation.
    """
    queries = [
        "investments",
        "fomc",
        "report",
        "macro",
        "argentina",
        "transport",
        "earnings",
        "interview",
        "research",
        "csv",
    ]

    times = []
    for q in queries:
        with _timed(f"  search '{q}'") as t:
            resp = await box_client.get("/search", params={"query": q})
        assert resp.status_code == 200
        times.append(t.elapsed_ms)

    avg_ms = sum(times) / len(times)
    p50 = sorted(times)[len(times) // 2]
    p99 = sorted(times)[int(len(times) * 0.99)]
    max_ms = max(times)

    logger.info(
        f"  10 searches: avg={avg_ms:.0f}ms p50={p50:.0f}ms "
        f"p99={p99:.0f}ms max={max_ms:.0f}ms"
    )
    assert max_ms < 10000, f"Worst search took {max_ms:.0f}ms (>10s)"


# ---------------------------------------------------------------------------
# Test: Folder traversal depth (triggers _get_path_collection N+1)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_deep_folder_path_collection(box_client: AsyncClient):
    """
    Create 5 nested folders, then GET the deepest one.
    This stresses _get_path_collection() which walks parent chain.
    """
    parent_id = "0"
    folder_ids = []

    for i in range(5):
        resp = await box_client.post(
            "/folders",
            json={"name": f"depth_{i}", "parent": {"id": parent_id}},
        )
        assert resp.status_code == 201
        parent_id = resp.json()["id"]
        folder_ids.append(parent_id)

    # Now GET the deepest folder — this triggers path_collection walk
    deepest_id = folder_ids[-1]
    with _timed(f"GET /folders/{deepest_id} (depth=5)") as t:
        resp = await box_client.get(f"/folders/{deepest_id}")

    assert resp.status_code == 200
    data = resp.json()
    path = data.get("path_collection", {})
    logger.info(
        f"  path_collection depth={path.get('total_count', '?')}, "
        f"time={t.elapsed_ms:.0f}ms"
    )
    assert t.elapsed_ms < 5000


# ---------------------------------------------------------------------------
# Tests: Parallel requests (4 concurrent) — simulates real agent bench load
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_parallel_4_searches(box_client: AsyncClient):
    """
    Fire 4 search requests in parallel and measure wall-clock time.
    This mirrors what happens when multiple agent turns hit the Box API
    concurrently during an evaluation run.
    """
    queries = ["investments", "fomc", "report", "macro"]

    async def do_search(q: str) -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await box_client.get("/search", params={"query": q})
        elapsed = (time.perf_counter() - t0) * 1000
        return q, elapsed, resp.status_code

    with _timed("PARALLEL: 4 searches") as wall:
        results = await asyncio.gather(*(do_search(q) for q in queries))

    for q, ms, status in results:
        logger.info(f"  parallel search '{q}': {ms:.0f}ms status={status}")
        assert status == 200

    max_individual = max(ms for _, ms, _ in results)
    logger.info(
        f"  wall_clock={wall.elapsed_ms:.0f}ms  max_individual={max_individual:.0f}ms"
    )
    assert wall.elapsed_ms < 10000, (
        f"4 parallel searches took {wall.elapsed_ms:.0f}ms wall-clock (>10s)"
    )


@pytest.mark.asyncio
async def test_parallel_4_folder_gets(box_client: AsyncClient):
    """
    Fire 4 GET /folders requests in parallel with different folder IDs.
    """
    folder_ids = ["0", "5610825569", "1973339758", "1173971943"]

    async def do_get(fid: str) -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await box_client.get(f"/folders/{fid}")
        elapsed = (time.perf_counter() - t0) * 1000
        return fid, elapsed, resp.status_code

    with _timed("PARALLEL: 4 folder GETs") as wall:
        results = await asyncio.gather(*(do_get(f) for f in folder_ids))

    for fid, ms, status in results:
        logger.info(f"  parallel GET /folders/{fid}: {ms:.0f}ms status={status}")
        assert status == 200

    max_individual = max(ms for _, ms, _ in results)
    logger.info(
        f"  wall_clock={wall.elapsed_ms:.0f}ms  max_individual={max_individual:.0f}ms"
    )
    assert wall.elapsed_ms < 10000, (
        f"4 parallel folder GETs took {wall.elapsed_ms:.0f}ms wall-clock (>10s)"
    )


@pytest.mark.asyncio
async def test_parallel_4_mixed_operations(box_client: AsyncClient):
    """
    Fire 4 different operation types in parallel — search, folder GET,
    list folder items, list hubs — simulating a realistic agent burst.
    """

    async def search() -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await box_client.get("/search", params={"query": "fomc"})
        return "search", (time.perf_counter() - t0) * 1000, resp.status_code

    async def get_folder() -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await box_client.get("/folders/0")
        return "get_folder", (time.perf_counter() - t0) * 1000, resp.status_code

    async def list_items() -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await box_client.get("/folders/0/items")
        return "list_items", (time.perf_counter() - t0) * 1000, resp.status_code

    async def list_hubs() -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await box_client.get("/hubs", headers={"box-version": "2025.0"})
        return "list_hubs", (time.perf_counter() - t0) * 1000, resp.status_code

    with _timed("PARALLEL: 4 mixed ops") as wall:
        results = await asyncio.gather(
            search(), get_folder(), list_items(), list_hubs()
        )

    for op, ms, status in results:
        logger.info(f"  parallel {op}: {ms:.0f}ms status={status}")
        assert status == 200

    max_individual = max(ms for _, ms, _ in results)
    logger.info(
        f"  wall_clock={wall.elapsed_ms:.0f}ms  max_individual={max_individual:.0f}ms"
    )
    assert wall.elapsed_ms < 10000, (
        f"4 parallel mixed ops took {wall.elapsed_ms:.0f}ms wall-clock (>10s)"
    )


@pytest.mark.asyncio
async def test_parallel_4_writes(box_client: AsyncClient):
    """
    Fire 4 write operations in parallel — create folders simultaneously.
    Tests DB write contention under concurrent load.
    """

    async def create_folder(name: str) -> tuple[str, float, int]:
        t0 = time.perf_counter()
        resp = await box_client.post(
            "/folders",
            json={"name": name, "parent": {"id": "0"}},
        )
        return name, (time.perf_counter() - t0) * 1000, resp.status_code

    names = ["Parallel_A", "Parallel_B", "Parallel_C", "Parallel_D"]

    with _timed("PARALLEL: 4 folder creates") as wall:
        results = await asyncio.gather(*(create_folder(n) for n in names))

    for name, ms, status in results:
        logger.info(f"  parallel POST /folders '{name}': {ms:.0f}ms status={status}")
        assert status == 201

    max_individual = max(ms for _, ms, _ in results)
    logger.info(
        f"  wall_clock={wall.elapsed_ms:.0f}ms  max_individual={max_individual:.0f}ms"
    )
    assert wall.elapsed_ms < 10000, (
        f"4 parallel folder creates took {wall.elapsed_ms:.0f}ms wall-clock (>10s)"
    )
