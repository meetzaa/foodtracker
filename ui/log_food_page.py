from tkinter import Canvas, Label, Button, PhotoImage, Listbox, END, Frame
from tkinter.font import Font
from .base_page import BasePage
from logic.meal_manager import MealManager  # Ensure this is the correct import path
from pathlib import Path
from .add_food_popup import AddFoodPopup
from utils.utils import get_user_document_by_key  # Assuming this fetches data from Firebase

OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame8"

def relative_to_assets(path: str) -> Path:
    return OUTPUT_PATH / "assets" / path

class LogFoodPage(BasePage):
    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.create_widgets()
        self.restore_meals()  # Load meals during initialization

    def create_widgets(self):
        self.configure(bg="#DAE6E4")

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("frame8/image_1.png", 30.0, 70.0, None, None, None),
            ("frame8/image_2.png", 321.0, 70.0, None, None, None),
            ("frame8/image_3.png", 612.0, 70.0, None, None, None),
            ("frame8/image_4.png", 184.0, 329.0, None, None, None),
            ("frame8/AddF_Breakfast.png", 79.0, 145.0, 110.0, 23.0, lambda: self.open_food_popup("breakfast")),
            ("frame8/AddF_Lunch.png", 372.0, 145.0, 110.0, 23.0, lambda: self.open_food_popup("lunch")),
            ("frame8/AddF_Dinner.png", 663.0, 145.0, 110.0, 23.0, lambda: self.open_food_popup("dinner")),
            ("frame8/Back.png", 14.0, 18.0, 59.0, 35.0, lambda: self.controller.show_page("AppPage1", self.user_key)),
            ("frame8/Add_Snack.png", 700.0, 380.0, 118.0, 15.0, lambda: self.open_food_popup("snacks"))
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img_path = relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            self.images.append(img)
            if command:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command, bg="#DAE6E4")
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                canvas.create_image(x, y, image=img, anchor='nw')

        font_large = Font(family="Consolas", slant="italic", size=20)
        font_medium = Font(family="Consolas", slant="italic", size=14)

        self.breakfast_listbox = self.create_listbox(self, 60, 170, 240, 120)
        self.lunch_listbox = self.create_listbox(self, 350, 170, 240, 120)
        self.dinner_listbox = self.create_listbox(self, 640, 170, 240, 120)
        self.snack_listbox = self.create_listbox(self, 350, 380, 240, 70)


    def open_food_popup(self, meal_type):
        popup = AddFoodPopup(self, user_key=self.user_key, selected_meal=meal_type)
        popup.grab_set()

    def create_listbox(self, master, x, y, width, height):
        frame_bg = "#FFFCF1"
        listbox_bg = "#FFFCF1"
        listbox_fg = "#000000"
        listbox_font = ("Consolas", 12)
        frame = Frame(master, bg=frame_bg, bd=2, relief="ridge")
        frame.place(x=x, y=y, width=width, height=height)
        listbox = Listbox(frame, width=23, height=5, bg=listbox_bg, fg=listbox_fg, font=listbox_font, bd=0, highlightthickness=0, relief="flat")
        listbox.pack(pady=5)
        return listbox

    def restore_meals(self):
        user_doc_id, user_data = get_user_document_by_key(self.user_key)
        if not user_data:
            print(f"No user data found for key {self.user_key}")
            return

        meal_data = {
            "breakfast": user_data.get("breakfast", []),
            "lunch": user_data.get("lunch", []),
            "dinner": user_data.get("dinner", []),
            "snacks": user_data.get("snacks", [])
        }

        self.breakfast_listbox.delete(0, END)
        self.lunch_listbox.delete(0, END)
        self.dinner_listbox.delete(0, END)
        self.snack_listbox.delete(0, END)

        for meal_type, listbox in [("breakfast", self.breakfast_listbox), ("lunch", self.lunch_listbox), ("dinner", self.dinner_listbox), ("snacks", self.snack_listbox)]:
            foods = meal_data[meal_type]
            if not foods:
                print(f"No foods found for meal type: {meal_type}")
            else:
                for food in foods:
                    listbox.insert(END, f"{food['name']} - {food['calories']} kcal")

    def get_listbox_by_meal_type(self, meal_type):
        if meal_type == "breakfast":
            return self.breakfast_listbox
        elif meal_type == "lunch":
            return self.lunch_listbox
        elif meal_type == "dinner":
            return self.dinner_listbox
        elif meal_type == "snacks":
            return self.snack_listbox

    def update(self, user_key):
        self.user_key = user_key
        self.restore_meals()
