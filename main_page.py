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

        button1 = ttk.Button(self, text="Интегрирование✅", command=lambda: controller.show_page("IntegrationPage"))
        button1.pack(fill="x")

        button2 = ttk.Button(self, text="Дифференциальные Уравнения❌", state=["disabled"])
        button2.pack(fill="x")

        button3 = ttk.Button(self, text="Разработчики🧑🏿‍💻", command=lambda: controller.show_page("DevPage"))
        button3.pack(fill="x")

        button4 = ttk.Button(self, text="Настройки⚙️", command=lambda: controller.show_page("SetPage"))
        button4.pack(fill="x")
