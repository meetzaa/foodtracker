from tkinter import Label, Entry, Button, Canvas, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from utils.utils import get_user_details_by_user_key, update_user_details
import concurrent.futures
from pathlib import Path

executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame13"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class ProfilePage(BasePage):
    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.user_key = user_key
        self.configure(bg="#DAE6E4")

        self.entry_bg_color = "#FFFCF1"

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("Back.png", 14.0, 18.0, 55.0, 36.0, lambda: controller.show_page("AppPage1", self.user_key)),
            ("next.png", 738.0, 268.0, 32.0, 39.0, lambda: controller.show_page("Profile2Page", self.user_key)),
            ("image_1.png", 90.0, 35.0),
            ("image_2.png", 47.0, 65.0),
            ("image_3.png", 161.0, 459.0),
            ("image_4.png", 581.0, 42.0),
            ("image_5.png", 935.0, 354.0),
            ("image_6.png", 891.0, 300.0),
            ("image_7.png", 741.0, 82.0),
            ("image_8.png", 830.0, 5.0),
            ("image_9.png", 10.0, 354.0),
            ("image_10.png", 548.0, 491.0),
            ("image_11.png", 52.0, 180.0),
            ("image_12.png", 240.0, -75.0),
            ("image_13.png", 818.0, 429.0),
            ("image_14.png", 912.0, 85.0),
            ("image_15.png", 430.0, 50.0),
            ("image_16.png", 430.0, 50.0),
            ("image_17.png", 267.0, 243.0),
            ("image_18.png", 267.0, 312.0),
            ("image_19.png", 520.0, 312.0),
            ("image_20.png", 267.0, 381.0),
            ("image_21.png", 520.0, 381.0),
            ("image_22.png", 520.0, 243.0)
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

        font_large = Font(family="Consolas", slant="italic", size=20)
        font_medium = Font(family="Consolas", slant="italic", size=16)

        Label(self, text="Last Name", font=font_medium, bg=self.entry_bg_color).place(x=267, y=193)
        Label(self, text="First Name", font=font_medium, bg=self.entry_bg_color).place(x=267, y=262)
        Label(self, text="My Profile", font=font_large, bg=self.entry_bg_color).place(x=260, y=105)
        Label(self, text="Age", font=font_medium, bg=self.entry_bg_color).place(x=520, y=331)
        Label(self, text="Password", font=font_medium, bg=self.entry_bg_color).place(x=520, y=193)
        Label(self, text="Email", font=font_medium, bg=self.entry_bg_color).place(x=267, y=331)
        Label(self, text="Username", font=font_medium, bg=self.entry_bg_color).place(x=520, y=262)

        self.first_name_entry = Entry(self, bd=0, bg=self.entry_bg_color, fg="#000716", highlightthickness=0, state='readonly')
        self.first_name_entry.place(x=270, y=292, width=200.0, height=20.0)

        self.last_name_entry = Entry(self, bd=0, bg=self.entry_bg_color, fg="#000716", highlightthickness=0, state='readonly')
        self.last_name_entry.place(x=270, y=223, width=200.0, height=20.0)

        self.username_entry = Entry(self, bd=0, bg=self.entry_bg_color, fg="#000716", highlightthickness=0, state='readonly')
        self.username_entry.place(x=523, y=292, width=200.0, height=20.0)

        self.email_entry = Entry(self, bd=0, bg=self.entry_bg_color, fg="#000716", highlightthickness=0, state='readonly')
        self.email_entry.place(x=270, y=361, width=200.0, height=20.0)

        self.age_entry = Entry(self, bd=0, bg=self.entry_bg_color, fg="#000716", highlightthickness=0, state='readonly')
        self.age_entry.place(x=525, y=361, width=200.0, height=20.0)

        self.edit_button = Button(self, text="Edit", command=self.enable_editing, bg=self.entry_bg_color)
        self.edit_button.place(x=350, y=400, width=100, height=30)

        self.save_button = Button(self, text="Save", command=self.save_changes, bg=self.entry_bg_color)
        self.save_button.place(x=500, y=400, width=100, height=30)
        self.save_button.config(state='disabled')

    def enable_editing(self):
        self.first_name_entry.config(state='normal', bg=self.entry_bg_color)
        self.last_name_entry.config(state='normal', bg=self.entry_bg_color)
        self.username_entry.config(state='normal', bg=self.entry_bg_color)
        self.email_entry.config(state='normal', bg=self.entry_bg_color)
        self.age_entry.config(state='normal', bg=self.entry_bg_color)
        self.save_button.config(state='normal')

    def save_changes(self):
        user_details = {
            "Email": self.email_entry.get(),
            "Nume": self.last_name_entry.get(),
            "Prenume": self.first_name_entry.get(),
            "Utilizator": self.username_entry.get(),
            "details": {"Age": self.age_entry.get()}
        }
        update_user_details(self.user_key, user_details)
        self.disable_editing()

    def disable_editing(self):
        self.first_name_entry.config(state='readonly', bg=self.entry_bg_color)
        self.last_name_entry.config(state='readonly', bg=self.entry_bg_color)
        self.username_entry.config(state='readonly', bg=self.entry_bg_color)
        self.email_entry.config(state='readonly', bg=self.entry_bg_color)
        self.age_entry.config(state='readonly', bg=self.entry_bg_color)
        self.save_button.config(state='disabled')

    def update(self, user_key=None):
        self.user_key = user_key or self.user_key
        print(f"Updating ProfilePage with user_key: {self.user_key}")
        executor.submit(self._fetch_user_details)

    def _fetch_user_details(self):
        user_details = get_user_details_by_user_key(self.user_key)
        print(f"Fetched user details: {user_details}")  # Debug statement
        self._update_ui_with_user_details(user_details)

    def _update_ui_with_user_details(self, user_details):
        if not user_details:
            print(f"No user details found for key {self.user_key}")
            return

        self.first_name_entry.config(state='normal', bg=self.entry_bg_color)
        self.first_name_entry.delete(0, 'end')
        self.first_name_entry.insert(0, user_details.get('Prenume', ''))
        self.first_name_entry.config(state='readonly', bg=self.entry_bg_color)

        self.last_name_entry.config(state='normal', bg=self.entry_bg_color)
        self.last_name_entry.delete(0, 'end')
        self.last_name_entry.insert(0, user_details.get('Nume', ''))
        self.last_name_entry.config(state='readonly', bg=self.entry_bg_color)

        self.username_entry.config(state='normal', bg=self.entry_bg_color)
        self.username_entry.delete(0, 'end')
        self.username_entry.insert(0, user_details.get('Utilizator', ''))
        self.username_entry.config(state='readonly', bg=self.entry_bg_color)

        self.email_entry.config(state='normal', bg=self.entry_bg_color)
        self.email_entry.delete(0, 'end')
        self.email_entry.insert(0, user_details.get('Email', ''))
        self.email_entry.config(state='readonly', bg=self.entry_bg_color)

        self.age_entry.config(state='normal', bg=self.entry_bg_color)
        self.age_entry.delete(0, 'end')
        self.age_entry.insert(0, user_details.get('details', {}).get('Age', ''))
        self.age_entry.config(state='readonly', bg=self.entry_bg_color)
