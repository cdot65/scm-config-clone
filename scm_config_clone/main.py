# scm_config_clone/main.py

"""
SCM Config Clone CLI Application

Provides commands to clone configuration objects between SCM tenants.

Commands:
- `addresses`: Clone address objects.
- `settings`: Create settings file.
- `tags`: Clone tag objects from source to destination tenant, focusing on a specific folder.

Usage:
    scm-clone <command> [OPTIONS]
"""

import logging

import typer

from scm_config_clone import (
    addresses,
    create_settings,
    tags,
)

# Initialize Typer app
app = typer.Typer(
    name="scm-clone",
    help="Clone configuration from one Strata Cloud Manager tenant to another.",
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register commands with explicit names and help text
app.command(
    name="settings",
    help="Create a YAML file containing the settings of our SCM cloning job (required for authentication).",
)(create_settings)

app.command(
    name="addresses",
    help="Clone address objects from the source SCM tenant to the destination SCM tenant.",
)(addresses)

app.command(
    name="tags",
    help="Clone tag objects from the source SCM tenant to the destination SCM tenant, filtered by the specified folder.",
)(tags)

if __name__ == "__main__":
    app()
