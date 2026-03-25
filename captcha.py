import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class CaptchaWindow:
    def __init__(self, root, username, on_success=None):
        self.root = root
        self.on_success = on_success
        self.root.title("Капча")
        self.root.geometry("300x500")

        self.image_files = ["1.png", "2.png", "3.png", "4.png"]

        self.photos = []
        for file in self.image_files:
            img = Image.open(file).resize((80, 80)) 
            self.photos.append(ImageTk.PhotoImage(img))

        self.order = list(range(4))
        random.shuffle(self.order)

        self.correct_order = [0, 1, 2, 3]

        self.user_order = []

        tk.Label(root, text="Нажмите картинки в правильном порядке").pack(pady=10)

        self.buttons = []
        frame = tk.Frame(root)
        frame.pack(pady=10)

        for i in range(4):
            btn = tk.Button(
                frame,
                image=self.photos[self.order[i]],
                command=lambda x=i: self.click(x)
            )
            btn.grid(row=0, column=i, padx=5)
            self.buttons.append(btn)

    def click(self, i):
        real_index = self.order[i]
        self.user_order.append(real_index)

        self.buttons[i].config(state="disabled")

        if len(self.user_order) == 4:
            self.check()

    def check(self):
        if self.user_order == self.correct_order:
            messagebox.showinfo("Отлично!", "Капча пройдена")
            self.root.destroy()
            if self.on_success:
                self.on_success()
        else:
            messagebox.showerror("Ошибка", "Неправильный порядок!")

            self.user_order = []
            for btn in self.buttons:
                btn.config(state="normal")