import tkinter as tk
from tkinter import ttk
from sympy import sympify


class IntegrationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label_title = ttk.Label(self, text="ИНТЕГРИРОВАНИЕ", font=("Helvetica", 20, "bold"))
        label_title.grid(row=0, column=0, columnspan=1, pady=10, padx=10, sticky="ns")

        labels = [
            "Подынтегральная функция:",
            "Нижний предел(a):",
            "Верхний предел(b):",
            "Точность:",
            "Кол-во разбиений:",
            "Метод:"
        ]

        self.label_function = ttk.Label(self, text=labels[0])
        self.entry_function = ttk.Entry(self)

        self.label_a = ttk.Label(self, text=labels[1])
        self.entry_a = ttk.Entry(self)

        self.label_b = ttk.Label(self, text=labels[2])
        self.entry_b = ttk.Entry(self)

        self.label_partitions = ttk.Label(self, text=labels[3])
        self.entry_tochno = ttk.Entry(self)

        self.label_partitions = ttk.Label(self, text=labels[4])
        self.entry_partitions = ttk.Entry(self)


        self.label_method = ttk.Label(self, text=labels[5])
        self.method_var = tk.StringVar()
        self.method_combobox = ttk.Combobox(self, textvariable=self.method_var,
                                            values=["Прямоугольники левых частей",
                                                    "Прямоугольники левых частей I",
                                                    "Прямоугольники левых частей II",
                                                    "Прямоугольники правых частей",
                                                    "Трапеции",
                                                    "Параболы"])


        self.calculate_button = ttk.Button(self, text="Вычислить", command=self.calculate_integral)

        self.button_main_page = ttk.Button(self, text="Сравнить результаты", command=lambda: self.controller.show_page("TablePage"))
        self.button_main_page.grid(row=8, column=0, columnspan=3, pady=10)

        self.button_main_page = ttk.Button(self, text="Назад", command=lambda: self.controller.show_page("MainPage"))
        self.button_main_page.grid(row=10, column=0, columnspan=3, pady=10)

        for i, label_text in enumerate(labels, start=1):
            tk.Label(self, text=label_text).grid(row=i, column=0, sticky="w", padx=10, pady=5)

        entry_widgets = [self.entry_function, self.entry_a, self.entry_b, self.entry_tochno, self.entry_partitions, self.method_combobox]
        for i, entry_widget in enumerate(entry_widgets, start=1):
            entry_widget.grid(row=i, column=1, padx=10, pady=5)

        self.calculate_button.grid(row=7, column=0, columnspan=3, pady=10)


    def calculate_integral(self):
        function_str = self.entry_function.get()
        a = float(self.entry_a.get())  # ВЕРХНИЙ ПРЕДЕЛ
        b = float(self.entry_b.get())  # НИЖНИЙ ПРЕДЕЛ
        tochno = float(self.entry_tochno.get())
        partitions = int(self.entry_partitions.get())  # РАЗБИЕНИЯ

        method = self.method_var.get()

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

        result_label = ttk.Label(self, text=f"Результат интегрирования: {result}")
        result_label.grid(row=9, column=0, columnspan=3, pady=10)


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
        step = (b - a) / partitions
        IN = 0.0
        I2N = 0.0
        R = 0.0
        x = a

        func = sympify(function_str)
        result = 0.0

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
                break  # добавлено условие выхода из цикла

        return result

    def calculate_left_second(self, function_str, a, b, partitions, tochno):
        step = (b - a) / partitions
        IN = 0
        S2 = 0
        x = a
        result = 0.0

        func = sympify(function_str)

        # S2 += abs(func.subs('x', x))
        # x += step

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
            result = I2N  # Исправлено: I2N присваивается в переменную result

        # print('это медленный метод', result)
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



