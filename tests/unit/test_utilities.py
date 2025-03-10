"""
Unit tests for the utility functions.
"""

import os
import tempfile
import pytest
import yaml

from scm_config_clone.utilities.settings import load_settings
from scm_config_clone.utilities.parse_csv import parse_csv_option, parse_csv_string
from scm_config_clone.utilities.compare_object_lists import compare_object_lists, find_missing_objects

from tests.factories.model_factories import AddressResponseModelFactory


class TestSettings:
    """Tests for the settings.py module."""
    
    def test_load_settings_valid_file(self):
        """Test loading settings from a valid YAML file."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            settings = {
                "oauth": {
                    "source": {
                        "client_id": "test-source-id",
                        "client_secret": "test-source-secret",
                        "tsg": "test-source-tsg",
                    },
                    "destination": {
                        "client_id": "test-dest-id",
                        "client_secret": "test-dest-secret",
                        "tsg": "test-dest-tsg",
                    },
                },
                "logging": "DEBUG",
                "auto_approve": True,
                "create_report": True,
                "dry_run": False,
                "quiet": False,
            }
            yaml.dump(settings, f)
            settings_path = f.name
        
        try:
            config = load_settings(settings_path)
            
            # Verify all keys are present with correct values
            assert config["source_scm"]["client_id"] == "test-source-id"
            assert config["source_scm"]["client_secret"] == "test-source-secret"
            assert config["source_scm"]["tenant"] == "test-source-tsg"
            
            assert config["destination_scm"]["client_id"] == "test-dest-id"
            assert config["destination_scm"]["client_secret"] == "test-dest-secret"
            assert config["destination_scm"]["tenant"] == "test-dest-tsg"
            
            assert config["logging"] == "DEBUG"
            assert config["auto_approve"] is True
            assert config["create_report"] is True
            assert config["dry_run"] is False
            assert config["quiet"] is False
        finally:
            os.unlink(settings_path)
    
    def test_load_settings_missing_keys(self):
        """Test loading settings with missing keys uses defaults."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            # Only include minimal settings
            settings = {
                "oauth": {
                    "source": {
                        "client_id": "test-source-id",
                        "client_secret": "test-source-secret",
                        "tsg": "test-source-tsg",
                    },
                    "destination": {
                        "client_id": "test-dest-id",
                        "client_secret": "test-dest-secret",
                        "tsg": "test-dest-tsg",
                    },
                },
            }
            yaml.dump(settings, f)
            settings_path = f.name
        
        try:
            config = load_settings(settings_path)
            
            # Verify defaults are used for missing keys
            assert config["logging"] == "INFO"
            assert config["auto_approve"] is False
            assert config["create_report"] is False
            assert config["dry_run"] is False
            assert config["quiet"] is False
        finally:
            os.unlink(settings_path)


class TestParseCSV:
    """Tests for the parse_csv.py module."""
    
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
    """Tests for the compare_object_lists.py module."""
    
    def test_compare_object_lists_all_match(self):
        """Test comparison when all source objects exist in destination."""
        # Create test objects
        names = ["obj1", "obj2", "obj3"]
        source_objects = [AddressResponseModelFactory(name=name) for name in names]
        destination_objects = [AddressResponseModelFactory(name=name) for name in names]
        
        results = compare_object_lists(source_objects, destination_objects)
        
        assert len(results) == 3
        assert all(r["already_configured"] for r in results)
        assert {r["name"] for r in results} == set(names)
    
    def test_compare_object_lists_no_match(self):
        """Test comparison when no source objects exist in destination."""
        source_objects = [
            AddressResponseModelFactory(name="src1"),
            AddressResponseModelFactory(name="src2"),
        ]
        destination_objects = [
            AddressResponseModelFactory(name="dst1"),
            AddressResponseModelFactory(name="dst2"),
        ]
        
        results = compare_object_lists(source_objects, destination_objects)
        
        assert len(results) == 2
        assert not any(r["already_configured"] for r in results)
        assert {r["name"] for r in results} == {"src1", "src2"}
    
    def test_compare_object_lists_partial_match(self):
        """Test comparison when some source objects exist in destination."""
        source_objects = [
            AddressResponseModelFactory(name="obj1"),
            AddressResponseModelFactory(name="obj2"),
            AddressResponseModelFactory(name="obj3"),
        ]
        destination_objects = [
            AddressResponseModelFactory(name="obj1"),
            AddressResponseModelFactory(name="obj3"),
            AddressResponseModelFactory(name="obj4"),
        ]
        
        results = compare_object_lists(source_objects, destination_objects)
        
        assert len(results) == 3
        
        # Check individual results
        obj1_result = next(r for r in results if r["name"] == "obj1")
        obj2_result = next(r for r in results if r["name"] == "obj2")
        obj3_result = next(r for r in results if r["name"] == "obj3")
        
        assert obj1_result["already_configured"] is True
        assert obj2_result["already_configured"] is False
        assert obj3_result["already_configured"] is True
    
    def test_find_missing_objects(self):
        """Test finding objects that exist in source but not in destination."""
        source_objects = [
            AddressResponseModelFactory(name="obj1"),
            AddressResponseModelFactory(name="obj2"),
            AddressResponseModelFactory(name="obj3"),
        ]
        destination_objects = [
            AddressResponseModelFactory(name="obj1"),
            AddressResponseModelFactory(name="obj4"),
        ]
        
        missing = find_missing_objects(source_objects, destination_objects)
        
        assert len(missing) == 2
        assert {obj.name for obj in missing} == {"obj2", "obj3"}
    
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
        source_objects = []
        destination_objects = [AddressResponseModelFactory(name="obj1")]
        
        missing = find_missing_objects(source_objects, destination_objects)
        
        assert len(missing) == 0
    
    def test_find_missing_objects_empty_destination(self):
        """Test finding missing objects with an empty destination list."""
        source_objects = [
            AddressResponseModelFactory(name="obj1"),
            AddressResponseModelFactory(name="obj2"),
        ]
        destination_objects = []
        
        missing = find_missing_objects(source_objects, destination_objects)
        
        assert len(missing) == 2
        assert {obj.name for obj in missing} == {"obj1", "obj2"}