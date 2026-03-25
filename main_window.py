from tkinter import *
from tkinter import messagebox
from db import get_connection
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
            "Клиенты": "customer",
            "Заказы клиентов": "customer_orders",
            "Произеденная продукция": "manufactured_products",
            "Производство": "manufacturing",
            "Материалы": "materials",
            "Использованные материалы": "materials_used",
            "Позиции заказов": "order_items",
            "Номенклатура": "product_range",
            "Спецификация": "specifications",
            "Пользователи клиенты": "user_customer",
            "Пользователи": "users"
        }

        self.treeviews = {}

        for tab_name, table_name in self.tables.items():
            self.create_tab(tab_name, table_name)
            
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text = "Обновить данные", command=self.refresh_all).pack()
        
        self.root.mainloop()

    def create_tab(self, tab_name, table_name):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=tab_name)

        tree = ttk.Treeview(frame, show="headings")
        tree.pack(fill="both", expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.treeviews[table_name] = tree

        self.load_table_data(tree, table_name)
        
    def load_table_data(self, tree: ttk.Treeview, table_name):
        try:
            conn = get_connection()
            if not conn:
                messagebox.showerror("Ошибка", "Не удалось подключиться к БД")
                return
            
            with conn.cursor() as cur:
                cur.execute(f"""
                            SELECT column_name 
                            FROM information_schema.columns
                            WHERE table_name = %s
                            ORDER BY ordinal_position""", (table_name,))
                
                columns = [row[0] for row in cur.fetchall()]

                cur.execute(f'SELECT * FROM "{table_name}"')
                rows = cur.fetchall()

            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col.upper())
                tree.column(col, width=120, anchor="center")

            for item in tree.get_children():
                tree.delete(item)

            for row in rows:
                tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке данных: {str(e)}")
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    def refresh_all(self):
        for table_name, tree in self.treeviews.items():
            self.load_table_data(tree, table_name)
        
def create_main_window(user_data):
    MainWindow(user_data)