from tkinter import *
from tkinter.font import Font
from pathlib import Path
from gui_common import setup_gravity_check_page
from tkinter import ttk


def show_gravity_check_page(master):
    for widget in master.winfo_children():
        widget.destroy()

    setup_gravity_check_page(master)


def setup_loading_page(master):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets/frame4"

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
        ("image_1.png", 510.0, 42.0),
        ("image_2.png", 330.0, 0.0),
        ("image_3.png", 115.0, 290.0)
    ]

    for image_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(image_name))
        canvas.create_image(x, y, image=img, anchor='nw')
        master.images.append(img)

    font_large = Font(family="Consolas", slant="italic", size=19)
    font_medium = Font(family="Consolas", slant="italic", size=13)
    font_medium_bold = Font(family="Consolas", slant="italic", weight="bold", underline=1, size=13)

    Label(master, text="Now let’s calculate your BMI! It will take just a few seconds!", font=font_large,
          bg="#DAE6E4").place(x=50, y=187)
    Label(master, text="Body Mass Index", font=font_medium_bold, bg="#DAE6E4").place(x=534, y=73)
    Label(master, text="is a person’s weight in ", font=font_medium, bg="#DAE6E4").place(x=676, y=73)
    Label(master, text="kilograms divided by the square of height ", font=font_medium, bg="#DAE6E4").place(x=534, y=96)
    Label(master, text="in meters. A high BMI can indicate high", font=font_medium, bg="#DAE6E4").place(x=534, y=119)
    Label(master, text="body fatness.", font=font_medium, bg="#DAE6E4").place(x=534, y=142)

    # Stilizarea barei de progres
    style = ttk.Style(master)
    style.theme_use('clam')
    style.configure("new.Horizontal.TProgressbar", troughcolor='#FFFFFF', background='#72918C', bordercolor='#FFFFFF',
                    lightcolor='#FFFFFF', darkcolor='#FFFFFF', borderwidth=0)

    progress = ttk.Progressbar(master, style="new.Horizontal.TProgressbar", orient="horizontal", length=732,
                               mode="determinate")
    progress.place(x=115.5, y=295.5, height=26)

    progress['value'] = 0
    master.update_idletasks()

    import time
    for i in range(100):
        time.sleep(0.05)
        progress['value'] += 1
        master.update_idletasks()
        # if progress['value'] >= 100:
        #     show_new_page(master)
        #     break


