from tkinter import *
from tkinter.font import Font
from pathlib import Path
from tkinter import ttk


def relative_to_assets(path: str, frame_directory: str) -> Path:
    """Returnează calea completă a unui asset relativ la directorul de assets specificat."""
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / frame_directory
    return ASSETS_PATH / Path(path)


# Definirea paginii de Log In
def setup_login_page(master):
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
        ("image_1.png", 467.0, 283.0),
        ("user.png", 468.5, 199.0),
        ("psswrd.png", 468.5, 323.0),
        ("LogIn.png", 337.0, 410.6),
        ("SignUp.png", 540.0, 458.0),
        ("image_2.png", 55.0, 457),
        ("image_3.png", 110.0, 338.0),
        ("image_4.png", 128.0, 411.0),
        ("image_5.png", 47.0, 371.0),
        ("image_6.png", 59.0, 322.0),
        ("image_7.png", 104.0, 254.0),
        ("image_8.png", 159.0, 299.0),
        ("image_9.png", 104.0, 319.0),
        ("image_10.png", 882.0, 445.0),
        ("image_11.png", 899.0, 347.4),
        ("image_12.png", 832.0, 375.0),
        ("image_13.png", 797.7, 316.0),
        ("image_14.png", 767.0, 375.0),
        ("image_15.png", 828.0, 265.0),
        ("image_16.png", 856.0, 306.0),
        ("image_17.png", 856.0, 409.0)
    ]

    for image_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame1"))
        if "SignUp.png" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            if "SignUp.png" == image_name:
                button.config(command=lambda: show_signup(master))
                button.place(x=x, y=y, width=71.0, height=19.0)
        elif "LogIn.png" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            if "LogIn.png" == image_name:
                # button.config(command=lambda m=master: show_login(m))
                button.place(x=x, y=y, width=273.0, height=41.365234375)
        else:
            canvas.create_image(x, y, image=img)
        master.images.append(img)

    entry_1 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_1.place(x=294.0, y=177.0, width=349.0, height=43.0)

    entry_2 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_2.place(x=294.0, y=300.0, width=349.0, height=43.0)

    TitluFont = Font(family="Consolas", slant="italic", size=26)
    TextFont = Font(family="Consolas", slant="italic", size=13)
    TextRFont = Font(family="Consolas", slant="italic", size=11)

    Label(master, text="Welcome back, gourmet guru!", font=TitluFont, bg="#DAE6E4").place(x=228, y=20)
    Label(master, text="Username", font=TextFont, bg="#FFFCF1").place(x=280, y=142)
    Label(master, text="Password", font=TextFont, bg="#FFFCF1").place(x=280, y=265)
    Label(master, text="Don't have an account?", font=TextRFont, bg="#FFFCF1", fg="#5E5858").place(x=335, y=455)


# Definrea paginii de Sign Up
def setup_signup_page(master):
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
        ("image_1.png", 469.0, 282.0),
        ("first_name.png", 273.5, 164.0),
        ("last_name.png", 676.5, 164.0),
        ("username.png", 274.0, 247.6),
        ("confirm_password.png", 676.5, 247.0),
        ("password.png", 275.0, 330),
        ("mail.png", 676.5, 330.0),
        ("Submit.png", 326.0, 392.0),
        ("Log_In.png", 550.0, 441.0)
    ]

    for image_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame2"))
        if "Submit.png" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            if "Submit.png" == image_name:
                button.config(command=lambda: show_gravity_check_page(master))
                button.place(x=x, y=y, width=296.0, height=43.0)
        elif "Log_In.png" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            if "Log_In.png" == image_name:
                button.config(command=lambda: show_login(master))
                button.place(x=x, y=y, width=62.0, height=20.0)
        else:
            canvas.create_image(x, y, image=img)
        master.images.append(img)

    Titlu1Font = Font(family="Consolas", slant="italic", size=20)
    Titlu2Font = Font(family="Consolas", slant="italic", size=20, weight="bold")
    InputFont = Font(family="Consolas", slant="italic", size=12)
    AccFont = Font(family="Consolas", slant="italic", size=11)

    entry_1 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_1.place(x=143.0, y=149.0, width=261.0, height=27.0)

    entry_2 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_2.place(x=546.0, y=149.0, width=261.0, height=27.0)

    entry_3 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_3.place(x=144.0, y=232.0, width=261.0, height=27.0)

    entry_4 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_4.place(x=546.0, y=232.0, width=261.0, height=27.0)

    entry_5 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_5.place(x=148.0, y=314.0, width=261.0, height=27.0)

    entry_6 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_6.place(x=546.0, y=314.0, width=261.0, height=27.0)

    Label(master, text="Bite-sized", font=Titlu1Font, bg="#DAE6E4").place(x=170, y=18)
    Label(master, text="sign-up", font=Titlu2Font, bg="#DAE6E4").place(x=330, y=18)
    Label(master, text="for your", font=Titlu1Font, bg="#DAE6E4").place(x=445, y=18)
    Label(master, text="mega appetite", font=Titlu2Font, bg="#DAE6E4").place(x=575, y=18)
    Label(master, text="!", font=Titlu1Font, bg="#DAE6E4").place(x=773, y=18)

    Label(master, text="First Name", font=InputFont, bg="#FFFCF1").place(x=137, y=117)
    Label(master, text="Username", font=InputFont, bg="#FFFCF1").place(x=539, y=117)
    Label(master, text="Password", font=InputFont, bg="#FFFCF1").place(x=539, y=200)
    Label(master, text="Confirm Password", font=InputFont, bg="#FFFCF1").place(x=539, y=283)
    Label(master, text="Last Name", font=InputFont, bg="#FFFCF1").place(x=137, y=200)
    Label(master, text="E-mail", font=InputFont, bg="#FFFCF1").place(x=137, y=283)

    Label(master, text="Already have an account?", font=AccFont, bg="#FFFCF1", fg="#5E5858").place(x=345, y=440)


def show_login(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_login_page(master)


def show_signup(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_signup_page(master)


# Definirea paginii pentru inputurile BMI-ului
def setup_gravity_check_page(master):
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
        ("entry_kg.png", 176.0, 293.0),
        ("entry_cm.png", 471.0, 293.0),
        ("entry_age.png", 772.0, 293.0),
        ("NextStep.png", 750.0, 405.0),
        ("GoBack.png", 80.0, 405.0),
        ("image_7.png", 890.0, 418.0),
        ("image_8.png", 65.0, 414.0)
    ]

    for image_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame3"))
        if "GoBack.png" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            if "GoBack.png" == image_name:
                button.config(command=lambda: show_signup(master))
                button.place(x=x, y=y, width=100.0, height=20.0)
        elif "NextStep.png" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            if "NextStep.png" == image_name:
                button.config(command=lambda: show_loading_page(master))
                button.place(x=x, y=y, width=120.0, height=30.0)
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


def show_gravity_check_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_gravity_check_page(master)


# Definirea paginii de Loading
def setup_loading_page(master):
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
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame4"))
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
        if progress['value'] >= 100:
            show_ready_page(master)
            break


def show_loading_page(master):
    for widget in master.winfo_children():
        widget.destroy()

    setup_loading_page(master)


# Definirea paginii de dupa loading
def setup_ready_page(master):
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


def show_ready_page(master):
    for widget in master.winfo_children():
        widget.destroy()

        setup_ready_page(master)