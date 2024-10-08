import configparser
import re
from datetime import datetime
from . import config
from . import utils

DATE_FORMAT = '%Y-%m-%d'
DATE_FORMAT_WORK_ORDER_NUMBER = '%y%m%d'

now = datetime.now()
formatted_date = now.strftime(DATE_FORMAT)

file_path = 'data/settings.ini'
defaults = {
    'application': {
        'window title': "Wally's Automotive",
        'window size': '1280x720',
        'start fullscreen': True,
        'stretch columns': 'notes,repairs'
    },
    'new work orders': {
        'use last completed date': False,
        'use last work order date': False
    },
    'colors': {
        'colorful lists': True,
        'neutral standing': '#e6e1ff',
        'good standing': '#d5ffd7',
        'moderate standing': '#fffdd5',
        'poor standing': '#ffe4d5'
    },
    'internal_dates': {
        'last job creation': formatted_date,
        'last date selected': formatted_date,
        'last date completed': formatted_date,
        'current index': '1'
    },
    'column widths': config.DEFAULT_FIELD_HEADER_WIDTHS
}

def validate_settings():
    conf = load_ini_settings()

    resolution_pattern = r'^(\d{3,4})x(\d{3,4})$'
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

def save_settings(restart=False):
    """Save settings to an INI file."""
    cfp = configparser.ConfigParser()
    
    for section, keys in config.items():
        cfp[section] = {}
        for key, value in keys.items():
            cfp[section][key] = str(value)
    
    with open(file_path, 'w') as configfile:
        cfp.write(configfile)

    if restart:
        utils.restart_script()

config = validate_settings()

utils.register_exit(save_settings)

# test usage
if __name__ == "__main__":
    for section, options in config.items():
        print(f"Section: {section}")
        for key, value in options.items():
            print(f"{key} = {value}")
