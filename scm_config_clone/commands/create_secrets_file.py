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
    typer.echo("*" * 79 + "\nCreating authentication file called .secrets.yaml in the current directory\n")

    # Prompt user for credentials
    typer.echo("-" * 79 + "\n\tEnter source SCM credentials (where are you cloning from?)\n" + "-" * 79)
    source_client_id = typer.prompt(
        default="example@1234567890.iam.panserviceaccount.com",
        text="Source SCM Client ID\n",
        show_default=True,
    )
    source_client_secret = typer.prompt(
        default="12345678-1234-1234-1234-123456789012",
        hide_input=True,
        show_default=True,
        text="Source SCM Client Secret (input hidden)\n",
    )
    source_tsg = typer.prompt(
        default="1234567890",
        show_default=True,
        text="Source SCM Tenant TSG ID\n",
    )
    source_folder = typer.prompt(
        default="Prisma Access",
        show_default=True,
        text="Source Configuration Folder\n",
    )

    typer.echo("\n" + "-" * 79 + "\n\tEnter destination SCM credentials (where are you cloning to?)\n" + "-" * 79)
    dest_client_id = typer.prompt(
        default="example@0987654321.iam.panserviceaccount.com",
        text="Destination SCM Client ID\n",
        show_default=True,
    )
    dest_client_secret = typer.prompt(
        default="87654321-4321-4321-4321-120987654321",
        hide_input=True,
        show_default=True,
        text="Destination SCM Client Secret (input hidden)\n",
    )
    dest_tsg = typer.prompt(
        default="0987654321",
        show_default=True,
        text="Destination SCM Tenant TSG ID\n",
    )
    dest_folder = typer.prompt(
        default="Prisma Access",
        show_default=True,
        text="Destination Configuration Folder\n",
    )

    # Build data dictionary
    data = {
        "oauth": {
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
    except Exception as e:
        logger.error(f"Error writing authentication file: {e}")
        raise typer.Exit(code=1)

    typer.echo("\n" + "-" * 79 + f"\n\tAuthentication file created successfully `{output_file}`\n" + "-" * 79 + "\n")
    typer.echo("*" * 79 )
