import configparser
import atexit
import re

file_path = 'data/settings.ini'
defaults = {
    'application': {
        'window title': "Wally's Automotive",
        'window size': '1280x720',
        'start fullscreen': True
    },
    'colors': {
        'linked entry': 'lightblue',
        'good standing': 'lightgreen',
        'moderate standing': 'lightyellow',
        'poor standing': 'lightred'
    }
}

def validate_settings():
    conf = load_ini_settings()

    resolution_pattern = r'^(\d{3,4})x(\d{3,4}})$'        
    if not re.match(resolution_pattern, conf['application']['window size']):
        conf['application']['window size'] = defaults['application']['window size']

    return conf

def load_ini_settings():
    """Load settings from an INI file."""
    cfp = configparser.ConfigParser()
    cfp.read(file_path)
    
    # Create a dictionary to hold the settings
    conf = {}
    
    if len(cfp.sections()) > 0:
        for section in cfp.sections():
            conf[section] = {}
            for key, value in cfp.items(section):
                if value.lower() in ['true', 'false', 'yes', 'no']:
                    if value.lower() == 'true' or value.lower() == 'yes':
                        conf[section][key] = True
                    else:
                        conf[section][key] = False
                else:
                    conf[section][key] = value
        
        # Load defaults for non-existent key/values
        for section, section_keys in defaults.items():
            if not section in conf:
                conf[section] = {}
            
            for k,v in section_keys.items():
                if not k in conf[section]:
                    conf[section][k] = v
    else:
        # Default Settings
        conf = defaults
    
    return conf

def save_settings():
    """Save settings to an INI file."""
    cfp = configparser.ConfigParser()
    
    for section, keys in config.items():
        cfp[section] = {}
        for key, value in keys.items():
            cfp[section][key] = str(value)
    
    with open(file_path, 'w') as configfile:
        cfp.write(configfile)

config = validate_settings()

atexit.register(save_settings)

# test usage
if __name__ == "__main__":
    for section, options in config.items():
        print(f"Section: {section}")
        for key, value in options.items():
            print(f"{key} = {value}")
