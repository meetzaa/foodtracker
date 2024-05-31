from tkinter import Canvas, Label, Button, PhotoImage, Entry
from tkinter.font import Font
from .base_page import BasePage
from utils.utils import get_user_details_by_user_key

class Profile2Page(BasePage):
    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.configure(bg="#DAE6E4")

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("Back.png", 14.0, 18.0, 55.0, 36.0, lambda: controller.show_page("AppPage1", user_key)),
            ("back_page.png", 182.94596222486825, 263.0, 32.0, 39.0, lambda: controller.show_page("ProfilePage", user_key)),
            ("image_1.png", 90.0, 35.0),
            ("image_2.png", 47.0, 65.0),
            ("image_3.png", 161.0, 459.0),
            ("image_4.png", 581.0, 42.0),
            ("image_5.png", 935.0, 354.0),
            ("image_6.png", 891.0, 300.0),
            ("image_7.png", 741.0, 82.0),
            ("image_8.png", 830.0, 5.0),
            ("image_9.png", 10.0, 354.0),
            ("image_10.png", 548.0, 491.0),
            ("image_11.png", 52.0, 180.0),
            ("image_12.png", 240.0, -75.0),
            ("image_13.png", 818.0, 429.0),
            ("image_14.png", 912.0, 85.0),
            ("image_15.png", 430.0, 50.0),
            ("image_16.png", 430.0, 50.0),
            ("image_17.png", 267.0, 243.0),
            ("image_18.png", 267.0, 312.0),
            ("image_19.png", 520.0, 312.0),
            ("image_20.png", 520.0, 243.0)
        ]

        for details in image_details:
            image_name, x, y, *args = details
            img = PhotoImage(file=f"assets/frame131/{image_name}")
            self.images.append(img)

            if len(args) == 3:
                width, height, command = args
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief='flat', command=command)
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                canvas.create_image(x, y, image=img, anchor='nw')

        font_large = Font(family="Consolas", slant="italic", size=20)
        font_medium = Font(family="Consolas", slant="italic", size=16)

        Label(self, text="My Profile", font=font_large, bg="#FFFCF1").place(x=260, y=105)
        Label(self, text="Weight", font=font_medium, bg="#FFFCF1").place(x=267, y=193)
        Label(self, text="Height", font=font_medium, bg="#FFFCF1").place(x=267, y=262)
        Label(self, text="BMI", font=font_medium, bg="#FFFCF1").place(x=520, y=193)
        Label(self, text="Goal", font=font_medium, bg="#FFFCF1").place(x=520, y=262)

        self.weight_entry = Entry(self, bd=0, bg="#FFFCF1", fg="#000716", highlightthickness=0, readonlybackground="#FFFCF1", state='readonly')
        self.weight_entry.place(x=262.0657958984375, y=213.0, width=200.0, height=20.0)

        self.height_entry = Entry(self, bd=0, bg="#FFFCF1", fg="#000716", highlightthickness=0, readonlybackground="#FFFCF1", state='readonly')
        self.height_entry.place(x=262.0657958984375, y=282.0, width=200.0, height=20.0)

        self.bmi_entry = Entry(self, bd=0, bg="#FFFCF1", fg="#000716", highlightthickness=0, readonlybackground="#FFFCF1", state='readonly')
        self.bmi_entry.place(x=515.0657958984375, y=282.0, width=200.0, height=20.0)

        self.goal_entry = Entry(self, bd=0, bg="#FFFCF1", fg="#000716", highlightthickness=0, readonlybackground="#FFFCF1", state='readonly')
        self.goal_entry.place(x=515.0657958984375, y=282.0, width=200.0, height=20.0)

    def update(self, user_key=None):
        self.user_key = user_key or self.user_key
        user_details = get_user_details_by_user_key(self.user_key)
        print(f"Debug: Retrieved user details in Profile2Page: {user_details}")
        if user_details and "details" in user_details:
            details = user_details["details"]
            self.weight_entry.config(state='normal')
            self.weight_entry.delete(0, "end")
            self.weight_entry.insert(0, details.get("Weight", ""))
            self.weight_entry.config(state='readonly')
            self.weight_entry.place(x= 270, y=223)

            self.height_entry.config(state='normal')
            self.height_entry.delete(0, "end")
            self.height_entry.insert(0, details.get("Height", ""))
            self.height_entry.config(state='readonly')
            self.height_entry.place(x= 270, y=292)

            self.bmi_entry.config(state='normal')
            self.bmi_entry.delete(0, "end")
            self.bmi_entry.insert(0, self.calculate_bmi(details.get("Weight"), details.get("Height")))
            self.bmi_entry.config(state='readonly')
            self.bmi_entry.place(x= 523, y=223)

            self.goal_entry.config(state='normal')
            self.goal_entry.delete(0, "end")
            self.goal_entry.insert(0, "Maintain Weight")  # Add actual goal if needed
            self.goal_entry.config(state='readonly')
            self.goal_entry.place(x= 523, y=292)

    def calculate_bmi(self, weight, height):
        if weight and height:
            try:
                weight = float(weight)
                height = float(height) / 100  # Convert cm to meters
                bmi = weight / (height ** 2)
                return f"{bmi:.2f}"
            except ValueError:
                return "N/A"
        return "N/A"