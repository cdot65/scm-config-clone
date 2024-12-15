# scm_config_clone/utilities/parse_csv.py

from typing import Optional, List


def parse_csv_option(value: Optional[str]) -> Optional[List[str]]:
    """
    Parse a comma-separated string into a list of stripped strings.

    This utility function converts an option like "val1,val2,val3"
    into ["val1", "val2", "val3"]. If the input string is None
    or empty, it returns None.

    Args:
        value: The raw input string from a CLI option, possibly
            containing comma-separated values.

    Returns:
        A list of strings if values are present, or None if the input
        is empty or None.
    """
    if not value:
        return None
    return [v.strip() for v in value.split(",") if v.strip()]
