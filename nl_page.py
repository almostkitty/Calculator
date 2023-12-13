import tkinter as tk
from tkinter import ttk
from sympy import symbols, diff, lambdify
import time
import numpy as np
import matplotlib.pyplot as plt


class NlPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="НЕЛИНЕЙНЫЕ", font=("Helvetica", 20, "bold"))
        label_title.pack(pady=20, padx=20)

        self.equation_var = tk.StringVar()
        self.method_var = tk.StringVar(value="Касательных")
        self.interval_var = tk.StringVar()
        self.tolerance_var = tk.DoubleVar(value=1e-6)

        equation_label = tk.Label(self, text="Уравнение:")
        equation_label.pack()
        self.equation_entry = ttk.Entry(self, textvariable=self.equation_var)
        self.equation_entry.pack()

        ttk.Label(self, text="Метод:").pack()
        self.method_combobox = ttk.Combobox(self, textvariable=self.method_var,
                                            values=["Касательных", "Хорд", "Отрезков"])
        self.method_combobox.pack()

        interval_label = tk.Label(self, text="Отрезок [a, b]:")
        interval_label.pack()
        self.interval_entry = ttk.Entry(self, textvariable=self.interval_var)
        self.interval_entry.pack()

        tolerance_label = tk.Label(self, text="Точность:")
        tolerance_label.pack()
        self.tolerance_entry = ttk.Entry(self, textvariable=self.tolerance_var)
        self.tolerance_entry.pack()

        result_label = tk.Label(self, text="Результат:")
        result_label.pack()

        self.result_text = tk.Text(self, height=3, width=50)
        self.result_text.pack()

        self.calculate_button = ttk.Button(self, text="Вычислить", command=self.solve_equation)
        self.calculate_button.pack()

        self.button_main_page = ttk.Button(self, text="️Главное меню", command=self.show_main_page)
        self.button_main_page.pack()

    def solve_equation(self):
        try:
            x = symbols('x')
            equation_str = self.equation_var.get()
            equation = self.parse_equation(equation_str)

            method = self.method_var.get()
            interval_str = self.interval_var.get()
            a, b = map(float, interval_str.split())
            tolerance = float(self.tolerance_var.get())

            start_time = time.time()

            if method == "Касательных":
                result = self.newton_method(equation, diff(equation(x), x), a, b, tolerance)
            elif method == "Хорд":
                result = self.hord_method(equation, a, b, tolerance)
            elif method == "Отрезков":
                result = self.bisection_method(equation, a, b, tolerance)
            else:
                result = "Выбран неверный метод."

            end_time = time.time()
            elapsed_time = end_time - start_time

            # Plot the graph
            x_values = np.linspace(a, b, 100)
            y_values = equation(x_values)
            plt.plot(x_values, y_values, label=f"{equation_str}", color='blue')
            plt.scatter([result], [equation(result)], color='red', marker='o', label='Root')
            plt.legend()
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('График')
            plt.show(block=False)

            self.result_text.config(state='normal')
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"Результат: {result}\nВремя выполнения: {elapsed_time:.5f} секунд")
            self.result_text.config(state='disabled')

            plt.pause(0.1)  # Pause to allow time for the plot to render

        except ValueError as e:
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            if "Метод бисекции" in str(e):
                error_message = "Ошибка ввода данных: Неверно выбран интервал для метода бисекции."
            else:
                error_message = f"Ошибка ввода данных: {str(e)}"
            self.result_text.insert(tk.END, error_message)

        self.result_text.config(state='disabled')

    def newton_method(self, func, func_derivative, a, b, tol=1e-6, max_iter=100):
        x = (a + b) / 2
        for i in range(max_iter):
            f_value = func(x)

            f_derivative_value = func_derivative.subs('x', x)

            if abs(f_value) < tol:
                return x  #

            if f_derivative_value == 0:
                raise ValueError("Производная равна нулю.")

            x = x - f_value / f_derivative_value

            if abs(f_value) < tol:
                return x

        raise ValueError("Достигнуто максимальное количество итераций. Метод Ньютона не сходится.")

    def hord_method(self, func, a, b, tol=1e-6, max_iter=100):
        if func(a) * func(b) >= 0:
            raise ValueError("Метод хорд требует, чтобы функция принимала разные знаки на концах интервала.")

        for i in range(max_iter):
            f_a = func(a)
            f_b = func(b)

            x = (a * f_b - b * f_a) / (f_b - f_a)

            f_x = func(x)

            if abs(f_x) < tol:
                return x

            if f_a * f_x < 0:
                b = x
            else:
                a = x

        raise ValueError("Достигнуто максимальное количество итераций. Метод хорд не сходится.")

    def bisection_method(self, func, a, b, tol=1e-6, max_iter=100):
        if func(a) * func(b) >= 0:
            raise ValueError("Метод бисекции требует, чтобы функция принимала разные знаки на концах интервала.")

        for i in range(max_iter):
            c = (a + b) / 2

            f_c = func(c)

            if abs(f_c) < tol:
                return c

            if func(a) * f_c < 0:
                b = c
            else:
                a = c

        raise ValueError("Достигнуто максимальное количество итераций. Метод бисекции не сходится.")

    def parse_equation(self, equation_str):
        x = symbols('x')
        equation = lambdify(x, equation_str, 'numpy')
        return equation

    def show_main_page(self):
        self.controller.show_page("MainPage")
