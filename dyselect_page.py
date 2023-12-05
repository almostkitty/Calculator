import tkinter as tk
from tkinter import ttk

class DySelectPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Диф.уравнения", font=("Helvetica", 20, "bold"))
        label_title.pack(pady=20, padx=20)

        label2 = ttk.Label(self, text="↪️Выберите раздел↩️")
        label2.pack(pady=10, padx=20)

        self.button_first_page = ttk.Button(self, text="I порядка️", command=self.show_dy_first_page)
        self.button_first_page.pack(fill="x")

        self.button_second_page = ttk.Button(self, text="II порядка", command=self.show_dy_second_page)
        self.button_second_page.pack(fill="x")

        self.button_second_page = ttk.Button(self, text="СДУ", command=self.show_dy_third_page)
        self.button_second_page.pack(fill="x")

        self.button_main_page = ttk.Button(self, text="Назад↩️", command=self.show_main_page)
        self.button_main_page.pack(pady=10, side="top")

    def show_dy_first_page(self):
        self.controller.show_page("DyFirstPage")

    def show_dy_second_page(self):
        self.controller.show_page("DySecondPage")

    def show_dy_third_page(self):
        self.controller.show_page("DyThirdPage")

    def show_main_page(self):
        self.controller.show_page("MainPage")
