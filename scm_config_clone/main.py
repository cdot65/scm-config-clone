# scm_config_clone/main.py

"""
SCM Config Clone CLI Application

Provides commands to clone configuration objects between SCM tenants.

Commands:
- `addresses`: Clone address objects.
- `settings`: Create settings file.
- `tags`: Clone tag objects from source to destination tenant, focusing on a specific folder.
- `remote-networks`: Clone remote network objects from source to destination tenant.

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
    dynamic_user_groups,
    external_dynamic_lists,
    hip_objects,
    hip_profiles,
    http_server_profiles,
    ike_crypto_profiles,
    log_forwarding_profiles,
    nat_rules,
    quarantined_devices,
    regions,
    remote_networks,
    schedules,
    security_rules,
    services,
    service_groups,
    syslog_server_profiles,
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

# HIP Profiles
app.command(
    name="hip-profiles",
    help="Clone HIP profiles.",
)(hip_profiles)

# NAT Rules
app.command(
    name="nat-rules",
    help="Clone NAT rules.",
)(nat_rules)

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

# Dynamic User Groups
app.command(
    name="dynamic-user-groups",
    help="Clone dynamic user groups.",
)(dynamic_user_groups)

# HTTP Server Profiles
app.command(
    name="http-server-profiles",
    help="Clone HTTP server profiles.",
)(http_server_profiles)

# Log Forwarding Profiles
app.command(
    name="log-forwarding-profiles",
    help="Clone log forwarding profiles.",
)(log_forwarding_profiles)

# Syslog Server Profiles
app.command(
    name="syslog-server-profiles",
    help="Clone syslog server profiles.",
)(syslog_server_profiles)

# Quarantined Devices
app.command(
    name="quarantined-devices",
    help="Clone quarantined devices.",
)(quarantined_devices)

# Region Objects
app.command(
    name="regions",
    help="Clone region objects.",
)(regions)

# Schedule Objects
app.command(
    name="schedules",
    help="Clone schedule objects.",
)(schedules)

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

# ---------------------------------------------------------------------------------------------------------------------
# Network Services
# ---------------------------------------------------------------------------------------------------------------------

# IKE Crypto Profiles
app.command(
    name="ike-crypto-profiles",
    help="Clone IKE crypto profiles.",
)(ike_crypto_profiles)

# IKE Gateways
app.command(
    name="ike-gateways",
    help="Clone IKE gateways.",
)(ike_gateways)

# IPsec Crypto Profiles
app.command(
    name="ipsec-crypto-profiles",
    help="Clone IPsec crypto profiles.",
)(ipsec_crypto_profiles)

# ---------------------------------------------------------------------------------------------------------------------
# Deployments
# ---------------------------------------------------------------------------------------------------------------------

# Remote Networks
app.command(
    name="remote-networks",
    help="Clone remote network objects between SASE tenants.",
)(remote_networks)


if __name__ == "__main__":
    app()
