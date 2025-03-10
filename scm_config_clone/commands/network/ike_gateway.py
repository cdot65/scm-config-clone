# scm_config_clone/commands/network/ike_gateway.py

import logging
from typing import List, Optional, Dict, Any, Set

import typer
from scm.client import Scm
from scm.config.network import IKEGateway
from scm.exceptions import (
    AuthenticationError,
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError,
)
from scm.models.network import IKEGatewayResponseModel, IKEGatewayCreateModel
from tabulate import tabulate

from scm_config_clone.utilities import (
    compare_object_lists,
    load_settings,
    parse_csv_option,
)


def build_create_params(
    src_obj: IKEGatewayResponseModel,
    destination: str,
    context_type: str = "folder",
) -> Dict[str, Any]:
    """
    Construct parameters for creating a new IKE gateway.

    Args:
        src_obj: The source IKE gateway object
        destination: The folder, snippet, or device where the object should be created
        context_type: The type of destination context ('folder', 'snippet', or 'device'). 
                     Defaults to "folder".

    Returns:
        Dict[str, Any]: Parameters for creating the IKE gateway
        
    Raises:
        ValueError: If required fields are missing or invalid.
    """
    # Basic parameters
    params = {
        "name": src_obj.name,
        context_type: destination,
    }

    # Add authentication
    if src_obj.authentication:
        params["authentication"] = src_obj.authentication.dict(exclude_unset=True)

    # Add peer_id if it exists
    if src_obj.peer_id:
        params["peer_id"] = src_obj.peer_id.dict(exclude_unset=True)

    # Add local_id if it exists
    if src_obj.local_id:
        params["local_id"] = src_obj.local_id.dict(exclude_unset=True)

    # Add protocol configuration
    if src_obj.protocol:
        params["protocol"] = src_obj.protocol.dict(exclude_unset=True)

    # Add protocol_common if it exists
    if src_obj.protocol_common:
        params["protocol_common"] = src_obj.protocol_common.dict(exclude_unset=True)

    # Add peer_address
    if src_obj.peer_address:
        params["peer_address"] = src_obj.peer_address.dict(exclude_unset=True)

    # Create a validated model and dump it to a dict
    create_model = IKEGatewayCreateModel(**params)
    return create_model.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )


