from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from pathlib import Path

# Define the paths for the assets
OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame14"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class SettingsPage(BasePage):
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
            ("Back.png", 14.0, 18.0, 59.0, 37.0, lambda: self.controller.show_page("SeeMorePage", self.user_key)),
            ("Edit_profile.png", 333.0, 161.0, 284.0, 47.0, lambda: self.controller.show_page("ProfilePage", self.user_key)),
            ("Change_goal.png", 342.0, 223.0, 275.0, 40.0, lambda: self.controller.show_page("GoalPage", self.user_key)),
            ("Info_goal.png", 299.0, 274.0, 359.0, 34.0, lambda: self.controller.show_page("GoalInfoPage", self.user_key)),
            ("App_details.png", 338.0, 328.0, 285.0, 43.0, lambda: self.controller.show_page("AppPage1", self.user_key)),
            ("SignOut.png", 340.0, 381.0, 277.0, 43.0, lambda: self.controller.show_page("LoginPage")),
            ("image_1.png", 225.0, 120.0),
            ("image_2.png", 350.0, 43.0),
            ("image_3.png", 918.0, 78.0),
            ("image_4.png", 773.0, 210.0),
            ("image_5.png", 872.0, 354.0),
            ("image_6.png", 795.0, 60.0),
            ("image_7.png", 726.0, 436.0),
            ("image_8.png", 630.0, 125.0),
            ("image_9.png", 215.0, -15.0),
            ("image_10.png", 388.0, 503.0),
            ("image_11.png", -20.0, 100.0),
            ("image_12.png", 239.0, 105.0),
            ("image_13.png", 100.0, 240.0),
            ("image_14.png", 81.0, 429.0)
        ]

        for details in image_details:
            image_name, x, y, *args = details
            img_path = relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            self.images.append(img)

            if len(args) == 3:
                width, height, command = args
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief='flat', command=command)
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                canvas.create_image(x, y, image=img, anchor='nw')

        font_large = Font(family="Consolas", slant="italic", size=32)
        Label(self, text="Settings", font=font_large, bg="#DAE6E4").place(x=413, y=42)

    def update(self, user_key=None):
        self.user_key = user_key or self.user_key
