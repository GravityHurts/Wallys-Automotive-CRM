from . import sql
from .utils import convert_to_property_display
from datetime import datetime

from ..utility import settings

class DBObject:
    """
    Represents a database object with common functionalities for interacting with database tables.

    Parameters:
    table_name (str): The name of the database table associated with the object.
    **kwargs: Additional keyword arguments to initialize the object's attributes.

    Attributes:
    db (sql.Database): The database instance used for interactions.
    table_name (str): The name of the associated database table.
    excludes (list): A list of attributes to exclude when saving to the database.

    Methods:
    to_tuple(): Converts the object's attributes to a tuple for database operations.
    get_value(key): Retrieves the value of the specified attribute.
    save(): Saves the object's attributes to the database table.
    delete(): Deletes the corresponding row from the database table.

    Note:
    - This class provides a foundation for interacting with various database tables.
    - When creating subclasses, specify the 'table_name' parameter to set the associated database table.
    - The class automatically fetches the table schema based on 'table_name' during initialization.
    - The attributes are initialized with provided values from **kwargs or default values based on the schema.
    - Certain attributes, specified in the 'excludes' list, are not saved to the database.
    - 'to_tuple()' method is used to convert the attributes to a tuple before database operations.
    - 'get_value(key)' method returns the value of the specified attribute or id_string if the attribute ends with '_id'.
    - 'save()' method updates the corresponding row in the database table with the current attribute values.
    - 'delete()' method deletes the row from the database if the object has a non-empty 'id' attribute.
    """
    def __init__(self, table_name, **kwargs):
        self.db = sql.Database()
        self.table_name = table_name
        self.excludes = ['property_display', 'excludes', 'db', 'table_name']

        # Fetch the schema regardless of whether kwargs are provided
        table_info = self.db.get_table_info(self.table_name)

        self.property_display = convert_to_property_display(table_info)

        # mark excludes for when we save to DB
        extra_keys = list(set(kwargs.keys()) - set(table_info.keys()))

        for key, data_type in table_info.items():
            # Use the kwarg value if provided, else use a default value
            default_value = '' #if data_type == 'TEXT' else 0
            setattr(self, key, kwargs.get(key, default_value))

        for key in extra_keys:
            setattr(self, key, kwargs.get(key, ''))
        
        self.excludes += extra_keys

    def to_tuple(self):
        return tuple(self.get_value(key) for key in vars(self) if key not in self.excludes)
        
    def get_value(self, key):
        if key.endswith('_id'):
            return self.id_string
        else:
            return getattr(self, key)
    
    def save(self):
        keys_values = {key: getattr(self, key) for key in self.__dict__.keys() if key not in self.excludes}
        self.db.update_row(self.table_name, keys_values)

    def delete(self):
        if hasattr(self, 'id'):
            if self.id != '' and self.id != 'NULL':
                self.db.delete_row(self.table_name, self.id)

class Customer(DBObject):
    def __init__(self, **kwargs):
        super().__init__('customers', **kwargs)
        if not hasattr(self,'status') or self.status == '' or self.status == None:
            self.status = 'neutral' 

    def __str__(self):
        return f'{self.fullname} {self.phone}'
    
class Vehicle(DBObject):
    def __init__(self, **kwargs):
        super().__init__('vehicles', **kwargs)
        
        if (self.customer_id == 'NULL'):
            self.customer_id = ''
        
        self.fullname = getattr(self, 'fullname', '') or ''
        if (self.fullname == ''):
            self.id_string = "No Customer"
        else:
            self.id_string    = self.fullname

        if (self.licence_number is None or self.licence_number == ''):
            self.licence_number = 'OH-'
        
    def __str__(self):
        return f"{self.id_string}: {self.year} {self.make} {self.model} - '{self.licence_number}'"

class Job(DBObject):
    def __init__(self, **kwargs):
        super().__init__('jobs', **kwargs)
        
        if (hasattr(self, 'customer_id') and self.customer_id == 'NULL'):
            self.customer_id = ''
        
        self.fullname = getattr(self, 'fullname', '') or ''
        if (self.fullname == ''):
            self.c_id_string = "No Customer"
        else:
            self.c_id_string    = self.fullname

        self.year = getattr(self, 'year', '') or ''
        self.make = getattr(self, 'make', '') or ''
        self.model = getattr(self, 'model', '') or ''
        self.licence_number = getattr(self, 'licence_number', '') or ''
        if ((str(self.year)+str(self.make)+str(self.model)+str(self.licence_number)) == ''):
            self.id_string = "No Vehicle??"
        else:
            self.id_string    = f"{self.c_id_string}: {self.year} {self.make} {self.model} - '{self.licence_number}'"

        if not hasattr(self, 'work_order_number') or self.work_order_number == '':
            self.labor_cost = 0
            self.parts_cost = 0
            self.labor_hours = 0
            dt = datetime.now()
            self.date_completed = dt.strftime(settings.DATE_FORMAT)
            if settings.config['dates']['last job creation'] != self.date_completed:
                settings.config['dates']['current index'] = '1'

            self.won = str(settings.config['dates']['current index']).zfill(2)
            wn = dt.strftime(settings.DATE_FORMAT_WORK_ORDER_NUMBER)
            self.work_order_number = f'{wn}{self.won}'

    def save(self):
        try:
            float(self.labor_hours)
        except ValueError:
            raise ValueError(f"Error: {self.property_display['labor_hours']} is not a number")
            
        try:
            float(self.labor_cost)
        except ValueError:
            raise ValueError(f"Error: {self.property_display['labor_cost']} is not a number")

        try:
            float(self.parts_cost)
        except ValueError:
            raise ValueError(f"Error: {self.property_display['parts_cost']} is not a number")
            
        super().save()
        if hasattr(self, 'won') and self.won is not None:
            settings.config['dates']['current index'] = str(int(settings.config['dates']['current index'])+1)

            

            

