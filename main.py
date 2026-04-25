import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import psycopg2, random

def db(query, params=(), fetch=False):
    try:
        conn = psycopg2.connect(
            host="localhost", port="5432",
            database="education", user="postgres", password="postgres"
        ) 
        cur = conn.cursor()
        cur.execute(query, params)
        res = cur.fetchall() if fetch else None
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        messagebox.showerror(f"Ошибка подключения к БД: {e}")
        return None
        

def login_user(username, password):
    row = db('SELECT "ID", username, password, failed_attempts, is_blocked, role FROM users WHERE username=%s', (username,) ,fetch=True)
    if not row: return None,"Неверный логин."

    uid, _, stored_password, failed_attemps, blocked, role = row[0]
    if blocked: return None,"Аккаунт заблокирован. Обратитесь к администратору."
    if stored_password == password:
        db('UPDATE users SET failed_attempts=0 WHERE "ID"=%s',(uid,))
        return (uid, username, None, None, "users", role=="admin"),None

    failed_attemps+=1
    blocked = failed_attemps >= 3
    
    db('UPDATE users SET failed_attempts=%s, is_blocked=%s WHERE "ID"=%s', (failed_attemps, blocked, uid))
    
    msg = "Аккаунт заблокирован после 3 неудачных попыток" if blocked else f"Неверный пароль. Попытка {failed_attemps}/3"
    return None, msg

class Captcha:
    def __init__(self,root,ok=None):
        self.root,self.ok = root,ok
        root.title("Капча-пазл"); root.geometry("340x380"); root.resizable(0,0)
        self.img = [ImageTk.PhotoImage(Image.open(f"{i}.png").resize((150,150))) for i in range(1,5)]
        self.order = list(range(4)); random.shuffle(self.order); self.selected = None
        self.frame = tk.Frame(root); self.frame.pack(pady=20)
        self.draw()
        tk.Button(root,text="Проверить",bg="#4CAF50",fg="white",command=self.check).pack(pady=10)

    def draw(self):
        [w.destroy() for w in self.frame.winfo_children()]
        self.buttons = [tk.Button(self.frame, image=self.img[self.order[i]], command=lambda x=i: self.click(x)) for i in range(4)]
        [buttons.grid(row=i//2, column=i%2, padx=5, pady=5) for i,buttons in enumerate(self.buttons)]

    def click(self,i):
        if self.selected is None: self.selected=i; self.buttons[i].config(relief="sunken", bd=5); return
        self.order[self.selected], self.order[i] = self.order[i], self.order[self.selected]
        self.selected = None; self.draw()
        if self.order == [0,1,2,3]: self.success()

    def check(self):
        self.success() if self.order == [0,1,2,3] else messagebox.showwarning("Неверно", "Попробуйте ещё раз.")

    def success(self):
        messagebox.showinfo("Успех", "Капча пройдена!")
        self.root.destroy()
        if self.ok: self.ok()

class Auth:
    def __init__(self,callback):
        self.callback=callback; root=self.root=tk.Tk()
        root.title("Авторизация"); root.geometry("300x300")
        tk.Label(root,text="Имя пользователя").pack()
        self.username=tk.Entry(root); self.username.pack()
        tk.Label(root,text="Пароль",bg="white").pack()
        self.password=tk.Entry(root,show="*"); self.password.pack()
        tk.Button(root,text="Войти",command=self.login).pack(pady=8)
        root.mainloop()

    def login(self):
        username,password=self.username.get(),self.password.get()
        if not username or not password: return messagebox.showerror("Ошибка","Заполните все поля.")
        user=login_user(username,password)
        messagebox.showinfo("Успех","Вы авторизовались!")
        self.root.destroy()
        cur=tk.Tk(); Captcha(cur,lambda:self.callback(user)); cur.mainloop()

class App:
    def __init__(self,user):
        if "Администратор" not in user:
            return messagebox.showinfo("Информация","Вы успешно авторизовались!")
        root=self.root=tk.Tk()
        root.title("Администратор - Управление пользователями"); root.state("zoomed")
        self.text=ttk.Treeview(root,show="headings"); self.text.pack(fill="both",expand=1,padx=10,pady=10)
        self.load()
        bf=ttk.Frame(root); bf.pack()
        for text,command in [("Добавить",self.add),("Редактировать",self.edit),("Разблокировать",self.unblock),("Обновить",self.load)]:
            ttk.pack(side="left",padx=5)
        root.mainloop()

    def load(self):
        cols=[command[0] for command in db('SELECT column_name FROM information_schema.columns WHERE table_name=%s ORDER BY ordinal_position',('users',),1)]
        rows=db('SELECT * FROM "users"',fetch=1)
        self.t["columns"]=cols
        for command in cols: self.text.heading(command,text=command); self.text.column(command,width=120)
        self.text.delete(*self.text.get_children())
        [self.text.insert("", "end", values=r) for r in rows]

    def sel(self):
        x=self.text.selection()

    def add(self):
        w=tk.Toplevel(); w.title("Добавить пользователя"); w.geometry("300x280")
        entries=[tk.Entry(w) for _ in range(3)]
        for t,e_ in zip(["ID","Логин","Пароль"],entries): tk.Label(w,text=t).pack(); e_.pack()
        entries[2].config(show="*")
        rv=tk.StringVar(value="user")
        ttk.Combobox(w,textvariable=rv,values=["admin","user"],state="readonly").pack()
        def save():
            try:
                db('INSERT INTO users ("ID",username,password,failed_attempts,is_blocked,role) VALUES (%s,%s,%s,0,FALSE,%s)',
                   (int(entries[0].get()),entries[1].get(),entries[2].get(),rv.get()))
                w.destroy(); self.load()
            except Exception as e: messagebox.showerror("Ошибка",str(e))
        tk.Button(w,text="Добавить",command=save).pack(pady=10)

    def edit(s):
        v=s.sel()
        if not v: return messagebox.showwarning("Ошибка","Выбери пользователя")
        uid=v[0]
        w=tk.Toplevel(); w.title("Редактировать"); w.geometry("300x280")
        tk.Label(w,text=f"ID: {uid}").pack()
        eu=tk.Entry(w); eu.insert(0,v[1]); eu.pack()
        ep=tk.Entry(w,show="*"); ep.pack()
        rv=tk.StringVar(value=(v[5] if len(v)>5 else "user"))
        ttk.Combobox(w,textvariable=rv,values=["admin","user"],state="readonly").pack()
        def save():
            try:
                db('UPDATE users SET username=%s'+(',password=%s' if ep.get() else '')+',role=%s WHERE "ID"=%s',
                   (eu.get(),*( [ep.get()] if ep.get() else [] ),rv.get(),uid))
                w.destroy(); s.load()
            except Exception as e: messagebox.showerror("Ошибка",str(e))
        tk.Button(w,text="Сохранить",command=save).pack(pady=10)

    def unblock(s):
        v=s.sel()
        if not v: return messagebox.showwarning("Ошибка","Выбери пользователя")
        try:
            db('UPDATE users SET failed_attempts=0,is_blocked=FALSE WHERE "ID"=%s',(v[0],))
            messagebox.showinfo("Готово","Разблокирован"); s.load()
        except Exception as e: messagebox.showerror("Ошибка",str(e))

if __name__=="__main__":
    Auth(lambda user: App(user))