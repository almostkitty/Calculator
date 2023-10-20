import tkinter as tk
from tkinter import ttk

class SetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = ttk.Label(self, text="Настройки", font=("Helvetica", 20, "bold"))
        label_title.grid(row=0, column=0, columnspan=1, pady=10, padx=10, sticky="ns")

        row_num = 1

        self.selected_theme = tk.StringVar()  # Make it an instance variable
        self.style = ttk.Style()  # Make it an instance variable

        ttk.Label(self, textvariable=self.selected_theme, font="Helvetica 13").grid(row=row_num, column=0, columnspan=3,
                                                                                    pady=10, sticky="nsew")

        row_num += 1

        for theme in self.style.theme_names():
            ttk.Radiobutton(self, text=theme,
                            value=theme,
                            variable=self.selected_theme,
                            command=self.change_theme).grid(row=row_num, column=0, columnspan=3, pady=5, sticky="nsew")
            row_num += 1

        self.button_main_page = ttk.Button(self, text="Назад", command=self.show_main_page)
        self.button_main_page.grid(row=row_num, column=0, columnspan=1, pady=10, sticky="n")

        # Configure columns and rows to expand and fill available space
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        for i in range(row_num + 1):
            self.grid_rowconfigure(i, weight=1)

    def change_theme(self):  # Now it's part of the class
        self.style.theme_use(self.selected_theme.get())

    def show_main_page(self):
        self.controller.show_page("MainPage")

