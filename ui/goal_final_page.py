from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from pathlib import Path
from utils.utils import get_user_physical_details_by_user_key


def relative_to_assets(path: str) -> Path:
    OUTPUT_PATH = Path(__file__).resolve().parent.parent
    return OUTPUT_PATH / "assets" / "frame12" / path


class GoalFinalPage(BasePage):
    def __init__(self, master, controller, user_key=None, nutrition_details=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.nutrition_details = nutrition_details or {
            "kcal": "N/A",
            "fats": "N/A",
            "protein": "N/A",
            "carbs": "N/A"
        }
        self.fats_multiplier = 0.5  # valoarea default pt weight loss
        self.protein_multiplier = 1.2  # valoarea default pt weight loss
        self.goal = None
        self.create_widgets()

    def find_weight_fats(self):
        physical_details = get_user_physical_details_by_user_key(self.user_key)
        if physical_details:
            weight = physical_details.get('Weight', 0)
            weight_result_fats = self.fats_multiplier * weight
            return weight_result_fats
        else:
            return "N/A"

    def find_weight_protein(self):
        physical_details = get_user_physical_details_by_user_key(self.user_key)
        if physical_details:
            weight = physical_details.get('Weight', 0)
            weight_result_protein = self.protein_multiplier * weight
            return weight_result_protein
        else:
            return "N/A"

    def create_widgets(self):
        self.configure(bg="#DAE6E4")
        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("Back.png", 14.0, 18.0, 63.0, 41.0, lambda: self.controller.show_page("AppPage1", self.user_key)),
            ("image_1.png", 70.0, 70.0),
            ("image_2.png", 70.0, 280.0),
            ("image_3.png", 500.0, 280.0),
            ("image_4.png", 500.0, 70.0)
        ]

        font_large = Font(family="Consolas", slant="italic", size=22)
        font_medium = Font(family="Consolas", slant="italic", size=18)

        for details in image_details:
            if len(details) == 6:  # Handles images with command
                image_name, x, y, width, height, command = details
            else:  # Handles static images without command
                image_name, x, y = details
                width, height, command = None, None, None

            img_path = relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            self.images.append(img)

            if command:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
                button.place(x=x, y=y, width=width, height=height)
                button.image = img  # Keep a reference to the image
            else:
                canvas.create_image(x, y, image=img, anchor='nw')

        # Use the result of find_weight_fats and find_weight_protein
        weight_result_fats = self.find_weight_fats()
        weight_result_protein = self.find_weight_protein()

        canvas.create_text(200.0, 115.0, anchor="nw", text=self.nutrition_details["kcal"], fill="#000000",
                           font=font_large)
        canvas.create_text(605.0, 115.0, anchor="nw", text=f"{weight_result_fats} g of fats", fill="#000000",
                           font=font_large)
        canvas.create_text(170.0, 329.0, anchor="nw", text=self.nutrition_details["carbs"] + " " + "of carbs ",
                           fill="#000000", font=font_large)
        canvas.create_text(578.0, 329.0, anchor="nw", text=f"{weight_result_protein} g of protein", fill="#000000",
                           font=font_large)

        # Labels displaying nutritional maximums
        Label(self, text="You ate      / " + self.nutrition_details["kcal"], font=font_medium, bg="#FFFCF1",
              fg="#515151").place(x=115, y=156)
        Label(self, text="You ate      / " + f"{weight_result_fats} g", font=font_medium, bg="#FFFCF1",
              fg="#515151").place(x=580, y=156)
        Label(self, text="You ate      / " + self.nutrition_details["carbs"], font=font_medium, bg="#FFFCF1",
              fg="#515151").place(x=140, y=369)
        Label(self, text="You ate      / " + f"{weight_result_protein} g", font=font_medium, bg="#FFFCF1",
              fg="#515151").place(x=580, y=369)

    def update(self, user_key, nutrition_details=None, goal=None):
        self.user_key = user_key
        if nutrition_details:
            self.nutrition_details = nutrition_details
        if goal:
            self.goal = goal
            if goal == "Weight Loss":
                self.fats_multiplier = 0.5
                self.protein_multiplier = 1.2
            elif goal == "Muscle Build":
                self.fats_multiplier = 1
                self.protein_multiplier = 2.5
            elif goal == "Maintenance":
                self.fats_multiplier = 0.8
                self.protein_multiplier = 2.0
        self.create_widgets()