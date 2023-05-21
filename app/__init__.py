from .mainwindow import MainWindow
from .utility.sql import SQLConnection


import atexit

s = SQLConnection()

def on_quit():
    s.close()
    
atexit.register(on_quit)
