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
    address_groups,
    applications,
    application_filters,
    application_groups,
    external_dynamic_lists,
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

# ---------------------------------------------------------------------------------------------------------------------
# scm-clone Configuration
# ---------------------------------------------------------------------------------------------------------------------

# Create a `settings.yaml` file with configuration needed to accomplish our tasks (required one-time setup)
app.command(
    name="settings",
    help="Create a `settings.yaml` file with configuration needed to accomplish our tasks (required one-time setup).",
)(create_settings)

# ---------------------------------------------------------------------------------------------------------------------
# Objects
# ---------------------------------------------------------------------------------------------------------------------

# Addresses
app.command(
    name="addresses",
    help="Clone addresses.",
)(addresses)

# Address Groups
app.command(
    name="address-groups",
    help="Clone address groups.",
)(address_groups)

# Applications
app.command(
    name="applications",
    help="Clone applications.",
)(applications)

# Application Filters
app.command(
    name="application-filters",
    help="Clone application filters.",
)(application_filters)

# Application Groups
app.command(
    name="application-groups",
    help="Clone application groups.",
)(application_groups)

# External Dynamic Lists
app.command(
    name="edls",
    help="Clone external dynamic lists.",
)(external_dynamic_lists)

# Tags
app.command(
    name="tags",
    help="Clone tags.",
)(tags)

# ---------------------------------------------------------------------------------------------------------------------
# Security Services
# ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app()
