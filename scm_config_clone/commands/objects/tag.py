# scm_config_clone/commands/objects/tag.py

import logging
from typing import List, Optional, Any

import typer
from scm.client import Scm
from scm.config.objects import Tag
from scm.exceptions import (
    AuthenticationError,
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError,
)
from tabulate import tabulate

from scm_config_clone.utilities import load_settings, parse_csv_option


def tags(
    folder: Optional[str] = typer.Option(
        None,
        "--folder",
        prompt="Please enter the folder name",
        help="The folder from which to clone tag objects.",
    ),
    exclude_folders: str = typer.Option(
        None,
        "--exclude-folders",
        help="Comma-separated list of folders to exclude from retrieval.",
    ),
    exclude_snippets: str = typer.Option(
        None,
        "--exclude-snippets",
        help="Comma-separated list of snippets to exclude from retrieval.",
    ),
    exclude_devices: str = typer.Option(
        None,
        "--exclude-devices",
        help="Comma-separated list of devices to exclude from retrieval.",
    ),
    commit_and_push: bool = typer.Option(
        False,
        "--commit-and-push",
        help="If set, commit the changes on the destination tenant after object creation.",
        is_flag=True,
    ),
    auto_approve_flag: Optional[bool] = typer.Option(
        None,
        "--auto-approve",
        "-A",
        help="If set, skip the confirmation prompt and automatically proceed with creation.",
        is_flag=True,
    ),
    create_report_flag: Optional[bool] = typer.Option(
        None,
        "--create-report",
        "-R",
        help="If set, create/append a 'result.csv' file with the task results.",
        is_flag=True,
    ),
    dry_run_flag: Optional[bool] = typer.Option(
        None,
        "--dry-run",
        "-D",
        help="If set, perform a dry run without applying changes.",
        is_flag=True,
    ),
    quiet_mode_flag: Optional[bool] = typer.Option(
        None,
        "--quiet-mode",
        "-Q",
        help="If set, hide all console output (except log messages).",
        is_flag=True,
    ),
    logging_level_flag: Optional[str] = typer.Option(
        None,
        "--logging-level",
        "-L",
        help="Override the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    ),
    settings_file: str = typer.Option(
        "settings.yaml",
        "--settings-file",
        "-s",
        help="Path to the YAML settings file containing tenant credentials and configuration.",
    ),
):
    """
    Clone tag objects from a source SCM tenant to a destination SCM tenant.

    This Typer CLI command automates the process of retrieving tag objects
    from a specified folder in a source tenant, applying optional filters,
    and then creating them in a destination tenant.

    Workflow:
    1. Load configuration and credentials from a YAML settings file.
    2. Override any settings with runtime flags if provided.
    3. Authenticate to the source tenant and retrieve tag objects from the given folder.
    4. Display the retrieved tag objects (if not quiet_mode). If not auto-approved, prompt the user.
    5. Authenticate to the destination tenant and create the retrieved tag objects there.
    6. If `--commit-and-push` is set and objects were created successfully, commit the changes.
    7. Display results and handle optional features (auto_approve, create_report, dry_run, quiet_mode).

    Args:
        folder: The folder from which to list and clone tag objects.
        exclude_folders: Folders to exclude from source retrieval.
        exclude_snippets: Snippets to exclude from source retrieval.
        exclude_devices: Devices to exclude from source retrieval.
        commit_and_push: If True, commit changes in the destination tenant after creation.
        auto_approve_flag: Override auto-approve setting; if True, skip confirmation prompt.
        create_report_flag: Override create_report setting; if True, record results in 'result.csv'.
        dry_run_flag: Override dry_run setting; if True, simulate without making changes.
        quiet_mode_flag: Override quiet_mode setting; if True, suppress console output (except logs).
        logging_level_flag: Override logging level if provided.
        settings_file: Path to the YAML settings file.

    Raises:
        typer.Exit: If authentication or retrieval fails, or if user chooses not to proceed.
    """
    typer.echo("🚀 Starting tag objects cloning...")

    # Load settings
    settings = load_settings(settings_file)

    # Apply fallback logic for runtime flags vs settings
    auto_approve = (
        settings["auto_approve"] if auto_approve_flag is None else auto_approve_flag
    )
    create_report = (
        settings["create_report"] if create_report_flag is None else create_report_flag
    )
    dry_run = settings["dry_run"] if dry_run_flag is None else dry_run_flag
    quiet_mode = settings["quiet"] if quiet_mode_flag is None else quiet_mode_flag

    # Determine logging level
    if logging_level_flag is None:
        logging_level_flag = settings["logging"]
    logging_level_flag = logging_level_flag.upper()

    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, logging_level_flag, logging.INFO))

    # Convert comma-separated strings to lists
    exclude_folders_list = parse_csv_option(exclude_folders)
    exclude_snippets_list = parse_csv_option(exclude_snippets)
    exclude_devices_list = parse_csv_option(exclude_devices)

    # Authenticate with source tenant
    try:
        source_creds = settings["source_scm"]
        source_client = Scm(
            client_id=source_creds["client_id"],
            client_secret=source_creds["client_secret"],
            tsg_id=source_creds["tenant"],
            log_level=logging_level_flag,
        )
        logger.info(f"Authenticated with source SCM tenant: {source_creds['tenant']}")
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with source tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with source authentication: {e}")
        raise typer.Exit(code=1)

    # Retrieve tag objects from source
    try:
        source_tags = Tag(source_client, max_limit=5000)
        tag_objects = source_tags.list(
            folder=folder,
            exact_match=True,
            exclude_folders=exclude_folders_list,
            exclude_snippets=exclude_snippets_list,
            exclude_devices=exclude_devices_list,
        )
        logger.info(
            f"Retrieved {len(tag_objects)} tag objects from source tenant folder '{folder}'."
        )
    except Exception as e:
        logger.error(f"Error retrieving tag objects from source: {e}")
        raise typer.Exit(code=1)

    # Display retrieved tags if not quiet_mode
    if tag_objects and not quiet_mode:
        tag_table = [
            [t.name, t.folder, t.snippet or "", t.device or ""] for t in tag_objects
        ]
        typer.echo(
            tabulate(
                tag_table,
                headers=["Name", "Folder", "Snippet", "Device"],
                tablefmt="fancy_grid",
            )
        )
    elif not tag_objects:
        typer.echo("No tag objects found in the source folder.")

    # Prompt if not auto-approved and objects exist
    if tag_objects and not auto_approve:
        proceed = typer.confirm(
            "Do you want to proceed with creating these tag objects in the destination tenant?"
        )
        if not proceed:
            typer.echo("Aborting tag objects cloning operation.")
            raise typer.Exit(code=0)

    # Authenticate with destination tenant
    try:
        dest_creds = settings["destination_scm"]
        destination_client = Scm(
            client_id=dest_creds["client_id"],
            client_secret=dest_creds["client_secret"],
            tsg_id=dest_creds["tenant"],
            log_level=logging_level_flag,
        )
        logger.info(
            f"Authenticated with destination SCM tenant: {dest_creds['tenant']}"
        )
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with destination tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with destination authentication: {e}")
        raise typer.Exit(code=1)

    # Create tag objects in the destination
    destination_tags = Tag(destination_client, max_limit=5000)
    created_objs: List[Any] = []
    error_objects: List[List[str]] = []

    # For each tag from source, create in destination
    for src_obj in tag_objects:
        create_params = {
            "name": src_obj.name,
            "folder": folder,
            "description": getattr(src_obj, "description", None),
        }

        # If dry_run: skip in future logic
        try:
            new_obj = destination_tags.create(create_params)
            created_objs.append(new_obj)
            logger.info(f"Created tag object in destination: {new_obj.name}")
        except (
            InvalidObjectError,
            MissingQueryParameterError,
            NameNotUniqueError,
            ObjectNotPresentError,
        ) as e:
            error_objects.append([src_obj.name, str(e)])
            continue
        except Exception as e:
            error_objects.append([src_obj.name, str(e)])
            continue

    # Display results if not quiet_mode
    if created_objs and not quiet_mode:
        typer.echo("\nSuccessfully created the following tag objects:")
        # Assuming new_obj has attributes similar to retrieved tags (name, folder, snippet, device)
        created_table = [
            [
                obj.name,
                obj.folder,
                obj.snippet if getattr(obj, "snippet", None) else "",
                obj.device if getattr(obj, "device", None) else "",
            ]
            for obj in created_objs
        ]

        typer.echo(
            tabulate(
                created_table,
                headers=["Name", "Folder", "Snippet", "Device"],
                tablefmt="fancy_grid",
            )
        )

    if error_objects and not quiet_mode:
        typer.echo("\nSome tag objects failed to be created:")
        typer.echo(
            tabulate(
                error_objects,
                headers=["Object Name", "Error"],
                tablefmt="fancy_grid",
            )
        )

    # Commit changes if requested
    if commit_and_push and created_objs:
        try:
            commit_params = {
                "folders": [folder],
                "description": "Cloned tag objects",
                "sync": True,
            }
            result = destination_tags.commit(**commit_params)
            job_status = destination_tags.get_job_status(result.job_id)
            logger.info(
                f"Commit job ID {result.job_id} status: {job_status.data[0].status_str}"
            )
        except Exception as e:
            logger.error(f"Error committing tag objects in destination: {e}")
            raise typer.Exit(code=1)
    else:
        if created_objs and not commit_and_push:
            logger.info(
                "Tag objects created, but --commit-and-push not specified, skipping commit."
            )
        else:
            logger.info("No new tag objects were created, skipping commit.")

    # If create_report is True, future logic will append results to 'result.csv'

    typer.echo("🎉 Tag objects cloning completed successfully! 🎉")
