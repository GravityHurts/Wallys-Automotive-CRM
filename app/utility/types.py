from . import sql

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
    