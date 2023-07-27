
from .utility.sql import SQLConnection, FIELD_HEADER_NAMES

from .utility.types import Customer
from .utility.types import COLUMN_INITIAL_WIDTH
from .textwithvar import TextWithVar

from .editwindow import EditEntity

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
        keys = list(sql.get_table_info('customers').keys())
        self.treeview['columns'] = keys

        self.treeview.column("#0", width=0, stretch=tk.NO)  # Hide the default treeview column
        self.treeview.column("id", width=0, stretch=tk.NO) # hide the internal ID

        for key in keys:
            if key == 'id': 
                continue
            self.treeview.column(key, anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
            self.treeview.heading(key, text=FIELD_HEADER_NAMES[key])

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
        ec = EditEntity(new_window, 'Customer', entry, self.load_entries).pack(expand=True, fill=tk.BOTH)

