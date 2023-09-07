
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

        self.options = {
            "All Vehicles with this Customer": self.show_all_vehicles
        }
        self.sort_type = {
            "column": "",
            "method": "NONE"
        }

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
        self.treeview.bind("<Button-1>", self.on_click)
        self.treeview.bind("<Double-1>", self.on_select)
        self.treeview.bind("<Button-3>", self.on_right_click)
        self.keys = list(sql.get_table_info('customers').keys())
        self.treeview['columns'] = self.keys

        self.treeview.column("#0", width=0, stretch=tk.NO)  # Hide the default treeview column
        self.treeview.column("id", width=0, stretch=tk.NO) # hide the internal ID

        for key in self.keys:
            if key == 'id': 
                continue
            self.treeview.column(key, anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
            self.treeview.heading(key, text=FIELD_HEADER_NAMES[key])

        self.context_menu = tk.Menu(self, tearoff=0)
        for k,v in self.options.items():
            self.context_menu.add_command(label=k, command=v)

        self.isLoading = False
        self.load_entries()  # Load the initial page of entries

    #@debounce(wait_time=1)
    def load_entries(self, *args):
        if self.isLoading == False:
            self.isLoading = True
            search_text = self.search_entry.get()#.lower()
            #self.entries = [entry for entry in self.entries if search_text in entry.lower()]
            self.entries = sql.search_customers(text=search_text, page=self.page_number, page_size=self.entries_per_page, sort=self.sort_type)

            self.update_treeview()

            self.isLoading = False

    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        
        counter=0
        for entry in self.entries:
            self.treeview.insert("", tk.END, values=entry.to_tuple(), iid=counter)  
            counter += 1
            
    def edit_customer(self, entry=None):
        new_window = tk.Toplevel(self)
        new_window.title("Customer Info")
        ec = EditEntity(new_window, 'Customer', entry, self.load_entries).pack(expand=True, fill=tk.BOTH)

    def on_select(self, event):
        if event.y < 25:
            self.column_sort(event)
        else:
            selected_entry = self.get_selected_item()
            if selected_entry is not None:
                self.edit_customer(selected_entry)

    def get_selected_item(self):
        selected_item = self.treeview.focus()
        
        if selected_item:
            selected_index = int(selected_item)  # Extract index from the item ID
            selected_entry = self.entries[selected_index]
            return selected_entry
        else:
            return None
        
    def update_headers(self):
        for col in self.treeview["columns"]:
            original_text = self.treeview.heading(col, option='text') 
            if ("↑" in original_text or "↓" in original_text):
                original_text = ' '.join(original_text.split(' ')[:-1]) #trim the arrow

            if col == self.sort_type['column']:
                sort = self.sort_type['method']
                arrow = ""
                if sort == "ASC":
                    arrow = " ↑"
                elif sort == "DESC":
                    arrow = " ↓"

                self.treeview.heading(col, text=f"{original_text}{arrow}")
            else:
                self.treeview.heading(col, text=original_text)


    def column_sort(self, event):
        col = self.treeview.identify_column(event.x)
        #col becomes "#3", so convert everything past the first character to an int, and look up the column name based on int value
        column = self.keys[int(col[1:])-1]

        if column != self.sort_type['column']:
            self.sort_type["method"] = "ASC"
            s = True
        else:
            # Reverse sort if already sorted
            s = getattr(self.treeview, f"{col}_sorted", None)
            if s is not None:
                if s: 
                    # reverse sort
                    self.sort_type["method"] = "DESC"
                    s = False
                else: # false, which should be the "third" state of 
                    self.sort_type["method"] = "NONE"
                    s = None
                    column = ""
            else:
                self.sort_type["method"] = "ASC"
                s = True

        self.sort_type["column"] = column

        setattr(self.treeview, f"{col}_sorted", s)
        self.update_headers()
        self.load_entries()

    def on_click(self, event):
        if event.y < 25: # header click
            self.column_sort(event)
        else: # item click
            item = self.treeview.identify_row(event.y)
            self.treeview.selection_set(item)

    def on_right_click(self, event):
        item = self.treeview.identify_row(event.y)
        self.treeview.selection_set(item)
        self.context_menu.post(event.x_root, event.y_root)

    def show_all_vehicles(self):
        selected_entry = self.get_selected_item()
        if selected_entry is not None:
            customer_id = selected_entry.id
            vehicle = self.parent.parent.vehiclesearch
            vehicle.search_entry.delete(0, tk.END)
            vehicle.search_entry.insert(0, customer_id)
            self.parent.select(1)
            vehicle.load_entries()
            
