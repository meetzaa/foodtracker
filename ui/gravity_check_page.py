from tkinter import Canvas, Label, Button, Entry, PhotoImage, messagebox
from tkinter.font import Font
from .base_page import BasePage
from utils.utils import save_user_details
import os

class GravityCheckPage(BasePage):
    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.setup_ui()

    def setup_ui(self):
        self.canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.images = []

        self.load_image("assets/frame3/image_1.png", 735.0, 35.0)
        self.load_image("assets/frame3/image_2.png", 107.0, 196.0)
        self.load_image("assets/frame3/image_3.png", 150.0, 221.0)
        self.load_image("assets/frame3/image_4.png", 398.0, 196.0)
        self.load_image("assets/frame3/image_5.png", 464.0, 212.0)
        self.load_image("assets/frame3/image_6.png", 692.0, 196.0)
        self.load_image("assets/frame3/entry_age.png", 750.0, 298.0)
        self.load_image("assets/frame3/entry_cm.png", 454.0, 298.0)
        self.load_image("assets/frame3/entry_kg.png", 160.0, 298.0)


        self.load_button("assets/frame3/NextStep.png", 750.0, 405.0, 120.0, 30.0, self.handle_save_user_details)

        self.entry_kg = Entry(self, bd=0, bg="#F9F8F8", fg="#000716", highlightthickness=0)
        self.entry_kg.place(x=170.0, y=305.0, width=40.0, height=25.0)
        self.entry_kg.bind("<Return>", self.handle_save_user_details)

        self.entry_cm = Entry(self, bd=0, bg="#F9F8F8", fg="#000716", highlightthickness=0)
        self.entry_cm.place(x=464.0, y=305.0, width=40.0, height=25.0)
        self.entry_cm.bind("<Return>", self.handle_save_user_details)

        self.entry_age = Entry(self, bd=0, bg="#F9F8F8", fg="#000716", highlightthickness=0)
        self.entry_age.place(x=760.0, y=305.0, width=40.0, height=25.0)
        self.entry_age.bind("<Return>", self.handle_save_user_details)

        font_large = Font(family="Consolas", slant="italic", size=32)
        font_small = Font(family="Consolas", slant="italic", size=16)
        font_medium = Font(family="Consolas", slant="italic", size=20)

        Label(self, text="Gravity Check!", font=font_large, bg="#DAE6E4").place(x=111, y=50)
        Label(self, text="Enter your details to keep your food in flight!", font=font_small, bg="#DAE6E4").place(x=111, y=115)
        Label(self, text="kg", font=font_small, bg="#FFFCF1").place(x=226, y=305)
        Label(self, text="cm", font=font_small, bg="#FFFCF1").place(x=516, y=305)
        Label(self, text="Age", font=font_medium, bg="#FFFCF1").place(x=755, y=235)

    def update(self, user_key):
        self.user_key = user_key

    def handle_save_user_details(self, event=None):
        weight_value = self.entry_kg.get()
        height_value = self.entry_cm.get()
        age_value = self.entry_age.get()

        print(f"Debug: Weight value: {weight_value}")
        print(f"Debug: Height value: {height_value}")
        print(f"Debug: Age value: {age_value}")

        if not weight_value or not height_value or not age_value:
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            save_user_details(self.controller, self.user_key, weight_value, height_value, age_value)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            print(f"Debug: Exception: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def load_image(self, path, x, y):
        try:
            img = PhotoImage(file=path)
            self.canvas.create_image(x, y, image=img, anchor='nw')
            self.images.append(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")

    def load_button(self, path, x, y, width, height, command):
        try:
            img = PhotoImage(file=path)
            button = Button(self, image=img, borderwidth=0, highlightthickness=0, command=command, relief="flat")
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        except Exception as e:
            print(f"Error loading button image {path}: {e}")
