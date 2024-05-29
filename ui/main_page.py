from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage
from pathlib import Path

# Define the paths for the assets
OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class MainPage(BasePage):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.images = []  # Initialize the images list here
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#FFFCF1")
        canvas = Canvas(self, bg="#FFFCF1", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Load and place images on the canvas
        image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(679.0, 365.0, image=image_image_1)
        self.images.append(image_image_1)  # Keep a reference

        image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(200.0, 251.0, image=image_image_2)
        self.images.append(image_image_2)  # Keep a reference

        JFont = Font(family="Consolas", slant="italic", size=17)
        JNFont = Font(family="Consolas", slant="italic", size=17, weight="bold")
        bigFont = Font(family="Consolas", slant="italic", underline=1, size=18)
        secondFont = Font(family="Consolas", slant="italic", underline=0)
        youFont = Font(family="Consolas", weight="bold", slant="italic")
        EatFont = Font(family="Consolas", size=17, slant="italic")

        labels = [
            ("Start your journey", JFont, 560, 340, "#FFFFFF"),
            ("NOW", JNFont, 640, 370, "#FFFFFF"),
            ("Who's counting?", bigFont, 435, 51, "#FFFCF1"),
            ("We are! So ", secondFont, 435, 91, "#FFFCF1"),
            ("you", youFont, 553, 91, "#FFFCF1"),
            ("don't have to!", secondFont, 593, 91, "#FFFCF1"),
            ("Eat", EatFont, 433, 119, "#FFFCF1")
        ]

        for text, font, x, y, bg in labels:
            Label(self, text=text, font=font, bg=bg).place(x=x, y=y)

        # Load button images and create buttons
        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_LogIn = Button(self, image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: self.controller.show_page("LoginPage"), relief="flat")
        button_LogIn.place(x=445.0, y=209.0, width=214.0, height=49.0)
        self.images.append(button_image_1)  # Keep a reference

        button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_SignUp = Button(self, image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: self.controller.show_page("SignupPage"), relief="flat")
        button_SignUp.place(x=695.0, y=210.0, width=214.0, height=49.0)
        self.images.append(button_image_2)  # Keep a reference

        text_label = Label(self, font=EatFont, bg="#FFFCF1", fg="#649089", text="")
        text_label.place(x=480, y=119)

        self.after(700, self.add_delete_text, ["Healthy", "Better", "Smart"], text_label, canvas)

    def add_delete_text(self, word_list, label, canvas, delay_ms=150, is_adding=True, index=0):
        if not word_list:
            return

        word = word_list[index] if index < len(word_list) else ""

        if is_adding:
            label_text = label.cget("text")
            if len(label_text) < len(word):
                label.config(text=word[:len(label_text) + 1])
                canvas.after(delay_ms, self.add_delete_text, word_list, label, canvas, delay_ms, True, index)
            else:
                next_index = (index + 1) % len(word_list)
                canvas.after(delay_ms, self.add_delete_text, word_list, label, canvas, delay_ms, False, next_index)
        else:
            if label.cget("text"):
                label.config(text=label.cget("text")[:-1])
                canvas.after(delay_ms, self.add_delete_text, word_list, label, canvas, delay_ms, False, index)
            else:
                canvas.after(delay_ms, self.add_delete_text, word_list, label, canvas, delay_ms, True, index)
