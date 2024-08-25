import sqlite3
from faker import Faker
import random

# Initialize the Faker library
fake = Faker()

# Create a connection to the SQLite database
conn = sqlite3.connect('data/test.mechanic_app.db')

# Create a cursor object
cursor = conn.cursor()

def fakestatus():
    return random.choice(['good', 'moderate', 'poor', 'neutral'])

# Create the 'customers' table if it does not already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        fullname TEXT,
        email TEXT,
        phone TEXT,
        street_address TEXT,
        city_address TEXT,
        state_address TEXT,
        zip_address TEXT,
        status TEXT,
        notes TEXT
    )
''')

# Create the 'vehicles' table if it does not already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        year INTEGER,
        make TEXT,
        model TEXT,
        licence_number TEXT,
        vin TEXT,
        notes TEXT,
        FOREIGN KEY (customer_id) 
            REFERENCES customers(id)
            ON DELETE SET NULL
    )
''')

# Create the 'jobs' table if it does not already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        vehicle_id INTEGER,
        work_order_number TEXT,
        date_completed TEXT,
        mileage INTEGER,
        repairs TEXT,
        labor_hours REAL,
        labor_cost REAL,
        parts_cost REAL,
        notes TEXT,
        FOREIGN KEY (vehicle_id) 
            REFERENCES vehicles(id)
            ON DELETE SET NULL
    )
''')

# Function to generate random customer data
def generate_customer_data():
    return (
        fake.name(),
        fake.email(),
        fake.phone_number(),
        fake.street_address(),
        fake.city(),
        fake.state(),
        fake.zipcode(),
        fakestatus(),
        fake.text(max_nb_chars=200)
    )

# Function to generate random vehicle data
def generate_vehicle_data(customer_id):
    return (
        customer_id,
        fake.year(),
        fake.word().capitalize(),
        fake.word().capitalize(),
        fake.license_plate(),
        fake.uuid4(),
        fake.text(max_nb_chars=100)
    )

# Function to generate random job data
def generate_job_data(vehicle_id):
    return (
        vehicle_id,
        fake.uuid4(),
        fake.date_this_decade().isoformat(),
        random.randint(0, 200000),
        fake.text(max_nb_chars=150),
        round(random.uniform(1, 10), 2),
        round(random.uniform(100, 1000), 2),
        round(random.uniform(50, 500), 2),
        fake.text(max_nb_chars=200)
    )

# Insert a few hundred random entries into the 'customers' table
customer_ids = []
for _ in range(3000):
    cursor.execute('''
        INSERT INTO customers (fullname, email, phone, street_address, city_address, state_address, zip_address, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', generate_customer_data())
    customer_ids.append(cursor.lastrowid)

# Insert random entries into the 'vehicles' table
vehicle_ids = []
for customer_id in customer_ids:
    for _ in range(random.randint(1, 3)):  # Each customer may have 1-3 vehicles
        cursor.execute('''
            INSERT INTO vehicles (customer_id, year, make, model, licence_number, vin, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', generate_vehicle_data(customer_id))
        vehicle_ids.append(cursor.lastrowid)

# Insert random entries into the 'jobs' table
for vehicle_id in vehicle_ids:
    for _ in range(random.randint(1, 15)):  # Each vehicle may have 1-5 jobs
        cursor.execute('''
            INSERT INTO jobs (vehicle_id, work_order_number, date_completed, mileage, repairs, labor_hours, labor_cost, parts_cost, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', generate_job_data(vehicle_id))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Database populated with random data for customers, vehicles, and jobs.")
