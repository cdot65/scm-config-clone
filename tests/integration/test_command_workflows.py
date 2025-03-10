"""
Integration tests for command workflows.

These tests simulate complete workflows across multiple commands,
focusing on the interaction between commands rather than individual command behavior.
"""

import pytest
from unittest.mock import patch, MagicMock
import tempfile
import os
import yaml
from typer.testing import CliRunner

from scm_config_clone.main import app
from tests.factories.model_factories import (
    AddressResponseModelFactory, 
    TagResponseModelFactory,
    ServiceResponseModelFactory
)


@pytest.fixture
def temp_settings_yml():
    """Create a temporary settings.yaml file."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        settings = {
            "oauth": {
                "source": {
                    "client_id": "test-src-id",
                    "client_secret": "test-src-secret",
                    "tsg": "test-src-tenant",
                },
                "destination": {
                    "client_id": "test-dst-id",
                    "client_secret": "test-dst-secret",
                    "tsg": "test-dst-tenant",
                },
            },
            "logging": "INFO",
            "auto_approve": True,
            "create_report": True,
            "dry_run": False,
            "quiet": False,
        }
        yaml.dump(settings, f)
        path = f.name
    
    yield path
    
    # Clean up
    os.unlink(path)


@pytest.fixture
def mock_all_apis():
    """
    Create mock SCM APIs for all object types we test.
    """
    with patch('scm.client.Scm') as mock_scm:
        # Prepare mock clients
        mock_src_client = MagicMock()
        mock_dst_client = MagicMock()
        mock_scm.side_effect = [mock_src_client, mock_dst_client]
        
        # Mock Address API
        with patch('scm.config.objects.Address') as mock_address_api:
            # Mock Tag API
            with patch('scm.config.objects.Tag') as mock_tag_api:
                # Mock Service API
                with patch('scm.config.objects.Service') as mock_service_api:
                    # Create source objects
                    src_addresses = [
                        AddressResponseModelFactory(name=f"address{i}", ip_netmask=f"10.0.0.{i}/32")
                        for i in range(1, 4)
                    ]
                    src_tags = [
                        TagResponseModelFactory(name=f"tag{i}", color=f"color{i}")
                        for i in range(1, 4)
                    ]
                    src_services = [
                        ServiceResponseModelFactory(
                            name=f"service{i}", 
                            protocol="tcp", 
                            port=str(440 + i)
                        )
                        for i in range(1, 4)
                    ]
                    
                    # Setup APIs
                    mock_src_address = MagicMock()
                    mock_src_address.list.return_value = src_addresses
                    mock_dst_address = MagicMock()
                    mock_dst_address.list.return_value = []
                    
                    mock_src_tag = MagicMock()
                    mock_src_tag.list.return_value = src_tags
                    mock_dst_tag = MagicMock()
                    mock_dst_tag.list.return_value = []
                    
                    mock_src_service = MagicMock()
                    mock_src_service.list.return_value = src_services
                    mock_dst_service = MagicMock()
                    mock_dst_service.list.return_value = []
                    
                    # Configure side effects
                    mock_address_api.side_effect = [mock_src_address, mock_dst_address, mock_dst_address]
                    mock_tag_api.side_effect = [mock_src_tag, mock_dst_tag, mock_dst_tag]
                    mock_service_api.side_effect = [mock_src_service, mock_dst_service, mock_dst_service]
                    
                    # Return a dict with all our mocks
                    yield {
                        "scm": mock_scm,
                        "address": mock_address_api,
                        "tag": mock_tag_api,
                        "service": mock_service_api,
                        "clients": {
                            "src": mock_src_client,
                            "dst": mock_dst_client
                        },
                        "apis": {
                            "address": {"src": mock_src_address, "dst": mock_dst_address},
                            "tag": {"src": mock_src_tag, "dst": mock_dst_tag},
                            "service": {"src": mock_src_service, "dst": mock_dst_service}
                        }
                    }


class TestCloneWorkflow:
    """Test complete cloning workflows."""
    
    def test_clone_objects_workflow(self, temp_settings_yml, mock_all_apis, runner):
        """
        Test a complete workflow cloning multiple object types.
        
        This tests the end-to-end workflow of cloning addresses, tags, and services
        from a source folder to a destination folder.
        """
        settings_path = temp_settings_yml
        
        # Run clone commands
        commands = [
            ["addresses", "--context", "folder", "--source", "test-folder", 
             "--destination", "test-dest-folder", "--settings-file", settings_path],
            ["tags", "--context", "folder", "--source", "test-folder", 
             "--destination", "test-dest-folder", "--settings-file", settings_path],
            ["services", "--context", "folder", "--source", "test-folder", 
             "--destination", "test-dest-folder", "--settings-file", settings_path],
        ]
        
        for cmd in commands:
            result = runner.invoke(app, cmd)
            assert result.exit_code == 0
        
        # Verify calls were made correctly
        address_api = mock_all_apis["apis"]["address"]
        tag_api = mock_all_apis["apis"]["tag"]
        service_api = mock_all_apis["apis"]["service"]
        
        # Each API should have list() called (source and destination)
        assert address_api["src"].list.call_count == 1
        assert address_api["dst"].list.call_count == 1
        assert tag_api["src"].list.call_count == 1
        assert tag_api["dst"].list.call_count == 1
        assert service_api["src"].list.call_count == 1
        assert service_api["dst"].list.call_count == 1
        
        # Each API should have create() called for each source object
        assert address_api["dst"].create.call_count == 3
        assert tag_api["dst"].create.call_count == 3
        assert service_api["dst"].create.call_count == 3


class TestReportGeneration:
    """Test report generation functionality."""
    
    def test_create_report_flag(self, temp_settings_yml, mock_all_apis, runner):
        """Test that report is generated when --create-report flag is used."""
        settings_path = temp_settings_yml
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                # Run command with create_report flag
                result = runner.invoke(
                    app, 
                    ["addresses", "--context", "folder", "--source", "test-folder", 
                     "--destination", "test-dest-folder", "--settings-file", settings_path,
                     "--create-report"]
                )
                
                assert result.exit_code == 0
                
                # Check that results.csv file was created
                assert os.path.exists("result.csv")
                
                # Check content of the file
                with open("result.csv", "r") as f:
                    content = f.read()
                    # Each address should be in the file
                    assert "address1" in content
                    assert "address2" in content
                    assert "address3" in content
            finally:
                # Change back to original directory
                os.chdir(original_dir)


class TestDryRunMode:
    """Test dry run mode functionality."""
    
    def test_dry_run_flag(self, temp_settings_yml, mock_all_apis, runner):
        """Test that objects aren't created when --dry-run flag is used."""
        settings_path = temp_settings_yml
        
        # Run command with dry_run flag
        result = runner.invoke(
            app, 
            ["addresses", "--context", "folder", "--source", "test-folder", 
             "--destination", "test-dest-folder", "--settings-file", settings_path,
             "--dry-run"]
        )
        
        assert result.exit_code == 0
        
        # Verify that list calls were made but not create calls
        address_api = mock_all_apis["apis"]["address"]
        assert address_api["src"].list.call_count == 1
        assert address_api["dst"].list.call_count == 1
        assert address_api["dst"].create.call_count == 0