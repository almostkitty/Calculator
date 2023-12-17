import tkinter as tk
from tkinter import ttk


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label1 = ttk.Label(self, text="МЕНЮ", font=("Helvetica", 20, "bold"))
        label1.pack(pady=20, padx=20)

        label2 = ttk.Label(self, text="↪️Выберите операцию↩️")
        label2.pack(pady=20, padx=20)

        button_data = [
            ("Интегрирование✅", "IntegrationPage"),
            ("Кратный интеграл✅", "KratniPage"),
            ("Дифференциальные Уравнения✅", "DySelectPage"),
            ("Элементарные функции✅", "ElPage"),
            ("Нелинейные Уравнения✅", "NlPage"),
            ("Разработчики🧑🏿‍💻", "DevPage"),
            ("Настройки⚙️", "SetPage"),
            ("Выйти️❌", lambda: self.close_app())
        ]

        for text, command in button_data:
            button = ttk.Button(self, text=text, command=lambda c=command: controller.show_page(c))
            button.pack(fill="x")

    def close_app(self):
        self.controller.quit()
