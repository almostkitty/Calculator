import tkinter as tk
from tkinter import ttk


class DevPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="РАЗРАБОТЧИКИ", font=("Helvetica", 20, "bold"))
        label_title.grid(row=0, column=0, columnspan=1, pady=10, padx=10, sticky="ns")

        label = ttk.Label(self, text="Герман П.-- Разработка\nИван П.--Алгоритмы\nДмитрий Щ.--Интерфейс и Документация\n\n-СПб 2023-")
        label.grid(row=1, column=0, columnspan=1, pady=10, padx=10)

        button_back = ttk.Button(self, text="Назад", command=lambda: self.controller.show_page("MainPage"))
        button_back.grid(row=2, column=0, columnspan=1, pady=10, padx=10)


        for i in range(3):
            self.grid_columnconfigure(i, weight=1)