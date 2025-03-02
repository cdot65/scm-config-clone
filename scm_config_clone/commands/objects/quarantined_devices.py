# scm_config_clone/commands/objects/quarantined_devices.py

import logging
from typing import List, Optional, Any, Dict

import typer
from scm.client import Scm
from scm.config.objects import QuarantinedDevices
from scm.exceptions import (
    AuthenticationError,
    InvalidObjectError,
    MissingQueryParameterError,
    ObjectNotPresentError,
)
from scm.models.objects import (
    QuarantinedDevicesCreateModel,
    QuarantinedDevicesResponseModel,
)
from tabulate import tabulate

from scm_config_clone.utilities import (
    load_settings,
)


def build_create_params(
    src_obj: QuarantinedDevicesResponseModel,
) -> Dict[str, Any]:
    """
    Construct the dictionary of parameters required to create a new quarantined device object.

    Given an existing QuarantinedDevicesResponseModel (source object), this function builds a dictionary
    with all necessary fields for creating a new quarantined device in the destination tenant.
    It uses `model_dump` on a Pydantic model to ensure only valid, explicitly set fields are included.

    Args:
        src_obj: The QuarantinedDevicesResponseModel representing the source quarantined device.

    Returns:
        A dictionary containing the fields required for `QuarantinedDevices.create()`.
        This dictionary is validated and pruned by QuarantinedDevicesCreateModel.
    """
    data = {
        "host_id": src_obj.host_id,
        "serial_number": (
            src_obj.serial_number if src_obj.serial_number is not None else None
        ),
    }

    create_model = QuarantinedDevicesCreateModel(**data)
    return create_model.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )


def compare_quarantined_devices(
    source_objects: List[QuarantinedDevicesResponseModel],
    destination_objects: List[QuarantinedDevicesResponseModel],
) -> List[Dict[str, Any]]:
    """
    Compare source and destination quarantined devices to determine which ones already exist.

    Args:
        source_objects: List of quarantined devices from the source tenant.
        destination_objects: List of quarantined devices from the destination tenant.

    Returns:
        List of dictionaries containing comparison results for each source object.
        Each dictionary has keys: "host_id", "serial_number", and "already_configured".
    """
    comparison_results = []

    # Create a set of destination host_ids for faster lookup
    destination_host_ids = {obj.host_id for obj in destination_objects}

    for src_obj in source_objects:
        already_configured = src_obj.host_id in destination_host_ids
        comparison_results.append(
            {
                "host_id": src_obj.host_id,
                "serial_number": src_obj.serial_number,
                "already_configured": already_configured,
            }
        )

    return comparison_results


