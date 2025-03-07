# Standard library imports
import logging
from typing import List, Optional, Dict, Any, Set
import sys

# Third-party imports
import rich
import typer
from tabulate import tabulate

# Local imports
from scm_config_clone.utilities.settings import load_settings
from scm_config_clone.utilities.compare_object_lists import find_missing_objects
from scm_config_clone.utilities.parse_csv import parse_csv_string

# SCM SDK imports
from scm.client import ScmClient
from scm.config.network import IKEGateway
from scm.exceptions import (
    InvalidObjectError,
    MissingQueryParameterError,
    UnauthorizedError,
    ConnectionError,
)
from scm.models.network import (
    IKEGatewayResponseModel,
    IKEGatewayCreateModel,
)

app = typer.Typer()
logger = logging.getLogger(__name__)


def build_create_params(
    source_object: IKEGatewayResponseModel,
    destination_context: str,
    destination_context_name: str,
) -> Dict[str, Any]:
    """
    Build parameters for creating an IKE gateway in the destination tenant.

    Args:
        source_object: The source IKE gateway object
        destination_context: The destination context type ('folder', 'snippet', or 'device')
        destination_context_name: The name of the destination context

    Returns:
        Dict[str, Any]: Parameters for creating the IKE gateway
    """
    # Basic parameters
    params = {
        "name": source_object.name,
    }

    # Add authentication
    if source_object.authentication:
        params["authentication"] = source_object.authentication.dict(exclude_unset=True)

    # Add peer_id if it exists
    if source_object.peer_id:
        params["peer_id"] = source_object.peer_id.dict(exclude_unset=True)

    # Add local_id if it exists
    if source_object.local_id:
        params["local_id"] = source_object.local_id.dict(exclude_unset=True)

    # Add protocol configuration
    if source_object.protocol:
        params["protocol"] = source_object.protocol.dict(exclude_unset=True)

    # Add protocol_common if it exists
    if source_object.protocol_common:
        params["protocol_common"] = source_object.protocol_common.dict(exclude_unset=True)

    # Add peer_address
    if source_object.peer_address:
        params["peer_address"] = source_object.peer_address.dict(exclude_unset=True)

    # Set the correct context parameter
    params[destination_context] = destination_context_name

    return params


