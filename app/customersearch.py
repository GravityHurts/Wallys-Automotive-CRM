
from .utility.functions import debounce
from .utility.sql import SQLConnection

from .utility.types import Customer
from .utility.types import COLUMN_INITIAL_WIDTH
from .textwithvar import TextWithVar

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


sql = SQLConnection()

class CustomerSearch(tk.Frame):
    def __init__(self, parent, entries_per_page=20):
        super().__init__(parent)
        self.parent = parent

        self.entries_per_page = entries_per_page
        self.page_number = 1
        self.entries = []

        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, pady=10)

        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(pady=10, padx=10, side=tk.LEFT)

        # Search Entry
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.size()
        self.search_entry.pack(pady=10, padx=20, side=tk.LEFT, expand=True, fill=tk.X)
        #self.search_entry.bind("<KeyRelease>", self.load_entries)
        self.search_entry.bind("<Return>", self.load_entries)

        # New customer button
        self.new_customer_button = tk.Button(search_frame, text="New Customer", command=self.edit_customer)
        self.new_customer_button.pack(pady=10, padx=20, side=tk.RIGHT)

        # search button
        self.new_customer_button = tk.Button(search_frame, text="Search", command=self.load_entries)
        self.new_customer_button.pack(pady=10, padx=20, side=tk.RIGHT)

        # Treeview
        self.treeview = ttk.Treeview(self)
        self.treeview.pack(expand=True, fill=tk.BOTH)
        #self.treeview.bind("<<TreeviewSelect>>", self.on_select)
        self.treeview.bind("<Double-1>", self.on_select)

        self.treeview['columns'] = ('id', 'firstname', 'lastname', 'email', 'phone', 'address', 'notes')  # Adjust the column names as per your SQL entries

        self.treeview.column("#0", width=0, stretch=tk.NO)  # Hide the default treeview column
        self.treeview.column("id", width=0, stretch=tk.NO) # hide the internal ID
        self.treeview.column("firstname", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("lastname", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("email", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("phone", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("address", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("notes", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)

        self.treeview.heading("id", text="ID")
        self.treeview.heading("firstname", text="First Name")
        self.treeview.heading("lastname", text="Last Name")
        self.treeview.heading("email", text="E-Mail Address")
        self.treeview.heading("phone", text="Phone Number")
        self.treeview.heading("address", text="Street Address")
        self.treeview.heading("notes", text="Notes")
        
        self.isLoading = False
        self.load_entries()  # Load the initial page of entries

    #@debounce(wait_time=1)
    def load_entries(self, *args):
        if self.isLoading == False:
            self.isLoading = True
            search_text = self.search_entry.get()#.lower()
            #self.entries = [entry for entry in self.entries if search_text in entry.lower()]
            self.entries = sql.search_customers(text=search_text, page=self.page_number, page_size=self.entries_per_page)

            self.update_treeview()

            self.isLoading = False

    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        
        counter=0
        for entry in self.entries:
            self.treeview.insert("", tk.END, values=entry.to_tuple(), iid=counter)  
            counter += 1

    def on_select(self, event):
        selected_item = self.treeview.focus()
        
        if selected_item:
            selected_index = int(selected_item)  # Extract index from the item ID
            selected_entry = self.entries[selected_index]
            self.edit_customer(selected_entry)

    def edit_customer(self, entry=None):
        new_window = tk.Toplevel(self)
        new_window.title("Customer Info")
        ec = EditCustomer(new_window, entry, self.load_entries).pack(expand=True, fill=tk.BOTH)

class EditCustomer(tk.Frame):
    def __init__(self, parent, entry=None, update_list=None):
        super().__init__(parent)
        self.parent = parent
        self.entry = entry
        self.update_list = update_list
        if self.update_list is None:
            self.update_list = lambda: None
        
        self.newentry = False
        if self.entry is None: 
            self.entry = Customer()
            self.newentry = True

        self.create_widgets()
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.parent.minsize(300, 300)

        self.parent.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_widgets(self):
        if self.entry.id != '':
            # Delete Button in Menu
            self.menu_bar = tk.Menu(self.parent)
            self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="File", menu=self.file_menu)
            
            self.file_menu.add_command(label="X Delete Customer X", command=self.delete_entry)
            self.parent.config(menu=self.menu_bar)
        

        # First Name
        self.firstname_label = tk.Label(self, text="First Name:")
        self.firstname_label.grid(row=0, column=0, sticky="e")
        self.firstname_var = tk.StringVar()
        self.firstname_entry = tk.Entry(self, textvariable=self.firstname_var)
        self.firstname_entry.grid(row=0, column=1, sticky="ew", columnspan=3)

        # Last Name
        self.lastname_label = tk.Label(self, text="Last Name:")
        self.lastname_label.grid(row=1, column=0, sticky="e")
        self.lastname_var = tk.StringVar()
        self.lastname_entry = tk.Entry(self, textvariable=self.lastname_var)
        self.lastname_entry.grid(row=1, column=1, sticky="ew", columnspan=3)

        # Email
        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=2, column=0, sticky="e")
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self, textvariable=self.email_var)
        self.email_entry.grid(row=2, column=1, sticky="ew", columnspan=3)

        # Phone
        self.phone_label = tk.Label(self, text="Phone:")
        self.phone_label.grid(row=3, column=0, sticky="e")
        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(self, textvariable=self.phone_var)
        self.phone_entry.grid(row=3, column=1, sticky="ew", columnspan=3)

        # Address
        self.address_label = tk.Label(self, text="Address:")
        self.address_label.grid(row=4, column=0, sticky="e")
        self.address_var = tk.StringVar()
        self.address_entry = tk.Entry(self, textvariable=self.address_var)
        self.address_entry.grid(row=4, column=1, sticky="ew", columnspan=3)

        # Notes
        self.sb = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.sb.grid(row=5, column=4, sticky="nse")

        self.notes_label = tk.Label(self, text="Notes:")
        self.notes_label.grid(row=5, column=0, sticky="ne")
        self.notes_var = tk.StringVar()
        self.notes_entry = TextWithVar(self, textvariable=self.notes_var, yscrollcommand=self.sb.set)
        self.sb.config(command=self.notes_entry.yview)
        self.notes_entry.grid(row=5, column=1, sticky="nsew", columnspan=3)


        # Save Button
        self.save_button = tk.Button(self, text="Save", command=self.save_info)
        self.save_button.grid(row=6, column=1, pady=10, padx=10)

        # Cancel Button
        self.cancel_button = tk.Button(self, text="Cancel", command=self.close_window)
        self.cancel_button.grid(row=6, column=3, pady=10, padx=10)


        self.fill_entries()

        if self.newentry:
            self.firstname_entry.focus()

    def save_info(self):
        # Get the values from the StringVar objects
        self.entry.firstname  = self.firstname_var.get()
        self.entry.lastname   = self.lastname_var.get()
        self.entry.email      = self.email_var.get()
        self.entry.phone      = self.phone_var.get()
        self.entry.address    = self.address_var.get()
        self.entry.notes      = self.notes_var.get()

        self.entry.save()
        
        self.close_window()

    def hasChanged(self):
        if ( # any property in the entry does not equal what we have in the text boxes
            self.entry.firstname != self.firstname_var.get() or
            self.entry.lastname != self.lastname_var.get() or
            self.entry.email != self.email_var.get() or
            self.entry.phone != self.phone_var.get() or
            self.entry.address != self.address_var.get() or
            self.entry.notes != self.notes_var.get()
        ):
            return True # has changed
        else:
            return False # everything matches


    def close_window(self):
        if self.hasChanged():
            # Ask for confirmation before quitting with unsaved changes
            result = messagebox.askyesno("Discard Changes", "You have unsaved changes. YES = Close without saving")

            if result:
                #self.entry.delete()
                self.close()
            else:
                # User cancelled deletion
                self.focus()
                pass
        else: # no unsaved changes
            self.close() 

    def close(self):
        self.parent.destroy()
        self.update_list()

    def delete_entry(self):
        # Ask for confirmation before deleting
        result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this Customer?")

        if result:
            self.entry.delete()
            self.close_window()
        else:
            # User cancelled deletion
            self.focus()
            pass


    def fill_entries(self):
        self.firstname_var.set(self.entry.firstname)
        self.lastname_var.set(self.entry.lastname)
        self.email_var.set(self.entry.email)
        self.phone_var.set(self.entry.phone)
        self.address_var.set(self.entry.address)
        self.notes_var.set(self.entry.notes)
        self.notes_entry.update_textvariable()
