"""
Unit tests for CLI commands.
"""

import pytest
from unittest.mock import patch, MagicMock
import typer
from typer.testing import CliRunner

from scm_config_clone.main import app
from tests.factories.model_factories import AddressResponseModelFactory, TagResponseModelFactory
from tests.factories.mock_client import MockScmApiFactory


class TestCLIBase:
    """Base class for CLI command tests."""
    
    @pytest.fixture
    def runner(self):
        """Return a CLI runner for testing commands."""
        return CliRunner()
    
    @pytest.fixture
    def mock_settings(self):
        """Mock settings for testing."""
        return {
            "source_scm": {
                "client_id": "test-src-id",
                "client_secret": "test-src-secret",
                "tenant": "test-src-tenant",
            },
            "destination_scm": {
                "client_id": "test-dst-id",
                "client_secret": "test-dst-secret",
                "tenant": "test-dst-tenant",
            },
            "logging": "INFO",
            "auto_approve": True,
            "create_report": False,
            "dry_run": True,
            "quiet": True,
        }


class TestAddressesCommand(TestCLIBase):
    """Tests for the addresses command."""
    
    @patch('scm_config_clone.commands.objects.address.Scm')
    @patch('scm_config_clone.commands.objects.address.Address')
    @patch('scm_config_clone.commands.objects.address.load_settings')
    def test_addresses_command_context_pattern(self, mock_load_settings, mock_address_api, mock_scm, runner, mock_settings):
        """Test address command with context pattern."""
        # Setup mocks
        mock_load_settings.return_value = mock_settings
        mock_source_client = MagicMock()
        mock_dest_client = MagicMock()
        mock_scm.side_effect = [mock_source_client, mock_dest_client]
        
        # Create mock objects
        source_objects = [
            AddressResponseModelFactory(name="address1", ip_netmask="10.0.0.1/32"),
            AddressResponseModelFactory(name="address2", ip_netmask="10.0.0.2/32"),
        ]
        
        # Setup Address API mock
        mock_source_api = MagicMock()
        mock_dest_api = MagicMock()
        mock_source_api.list.return_value = source_objects
        mock_dest_api.list.return_value = []  # No destination objects
        mock_address_api.side_effect = [mock_source_api, mock_dest_api, mock_dest_api]
        
        # Run the command
        result = runner.invoke(
            app, 
            ["addresses", "--context", "folder", "--source", "test-folder", 
             "--destination", "test-dest-folder", "--auto-approve"]
        )
        
        # Check the result
        assert result.exit_code == 0
        assert "Starting address objects cloning" in result.stdout
        
        # Verify the mock calls
        mock_source_api.list.assert_called_once()
        mock_dest_api.list.assert_called_once()
        assert mock_dest_api.create.call_count == 2  # Should create both addresses
    
    @patch('scm_config_clone.commands.objects.address.Scm')
    @patch('scm_config_clone.commands.objects.address.Address')
    @patch('scm_config_clone.commands.objects.address.load_settings')
    def test_addresses_command_legacy_pattern(self, mock_load_settings, mock_address_api, mock_scm, runner, mock_settings):
        """Test address command with legacy pattern."""
        # Setup mocks
        mock_load_settings.return_value = mock_settings
        mock_source_client = MagicMock()
        mock_dest_client = MagicMock()
        mock_scm.side_effect = [mock_source_client, mock_dest_client]
        
        # Create mock objects
        source_objects = [
            AddressResponseModelFactory(name="address1", ip_netmask="10.0.0.1/32"),
            AddressResponseModelFactory(name="address2", ip_netmask="10.0.0.2/32"),
        ]
        
        # Setup Address API mock
        mock_source_api = MagicMock()
        mock_dest_api = MagicMock()
        mock_source_api.list.return_value = source_objects
        mock_dest_api.list.return_value = []  # No destination objects
        mock_address_api.side_effect = [mock_source_api, mock_dest_api, mock_dest_api]
        
        # Run the command
        result = runner.invoke(
            app, 
            ["addresses", "--source-folder", "test-folder", 
             "--destination-folder", "test-dest-folder", "--auto-approve"]
        )
        
        # Check the result
        assert result.exit_code == 0
        assert "Starting address objects cloning" in result.stdout
        
        # Verify the mock calls
        mock_source_api.list.assert_called_once()
        mock_dest_api.list.assert_called_once()
        assert mock_dest_api.create.call_count == 2  # Should create both addresses


class TestTagsCommand(TestCLIBase):
    """Tests for the tags command."""
    
    @patch('scm_config_clone.commands.objects.tag.Scm')
    @patch('scm_config_clone.commands.objects.tag.Tag')
    @patch('scm_config_clone.commands.objects.tag.load_settings')
    def test_tags_command(self, mock_load_settings, mock_tag_api, mock_scm, runner, mock_settings):
        """Test tag command."""
        # Setup mocks
        mock_load_settings.return_value = mock_settings
        mock_source_client = MagicMock()
        mock_dest_client = MagicMock()
        mock_scm.side_effect = [mock_source_client, mock_dest_client]
        
        # Create mock objects
        source_objects = [
            TagResponseModelFactory(name="tag1", color="color1"),
            TagResponseModelFactory(name="tag2", color="color2"),
        ]
        
        # Setup Tag API mock
        mock_source_api = MagicMock()
        mock_dest_api = MagicMock()
        mock_source_api.list.return_value = source_objects
        mock_dest_api.list.return_value = []  # No destination objects
        mock_tag_api.side_effect = [mock_source_api, mock_dest_api, mock_dest_api]
        
        # Run the command
        result = runner.invoke(
            app, 
            ["tags", "--context", "folder", "--source", "test-folder", 
             "--destination", "test-dest-folder", "--auto-approve"]
        )
        
        # Check result code
        assert result.exit_code == 0


class TestIKECryptoProfilesCommand(TestCLIBase):
    """Tests for the ike-crypto-profiles command."""
    
    @patch('scm_config_clone.commands.network.ike_crypto_profile.Scm')
    @patch('scm_config_clone.commands.network.ike_crypto_profile.IKECryptoProfile')
    @patch('scm_config_clone.commands.network.ike_crypto_profile.load_settings')
    def test_ike_crypto_profiles_command(self, mock_load_settings, mock_api, mock_scm, runner, mock_settings):
        """Test IKE crypto profiles command."""
        # Setup mocks
        mock_load_settings.return_value = mock_settings
        mock_source_client = MagicMock()
        mock_dest_client = MagicMock()
        mock_scm.side_effect = [mock_source_client, mock_dest_client]
        
        # Create mock objects
        class IKEProfileFactory(TagResponseModelFactory):
            class Meta:
                class Fake:
                    def __init__(self, **kwargs):
                        self.__dict__.update(kwargs)
                model = Fake
            
            dh_group = ["group1", "group2"]
            authentication = ["sha1"]
            encryption = ["aes-128-cbc"]
            lifetime_seconds = 28800
        
        source_objects = [
            IKEProfileFactory(name="ike-profile1"),
            IKEProfileFactory(name="ike-profile2"),
        ]
        
        # Setup API mock
        mock_source_api = MagicMock()
        mock_dest_api = MagicMock()
        mock_source_api.list.return_value = source_objects
        mock_dest_api.list.return_value = []  # No destination objects
        mock_api.side_effect = [mock_source_api, mock_dest_api, mock_dest_api]
        
        # Run the command
        result = runner.invoke(
            app, 
            ["ike-crypto-profiles", "--context", "folder", "--source", "test-folder", 
             "--destination", "test-dest-folder", "--auto-approve"]
        )
        
        # Check result code
        assert result.exit_code == 0