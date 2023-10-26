import tkinter as tk
from tkinter import ttk
from sympy import symbols, integrate, pi, sympify
import time


class KratniPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label1 = ttk.Label(self, text="КРАТНЫЙ ИНТЕГРАЛ", font=("Helvetica", 20, "bold"))
        label1.pack(pady=20, padx=20)

        self.label_function = ttk.Label(self, text="Подынтегральная функция:")
        self.entry_function = ttk.Entry(self)
        self.label_function.pack()
        self.entry_function.pack()

        self.label_a = ttk.Label(self, text="Нижний предел(a):")
        self.entry_a = ttk.Entry(self)
        self.label_a.pack()
        self.entry_a.pack()

        self.label_b = ttk.Label(self, text="Верхний предел(b):")
        self.entry_b = ttk.Entry(self)
        self.label_b.pack()
        self.entry_b.pack()

        self.label_c = ttk.Label(self, text="Нижний предел(c):")
        self.entry_c = ttk.Entry(self)
        self.label_c.pack()
        self.entry_c.pack()

        self.label_d = ttk.Label(self, text="Верхний предел(d):")
        self.entry_d = ttk.Entry(self)
        self.label_d.pack()
        self.entry_d.pack()

        ttk.Label(self, text="Кол-во разбиений(nx):").pack()
        self.entry_partitions_nx = ttk.Entry(self)
        self.entry_partitions_nx.pack()

        ttk.Label(self, text="Кол-во разбиений(ny):").pack()
        self.entry_partitions_ny = ttk.Entry(self)
        self.entry_partitions_ny.pack()

        ttk.Label(self, text="Метод:").pack()
        self.method_var = tk.StringVar()
        self.method_combobox = ttk.Combobox(self, textvariable=self.method_var, values=["Кратный интеграл"])
        self.method_combobox.pack()

        self.result_text = tk.Text(self, height=3, width=50)
        self.result_text.pack()

        ttk.Button(self, text="Вычислить", command=self.calculate_integral).pack()
        ttk.Button(self, text="Назад↩️", command=lambda: self.controller.show_page("MainPage")).pack()

    def calculate_integral(self):
        try:
            function_str = self.entry_function.get()
            a = self.get_limit_value(self.entry_a.get())
            b = self.get_limit_value(self.entry_b.get())
            c = self.get_limit_value(self.entry_c.get())
            d = self.get_limit_value(self.entry_d.get())
            nx = self.get_limit_value(self.entry_partitions_nx.get())
            ny = self.get_limit_value(self.entry_partitions_ny.get())

            method = self.method_var.get()

            start_time = time.time()

            if method == "Кратный интеграл":
                result = self.calculate_kratni(function_str, a, b, c, d, nx, ny)

            end_time = time.time()
            elapsed_time = end_time - start_time

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Результат интегрирования: {result}\n"
                                            f"Время выполнения: {elapsed_time:.4f} секунд")

        except ValueError as e:
            self.result_text.delete(1.0, tk.END)
            error_message = f"Ошибка ввода данных: {str(e)}"
            self.result_text.insert(tk.END, error_message)

    def get_limit_value(self, limit_str):
        try:
            value = sympify(limit_str).evalf()
            return float(value)
        except (ValueError, TypeError, SyntaxError):
            raise ValueError(f"Invalid limit value: {limit_str}")

    def calculate_kratni(self, function_str, a, b, c, d, nx, ny):
        result = 0.0
        hx = (b - a) / nx
        hy = (d - c) / ny

        x_symbol, y_symbol = symbols('x y')

        expr = sympify(function_str)

        for x in range(int(nx)):  # nx в int
            xi = a + x * hx
            for y in range(int(ny)):  # ny в int
                yi = c + y * hy

                result += expr.subs({x_symbol: xi, y_symbol: yi}).evalf()

        result *= hx * hy
        return result

    def show_page(self):
        self.controller.show_page("MainPage")
