# ui/goal_info_page.py
from tkinter import Canvas, Label, Button, PhotoImage
from tkinter.font import Font
from .base_page import BasePage


class GoalInfoPage(BasePage):
    def __init__(self, master, controller, user_key=None):
        super().__init__(master, controller)
        self.configure(bg="#DAE6E4")

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("back.png", 22.0, 17.0, 42, 36, lambda: controller.show_page("SetGoalPage")),
            ("image_1.png", 313.0, 396.0, None, None, None),
            ("image_2.png", 313.0, 396.0, None, None, None),
            ("image_3.png", 313.0, 396.0, None, None, None),
            ("image_4.png", 313.0, 396.0, None, None, None)
        ]

        for details in image_details:
            image_name, x, y, width, height, command = details
            img = PhotoImage(file=f"assets/frame_goal_info/{image_name}")
            self.images.append(img)
            if command is not None:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
                button.place(x=x, y=y, width=width, height=height)
                button.image = img
            else:
                canvas.create_image(x, y, image=img, anchor='nw')

        font_large = Font(family="Consolas", slant="italic", size=26)
        font_medium = Font(family="Consolas", slant="italic", size=20)

        Label(self, text="Goal Information", font=font_large, bg="#DAE6E4").place(x=228, y=20)
        Label(self, text="Details about your selected goal will be shown here.", font=font_medium, bg="#DAE6E4").place(
            x=228, y=70)

    def update(self, user_key):
        self.user_key = user_key
        # Update the page with user-specific information if needed
