import tkinter as tk
from tkinter import ttk

class TablePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Сравнение", font=("Helvetica", 20, "bold"))
        label_title.grid(row=0, column=0, columnspan=5, pady=10, padx=10, sticky="nsew")

        button_back = ttk.Button(self, text="Назад", command=lambda: self.controller.show_page("IntegrationPage"))
        button_back.grid(row=2, column=0, columnspan=5, pady=10, padx=10, sticky="nsew")

        columns = ('Параметры', ' ', 'Результат')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)

        data = [
            ('Функция', '-'),
            ('Пределы', '-'),
            ('Точность:', '-'),
            ('Кол-во разбиений:', '-'),
            ('Метод', '-'),
            ('Прямоугольники левых частей', '-'),
            ('Прямоугольники левых частей I', '-'),
            ('Прямоугольники левых частей II', '-'),
            ('Прямоугольники правых частей', '-'),
            ('Трапеции', '-'),
            ('Параболы', '-')

        ]

        for row in data:
            self.tree.insert('', tk.END, values=row)

        self.tree.grid(row=1, column=0, columnspan=5, pady=10, padx=10, sticky="nsew")

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

        for i in range(3):
            self.grid_rowconfigure(i, weight=1)