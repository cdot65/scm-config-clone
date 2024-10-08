# scm_config_clone/commands/clone_security_profile_groups.py

import typer
import logging

from scm_config_clone.utilities.helpers import (
    authenticate_scm,
    create_scm_security_profile_groups,
)
from scm_config_clone.config.settings import load_settings
from panapi.config.security import ProfileGroup

logger = logging.getLogger(__name__)


def clone_security_profile_groups(
    settings_file: str = typer.Option(
        ".secrets.yaml",
        "--settings-file",
        "-s",
        help="Path to the settings YAML file.",
    ),
):
    """
    Clone security profile groups from the source to the destination SCM tenant.

    Authenticates with both source and destination tenants, retrieves security profile groups from the source,
    and creates them in the destination tenant.

    Args:
        settings_file (str): Path to the YAML settings file.

    Error:
        typer.Exit: Exits the application if an error occurs during the process.

    Return:
        None
    """
    typer.echo("Starting security profile groups migration...")

    # Load settings
    settings = load_settings(settings_file)

    # Authenticate with source tenant
    try:
        source_session = authenticate_scm(settings["source_scm"])
    except Exception as e:
        logger.error(f"Error authenticating with source tenant: {e}")
        raise typer.Exit(code=1)

    # Retrieve security profile groups from source
    try:
        folder = {"folder": settings["source_scm"]["folder"]}
        source_profile_group = ProfileGroup(**folder)
        profile_groups = source_profile_group.list(source_session)
        logger.info(f"Retrieved {len(profile_groups)} security profile groups from source.")
    except Exception as e:
        logger.error(f"Error retrieving security profile groups from source: {e}")
        raise typer.Exit(code=1)

    # Authenticate with destination tenant
    try:
        destination_session = authenticate_scm(settings["destination_scm"])
    except Exception as e:
        logger.error(f"Error authenticating with destination tenant: {e}")
        raise typer.Exit(code=1)

    # Create security profile groups in destination
    try:
        created_profile_groups = create_scm_security_profile_groups(
            profile_groups=profile_groups,
            folder=settings["destination_scm"]["folder"],
            session=destination_session,
        )
        logger.info(
            f"Successfully created {len(created_profile_groups)} security profile groups in destination."
        )
    except Exception as e:
        logger.error(f"Error creating security profile groups in destination: {e}")
        raise typer.Exit(code=1)

    typer.echo("Security profile groups migration completed successfully.")
