"""Writer serialization tests.

The classifier has its own tests; this file pins down the on-disk
artifact shape so downstream steps can rely on it. Only the surface
that downstream code will consume is asserted — deep equality would
lock us into incidental ordering choices.
"""

from __future__ import annotations

import json
from pathlib import Path

from fk_pipeline.bucketing import build_map
from fk_pipeline.writer import ARTIFACT_FILENAME, ArtifactMeta, write_artifact

from .conftest import make_alias_map, make_op, make_spec


def _run(tmp_path: Path, naming, spec, resources):
    alias_map = make_alias_map({r: [] for r in resources})
    rem = build_map(spec, alias_map, naming)
    out_path = tmp_path / ARTIFACT_FILENAME
    meta = ArtifactMeta(
        app_slug="test",
        source_spec="/nowhere",
        model="claude-haiku-4-5",
        prompt_version="v1",
        user_resource_count=len(resources),
        endpoint_count=len(rem.endpoints),
        edge_count=len(rem.edges),
        unbucketed_count=len(rem.unbucketed_endpoints),
        vocabulary_cache_hit=False,
    )
    write_artifact(rem, out_path, meta, resource_order=resources)
    return json.loads(out_path.read_text())


def test_artifact_top_level_keys(tmp_path: Path, default_naming):
    spec = make_spec(
        {
            "/projects": {"get": make_op(operation_id="list")},
            "/projects/{id}": {"get": make_op(path_params=["id"])},
        }
    )
    data = _run(tmp_path, default_naming, spec, ["projects"])
    assert set(data.keys()) == {
        "_meta", "resource_aliases", "resources", "endpoints", "unbucketed_endpoints",
    }


def test_artifact_meta_populated(tmp_path: Path, default_naming):
    spec = make_spec({"/projects": {"get": make_op()}})
    data = _run(tmp_path, default_naming, spec, ["projects"])
    meta = data["_meta"]
    assert meta["app_slug"] == "test"
    assert meta["user_resource_count"] == 1
    assert meta["endpoint_count"] == 1
    assert meta["edge_count"] == 1
    assert meta["prompt_version"] == "v1"


def test_artifact_resource_order_preserved(tmp_path: Path, default_naming):
    spec = make_spec(
        {
            "/projects": {"get": make_op()},
            "/tasks": {"get": make_op()},
        }
    )
    data = _run(tmp_path, default_naming, spec, ["tasks", "projects"])
    assert list(data["resources"].keys())[:2] == ["tasks", "projects"]


def test_artifact_endpoint_has_raw_operation(tmp_path: Path, default_naming):
    """raw_operation is preserved verbatim so downstream can walk schemas."""
    spec = make_spec(
        {
            "/projects/{id}": {
                "get": make_op(
                    operation_id="get_project",
                    path_params=["id"],
                )
            }
        }
    )
    data = _run(tmp_path, default_naming, spec, ["projects"])
    endpoint = data["endpoints"]["GET /projects/{id}"]
    assert endpoint["operation_id"] == "get_project"
    assert endpoint["raw_operation"]["operationId"] == "get_project"
    assert endpoint["resource_edges"]


def test_artifact_unbucketed_endpoints_preserved(tmp_path: Path, default_naming):
    spec = make_spec(
        {"/health": {"get": make_op(operation_id="health_check")}}
    )
    data = _run(tmp_path, default_naming, spec, ["projects"])
    assert len(data["unbucketed_endpoints"]) == 1
    unb = data["unbucketed_endpoints"][0]
    assert unb["path"] == "/health"
    assert unb["method"] == "GET"
    assert unb["raw_operation"]["operationId"] == "health_check"


def test_resource_edges_sorted_by_strength(tmp_path: Path, default_naming):
    """Within a resource, stronger edges come first in the resources view."""
    spec = make_spec(
        {
            # OWNER_ITEM
            "/projects/{id}": {"get": make_op(path_params=["id"])},
            # OWNER_COLLECTION
            "/projects": {"get": make_op()},
        }
    )
    data = _run(tmp_path, default_naming, spec, ["projects"])
    roles = [e["role"] for e in data["resources"]["projects"]]
    # OWNER_ITEM is strongest (index 0), OWNER_COLLECTION is second.
    assert roles[0] == "OWNER_ITEM"
    assert roles[1] == "OWNER_COLLECTION"
