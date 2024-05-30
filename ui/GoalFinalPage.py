from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from pathlib import Path

class GoalFinalPage(BasePage):
    goal_details = {
        "Weight Loss": {"kcal": "1500 kcal", "fats": "50g", "protein": "60g", "carbs": "100g"},
        "Muscle Build": {"kcal": "3000 kcal", "fats": "80g", "protein": "150g", "carbs": "350g"},
        "Maintenance": {"kcal": "2500 kcal", "fats": "70g", "protein": "120g", "carbs": "200g"}
    }

    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.configure(bg="#DAE6E4")
        self.images = []
        self.setup_ui()

    def relative_to_assets(self, path: str) -> str:
        base_path = Path(__file__).parent.parent
        return base_path / "assets/frame12" / Path(path)

    def setup_ui(self):
        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        image_details = [
            ("Back.png", 14.0, 18.0, 63.0, 41.0, lambda: self.controller.show_page("AppPage1", self.user_key)),
            ("image_1.png", 70.0, 70.0, None, None, None),
            ("image_2.png", 70.0, 280.0, None, None, None),
            ("image_3.png", 500.0, 280.0, None, None, None),
            ("image_4.png", 500.0, 70.0, None, None, None)
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img_path = self.relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            self.images.append(img)

            if width and height:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                canvas.create_image(x, y, image=img, anchor='nw')

        details = self.goal_details[self.controller.current_goal]

        canvas.create_text(200.0, 115.0, anchor="nw", text=details["kcal"], fill="#000000", font=("Consolas Italic", 22))
        canvas.create_text(630.0, 115.0, anchor="nw", text=details["fats"] + " of fat", fill="#000000", font=("Consolas Italic", 22))
        canvas.create_text(170.0, 329.0, anchor="nw", text=details["carbs"] + " of carbs", fill="#000000", font=("Consolas Italic", 22))
        canvas.create_text(593.0, 329.0, anchor="nw", text=details["protein"] + " of protein", fill="#000000", font=("Consolas Italic", 22))

        font_m = Font(family="Consolas", slant="italic", size=18)

        Label(self, text="You ate " "      / " + details["kcal"], font=font_m, bg="#FFFCF1", fg="#515151").place(x=115, y=156)
        Label(self, text="You ate " + "      / " + details["fats"], font=font_m, bg="#FFFCF1", fg="#515151").place(x=580, y=156)
        Label(self, text="You ate " + "      / " + details["carbs"], font=font_m, bg="#FFFCF1", fg="#515151").place(x=140, y=369)
        Label(self, text="You ate " + "      / " + details["protein"], font=font_m, bg="#FFFCF1", fg="#515151").place(x=580, y=369)
