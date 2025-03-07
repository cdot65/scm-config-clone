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
from scm.config.network import IPsecCryptoProfile
from scm.exceptions import (
    InvalidObjectError,
    MissingQueryParameterError,
    UnauthorizedError,
    ConnectionError,
)
from scm.models.network import (
    IPsecCryptoProfileResponseModel,
    IPsecCryptoProfileCreateModel,
)

app = typer.Typer()
logger = logging.getLogger(__name__)


def build_create_params(
    source_object: IPsecCryptoProfileResponseModel,
    destination_context: str,
    destination_context_name: str,
) -> Dict[str, Any]:
    """
    Build parameters for creating an IPsec crypto profile in the destination tenant.

    Args:
        source_object: The source IPsec crypto profile object
        destination_context: The destination context type ('folder', 'snippet', or 'device')
        destination_context_name: The name of the destination context

    Returns:
        Dict[str, Any]: Parameters for creating the IPsec crypto profile
    """
    # Basic parameters
    params = {
        "name": source_object.name,
    }

    # Add DH group if exists
    if source_object.dh_group:
        params["dh_group"] = source_object.dh_group.value

    # Add lifetime if exists
    if source_object.lifetime:
        params["lifetime"] = source_object.lifetime.dict(exclude_unset=True)

    # Add lifesize if exists
    if source_object.lifesize:
        params["lifesize"] = source_object.lifesize.dict(exclude_unset=True)

    # Add ESP configuration if exists
    if source_object.esp:
        params["esp"] = {
            "encryption": [e.value for e in source_object.esp.encryption],
            "authentication": [a.value for a in source_object.esp.authentication]
        }

    # Add AH configuration if exists
    if source_object.ah:
        params["ah"] = {
            "authentication": [a.value for a in source_object.ah.authentication]
        }

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
        help="Comma-separated list of IPsec crypto profile names to clone",
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
    Clone IPsec crypto profiles from source to destination tenant.
    
    This command clones IPsec crypto profile objects based on the specified context
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
    
    # Initialize IPsec crypto profile services
    source_ipsec_crypto_profile = IPsecCryptoProfile(source_client)
    destination_ipsec_crypto_profile = IPsecCryptoProfile(destination_client)
    
    # Fetch source profiles
    logger.info(f"🔍 Fetching IPsec crypto profiles from source {source_context}: {source_context_name}")
    try:
        # Create kwargs for dynamic context parameter
        kwargs = {source_context: source_context_name}
        source_profiles = source_ipsec_crypto_profile.list(**kwargs)
        
        # Filter by name if specified
        if name_filter:
            source_profiles = [
                profile for profile in source_profiles 
                if profile.name in name_filter
            ]
        
        if not source_profiles:
            logger.warning(f"⚠️ No IPsec crypto profiles found in source {source_context}")
            if name_filter:
                logger.warning(f"⚠️ Check if the specified names exist in the source {source_context}")
            return
        
        logger.info(f"✅ Found {len(source_profiles)} IPsec crypto profiles in source {source_context}")
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
    logger.info(f"🔍 Fetching IPsec crypto profiles from destination {destination_context}: {destination_context_name}")
    try:
        # Create kwargs for dynamic context parameter
        kwargs = {destination_context: destination_context_name}
        destination_profiles = destination_ipsec_crypto_profile.list(**kwargs)
        
        logger.info(f"✅ Found {len(destination_profiles)} IPsec crypto profiles in destination {destination_context}")
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
        logger.info("✅ No new IPsec crypto profiles to create")
        return
    
    # Display profiles to create
    if not quiet:
        table_data = []
        for profile in profiles_to_create:
            # Determine profile type
            profile_type = "ESP" if profile.esp else "AH" if profile.ah else "Unknown"
            
            # Extract encryption algorithms for ESP
            encryption = "N/A"
            if profile.esp and profile.esp.encryption:
                encryption = ", ".join([e.value for e in profile.esp.encryption])
            
            # Extract authentication algorithms for ESP or AH
            auth_algorithms = []
            if profile.esp and profile.esp.authentication:
                auth_algorithms.extend([a.value for a in profile.esp.authentication])
            if profile.ah and profile.ah.authentication:
                auth_algorithms.extend([a.value for a in profile.ah.authentication])
            
            authentication = ", ".join(auth_algorithms) if auth_algorithms else "N/A"
            
            # DH Group
            dh_group = profile.dh_group.value if profile.dh_group else "None"
            
            # Lifetime
            lifetime = "N/A"
            if profile.lifetime:
                if hasattr(profile.lifetime, 'seconds') and profile.lifetime.seconds:
                    lifetime = f"{profile.lifetime.seconds} seconds"
                elif hasattr(profile.lifetime, 'minutes') and profile.lifetime.minutes:
                    lifetime = f"{profile.lifetime.minutes} minutes"
                elif hasattr(profile.lifetime, 'hours') and profile.lifetime.hours:
                    lifetime = f"{profile.lifetime.hours} hours"
                elif hasattr(profile.lifetime, 'days') and profile.lifetime.days:
                    lifetime = f"{profile.lifetime.days} days"
            
            # Add to table data
            table_data.append([
                profile.name,
                profile_type,
                encryption,
                authentication,
                dh_group,
                lifetime
            ])
        
        table_headers = ["Name", "Type", "Encryption", "Authentication", "DH Group", "Lifetime"]
        print("\nIPsec crypto profiles to create:")
        print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
    
    # Confirm before proceeding
    if not auto_approve and not dry_run:
        confirmed = typer.confirm(
            f"Do you want to create {len(profiles_to_create)} IPsec crypto profiles?"
        )
        if not confirmed:
            logger.info("❌ Operation cancelled by user")
            return
    
    if dry_run:
        logger.info(f"🏁 Dry run complete, would create {len(profiles_to_create)} IPsec crypto profiles")
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
            result = destination_ipsec_crypto_profile.create(create_params)
            created_profiles.append(result)
            logger.info(f"✅ Created IPsec crypto profile: {result.name}")
        except (InvalidObjectError, MissingQueryParameterError) as e:
            logger.error(f"❌ Failed to create IPsec crypto profile {profile.name}: {e}")
            failed_profiles.append((profile.name, str(e)))
        except Exception as e:
            logger.error(f"❌ Unexpected error creating IPsec crypto profile {profile.name}: {e}")
            failed_profiles.append((profile.name, str(e)))
    
    # Summary
    if not quiet:
        if created_profiles:
            logger.info(f"✅ Successfully created {len(created_profiles)} IPsec crypto profiles")
        
        if failed_profiles:
            logger.error(f"❌ Failed to create {len(failed_profiles)} IPsec crypto profiles")
            table_data = [[name, error] for name, error in failed_profiles]
            print(tabulate(table_data, headers=["Name", "Error"], tablefmt="grid"))
    
    return created_profiles


if __name__ == "__main__":
    app()