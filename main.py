from tkinter import *
import tkinter as tk

root = Tk()
root.title("Производство")

root.geometry("400x400+500+200")
root.resizable(width = True, height = True)
root.minsize(300, 300)


def click ():
    print("Вы успешно вошли!")

btn = Button(root, text = "Войти", command = click, font = "Arial 20", bg = "lightblue", fg = "black", activebackground = "blue", activeforeground = "white")
btn.pack()

login = Entry(root)
login.pack()

login.insert(12, "Введите логин")

image_label = tk.Label(root)

root.mainloop()