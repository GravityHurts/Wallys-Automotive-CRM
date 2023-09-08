
from .utility.sql import SQLConnection, FIELD_HEADER_NAMES
from .utility.types import COLUMN_INITIAL_WIDTH
from .editwindow import EditEntity

import math

import tkinter as tk
from tkinter import ttk

sql = SQLConnection()

class Search(tk.Frame):
    def __init__(self, parent, params, entries_per_page=20):
        super().__init__(parent)
        self.parent = parent
        self.params = params
        self.count = 0

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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        search_frame = tk.Frame(self)
        #search_frame.pack(fill=tk.X, pady=10)
        search_frame.grid(row=0, column=0, sticky='ew')

        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(pady=10, padx=10, side=tk.LEFT)

        # Search Entry
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.size()
        self.search_entry.pack(pady=10, padx=20, side=tk.LEFT, expand=True, fill=tk.X)
        #self.search_entry.bind("<KeyRelease>", self.load_entries)
        self.search_entry.bind("<Return>", self.load_entries)

        # New item button
        self.new_item_button = tk.Button(search_frame, text=f"New {self.params['name']}", command=self.edit_item)
        self.new_item_button.pack(pady=10, padx=20, side=tk.RIGHT)

        # search button
        self.search_button = tk.Button(search_frame, text="Search", command=self.load_entries)
        self.search_button.pack(pady=10, padx=20, side=tk.RIGHT)

        # Treeview
        self.treeview = ttk.Treeview(self)
        #self.treeview.pack(expand=True, fill=tk.BOTH)
        self.treeview.grid(row=1,column=0, sticky='nsew')
        #self.treeview.bind("<<TreeviewSelect>>", self.on_select)
        self.treeview.bind("<ButtonPress-1>", self.start_timer)
        self.treeview.bind("<ButtonRelease-1>", self.check_click_or_resize)
        self.treeview.bind("<Double-1>", self.on_select)
        self.treeview.bind("<Button-3>", self.on_right_click)
        self.keys = list(sql.get_table_info(self.params['dbname']).keys())
        self.treeview['columns'] = self.keys

        self.treeview.column("#0", width=0, stretch=tk.NO)  # Hide the default treeview column
        self.treeview.column("id", width=0, stretch=tk.NO) # hide the internal ID

        for key in self.keys:
            if key == 'id': 
                continue
            self.treeview.column(key, anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
            self.treeview.heading(key, text=FIELD_HEADER_NAMES[key])

        self.page_frame = tk.Frame(self)
        #self.page_frame.pack(pady=10, padx=20, anchor=tk.CENTER, expand=True, fill=tk.X)
        self.page_frame.grid(row=2, column=0, sticky='ew')

        self.page_frame.grid_columnconfigure(0, weight=2)
        self.page_frame.grid_columnconfigure(1, weight=1)
        self.page_frame.grid_columnconfigure(2, weight=2)

        self.left_arrow = tk.Button(self.page_frame, text="  ←  ", cursor="hand2", command=self.prev_page)
        self.left_arrow.grid(row=0, column=0, sticky='e')

        self.page_label = tk.Label(self.page_frame, text=f"Page {self.page_number}")
        self.page_label.grid(row=0, column=1, padx=15)

        self.right_arrow = tk.Button(self.page_frame, text="  →  ", cursor="hand2", command=self.next_page)
        self.right_arrow.grid(row=0, column=2, sticky='w')

        self.context_menu = tk.Menu(self, tearoff=0)
        for k,v in self.options.items():
            self.context_menu.add_command(label=k, command=v)

        self.isLoading = False
        self.load_entries()  # Load the initial page of entries

        self.timer_started = False

    def prev_page(self):
        if self.page_number > 1:
            self.page_number -= 1
            self.load_entries()

    def next_page(self):
        if self.page_number < self.total_pages():
            self.page_number += 1
            self.load_entries()

    def total_pages(self):
        return math.ceil(self.count/self.entries_per_page)

    def update_page_label(self):
        print(self.params['name'], "test", self.count, self.page_number)
        if self.count >= self.entries_per_page:
            self.page_frame.grid(row=2, column=0, sticky='ew')
            self.page_label.config(text=f"Page {self.page_number} of {self.total_pages()}")
        else:
            self.page_frame.grid_forget()
            self.page_label.config(text=f"Page {self.page_number}")


    def start_timer(self, event):
        col = self.treeview.identify_column(event.x)
        if col:
            self.timer_started = True
            self.parent.after(200, self.set_timer_flag_to_false)

    def set_timer_flag_to_false(self):
        self.timer_started = False

    def check_click_or_resize(self, event):
        col = self.treeview.identify_column(event.x)
        if col and self.timer_started:
            self.on_click(event)

    def get_function(self, starting_name, obj=None):
        key = 'dbname'
        return getattr(obj, f"{starting_name}_{self.params[key]}")

    #@debounce(wait_time=1)
    def load_entries(self, *args):
        if self.isLoading == False:
            self.isLoading = True
            search_text = self.search_entry.get()#.lower()
            #self.entries = [entry for entry in self.entries if search_text in entry.lower()]
            entries = self.get_function("search", obj=sql)(text=search_text, page=self.page_number, page_size=self.entries_per_page, sort=self.sort_type)

            self.entries = entries['entries']
            self.count = entries['count']

            self.update_treeview()

            self.isLoading = False

    def update_treeview(self):
        self.update_page_label()
        self.treeview.delete(*self.treeview.get_children())
        
        counter=0
        for entry in self.entries:
            self.treeview.insert("", tk.END, values=entry.to_tuple(), iid=counter)  
            counter += 1
            
    def edit_item(self, entry=None):
        new_window = tk.Toplevel(self)
        new_window.title(f"{self.params['name']} Info")
        ec = EditEntity(new_window, self.params['name'], entry, self.load_entries).pack(expand=True, fill=tk.BOTH)

    def on_select(self, event):
        if event.y < 25:
            self.column_sort(event)
        else:
            selected_entry = self.get_selected_item()
            if selected_entry is not None:
                self.edit_item(selected_entry)

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
            
