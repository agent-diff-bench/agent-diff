"""Tests for replication JSONB handling."""

import pytest
from src.platform.evaluationEngine.replication import GlobalReplicationWorker


class TestZipColumns:
    def test_basic_zip(self):
        """Test basic column zipping without types."""
        names = ["a", "b", "c"]
        values = [1, "hello", True]
        
        result = GlobalReplicationWorker._zip_columns(names, values)
        
        assert result == {"a": 1, "b": "hello", "c": True}

    def test_zip_with_none(self):
        """Test that None inputs return None."""
        assert GlobalReplicationWorker._zip_columns(None, [1, 2]) is None
        assert GlobalReplicationWorker._zip_columns(["a", "b"], None) is None
        assert GlobalReplicationWorker._zip_columns(None, None) is None

    def test_jsonb_parsing(self):
        """Test that JSONB columns are parsed from strings to dicts."""
        names = ["id", "data", "config"]
        values = [
            "123",
            '{"name": "test", "nested": {"key": "value"}}',
            '{"enabled": true}',
        ]
        types = ["text", "jsonb", "jsonb"]
        
        result = GlobalReplicationWorker._zip_columns(names, values, types)
        
        assert result["id"] == "123"  # text stays as string
        assert result["data"] == {"name": "test", "nested": {"key": "value"}}
        assert result["config"] == {"enabled": True}

    def test_json_parsing(self):
        """Test that JSON columns (not just JSONB) are also parsed."""
        names = ["data"]
        values = ['[1, 2, 3]']
        types = ["json"]
        
        result = GlobalReplicationWorker._zip_columns(names, values, types)
        
        assert result["data"] == [1, 2, 3]

    def test_calendar_event_start_field(self):
        """Test parsing of calendar event start/end fields (like the bug scenario)."""
        names = ["id", "summary", "start", "end"]
        values = [
            "event_123",
            "Test Event",
            '{"dateTime": "2018-06-18T08:00:00", "timeZone": "America/Los_Angeles"}',
            '{"dateTime": "2018-06-18T09:00:00", "timeZone": "America/Los_Angeles"}',
        ]
        types = ["text", "text", "jsonb", "jsonb"]
        
        result = GlobalReplicationWorker._zip_columns(names, values, types)
        
        # After parsing, nested access should work
        assert result["start"]["dateTime"] == "2018-06-18T08:00:00"
        assert result["start"]["timeZone"] == "America/Los_Angeles"
        assert result["end"]["dateTime"] == "2018-06-18T09:00:00"

    def test_invalid_json_stays_as_string(self):
        """Test that invalid JSON values are kept as strings."""
        names = ["data"]
        values = ["this is not valid json {"]
        types = ["jsonb"]
        
        result = GlobalReplicationWorker._zip_columns(names, values, types)
        
        assert result["data"] == "this is not valid json {"

    def test_without_types(self):
        """Test that without types, all values stay as-is."""
        names = ["data"]
        values = ['{"key": "value"}']
        
        result = GlobalReplicationWorker._zip_columns(names, values)
        
        # Without types, JSONB string is NOT parsed
        assert result["data"] == '{"key": "value"}'

    def test_jsonb_already_parsed(self):
        """Test that already-parsed values are not double-parsed."""
        names = ["data"]
        values = [{"key": "value"}]  # Already a dict, not a string
        types = ["jsonb"]
        
        result = GlobalReplicationWorker._zip_columns(names, values, types)
        
        assert result["data"] == {"key": "value"}
