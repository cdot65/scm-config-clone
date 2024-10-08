# scm_config_clone/commands/clone_address_objects.py

import typer
import logging
from pathlib import Path

from scm_config_clone.utilities.helpers import (
    authenticate_scm,
    create_scm_address_objects,
)
from scm_config_clone.config.settings import load_settings
from panapi.config.objects import Address

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
    Clone address objects from the source to the destination SCM tenant.

    Authenticates with both source and destination tenants, retrieves address objects from the source,
    and creates them in the destination tenant.

    Args:
        settings_file (str): Path to the YAML settings file.

    Error:
        typer.Exit: Exits the application if an error occurs during the process.

    Return:
        None
    """
    typer.echo("Starting address objects migration...")

    # Load settings
    settings = load_settings(settings_file)

    # Authenticate with source tenant
    try:
        source_session = authenticate_scm(settings["source_scm"])
    except Exception as e:
        logger.error(f"Error authenticating with source tenant: {e}")
        raise typer.Exit(code=1)

    # Retrieve address objects from source
    try:
        folder = {"folder": settings["source_scm"]["folder"]}
        source_address = Address(**folder)
        address_objects = source_address.list(source_session)
        logger.info(f"Retrieved {len(address_objects)} address objects from source.")
    except Exception as e:
        logger.error(f"Error retrieving address objects from source: {e}")
        raise typer.Exit(code=1)

    # Authenticate with destination tenant
    try:
        destination_session = authenticate_scm(settings["destination_scm"])
    except Exception as e:
        logger.error(f"Error authenticating with destination tenant: {e}")
        raise typer.Exit(code=1)

    # Create address objects in destination
    try:
        created_objects = create_scm_address_objects(
            address_objects=address_objects,
            folder=settings["destination_scm"]["folder"],
            session=destination_session,
        )
        logger.info(
            f"Successfully created {len(created_objects)} address objects in destination."
        )
    except Exception as e:
        logger.error(f"Error creating address objects in destination: {e}")
        raise typer.Exit(code=1)

    typer.echo("Address objects migration completed successfully.")
