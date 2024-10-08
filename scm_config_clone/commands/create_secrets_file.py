# scm_config_clone/commands/create_secrets_file.py

import typer
import logging
import yaml

logger = logging.getLogger(__name__)


def create_secrets_file(
    output_file: str = typer.Option(
        ".secrets.yaml",
        "--output-file",
        "-o",
        help="Path to the output settings file.",
    ),
):
    """
    Create an authentication file (.secrets.yaml) with SCM credentials.

    Prompts the user for source and destination SCM credentials and writes them to a YAML file.

    Args:
        output_file (str): Path to the output settings YAML file.

    Error:
        typer.Exit: Exits the application if an error occurs during file writing.

    Return:
        None
    """
    typer.echo("Creating authentication file...")

    # Prompt user for credentials
    typer.echo("Enter source Strata Cloud Manager credentials:")
    source_client_id = typer.prompt("Source Client ID")
    source_client_secret = typer.prompt("Source Client Secret", hide_input=True)
    source_tsg = typer.prompt("Source Tenant TSG")
    source_folder = typer.prompt("Source Folder", default="Prisma Access")

    typer.echo("Enter destination Strata Cloud Manager credentials:")
    dest_client_id = typer.prompt("Destination Client ID")
    dest_client_secret = typer.prompt("Destination Client Secret", hide_input=True)
    dest_tsg = typer.prompt("Destination Tenant TSG")
    dest_folder = typer.prompt("Destination Folder", default="Prisma Access")

    token_url = typer.prompt(
        "Token URL",
        default="https://auth.apps.paloaltonetworks.com/oauth2/access_token",
    )

    # Build data dictionary
    data = {
        "oauth": {
            "token_url": token_url,
            "source": {
                "client_id": source_client_id,
                "client_secret": source_client_secret,
                "tsg": source_tsg,
                "folder": source_folder,
            },
            "destination": {
                "client_id": dest_client_id,
                "client_secret": dest_client_secret,
                "tsg": dest_tsg,
                "folder": dest_folder,
            },
        }
    }

    # Write to YAML file
    try:
        with open(output_file, "w") as f:
            yaml.dump(data, f)
        logger.info(f"Authentication file written to {output_file}")
    except Exception as e:
        logger.error(f"Error writing authentication file: {e}")
        raise typer.Exit(code=1)

    typer.echo("Authentication file created successfully.")
