from tkinter import *
from pages import MultiPageApp


if __name__ == "__main__":
    app = MultiPageApp()
    app.title("Калькулятор v1.2")
    app.geometry("500x500")
    app.resizable(False, False)
    app.attributes("-alpha", 0.95)
    icon = PhotoImage(file="icon.png")
    app.iconphoto(False, icon)
    app.mainloop()
