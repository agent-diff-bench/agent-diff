"""Tests for the body-level reference extractor (Group E)."""

from __future__ import annotations

from pipeline.extraction.body_references import BodyReference, find_body_references


def test_empty_operation_returns_nothing() -> None:
    assert find_body_references({}, {}, {}) == []


def test_request_body_direct_ref_emits_hit() -> None:
    operation = {
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/IssueCreate"},
                },
            },
        },
    }
    references = find_body_references(operation, {}, {"IssueCreate": "issues"})
    assert references == [
        BodyReference(
            resource="issues",
            role="request",
            status_code=None,
            media_type="application/json",
            schema_name="IssueCreate",
        ),
    ]


def test_response_body_direct_ref_emits_hit_with_status() -> None:
    operation = {
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Issue"},
                    },
                },
            },
        },
    }
    references = find_body_references(operation, {}, {"Issue": "issues"})
    assert len(references) == 1
    reference = references[0]
    assert reference.role == "response"
    assert reference.status_code == "200"
    assert reference.resource == "issues"
    assert reference.schema_name == "Issue"


def test_response_array_items_walked() -> None:
    """``type: array, items: {$ref: Issue}`` emits one hit via the items walk."""
    operation = {
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Issue"},
                        },
                    },
                },
            },
        },
    }
    references = find_body_references(operation, {}, {"Issue": "issues"})
    assert len(references) == 1
    assert references[0].resource == "issues"
    assert references[0].schema_name == "Issue"


def test_request_body_ref_into_components_is_dereferenced() -> None:
    """``requestBody: {$ref: #/components/requestBodies/Foo}`` resolves to the component."""
    operation = {
        "requestBody": {"$ref": "#/components/requestBodies/IssueCreate"},
    }
    spec = {
        "components": {
            "requestBodies": {
                "IssueCreate": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Issue"},
                        },
                    },
                },
            },
        },
    }
    references = find_body_references(operation, spec, {"Issue": "issues"})
    assert len(references) == 1
    assert references[0].role == "request"
    assert references[0].resource == "issues"


def test_response_ref_into_components_is_dereferenced() -> None:
    """``responses.200: {$ref: #/components/responses/Foo}`` resolves to the component."""
    operation = {
        "responses": {
            "200": {"$ref": "#/components/responses/IssueResponse"},
        },
    }
    spec = {
        "components": {
            "responses": {
                "IssueResponse": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Issue"},
                        },
                    },
                },
            },
        },
    }
    references = find_body_references(operation, spec, {"Issue": "issues"})
    assert len(references) == 1
    assert references[0].role == "response"
    assert references[0].status_code == "200"
    assert references[0].resource == "issues"


def test_response_ref_to_missing_component_is_skipped() -> None:
    """If the ``$ref`` target isn't in ``components.responses``, skip silently."""
    operation = {
        "responses": {
            "200": {"$ref": "#/components/responses/Unknown"},
        },
    }
    spec = {"components": {"responses": {}}}
    assert find_body_references(operation, spec, {"Issue": "issues"}) == []


def test_one_of_emits_every_bound_branch() -> None:
    """Error-union responses emit one hit per branch that binds."""
    operation = {
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "schema": {
                            "oneOf": [
                                {"$ref": "#/components/schemas/Issue"},
                                {"$ref": "#/components/schemas/Error"},
                            ],
                        },
                    },
                },
            },
        },
    }
    # Only Issue binds; Error is unbound.
    references = find_body_references(operation, {}, {"Issue": "issues"})
    assert len(references) == 1
    assert references[0].resource == "issues"


def test_all_of_emits_every_bound_branch() -> None:
    operation = {
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "allOf": [
                            {"$ref": "#/components/schemas/BaseIssue"},
                            {"$ref": "#/components/schemas/IssueUpdate"},
                        ],
                    },
                },
            },
        },
    }
    bindings = {"BaseIssue": "issues", "IssueUpdate": "issues"}
    references = find_body_references(operation, {}, bindings)
    # Same resource, two different schema_names → two entries.
    schema_names = {reference.schema_name for reference in references}
    assert schema_names == {"BaseIssue", "IssueUpdate"}


def test_inline_schema_without_ref_emits_nothing() -> None:
    """An inline object body with no ``$ref`` produces no hits — this is Group C's job."""
    operation = {
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "assignee": {"$ref": "#/components/schemas/User"},
                        },
                    },
                },
            },
        },
    }
    references = find_body_references(operation, {}, {"User": "users"})
    # Property-level $ref is deliberately NOT walked.
    assert references == []


def test_unbound_ref_is_silently_skipped() -> None:
    """A ``$ref`` to a schema not in the bindings table produces no hit (no FP)."""
    operation = {
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Unknown"},
                    },
                },
            },
        },
    }
    assert find_body_references(operation, {}, {"Issue": "issues"}) == []


def test_multiple_response_codes_each_emit_separately() -> None:
    operation = {
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Issue"},
                    },
                },
            },
            "201": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Issue"},
                    },
                },
            },
        },
    }
    references = find_body_references(operation, {}, {"Issue": "issues"})
    status_codes = {reference.status_code for reference in references}
    assert status_codes == {"200", "201"}


def test_dedup_collapses_identical_hits() -> None:
    """Same (resource, role, status, media, schema) dedupes to one entry."""
    operation = {
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "schema": {
                            "allOf": [
                                {"$ref": "#/components/schemas/Issue"},
                                {"$ref": "#/components/schemas/Issue"},
                            ],
                        },
                    },
                },
            },
        },
    }
    references = find_body_references(operation, {}, {"Issue": "issues"})
    assert len(references) == 1
