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
    anti_spyware_profiles,
    applications,
    application_filters,
    application_groups,
    create_settings,
    decryption_profiles,
    dns_security_profiles,
    external_dynamic_lists,
    hip_objects,
    security_rules,
    services,
    service_groups,
    tags,
    url_categories,
    vulnerability_protection_profiles,
    wildfire_antivirus_profiles,
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

# HIP Objects
app.command(
    name="hip-objects",
    help="Clone hip objects.",
)(hip_objects)

# Services
app.command(
    name="services",
    help="Clone services.",
)(services)

# Service Groups
app.command(
    name="service-groups",
    help="Clone service groups.",
)(service_groups)

# Tags
app.command(
    name="tags",
    help="Clone tags.",
)(tags)

# ---------------------------------------------------------------------------------------------------------------------
# Security Services
# ---------------------------------------------------------------------------------------------------------------------

# Anti-Spyware Profiles
app.command(
    name="anti-spyware-profiles",
    help="Clone anti-spyware profiles.",
)(anti_spyware_profiles)


# Decryption Profiles
app.command(
    name="decryption-profiles",
    help="Clone decryption profiles.",
)(decryption_profiles)

# DNS Security Profiles
app.command(
    name="dns-security-profiles",
    help="Clone DNS Security profiles.",
)(dns_security_profiles)

# Security Rules
app.command(
    name="security-rules",
    help="Clone security rules.",
)(security_rules)

# URL Categories Rules
app.command(
    name="url-categories",
    help="Clone URL categories.",
)(url_categories)

# Vulnerability Protection Profiles
app.command(
    name="vulnerability-profiles",
    help="Clone vulnerability protection profiles.",
)(vulnerability_protection_profiles)

# Wildfire AV Profiles
app.command(
    name="wildfire-profiles",
    help="Clone Wildfire AV profiles.",
)(wildfire_antivirus_profiles)


if __name__ == "__main__":
    app()
