import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import math
import time


class DyThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Решение СДУ", font=("Helvetica", 20, "bold"))
        label_title.pack(pady=20, padx=20)

        image = PhotoImage(file="sdu.png")

        resized_image = image.subsample(2, 2)

        label_image = ttk.Label(self, image=resized_image)
        label_image.image = resized_image
        label_image.pack()

        frame_xyz = ttk.Frame(self)
        frame_xyz.pack()

        self.label_x = ttk.Label(frame_xyz, text="x:")
        self.entry_x = ttk.Entry(frame_xyz, width=3)
        self.label_x.pack(side="left")
        self.entry_x.pack(side="left", padx=5)

        self.label_y = ttk.Label(frame_xyz, text="y:")
        self.entry_y = ttk.Entry(frame_xyz, width=3)
        self.label_y.pack(side="left")
        self.entry_y.pack(side="left", padx=5)

        self.label_z = ttk.Label(frame_xyz, text="z:")
        self.entry_z = ttk.Entry(frame_xyz, width=3)
        self.label_z.pack(side="left")
        self.entry_z.pack(side="left", padx=5)

        frame_tth = ttk.Frame(self)
        frame_tth.pack()

        self.label_to = ttk.Label(frame_tth, text="t0:")
        self.entry_to = ttk.Entry(frame_tth, width=3)
        self.label_to.pack(side="left")
        self.entry_to.pack(side="left", padx=5)

        self.label_td = ttk.Label(frame_tth, text="t:")
        self.entry_td = ttk.Entry(frame_tth, width=3)
        self.label_td.pack(side="left")
        self.entry_td.pack(side="left", padx=5)

        self.label_h = ttk.Label(frame_tth, text="h:")
        self.entry_h = ttk.Entry(frame_tth, width=5)
        self.label_h.pack(side="left")
        self.entry_h.pack(side="left", padx=5)

        ttk.Label(self, text="Метод:").pack()

        self.result_text = tk.Text(self, height=13, width=50)

        scrollbar = ttk.Scrollbar(self, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack()
        scrollbar.pack()

        ttk.Button(self, text="Решить СДУ", command=self.calculate_system).pack()

        self.button_dy_page = ttk.Button(self, text="Назад↩️", command=self.show_dy_page)
        self.button_dy_page.pack()

        self.button_main_page = ttk.Button(self, text="️Главное меню", command=self.show_main_page)
        self.button_main_page.pack()

    def calculate_system(self):
        try:
            start_time = time.time()

            x = float(self.entry_x.get())
            y = float(self.entry_y.get())
            z = float(self.entry_z.get())
            t_start = float(self.entry_to.get())
            t_end = float(self.entry_td.get())
            h = float(self.entry_h.get())

            result_text = ""

            while t_start < t_end:
                result_text += f"t={t_start}|x={x}|y={y}|z={z}\n\n"
                x1 = x + (((-2 * x) + (5 * z)) * h)
                y1 = y + ((math.sin(t_start - 1) * x - y + 3 * z) * h)
                z1 = z + ((-x + 2 * z) * h)
                x, y, z = x1, y1, z1
                t_start += h

            elapsed_time = time.time() - start_time
            result_text += f"Время выполнения: {elapsed_time:.4f} секунд"

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_text)



        except ValueError as e:
            error_message = f"Ошибка: {str(e)}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, error_message)


    def show_dy_page(self):
        self.controller.show_page("DySelectPage")

    def show_main_page(self):
        self.controller.show_page("MainPage")