def ike_gateways(
    context_type: str = typer.Option(
        "folder",
        "--context",
        help="Specify the context type: 'folder', 'snippet', or 'device'",
    ),
    context_source_name: Optional[str] = typer.Option(
        None,
        "--source",
        help="Name of the source folder, snippet, or device to retrieve objects from.",
    ),
    context_destination_name: Optional[str] = typer.Option(
        None,
        "--destination",
        help="Name of the destination folder, snippet, or device to create objects in.",
    ),
    # Legacy parameters (deprecated)
    source_folder: Optional[str] = typer.Option(
        None,
        "--source-folder",
        help="[DEPRECATED] Use --source with --context=folder instead.",
    ),
    source_snippet: Optional[str] = typer.Option(
        None,
        "--source-snippet",
        help="[DEPRECATED] Use --source with --context=snippet instead.",
    ),
    source_device: Optional[str] = typer.Option(
        None,
        "--source-device",
        help="[DEPRECATED] Use --source with --context=device instead.",
    ),
    destination_folder: Optional[str] = typer.Option(
        None,
        "--destination-folder",
        help="[DEPRECATED] Use --destination with --context=folder instead.",
    ),
    destination_snippet: Optional[str] = typer.Option(
        None,
        "--destination-snippet",
        help="[DEPRECATED] Use --destination with --context=snippet instead.",
    ),
    destination_device: Optional[str] = typer.Option(
        None,
        "--destination-device",
        help="[DEPRECATED] Use --destination with --context=device instead.",
    ),
    # Filter options
    names: Optional[str] = typer.Option(
        None,
        "--names",
        "-n",
        help="Comma-separated list of IKE gateway names to clone",
    ),
    # Exclusion options
    exclude_folders: str = typer.Option(
        None,
        "--exclude-folders",
        help="Comma-separated list of folders to exclude from the retrieval.",
    ),
    exclude_snippets: str = typer.Option(
        None,
        "--exclude-snippets",
        help="Comma-separated list of snippets to exclude from the retrieval.",
    ),
    exclude_devices: str = typer.Option(
        None,
        "--exclude-devices",
        help="Comma-separated list of devices to exclude from the retrieval.",
    ),
    # Action options
    commit_and_push: bool = typer.Option(
        False,
        "--commit-and-push",
        help="If set, commit the changes on the destination tenant after object creation.",
        is_flag=True,
    ),
    # General options
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
    Clone IKE gateways from a source SCM tenant to a destination SCM tenant.
    
    This Typer CLI command automates the process of retrieving IKE gateway objects
    from a specified folder, snippet, or device in a source tenant, optionally filters them
    based on user-defined criteria, and then creates them in a destination tenant.
    
    The workflow is:
    1. Load authentication and configuration settings from the YAML file.
    2. If any runtime flags are provided, they override the corresponding settings from the file.
    3. Authenticate to the source tenant and retrieve IKE gateways from the given context.
    4. Display the retrieved source objects. If not auto-approved, prompt the user before proceeding.
    5. Authenticate to the destination tenant and create the retrieved objects there.
    6. If `--commit-and-push` is provided and objects were created successfully, commit the changes.
    7. Display the results, including successfully created objects and any errors.
    
    Args:
        context_type: The type of context to use for source and destination (folder, snippet, device).
        context_source_name: The source context name to retrieve objects from.
        context_destination_name: The destination context name to create objects in.
        source_folder, source_snippet, source_device: Legacy parameters (deprecated).
        destination_folder, destination_snippet, destination_device: Legacy parameters (deprecated).
        names: Comma-separated list of specific gateway names to clone.
        exclude_folders, exclude_snippets, exclude_devices: Lists of contexts to exclude.
        commit_and_push: Whether to commit changes after creation.
        auto_approve, create_report, dry_run, quiet_mode: Control flags.
        logging_level: Logging verbosity level.
        settings_file: Path to the settings file with tenant credentials.
        
    Raises:
        typer.Exit: Exits if authentication fails, retrieval fails, or if the user opts not to proceed.
    """
    typer.echo("🚀 Starting IKE gateways cloning...")

    # Load settings from file
    settings = load_settings(settings_file)

    # Apply fallback logic: if a flag wasn't provided at runtime, use settings.yaml values
    auto_approve = settings["auto_approve"] if auto_approve is None else auto_approve
    create_report = settings["create_report"] if create_report is None else create_report
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
    exclude_snippets_list = parse_csv_option(exclude_snippets)
    exclude_devices_list = parse_csv_option(exclude_devices)
    name_filter = parse_csv_option(names)

    # Resolve parameters (prioritize new over legacy)
    source_context_resolved = None
    if context_source_name:
        source_context_resolved = context_source_name
    elif source_folder and context_type == "folder":
        source_context_resolved = source_folder
    elif source_snippet and context_type == "snippet":
        source_context_resolved = source_snippet
    elif source_device and context_type == "device":
        source_context_resolved = source_device

    destination_context_resolved = None
    if context_destination_name:
        destination_context_resolved = context_destination_name
    elif destination_folder and context_type == "folder":
        destination_context_resolved = destination_folder
    elif destination_snippet and context_type == "snippet":
        destination_context_resolved = destination_snippet
    elif destination_device and context_type == "device":
        destination_context_resolved = destination_device

    # Prompt if still None after resolution
    if source_context_resolved is None:
        source_context_resolved = typer.prompt(
            f"Name of source {context_type} where objects are located"
        )
    if destination_context_resolved is None:
        destination_context_resolved = typer.prompt(
            f"Name of destination {context_type} where objects will go"
        )

    # Authenticate with source
    try:
        source_creds = settings["source_scm"]
        source_client = Scm(
            client_id=source_creds["client_id"],
            client_secret=source_creds["client_secret"],
            tsg_id=source_creds["tenant"],
            log_level=logging_level,
        )
        logger.info(f"Authenticated with source SCM tenant: {source_creds['tenant']}")
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with source tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with source authentication: {e}")
        raise typer.Exit(code=1)

    # Authenticate with destination
    try:
        destination_creds = settings["destination_scm"]
        destination_client = Scm(
            client_id=destination_creds["client_id"],
            client_secret=destination_creds["client_secret"],
            tsg_id=destination_creds["tenant"],
            log_level=logging_level,
        )
        logger.info(
            f"Authenticated with destination SCM tenant: {destination_creds['tenant']}"
        )
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with destination tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with destination authentication: {e}")
        raise typer.Exit(code=1)

    # Retrieve IKE gateways from source
    try:
        source_api = IKEGateway(source_client)

        # Call list() with different parameters based on context
        list_params = {
            "exact_match": True,
            "exclude_folders": exclude_folders_list,
            "exclude_snippets": exclude_snippets_list,
            "exclude_devices": exclude_devices_list,
        }

        # Add context-specific parameter
        list_params[context_type] = source_context_resolved

        # If names filter is provided, add it to parameters
        if name_filter:
            list_params["name"] = name_filter

        source_gateways = source_api.list(**list_params)

        logger.info(
            f"Retrieved {len(source_gateways)} IKE gateways from source {context_type} '{source_context_resolved}'."
        )
    except Exception as e:
        logger.error(f"Error retrieving IKE gateways from source: {e}")
        raise typer.Exit(code=1)

    # Retrieve IKE gateways from destination
    try:
        destination_api = IKEGateway(destination_client)

        # Different API call based on context type
        list_params = {
            context_type: destination_context_resolved,
            "exact_match": True,
            "exclude_folders": exclude_folders_list,
            "exclude_snippets": exclude_snippets_list,
            "exclude_devices": exclude_devices_list,
        }
        
        destination_gateways = destination_api.list(**list_params)
        logger.info(
            f"Retrieved {len(destination_gateways)} gateways from destination {context_type} '{destination_context_resolved}'"
        )
    except Exception as e:
        logger.error(f"Error retrieving gateways: {e}")
        raise typer.Exit(code=1)

    # Compare and get the status information
    comparison_results = compare_object_lists(
        source_gateways,
        destination_gateways,
    )

    if source_gateways and not quiet_mode:
        table_data = []
        for result in comparison_results:
            # Get the corresponding source gateway
            source_gateway = next(
                (g for g in source_gateways if g.name == result["name"]), None
            )
            if source_gateway:
                # Determine peer type and value
                peer_type = "N/A"
                peer_value = "N/A"
                
                if source_gateway.peer_address:
                    if hasattr(source_gateway.peer_address, 'ip') and source_gateway.peer_address.ip:
                        peer_type = "IP"
                        peer_value = source_gateway.peer_address.ip
                    elif hasattr(source_gateway.peer_address, 'fqdn') and source_gateway.peer_address.fqdn:
                        peer_type = "FQDN"
                        peer_value = source_gateway.peer_address.fqdn
                    elif hasattr(source_gateway.peer_address, 'dynamic') and source_gateway.peer_address.dynamic:
                        peer_type = "Dynamic"
                        peer_value = "Yes"
                
                # Authentication type
                auth_type = "N/A"
                if source_gateway.authentication:
                    if hasattr(source_gateway.authentication, 'pre_shared_key') and source_gateway.authentication.pre_shared_key:
                        auth_type = "Pre-shared Key"
                    elif hasattr(source_gateway.authentication, 'certificate') and source_gateway.authentication.certificate:
                        auth_type = "Certificate"
                
                # Add to table data
                table_row = [
                    source_gateway.name,
                    peer_type,
                    peer_value,
                    auth_type,
                    "x" if result["already_configured"] else ""
                ]
                table_data.append(table_row)

        typer.echo(
            tabulate(
                table_data,
                headers=["Name", "Peer Type", "Peer Value", "Auth Type", "Destination Status"],
                tablefmt="fancy_grid",
            )
        )

    # Prompt if not auto-approved and objects exist
    if source_gateways and not auto_approve:
        proceed = typer.confirm(
            "Do you want to proceed with creating these objects in the destination tenant?"
        )
        if not proceed:
            typer.echo("Aborting cloning operation.")
            raise typer.Exit(code=0)

    # Determine which objects need to be created (those not already configured)
    already_configured_names = {
        res["name"] for res in comparison_results if res["already_configured"]
    }

    gateways_to_create = [
        obj for obj in source_gateways if obj.name not in already_configured_names
    ]

    # Create IKE gateways in destination
    destination_api = IKEGateway(destination_client)
    created_gateways = []
    error_gateways = []

    for src_obj in gateways_to_create:
        if dry_run:
            logger.info(
                f"Skipping creation of IKE gateway in destination (dry run): {src_obj.name}"
            )
            continue

        if create_report:
            with open("result.csv", "a") as f:
                f.write(
                    f"IKEGateway,{src_obj.name},{getattr(src_obj, context_type)}\n"
                )

        try:
            create_params = build_create_params(
                src_obj=src_obj,
                destination=destination_context_resolved,
                context_type=context_type,
            )
        except ValueError as ve:
            error_gateways.append([src_obj.name, str(ve)])
            continue

        try:
            new_obj = destination_api.create(create_params)
            created_gateways.append(new_obj)
            logger.info(f"Created IKE gateway in destination: {new_obj.name}")
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
            error_gateways.append([src_obj.name, error_type])
        except Exception as e:  # noqa
            if logging_level == "DEBUG":
                error_type = str(e)
            else:
                error_type = "Unknown Error, enable debug logging for more details."
            error_gateways.append([src_obj.name, error_type])
            continue

    # Display results if not quiet_mode
    if created_gateways and not quiet_mode:
        typer.echo("\nSuccessfully created the following IKE gateways:")
        created_table = []
        for obj in created_gateways:
            created_table.append([obj.name])

        typer.echo(
            tabulate(
                created_table,
                headers=["Name"],
                tablefmt="fancy_grid",
            )
        )

    if error_gateways and not quiet_mode:
        typer.echo("\nSome IKE gateways failed to be created:")
        typer.echo(
            tabulate(
                error_gateways,
                headers=["Object Name", "Error"],
                tablefmt="fancy_grid",
            )
        )

    # Commit changes if requested and objects were created
    if commit_and_push and created_gateways and context_type == "folder":
        try:
            commit_params = {
                "folders": [destination_context_resolved],
                "description": f"Cloned IKE gateways from {context_type} {source_context_resolved}",
                "sync": True,
            }

            result = destination_api.commit(**commit_params)
            job_status = destination_api.get_job_status(result.job_id)
            logger.info(
                f"Commit job ID {result.job_id} status: {job_status.data[0].status_str}"
            )
        except Exception as e:
            logger.error(f"Error committing IKE gateways in destination: {e}")
            raise typer.Exit(code=1)
    elif commit_and_push and created_gateways and context_type != "folder":
        logger.info(
            f"SCM does not support committing with a {context_type} context; perform this task on the destination tenant folder manually. Skipping commit."
        )
    else:
        if created_gateways and not commit_and_push:
            logger.info(
                "Objects created, but --commit-and-push not specified, skipping commit."
            )
        else:
            logger.info("No new IKE gateways were created, skipping commit.")

    typer.echo("🎉 IKE gateways cloning completed successfully! 🎉")