def quarantined_devices(
    host_id: Optional[str] = typer.Option(
        None,
        "--host-id",
        help="Filter quarantined devices by host ID.",
    ),
    serial_number: Optional[str] = typer.Option(
        None,
        "--serial-number",
        help="Filter quarantined devices by serial number.",
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
    Clone quarantined devices from a source SCM tenant to a destination SCM tenant.

    This Typer CLI command automates the process of retrieving quarantined devices
    from a source tenant, optionally filters them by host_id or serial_number,
    and then creates them in a destination tenant.

    The workflow is:
    1. Load authentication and configuration settings (e.g., credentials, logging) from the YAML file.
    2. If any runtime flags are provided, they override the corresponding settings from the file.
    3. Authenticate to the source tenant and retrieve quarantined devices, with optional filtering.
    4. Display the retrieved source objects. If not auto-approved, prompt the user before proceeding.
    5. Authenticate to the destination tenant and create the retrieved objects there.
    6. Display the results, including successfully created objects and any errors.

    Args:
        host_id: Optional filter by device host ID.
        serial_number: Optional filter by device serial number.
        auto_approve: If True or set in settings, skip the confirmation prompt before creating objects.
        create_report: If True or set in settings, create/append a CSV file with task results.
        dry_run: If True or set in settings, perform a dry run without applying changes.
        quiet_mode: If True or set in settings, hide console output except log messages.
        logging_level: If provided, override the logging level from settings.yaml.
        settings_file: Path to the YAML settings file for loading authentication and configuration.

    Raises:
        typer.Exit: Exits if authentication fails, retrieval fails, or if the user opts not to proceed.
    """
    typer.echo("🚀 Starting quarantined devices cloning...")

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

    # Retrieve quarantined devices from source
    try:
        source_quarantined_devices_api = QuarantinedDevices(source_client)

        # Call list() with filters if provided
        list_params = {}
        if host_id is not None:
            list_params["host_id"] = host_id
        if serial_number is not None:
            list_params["serial_number"] = serial_number

        source_objects = source_quarantined_devices_api.list(**list_params)

        logger.info(
            f"Retrieved {len(source_objects)} quarantined devices from source tenant."
        )
    except Exception as e:
        logger.error(f"Error retrieving quarantined devices from source: {e}")
        raise typer.Exit(code=1)

    # Retrieve quarantined devices from destination
    try:
        destination_quarantined_devices_api = QuarantinedDevices(destination_client)
        destination_objects = destination_quarantined_devices_api.list()
        logger.info(
            f"Retrieved {len(destination_objects)} quarantined devices from destination tenant."
        )
    except Exception as e:
        logger.error(f"Error retrieving quarantined devices from destination: {e}")
        raise typer.Exit(code=1)

    # Compare and get the status information
    comparison_results = compare_quarantined_devices(
        source_objects,
        destination_objects,
    )

    if source_objects and not quiet_mode:
        devices_table = []
        for result in comparison_results:
            # 'x' if already configured else ''
            status = "x" if result["already_configured"] else ""
            devices_table.append([result["host_id"], result["serial_number"], status])

        typer.echo(
            tabulate(
                devices_table,
                headers=["Host ID", "Serial Number", "Destination Status"],
                tablefmt="fancy_grid",
            )
        )

    # Prompt if not auto-approved and objects exist
    if source_objects and not auto_approve:
        proceed = typer.confirm(
            "Do you want to proceed with creating these quarantined devices in the destination tenant?"
        )
        if not proceed:
            typer.echo("Aborting cloning operation.")
            raise typer.Exit(code=0)

    # Determine which objects need to be created (those not already configured)
    already_configured_host_ids = {
        res["host_id"] for res in comparison_results if res["already_configured"]
    }

    objects_to_create = [
        obj for obj in source_objects if obj.host_id not in already_configured_host_ids
    ]

    # Create quarantined devices in destination
    destination_quarantined_devices = QuarantinedDevices(destination_client)
    created_objs: List[QuarantinedDevicesResponseModel] = []
    error_objects: List[List[str]] = []

    for src_obj in objects_to_create:
        if dry_run:
            logger.info(
                f"Skipping creation of quarantined device in destination (dry run): {src_obj.host_id}"
            )
            continue

        if create_report:
            with open("result.csv", "a") as f:
                f.write(
                    f"Quarantined Device,{src_obj.host_id},{src_obj.serial_number or 'N/A'}\n"
                )

        try:
            create_params = build_create_params(src_obj=src_obj)
        except ValueError as ve:
            error_objects.append([src_obj.host_id, str(ve)])
            continue

        try:
            new_obj = destination_quarantined_devices.create(create_params)
            created_objs.append(new_obj)
            logger.info(f"Created quarantined device in destination: {new_obj.host_id}")
        except (
            InvalidObjectError,
            MissingQueryParameterError,
            ObjectNotPresentError,
        ) as e:
            if logging_level == "DEBUG":
                error_type = str(e)
            else:
                error_type = type(e).__name__
            error_objects.append([src_obj.host_id, error_type])
        except Exception as e:  # noqa
            if logging_level == "DEBUG":
                error_type = str(e)
            else:
                error_type = "Unknown Error, enable debug logging for more details."
            error_objects.append([src_obj.host_id, error_type])
            continue

    # Display results if not quiet_mode
    if created_objs and not quiet_mode:
        typer.echo("\nSuccessfully created the following quarantined devices:")
        created_table = []
        for obj in created_objs:
            created_table.append([obj.host_id, obj.serial_number or "N/A"])

        typer.echo(
            tabulate(
                created_table,
                headers=["Host ID", "Serial Number"],
                tablefmt="fancy_grid",
            )
        )

    if error_objects and not quiet_mode:
        typer.echo("\nSome quarantined devices failed to be created:")
        typer.echo(
            tabulate(
                error_objects,
                headers=["Host ID", "Error"],
                tablefmt="fancy_grid",
            )
        )

    typer.echo("🎉 Quarantined devices cloning completed successfully! 🎉")
