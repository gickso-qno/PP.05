from tkinter import *
from tkinter import messagebox
from db import get_conection
from tkinter import ttk

class MainWindow:
    def __init__(self, user_data):
        self.user_data = user_data
        self.root = Tk()
        self.root.title("Производство")
        self.root.state("zoomed")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tables = {
            "Клиенты": "customers"
        }



    self.root.mainloop()








def create_main_window(user_data):
    MainWindow(user_data)