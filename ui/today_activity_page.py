from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from pathlib import Path
from .base_page import BasePage
from logic.meal_manager import MealManager

class TodayActivityPage(BasePage):
    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.controller = controller
        self.configure(bg="#DAE6E4")
        self.images = []
        self.create_widgets()

    def create_widgets(self):
        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        image_details = [
            ("Back.png", 14.0, 18.0, 59.0, 38.0, lambda: self.controller.show_page("AppPage1", self.user_key)),
            ("image_1.png", 464.0, 257.0, None, None, None),
            ("image_2.png", 468.0, 176.99999999999994, None, None, None),
            ("image_3.png", 468.0, 244.99999999999994, None, None, None),
            ("image_4.png", 467.0, 312.9999999999999, None, None, None),
            ("image_5.png", 468.0, 380.9999999999999, None, None, None)
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img_path = self.relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            self.images.append(img)
            if command is not None:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                if width is not None and height is not None:
                    canvas.create_image(x, y, image=img, anchor='nw')
                else:
                    canvas.create_image(x, y, image=img)

        font_large = Font(family="Consolas", slant="italic", size=20, underline=1)
        font_medium = Font(family="Consolas", slant="italic", size=16)

        Label(self, text="Today's Activity", font=font_large, bg="#FFFCF1").place(x=360, y=73)
        Label(self, text="Breakfast Meal:", font=font_medium, bg="#FFFCF1").place(x=324, y=146)
        Label(self, text="Lunch Meal:", font=font_medium, bg="#FFFCF1").place(x=324, y=214)
        Label(self, text="Dinner Meal:", font=font_medium, bg="#FFFCF1").place(x=324, y=282)
        Label(self, text="Water:", font=font_medium, bg="#FFFCF1").place(x=324, y=350)

        meal_manager = MealManager(self.user_key)

        breakfast_foods, breakfast_calories = meal_manager.get_meal('breakfast')
        lunch_foods, lunch_calories = meal_manager.get_meal('lunch')
        dinner_foods, dinner_calories = meal_manager.get_meal('dinner')
        snack_foods, snack_calories = meal_manager.get_meal('snacks')

        Label(self, text=f"Total Calories: {breakfast_calories:.2f} kcal", font=font_medium, bg="#FFFCF1").place(x=324, y=176)
        Label(self, text=f"Total Calories: {lunch_calories:.2f} kcal", font=font_medium, bg="#FFFCF1").place(x=324, y=244)
        Label(self, text=f"Total Calories: {dinner_calories:.2f} kcal", font=font_medium, bg="#FFFCF1").place(x=324, y=312)
        Label(self, text=f"Total Calories: {snack_calories:.2f} kcal", font=font_medium, bg="#FFFCF1").place(x=324, y=380)

    def update(self, user_key):
        self.user_key = user_key
        # Add any necessary logic to update the page with new data

    def relative_to_assets(self, path: str) -> str:
        base_path = Path(__file__).resolve().parent.parent
        full_path = base_path / 'assets' / 'frame9' / path
        return str(full_path)
