def compare_object_lists(source_objects: list, destination_objects: list) -> list:
    """
    Compare two lists of objects (source and destination) and determine
    which source objects are already configured on the destination.

    Args:
        source_objects: A list of objects from the source.
                        Each object should have a 'name' attribute.
        destination_objects: A list of objects from the destination.
                             Each object should have a 'name' attribute.

    Returns:
        A list of dictionaries. Each dictionary has:
            "name": the object's name (string)
            "already_configured": boolean indicating if the object
                                  exists in the destination.
    """
    # Create a set of names from the destination to allow O(1) lookups
    destination_names = {obj.name for obj in destination_objects}

    results = []
    for src_obj in source_objects:
        results.append(
            {
                "name": src_obj.name,
                "already_configured": src_obj.name in destination_names,
            }
        )

    return results


def find_missing_objects(source_objects: list, destination_objects: list, name_attribute: str = 'name') -> list:
    """
    Compare two lists of objects and return the source objects that are not present in the destination.

    Args:
        source_objects: A list of objects from the source.
        destination_objects: A list of objects from the destination.
        name_attribute: The attribute to use for comparison (default: 'name').

    Returns:
        A list of source objects that are not present in the destination.
    """
    # Create a set of names from the destination for O(1) lookups
    destination_names = {getattr(obj, name_attribute) for obj in destination_objects}
    
    # Return objects from source that are not in destination
    return [obj for obj in source_objects if getattr(obj, name_attribute) not in destination_names]
