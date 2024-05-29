from tkinter import Canvas, Label, Button, PhotoImage, Listbox, END, Frame, messagebox
from tkinter.font import Font
from .base_page import BasePage
from google.cloud import firestore
from firebase_config import db  # Ensure this is correctly importing your Firestore configuration
from pathlib import Path
from .add_food_page import AddFoodPage


class LogFoodPage(BasePage):
    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.configure(bg="#DAE6E4")

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("image_1.png", 30.0, 70.0, None, None, None),
            ("image_2.png", 321.0, 70.0, None, None, None),
            ("image_3.png", 612.0, 70.0, None, None, None),
            ("image_4.png", 184.0, 329.0, None, None, None),
            ("AddF_Breakfast.png", 79.0, 145.0, 110.0, 23.0, lambda: self.show_add_food_page("breakfast")),
            ("AddF_Lunch.png", 372.0, 145.0, 110.0, 23.0, lambda: self.show_add_food_page("lunch")),
            ("AddF_Dinner.png", 663.0, 145.0, 110.0, 23.0, lambda: self.show_add_food_page("dinner")),
            ("Back.png", 14.0, 18.0, 59.0, 35.0, lambda: self.controller.show_page("AppPage1", self.user_key)),
            ("Add_Snack.png", 700.0, 380.0, 118.0, 15.0, lambda: self.show_add_food_page("snacks"))
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img = PhotoImage(file=self.relative_to_assets(image_name))
            if command:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command,
                                bg="#DAE6E4")
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                canvas.create_image(x, y, image=img, anchor='nw')
            self.images.append(img)

        font_large = Font(family="Consolas", slant="italic", size=20)
        font_medium = Font(family="Consolas", slant="italic", size=14)

        self.breakfast_listbox = self.create_listbox(master, 60, 170, 240, 120)
        self.lunch_listbox = self.create_listbox(master, 350, 170, 240, 120)
        self.dinner_listbox = self.create_listbox(master, 640, 170, 240, 120)
        self.snack_listbox = self.create_listbox(master, 350, 380, 240, 70)

        Label(self, text="Welcome, ", font=font_large, bg="#DAE6E4").place(x=80, y=33)
        Label(self, text="Log Food", font=font_medium, bg="#DAE6E4").place(x=171, y=255)
        Label(self, text="Today's Activity", font=font_medium, bg="#DAE6E4").place(x=398, y=255)
        Label(self, text="Goals", font=font_medium, bg="#DAE6E4").place(x=715, y=255)

    def create_listbox(self, master, x, y, width, height):
        frame_bg = "#FFFCF1"
        listbox_bg = "#FFFCF1"
        listbox_fg = "#000000"
        listbox_font = ("Consolas", 12)
        frame = Frame(master, bg=frame_bg, bd=2, relief="ridge")
        frame.place(x=x, y=y, width=width, height=height)
        listbox = Listbox(frame, width=23, height=5, bg=listbox_bg, fg=listbox_fg, font=listbox_font, bd=0,
                          highlightthickness=0, relief="flat")
        listbox.pack(pady=5)
        return listbox

    def restore_meals(self):
        for meal_type, listbox in [("breakfast", self.breakfast_listbox), ("lunch", self.lunch_listbox),
                                   ("dinner", self.dinner_listbox), ("snacks", self.snack_listbox)]:
            self.load_meal(meal_type, listbox)

    def load_meal(self, meal_type, listbox):
        listbox.delete(0, END)
        user_ref = db.collection('users').document(self.user_key).collection('meals').document(meal_type).collection(
            'items')
        meals = user_ref.stream()
        for meal in meals:
            food = meal.to_dict()
            listbox.insert(END, f"{food['description']} - {food['calories']} kcal")

    def show_add_food_page(self, meal_type):
        # Ensure the meal document exists before showing the AddFoodPage
        try:
            user_ref = db.collection('users').document(self.user_key)
            meal_ref = user_ref.collection('meals').document(meal_type)

            if not meal_ref.get().exists:
                meal_ref.set({})  # Create the meal document if it does not exist

            self.controller.add_page("AddFoodPage", AddFoodPage, self.user_key, meal_type)
            self.controller.show_page("AddFoodPage", self.user_key, meal_type)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create meal collection: {e}")

    def update(self, user_key):
        self.user_key = user_key
        self.restore_meals()

    def relative_to_assets(self, path: str) -> str:
        return str(Path(__file__).parent.parent / 'assets' / 'frame8' / path)
