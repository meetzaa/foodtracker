from tkinter import *
from tkinter.font import Font
from pathlib import Path
from gui_common import show_loading_page, show_signup, setup_signup_page, setup_loading_page


def show_signup(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_signup_page(master)


def show_loading_page(master):
    for widget in master.winfo_children():
        widget.destroy()

    setup_loading_page(master)


def setup_gravity_check_page(master):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets/frame3"

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
        ("image_1.png", 750.0, 95.0),
        ("image_2.png", 187.0, 267.0),
        ("image_3.png", 184.0, 227.0),
        ("image_4.png", 478.0, 266.0),
        ("image_5.png", 479.0, 227.0),
        ("image_6.png", 772.0, 266.0),
        ("entry_1.png", 176.0, 293.0),
        ("entry_2.png", 471.0, 293.0),
        ("entry_3.png", 772.0, 293.0),
        ("button_1.png", 750.0, 405.0),
        ("button_2.png", 80.0, 405.0),
        ("image_7.png", 890.0, 418.0),
        ("image_8.png", 65.0, 414.0)
    ]

    for image_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(image_name))
        if "button" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            if "button_1.png" == image_name:  # button_1 este butonul de "Next Step"
                button.config(command=lambda m=master: show_loading_page(m), bg="#DAE6E4")
                button.place(x=x, y=y, width=300.0, height=43.0)
            elif "button_2.png" == image_name:  # button_2 este butonul de "Go Back"
                button.config(command=lambda m=master: show_signup(m))
                button.place(x=x, y=y, width=62.0, height=20.0)
        else:
            canvas.create_image(x, y, image=img)
        master.images.append(img)

    font_large = Font(family="Consolas", slant="italic", size=32)
    font_medium = Font(family="Consolas", slant="italic", size=18)
    font_small = Font(family="Consolas", slant="italic", size=16)

    entry_kg = Entry(master, bd=0, bg="#F9F8F8", fg="#000716", highlightthickness=0)
    entry_kg.place(x=155.0, y=283.0, width=40.0, height=25.0)

    entry_cm = Entry(master, bd=0, bg="#F9F8F8", fg="#000716", highlightthickness=0)
    entry_cm.place(x=454.0, y=283.0, width=40.0, height=25.0)

    entry_age = Entry(master, bd=0, bg="#F9F8F8", fg="#000716", highlightthickness=0)
    entry_age.place(x=750.0, y=283.0, width=40.0, height=25.0)

    Label(master, text="Gravity Check!", font=font_large, bg="#DAE6E4").place(x=111, y=50)
    Label(master, text="Enter your details to keep your food in flight!", font=font_small, bg="#DAE6E4").place(x=111,
                                                                                                               y=115)
    Label(master, text="kg", font=font_small, bg="#FFFCF1").place(x=218, y=278)
    Label(master, text="cm", font=font_small, bg="#FFFCF1").place(x=511, y=278)
    Label(master, text="Age", font=font_medium, bg="#FFFCF1").place(x=750, y=225)