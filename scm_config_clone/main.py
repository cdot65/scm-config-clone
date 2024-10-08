# scm_config_clone/main.py

"""
SCM Config Clone CLI Application

Provides commands to clone configuration objects between SCM tenants.

Commands:
- `clone-address-objects`: Clone address objects.
- `clone-address-groups`: Clone address groups.
- `create-secrets-file`: Create authentication file.

Usage:
    scm-clone <command> [OPTIONS]
"""

import typer
import logging

from scm_config_clone.commands import (
    clone_address_objects,
    clone_address_groups,
    clone_security_profile_groups,
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
app.command()(clone_address_groups)
app.command()(clone_security_profile_groups)
app.command()(create_secrets_file)

if __name__ == "__main__":
    app()
