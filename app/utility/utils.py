from .config import FIELD_HEADER_NAMES

def singleton(class_):
    """
    Decorator to implement the singleton pattern for a class.

    Parameters:
    class_ (class): The class to be decorated as a singleton.

    Returns:
    function: A closure that ensures only one instance of the class exists and returns that instance.

    Note:
    - The singleton pattern ensures that only one instance of the decorated class is created and shared across all
      subsequent calls.
    - The first time the decorated class is instantiated with specific arguments (if any), a new instance is created.
    - Subsequent calls with the same arguments will return the previously created instance.
    - If no arguments are provided during instantiation, the same instance will be shared among all calls.
    """
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

def convert_to_property_display(data, header_names=FIELD_HEADER_NAMES):
    """
    Convert the given data dictionary to a property:display dictionary using the provided header names.

    Parameters:
        data (dict): A dictionary containing field names and their data types.
        header_names (dict): A dictionary containing field names and their corresponding display names.

    Returns:
        dict: A new dictionary with field names as keys and corresponding display names as values.
    """
    property_display_dict = {}
    for field, data_type in data.items():
        display_name = header_names.get(field, field.capitalize())
        property_display_dict[field] = display_name

    return property_display_dict
