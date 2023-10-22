import tkinter as tk
from tkinter import ttk

class SetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Настройки", font=("Helvetica", 20, "bold"))
        label_title.pack(pady=20, padx=20)

        label2 = ttk.Label(self, text="↪️Выберите тему↩️")
        label2.pack(pady=10, padx=20)


        self.selected_theme = tk.StringVar()
        self.style = ttk.Style()

        for theme in self.style.theme_names():
            ttk.Radiobutton(self, text=theme,
                            value=theme,
                            variable=self.selected_theme,
                            command=self.change_theme).pack(fill="both")

        self.button_main_page = ttk.Button(self, text="Назад↩️", command=self.show_main_page)
        self.button_main_page.pack(pady=10, side="top")

    def change_theme(self):
        self.style.theme_use(self.selected_theme.get())

    def show_main_page(self):
        self.controller.show_page("MainPage")
