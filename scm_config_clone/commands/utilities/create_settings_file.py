# scm_config_clone/commands/create_settings_file.py

# standard library
import logging

# third party library
import pandas as pd
import typer
import yaml
from tabulate import tabulate

logger = logging.getLogger(__name__)


def create_settings(
    output_file: str = typer.Option(
        "settings.yaml",
        "--output-file",
        "-o",
        help="Path to the output YAML settings file where credentials and configuration will be stored.",
    ),
):
    """
    Interactively create a .settings.yaml file containing SCM credentials, logging configuration,
    and additional runtime options.

    This Typer CLI command prompts the user for:
    - Source and destination SCM credentials (Client ID, Client Secret, TSG ID)
    - Logging level preference (DEBUG, INFO, etc.)
    - Additional boolean options (auto_approve, create_report, dry_run, quiet)

    It then writes these values to a YAML file, enabling subsequent commands to load these
    settings automatically.

    Workflow:
    1. Prompt user for source SCM credentials.
    2. Prompt user for destination SCM credentials.
    3. Prompt user for logging level.
    4. Prompt user for additional boolean options (auto_approve, create_report, dry_run, quiet).
    5. Write the collected configuration to the specified YAML settings file.
    6. Display a summary table with masked secrets.

    Args:
        output_file (str): The file path where the generated .settings.yaml will be written.
            Defaults to ".settings.yaml".

    Raises:
        typer.Exit: If an error occurs while writing the YAML file, the command exits
        with a non-zero code after logging the error.

    Example:
        Running the command without arguments:
        ```
        scm-clone create-secrets-file
        ```
        This will prompt the user interactively and create `.settings.yaml` in the current directory.
    """
    typer.echo("🚀 " + ("*" * 79))
    typer.echo(f"Creating settings file called {output_file} in the current directory")
    typer.echo()

    # Prompt user for source SCM credentials
    typer.echo("-" * 79)
    typer.echo("🔑 Enter source SCM credentials (used as the configuration source)")
    typer.echo("-" * 79)
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

    # Prompt user for destination SCM credentials
    typer.echo()
    typer.echo("-" * 79)
    typer.echo("🔑 Enter destination SCM credentials (target of configuration cloning)")
    typer.echo("-" * 79)
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

    # Prompt user for logging level
    typer.echo()
    typer.echo("-" * 79)
    typer.echo(
        "🪵 Specify desired logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    typer.echo("-" * 79)
    logging_level = typer.prompt(
        default="INFO",
        show_default=True,
        text="Logging Level\n",
    )

    # Additional questions
    typer.echo()
    typer.echo("-" * 79)
    typer.echo("⚙️  Additional Configuration Options:")
    typer.echo("-" * 79)

    auto_approve = typer.confirm(
        "Would you like to auto-approve changes without review?",
        default=False,
    )
    create_report = typer.confirm(
        "Would you like to create a .csv file reporting the job?",
        default=False,
    )
    dry_run = typer.confirm(
        "Would you like to perform a dry run (no changes applied)?",
        default=False,
    )
    quiet = typer.confirm(
        "Would you like to hide all console output (except log messages)?",
        default=False,
    )

    # Build data dictionary to write to YAML
    data = {
        "oauth": {
            "source": {
                "client_id": source_client_id,
                "client_secret": source_client_secret,
                "tsg": source_tsg,
            },
            "destination": {
                "client_id": dest_client_id,
                "client_secret": dest_client_secret,
                "tsg": dest_tsg,
            },
        },
        "logging": logging_level,
        "auto_approve": auto_approve,
        "create_report": create_report,
        "dry_run": dry_run,
        "quiet": quiet,
    }

    # Write data to the specified YAML file
    try:
        with open(output_file, "w") as f:
            yaml.dump(data, f)
    except Exception as e:
        logger.error(f"Error writing settings file: {e}")
        raise typer.Exit(code=1)

    # Mask client secrets for display
    masked_source_secret = source_client_secret[:4] + "****"
    masked_dest_secret = dest_client_secret[:4] + "****"

    # Prepare data for tabular display
    display_data = {
        "Source Client ID": source_client_id,
        "Source Client Secret": masked_source_secret,
        "Source TSG": source_tsg,
        "Destination Client ID": dest_client_id,
        "Destination Client Secret": masked_dest_secret,
        "Destination TSG": dest_tsg,
        "Logging Level": logging_level,
        "Auto Approve": auto_approve,
        "Create Report": create_report,
        "Dry Run": dry_run,
        "Quiet Mode": quiet,
    }

    df = pd.DataFrame(
        list(display_data.items()), columns=["Configuration Key", "Value"]
    )

    typer.echo()
    typer.echo("-" * 79)
    typer.echo(
        "✅ Settings file created successfully and the following configuration was saved:\n"
    )
    typer.echo(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
    typer.echo("-" * 79)
    typer.echo("🎉 Setup complete! 🎉")
