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
from scm.config.network import IKECryptoProfile
from scm.exceptions import (
    InvalidObjectError,
    MissingQueryParameterError,
    UnauthorizedError,
    ConnectionError,
)
from scm.models.network import (
    IKECryptoProfileResponseModel,
    IKECryptoProfileCreateModel,
)

app = typer.Typer()
logger = logging.getLogger(__name__)


def build_create_params(
    source_object: IKECryptoProfileResponseModel,
    destination_context: str,
    destination_context_name: str,
) -> Dict[str, Any]:
    """
    Build parameters for creating an IKE crypto profile in the destination tenant.

    Args:
        source_object: The source IKE crypto profile object
        destination_context: The destination context type ('folder', 'snippet', or 'device')
        destination_context_name: The name of the destination context

    Returns:
        Dict[str, Any]: Parameters for creating the IKE crypto profile
    """
    params = {
        "name": source_object.name,
        "hash": [h.value for h in source_object.hash],
        "encryption": [e.value for e in source_object.encryption],
        "dh_group": [dh.value for dh in source_object.dh_group],
    }

    # Add lifetime if it exists
    if source_object.lifetime:
        params["lifetime"] = source_object.lifetime.dict(exclude_unset=True)

    # Add authentication_multiple if it exists and is not None
    if source_object.authentication_multiple is not None:
        params["authentication_multiple"] = source_object.authentication_multiple

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
        help="Comma-separated list of IKE crypto profile names to clone",
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
    Clone IKE crypto profiles from source to destination tenant.
    
    This command clones IKE crypto profile objects based on the specified context
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
        logger.info(f"🔍 Filtering profiles by names: {', '.join(name_filter)}")
    
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
    
    # Initialize IKE crypto profile services
    source_ike_crypto_profile = IKECryptoProfile(source_client)
    destination_ike_crypto_profile = IKECryptoProfile(destination_client)
    
    # Fetch source profiles
    logger.info(f"🔍 Fetching IKE crypto profiles from source {source_context}: {source_context_name}")
    try:
        # Create kwargs for dynamic context parameter
        kwargs = {source_context: source_context_name}
        source_profiles = source_ike_crypto_profile.list(**kwargs)
        
        # Filter by name if specified
        if name_filter:
            source_profiles = [
                profile for profile in source_profiles 
                if profile.name in name_filter
            ]
        
        if not source_profiles:
            logger.warning(f"⚠️ No IKE crypto profiles found in source {source_context}")
            if name_filter:
                logger.warning(f"⚠️ Check if the specified names exist in the source {source_context}")
            return
        
        logger.info(f"✅ Found {len(source_profiles)} IKE crypto profiles in source {source_context}")
    except (InvalidObjectError, MissingQueryParameterError) as e:
        logger.error(f"❌ Failed to fetch source profiles: {e}")
        sys.exit(1)
    except (UnauthorizedError, ConnectionError) as e:
        logger.error(f"❌ Authentication or connection error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)
    
    # Fetch destination profiles to compare
    logger.info(f"🔍 Fetching IKE crypto profiles from destination {destination_context}: {destination_context_name}")
    try:
        # Create kwargs for dynamic context parameter
        kwargs = {destination_context: destination_context_name}
        destination_profiles = destination_ike_crypto_profile.list(**kwargs)
        
        logger.info(f"✅ Found {len(destination_profiles)} IKE crypto profiles in destination {destination_context}")
    except (InvalidObjectError, MissingQueryParameterError) as e:
        logger.error(f"❌ Failed to fetch destination profiles: {e}")
        sys.exit(1)
    except (UnauthorizedError, ConnectionError) as e:
        logger.error(f"❌ Authentication or connection error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)
    
    # Determine profiles to create (missing in destination)
    profiles_to_create = find_missing_objects(
        source_objects=source_profiles, 
        destination_objects=destination_profiles,
        name_attribute="name"
    )
    
    if not profiles_to_create:
        logger.info("✅ No new IKE crypto profiles to create")
        return
    
    # Display profiles to create
    if not quiet:
        table_data = [
            [profile.name, ",".join([h.value for h in profile.hash]), 
             ",".join([e.value for e in profile.encryption]),
             ",".join([dh.value for dh in profile.dh_group])]
            for profile in profiles_to_create
        ]
        
        table_headers = ["Name", "Hash Algorithms", "Encryption Algorithms", "DH Groups"]
        print("\nIKE crypto profiles to create:")
        print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
    
    # Confirm before proceeding
    if not auto_approve and not dry_run:
        confirmed = typer.confirm(
            f"Do you want to create {len(profiles_to_create)} IKE crypto profiles?"
        )
        if not confirmed:
            logger.info("❌ Operation cancelled by user")
            return
    
    if dry_run:
        logger.info(f"🏁 Dry run complete, would create {len(profiles_to_create)} IKE crypto profiles")
        return
    
    # Create the profiles
    created_profiles = []
    failed_profiles = []
    
    for profile in profiles_to_create:
        try:
            # Build create parameters
            create_params = build_create_params(
                source_object=profile,
                destination_context=destination_context,
                destination_context_name=destination_context_name,
            )
            
            # Create profile
            result = destination_ike_crypto_profile.create(create_params)
            created_profiles.append(result)
            logger.info(f"✅ Created IKE crypto profile: {result.name}")
        except (InvalidObjectError, MissingQueryParameterError) as e:
            logger.error(f"❌ Failed to create IKE crypto profile {profile.name}: {e}")
            failed_profiles.append((profile.name, str(e)))
        except Exception as e:
            logger.error(f"❌ Unexpected error creating IKE crypto profile {profile.name}: {e}")
            failed_profiles.append((profile.name, str(e)))
    
    # Summary
    if not quiet:
        if created_profiles:
            logger.info(f"✅ Successfully created {len(created_profiles)} IKE crypto profiles")
        
        if failed_profiles:
            logger.error(f"❌ Failed to create {len(failed_profiles)} IKE crypto profiles")
            table_data = [[name, error] for name, error in failed_profiles]
            print(tabulate(table_data, headers=["Name", "Error"], tablefmt="grid"))
    
    return created_profiles


if __name__ == "__main__":
    app()