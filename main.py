import tkinter as tk
import app

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Mechanic app")
        self.geometry("800x600")

        self.mw = app.MainWindow(self)
        self.mw.pack(fill='both', expand=True)



if __name__ == "__main__":
    root = MainApplication()
    root.mainloop()

