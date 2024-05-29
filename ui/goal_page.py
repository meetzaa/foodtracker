from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from pathlib import Path

# Define the paths for the assets
OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame10"

def relative_to_assets(path: str) -> Path:
    return OUTPUT_PATH / "assets" / path

class GoalPage(BasePage):
    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#DAE6E4")

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("frame10/Weight_Loss.png", 289.0, 193.0, 350.0, 81.0, lambda: self.controller.show_page("GoalInfoPage", self.user_key)),
            ("frame10/Muscle_Build.png", 289.0, 283.0, 350.0, 81.0, lambda: self.controller.show_page("GoalInfoPage", self.user_key)),
            ("frame10/Maintenance.png", 289.0, 373.0, 350.0, 81.0, lambda: self.controller.show_page("GoalInfoPage", self.user_key))
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img_path = relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            self.images.append(img)
            button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img

        font_large = Font(family="Consolas", slant="italic", size=26, weight="bold")
        font_medium = Font(family="Consolas", slant="italic", size=20)

        Label(self, text="Let’s set your goals!", font=font_large, bg="#DAE6E4", fg="#000000").place(x=267, y=49)
        Label(self, text="First thing first, what do you want to achieve?", font=font_medium, bg="#DAE6E4",
              fg="#000000").place(x=147, y=108)

    def update(self, user_key):
        self.user_key = user_key
