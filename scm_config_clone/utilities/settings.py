# scm_config_clone/config/settings.py

from dynaconf import Dynaconf
from typing import Dict
import logging

logger = logging.getLogger(__name__)


def load_settings(settings_file: str) -> Dict[str, Dict[str, str]]:
    """
    Load settings from a YAML configuration file.

    Reads the settings file and extracts source and destination SCM authentication details.

    Args:
        settings_file (str): Path to the YAML settings file.

    Error:
        Exception: Raises an exception if an error occurs during loading.

    Return:
        Dict[str, Dict[str, str]]: A dictionary containing source and destination SCM configurations.
    """
    try:
        settings = Dynaconf(settings_files=[settings_file])
        source_scm = {
            "client_id": settings.oauth.source.client_id,
            "client_secret": settings.oauth.source.client_secret,
            "tenant": settings.oauth.source.tsg,
            "token_url": settings.oauth.token_url,
            "folder": settings.oauth.source.folder,
        }
        destination_scm = {
            "client_id": settings.oauth.destination.client_id,
            "client_secret": settings.oauth.destination.client_secret,
            "tenant": settings.oauth.destination.tsg,
            "token_url": settings.oauth.token_url,
            "folder": settings.oauth.destination.folder,
        }
        return {
            "source_scm": source_scm,
            "destination_scm": destination_scm,
        }
    except Exception as e:
        logger.error(f"Error loading settings from {settings_file}: {e}")
        raise
