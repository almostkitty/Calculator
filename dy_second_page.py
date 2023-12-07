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

        self.label_equation = ttk.Label(self, text="Уравнение:")
        self.entry_equation = ttk.Entry(self)
        self.label_equation.pack()
        self.entry_equation.pack()

        self.label_interval = ttk.Label(self, text="Отрезок")
        self.label_interval.pack()

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

        self.label_initial_conditions = ttk.Label(self, text="Начальные условия")
        self.label_initial_conditions.pack()

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

        self.label_d_prime = ttk.Label(frame_cd, text="y'0 =")
        self.entry_d_prime = ttk.Entry(frame_cd, width=3)
        self.label_d_prime.pack(side="left")
        self.entry_d_prime.pack(side="left", padx=5)

        ttk.Label(self, text="Кол-во разбиений:").pack()
        self.entry_partitions = ttk.Entry(self, width=6)
        self.entry_partitions.pack()

        ttk.Label(self, text="Метод:").pack()

        self.method_var = tk.StringVar()
        self.method_var.set("Рунге–Кутта")

        methods = ["Рунге–Кутта"]

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
            equation_str = self.entry_equation.get()
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            c = float(self.entry_c.get())
            d = float(self.entry_d.get())
            d_prime = float(self.entry_d_prime.get())
            partitions = int(self.entry_partitions.get())

            method = self.method_var.get()

            start_time = time.time()

            result = self.calculate_runge_kutta_second(equation_str, a, b, c, d, d_prime, partitions)

            end_time = time.time()
            elapsed_time = end_time - start_time

            self.result_text.delete(1.0, tk.END)

            pair_number = 1
            for x, y in result:
                formatted_result = f"{pair_number} пара ---- x={x:.5f}, y={y:.5f}\n"
                self.result_text.insert(tk.END, formatted_result)
                pair_number += 1

            self.result_text.insert(tk.END, f"Время выполнения: {elapsed_time:.5f} секунд")

            self.after(10, lambda: self.update_plot(result, method, partitions))

        except ValueError as e:
            self.result_text.delete(1.0, tk.END)
            error_message = f"Ошибка ввода данных: {str(e)}"
            self.result_text.insert(tk.END, error_message)

    def update_plot(self, result, method, partitions):
        plt.clf()

        x_values, y_values = zip(*result)

        plt.plot(x_values, y_values, label=f"Рунге–Кутта ({partitions} разбиений)", marker='o')
        plt.title("Интегральные кривые")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()

        plt.pause(0.01)


    def calculate_runge_kutta_second(self, equation_str, a, b, c, d, d_prime, partitions):
        result = []
        h = (b - a) / partitions

        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
        equation = sympify(equation_str)

        while c <= (b - h):
            k1_y = d_prime
            k1_z = equation.subs({x: c, y: d, z: d_prime})
            k2_y = d_prime + h * k1_z / 2
            k2_z = equation.subs({x: c + h / 2, y: d + h * k1_y / 2, z: d_prime + h * k1_z / 2})
            k3_y = d_prime + h * k2_z / 2
            k3_z = equation.subs({x: c + h / 2, y: d + h * k2_y / 2, z: d_prime + h * k2_z / 2})
            k4_y = d_prime + h * k3_z
            k4_z = equation.subs({x: c + h, y: d + h * k3_y, z: d_prime + h * k3_z})
            d_prime = d_prime + h / 6 * (k1_z + 2 * k2_z + 2 * k3_z + k4_z)
            d = d + h / 6 * (k1_y + 2 * k2_y + 2 * k3_y + k4_y)
            result.append((c + h, d))
            c = c + h
        return result

    def show_dy_page(self):
        plt.close()
        self.controller.show_page("DySelectPage")

    def show_main_page(self):
        plt.close()
        self.controller.show_page("MainPage")
