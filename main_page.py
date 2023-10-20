import tkinter as tk
from tkinter import ttk

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="МЕНЮ", font=("Helvetica", 20, "bold"))
        label_title.grid(row=0, column=0, columnspan=1, pady=10, padx=10, sticky="ns")

        label = ttk.Label(self, text="Выберите операцию:")
        label.grid(row=1, column=0, columnspan=1, pady=10, padx=10, sticky="ns")

        button1 = ttk.Button(self, text="Интегрирование", command=lambda: controller.show_page("IntegrationPage"))
        button2 = ttk.Button(self, text="Диф.Уравнения", state=tk.DISABLED)
        button3 = ttk.Button(self, text="Разработчики", command=lambda: controller.show_page("DevPage"))
        button4 = ttk.Button(self, text="Настройки", command=lambda: controller.show_page("SetPage"))

        # Configure the buttons to span the center column and center vertically
        for i, button in enumerate([button1, button2, button3, button4]):
            button.grid(row=i + 2, column=0, columnspan=1, pady=5, padx=5, sticky="nsew")

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        for i in range(6):  # Assuming you have 6 rows including the title and buttons
            self.grid_rowconfigure(i, weight=1, uniform="row_weight")
