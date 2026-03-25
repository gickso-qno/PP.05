from tkinter import *
from tkinter import messagebox
from db import login_user


def open_main_window(user_data):
    auth_root.destroy()
    import main_window
    main_window.create_main_window(user_data)

def login_click():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Ошибка", "Не оставляйте поля пустыми.")
        return
    
    user_data, error = login_user(username, password)

    if error:
        messagebox.showerror("Ошибка", error)
    else:
        messagebox.showinfo("Успех!", "Вы успешно авторизовались!")
        open_main_window(user_data)


auth_root = Tk()
auth_root.title("Авторизация")

auth_root.geometry("200x50+500+200")
auth_root.resizable(width = True, height = True)
auth_root.minsize(300, 300)
auth_root["bg"] = "white"


main_label = Label(auth_root, text="Авторизация", font="Arial 15 bold", bg="white", fg="black")
main_label.pack()

username_label = Label(auth_root, text="Имя пользователя", font="Arial 12 bold", bg="white", fg="black", padx=10, pady=8)
username_label.pack()

username_entry = Entry(auth_root, bg="white", fg="black", font="Arial 12")
username_entry.pack()

password_label = Label(auth_root, text="Пароль", font="Arial 12 bold", bg="white", fg="black")
password_label.pack()

password_entry = Entry(auth_root, bg="white", fg="black", font="Arial 12", show="*")
password_entry.pack()

send_btn = Button(auth_root, text="Войти", command=login_click)
send_btn.pack(padx=10, pady=8)

auth_root.mainloop()