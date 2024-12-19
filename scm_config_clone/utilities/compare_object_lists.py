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
