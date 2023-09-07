import sqlite3
from app.utility.types import Customer, Vehicle, Job
from .utils import singleton
from .config import FIELD_HEADER_NAMES

DB_NAME = "mechanic_app.db"

@singleton
class Database:
    """
    Represents a SQLite database connection and provides methods for interacting with database tables.

    Attributes:
    conn: The SQLite database connection object.
    cursor: The SQLite cursor object for executing SQL queries.

    Methods:
    close(): Closes the database connection.
    get_table_info(table_name): Retrieves information about the columns of the specified table.
    create_row(table_name, keys_values): Inserts a new row into the specified table with the provided data.
    update_row(table_name, keys_values): Updates an existing row in the specified table with the provided data.
    delete_row(table_name, id): Deletes a row with the given 'id' from the specified table.
    read_row(table_name, id): Retrieves a single row from the specified table with the given 'id'.
    search_rows(table_name, select='*', left_join='', search_query='', offset=None, page_size=None):
        Searches for rows in the specified table that match the provided 'search_query'.
    get_object(table_name, **row_dict): Returns an instance of the corresponding class mapped to the 'table_name'.

    Note:
    - This class encapsulates database-related operations using SQLite.
    - It provides functionalities to perform CRUD operations on different database tables.
    - The class is designed to work with specific table schemas (customers, vehicles, jobs) and their corresponding classes.
    - The 'initialize_db()' method creates the necessary tables if they don't exist.
    - It supports queries to retrieve, insert, update, and delete data from the database.
    - The 'search_rows()' method allows searching for rows based on text matching in the specified columns.
    - The 'get_object()' method is used to map database rows to corresponding class instances.
    """
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()   

    def close(self):
        self.conn.close()

    def get_table_info(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return {column[1]: column[2] for column in self.cursor.fetchall()}  # map column names to data types

    def create_row(self, table_name, keys_values):
        keys_values = {key: value for key, value in keys_values.items() if key != 'id'}

        keys_clause = ", ".join(keys_values.keys())
        placeholders = ", ".join(["?" for _ in keys_values])
        sql_query = f"INSERT INTO {table_name} ({keys_clause}) VALUES ({placeholders})"

        self.cursor.execute(sql_query, list(keys_values.values()))
        self.conn.commit()

    def update_row(self, table_name, keys_values):
        # Prevent irrelevant columns making it here
        cols = self.get_table_info(table_name).keys()
        keys_values = {key: value for key, value in keys_values.items() if key in cols}

        if ('id' not in keys_values or keys_values['id'] == '' or keys_values['id'] == None): 
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

    def search_rows(self, table_name, select='*', left_join='', search_query='', offset=None, page_size=None, sort=None):
        sql_query = f"SELECT {select} FROM {table_name} "

        if left_join != '':
            sql_query += f"LEFT JOIN {left_join} "

        if search_query != '':
            sql_query += f"WHERE {search_query} "
            
        if sort is not None and sort["method"] != "NONE" and sort["column"] != "":
            sql_query += f"ORDER BY {sort['column']} {sort['method']} "

        if offset is not None and page_size is not None:
            sql_query += f"LIMIT {offset},{page_size} "
            

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
                licence_number TEXT,
                licence_state TEXT,
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
                date_in DATE,
                repairs TEXT,
                labor_hours REAL,
                labor_hourly_rate REAL,
                parts_cost REAL,
                mileage INTEGER,
                notes TEXT,
                FOREIGN KEY (vehicle_id) 
                            REFERENCES vehicles(id)
                            ON DELETE SET NULL
            )
        ''')

        self.conn.commit()

@singleton
class SQLConnection:
    """
    Represents a singleton instance of an SQLite database connection.

    Note:
    - This class is a singleton created using the 'singleton' decorator.
    - It provides access to a single instance of the 'Database' class throughout the application.
    - The 'db' attribute represents the underlying 'Database' instance.
    - The class offers convenience methods for querying specific tables (customers, vehicles, jobs).
    - The methods retrieve data from the 'Database' instance and return relevant class instances.
    - It facilitates searching and retrieving paginated data from different tables.
    - Use this class to interact with the database in a consistent and efficient manner.

    Methods:
    close(): Closes the underlying database connection.
    get_table_info(table_name): Retrieves information about the columns of the specified table.
    id_customer(id): Retrieves a customer from the database with the specified 'id'.
    search_customers(text="", page=1, page_size=25): Searches for customers in the database based on the provided search 'text'.
    id_vehicle(id): Retrieves a vehicle from the database with the specified 'id'.
    search_vehicles(text="", page=1, page_size=25): Searches for vehicles in the database based on the provided search 'text'.
    id_job(id): Retrieves a job from the database with the specified 'id'.
    search_jobs(text="", page=1, page_size=25): Searches for jobs in the database based on the provided search 'text'.

    Note:
    - The class uses the 'singleton' decorator to ensure a single instance of the 'Database' class is utilized
      across all calls, promoting resource efficiency and data consistency.
    - It provides methods to access specific tables (customers, vehicles, jobs) in a structured manner,
      allowing retrieval of relevant class instances and data based on specific queries.
    - The 'search_customers()', 'search_vehicles()', and 'search_jobs()' methods support text-based search
      within the respective tables, enabling easy data retrieval based on user input.
    - The 'id_customer()', 'id_vehicle()', and 'id_job()' methods allow fetching individual records
      from the respective tables using their unique 'id' attribute.
    - Use this class as the main entry point for performing database operations in the application.
    """
    def __init__(self):
        self.db = Database()
        self.db.initialize_db()
        self.close = self.db.close
        self.get_table_info = self.db.get_table_info

    # CUSTOMER QUERIES
    def id_customer(self, id):
        if id == '': return None
        return self.db.read_row('customers', id)

    def search_customers(self, text="", page=1, page_size=25, sort=None):
        offset = (page-1) * 1 # the offset value of what "page" we're on

        keys = self.db.get_table_info('customers').keys()
        search = ' OR '.join([f"{col} LIKE '%{text}%'" for col in keys]) 
        
        return self.db.search_rows('customers', search_query=search, offset=offset, page_size=page_size, sort=sort)

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

