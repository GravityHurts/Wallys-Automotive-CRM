from . import sql

COLUMN_INITIAL_WIDTH = 10

class DBObject:
    def __init__(self, table_name, **kwargs):
        self.db = sql.Database()
        self.table_name = table_name
        self.excludes = ['excludes', 'db', 'table_name']

        # Fetch the schema regardless of whether kwargs are provided
        table_info = self.db.get_table_info(self.table_name)

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

    def __str__(self):
        #return f'ID: {self.id} - {self.firstname} {self.lastname} {self.phone}'
        return f'{self.firstname} {self.lastname} {self.phone}'
    
class Vehicle(DBObject):
    def __init__(self, **kwargs):
        super().__init__('vehicles', **kwargs)
        
        if (self.customer_id == 'NULL'):
            self.customer_id = ''
        
        self.firstname = getattr(self, 'firstname', '') or ''
        self.lastname = getattr(self, 'lastname', '') or ''
        if (self.firstname+self.lastname == ''):
            self.id_string = "No Customer"
        else:
            #self.id_string    = f"ID: {self.customer_id} - {firstname} {lastname}"
            self.id_string    = f"{self.firstname} {self.lastname}"
        
    def __str__(self):
        return f'{self.year} {self.make} {self.model} {self.vin}'

class Job(DBObject):
    def __init__(self, **kwargs):
        super().__init__('jobs', **kwargs)

        self.year = getattr(self, 'year', '') or ''
        self.make = getattr(self, 'make', '') or ''
        self.model = getattr(self, 'model', '') or ''
        if ((str(self.year)+str(self.make)+str(self.model)) == ''):
            self.id_string = "No Vehicle??"
        else:
            self.id_string    = f"{self.year} {self.make} {self.model}"

