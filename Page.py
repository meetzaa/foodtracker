from tkinter import Frame

class Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

    def show(self):
        self.lift()