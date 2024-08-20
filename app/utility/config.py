from . import settings

FIELD_HEADER_NAMES = {
    'customer_id': 'Customer',
    'vehicle_id': 'Vehicle',
    'firstname': 'First Name',
    'lastname': 'Last Name',
    'email': 'E-Mail',
    'phone': 'Phone',
    'street_address': 'Street Address',
    'city_address': 'City',
    'state_address': 'State',
    'zip_address': 'ZIP Code',
    'notes': 'Notes',
    'year': 'Year',
    'make': 'Make',
    'model': 'Model',
    'licence_number': 'Licence Plate',
    'date_completed': 'Completed',
    'vin': 'VIN',
    'repairs': 'Repairs Made',
    'labor_hours': 'Labor Hours',
    'labor_cost': 'Labor Cost $',
    'parts_cost': 'Parts Cost $',
    'mileage': 'Mileage',
    'id': 'ID',
    'work_order_number': 'Work Order #'
}

DEFAULT_WIDTH = int(settings.config['application']['default column width'])
FIELD_HEADER_WIDTHS = {
    'customer_id':       int(DEFAULT_WIDTH * 2.25),
    'vehicle_id':        int(DEFAULT_WIDTH * 2.25),
    'firstname':         int(DEFAULT_WIDTH * 1.3),
    'lastname':          int(DEFAULT_WIDTH * 1.3),
    'email':             int(DEFAULT_WIDTH * 2.0),
    'phone':             int(DEFAULT_WIDTH * 1.125),
    'street_address':    int(DEFAULT_WIDTH * 2.25),
    'city_address':      int(DEFAULT_WIDTH * 0.9),
    'state_address':     int(DEFAULT_WIDTH * 0.8),
    'zip_address':       int(DEFAULT_WIDTH * 1.0),
    'notes':             int(DEFAULT_WIDTH * 1.0),
    'year':              int(DEFAULT_WIDTH * 0.75),
    'make':              int(DEFAULT_WIDTH * 1.0),
    'model':             int(DEFAULT_WIDTH * 1.0),
    'licence_number':    int(DEFAULT_WIDTH * 1.0),
    'date_completed':    int(DEFAULT_WIDTH * 1.125),
    'vin':               int(DEFAULT_WIDTH * 1.125),
    'repairs':           int(DEFAULT_WIDTH * 1.0),
    'labor_hours':       int(DEFAULT_WIDTH * 1.0),
    'labor_cost':        int(DEFAULT_WIDTH * 1.0),
    'parts_cost':        int(DEFAULT_WIDTH * 1.0),
    'mileage':           int(DEFAULT_WIDTH * 1.0),
    'id':                int(DEFAULT_WIDTH * 1.0),
    'work_order_number': int(DEFAULT_WIDTH * 1.1)
}

FIELD_HEADER_NAMES_RLOOKUP = {}
for k,v in FIELD_HEADER_NAMES.items():
    FIELD_HEADER_NAMES_RLOOKUP[v] = k
