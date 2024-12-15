# scm_config_clone/utilities/settings.py

import logging
from typing import Dict, Any

import typer
import yaml

logger = logging.getLogger(__name__)


def load_settings(settings_file: str) -> Dict[str, Any]:
    """
    Load configuration settings from a YAML file.

    This function reads the provided YAML settings file (e.g., "settings.yaml") and
    extracts the following information:
    - Source and destination SCM configurations (client_id, client_secret, tenant).
    - Logging level.
    - Additional boolean options: auto_approve, create_report, dry_run, quiet.

    The returned dictionary is structured as follows:
    {
        "source_scm": {
            "client_id": str,
            "client_secret": str,
            "tenant": str
        },
        "destination_scm": {
            "client_id": str,
            "client_secret": str,
            "tenant": str
        },
        "logging": str,
        "auto_approve": bool,
        "create_report": bool,
        "dry_run": bool,
        "quiet": bool
    }

    Args:
        settings_file (str): Path to the YAML settings file containing SCM credentials
                             and configuration.

    Raises:
        typer.Exit: If an error occurs during file reading or parsing, the function
                    logs the error and exits.

    Returns:
        Dict[str, Any]: A dictionary containing all relevant configuration keys
                        required by the CLI.
    """
    try:
        with open(settings_file, "r") as f:
            data = yaml.safe_load(f) or {}

        # Safely retrieve nested keys with defaults
        source = data.get("oauth", {}).get("source", {})
        destination = data.get("oauth", {}).get("destination", {})

        # Construct the dictionary
        config = {
            "source_scm": {
                "client_id": source.get("client_id"),
                "client_secret": source.get("client_secret"),
                "tenant": source.get("tsg"),
            },
            "destination_scm": {
                "client_id": destination.get("client_id"),
                "client_secret": destination.get("client_secret"),
                "tenant": destination.get("tsg"),
            },
            "logging": data.get("logging", "INFO"),
            "auto_approve": data.get("auto_approve", False),
            "create_report": data.get("create_report", False),
            "dry_run": data.get("dry_run", False),
            "quiet": data.get("quiet", False),
        }

        return config

    except Exception as e:
        logger.error(f"Error loading settings from {settings_file}: {e}")
        typer.echo(
            f"❌ Error loading configuration. Please check that '{settings_file}' is accessible and properly formatted."
        )
        raise typer.Exit(code=1)
