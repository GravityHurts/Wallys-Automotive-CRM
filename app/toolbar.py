import tkinter as tk

class Toolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Create a menu bar
        menu_bar = tk.Menu(self.parent)
        file_menu = tk.Menu(menu_bar, tearoff=0)

        # Add options to the menu bar
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Add an Exit option to the File menu
        file_menu.add_command(label="Exit", command=self.close_app)

        self.parent.parent.config(menu=menu_bar)

    def close_app(self):
        self.parent.destroy()
        