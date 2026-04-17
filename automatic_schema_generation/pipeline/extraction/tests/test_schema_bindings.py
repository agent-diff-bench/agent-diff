"""Tests for schema bindings (Group D)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pipeline.config import PipelineConfig, load_config
from pipeline.extraction.schema_bindings import build_schema_bindings


def _config(tmp_path: Path, resources: dict[str, Any]) -> PipelineConfig:
    spec_path = tmp_path / "spec.json"
    spec_path.write_text('{"paths": {}, "components": {"schemas": {}}}')
    cfg_path = tmp_path / "app.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "app_slug": "test",
        "app_name": "Test",
        "openapi_path": "spec.json",
        "target_dir": "out",
        "resources": resources,
    }))
    return load_config(cfg_path)


def test_empty_components_returns_empty(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    assert build_schema_bindings({}, config) == {}
    assert build_schema_bindings({"components": {}}, config) == {}


def test_direct_name_hit_binds(tmp_path: Path) -> None:
    """``SimpleUser`` normalizes to ``simple_user`` → ``users`` alias."""
    config = _config(
        tmp_path,
        {"users": {"aliases": ["user", "simple_user"]}},
    )
    spec = {"components": {"schemas": {"SimpleUser": {"type": "object"}}}}
    assert build_schema_bindings(spec, config) == {"SimpleUser": "users"}


def test_non_matching_schema_name_does_not_bind(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {"components": {"schemas": {"Widget": {"type": "object"}}}}
    assert build_schema_bindings(spec, config) == {}


def test_all_of_inherits_binding_from_ref_branch(tmp_path: Path) -> None:
    """``Issue`` composes over ``BaseIssue`` which itself hits ``issues``."""
    config = _config(tmp_path, {"issues": {"aliases": ["issue", "base_issue"]}})
    spec = {
        "components": {
            "schemas": {
                "BaseIssue": {"type": "object"},
                "Issue": {
                    "allOf": [
                        {"$ref": "#/components/schemas/BaseIssue"},
                        {"type": "object", "properties": {"extra": {}}},
                    ],
                },
            }
        }
    }
    bindings = build_schema_bindings(spec, config)
    assert bindings == {"BaseIssue": "issues", "Issue": "issues"}


def test_all_of_conflicting_branches_leave_unbound(tmp_path: Path) -> None:
    """``allOf`` with two different bound branches → outer stays unbound."""
    config = _config(
        tmp_path,
        {
            "users": {"aliases": ["user"]},
            "repos": {"aliases": ["repo"]},
        },
    )
    spec = {
        "components": {
            "schemas": {
                "User": {"type": "object"},
                "Repo": {"type": "object"},
                "Weird": {
                    "allOf": [
                        {"$ref": "#/components/schemas/User"},
                        {"$ref": "#/components/schemas/Repo"},
                    ],
                },
            }
        }
    }
    bindings = build_schema_bindings(spec, config)
    assert bindings == {"User": "users", "Repo": "repos"}
    assert "Weird" not in bindings


def test_one_of_all_branches_agree_binds(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users": {"aliases": ["user", "simple_user"]}})
    spec = {
        "components": {
            "schemas": {
                "User": {"type": "object"},
                "SimpleUser": {"type": "object"},
                "AnyUser": {
                    "oneOf": [
                        {"$ref": "#/components/schemas/User"},
                        {"$ref": "#/components/schemas/SimpleUser"},
                    ],
                },
            }
        }
    }
    bindings = build_schema_bindings(spec, config)
    assert bindings["AnyUser"] == "users"


def test_one_of_with_unbound_branch_does_not_bind(tmp_path: Path) -> None:
    """If any ``oneOf`` branch is unbound, the outer stays unbound."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "components": {
            "schemas": {
                "User": {"type": "object"},
                "Anonymous": {"type": "object"},
                "Maybe": {
                    "oneOf": [
                        {"$ref": "#/components/schemas/User"},
                        {"$ref": "#/components/schemas/Anonymous"},
                    ],
                },
            }
        }
    }
    bindings = build_schema_bindings(spec, config)
    assert "Maybe" not in bindings


def test_transitive_chain_binds_via_fixed_point(tmp_path: Path) -> None:
    """``A`` → ``B`` → ``User`` should all end up bound after propagation."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "components": {
            "schemas": {
                "User": {"type": "object"},
                "B": {"allOf": [{"$ref": "#/components/schemas/User"}]},
                "A": {"allOf": [{"$ref": "#/components/schemas/B"}]},
            }
        }
    }
    bindings = build_schema_bindings(spec, config)
    assert bindings == {"User": "users", "B": "users", "A": "users"}


def test_bare_ref_pass_through_chain_binds(tmp_path: Path) -> None:
    """A chain of pure top-level ``$ref`` aliases propagates through every hop."""
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "components": {
            "schemas": {
                "User": {"type": "object"},
                "UserRef": {"$ref": "#/components/schemas/User"},
                "UserAlias": {"$ref": "#/components/schemas/UserRef"},
            }
        }
    }
    bindings = build_schema_bindings(spec, config)
    assert bindings == {
        "User": "users",
        "UserRef": "users",
        "UserAlias": "users",
    }


def test_property_level_ref_does_not_bind_container(tmp_path: Path) -> None:
    """A schema with a ``$ref`` inside a property is not itself that resource.

    ``Comment`` has an ``author`` property that refs ``User`` — that's a
    reference FROM ``Comment`` TO ``User`` (Group C), not schema
    identity. The binder must not confuse them.
    """
    config = _config(tmp_path, {"users": {"aliases": ["user"]}})
    spec = {
        "components": {
            "schemas": {
                "User": {"type": "object"},
                "Comment": {
                    "type": "object",
                    "properties": {
                        "author": {"$ref": "#/components/schemas/User"},
                    },
                },
            }
        }
    }
    bindings = build_schema_bindings(spec, config)
    assert bindings == {"User": "users"}
    assert "Comment" not in bindings
