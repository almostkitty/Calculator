import tkinter as tk
from tkinter import ttk


class DevPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = ttk.Label(self, text="Информация о разработчиках", font=("Helvetica", 20, "bold"))
        self.label.pack(pady=20)

        self.developer_info = tk.Text(self, wrap=tk.WORD, width=27, height=13)
        self.developer_info.insert(tk.END, "--Герман П.\n"
                                           "Разработка\n\n"
                                           "--Иван П.\n"
                                           "Алгоритмы\n\n"
                                           "--Дмитрий Щ.\n"
                                           "Интерфейс и Документация\n\n"
                                           "--Обратная связь:\n"
                                           "test@mail.ru\n\n"
                                           "--СПб 2023--")
        self.developer_info.pack(pady=20)

        button_back_main = ttk.Button(self, text="Назад↩️", command=lambda: controller.show_page("MainPage"))
        button_back_main.pack(fill="x")
