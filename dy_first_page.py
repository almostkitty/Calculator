import tkinter as tk
from tkinter import ttk
from sympy import sympify, Symbol
import time
import matplotlib.pyplot as plt


class DyFirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Решение уравнений I порядка", font=("Helvetica", 20, "bold"))
        label_title.pack(pady=20, padx=20)

        self.label_function = ttk.Label(self, text="Уравнение:")
        self.entry_function = ttk.Entry(self)
        self.label_function.pack()
        self.entry_function.pack()

        self.label_function = ttk.Label(self, text="Отрезок")
        self.label_function.pack()

        frame_ab = ttk.Frame(self)
        frame_ab.pack()

        self.label_a = ttk.Label(frame_ab, text="От")
        self.entry_a = ttk.Entry(frame_ab, width=3)
        self.label_a.pack(side="left")
        self.entry_a.pack(side="left", padx=5)

        self.label_b = ttk.Label(frame_ab, text="До")
        self.entry_b = ttk.Entry(frame_ab, width=3)
        self.label_b.pack(side="left")
        self.entry_b.pack(side="left", padx=5)

        self.label_function = ttk.Label(self, text="Начальные условия")
        self.label_function.pack()

        frame_cd = ttk.Frame(self)
        frame_cd.pack()

        self.label_c = ttk.Label(frame_cd, text="x0 =")
        self.entry_c = ttk.Entry(frame_cd, width=3)
        self.label_c.pack(side="left")
        self.entry_c.pack(side="left", padx=5)

        self.label_d = ttk.Label(frame_cd, text="y0 =")
        self.entry_d = ttk.Entry(frame_cd, width=3)
        self.label_d.pack(side="left")
        self.entry_d.pack(side="left", padx=5)

        ttk.Label(self, text="Кол-во разбиений:").pack()
        self.entry_partitions = ttk.Entry(self, width=6)
        self.entry_partitions.pack()

        ttk.Label(self, text="Метод:").pack()

        self.method_var = tk.StringVar()
        self.method_var.set("Эйлера")  # Метод по умолчанию

        methods = ["Эйлера", "Рунге–Кутта"]

        for method in methods:
            ttk.Radiobutton(self, text=method, variable=self.method_var, value=method).pack()

        self.result_text = tk.Text(self, height=5, width=50)

        scrollbar = ttk.Scrollbar(self, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack()
        scrollbar.pack()

        ttk.Button(self, text="Вычислить", command=self.calculate).pack()

        self.button_dy_page = ttk.Button(self, text="Назад↩️", command=self.show_dy_page)
        self.button_dy_page.pack()

        self.button_main_page = ttk.Button(self, text="️Главное меню", command=self.show_main_page)
        self.button_main_page.pack()


    def calculate(self):
        try:
            function_str = self.entry_function.get()
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            c = float(self.entry_c.get())
            d = float(self.entry_d.get())
            partitions = int(self.entry_partitions.get())

            method = self.method_var.get()

            start_time = time.time()

            if method == "Эйлера":
                result = self.calculate_euler(function_str, a, b, c, d, partitions)
            elif method == "Рунге–Кутта":
                result = self.calculate_runge_kutta(function_str, a, b, c, d, partitions)

            end_time = time.time()
            elapsed_time = end_time - start_time

            self.result_text.delete(1.0, tk.END)

            pair_number = 1
            for x, y in result:
                formatted_result = f"{pair_number} пара ---- x={x:.3f}, y={y:.3f}\n"
                self.result_text.insert(tk.END, formatted_result)
                pair_number += 1

            # Добавим время выполнения
            self.result_text.insert(tk.END, f"Время выполнения: {elapsed_time:.4f} секунд")

            # Use the after() method to schedule the update_plot() function on the main thread
            self.after(10, lambda: self.update_plot(result, method, partitions))

        except ValueError as e:
            self.result_text.delete(1.0, tk.END)
            error_message = f"Ошибка ввода данных: {str(e)}"
            self.result_text.insert(tk.END, error_message)

    def perform_calculations(self, function_str, a, b, c, d, partitions, method):
        start_time = time.time()

        if method == "Эйлера":
            result = self.calculate_euler(function_str, a, b, c, d, partitions)
        elif method == "Рунге–Кутта":
            result = self.calculate_runge_kutta(function_str, a, b, c, d, partitions)

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Use the main thread to update the text field
        self.result_text.delete(1.0, tk.END)
        for x, y in result:
            formatted_result = f"x={x:.3f}, y={y:.3f}\n"
            self.result_text.insert(tk.END, formatted_result)
        self.result_text.insert(tk.END, f"Время выполнения: {elapsed_time:.4f} секунд")

        # Use the main thread to update the plot
        self.update_plot(result, method, partitions)

    def update_plot(self, result, method, partitions):
        plt.clf()  # Clear the current plot

        # Prepare data for plotting
        x_values, y_values = zip(*result)

        # Plot the graph
        if method == "Эйлера":
            plt.plot(x_values, y_values, label=f"Эйлера ({partitions} разбиений)")
        elif method == "Рунге–Кутта":
            plt.plot(x_values, y_values, label=f"Рунге–Кутта ({partitions} разбиений)")

        # Add labels and legend
        plt.title("Интегральные кривые")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()

        # Show the plot
        plt.pause(0.01)  # Pause to allow the plot to update

    def calculate_euler(self, function_str, a, b, c, d, partitions):
        result = []
        h = (b - a) / partitions

        x, y = Symbol('x'), Symbol('y')
        expression = sympify(function_str)

        while c <= (b - h):
            d = d + h * expression.subs({x: c, y: d})
            result.append((c + h, d))
            c = c + h

        return result

    def calculate_runge_kutta(self, function_str, a, b, c, d, partitions):
        result = []
        h = (b - a) / partitions

        x, y = Symbol('x'), Symbol('y')
        expression = sympify(function_str)

        while c <= (b - h):
            k1 = expression.subs({x: c, y: d})
            k2 = expression.subs({x: c + h / 2, y: d + (h / 2) * k1})
            k3 = expression.subs({x: c + h / 2, y: d + (h / 2) * k2})
            k4 = expression.subs({x: c + h, y: d + h * k3})

            d = d + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

            result.append((c + h, d))
            c = c + h

        return result

    def show_dy_page(self):
        plt.close()
        self.controller.show_page("DySelectPage")

    def show_main_page(self):
        plt.close()
        self.controller.show_page("MainPage")
