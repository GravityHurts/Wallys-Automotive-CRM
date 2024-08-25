import tkinter as tk

from ..utility import utils

class Dropdown(tk.Frame):
    def __init__(self, parent, options, textvariable=None, default=None, command=None):
        """
        Initialize the dropdown component.

        :param parent: Parent widget (usually a Tk root or frame).
        :param options: List of options to display in the dropdown.
        :param default: The default selected option (optional).
        :param command: Function to call when an option is selected (optional).
        """
        super().__init__(parent)

        if not textvariable:
            textvariable = tk.StringVar(self)
        self.variable = textvariable
        self.variable.set(default if default else options[0])
        
        self.dropdown = tk.OptionMenu(self, self.variable, *options, command=self._on_select)
        self.dropdown.pack()
        
        self.command = command

    def _on_select(self, value):
        """Internal callback function for option selection."""
        if self.command:
            self.command(value)
    def get_value(self):
        """
        Get the currently selected value.

        :return: The currently selected value as a string.
        """
        return self.variable.get()

    def set_options(self, options, default=None):
        """
        Update the dropdown options.

        :param options: New list of options for the dropdown.
        :param default: New default selected option (optional).
        """
        menu = self.dropdown["menu"]
        menu.delete(0, "end")
        for option in options:
            menu.add_command(label=option, command=lambda value=option: self.variable.set(value))
        if default:
            self.variable.set(default)

    def set_color(self, color):
        self.dropdown.configure(bg=color, activebackground=utils.darken_hex_color(color))

# Example usage of the Dropdown class
if __name__ == "__main__":
    def on_select(value):
        print(f"Selected: {value}")

    root = tk.Tk()
    root.title("Reusable Dropdown Example")

    # Create a Dropdown instance
    dropdown = Dropdown(root, options=["Option 1", "Option 2", "Option 3"], default="Option 1", command=on_select)

    # Retrieve the selected value
    print(f"Initially selected: {dropdown.get_value()}")

    root.mainloop()
