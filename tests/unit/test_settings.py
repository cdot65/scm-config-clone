"""
Tests for the settings module.
"""

import os
import sys
import tempfile
import importlib.util
import pytest
import yaml


# Directly import the modules we want to test without going through __init__.py
def load_module_from_path(module_name, file_path):
    """Load a module directly from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Load the settings module directly
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
settings_module = load_module_from_path(
    'settings_module',
    os.path.join(base_path, 'scm_config_clone', 'utilities', 'settings.py')
)


class TestSettings:
    """Tests for the settings.py module."""
    
    def test_load_settings_valid_file(self):
        """Test loading settings from a valid YAML file."""
        settings_file = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml")
        settings_path = settings_file.name
        settings_file.close()
        
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
        
        with open(settings_path, 'w') as f:
            yaml.dump(settings, f)
        
        try:
            config = settings_module.load_settings(settings_path)
            
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
        settings_file = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml")
        settings_path = settings_file.name
        settings_file.close()
        
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
        
        with open(settings_path, 'w') as f:
            yaml.dump(settings, f)
        
        try:
            config = settings_module.load_settings(settings_path)
            
            # Verify defaults are used for missing keys
            assert config["logging"] == "INFO"
            assert config["auto_approve"] is False
            assert config["create_report"] is False
            assert config["dry_run"] is False
            assert config["quiet"] is False
        finally:
            os.unlink(settings_path)