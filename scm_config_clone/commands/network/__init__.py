# scm_config_clone/commands/network/__init__.py

"""
Network command modules.

This package contains modules for cloning network-related objects 
between Strata Cloud Manager tenants.
"""

from scm_config_clone.commands.network.ike_crypto_profile import clone as ike_crypto_profile
from scm_config_clone.commands.network.ike_gateway import clone as ike_gateway
from scm_config_clone.commands.network.ipsec_crypto_profile import clone as ipsec_crypto_profile
from scm_config_clone.commands.network.nat_rule import clone as nat_rule

__all__ = [
    "ike_crypto_profile",
    "ike_gateway",
    "ipsec_crypto_profile",
    "nat_rule",
]