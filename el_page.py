import numpy as np
import tkinter as tk
from tkinter import ttk


class ElPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Элементарные функции", font=("Helvetica", 20, "bold"))
        label_title.pack(pady=20, padx=20)

        self.frame_data = [
            {"label_text": "eˆx", "from_text": "x="},
            {"label_text": "sin(x)", "from_text": "x="},
            {"label_text": "√x", "from_text": "x=", "to_text": "y="},
            {"label_text": "1/√x", "from_text": "x=", "to_text": "y="}
        ]

        for data in self.frame_data:
            frame = ttk.Frame(self)
            frame.pack()

            label_sqrt = ttk.Label(frame, text=data["label_text"])
            label_sqrt.pack()

            entry_frame = ttk.Frame(frame)
            entry_frame.pack()

            label_a = ttk.Label(entry_frame, text=data["from_text"])
            entry_a = ttk.Entry(entry_frame, width=3)
            label_a.pack(side="left")
            entry_a.pack(side="left", padx=5)

            data["entry_a"] = entry_a

            to_text = data.get("to_text", "")

            if to_text:
                label_b = ttk.Label(entry_frame, text=to_text)
                entry_b = ttk.Entry(entry_frame, width=3)
                label_b.pack(side="left")
                entry_b.pack(side="left", padx=5)
                data["entry_b"] = entry_b

            calculate_button = ttk.Button(
                frame,
                text="Вычислить",
                command=lambda data=data,
                               entry_a=entry_a,
                               entry_b=data.get("entry_b"): self.calculate(data, entry_a, entry_b)
            )

            calculate_button.pack(side="left", padx=5)

            result_text = tk.Text(frame, height=1, width=20)
            result_text.pack(side="left", padx=5)
            data["result_text"] = result_text

        self.button_clear = ttk.Button(self, text="Очистить", command=self.clear)
        self.button_clear.pack()

        self.button_main_page = ttk.Button(self, text="️Главное меню", command=self.show_main_page)
        self.button_main_page.pack()

    def calculate(self, data, entry_a, entry_b):
        try:
            value_a = float(entry_a.get())
            value_b = float(data.get("entry_b").get()) if data.get("entry_b") else None

            if data["label_text"] == "eˆx":
                result = self.calculate_e(value_a)
            elif data["label_text"] == "sin(x)":
                result = self.calculate_sin(value_a)
            elif data["label_text"] == "√x":
                result = self.calculate_sqrt(value_a, value_b)
            elif data["label_text"] == "1/√x":
                result = self.calculate_div_sqrt(value_a, value_b)
            else:
                result = None

        except ValueError as e:
            error_message = f"Error: Некорректный ввод - {str(e)}"
            data["result_text"].delete(1.0, tk.END)
            data["result_text"].insert(tk.END, error_message)

        data["result_text"].delete(1.0, tk.END)  # Очищаем текущий текст
        data["result_text"].insert(tk.END, result)  # Вставляем новый текст

    def cheb(self, x, n):
        if n == 0:
            return np.ones_like(x)
        elif n == 1:
            return x
        else:
            return 2 * x * self.cheb(x, n - 1) - self.cheb(x, n - 2)

    def cheb_exp(self, x, n, a):
        t = self.cheb(x, n)
        return np.sum(a * t)

    def calculate_e(self, entry_a):
        try:
            x = float(entry_a)
        except ValueError:
            return "Error: Некорректный ввод"

        if abs(x) > 1:
            return "Error: Введите число не больше 1"

        a = np.array([0.9999998, 1.0000000, 0.5000063, 0.1666674, 0.0416350, 0.0083298, 0.0014393, 0.0002040])
        b = 2 * 10 ** (-7)

        if abs(x) <= 1:
            result = np.exp(x) * (1 + b * self.cheb_exp(x, 8, a))
            return str(result)
        else:
            return "Некорректный ввод"

    def cheb_sin(self, x, a, n):
        t = self.cheb(x, n)
        return np.sum(a * t)

    def calculate_sin(self, entry_a):
        try:
            x = float(entry_a)
        except ValueError:
            return "Error: Некорректный ввод"

        if abs(x) <= np.pi / 2:
            a = np.array([1.000000002, -1.66666589, 0.008333075, -0.000198107, 0.000002608])
            b = 6 * 10 ** (-9)

            result = np.sin(x) * (1 + b * self.cheb_sin(x, a, 5))
            return str(result)
        else:
            return "Error: Введите число не больше pi/2"

    def calculate_sqrt(self, entry_a, entry_b):
        try:
            x = float(entry_a)
            y = float(entry_b)
        except ValueError:
            return "Error: Некорректный ввод"

        eps = 1e-7
        y_res = y
        y = 0

        while eps < abs(y_res - y):
            y = y_res
            y_res = 0.5 * (y + x / y)

        return str(y_res)

    def calculate_div_sqrt(self, entry_a, entry_b):
        try:
            x = float(entry_a)
            y = float(entry_b)
        except ValueError:
            return "Error: Некорректный ввод"

        eps = 1e-7
        y_res = y
        y = 0

        while eps < abs(y_res - y):
            y = y_res
            if y == 0:
                return "Error: Деление на ноль"
            y_res = y / 2 * (3 - x * y * y)

        return str(y_res)

    def clear(self):
        for data in self.frame_data:
            data["result_text"].delete(1.0, tk.END)  # Очищаем текстовые поля
            data["entry_a"].delete(0, tk.END)  # Очищаем "x"

            if "entry_b" in data:
                data["entry_b"].delete(0, tk.END)  # Очищаем "y"

    def show_main_page(self):
        self.controller.show_page("MainPage")