@app.command()
def clone(
    # Context options
    source_folder: Optional[str] = typer.Option(
        None,
        "--source-folder",
        "-sf",
        help="Source folder name",
    ),
    source_snippet: Optional[str] = typer.Option(
        None,
        "--source-snippet",
        "-ss",
        help="Source snippet name",
    ),
    source_device: Optional[str] = typer.Option(
        None,
        "--source-device",
        "-sd",
        help="Source device name",
    ),
    destination_folder: Optional[str] = typer.Option(
        None,
        "--destination-folder",
        "-df",
        help="Destination folder name",
    ),
    destination_snippet: Optional[str] = typer.Option(
        None,
        "--destination-snippet",
        "-ds",
        help="Destination snippet name",
    ),
    destination_device: Optional[str] = typer.Option(
        None,
        "--destination-device",
        "-dd",
        help="Destination device name",
    ),
    # Filter options
    names: Optional[str] = typer.Option(
        None,
        "--names",
        "-n",
        help="Comma-separated list of IKE gateway names to clone",
    ),
    # General options
    settings_file: str = typer.Option(
        "settings.yaml", "--settings", "-s", help="Settings file path"
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress output"),
    auto_approve: bool = typer.Option(
        False, "--yes", "-y", help="Skip confirmation prompts"
    ),
    log_level: str = typer.Option(
        "INFO", "--log-level", "-l", help="Logging level"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-d", help="Perform a dry run without making changes"
    ),
):
    """
    Clone IKE gateways from source to destination tenant.
    
    This command clones IKE gateway objects based on the specified context
    (folder, snippet, or device) from a source tenant to a destination tenant.
    """
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(message)s",
        handlers=[rich.logging.RichHandler(rich_tracebacks=True)],
    )
    
    # Load settings
    settings = load_settings(settings_file)
    if not settings:
        logger.error(f"❌ Failed to load settings from {settings_file}")
        sys.exit(1)
    
    # Determine source context
    source_context = None
    source_context_name = None
    
    if source_folder:
        source_context = "folder"
        source_context_name = source_folder
    elif source_snippet:
        source_context = "snippet"
        source_context_name = source_snippet
    elif source_device:
        source_context = "device"
        source_context_name = source_device
    else:
        logger.error("❌ Source context (folder, snippet, or device) is required")
        sys.exit(1)
    
    # Determine destination context
    destination_context = None
    destination_context_name = None
    
    if destination_folder:
        destination_context = "folder"
        destination_context_name = destination_folder
    elif destination_snippet:
        destination_context = "snippet"
        destination_context_name = destination_snippet
    elif destination_device:
        destination_context = "device"
        destination_context_name = destination_device
    else:
        logger.error("❌ Destination context (folder, snippet, or device) is required")
        sys.exit(1)
    
    # Parse names filter if provided
    name_filter: Set[str] = set()
    if names:
        name_filter = set(parse_csv_string(names))
        logger.info(f"🔍 Filtering gateways by names: {', '.join(name_filter)}")
    
    # Initialize SCM clients
    try:
        # Source tenant client
        source_client = ScmClient(
            client_id=settings["source"]["client_id"],
            client_secret=settings["source"]["client_secret"],
            tsg_id=settings["source"]["tsg_id"],
        )
        
        # Destination tenant client
        destination_client = ScmClient(
            client_id=settings["destination"]["client_id"],
            client_secret=settings["destination"]["client_secret"],
            tsg_id=settings["destination"]["tsg_id"],
        )
        
        logger.info("✅ Successfully initialized SCM clients")
    except (KeyError, ValueError) as e:
        logger.error(f"❌ Failed to initialize SCM clients: {e}")
        sys.exit(1)
    
    # Initialize IKE gateway services
    source_ike_gateway = IKEGateway(source_client)
    destination_ike_gateway = IKEGateway(destination_client)
    
    # Fetch source gateways
    logger.info(f"🔍 Fetching IKE gateways from source {source_context}: {source_context_name}")
    try:
        # Create kwargs for dynamic context parameter
        kwargs = {source_context: source_context_name}
        source_gateways = source_ike_gateway.list(**kwargs)
        
        # Filter by name if specified
        if name_filter:
            source_gateways = [
                gateway for gateway in source_gateways 
                if gateway.name in name_filter
            ]
        
        if not source_gateways:
            logger.warning(f"⚠️ No IKE gateways found in source {source_context}")
            if name_filter:
                logger.warning(f"⚠️ Check if the specified names exist in the source {source_context}")
            return
        
        logger.info(f"✅ Found {len(source_gateways)} IKE gateways in source {source_context}")
    except (InvalidObjectError, MissingQueryParameterError) as e:
        logger.error(f"❌ Failed to fetch source gateways: {e}")
        sys.exit(1)
    except (UnauthorizedError, ConnectionError) as e:
        logger.error(f"❌ Authentication or connection error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)
    
    # Fetch destination gateways to compare
    logger.info(f"🔍 Fetching IKE gateways from destination {destination_context}: {destination_context_name}")
    try:
        # Create kwargs for dynamic context parameter
        kwargs = {destination_context: destination_context_name}
        destination_gateways = destination_ike_gateway.list(**kwargs)
        
        logger.info(f"✅ Found {len(destination_gateways)} IKE gateways in destination {destination_context}")
    except (InvalidObjectError, MissingQueryParameterError) as e:
        logger.error(f"❌ Failed to fetch destination gateways: {e}")
        sys.exit(1)
    except (UnauthorizedError, ConnectionError) as e:
        logger.error(f"❌ Authentication or connection error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)
    
    # Determine gateways to create (missing in destination)
    gateways_to_create = find_missing_objects(
        source_objects=source_gateways, 
        destination_objects=destination_gateways,
        name_attribute="name"
    )
    
    if not gateways_to_create:
        logger.info("✅ No new IKE gateways to create")
        return
    
    # Display gateways to create
    if not quiet:
        table_data = []
        for gateway in gateways_to_create:
            peer_type = "N/A"
            peer_value = "N/A"
            
            if gateway.peer_address:
                if hasattr(gateway.peer_address, 'ip') and gateway.peer_address.ip:
                    peer_type = "IP"
                    peer_value = gateway.peer_address.ip
                elif hasattr(gateway.peer_address, 'fqdn') and gateway.peer_address.fqdn:
                    peer_type = "FQDN"
                    peer_value = gateway.peer_address.fqdn
                elif hasattr(gateway.peer_address, 'dynamic') and gateway.peer_address.dynamic:
                    peer_type = "Dynamic"
                    peer_value = "Yes"
            
            # Authentication type
            auth_type = "N/A"
            if gateway.authentication:
                if hasattr(gateway.authentication, 'pre_shared_key') and gateway.authentication.pre_shared_key:
                    auth_type = "Pre-shared Key"
                elif hasattr(gateway.authentication, 'certificate') and gateway.authentication.certificate:
                    auth_type = "Certificate"
            
            # IKE version
            ike_version = "N/A"
            if gateway.protocol and hasattr(gateway.protocol, 'version'):
                ike_version = gateway.protocol.version
            
            # Add to table data
            table_data.append([
                gateway.name,
                peer_type,
                peer_value,
                auth_type,
                ike_version
            ])
        
        table_headers = ["Name", "Peer Type", "Peer Value", "Auth Type", "IKE Version"]
        print("\nIKE gateways to create:")
        print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
    
    # Confirm before proceeding
    if not auto_approve and not dry_run:
        confirmed = typer.confirm(
            f"Do you want to create {len(gateways_to_create)} IKE gateways?"
        )
        if not confirmed:
            logger.info("❌ Operation cancelled by user")
            return
    
    if dry_run:
        logger.info(f"🏁 Dry run complete, would create {len(gateways_to_create)} IKE gateways")
        return
    
    # Create the gateways
    created_gateways = []
    failed_gateways = []
    
    for gateway in gateways_to_create:
        try:
            # Build create parameters
            create_params = build_create_params(
                source_object=gateway,
                destination_context=destination_context,
                destination_context_name=destination_context_name,
            )
            
            # Create gateway
            result = destination_ike_gateway.create(create_params)
            created_gateways.append(result)
            logger.info(f"✅ Created IKE gateway: {result.name}")
        except (InvalidObjectError, MissingQueryParameterError) as e:
            logger.error(f"❌ Failed to create IKE gateway {gateway.name}: {e}")
            failed_gateways.append((gateway.name, str(e)))
        except Exception as e:
            logger.error(f"❌ Unexpected error creating IKE gateway {gateway.name}: {e}")
            failed_gateways.append((gateway.name, str(e)))
    
    # Summary
    if not quiet:
        if created_gateways:
            logger.info(f"✅ Successfully created {len(created_gateways)} IKE gateways")
        
        if failed_gateways:
            logger.error(f"❌ Failed to create {len(failed_gateways)} IKE gateways")
            table_data = [[name, error] for name, error in failed_gateways]
            print(tabulate(table_data, headers=["Name", "Error"], tablefmt="grid"))
    
    return created_gateways


if __name__ == "__main__":
    app()