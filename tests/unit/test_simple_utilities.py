"""
Simple unit tests for utility functions that don't require importing the main app.
We directly import the utility modules to avoid initialization issues with the main codebase.
"""

import sys
import os
import importlib.util
import pytest


# Directly import the utility modules we want to test without going through __init__.py
def load_module_from_path(module_name, file_path):
    """Load a module directly from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Load the modules directly
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
parse_csv_module = load_module_from_path(
    'parse_csv_module',
    os.path.join(base_path, 'scm_config_clone', 'utilities', 'parse_csv.py')
)

compare_objects_module = load_module_from_path(
    'compare_objects_module',
    os.path.join(base_path, 'scm_config_clone', 'utilities', 'compare_object_lists.py')
)


class TestParseCSV:
    """Tests for the parse_csv.py module."""
    
    def test_parse_csv_option_with_values(self):
        """Test parsing a CSV string with multiple values."""
        result = parse_csv_module.parse_csv_option("value1,value2,value3")
        assert result == ["value1", "value2", "value3"]
    
    def test_parse_csv_option_with_whitespace(self):
        """Test parsing a CSV string with whitespace."""
        result = parse_csv_module.parse_csv_option(" value1 , value2 , value3 ")
        assert result == ["value1", "value2", "value3"]
    
    def test_parse_csv_option_with_empty_values(self):
        """Test parsing a CSV string with empty values."""
        result = parse_csv_module.parse_csv_option("value1,,value3,")
        assert result == ["value1", "value3"]
    
    def test_parse_csv_option_with_none(self):
        """Test parsing None."""
        result = parse_csv_module.parse_csv_option(None)
        assert result is None
    
    def test_parse_csv_option_with_empty_string(self):
        """Test parsing an empty string."""
        result = parse_csv_module.parse_csv_option("")
        assert result is None
    
    def test_parse_csv_string_with_values(self):
        """Test parsing a CSV string with multiple values."""
        result = parse_csv_module.parse_csv_string("value1,value2,value3")
        assert result == ["value1", "value2", "value3"]
    
    def test_parse_csv_string_with_whitespace(self):
        """Test parsing a CSV string with whitespace."""
        result = parse_csv_module.parse_csv_string(" value1 , value2 , value3 ")
        assert result == ["value1", "value2", "value3"]
    
    def test_parse_csv_string_with_empty_values(self):
        """Test parsing a CSV string with empty values."""
        result = parse_csv_module.parse_csv_string("value1,,value3,")
        assert result == ["value1", "value3"]
    
    def test_parse_csv_string_with_empty_string(self):
        """Test parsing an empty string."""
        result = parse_csv_module.parse_csv_string("")
        assert result == []


class TestFindMissingObjects:
    """Test the find_missing_objects function."""
    
    def test_find_missing_objects_custom_attribute(self):
        """Test finding missing objects using a custom attribute name."""
        class TestObject:
            def __init__(self, id_value):
                self.id_value = id_value
        
        source_objects = [TestObject("id1"), TestObject("id2"), TestObject("id3")]
        destination_objects = [TestObject("id1"), TestObject("id3")]
        
        missing = compare_objects_module.find_missing_objects(
            source_objects, destination_objects, name_attribute="id_value"
        )
        
        assert len(missing) == 1
        assert missing[0].id_value == "id2"
    
    def test_find_missing_objects_empty_source(self):
        """Test finding missing objects with an empty source list."""
        class TestObject:
            def __init__(self, name):
                self.name = name
                
        source_objects = []
        destination_objects = [TestObject("obj1")]
        
        missing = compare_objects_module.find_missing_objects(source_objects, destination_objects)
        
        assert len(missing) == 0
    
    def test_find_missing_objects_empty_destination(self):
        """Test finding missing objects with an empty destination list."""
        class TestObject:
            def __init__(self, name):
                self.name = name
                
        source_objects = [TestObject("obj1"), TestObject("obj2")]
        destination_objects = []
        
        missing = compare_objects_module.find_missing_objects(source_objects, destination_objects)
        
        assert len(missing) == 2
        assert sorted([obj.name for obj in missing]) == ["obj1", "obj2"]
    
    def test_compare_object_lists(self):
        """Test the compare_object_lists function."""
        class TestObject:
            def __init__(self, name):
                self.name = name
        
        source_objects = [TestObject("obj1"), TestObject("obj2"), TestObject("obj3")]
        destination_objects = [TestObject("obj1"), TestObject("obj3")]
        
        results = compare_objects_module.compare_object_lists(source_objects, destination_objects)
        
        assert len(results) == 3
        
        # Check individual results
        assert results[0]["name"] == "obj1"
        assert results[0]["already_configured"] is True
        
        assert results[1]["name"] == "obj2"
        assert results[1]["already_configured"] is False
        
        assert results[2]["name"] == "obj3"
        assert results[2]["already_configured"] is True