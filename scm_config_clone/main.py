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
    ike_gateways,
    ipsec_crypto_profiles,
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
# Configuration Commands
# ---------------------------------------------------------------------------------------------------------------------

# Address Groups
app.command(
    name="address-groups",
    help="Clone address groups between environments. Maintains hierarchical relationships.",
)(address_groups)

# Addresses
app.command(
    name="addresses",
    help="Clone IP, FQDN or range addresses between environments. Preserves all address properties.",
)(addresses)

# Anti-Spyware Profiles
app.command(
    name="anti-spyware-profiles",
    help="Clone anti-spyware security profiles with all threat exceptions and settings.",
)(anti_spyware_profiles)

# Application Filters
app.command(
    name="application-filters",
    help="Clone application filters with all filter criteria and configurations.",
)(application_filters)

# Application Groups
app.command(
    name="application-groups",
    help="Clone application groups with all member applications and nested groups.",
)(application_groups)

# Applications
app.command(
    name="applications",
    help="Clone custom application definitions with all properties and signatures.",
)(applications)

# Decryption Profiles
app.command(
    name="decryption-profiles",
    help="Clone SSL decryption profiles with all settings and exclusions.",
)(decryption_profiles)

# DNS Security Profiles
app.command(
    name="dns-security-profiles",
    help="Clone DNS Security profiles with all protections and whitelists.",
)(dns_security_profiles)

# Dynamic User Groups
app.command(
    name="dynamic-user-groups",
    help="Clone dynamic user groups with all membership criteria and settings.",
)(dynamic_user_groups)

# External Dynamic Lists
app.command(
    name="edls",
    help="Clone external dynamic lists with source URLs and update schedules.",
)(external_dynamic_lists)

# HIP Objects
app.command(
    name="hip-objects",
    help="Clone host information profile objects with all match criteria.",
)(hip_objects)

# HIP Profiles
app.command(
    name="hip-profiles",
    help="Clone HIP profiles with all associated HIP objects and match conditions.",
)(hip_profiles)

# HTTP Server Profiles
app.command(
    name="http-server-profiles",
    help="Clone HTTP server profiles with all header configurations and settings.",
)(http_server_profiles)

# IKE Crypto Profiles
app.command(
    name="ike-crypto-profiles",
    help="Clone IKE crypto profiles with encryption, authentication, and DH group settings.",
)(ike_crypto_profiles)

# IKE Gateways
app.command(
    name="ike-gateways",
    help="Clone IKE gateways with all authentication and connection settings.",
)(ike_gateways)

# IPsec Crypto Profiles
app.command(
    name="ipsec-crypto-profiles",
    help="Clone IPsec crypto profiles with encryption and authentication settings.",
)(ipsec_crypto_profiles)

# Log Forwarding Profiles
app.command(
    name="log-forwarding-profiles",
    help="Clone log forwarding profiles with all destinations and filtering rules.",
)(log_forwarding_profiles)

# NAT Rules
app.command(
    name="nat-rules",
    help="Clone network address translation rules with all source/destination settings.",
)(nat_rules)

# Quarantined Devices
app.command(
    name="quarantined-devices",
    help="Clone quarantined device definitions with associated policies and timeouts.",
)(quarantined_devices)

# Regions
app.command(
    name="regions",
    help="Clone region objects with all geographic specifications and IP ranges.",
)(regions)

# Remote Networks
app.command(
    name="remote-networks",
    help="Clone remote network objects between SASE tenants with all connection settings.",
)(remote_networks)

# Schedules
app.command(
    name="schedules",
    help="Clone schedule objects with all time specifications and recurrence settings.",
)(schedules)

# Security Rules
app.command(
    name="security-rules",
    help="Clone security policy rules with all source, destination, and action settings.",
)(security_rules)

# Service Groups
app.command(
    name="service-groups",
    help="Clone service groups with all member services and nested groups.",
)(service_groups)

# Services
app.command(
    name="services",
    help="Clone service definitions with protocol, port, and timeout settings.",
)(services)

# Syslog Server Profiles
app.command(
    name="syslog-server-profiles",
    help="Clone syslog server profiles with all server configurations and format settings.",
)(syslog_server_profiles)

# Tags
app.command(
    name="tags",
    help="Clone tags with colors and comments for object classification.",
)(tags)

# URL Categories
app.command(
    name="url-categories",
    help="Clone custom URL categories with all included URLs and settings.",
)(url_categories)

# Vulnerability Protection Profiles
app.command(
    name="vulnerability-profiles",
    help="Clone vulnerability protection profiles with all exception rules and severities.",
)(vulnerability_protection_profiles)

# Wildfire AV Profiles
app.command(
    name="wildfire-profiles",
    help="Clone Wildfire anti-virus profiles with all file type settings and actions.",
)(wildfire_antivirus_profiles)


if __name__ == "__main__":
    app()
