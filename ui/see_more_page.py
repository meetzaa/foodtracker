from tkinter import Canvas, Label, Button, Entry, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from pathlib import Path
from utils.utils import save_water_data, load_water_data, reset_water_data
import datetime

# Define the paths for the assets
OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame7"

def relative_to_assets(path: str) -> Path:
    return OUTPUT_PATH / "assets" / path

class SeeMorePage(BasePage):
    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.water_consumed = 0.0
        self.last_updated = datetime.date.today()
        self.create_widgets()
        self.load_water_data()
        self.check_new_day()

    def create_widgets(self):
        self.configure(bg="#DAE6E4")

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("frame7/Back.png", -50.0, 369.0, 203.0, 67.0, lambda: self.controller.show_page("AppPage1", self.user_key)),
            ("frame7/AddWater.png", 589.0, 74.0, 50.0, 40.0, self.add_water),
            ("frame7/RemoveWater.png", 398.0, 80.0, 50.0, 30.0, self.remove_water),
            ("frame7/MyProfile.png", 223.0, 298.0, 160.0, 131.0, lambda: self.controller.show_page("ProfilePage", self.user_key)),
            ("frame7/MyMeals.png", 432.0, 298.0, 160.0, 131.0, lambda: self.placeholder_function("MyMeals")),
            ("frame7/Settings.png", 642.0, 298.0, 160.0, 131.0, lambda: self.controller.show_page("SettingsPage", self.user_key)),
            ("frame7/image_1.png", 320.0, 10.0, None, None, None),
            ("frame7/image_2.png", 485.0, 39.0, None, None, None),
            ("frame7/image_3.png", 380.0, 215.0, None, None, None),
            ("frame7/entry_Water.png", 483.0, 136.5, 47.0, 30.0, None)
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img_path = relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            self.images.append(img)

            if width is None or height is None:
                width, height = 100, 100

            if command:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                canvas.create_image(x, y, image=img, anchor='nw')

        font_medium = Font(family="Consolas", slant="italic", size=15)

        Label(self, text="My Profile", font=font_medium, bg="#DAE6E4").place(x=250, y=428)
        Label(self, text="My Meals", font=font_medium, bg="#DAE6E4").place(x=473, y=428)
        Label(self, text="Settings", font=font_medium, bg="#DAE6E4").place(x=681, y=428)
        Label(self, text="Streak", font=font_medium, bg="#DAE6E4").place(x=92, y=21)
        Label(self, text="days", font=font_medium, bg="#DAE6E4").place(x=101, y=96)
        Label(self, text="Liters", font=font_medium, bg="#FFFCF1").place(x=572, y=144)

        self.liters_label = Label(self, text="0.0", font=font_medium, bg="#FFFCF1")
        self.liters_label.place(x=500, y=144)

        self.entry_Water = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_Water.place(x=500.0, y=145.0, width=53.0, height=22.5)

        self.liters_today_label = Label(self, text="0.0", font=font_medium, bg="#FFFCF1")
        self.liters_today_label.place(x=423, y=225)

    def placeholder_function(self, button_name):
        print(f"{button_name} button pressed. Functionality under construction.")

    def update(self, user_key):
        self.user_key = user_key
        self.load_water_data()

    def add_water(self):
        try:
            amount = float(self.entry_Water.get())
            self.water_consumed += amount
            save_water_data(self.user_key, self.water_consumed)
        except ValueError:
            print("Invalid input for water amount.")
        self.update_water_display()

    def remove_water(self):
        try:
            amount = float(self.entry_Water.get())
            self.water_consumed -= amount
            save_water_data(self.user_key, self.water_consumed)
        except ValueError:
            print("Invalid input for water amount.")
        self.update_water_display()

    def update_water_display(self):
        self.liters_label.config(text=f"{self.water_consumed:.1f}")
        self.liters_today_label.config(text=f"{self.water_consumed:.1f}")

    def load_water_data(self):
        self.water_consumed = load_water_data(self.user_key)
        self.update_water_display()

    def reset_water_data(self):
        self.water_consumed = 0.0
        save_water_data(self.user_key, self.water_consumed)
        self.update_water_display()

    def check_new_day(self):
        today = datetime.date.today()
        if today != self.last_updated:
            self.reset_water_data()
            self.last_updated = today
