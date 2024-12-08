# scm_config_clone/commands/objects/address.py

import typer
import logging
from typing import List

from scm.client import Scm
from scm.config.objects import Address
from scm.exceptions import (
    AuthenticationError,
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError,
)
from scm_config_clone.utilities.settings import load_settings

logger = logging.getLogger(__name__)


def clone_address_objects(
    settings_file: str = typer.Option(
        ".secrets.yaml",
        "--settings-file",
        "-s",
        help="Path to the settings YAML file.",
    ),
):
    """
    Clone address objects from the source to the destination SCM tenant using the pan-scm-sdk.

    Steps:
    1. Load SCM settings from a YAML file.
    2. Authenticate with both source and destination tenants using provided credentials.
    3. Retrieve all address objects from the source tenant.
    4. Create these address objects in the destination tenant.
    5. Commit the changes on the destination tenant.

    Args:
        settings_file (str): Path to the YAML settings file.

    Errors:
        typer.Exit: Exits the CLI if authentication, retrieval, creation, or commit fails.
    """
    typer.echo("Starting address objects migration...")

    # Load settings
    settings = load_settings(settings_file)

    # --- Authenticate with source tenant ---
    try:
        source_creds = settings["source_scm"]
        source_client = Scm(
            client_id=source_creds["client_id"],
            client_secret=source_creds["client_secret"],
            tsg_id=source_creds["tsg_id"],
            log_level="INFO",
        )
        logger.info(f"Authenticated with source SCM tenant: {source_creds['tsg_id']}")
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with source tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with source authentication: {e}")
        raise typer.Exit(code=1)

    # --- Retrieve address objects from source ---
    try:
        source_addresses = Address(source_client)
        source_folder = source_creds["folder"]
        address_objects = source_addresses.list(folder=source_folder)
        logger.info(
            f"Retrieved {len(address_objects)} address objects from source tenant."
        )
    except Exception as e:
        logger.error(f"Error retrieving address objects from source: {e}")
        raise typer.Exit(code=1)

    # --- Authenticate with destination tenant ---
    try:
        dest_creds = settings["destination_scm"]
        destination_client = Scm(
            client_id=dest_creds["client_id"],
            client_secret=dest_creds["client_secret"],
            tsg_id=dest_creds["tsg_id"],
            log_level="INFO",
        )
        logger.info(
            f"Authenticated with destination SCM tenant: {dest_creds['tsg_id']}"
        )
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with destination tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with destination authentication: {e}")
        raise typer.Exit(code=1)

    # --- Create address objects in the destination ---
    destination_addresses = Address(destination_client)
    destination_folder = dest_creds["folder"]

    created_objects: List[str] = []
    for src_obj in address_objects:
        # Build create parameters based on source object's attributes
        create_params = {
            "name": src_obj.name,
            "folder": destination_folder,
            "description": getattr(src_obj, "description", None),
            "tag": getattr(src_obj, "tag", []),
        }

        # Determine the address type and assign the appropriate field
        if getattr(src_obj, "ip_netmask", None):
            create_params["ip_netmask"] = src_obj.ip_netmask
        elif getattr(src_obj, "fqdn", None):
            create_params["fqdn"] = src_obj.fqdn
        elif getattr(src_obj, "ip_range", None):
            create_params["ip_range"] = src_obj.ip_range
        elif getattr(src_obj, "ip_wildcard", None):
            create_params["ip_wildcard"] = src_obj.ip_wildcard
        else:
            # If no recognizable address type is found, skip this object
            logger.warning(
                f"Skipping {src_obj.name}: No valid address type (ip_netmask, fqdn, ip_range, ip_wildcard)."
            )
            continue

        # Create the address object
        try:
            new_obj = destination_addresses.create(create_params)
            created_objects.append(new_obj.name)
            logger.info(f"Created address object in destination: {new_obj.name}")
        except (
            InvalidObjectError,
            MissingQueryParameterError,
            NameNotUniqueError,
            ObjectNotPresentError,
        ) as e:
            logger.error(
                f"Error creating address object {src_obj.name} in destination: {e}"
            )
            # Decide whether to continue or exit; continuing for now
            continue
        except Exception as e:
            logger.error(
                f"Unexpected error creating address object {src_obj.name} in destination: {e}"
            )
            continue

    # --- Commit changes on destination ---
    if created_objects:
        try:
            commit_params = {
                "folders": [destination_folder],
                "description": "Cloned address objects",
                "sync": True,
            }
            result = destination_addresses.commit(**commit_params)
            job_status = destination_addresses.get_job_status(result.job_id)
            logger.info(
                f"Commit job ID {result.job_id} status: {job_status.data[0].status_str}"
            )
        except Exception as e:
            logger.error(f"Error committing address objects in destination: {e}")
            raise typer.Exit(code=1)
    else:
        logger.info("No new address objects were created, skipping commit.")

    typer.echo("Address objects migration completed successfully.")
