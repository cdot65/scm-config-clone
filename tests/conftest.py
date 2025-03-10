"""
Global pytest fixtures for scm-config-clone tests.
"""

import os
import tempfile
from pathlib import Path
import pytest
import yaml
from typer.testing import CliRunner


@pytest.fixture
def runner():
    """
    Return a Typer CLI runner for testing commands.
    """
    return CliRunner()


@pytest.fixture
def temp_settings_file():
    """
    Create a temporary settings.yaml file for testing.

    Returns the path to the temporary file.
    The file is automatically deleted after the test completes.
    """
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        # Create a minimal settings file with test values
        settings = {
            "oauth": {
                "source": {
                    "client_id": "test-source-client-id",
                    "client_secret": "test-source-client-secret",
                    "tsg": "test-source-tenant",
                },
                "destination": {
                    "client_id": "test-dest-client-id",
                    "client_secret": "test-dest-client-secret",
                    "tsg": "test-dest-tenant",
                },
            },
            "logging": "INFO",
            "auto_approve": True,
            "create_report": False,
            "dry_run": True,
            "quiet": True,
        }
        yaml.dump(settings, f)
        settings_path = f.name

    yield settings_path
    
    # Clean up the temporary file after the test
    os.unlink(settings_path)