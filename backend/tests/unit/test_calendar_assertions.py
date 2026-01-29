"""
Test calendar benchmark assertions to verify they work correctly.
This test simulates the diff that would be produced by the Cosmic Voyagers prompt.
"""
import pytest
from src.platform.evaluationEngine.assertion import AssertionEngine


class TestCalendarCosmicVoyagersAssertions:
    """Test assertions for Prompt 1: Cosmic Voyagers Astronomy Club"""
    
    @pytest.fixture
    def spec(self):
        """The assertion spec from calendar_bench.json test_1"""
        return {
            "version": "0.1",
            "ignore_fields": {
                "global": [
                    "created_at",
                    "updated_at",
                    "etag",
                    "html_link",
                    "ical_uid",
                    "sequence"
                ]
            },
            "assertions": [
                {
                    "diff_type": "added",
                    "entity": "calendars",
                    "where": {
                        "summary": {"contains": "Cosmic Voyagers HQ"}
                    },
                    "expected_count": 1
                },
                {
                    "diff_type": "added",
                    "entity": "calendar_acl_rules",
                    "where": {
                        "scope_value": {"eq": "yuki@test.com"},
                        "role": {"eq": "writer"}
                    },
                    "expected_count": 1
                },
                {
                    "diff_type": "added",
                    "entity": "calendar_events",
                    "where": {
                        "summary": {"contains": "Perseid Meteor Shower Watch Party"}
                    },
                    "expected_count": 1
                },
                {
                    "diff_type": "added",
                    "entity": "calendar_events",
                    "where": {
                        "summary": {"contains": "Telescope Alignment Ceremony"}
                    },
                    "expected_count": 1
                },
                {
                    "diff_type": "changed",
                    "entity": "calendar_events",
                    "where": {
                        "summary": {"contains": "Perseid Meteor Shower Watch Party"}
                    },
                    "expected_changes": {
                        "location": {
                            "to": {"contains": "Hillcrest Observatory Field"}
                        }
                    }
                },
                {
                    "diff_type": "removed",
                    "entity": "calendar_events",
                    "where": {
                        "id": {"eq": "event_failed_rocket"}
                    },
                    "expected_count": 1
                }
            ]
        }
    
    def test_all_assertions_pass_with_correct_diff(self, spec):
        """Test that all assertions pass when the diff contains expected changes"""
        # Simulate the diff that a correctly-behaving agent would produce
        diff = {
            "inserts": [
                # New calendar created
                {
                    "__table__": "calendars",
                    "id": "cosmic_voyagers_hq_123",
                    "summary": "Cosmic Voyagers HQ",
                    "owner_id": "user_agent",
                    "time_zone": "America/Los_Angeles"
                },
                # ACL rule for Yuki
                {
                    "__table__": "calendar_acl_rules",
                    "id": "acl_yuki_cosmic",
                    "calendar_id": "cosmic_voyagers_hq_123",
                    "scope_value": "yuki@test.com",
                    "scope_type": "user",
                    "role": "writer"
                },
                # Perseid event (will also appear in updates for location change)
                {
                    "__table__": "calendar_events",
                    "id": "event_perseid_123",
                    "calendar_id": "cosmic_voyagers_hq_123",
                    "summary": "Perseid Meteor Shower Watch Party",
                    "location": None
                },
                # Telescope alignment event
                {
                    "__table__": "calendar_events",
                    "id": "event_telescope_456",
                    "calendar_id": "cosmic_voyagers_hq_123",
                    "summary": "Telescope Alignment Ceremony",
                    "description": "Setting up equipment before the watch party"
                },
                # Calendar list entry for the new calendar
                {
                    "__table__": "calendar_list_entries",
                    "id": "cle_cosmic",
                    "user_id": "user_agent",
                    "calendar_id": "cosmic_voyagers_hq_123",
                    "access_role": "owner"
                }
            ],
            "updates": [
                # Location update for Perseid event
                {
                    "__table__": "calendar_events",
                    "before": {
                        "id": "event_perseid_123",
                        "summary": "Perseid Meteor Shower Watch Party",
                        "location": None
                    },
                    "after": {
                        "id": "event_perseid_123",
                        "summary": "Perseid Meteor Shower Watch Party",
                        "location": "Hillcrest Observatory Field"
                    }
                }
            ],
            "deletes": [
                # Deleted the failed rocket event
                {
                    "__table__": "calendar_events",
                    "id": "event_failed_rocket",
                    "summary": "Failed Rocket Launch Viewing (Cancelled)",
                    "calendar_id": "test.user@test.com"
                }
            ]
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        
        # Print details for debugging
        print(f"\n=== Evaluation Result ===")
        print(f"Passed: {result['passed']}")
        print(f"Score: {result['score']}")
        if result.get('failures'):
            for i, failure in enumerate(result['failures']):
                print(f"Failure {i+1}: {failure}")
        
        assert result["passed"] is True, f"Assertions failed: {result.get('failures', [])}"
        assert result["score"]["passed"] == 6
        assert result["score"]["total"] == 6
    
    def test_fails_when_calendar_not_created(self, spec):
        """Test that assertions fail when calendar is not created"""
        diff = {
            "inserts": [],
            "updates": [],
            "deletes": []
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        
        assert result["passed"] is False
        assert result["score"]["passed"] < result["score"]["total"]
    
    def test_fails_when_wrong_acl_role(self, spec):
        """Test that assertions fail when Yuki gets wrong role"""
        diff = {
            "inserts": [
                {
                    "__table__": "calendars",
                    "id": "cosmic_voyagers_hq_123",
                    "summary": "Cosmic Voyagers HQ"
                },
                # Wrong role - reader instead of writer
                {
                    "__table__": "calendar_acl_rules",
                    "scope_value": "yuki@test.com",
                    "scope_type": "user",
                    "role": "reader"  # Should be "writer"
                },
                {
                    "__table__": "calendar_events",
                    "summary": "Perseid Meteor Shower Watch Party"
                },
                {
                    "__table__": "calendar_events",
                    "summary": "Telescope Alignment Ceremony"
                }
            ],
            "updates": [
                {
                    "__table__": "calendar_events",
                    "before": {"summary": "Perseid Meteor Shower Watch Party", "location": None},
                    "after": {"summary": "Perseid Meteor Shower Watch Party", "location": "Hillcrest Observatory Field"}
                }
            ],
            "deletes": [
                {"__table__": "calendar_events", "id": "event_failed_rocket"}
            ]
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        
        # Should fail because Yuki has reader role instead of writer
        assert result["passed"] is False
        # 5 should pass, 1 should fail (ACL role)
        assert result["score"]["passed"] == 5
        assert result["score"]["total"] == 6


class TestSingleAssertions:
    """Test individual assertion types in isolation"""
    
    def test_calendar_added(self):
        """Test detecting a new calendar"""
        spec = {
            "version": "0.1",
            "assertions": [
                {
                    "diff_type": "added",
                    "entity": "calendars",
                    "where": {"summary": {"contains": "Test Calendar"}},
                    "expected_count": 1
                }
            ]
        }
        diff = {
            "inserts": [
                {"__table__": "calendars", "id": "cal123", "summary": "My Test Calendar"}
            ],
            "updates": [],
            "deletes": []
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        assert result["passed"] is True
    
    def test_event_deleted(self):
        """Test detecting an event deletion"""
        spec = {
            "version": "0.1",
            "assertions": [
                {
                    "diff_type": "removed",
                    "entity": "calendar_events",
                    "where": {"summary": {"contains": "Cancelled"}},
                    "expected_count": 1
                }
            ]
        }
        diff = {
            "inserts": [],
            "updates": [],
            "deletes": [
                {"__table__": "calendar_events", "id": "e1", "summary": "Meeting (Cancelled)"}
            ]
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        assert result["passed"] is True
    
    def test_event_location_changed(self):
        """Test detecting an event location update"""
        spec = {
            "version": "0.1",
            "assertions": [
                {
                    "diff_type": "changed",
                    "entity": "calendar_events",
                    "where": {"id": {"eq": "event_123"}},
                    "expected_changes": {
                        "location": {
                            "to": {"eq": "New Location"}
                        }
                    }
                }
            ]
        }
        diff = {
            "inserts": [],
            "updates": [
                {
                    "__table__": "calendar_events",
                    "before": {"id": "event_123", "location": "Old Location"},
                    "after": {"id": "event_123", "location": "New Location"}
                }
            ],
            "deletes": []
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        assert result["passed"] is True
    
    def test_acl_writer_added(self):
        """Test detecting an ACL rule with writer role"""
        spec = {
            "version": "0.1",
            "assertions": [
                {
                    "diff_type": "added",
                    "entity": "calendar_acl_rules",
                    "where": {
                        "scope_value": {"eq": "user@example.com"},
                        "role": {"eq": "writer"}
                    },
                    "expected_count": 1
                }
            ]
        }
        diff = {
            "inserts": [
                {
                    "__table__": "calendar_acl_rules",
                    "id": "acl_1",
                    "scope_value": "user@example.com",
                    "scope_type": "user",
                    "role": "writer"
                }
            ],
            "updates": [],
            "deletes": []
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        assert result["passed"] is True


class TestGreenThumbsGardenAssertions:
    """Test assertions for Prompt 2: Green Thumbs Urban Garden Collective"""
    
    @pytest.fixture
    def spec(self):
        """The assertion spec from calendar_bench.json test_2"""
        return {
            "version": "0.1",
            "ignore_fields": {
                "global": [
                    "created_at",
                    "updated_at",
                    "etag",
                    "html_link",
                    "ical_uid",
                    "sequence"
                ]
            },
            "assertions": [
                {
                    "diff_type": "added",
                    "entity": "calendar_events",
                    "where": {
                        "summary": {"contains": "Sacred Tomato Planting Ritual"}
                    },
                    "expected_count": 1
                },
                {
                    "diff_type": "changed",
                    "entity": "calendar_events",
                    "where": {
                        "summary": {"contains": "Sacred Tomato Planting Ritual"}
                    },
                    "expected_changes": {
                        "description": {
                            "to": {"i_contains": "seedlings"}
                        }
                    }
                },
                {
                    "diff_type": "added",
                    "entity": "calendar_events",
                    "where": {
                        "summary": {"contains": "Compost Communion"},
                        "calendar_id": {"eq": "cal_harvest_schedule"}
                    },
                    "expected_count": 1
                },
                {
                    "diff_type": "removed",
                    "entity": "calendar_events",
                    "where": {
                        "id": {"eq": "event_weed_warrior"}
                    },
                    "expected_count": 1
                },
                {
                    "diff_type": "added",
                    "entity": "calendar_acl_rules",
                    "where": {
                        "scope_value": {"eq": "chisom@test.com"},
                        "role": {"eq": "reader"},
                        "calendar_id": {"eq": "cal_harvest_schedule"}
                    },
                    "expected_count": 1
                },
                {
                    "diff_type": "changed",
                    "entity": "calendar_events",
                    "where": {
                        "summary": {"contains": "Compost Communion"}
                    },
                    "expected_changes": {
                        "attendees": {
                            "to": {"contains": "dariush@test.com"}
                        }
                    }
                },
                {
                    "diff_type": "added",
                    "entity": "calendars",
                    "where": {
                        "summary": {"contains": "Greenhouse Experiments"}
                    },
                    "expected_count": 1
                }
            ]
        }
    
    def test_all_assertions_pass_with_correct_diff(self, spec):
        """Test that all 7 assertions pass when the diff contains expected changes"""
        # Simulate the diff that a correctly-behaving agent would produce
        diff = {
            "inserts": [
                # Sacred Tomato Planting Ritual event (will also appear in updates)
                {
                    "__table__": "calendar_events",
                    "id": "event_tomato_ritual",
                    "calendar_id": "test.user@test.com",
                    "summary": "Sacred Tomato Planting Ritual",
                    "description": None
                },
                # Compost Communion event on Harvest Schedule
                {
                    "__table__": "calendar_events",
                    "id": "event_compost_communion",
                    "calendar_id": "cal_harvest_schedule",
                    "summary": "Compost Communion: The Turning of the Heap",
                    "description": "Compost turning ceremony"
                },
                # ACL rule for Chisom with reader access
                {
                    "__table__": "calendar_acl_rules",
                    "id": "acl_chisom_harvest",
                    "calendar_id": "cal_harvest_schedule",
                    "scope_value": "chisom@test.com",
                    "scope_type": "user",
                    "role": "reader"
                },
                # New Greenhouse Experiments calendar
                {
                    "__table__": "calendars",
                    "id": "cal_greenhouse_experiments",
                    "summary": "Greenhouse Experiments",
                    "owner_id": "user_agent"
                },
                # Calendar list entry for new calendar
                {
                    "__table__": "calendar_list_entries",
                    "id": "cle_greenhouse",
                    "user_id": "user_agent",
                    "calendar_id": "cal_greenhouse_experiments"
                }
            ],
            "updates": [
                # Sacred Tomato Planting Ritual description update
                {
                    "__table__": "calendar_events",
                    "before": {
                        "id": "event_tomato_ritual",
                        "summary": "Sacred Tomato Planting Ritual",
                        "description": None
                    },
                    "after": {
                        "id": "event_tomato_ritual",
                        "summary": "Sacred Tomato Planting Ritual",
                        "description": "Bring your own seedlings and prayers"
                    }
                },
                # Compost Communion attendees update
                {
                    "__table__": "calendar_events",
                    "before": {
                        "id": "event_compost_communion",
                        "summary": "Compost Communion: The Turning of the Heap",
                        "attendees": None
                    },
                    "after": {
                        "id": "event_compost_communion",
                        "summary": "Compost Communion: The Turning of the Heap",
                        "attendees": "[{\"email\": \"dariush@test.com\", \"responseStatus\": \"needsAction\"}]"
                    }
                }
            ],
            "deletes": [
                # Deleted the Weed Warrior Wednesday event
                {
                    "__table__": "calendar_events",
                    "id": "event_weed_warrior",
                    "calendar_id": "cal_harvest_schedule",
                    "summary": "Weed Warrior Wednesday"
                }
            ]
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        
        # Print details for debugging
        print(f"\n=== Green Thumbs Evaluation Result ===")
        print(f"Passed: {result['passed']}")
        print(f"Score: {result['score']}")
        if result.get('failures'):
            for i, failure in enumerate(result['failures']):
                print(f"Failure {i+1}: {failure}")
        
        assert result["passed"] is True, f"Assertions failed: {result.get('failures', [])}"
        assert result["score"]["passed"] == 7
        assert result["score"]["total"] == 7
    
    def test_fails_when_no_actions_taken(self, spec):
        """Test that assertions fail when no actions are taken"""
        diff = {
            "inserts": [],
            "updates": [],
            "deletes": []
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        
        assert result["passed"] is False
        assert result["score"]["passed"] == 0
        assert result["score"]["total"] == 7
    
    def test_partial_pass_when_calendar_created_only(self, spec):
        """Test that only calendar creation passes when that's all that's done"""
        diff = {
            "inserts": [
                {
                    "__table__": "calendars",
                    "id": "cal_greenhouse",
                    "summary": "Greenhouse Experiments"
                }
            ],
            "updates": [],
            "deletes": []
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        
        assert result["passed"] is False
        # Only 1 assertion should pass (calendar created)
        assert result["score"]["passed"] == 1
        assert result["score"]["total"] == 7
    
    def test_fails_when_wrong_acl_role(self, spec):
        """Test that ACL assertion fails when Chisom gets writer instead of reader"""
        diff = {
            "inserts": [
                {
                    "__table__": "calendar_events",
                    "summary": "Sacred Tomato Planting Ritual"
                },
                {
                    "__table__": "calendar_events",
                    "calendar_id": "cal_harvest_schedule",
                    "summary": "Compost Communion: The Turning of the Heap"
                },
                # Wrong role - writer instead of reader
                {
                    "__table__": "calendar_acl_rules",
                    "calendar_id": "cal_harvest_schedule",
                    "scope_value": "chisom@test.com",
                    "role": "writer"  # Should be "reader"
                },
                {
                    "__table__": "calendars",
                    "summary": "Greenhouse Experiments"
                }
            ],
            "updates": [
                {
                    "__table__": "calendar_events",
                    "before": {"summary": "Sacred Tomato Planting Ritual", "description": None},
                    "after": {"summary": "Sacred Tomato Planting Ritual", "description": "Bring seedlings"}
                },
                {
                    "__table__": "calendar_events",
                    "before": {"summary": "Compost Communion: The Turning of the Heap", "attendees": None},
                    "after": {"summary": "Compost Communion: The Turning of the Heap", "attendees": "dariush@test.com"}
                }
            ],
            "deletes": [
                {"__table__": "calendar_events", "id": "event_weed_warrior"}
            ]
        }
        
        engine = AssertionEngine(spec)
        result = engine.evaluate(diff)
        
        # Should fail because Chisom has writer role instead of reader
        assert result["passed"] is False
        # 6 should pass, 1 should fail (ACL role)
        assert result["score"]["passed"] == 6
        assert result["score"]["total"] == 7
