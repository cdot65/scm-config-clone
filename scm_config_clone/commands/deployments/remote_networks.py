# scm_config_clone/commands/deployments/remote_networks.py

import logging
from typing import List, Optional, Any, Dict

import typer
from scm.client import Scm
from scm.config.deployment import RemoteNetworks
from scm.exceptions import (
    AuthenticationError,
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError,
)
from scm.models.deployment import (
    RemoteNetworkCreateModel,
    RemoteNetworkResponseModel,
)
from tabulate import tabulate

from scm_config_clone.utilities import (
    compare_object_lists,
    load_settings,
    parse_csv_option,
)


def build_create_params(
    src_obj: RemoteNetworkResponseModel,
    destination: str,
) -> Dict[str, Any]:
    """
    Construct the dictionary of parameters required to create a new remote network object.

    Given an existing RemoteNetworkResponseModel (source object) and a destination folder,
    this function builds a dictionary with all necessary fields for creating
    a new remote network in the destination tenant. It uses `model_dump` on a Pydantic model
    to ensure only valid, explicitly set fields are included.

    Args:
        src_obj: The RemoteNetworkResponseModel representing the source remote network object.
        destination: The folder in the destination tenant where the object should be created.

    Returns:
        A dictionary containing the fields required for `RemoteNetworks.create()`.
        This dictionary is validated and pruned by RemoteNetworkCreateModel.
    """
    data = {
        "name": src_obj.name,
        "folder": destination,
        "description": (
            src_obj.description
            if hasattr(src_obj, "description") and src_obj.description is not None
            else None
        ),
        "region": src_obj.region,
        "spn_name": src_obj.spn_name,
        "license_type": src_obj.license_type,
        "ecmp_load_balancing": src_obj.ecmp_load_balancing,
        "subnets": (
            src_obj.subnets if hasattr(src_obj, "subnets") and src_obj.subnets else []
        ),
    }

    # Add conditional fields based on ecmp_load_balancing
    if src_obj.ecmp_load_balancing and src_obj.ecmp_load_balancing.value == "disable":
        data["ipsec_tunnel"] = src_obj.ipsec_tunnel
    elif (
        src_obj.ecmp_load_balancing
        and src_obj.ecmp_load_balancing.value == "enable"
        and hasattr(src_obj, "ecmp_tunnels")
    ):
        data["ecmp_tunnels"] = src_obj.ecmp_tunnels

    # Add protocol BGP if it exists
    if hasattr(src_obj, "protocol") and src_obj.protocol:
        data["protocol"] = src_obj.protocol

    create_model = RemoteNetworkCreateModel(**data)
    return create_model.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )


