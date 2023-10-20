from pages import MultiPageApp


if __name__ == "__main__":
    app = MultiPageApp()
    # app.geometry("450x500")
    # app.resizable(False, False)
    app.attributes("-alpha", 0.95)
    app.mainloop()
