import tkinter as tk
import app
from app.utility import settings


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title(settings.config['application']['window title'])
        self.geometry(settings.config['application']['window size'])
        self.state(settings.config['application']['start fullscreen'] == True and "zoomed" or "normal")
        self.iconbitmap("media/app.ico")

        self.mw = app.MainWindow(self)
        self.mw.pack(fill='both', expand=True)



if __name__ == "__main__":
    root = MainApplication()
    root.mainloop()