def remote_networks(
    context_source_name: Optional[str] = typer.Option(
        None,
        "--source",
        help="Name of the source folder to retrieve remote networks from.",
    ),
    context_destination_name: Optional[str] = typer.Option(
        None,
        "--destination",
        help="Name of the destination folder to create remote networks in.",
    ),
    # Legacy parameters (deprecated)
    source_folder: Optional[str] = typer.Option(
        None,
        "--source-folder",
        help="[DEPRECATED] Use --source instead.",
    ),
    destination_folder: Optional[str] = typer.Option(
        None,
        "--destination-folder",
        help="[DEPRECATED] Use --destination instead.",
    ),
    exclude_folders: str = typer.Option(
        None,
        "--exclude-folders",
        help="Comma-separated list of folders to exclude from the retrieval.",
    ),
    commit_and_push: bool = typer.Option(
        False,
        "--commit-and-push",
        help="If set, commit the changes on the destination tenant after object creation.",
        is_flag=True,
    ),
    auto_approve: bool = typer.Option(
        None,
        "--auto-approve",
        "-A",
        help="If set, skip the confirmation prompt and automatically proceed with creation.",
        is_flag=True,
    ),
    create_report: bool = typer.Option(
        None,
        "--create-report",
        "-R",
        help="If set, create or append to a 'result.csv' file with the task results.",
        is_flag=True,
    ),
    dry_run: bool = typer.Option(
        None,
        "--dry-run",
        "-D",
        help="If set, perform a dry run without applying any changes.",
        is_flag=True,
    ),
    quiet_mode: bool = typer.Option(
        None,
        "--quiet-mode",
        "-Q",
        help="If set, hide all console output (except log messages).",
        is_flag=True,
    ),
    logging_level: str = typer.Option(
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
    Clone remote network objects from a source SASE tenant to a destination SASE tenant.

    This Typer CLI command automates the process of retrieving remote network objects
    from a specified folder in a source tenant, optionally filters them out based
    on user-defined exclusion criteria, and then creates them in a destination tenant.

    The workflow is:
    1. Load authentication and configuration settings (e.g., credentials, logging) from the YAML file.
    2. If any runtime flags are provided, they override the corresponding settings from the file.
    3. Authenticate to the source tenant and retrieve remote network objects from the given folder.
    4. Display the retrieved source objects. If not auto-approved, prompt the user before proceeding.
    5. Authenticate to the destination tenant and create the retrieved objects there.
    6. If `--commit-and-push` is provided and objects were created successfully, commit the changes.
    7. Display the results, including successfully created objects and any errors.

    Args:
        context_source_name: Name of source folder to retrieve remote network objects from.
        context_destination_name: Name of destination folder to create remote network objects in.
        source_folder: [DEPRECATED] The source folder from which to retrieve remote network objects.
        destination_folder: [DEPRECATED] The destination folder from which to push remote network objects.
        exclude_folders: Comma-separated folder names to exclude from source retrieval.
        commit_and_push: If True, commit changes in the destination tenant after creation.
        auto_approve: If True or set in settings, skip the confirmation prompt before creating objects.
        create_report: If True or set in settings, create/append a CSV file with task results.
        dry_run: If True or set in settings, perform a dry run without applying changes.
        quiet_mode: If True or set in settings, hide console output except log messages.
        logging_level: If provided, override the logging level from settings.yaml.
        settings_file: Path to the YAML settings file for loading authentication and configuration.

    Raises:
        typer.Exit: Exits if authentication fails, retrieval fails, or if the user opts not to proceed.
    """
    typer.echo("🚀 Starting remote network objects cloning...")

    # Load settings from file
    settings = load_settings(settings_file)

    # Apply fallback logic: if a flag wasn't provided at runtime, use settings.yaml values
    auto_approve = settings["auto_approve"] if auto_approve is None else auto_approve
    create_report = (
        settings["create_report"] if create_report is None else create_report
    )
    dry_run = settings["dry_run"] if dry_run is None else dry_run
    quiet_mode = settings["quiet"] if quiet_mode is None else quiet_mode

    # Logging level fallback
    if logging_level is None:
        logging_level = settings["logging"]
    logging_level = logging_level.upper()

    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, logging_level, logging.INFO))

    # Parse CSV options
    exclude_folders_list = parse_csv_option(exclude_folders)

    # Resolve parameters (prioritize new over legacy)
    resolved_source = context_source_name or source_folder
    resolved_destination = context_destination_name or destination_folder

    # Prompt if still None after resolution
    if resolved_source is None:
        resolved_source = typer.prompt(
            "Name of source folder where remote networks are located"
        )
    if resolved_destination is None:
        resolved_destination = typer.prompt(
            "Name of destination folder where remote networks will go"
        )

    # Check if source_sase and destination_sase are in settings
    # If not, fall back to using source_scm and destination_scm
    source_creds = settings.get("source_sase", settings.get("source_scm", {}))
    destination_creds = settings.get(
        "destination_sase", settings.get("destination_scm", {})
    )

    # Authenticate with source
    try:
        source_client = Scm(
            client_id=source_creds["client_id"],
            client_secret=source_creds["client_secret"],
            tsg_id=source_creds["tenant"],
            log_level=logging_level,
        )
        # The RemoteNetworks class will set the proper API base URL
        logger.info(f"Authenticated with source tenant: {source_creds['tenant']}")
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with source tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with source authentication: {e}")
        raise typer.Exit(code=1)

    # Authenticate with destination
    try:
        destination_client = Scm(
            client_id=destination_creds["client_id"],
            client_secret=destination_creds["client_secret"],
            tsg_id=destination_creds["tenant"],
            log_level=logging_level,
        )
        # The RemoteNetworks class will set the proper API base URL
        logger.info(
            f"Authenticated with destination tenant: {destination_creds['tenant']}"
        )
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with destination tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with destination authentication: {e}")
        raise typer.Exit(code=1)

    # Retrieve remote network objects from source
    try:
        source_remote_networks_api = RemoteNetworks(source_client, max_limit=5000)

        # Call list() with folder parameter
        list_params = {
            "exact_match": True,
            "exclude_folders": exclude_folders_list,
            "folder": resolved_source,
        }

        source_objects = source_remote_networks_api.list(**list_params)

        logger.info(
            f"Retrieved {len(source_objects)} remote network objects from source folder '{resolved_source}'."
        )
    except Exception as e:
        logger.error(f"Error retrieving remote network objects from source: {e}")
        raise typer.Exit(code=1)

    # Retrieve remote network objects from destination
    try:
        destination_client_api = RemoteNetworks(destination_client, max_limit=5000)

        destination_objects = destination_client_api.list(
            folder=resolved_destination,
            exact_match=True,
            exclude_folders=exclude_folders_list,
        )
        logger.info(
            f"Retrieved {len(destination_objects)} objects from destination folder '{resolved_destination}'"
        )
    except Exception as e:
        logger.error(f"Error retrieving objects: {e}")
        raise typer.Exit(code=1)

    # Compare and get the status information
    comparison_results = compare_object_lists(
        source_objects,
        destination_objects,
    )

    if source_objects and not quiet_mode:
        remote_networks_table = []
        for result in comparison_results:
            # 'x' if already configured else ''
            status = "x" if result["already_configured"] else ""
            remote_networks_table.append([result["name"], status])

        typer.echo(
            tabulate(
                remote_networks_table,
                headers=["Name", "Destination Status"],
                tablefmt="fancy_grid",
            )
        )

    # Prompt if not auto-approved and objects exist
    if source_objects and not auto_approve:
        proceed = typer.confirm(
            "Do you want to proceed with creating these remote networks in the destination tenant?"
        )
        if not proceed:
            typer.echo("Aborting cloning operation.")
            raise typer.Exit(code=0)

    # Determine which objects need to be created (those not already configured)
    already_configured_names = {
        res["name"] for res in comparison_results if res["already_configured"]
    }

    objects_to_create = [
        obj for obj in source_objects if obj.name not in already_configured_names
    ]

    # Create remote network objects in destination
    destination_remote_networks = RemoteNetworks(destination_client, max_limit=5000)
    created_objs: List[RemoteNetworkResponseModel] = []
    error_objects: List[List[str]] = []

    for src_obj in objects_to_create:
        if dry_run:
            logger.info(
                f"Skipping creation of remote network object in destination (dry run): {src_obj.name}"
            )
            continue

        if create_report:
            with open("result.csv", "a") as f:
                f.write(f"RemoteNetwork,{src_obj.name},{src_obj.folder}\n")

        try:
            create_params = build_create_params(
                src_obj=src_obj,
                destination=resolved_destination,
            )
        except ValueError as ve:
            error_objects.append([src_obj.name, str(ve)])
            continue

        try:
            new_obj = destination_remote_networks.create(create_params)
            created_objs.append(new_obj)
            logger.info(f"Created remote network object in destination: {new_obj.name}")
        except (
            InvalidObjectError,
            MissingQueryParameterError,
            NameNotUniqueError,
            ObjectNotPresentError,
        ) as e:
            if logging_level == "DEBUG":
                error_type = str(e)
            else:
                error_type = type(e).__name__
            error_objects.append([src_obj.name, error_type])
        except Exception as e:  # noqa
            if logging_level == "DEBUG":
                error_type = str(e)
            else:
                error_type = "Unknown Error, enable debug logging for more details."
            error_objects.append([src_obj.name, error_type])
            continue

    # Display results if not quiet_mode
    if created_objs and not quiet_mode:
        typer.echo("\nSuccessfully created the following remote network objects:")
        created_table = []
        for obj in created_objs:
            created_table.append([obj.name])

        typer.echo(
            tabulate(
                created_table,
                headers=["Name"],
                tablefmt="fancy_grid",
            )
        )

    if error_objects and not quiet_mode:
        typer.echo("\nSome remote network objects failed to be created:")
        typer.echo(
            tabulate(
                error_objects,
                headers=["Object Name", "Error"],
                tablefmt="fancy_grid",
            )
        )

    # Commit changes if requested and objects were created
    if commit_and_push and created_objs:
        try:
            commit_params = {
                "folders": [resolved_destination],
                "description": f"Cloned remote network objects from folder {resolved_source}",
                "sync": True,
            }
            result = destination_remote_networks.commit(**commit_params)
            job_status = destination_remote_networks.get_job_status(result.job_id)
            logger.info(
                f"Commit job ID {result.job_id} status: {job_status.data[0].status_str}"
            )
        except Exception as e:
            logger.error(f"Error committing remote network objects in destination: {e}")
            raise typer.Exit(code=1)
    else:
        if created_objs and not commit_and_push:
            logger.info(
                "Objects created, but --commit-and-push not specified, skipping commit."
            )
        else:
            logger.info("No new remote network objects were created, skipping commit.")

    typer.echo("🎉 Remote network objects cloning completed successfully! 🎉")
