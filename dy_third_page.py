import tkinter as tk
from tkinter import ttk
from sympy import sympify, Symbol
import time
import matplotlib.pyplot as plt

class DyThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Решение СДУ", font=("Helvetica", 20, "bold"))
        label_title.pack(pady=20, padx=20)

        frame_ux = ttk.Frame(self)
        frame_ux.pack()

        self.label_function_x = ttk.Label(frame_ux, text="Уравнение dx/dt:")
        self.entry_function_x = ttk.Entry(frame_ux)
        self.label_function_x.pack(side="left")
        self.entry_function_x.pack(side="left")

        frame_uy = ttk.Frame(self)
        frame_uy.pack()

        self.label_function_y = ttk.Label(frame_uy, text="Уравнение dy/dt:")
        self.entry_function_y = ttk.Entry(frame_uy)
        self.label_function_y.pack(side="left")
        self.entry_function_y.pack(side="left")

        frame_uz = ttk.Frame(self)
        frame_uz.pack()

        self.label_function_z = ttk.Label(frame_uz, text="Уравнение dz/dt:")
        self.entry_function_z = ttk.Entry(frame_uz)
        self.label_function_z.pack(side="left")
        self.entry_function_z.pack(side="left")

        # Ввод начальных условий
        self.label_c = ttk.Label(self, text="Начальные условия:")
        self.label_c.pack()

        frame_cd = ttk.Frame(self)
        frame_cd.pack()

        self.label_x0 = ttk.Label(frame_cd, text="x0 =")
        self.entry_x0 = ttk.Entry(frame_cd, width=3)
        self.label_x0.pack(side="left")
        self.entry_x0.pack(side="left", padx=5)

        self.label_y0 = ttk.Label(frame_cd, text="y0 =")
        self.entry_y0 = ttk.Entry(frame_cd, width=3)
        self.label_y0.pack(side="left")
        self.entry_y0.pack(side="left", padx=5)

        self.label_z0 = ttk.Label(frame_cd, text="z0 =")
        self.entry_z0 = ttk.Entry(frame_cd, width=3)
        self.label_z0.pack(side="left")
        self.entry_z0.pack(side="left", padx=5)

        # Отрезок и шаг
        ttk.Label(self, text="Отрезок:").pack()

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

        ttk.Label(self, text="Шаг (h):").pack()
        self.entry_h = ttk.Entry(self, width=6)
        self.entry_h.pack()

        # Метод
        ttk.Label(self, text="Метод:").pack()

        self.method_var = tk.StringVar()
        self.method_var.set("Эйлера")  # Метод по умолчанию

        ttk.Radiobutton(self, text="Эйлера", variable=self.method_var, value="Эйлера").pack()

        # Результаты
        self.result_text = tk.Text(self, height=5, width=50)

        scrollbar = ttk.Scrollbar(self, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack()
        scrollbar.pack()

        # Кнопки
        ttk.Button(self, text="Вычислить", command=self.calculate).pack()

        self.button_dy_page = ttk.Button(self, text="Назад↩️", command=self.show_dy_page)
        self.button_dy_page.pack()

        self.button_main_page = ttk.Button(self, text="️Главное меню", command=self.show_main_page)
        self.button_main_page.pack()

    def calculate(self):
        try:
            function_x_str = self.entry_function_x.get()
            function_y_str = self.entry_function_y.get()
            function_z_str = self.entry_function_z.get()
            x0 = float(self.entry_x0.get())
            y0 = float(self.entry_y0.get())
            z0 = float(self.entry_z0.get())
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            h = float(self.entry_h.get())
            method = self.method_var.get()

            # Проведение расчетов и вывод результатов
            result = self.calculate_system(
                function_x_str, function_y_str, function_z_str, x0, y0, z0, a, b, h, method
            )

            self.display_results(result)

        except ValueError as e:
            self.result_text.delete(1.0, tk.END)
            error_message = f"Ошибка ввода данных: {str(e)}"
            self.result_text.insert(tk.END, error_message)

    def update_plot(self, result):
        plt.clf()  # Очистим текущий график

        # Подготовка данных для построения
        t_values, x_values, y_values, z_values = zip(*result)

        # Построение графика
        plt.plot(t_values, x_values, label="x(t)")
        plt.plot(t_values, y_values, label="y(t)")
        plt.plot(t_values, z_values, label="z(t)")

        # Добавление меток и легенды
        plt.title("Графики x(t), y(t), z(t)")
        plt.xlabel("t")
        plt.ylabel("Значения")
        plt.legend()

        # Показать график
        plt.pause(0.01)  # Пауза для обновления графика

    def calculate_system(self, function_x_str, function_y_str, function_z_str, x0, y0, z0, a, b, h, method):
        result = []
        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
        expressions = [
            sympify(function_x_str),
            sympify(function_y_str),
            sympify(function_z_str)
        ]

        while a <= (b - h):
            values = [a, x0, y0, z0]
            new_values = [values[i] + h * expressions[i - 1].subs({x: values[1], y: values[2], z: values[3]}) for i in
                          range(1, 4)]
            result.append((values[0], new_values[0], new_values[1], new_values[2]))
            a += h
            x0, y0, z0 = new_values[0], new_values[1], new_values[2]

        # Обновление графика
        self.update_plot(result)

        return result

    def display_results(self, result):
        self.result_text.delete(1.0, tk.END)

        for row in result:
            t, x, y, z = row
            formatted_result = f"t={t:.3f}, x={x.evalf():.3f}, y={y.evalf():.3f}, z={z.evalf():.3f}\n"
            self.result_text.insert(tk.END, formatted_result)

        self.result_text.insert(tk.END, "Результаты вычислений:\n")

    def show_dy_page(self):
        plt.close()
        self.controller.show_page("DySelectPage")

    def show_main_page(self):
        plt.close()
        self.controller.show_page("MainPage")
