from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from pathlib import Path

def relative_to_assets(path: str) -> Path:
    OUTPUT_PATH = Path(__file__).resolve().parent.parent
    return OUTPUT_PATH / "assets" / path

class GoalInfoPage(BasePage):
    def __init__(self, master, controller, user_key=None, goal=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.current_goal = goal  # Salvează obiectivul selectat
        self.goal_info_texts = {
            "Weight Loss": {
                "kcal": "1200 to 1500 kcal",
                "fats": "~0.3 to 0.5 grams per kg of fats",
                "protein": "1.0/1.2 grams of protein per kg of body weight",
                "carbs": "50 to 100 grams of carbohydrates",
                "reminder": "Increase your water intake to aid in fat loss!"
            },
            "Muscle Build": {
                "kcal": "2500 to 3000 kcal",
                "fats": "0.8 to 1 grams per kg of fats",
                "protein": "2.0/2.5 grams of protein per kg of body weight",
                "carbs": "300 to 350 grams of carbohydrates",
                "reminder": "Protein is crucial for muscle repair and growth!"
            },
            "Maintenance": {
                "kcal": "2000 to 2500 kcal",
                "fats": "0.6 to 0.8 grams per kg of fats",
                "protein": "1.5/2.0 grams of protein per kg of body weight",
                "carbs": "150 to 200 grams of carbohydrates",
                "reminder": "Maintaining balance is key to long-term health!"
            }
        }
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#DAE6E4")

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("frame11/PlanReady.png", 646.0, 433.0, 265.0, 39.0, lambda: self.controller.show_final_page(self.user_key, self.current_goal)),
            ("frame11/image_1.png", 150.0, 154.0, None, None, None),
            ("frame11/image_2.png", 150.0, 190.0, None, None, None),
            ("frame11/image_3.png", 150.0, 226.0, None, None, None),
            ("frame11/image_4.png", 150.0, 262.0, None, None, None),
            ("frame11/image_5.png", 170.0, 305.0, None, None, None)
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img_path = relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            self.images.append(img)

            if width and height:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                canvas.create_image(x, y, image=img, anchor='nw')

        font_large = Font(family="Consolas", size=19)
        font_medium = Font(family="Consolas", size=15)
        font_small = Font(family="Consolas", size=13)

        details = self.goal_info_texts.get(self.current_goal, {
            "kcal": "N/A",
            "fats": "N/A",
            "protein": "N/A",
            "carbs": "N/A",
            "reminder": "N/A"
        })


        Label(self, text="Based on your choice, you should eat approximately (per day):", font=font_large, bg="#DAE6E4").place(x=59, y=80)

        Label(self, text=f"Calories: {details['kcal']}", bg="#DAE6E4", font= font_medium).place(x=180, y=147)
        Label(self, text=f"Fats: {details['fats']}", bg="#DAE6E4", font= font_medium).place(x=180, y=183)
        Label(self, text=f"Protein: {details['protein']}", bg="#DAE6E4", font= font_medium).place(x=180, y=220)
        Label(self, text=f"Carbs: {details['carbs']}", bg="#DAE6E4", font= font_medium).place(x=180, y=256)
        Label(self, text=f"Reminder: {details['reminder']}", bg="#FFFCF1", font= font_small).place(x=240, y=360)

    def update(self, user_key, goal=None):
        self.user_key = user_key
        if goal:
            self.current_goal = goal
        self.create_widgets()