import sqlite3
from app.utility.types import Customer, Vehicle, Job, DBObject
from .functions import singleton
from collections import namedtuple

DB_NAME = "mechanic_app.db"

FIELD_HEADER_NAMES = {
    'customer_id': 'Customer',
    'vehicle_id': 'Vehicle',
    'firstname': 'First Name',
    'lastname': 'Last Name',
    'email': 'E-Mail',
    'phone': 'Phone',
    'address': 'Address',
    'notes': 'Notes',
    'year': 'Year',
    'make': 'Make',
    'model': 'Model',
    'vin': 'VIN',
    'description': 'Description',
    'cost': 'Cost',
    'mileage_in': 'Mileage In',
    'mileage_out': 'Mileage Out'
}

@singleton
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()   

    def close(self):
        self.conn.close()

    def get_table_info(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return {column[1]: column[2] for column in self.cursor.fetchall()}  # map column names to data types

    def create_row(self, table_name, keys_values):
        keys_clause = ", ".join(keys_values.keys())
        placeholders = ", ".join(["?" for _ in keys_values])
        sql_query = f"INSERT INTO {table_name} ({keys_clause}) VALUES ({placeholders})"

        self.cursor.execute(sql_query, list(keys_values.values()))
        self.conn.commit()

    def update_row(self, table_name, keys_values):
        # Prevent irrelevant columns making it here
        cols = self.get_table_info(table_name).keys()
        keys_values = {key: value for key, value in keys_values.items() if key in cols}

        if ('id' not in keys_values.keys()): 
            return self.create_row(table_name, keys_values)

        set_clause = ", ".join([f"{key}=?" for key in keys_values.keys()])
        sql_query = f"UPDATE {table_name} SET {set_clause} WHERE id=?"

        self.cursor.execute(sql_query, list(keys_values.values()) + [keys_values.get('id')])
        self.conn.commit()

    def delete_row(self, table_name, id):
        sql_query = f"DELETE FROM {table_name} WHERE id=?"
        self.cursor.execute(sql_query, (id,))
        self.conn.commit()

    def read_row(self, table_name, id):
        sql_query = f"SELECT * FROM {table_name} WHERE id=?"
        self.cursor.execute(sql_query, (id,))
        row = self.cursor.fetchone()
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            row_dict = dict(zip(columns, row))
            return self.get_object(table_name, **row_dict)
        else:
            return None

    def search_rows(self, table_name, select='*', left_join='', search_query='', offset=None, page_size=None):
        sql_query = f"SELECT {select} FROM {table_name} "

        if left_join != '':
            sql_query += f"LEFT JOIN {left_join} "

        if search_query != '':
            sql_query += f"WHERE {search_query} "

        if offset is not None and page_size is not None:
            sql_query += f"LIMIT {offset},{page_size}"

        self.cursor.execute(sql_query)
        rows = self.cursor.fetchall()
        db_objects = []
        if rows:
            columns = [desc[0] for desc in self.cursor.description]
            for row in rows:
                row_dict = dict(zip(columns, row))
                db_objects.append(self.get_object(table_name, **row_dict))
        return db_objects

    def get_object(self, table_name, **row_dict):
        table_map = {
            'vehicles': Vehicle,
            'customers': Customer,
            'jobs': Job
        }
        return table_map[table_name](**row_dict)
    
    def initialize_db(self): 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                firstname TEXT,
                lastname TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                notes TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                year INTEGER,
                make TEXT,
                model TEXT,
                vin TEXT,
                notes TEXT,
                FOREIGN KEY (customer_id) 
                            REFERENCES customers(id)
                            ON DELETE SET NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                vehicle_id INTEGER,
                description TEXT,
                notes TEXT,
                cost TEXT,
                mileage_in INTEGER,
                mileage_out INTEGER,
                FOREIGN KEY (vehicle_id) 
                            REFERENCES vehicles(id)
                            ON DELETE SET NULL
            )
        ''')

        self.conn.commit()

@singleton
class SQLConnection:
    def __init__(self):
        self.db = Database()
        self.db.initialize_db()
        self.close = self.db.close
        self.get_table_info = self.db.get_table_info

    # CUSTOMER QUERIES
    def id_customer(self, id):
        if id == '': return None
        return self.db.read_row('customers', id)

    def search_customers(self, text="", page=1, page_size=25):
        offset = (page-1) * 1 # the offset value of what "page" we're on

        keys = self.db.get_table_info('customers').keys()
        search = ' OR '.join([f"{col} LIKE '%{text}%'" for col in keys]) 
        
        return self.db.search_rows('customers', search_query=search, offset=offset, page_size=page_size)

    # VEHICLE QUERIES
    def id_vehicle(self, id):
        if id == '': return None
        return self.db.read_row('vehicles', id)

    def search_vehicles(self, text="", page=1, page_size=25):
        offset = (page-1) * page_size  # the offset value of what "page" we're on

        select = 'vehicles.*, customers.firstname, customers.lastname'
        left_join = 'customers ON customers.id = vehicles.customer_id'

        keys = ['vehicles.'+key for key in self.db.get_table_info('vehicles').keys()]
        keys += ['customers.firstname', 'customers.lastname']
        search = ' OR '.join([f"{col} LIKE '%{text}%'" for col in keys]) 
        
        return self.db.search_rows('vehicles', select=select, left_join=left_join, search_query=search, offset=offset, page_size=page_size)

    # JOB QUERIES
    def id_job(self, id):
        if id == '': return None
        return self.db.read_row('jobs', id)
    
    def search_jobs(self, text="", page=1, page_size=25):
        offset = (page-1) * page_size  # the offset value of what "page" we're on

        select = 'jobs.*, vehicles.year, vehicles.make, vehicles.model'
        left_join = 'vehicles ON vehicles.id = jobs.vehicle_id'

        keys = ['jobs.'+key for key in self.db.get_table_info('jobs').keys()]
        keys += ['vehicles.year', 'vehicles.make', 'vehicles.model']
        search = ' OR '.join([f"{col} LIKE '%{text}%'" for col in keys]) 
        
        return self.db.search_rows('jobs', select=select, left_join=left_join, search_query=search, offset=offset, page_size=page_size)

