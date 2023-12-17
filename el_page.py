import tkinter as tk
from tkinter import ttk
from math import pi


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

            label_b = ttk.Label(entry_frame, text=to_text)
            entry_b = ttk.Entry(entry_frame, width=3)
            label_b.pack(side="left")
            entry_b.pack(side="left", padx=5)

            data["entry_b"] = entry_b

            calculate_button = ttk.Button(frame, text="Вычислить", command=lambda data=data, entry_a=entry_a, entry_b=entry_b: self.calculate(data, entry_a, entry_b)
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
            value_b = float(entry_b.get())

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

    def calculate_e(self, entry_a):
        try:
            x = float(entry_a)
        except ValueError:
            return "Error: Некорректный ввод"

        if abs(x) > 1:
            return "Error: Введите число не больше 1"

        a = [0.9999998, 1.0000000, 0.5000063, 0.1666674, 0.0416350, 0.0083298, 0.0014393, 0.0002040]
        eps = 2e-7

        x_scaled = x / 2  # Масштабируем x для использования метода Чебышева на интервале [-1, 1]
        u = 2 * x_scaled  # Переменная u для метода Чебышева

        i = len(a) - 1
        result = a[i]

        while i > 0:
            i -= 1
            temp = result
            result_old = result
            result = a[i] + u * result - temp

            # Проверяем точность
            if abs(result - result_old) < eps:
                break

        result *= 2 * x_scaled  # Масштабируем результат обратно

        return result

    def calculate_sin(self, entry_a):
        try:
            x = float(entry_a)
        except ValueError:
            return "Error: Некорректный ввод"

        if x > pi / 2:
            return "Error: Введите число не больше pi/2"

        a = [1.000000002, -1.66666589, 0.008333075, -0.000198107, 0.000002608]
        eps = 6e-9

        x_scaled = x / (pi / 2)  # Масштабируем x для использования метода Чебышева на интервале [-1, 1]
        u = 2 * x_scaled - 1  # Переменная u для метода Чебышева

        i = len(a) - 1
        result = a[i]
        term = result
        u_power = u

        while i > 0:
            i -= 1
            term = a[i] + u * term
            result += term
            u_power *= u

            if abs(term * u_power) < eps:  # Проверяем завершения
                break

        result *= x_scaled  # Масштабируем результат

        return result


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

        return y_res

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
            y_res = y / 2 * (3 - x * y * y)

        return y_res

    def clear(self):
        for data in self.frame_data:
            data["result_text"].delete(1.0, tk.END)  # Очищаем текстовые поля
            data["entry_a"].delete(0, tk.END)  # Очищаем поле ввода "x"
            data["entry_b"].delete(0, tk.END)  # Очищаем поле ввода "y"

    def show_main_page(self):
        self.controller.show_page("MainPage")
