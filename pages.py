import tkinter as tk
from main_page import MainPage
from integration_page import IntegrationPage
from dev_page import DevPage
from settings_page import SetPage
from kratni_page import KratniPage
from dyselect_page import DySelectPage
from dy_first_page import DyFirstPage
from dy_second_page import DySecondPage
from dy_third_page import DyThirdPage


class MultiPageApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.pages = {}

        for PageClass in (MainPage, IntegrationPage, DevPage, SetPage, KratniPage, DySelectPage, DyFirstPage, DySecondPage, DyThirdPage):
            page_name = PageClass.__name__
            page = PageClass(parent=container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("MainPage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()
