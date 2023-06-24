from . import sql

COLUMN_INITIAL_WIDTH = 10

class Customer:
    def __init__(self, id='', firstname='', lastname='', email='', phone='', address='', notes='', **kwargs):
        self.id        = kwargs.get('id',        id)
        self.firstname = kwargs.get('firstname', firstname)
        self.lastname  = kwargs.get('lastname',  lastname)
        self.email     = kwargs.get('email',     email)
        self.phone     = kwargs.get('phone',     phone)
        self.address   = kwargs.get('address',   address)
        self.notes     = kwargs.get('notes',     notes)
        self.sql = sql.SQLConnection()

    def __str__(self):
        return f'ID: {self.id} - {self.firstname} {self.lastname} {self.phone}'

    def save(self):
        self.sql.update_customer(
            self.id, # if id == '' this is handled in the sql function
            self.firstname,
            self.lastname,
            self.email,
            self.phone,
            self.address,
            self.notes
        )

    def delete(self):
        if self.id != '':
            self.sql.delete_customer(id=self.id)
    
    #don't need?
    def to_tuple(self):
        return (
            self.id,
            self.firstname,
            self.lastname,
            self.email,
            self.phone,
            self.address,
            self.notes
        )
    

class Vehicle:
    def __init__(self, id='', customer_id='', year='', make='', model='', vin='', notes='', firstname='', lastname='', **kwargs):
        self.id           = kwargs.get('id', id)
        self.customer_id  = kwargs.get('customer_id', customer_id)
        if (self.customer_id == 'NULL'):
            self.customer_id = ''

        self.firstname    = kwargs.get('firstname', firstname) or ''
        self.lastname     = kwargs.get('lastname', lastname) or ''

        if (self.firstname+self.lastname == ''):
            self.id_string = "No Customer"
        else:
            #self.id_string    = f"ID: {self.customer_id} - {firstname} {lastname}"
            self.id_string    = f"{self.firstname} {self.lastname}"

        self.year         = kwargs.get('year', year)
        self.make         = kwargs.get('make', make)
        self.model        = kwargs.get('model', model)
        self.vin          = kwargs.get('vin', vin)
        self.notes        = kwargs.get('notes', notes)
        self.sql = sql.SQLConnection()
        
    def __str__(self):
        return f'{self.year} {self.make} {self.model} {self.vin}'

    def save(self):
        self.sql.update_vehicle(
            self.id,  # if id == '', this is handled in the SQL function
            self.customer_id,
            self.year,
            self.make,
            self.model,
            self.vin,
            self.notes
        )

    def delete(self):
        if self.id != '':
            self.sql.delete_vehicle(id=self.id)

    def to_tuple(self):
        return (
            self.id,
            #self.customer_id,
            self.id_string,
            self.year,
            self.make,
            self.model,
            self.vin,
            self.notes
        )

class Job:
    def __init__(self, id='', vehicle_id='', description='', notes='', cost='', mileage_in='', mileage_out='', year='', make='', model='', **kwargs):
        self.id             = kwargs.get('id', id)
        self.vehicle_id     = kwargs.get('vehicle_id', vehicle_id)
        if self.vehicle_id == 'NULL':
            self.vehicle_id = ''

        self.year           = kwargs.get('year', year) or ''
        self.make           = kwargs.get('make', make) or ''
        self.model          = kwargs.get('model', model) or ''
        if ((str(self.year)+str(self.make)+str(self.model)) == ''):
            self.id_string = "No Vehicle??"
        else:
            self.id_string    = f"{self.year} {self.make} {self.model}"
            
        self.description    = kwargs.get('description', description)
        self.notes          = kwargs.get('notes', notes)
        self.cost           = kwargs.get('cost', cost)
        self.mileage_in     = kwargs.get('mileage_in', mileage_in)
        self.mileage_out    = kwargs.get('mileage_out', mileage_out)
        self.sql = sql.SQLConnection()

    def save(self):
        self.sql.update_job(
            self.id,  # if id == '', this is handled in the SQL function
            self.vehicle_id,
            self.description,
            self.notes,
            self.cost,
            self.mileage_in,
            self.mileage_out
        )

    def delete(self):
        if self.id != '':
            self.sql.delete_job(id=self.id)

    def to_tuple(self):
        return (
            self.id,
            #self.vehicle_id,
            self.id_string,
            self.description,
            self.notes,
            self.cost,
            self.mileage_in,
            self.mileage_out
        )

