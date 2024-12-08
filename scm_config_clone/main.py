# scm_config_clone/main.py

"""
SCM Config Clone CLI Application

Provides commands to clone configuration objects between SCM tenants.

Commands:
- `clone-address-objects`: Clone address objects.
- `create-secrets-file`: Create authentication file.

Usage:
    scm-clone <command> [OPTIONS]
"""

import typer
import logging

from scm_config_clone.commands.create_secrets_file import create_secrets_file
from scm_config_clone.commands.objects import clone_address_objects

# Initialize Typer app
app = typer.Typer(
    name="scm-clone",
    help="Clone configuration from one Strata Cloud Manager tenant to another.",
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register commands with clearer parameters
app.command(
    name="create-secrets-file",
    help="Create a YAML file containing SCM authentication details.",
)(create_secrets_file)

app.command(
    name="clone-address-objects",
    help="Clone address objects from the source SCM tenant to the destination SCM tenant.",
)(clone_address_objects)

if __name__ == "__main__":
    app()
