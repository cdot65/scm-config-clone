# scm_config_clone/utilities/helpers.py

import logging
from typing import Dict, List

from panapi import PanApiSession
from panapi.config.objects import Address, AddressGroup

logger = logging.getLogger(__name__)


def authenticate_scm(scm_info: Dict[str, str]) -> PanApiSession:
    """
    Authenticate with a Strata Cloud Manager tenant and return an API session.

    Args:
        scm_info (Dict[str, str]): SCM authentication details.

    Error:
        Exception: Raises an exception if authentication fails.

    Return:
        PanApiSession: An authenticated API session object.
    """
    session = PanApiSession()
    try:
        session.authenticate(
            client_id=scm_info["client_id"],
            client_secret=scm_info["client_secret"],
            scope=f"profile tsg_id:{scm_info['tenant']} email",
            token_url=scm_info["token_url"],
        )
        logger.info(
            f"Authenticated with Strata Cloud Manager tenant {scm_info['tenant']}"
        )
        return session
    except Exception as e:
        logger.error(f"Error with Prisma authentication: {e}")
        raise


def create_scm_address_objects(
    address_objects: List[Address],
    folder: str,
    session: PanApiSession,
) -> List[Dict[str, str]]:
    """
    Create address objects in the destination SCM tenant.

    Iterates over address objects and creates them in the specified folder of the destination tenant.

    Args:
        address_objects (List[Address]): List of address objects to create.
        folder (str): Folder name in the destination tenant.
        session (PanApiSession): Authenticated API session for the destination tenant.

    Error:
        Exception: Raises an exception if creation fails.

    Return:
        List[Dict[str, str]]: List of created address objects data.
    """
    scm_address_objects = []

    for address_object in address_objects:
        # Extract attributes
        scm_address_data = {
            "name": address_object.name,
            "folder": folder,
        }

        # Optional fields
        if getattr(address_object, "description", None):
            scm_address_data["description"] = address_object.description

        # Determine address type
        if getattr(address_object, "ip_netmask", None):
            scm_address_data["ip_netmask"] = address_object.ip_netmask
        elif getattr(address_object, "fqdn", None):
            scm_address_data["fqdn"] = address_object.fqdn
        elif getattr(address_object, "ip_range", None):
            scm_address_data["ip_range"] = address_object.ip_range
        else:
            logger.warning(
                f"Address object {address_object.name} has no valid address type."
            )
            continue

        logger.debug(f"Processing scm_address_data: {scm_address_data}.")

        # Create address object
        try:
            scm_address = Address(**scm_address_data)
            scm_address.create(session)
            scm_address_objects.append(scm_address_data)
            logger.info(f"Created address object {address_object.name}")
        except Exception as e:
            logger.error(f"Error creating address object {address_object.name}: {e}")
            raise

    return scm_address_objects


def create_scm_address_groups(
    address_groups: List[AddressGroup],
    folder: str,
    session: PanApiSession,
) -> List[Dict[str, str]]:
    """
    Create address groups in the destination SCM tenant.

    Iterates over address groups and creates them in the specified folder of the destination tenant.

    Args:
        address_groups (List[AddressGroup]): List of address groups to create.
        folder (str): Folder name in the destination tenant.
        session (PanApiSession): Authenticated API session for the destination tenant.

    Error:
        Exception: Raises an exception if creation fails.

    Return:
        List[Dict[str, str]]: List of created address groups data.
    """
    scm_address_groups = []

    for address_group in address_groups:
        logger.debug(f"Processing address group: {address_group.name}")

        scm_address_group_data = {
            "folder": folder,
            "name": address_group.name,
        }

        # Optional fields
        if getattr(address_group, "description", None):
            scm_address_group_data["description"] = address_group.description

        # Handle static and dynamic groups
        if getattr(address_group, "static", None):
            scm_address_group_data["static"] = list(address_group.static)
        elif getattr(address_group, "dynamic", None):
            scm_address_group_data["dynamic"] = {
                "filter": address_group.dynamic["filter"]
            }
        else:
            logger.warning(
                f"Address group {address_group.name} has no valid type (static or dynamic)."
            )
            continue

        # Create address group
        try:
            scm_address_group = AddressGroup(**scm_address_group_data)
            scm_address_group.create(session)
            scm_address_groups.append(scm_address_group_data)
            logger.info(f"Created address group {address_group.name}")
        except Exception as e:
            logger.error(f"Error creating address group {address_group.name}: {e}")
            raise

    return scm_address_groups
