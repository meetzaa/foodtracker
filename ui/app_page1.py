from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from utils.utils import get_user_details_by_user_key
import concurrent.futures
from pathlib import Path

executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

# Define the paths for the assets
OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame6"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class AppPage1(BasePage):
    def __init__(self, master, controller, user_key=""):
        super().__init__(master, controller)
        self.user_key = user_key
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#DAE6E4")
        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("Profile.png", 25.0, 25.0, 43.0, 45.0, lambda: self.controller.show_page("ProfilePage", self.user_key)),
            ("LogFood.png", 125.0, 102.0, 185.0, 160.0, lambda: self.controller.show_page("LogFoodPage", self.user_key)),
            ("TodayActivity.png", 381.0, 102.0, 198.0, 154.0, lambda: self.controller.show_page("TodayActivityPage", self.user_key)),
            ("Goals.png", 640.0, 102.0, 198.0, 154.0, lambda: self.controller.show_page("GoalPage", self.user_key)),
            ("SeeMore.png", 759.0, 369.0, 206.0, 69.0, lambda: self.controller.show_page("SeeMorePage", self.user_key)),
            ("Calories.png", 531.0, 341.0, 100.0, 33.0, lambda: self.placeholder_function("Calories")),
            ("BMI.png", 531.0, 382.0, 100.0, 33.0, lambda: self.placeholder_function("BMI")),
            ("Macros.png", 531.0, 423.0, 100.0, 33.0, lambda: self.placeholder_function("Macros")),
            ("image_1.png", 313.0, 396.0, None, None, None)
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img_path = relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            self.images.append(img)

            if command:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                canvas.create_image(x, y, image=img, anchor='nw')

        font_large = Font(family="Consolas", slant="italic", size=20)
        font_medium = Font(family="Consolas", slant="italic", size=14)

        self.welcome_label = Label(self, text="Welcome, ", font=font_large, bg="#DAE6E4")
        self.welcome_label.place(x=80, y=33)
        Label(self, text="Log Food", font=font_medium, bg="#DAE6E4").place(x=171, y=255)
        Label(self, text="Today's Activity", font=font_medium, bg="#DAE6E4").place(x=398, y=255)
        Label(self, text="Goals", font=font_medium, bg="#DAE6E4").place(x=715, y=255)

    def placeholder_function(self, button_name):
        print(f"{button_name} button pressed. Functionality under construction.")

    def update(self, user_key):
        self.user_key = user_key
        executor.submit(self._fetch_user_details)

    def _fetch_user_details(self):
        user_details = get_user_details_by_user_key(self.user_key)
        self._update_ui_with_user_details(user_details)

    def _update_ui_with_user_details(self, user_details):
        if not user_details:
            print(f"No user details found for key {self.user_key}")
            return

        username = user_details.get('Utilizator', 'User')
        self.welcome_label.config(text=f"Welcome, {username}")
