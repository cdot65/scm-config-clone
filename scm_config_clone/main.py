# src/scm_config_clone/main.py

"""
SCM Config Clone CLI Application

This application provides commands to clone configuration objects from a source Strata Cloud Manager tenant to a destination tenant.

Commands:
- `address-objects`: Clone address objects.
- `address-groups`: Clone address groups.
- `auth`: Create authentication file.

Usage:
    scm-clone <command> [OPTIONS]
"""

import typer
import logging

from scm_config_clone.commands import (
    clone_address_objects,
    address_groups_cmd,
    create_secrets_file,
)

# Initialize Typer app
app = typer.Typer(
    name="scm-clone",
    help="Clone configuration from one Strata Cloud Manager tenant to another.",
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register commands
app.command()(clone_address_objects)
app.command()(address_groups_cmd)
app.command()(create_secrets_file)

if __name__ == "__main__":
    app()
