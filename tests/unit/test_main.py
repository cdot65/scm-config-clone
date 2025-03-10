"""
Tests for the main CLI application.
"""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch

from scm_config_clone.main import app


@pytest.fixture
def runner():
    """Return a CLI runner for testing commands."""
    return CliRunner()


class TestMainApp:
    """Tests for the main Typer app."""
    
    def test_app_help(self, runner):
        """Test that the app help message displays correctly."""
        result = runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        assert "Usage:" in result.stdout
        assert "Clone configuration from one Strata Cloud Manager tenant to another." in result.stdout
    
    def test_app_version(self, runner):
        """Test that the app version command works."""
        with patch('typer.echo') as mock_echo:
            result = runner.invoke(app, ["--version"])
            
            assert result.exit_code == 0
    
    def test_all_commands_exist(self, runner):
        """Test that all expected commands are registered."""
        result = runner.invoke(app, ["--help"])
        
        # Check for object commands
        assert "addresses" in result.stdout
        assert "address-groups" in result.stdout
        assert "tags" in result.stdout
        assert "applications" in result.stdout
        
        # Check for network commands
        assert "nat-rules" in result.stdout
        assert "ike-crypto-profiles" in result.stdout
        assert "ike-gateways" in result.stdout
        assert "ipsec-crypto-profiles" in result.stdout
        
        # Check for security commands
        assert "security-rules" in result.stdout
        assert "anti-spyware-profiles" in result.stdout
        
        # Check for deployment commands
        assert "remote-networks" in result.stdout
        
        # Check for utility commands
        assert "settings" in result.stdout
    
    @patch('scm_config_clone.commands.utilities.create_settings_file.create_settings')
    def test_settings_command(self, mock_create_settings, runner):
        """Test that the settings command is properly wired up."""
        result = runner.invoke(app, ["settings"])
        
        assert result.exit_code == 0
        mock_create_settings.assert_called_once()
    
    @patch('scm_config_clone.main.addresses')
    def test_addresses_command(self, mock_addresses, runner):
        """Test that the addresses command is properly wired up."""
        result = runner.invoke(app, ["addresses"])
        
        assert result.exit_code == 0
        mock_addresses.assert_called_once()
    
    @patch('scm_config_clone.main.remote_networks')
    def test_remote_networks_command(self, mock_remote_networks, runner):
        """Test that the remote-networks command is properly wired up."""
        result = runner.invoke(app, ["remote-networks"])
        
        assert result.exit_code == 0
        mock_remote_networks.assert_called_once()