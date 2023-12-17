import tkinter as tk
from tkinter import ttk

class ElPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Элементарные функции", font=("Helvetica", 20, "bold"))
        label_title.pack(pady=20, padx=20)






        #ttk.Button(self, text="Вычислить", command=self.calculate).pack()

        self.button_main_page = ttk.Button(self, text="️Главное меню", command=self.show_main_page)
        self.button_main_page.pack()











    def show_main_page(self):
        self.controller.show_page("MainPage")
