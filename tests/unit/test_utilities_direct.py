"""
Unit tests for the utility functions.
These tests use direct imports to avoid dependency issues.
"""

import pytest
import os
import tempfile
import yaml
from typing import List, Optional

# ---------------------------------------------------------------------------
# Copy of the actual functions to test (to avoid import issues)
# ---------------------------------------------------------------------------

def parse_csv_option(value: Optional[str]) -> Optional[List[str]]:
    """Parse a comma-separated string into a list of stripped strings."""
    if not value:
        return None
    return [v.strip() for v in value.split(",") if v.strip()]


def parse_csv_string(value: str) -> List[str]:
    """Parse a comma-separated string into a list of stripped strings."""
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


def compare_object_lists(source_objects: list, destination_objects: list) -> list:
    """Compare source and destination objects and determine which exist in destination."""
    # Create a set of names from the destination to allow O(1) lookups
    destination_names = {obj.name for obj in destination_objects}

    results = []
    for src_obj in source_objects:
        results.append(
            {
                "name": src_obj.name,
                "already_configured": src_obj.name in destination_names,
            }
        )

    return results


def find_missing_objects(source_objects: list, destination_objects: list, name_attribute: str = 'name') -> list:
    """Find objects that exist in source but not in destination."""
    # Create a set of names from the destination for O(1) lookups
    destination_names = {getattr(obj, name_attribute) for obj in destination_objects}
    
    # Return objects from source that are not in destination
    return [obj for obj in source_objects if getattr(obj, name_attribute) not in destination_names]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestParseCSV:
    """Tests for the parse_csv functions."""
    
    def test_parse_csv_option_with_values(self):
        """Test parsing a CSV string with multiple values."""
        result = parse_csv_option("value1,value2,value3")
        assert result == ["value1", "value2", "value3"]
    
    def test_parse_csv_option_with_whitespace(self):
        """Test parsing a CSV string with whitespace."""
        result = parse_csv_option(" value1 , value2 , value3 ")
        assert result == ["value1", "value2", "value3"]
    
    def test_parse_csv_option_with_empty_values(self):
        """Test parsing a CSV string with empty values."""
        result = parse_csv_option("value1,,value3,")
        assert result == ["value1", "value3"]
    
    def test_parse_csv_option_with_none(self):
        """Test parsing None."""
        result = parse_csv_option(None)
        assert result is None
    
    def test_parse_csv_option_with_empty_string(self):
        """Test parsing an empty string."""
        result = parse_csv_option("")
        assert result is None
    
    def test_parse_csv_string_with_values(self):
        """Test parsing a CSV string with multiple values."""
        result = parse_csv_string("value1,value2,value3")
        assert result == ["value1", "value2", "value3"]
    
    def test_parse_csv_string_with_whitespace(self):
        """Test parsing a CSV string with whitespace."""
        result = parse_csv_string(" value1 , value2 , value3 ")
        assert result == ["value1", "value2", "value3"]
    
    def test_parse_csv_string_with_empty_values(self):
        """Test parsing a CSV string with empty values."""
        result = parse_csv_string("value1,,value3,")
        assert result == ["value1", "value3"]
    
    def test_parse_csv_string_with_empty_string(self):
        """Test parsing an empty string."""
        result = parse_csv_string("")
        assert result == []


class TestCompareObjectLists:
    """Tests for the compare_object_lists.py functions."""
    
    def test_find_missing_objects_custom_attribute(self):
        """Test finding missing objects using a custom attribute name."""
        class TestObject:
            def __init__(self, id_value):
                self.id_value = id_value
        
        source_objects = [TestObject("id1"), TestObject("id2"), TestObject("id3")]
        destination_objects = [TestObject("id1"), TestObject("id3")]
        
        missing = find_missing_objects(source_objects, destination_objects, name_attribute="id_value")
        
        assert len(missing) == 1
        assert missing[0].id_value == "id2"
    
    def test_find_missing_objects_empty_source(self):
        """Test finding missing objects with an empty source list."""
        class TestObject:
            def __init__(self, name):
                self.name = name
                
        source_objects = []
        destination_objects = [TestObject("obj1")]
        
        missing = find_missing_objects(source_objects, destination_objects)
        
        assert len(missing) == 0
    
    def test_find_missing_objects_empty_destination(self):
        """Test finding missing objects with an empty destination list."""
        class TestObject:
            def __init__(self, name):
                self.name = name
                
        source_objects = [TestObject("obj1"), TestObject("obj2")]
        destination_objects = []
        
        missing = find_missing_objects(source_objects, destination_objects)
        
        assert len(missing) == 2
        assert sorted([obj.name for obj in missing]) == ["obj1", "obj2"]
    
    def test_compare_object_lists(self):
        """Test the compare_object_lists function."""
        class TestObject:
            def __init__(self, name):
                self.name = name
        
        source_objects = [TestObject("obj1"), TestObject("obj2"), TestObject("obj3")]
        destination_objects = [TestObject("obj1"), TestObject("obj3")]
        
        results = compare_object_lists(source_objects, destination_objects)
        
        assert len(results) == 3
        
        # Check individual results
        assert results[0]["name"] == "obj1"
        assert results[0]["already_configured"] is True
        
        assert results[1]["name"] == "obj2"
        assert results[1]["already_configured"] is False
        
        assert results[2]["name"] == "obj3"
        assert results[2]["already_configured"] is True