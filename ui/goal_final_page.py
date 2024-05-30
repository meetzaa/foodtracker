from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from pathlib import Path

# Define the paths for the assets
OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame12"

def relative_to_assets(path: str) -> Path:
    return OUTPUT_PATH / "assets" / path

class GoalFinalPage(BasePage):
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
            ("frame12/Back.png", 14.0, 18.0, 63.0, 41.0, lambda: self.controller.show_page("AppPage1", self.user_key)),
            ("frame12/image_1.png", 70.0, 70.0, None, None, None),
            ("frame12/image_2.png", 70.0, 280.0, None, None, None),
            ("frame12/image_3.png", 500.0, 280.0, None, None, None),
            ("frame12/image_4.png", 500.0, 70.0, None, None, None)
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

        font_m = Font(family="Consolas", slant="italic", size=18)

        Label(self, text="You eat ", font=font_m, bg="#FFFCF1", fg="#515151").place(x=115, y=156)
        Label(self, text="You eat ", font=font_m, bg="#FFFCF1", fg="#515151").place(x=580, y=156)
        Label(self, text="You eat ", font=font_m, bg="#FFFCF1", fg="#515151").place(x=140, y=369)
        Label(self, text="You eat ", font=font_m, bg="#FFFCF1", fg="#515151").place(x=580, y=369)

    def update(self, user_key):
        self.user_key = user_key
