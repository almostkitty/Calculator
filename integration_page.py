import tkinter as tk
from tkinter import ttk
from sympy import sympify
import time


class IntegrationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label1 = ttk.Label(self, text="ИНТЕГРИРОВАНИЕ", font=("Helvetica", 20, "bold"))
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

        self.label_tochno = ttk.Label(self, text="Точность:")
        self.entry_tochno = ttk.Entry(self)
        self.label_tochno.pack()
        self.entry_tochno.pack()

        ttk.Label(self, text="Кол-во разбиений:").pack()
        self.entry_partitions = ttk.Entry(self)
        self.entry_partitions.pack()

        ttk.Label(self, text="Метод:").pack()
        self.method_var = tk.StringVar()
        self.method_combobox = ttk.Combobox(self, textvariable=self.method_var,
                                           values=["Прямоугольники левых частей",
                                                   "Прямоугольники левых частей I",
                                                   "Прямоугольники левых частей II",
                                                   "Прямоугольники правых частей",
                                                   "Трапеции",
                                                   "Параболы"])
        self.method_combobox.pack()

        self.result_text = tk.Text(self, height=3, width=50)
        self.result_text.pack()

        ttk.Button(self, text="Вычислить", command=self.calculate_integral).pack()
        ttk.Button(self, text="Назад↩️", command=lambda: self.controller.show_page("MainPage")).pack()

    def calculate_integral(self):
        try:
            function_str = self.entry_function.get()
            a = float(self.entry_a.get())  # ВЕРХНИЙ ПРЕДЕЛ
            b = float(self.entry_b.get())  # НИЖНИЙ ПРЕДЕЛ
            tochno = float(self.entry_tochno.get())
            partitions = int(self.entry_partitions.get())  # РАЗБИЕНИЯ

            method = self.method_var.get()

            start_time = time.time()

            if method == "Прямоугольники левых частей":
                result = self.calculate_left_rectangles(function_str, a, b, partitions)
            elif method == "Прямоугольники левых частей I":
                result = self.calculate_left_first(function_str, a, b, partitions, tochno)
            elif method == "Прямоугольники левых частей II":
                result = self.calculate_left_second(function_str, a, b, partitions, tochno)
            elif method == "Прямоугольники правых частей":
                result = self.calculate_right_rectangles(function_str, a, b, partitions)
            elif method == "Трапеции":
                result = self.calculate_trapezoids(function_str, a, b, partitions)
            elif method == "Параболы":
                result = self.calculate_parabolas(function_str, a, b, partitions)
            elif method == "Кратный интеграл":
                result = self.calculate_kratni(function_str, a, b, partitions)

            end_time = time.time()
            elapsed_time = end_time - start_time

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Результат интегрирования: {result}\n"
                                             f"Время выполнения: {elapsed_time:.4f} секунд")

        except ValueError as e:
            self.result_text.delete(1.0, tk.END)
            error_message = f"Ошибка ввода данных: {str(e)}"
            self.result_text.insert(tk.END, error_message)

    def calculate_left_rectangles(self, function_str, a, b, partitions):
        result = 0.0
        step = (b - a) / partitions

        for i in range(partitions):
            x = a + i * step
            expr = sympify(function_str)
            result += expr.subs('x', x)

        result *= step
        return result

    def calculate_left_first(self, function_str, a, b, partitions, tochno):
        result = 0.0
        step = (b - a) / partitions
        IN = 0.0
        I2N = 0.0
        R = 0.0
        x = a
        func = sympify(function_str)

        while True:
            result = 0.0
            x = a
            while x <= (b - step):
                result = result + func.subs('x', x)
                x = x + step

            I2N = step * result
            R = abs(I2N - IN)
            IN = I2N
            step = step / 2

            result = I2N

            if R <= tochno:
                break

        return result

    def calculate_left_second(self, function_str, a, b, partitions, tochno):
        step = (b - a) / partitions
        IN = 0
        S2 = 0
        x = a
        result = 0.0

        func = sympify(function_str)

        while x <= b - step:
            S2 += abs(func.subs('x', x))
            x += step

        I2N = step * S2
        R = abs(I2N - IN)
        IN = I2N
        step /= 2

        while R > tochno:
            I2N = 0
            x = a + step / 2

            while x <= b - step:
                I2N += abs(func.subs('x', x))
                x += step

            I2N = (step / 2) * (S2 + 2 * I2N)
            R = abs(I2N - IN)
            IN = I2N
            step /= 2
            result = I2N

        return result


    def calculate_right_rectangles(self, function_str, a, b, partitions):
        result = 0.0
        step = (b - a) / partitions

        for i in range(1, partitions + 1):
            x = a + i * step
            expr = sympify(function_str)
            result += expr.subs('x', x)

        result *= step
        return result

    def calculate_trapezoids(self, function_str, a, b, partitions):
        result = 0.0
        step = (b - a) / partitions

        for i in range(partitions):
            x1 = a + i * step
            x2 = a + (i + 1) * step
            expr = sympify(function_str)
            result += (expr.subs('x', x1) + expr.subs('x', x2)) / 2

        result *= step
        return result

    def calculate_parabolas(self, function_str, a, b, partitions):
        result = 0.0
        step = (b - a) / partitions

        for i in range(partitions):
            x1 = a + i * step
            x2 = a + (i + 1) * step
            x3 = a + (i + 2) * step
            expr = sympify(function_str)
            result += (expr.subs('x', x1) + 4 * expr.subs('x', x2) + expr.subs('x', x3)) / 6

        result *= step
        return result


    def show_page(self):
        self.controller.show_page("MainPage")

