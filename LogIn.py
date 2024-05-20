from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from gui_common import show_gravity_check_page
from gui_common import setup_signup_page, show_signup,show_gravity_check_page,relative_to_assets,login
cred = credentials.Certificate('serviceAccountKey.json')
db = firestore.client()
from gui_common import login

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
                button.config(command=lambda: login(master, entry_Username.get(), entry_Password.get()))
                button.place(x=x, y=y, width=273.0, height=41.365234375)
        else:
            canvas.create_image(x, y, image=img)
        master.images.append(img)

    entry_Username = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_Username.place(x=294.0, y=177.0, width=349.0, height=43.0)

    entry_Password = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="***")
    entry_Password.place(x=294.0, y=300.0, width=349.0, height=43.0)

    TitluFont = Font(family="Consolas", slant="italic", size=26)
    TextFont = Font(family="Consolas", slant="italic", size=13)
    TextRFont = Font(family="Consolas", slant="italic", size=11)

    Label(master, text="Welcome back, gourmet guru!", font=TitluFont, bg="#DAE6E4").place(x=228, y=20)
    Label(master, text="Username", font=TextFont, bg="#FFFCF1").place(x=280, y=142)
    Label(master, text="Password", font=TextFont, bg="#FFFCF1").place(x=280, y=265)
    Label(master, text="Don't have an account?", font=TextRFont, bg="#FFFCF1", fg="#5E5858").place(x=335, y=455)