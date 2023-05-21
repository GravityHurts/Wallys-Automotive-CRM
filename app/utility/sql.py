import sqlite3
from app.utility.types import Customer
from .functions import singleton
import queue
from functools import wraps

DB_NAME = "mechanic_app.db"

@singleton
class SQLConnection:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_db()

    def close(self):
        self.conn.close()

    def create_db(self): 
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
                FOREIGN KEY (customer_id) REFERENCES customers(id)
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
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
            )
        ''')

        self.conn.commit()

    def delete_customer(self, id):
        if id == '': return 

        #TODO: need to remove or update references to this customer id
        
        self.cursor.execute(f'DELETE FROM customers WHERE id = ?', (id,))
        self.conn.commit()
        
    def update_customer(self, id="", firstname="", lastname="", email="", phone="", address="", notes=""):
        if ''.join([str(id), firstname, lastname, email, phone, address, notes]).strip() == '':
            return
        
        if id == '': 
            self.insert_customer(firstname, lastname, email, phone, address, notes)
            return 
        
        self.cursor.execute('UPDATE customers SET firstname = ?, lastname = ?, email = ?, phone = ?, address = ?, notes = ? WHERE id = ?', (firstname, lastname, email, phone, address, notes, id))
        self.conn.commit()

    def insert_customer(self, firstname="", lastname="", email="", phone="", address="", notes=""):
        self.cursor.execute('INSERT INTO customers (firstname, lastname, email, phone, address, notes) VALUES (?, ?, ?, ?, ?, ?)', (firstname, lastname, email, phone, address, notes))
        self.conn.commit()

    def search_customers(self, text="", page=1, page_size=25):
        offset = (page-1) * 1 # the offset value of what "page" we're on

        search = ""
        if text != "":
            search = f'''
            WHERE 
            firstname LIKE '%{text}%' OR
            lastname LIKE '%{text}%' OR
            email LIKE '%{text}%' OR
            phone LIKE '%{text}%' OR
            address LIKE '%{text}%' OR
            notes LIKE '%{text}%' 
            '''

        statement = f"SELECT * FROM customers {search} LIMIT {offset},{page_size}"
        
        self.cursor.execute(statement)

        values = self.cursor.fetchall()

        vals = [Customer(*value) for value in values]
        
        return vals

    def search_vehicles(self, text="", page=1, page_size=25):
        offset = (page-1) * 1 # the offset value of what "page" we're on

        search = ""
        if text != "":
            search = f"WHERE ((year+make+model+vin+notes) LIKE '%{text}%')"

        statement = f"SELECT * FROM vehicles {search} LIMIT {offset},{page_size}"

        self.cursor.execute(statement)

        values = self.cursor.fetchall()

        return values

    def search_jobs(self, text="", page=1, page_size=25):
        offset = (page-1) * 1 # the offset value of what "page" we're on

        search = ""
        if text != "":
            search = f"WHERE ((description+notes+cost+mileage_in+mileage_out) LIKE '%{text}%')"

        statement = f"SELECT * FROM customers {search} LIMIT {offset},{page_size}"

        self.cursor.execute(statement)

        values = self.cursor.fetchall()

        return values


