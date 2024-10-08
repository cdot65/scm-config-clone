# scm_config_clone/commands/clone_address_groups.py

import logging
import typer
from panapi.config.objects import AddressGroup

from scm_config_clone.config.settings import load_settings
from scm_config_clone.utilities.helpers import (
    authenticate_scm,
    create_scm_address_groups,
)

logger = logging.getLogger(__name__)

def clone_address_groups(
    settings_file: str = typer.Option(
        ".secrets.yaml",
        "--settings-file",
        "-s",
        help="Path to the settings YAML file.",
    ),
):
    """
    Clone address groups from the source to the destination SCM tenant.

    Authenticates with both source and destination tenants, retrieves address groups from the source,
    and creates them in the destination tenant.

    Args:
        settings_file (str): Path to the YAML settings file.

    Error:
        typer.Exit: Exits the application if an error occurs during the process.

    Return:
        None
    """
    typer.echo("Starting address groups migration...")

    # Load settings
    settings = load_settings(settings_file)

    # Authenticate with source tenant
    try:
        source_session = authenticate_scm(settings["source_scm"])
    except Exception as e:
        logger.error(f"Error authenticating with source tenant: {e}")
        raise typer.Exit(code=1)

    # Retrieve address groups from source
    try:
        folder = {"folder": settings["source_scm"]["folder"]}
        source_address_group = AddressGroup(**folder)
        address_groups = source_address_group.list(source_session)
        logger.info(f"Retrieved {len(address_groups)} address groups from source.")
    except Exception as e:
        logger.error(f"Error retrieving address groups from source: {e}")
        raise typer.Exit(code=1)

    # Authenticate with destination tenant
    try:
        destination_session = authenticate_scm(settings["destination_scm"])
    except Exception as e:
        logger.error(f"Error authenticating with destination tenant: {e}")
        raise typer.Exit(code=1)

    # Create address groups in destination
    try:
        created_groups = create_scm_address_groups(
            address_groups=address_groups,
            folder=settings["destination_scm"]["folder"],
            session=destination_session,
        )
        logger.info(
            f"Successfully created {len(created_groups)} address groups in destination."
        )
    except Exception as e:
        logger.error(f"Error creating address groups in destination: {e}")
        raise typer.Exit(code=1)

    typer.echo("Address groups migration completed successfully.")