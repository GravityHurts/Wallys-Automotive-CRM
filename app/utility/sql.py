import sqlite3
from app.utility.types import Customer, Vehicle, Job
from .functions import singleton

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


    # CUSTOMER QUERIES
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

    def id_customer(self, id):
        if id == '': return None
        
        self.cursor.execute(f'SELECT * FROM customers WHERE id = ? LIMIT 1', (id,))

        values = self.cursor.fetchall()

        vals = [Customer(*value) for value in values]
        
        return vals

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

    # VEHICLE QUERIES
    def delete_vehicle(self, id):
        if id == '':
            return 

        # TODO: need to remove or update references to this vehicle id
        
        self.cursor.execute("DELETE FROM vehicles WHERE id = ?", (id,))
        self.conn.commit()

    def update_vehicle(self, id="", customer_id="", year="", make="", model="", vin="", notes=""):
        if ''.join([str(id), str(customer_id), str(year), make, model, vin, notes]).strip() == '':
            return
        
        if id == '':
            self.insert_vehicle(customer_id, year, make, model, vin, notes)
            return 
        
        if (customer_id == ''):
            customer_id = 'NULL'
        self.cursor.execute("UPDATE vehicles SET customer_id = ?, year = ?, make = ?, model = ?, vin = ?, notes = ? WHERE id = ?", (customer_id, year, make, model, vin, notes, id))
        self.conn.commit()

    def insert_vehicle(self, customer_id="", year="", make="", model="", vin="", notes=""):
        if (customer_id == ''):
            customer_id = 'NULL'

        ret = self.cursor.execute("INSERT INTO vehicles (customer_id, year, make, model, vin, notes) VALUES (?, ?, ?, ?, ?, ?)", (customer_id, year, make, model, vin, notes))
        self.conn.commit()

    def id_vehicle(self, id):
        if id == '': return None
        
        self.cursor.execute(f'SELECT * FROM vehicles WHERE id = ? LIMIT 1', (id,))
        
        values = self.cursor.fetchall()

        vals = [Vehicle(*value) for value in values]
        
        return vals

    def search_vehicles(self, text="", page=1, page_size=25):
        offset = (page-1) * page_size  # the offset value of what "page" we're on

        search = ""
        if text != "":
            search = f'''
            WHERE 
            vehicles.id LIKE '%{text}%' OR
            customer_id LIKE '%{text}%' OR
            year LIKE '%{text}%' OR
            make LIKE '%{text}%' OR
            model LIKE '%{text}%' OR
            vin LIKE '%{text}%' OR
            vehicles.notes LIKE '%{text}%' OR 
            customers.firstname LIKE '%{text}%' OR 
            customers.lastname LIKE '%{text}%'
            '''

        statement = f"SELECT vehicles.*, customers.firstname, customers.lastname FROM vehicles LEFT JOIN customers ON customers.id = vehicles.customer_id {search} LIMIT {offset},{page_size}"
        
        self.cursor.execute(statement)
        values = self.cursor.fetchall()
        print(values)
        vehicles = [Vehicle(*value) for value in values]
        
        return vehicles

    # JOB QUERIES
    def delete_job(self, id):
        if id == '':
            return

        # TODO: need to remove or update references to this job id

        self.cursor.execute("DELETE FROM jobs WHERE id = ?", (id,))
        self.conn.commit()

    def update_job(self, id="", vehicle_id="", description="", notes="", cost="", mileage_in="", mileage_out=""):
        if ''.join([str(id), str(vehicle_id), description, notes, cost, str(mileage_in), str(mileage_out)]).strip() == '':
            return

        if id == '':
            self.insert_job(vehicle_id, description, notes, cost, mileage_in, mileage_out)
            return

        self.cursor.execute("UPDATE jobs SET vehicle_id = ?, description = ?, notes = ?, cost = ?, mileage_in = ?, mileage_out = ? WHERE id = ?", (vehicle_id, description, notes, cost, mileage_in, mileage_out, id))
        self.conn.commit()

    def insert_job(self, vehicle_id="", description="", notes="", cost="", mileage_in="", mileage_out=""):
        self.cursor.execute("INSERT INTO jobs (vehicle_id, description, notes, cost, mileage_in, mileage_out) VALUES (?, ?, ?, ?, ?, ?)", (vehicle_id, description, notes, cost, mileage_in, mileage_out))
        self.conn.commit()

    def search_jobs(self, text="", page=1, page_size=25):
        offset = (page-1) * page_size  # the offset value of what "page" we're on

        search = ""
        if text != "":
            search = f'''
            WHERE 
            description LIKE '%{text}%' OR
            notes LIKE '%{text}%' OR
            cost LIKE '%{text}%' OR
            mileage_in LIKE '%{text}%' OR
            mileage_out LIKE '%{text}%' 
            '''

        statement = f"SELECT * FROM jobs {search} LIMIT {offset},{page_size}"

        self.cursor.execute(statement)
        values = self.cursor.fetchall()
        jobs = [Job(*value) for value in values]

        return jobs
