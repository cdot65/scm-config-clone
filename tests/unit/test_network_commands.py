"""
Unit tests for network-related commands.
"""

import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from scm_config_clone.main import app


class TestIKECryptoProfilesCommand:
    """Tests for the IKE crypto profiles command."""
    
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
            "dry_run": False,
            "quiet": True,
        }
    
    @pytest.fixture
    def runner(self):
        """Return a CLI runner for testing commands."""
        return CliRunner()
    
    @patch('scm_config_clone.commands.network.ike_crypto_profile.Scm')
    @patch('scm_config_clone.commands.network.ike_crypto_profile.IKECryptoProfile')
    @patch('scm_config_clone.commands.network.ike_crypto_profile.load_settings')
    def test_ike_crypto_profiles_basic(self, mock_load_settings, mock_api, mock_scm, runner, mock_settings):
        """Test basic IKE crypto profiles cloning."""
        # Setup mocks
        mock_load_settings.return_value = mock_settings
        mock_source_client = MagicMock()
        mock_dest_client = MagicMock()
        mock_scm.side_effect = [mock_source_client, mock_dest_client]
        
        # Create mock objects
        class FakeIKEProfile:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
        
        source_objects = [
            FakeIKEProfile(
                name="test-ike-profile1",
                description="Test IKE Profile 1",
                folder="test-folder",
                dh_group=["group1", "group2"],
                authentication=["sha1"],
                encryption=["aes-128-cbc"],
                lifetime_seconds=28800,
            ),
            FakeIKEProfile(
                name="test-ike-profile2",
                description="Test IKE Profile 2",
                folder="test-folder",
                dh_group=["group14"],
                authentication=["sha256"],
                encryption=["aes-256-cbc"],
                lifetime_seconds=3600,
            ),
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
        
        # Check result
        assert result.exit_code == 0
        
        # Verify API calls
        mock_source_api.list.assert_called_once()
        assert mock_dest_api.create.call_count == 2
        
        # Check create parameters for first profile
        create_calls = mock_dest_api.create.call_args_list
        first_call_args = create_calls[0][0][0]
        
        assert "dh_group" in first_call_args
        assert "authentication" in first_call_args
        assert "encryption" in first_call_args
        assert "lifetime_seconds" in first_call_args
        assert "name" in first_call_args


class TestIKEGatewayCommand:
    """Tests for the IKE gateway command."""
    
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
            "dry_run": False,
            "quiet": True,
        }
    
    @pytest.fixture
    def runner(self):
        """Return a CLI runner for testing commands."""
        return CliRunner()
    
    @patch('scm_config_clone.commands.network.ike_gateway.Scm')
    @patch('scm_config_clone.commands.network.ike_gateway.IKEGateway')
    @patch('scm_config_clone.commands.network.ike_gateway.load_settings')
    def test_ike_gateway_basic(self, mock_load_settings, mock_api, mock_scm, runner, mock_settings):
        """Test basic IKE gateway cloning."""
        # Setup mocks
        mock_load_settings.return_value = mock_settings
        mock_source_client = MagicMock()
        mock_dest_client = MagicMock()
        mock_scm.side_effect = [mock_source_client, mock_dest_client]
        
        # Create mock objects
        class FakeGateway:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
        
        source_objects = [
            FakeGateway(
                name="test-gateway1",
                description="Test Gateway 1",
                folder="test-folder",
                version="ikev2",
                interface="ethernet1/1",
                local_ip_address="10.0.0.1",
                peer_ip_address="20.0.0.1",
                preshared_key="test-key",
                local_id_type="ipaddr",
                local_id_value="10.0.0.1",
                peer_id_type="ipaddr",
                peer_id_value="20.0.0.1",
                ike_crypto_profile="test-ike-profile1",
            ),
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
            ["ike-gateways", "--context", "folder", "--source", "test-folder", 
             "--destination", "test-dest-folder", "--auto-approve"]
        )
        
        # Check result
        assert result.exit_code == 0
        
        # Verify API calls
        mock_source_api.list.assert_called_once()
        assert mock_dest_api.create.call_count == 1


class TestIPSecCryptoProfileCommand:
    """Tests for the IPSec crypto profiles command."""
    
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
            "dry_run": False,
            "quiet": True,
        }
    
    @pytest.fixture
    def runner(self):
        """Return a CLI runner for testing commands."""
        return CliRunner()
    
    @patch('scm_config_clone.commands.network.ipsec_crypto_profile.Scm')
    @patch('scm_config_clone.commands.network.ipsec_crypto_profile.IPSecCryptoProfile')
    @patch('scm_config_clone.commands.network.ipsec_crypto_profile.load_settings')
    def test_ipsec_crypto_profiles_basic(self, mock_load_settings, mock_api, mock_scm, runner, mock_settings):
        """Test basic IPSec crypto profiles cloning."""
        # Setup mocks
        mock_load_settings.return_value = mock_settings
        mock_source_client = MagicMock()
        mock_dest_client = MagicMock()
        mock_scm.side_effect = [mock_source_client, mock_dest_client]
        
        # Create mock objects
        class FakeIPSecProfile:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
        
        source_objects = [
            FakeIPSecProfile(
                name="test-ipsec-profile1",
                description="Test IPSec Profile 1",
                folder="test-folder",
                esp_encryption=["aes-128-cbc"],
                esp_authentication=["sha1"],
                ah_authentication=None,
                dh_group="group2",
                lifetime_seconds=3600,
                lifetime_kilobytes=None,
            ),
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
            ["ipsec-crypto-profiles", "--context", "folder", "--source", "test-folder", 
             "--destination", "test-dest-folder", "--auto-approve"]
        )
        
        # Check result
        assert result.exit_code == 0
        
        # Verify API calls
        mock_source_api.list.assert_called_once()
        assert mock_dest_api.create.call_count == 1