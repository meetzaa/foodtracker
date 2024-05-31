from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from utils.utils import get_user_document_by_key,get_user_physical_details_by_user_key
from pathlib import Path
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame9"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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
            img_path = relative_to_assets(image_name)
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

        font_large = Font(family="Consolas", slant="italic", size=18, underline=1)
        font_medium = Font(family="Consolas", slant="italic", size=12)

        Label(self, text="Today's Activity", font=font_large, bg="#FFFCF1").place(x=360, y=73)
        self.breakfast_label = Label(self, text="Breakfast Meal:", font=font_medium, bg="#FFFCF1")
        self.breakfast_label.place(x=284, y=146)
        self.lunch_label = Label(self, text="Lunch Meal:", font=font_medium, bg="#FFFCF1")
        self.lunch_label.place(x=284, y=214)
        self.dinner_label = Label(self, text="Dinner Meal:", font=font_medium, bg="#FFFCF1")
        self.dinner_label.place(x=284, y=282)
        self.snacks_label = Label(self, text="Snacks:", font=font_medium, bg="#FFFCF1")
        self.snacks_label.place(x=284, y=350)

        self.bmi_result_label = Label(self, text="", font=font_medium, bg="#FFFCF1")
        self.bmi_result_label.place(x=324, y=418)

        self.calories_label = Label(self, text="", font=font_medium, bg="#FFFCF1")
        self.calories_label.place(x=324, y=486)

    def update(self, user_key):
        self.user_key = user_key
        self.fetch_and_display_meal_data()

    def fetch_and_display_meal_data(self):
        user_doc_id, user_data = get_user_document_by_key(self.user_key)
        if not user_data:
            print(f"No user data found for key {self.user_key}")
            self._update_labels("No data available", "No data available")
            return

        breakfast_calories = sum(food['calories'] for food in user_data.get('breakfast', []))
        lunch_calories = sum(food['calories'] for food in user_data.get('lunch', []))
        dinner_calories = sum(food['calories'] for food in user_data.get('dinner', []))
        snacks_calories = sum(food['calories'] for food in user_data.get('snacks', []))

        self.breakfast_label.config(text=f"Breakfast Meal: Total Calories: {breakfast_calories:.2f} kcal")
        self.lunch_label.config(text=f"Lunch Meal: Total Calories: {lunch_calories:.2f} kcal")
        self.dinner_label.config(text=f"Dinner Meal: Total Calories: {dinner_calories:.2f} kcal")
        self.snacks_label.config(text=f"Snacks: Total Calories: {snacks_calories:.2f} kcal")
    def _fetch_and_display_total_calories(self):
        user_doc_id, user_data = get_user_document_by_key(self.user_key)
        if not user_data:
            print(f"No user data found for key {self.user_key}")
            self._update_calories_label("No data available")
            return

        total_calories = sum(
            food['calories'] for meal in ['breakfast', 'lunch', 'dinner', 'snacks'] for food in user_data.get(meal, [])
        )
        self._update_calories_label(f"Total Calories: {total_calories:.2f} kcal")

    def _update_calories_label(self, text):
        self.calories_label.config(text=text)

    def _clear_labels(self):
        self.bmi_result_label.config(text="")
        self.calories_label.config(text="")
