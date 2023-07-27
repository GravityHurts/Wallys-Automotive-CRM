import tkinter as tk
from tkinter import messagebox

from .utility.types import Customer, Vehicle, Job
from .autocompleteentry import AutocompleteEntry

from .textwithvar import TextWithVar

from .utility.sql import SQLConnection

sql = SQLConnection()


class IDSuggestEntry(AutocompleteEntry):
    def __init__(self, parent, ctype, *args, **kwargs):
        super().__init__([], parent, *args, **kwargs)
        self.search_function = getattr(sql, 'search_'+ctype.lower()+'s', lambda: None)

    def comparison(self): 
        search_text = self.var.get()
        #return sql.search_customers(search_text, 1, 8)
        return self.search_function(search_text, 1, 8)
    
class EditEntity(tk.Frame):
    def __init__(self, parent, ctype, entity=None, update_list=None):
        super().__init__(parent)
        self.parent = parent
        self.entity = entity
        self.ctype = ctype.lower()
        self.update_list = update_list

        if self.update_list is None:
            self.update_list = lambda: None

        if self.entity is None: 
            self.entity = eval(ctype)()
            self.new_entity = True
        else:
            self.new_entity = False

        self.properties = self.entity.property_display

        self.create_widgets()
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.parent.minsize(300, 300)

        self.parent.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_widgets(self):
        if not self.new_entity:
            # Delete Button in Menu
            self.menu_bar = tk.Menu(self.parent)
            self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="File", menu=self.file_menu)
            
            self.file_menu.add_command(label=f"X Delete {self.ctype} X", command=self.delete_entity)
            self.parent.config(menu=self.menu_bar)

        # Create widgets for each property
        row = 0
        self.property_widgets = {}

        for property_name, label_text in self.properties.items():
            if property_name.lower() == 'id':
                continue

            var = tk.StringVar()

            if property_name.lower() == 'notes': # we want a bigger notes area
                sb = tk.Scrollbar(self, orient=tk.VERTICAL)
                sb.grid(row=row, column=4, sticky="nse")

                label = tk.Label(self, text=label_text + ":")
                label.grid(row=row, column=0, sticky="ne")

                entry = TextWithVar(self, textvariable=var, yscrollcommand=sb.set)
                sb.config(command=entry.yview)
                entry.grid(row=row, column=1, sticky="nsew", columnspan=3)
            elif property_name.lower().endswith('_id'):
                label = tk.Label(self, text=label_text + ":")
                label.grid(row=row, column=0, sticky="e")

                entry = IDSuggestEntry(self, property_name.split('_')[0], textvariable=var)
                entry.grid(row=row, column=1, sticky="ew", columnspan=3) 
            else:
                label = tk.Label(self, text=label_text + ":")
                label.grid(row=row, column=0, sticky="e")

                entry = tk.Entry(self, textvariable=var)
                entry.grid(row=row, column=1, sticky="ew", columnspan=3)

            self.property_widgets[property_name] = (var, entry)
            row += 1

        # Save Button
        self.save_button = tk.Button(self, text="Save", command=self.save_info)
        self.save_button.grid(row=row, column=1, pady=10, padx=10)

        # Cancel Button
        self.cancel_button = tk.Button(self, text="Cancel", command=self.close_window)
        self.cancel_button.grid(row=row, column=3, pady=10, padx=10)

        self.fill_entries()

        if self.new_entity:
            first_entry = next(iter(self.property_widgets.values()))[1]
            first_entry.focus()

    def save_info(self):
        # Get the values from the StringVar objects and update the entity
        for property_name, (var, widget) in self.property_widgets.items():
            if property_name.lower().endswith('_id'):
                id_entity = getattr(sql, 'id_'+property_name.split('_')[0])
                if widget.selected is not None:
                    link = id_entity(widget.selected.id)
                    if link is not None:
                        setattr(self.entity, property_name, link.id)
                else:
                    setattr(self.entity, property_name, '')
            else:
                setattr(self.entity, property_name, var.get())
        try:
            self.entity.save()
            self.close_window()
        except ValueError as e:
            messagebox.showerror("Invalid Format", f"One of the properties is not in the expected format:\n{e}")
            self.focus()


    def has_changed(self):
        # Check if any property in the entity does not equal the corresponding value in the text boxes
        for property_name, (var, _) in self.property_widgets.items():
            if property_name.lower().endswith('_id'):
                continue
            if str(getattr(self.entity, property_name)) != var.get():
                return True  # has changed
        return False  # everything matches

    def close_window(self):
        if self.has_changed():
            # Ask for confirmation before quitting with unsaved changes
            result = messagebox.askyesno("Discard Changes", "You have unsaved changes. YES = Close without saving")

            if result:
                self.close()
            else:
                # User canceled closing without saving
                self.focus()
        else:  # no unsaved changes
            self.close()

    def close(self):
        self.parent.destroy()
        self.update_list()

    def delete_entity(self):
        # Ask for confirmation before deleting
        result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this Entity?")

        if result:
            self.entity.delete()
            self.close_window()
        else:
            # User canceled deletion
            self.focus()
            pass

    def fill_entries(self):
        # Fill the text boxes with the current property values of the entity
        for property_name, (var, widget) in self.property_widgets.items():
            if property_name.lower().endswith('_id'):
                id_entity = getattr(sql, 'id_'+property_name.split('_')[0])
                link = id_entity(getattr(self.entity, property_name))
                if link is not None:
                    widget.selected = link
                    widget.set_variable(link)
            else:
                var.set(getattr(self.entity, property_name))

            if property_name.lower() == 'notes':
                widget.update_textvariable()
        

