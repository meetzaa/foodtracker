from tkinter import *
from tkinter.font import Font
from pathlib import Path
from gui_common import setup_loading_page


def show_loading_page(master):
    for widget in master.winfo_children():
        widget.destroy()

    setup_loading_page(master)


def setup_ready_page(master):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets/frame5"

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    master.configure(bg="#DAE6E4")

    canvas = Canvas(
        master,
        bg="#DAE6E4",
        height=503,
        width=937,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    master.images = []

    image_details = [
        ("image_1.png", 200.0, 10.0),
        ("image_2.png", 590.0, 70.0),
        ("LetsDoIt.png", 360.0, 415.0)
    ]

    for image_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame5"))
        if "LetsDoIt.png" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.place(x=x, y=y, width=230.0, height=38.0)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')
            master.images.append(img)

    font_large = Font(family="Consolas", slant="italic", size=32, weight="bold")
    font_medium = Font(family="Consolas", slant="italic", size=24)

    canvas.create_text(270, 170, text="You're all set!", font=font_large, fill="black")
    canvas.create_text(460, 232, text="Let’s dive into your eating habits", font=font_medium, fill="black")
    canvas.create_text(610, 268, text="and start optimizing now!", font=font_medium, fill="black")


