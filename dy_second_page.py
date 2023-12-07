import tkinter as tk
from tkinter import ttk
from sympy import sympify, Symbol
import time
import matplotlib.pyplot as plt

class DySecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Решение уравнений II порядка", font=("Helvetica", 20, "bold"))
        label_title.pack(pady=20, padx=20)

        frame_ur = ttk.Frame(self)
        frame_ur.pack()

        self.label_function_1 = ttk.Label(frame_ur, text="Ур–ние:")
        self.entry_function = ttk.Entry(frame_ur)
        self.label_function_1.pack(side="left")
        self.entry_function.pack(side="left")


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

        self.label_c = ttk.Label(frame_cd, text="")
        self.entry_c = ttk.Entry(frame_cd, width=3)
        self.label_c.pack(side="left")
        self.entry_c.pack(side="left", padx=5)

        self.label_d = ttk.Label(frame_cd, text="")
        self.entry_d = ttk.Entry(frame_cd, width=3)
        self.label_d.pack(side="left")
        self.entry_d.pack(side="left", padx=5)

        # Bind the function to the entry widget
        self.entry_a.bind('<FocusOut>', self.update_labels)

        ttk.Label(self, text="Шаг:").pack()
        self.entry_h = ttk.Entry(self, width=6)
        self.entry_h.pack()

        ttk.Label(self, text="Метод:").pack()

        self.method_var = tk.StringVar()
        self.method_var.set("Эйлера")  # Метод по умолчанию

        methods = ["Эйлера"]

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

    def update_labels(self, event):
        # Get the value from entry_a and update labels
        a_value = self.entry_a.get()
        self.label_c.config(text=f"y'({a_value}) =")
        self.label_d.config(text=f"y''({a_value}) =")

    def calculate(self):
        try:
            function_str = self.entry_function.get()
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            c = float(self.entry_c.get())
            d = float(self.entry_d.get())
            h = int(self.entry_h.get())

            result = self.calculate_double_euler(function_str, a, b, c, d, h)

            start_time = time.time()

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
            self.after(10, lambda: self.update_plot(result, h))

        except ValueError as e:
            self.result_text.delete(1.0, tk.END)
            error_message = f"Ошибка ввода данных: {str(e)}"
            self.result_text.insert(tk.END, error_message)


    def perform_calculations(self, function_str, a, b, c, d, h, method):
        start_time = time.time()

        result = self.calculate_euler(function_str, a, b, c, d, h)

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Use the main thread to update the text field
        self.result_text.delete(1.0, tk.END)
        for x, y in result:
            formatted_result = f"x={x:.3f}, y={y:.3f}\n"
            self.result_text.insert(tk.END, formatted_result)
        self.result_text.insert(tk.END, f"Время выполнения: {elapsed_time:.4f} секунд")

        # Use the main thread to update the plot
        self.update_plot(result, method, h)

    def update_plot(self, result, method, h):
        plt.clf()  # Clear the current plot

        # Prepare data for plotting
        x_values, y_values = zip(*result)

        # Plot the graph
        plt.plot(x_values, y_values, label=f"Эйлера ({h} разбиений)")

        # Add labels and legend
        plt.title("Интегральные кривые")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()

        # Show the plot
        plt.pause(0.01)  # Pause to allow the plot to update

    def calculate_euler(function_str, a, b, c, d, h):
        result = []

        x, y = Symbol('x'), Symbol('y')
        expression = sympify(function_str)

        while c <= (b - h):
            dy1 = h * expression.subs({x: c, y: d})
            dy2 = h * expression.subs({x: c + h, y: d + dy1})

            d = d + (dy1 + dy2) / 2
            result.append((c + h, d))
            c = c + h

        return result


    def show_dy_page(self):
        plt.close()
        self.controller.show_page("DySelectPage")

    def show_main_page(self):
        plt.close()
        self.controller.show_page("MainPage")
