from .config import FIELD_HEADER_NAMES
import os
import sys
import atexit

logfile = open("logs/app-log.txt", "a")

class DualWriter:
    def __init__(self, file):
        self.file = file

    def write(self, message):
        # Write to the console
        sys.__stdout__.write(message)
        # Write to the file
        self.file.write(message)

    def flush(self):
        # Ensure the output is flushed to both streams
        sys.__stdout__.flush()
        self.file.flush()
    
    def close(self):
        self.file.close()

dual_writer = DualWriter(logfile)

sys.stdout = dual_writer
sys.stderr = dual_writer 

def register_exit(test):
    atexit.register(test)
    atexit.register(dual_writer.close)

def restart_script():
    """Restarts the current script."""
    print("Restarting script...")
    os.execv(sys.executable, ['python'] + sys.argv)

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

def darken_hex_color(hex_color, factor=0.9):
    # Ensure the hex_color starts with '#'
    hex_color = hex_color.lstrip('#')
    
    # Convert hex to RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Apply darkening factor
    darkened_rgb = tuple(max(0, int(c * factor)) for c in rgb)
    
    # Convert RGB back to hex
    darkened_hex = '#{:02x}{:02x}{:02x}'.format(*darkened_rgb)
    
    return darkened_hex

def lighten_hex_color(hex_color, factor=0.1):
    # Ensure the hex_color starts with '#'
    hex_color = hex_color.lstrip('#')
    
    # Convert hex to RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Apply lightening factor
    lightened_rgb = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
    
    # Convert RGB back to hex
    lightened_hex = '#{:02x}{:02x}{:02x}'.format(*lightened_rgb)
    
    return lightened_hex
