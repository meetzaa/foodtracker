from tkinter import Frame

class BasePage(Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

    def show(self, *args):
        self.lift()