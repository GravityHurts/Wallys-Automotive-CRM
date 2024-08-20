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
    'date_completed': 'Date Completed',
    'vin': 'VIN',
    'repairs': 'Repairs Made',
    'labor_hours': 'Labor Hours',
    'labor_cost': 'Labor Cost $',
    'parts_cost': 'Parts Cost $',
    'mileage': 'Mileage',
    'id': 'ID',
    'work_order_number': 'Work Order #'
}

FIELD_HEADER_NAMES_RLOOKUP = {}
for k,v in FIELD_HEADER_NAMES.items():
    FIELD_HEADER_NAMES_RLOOKUP[v] = k
