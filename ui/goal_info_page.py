from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from pathlib import Path

# Define the paths for the assets
OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame11"

def relative_to_assets(path: str) -> Path:
    return OUTPUT_PATH / "assets" / path

class GoalInfoPage(BasePage):
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
            ("frame11/PlanReady.png", 646.0, 433.0, 265.0, 39.0, lambda: self.controller.show_page("GoalFinalPage", self.user_key)),
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

        font_large = Font(family="Consolas", slant="italic", size=19)

        Label(self, text="Based on your choice, you should eat aproximatively(per day): ", font=font_large,
              bg="#DAE6E4").place(x=59, y=80)

    def update(self, user_key):
        self.user_key = user_key
