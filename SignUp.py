import tkinter
from pathlib import Path
from tkinter import *
from tkinter.font import Font

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from gui_common import setup_login_page, show_login
import re
from tkinter import messagebox

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://foodtracker-8fe6b-default-rtdb.europe-west1.firebasedatabase.app/'
})
db = firestore.client()

def is_valid_email(email):
    # Definiți expresia regulată pentru validarea adresei de e-mail
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Verificați dacă adresa de e-mail respectă expresia regulată
    if re.match(regex, email):
        return True
    else:
        return False
def check_existing_user(username, email):
    # Interogare utilizator după nume de utilizator
    query_username = db.collection("users").where("Utilizator", "==", username).limit(1).get()
    # Interogare utilizator după adresă de e-mail
    query_email = db.collection("users").where("Email", "==", email).limit(1).get()

    return len(query_username) > 0 or len(query_email) > 0
def show_login(master):
    for widget in master.winfo_children():
        widget.destroy()

    setup_login_page(master)

    def check_existing_user(username):
        query = db.collection("users").where("username", "==", username).limit(1).get()
        return len(query) > 0
def setup_signup_page(master):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets/frame2"

    def relative_to_assets(path: str) -> str:
        return str(ASSETS_PATH / path)

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
        ("Log_In.png", 545.0, 441.0)
    ]

    def submit_button_pressed():
        first_name_value = first_name.get()
        last_name_value = last_name.get()
        username_value = username.get()
        email_value = mail.get()
        password_value = password.get()
        confirm_password_value = confirm_password.get()
        if confirm_password_value != password_value:
            messagebox.showerror("Eroare","Parolele nu coincid")
            return
        if check_existing_user(username_value, email_value):

            messagebox.showerror("Eroare","Un utilizator cu același nume  sau aceeași adresă de e-mail există deja!")
            return
        if not is_valid_email(email_value):
            messagebox.showerror("Eroare","Adresa de e-mail nu este într-un format corect")
            return
        user_data = {
            "Utilizator": username_value,
            "Nume": last_name_value,
            "Prenume": first_name_value,
            "Email": email_value,
            "Parola": password_value
        }
        assert isinstance(db, object)
        db.collection("users").add(user_data)
        messagebox.showinfo("Titlu", "Inregistrare cu succes!")

    for image_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(image_name))
        if "Submit.png" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            if "Submit.png" == image_name:
                button.config(command=lambda m=master: show_gravity_check_page(m))
                button.place(x=x, y=y, width=296.0, height=43.0)
        elif "Log_In.png" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            if "Log_In.png" == image_name:
                button.config(command=lambda m=master: show_login(m))
                button.place(x=x, y=y, width=62.0, height=20.0)
        else:
            canvas.create_image(x, y, image=img)
        master.images.append(img)

        # Fonturi
    Titlu1Font = Font(family="Consolas", slant="italic", size=20)
    Titlu2Font = Font(family="Consolas", slant="italic", size=20, weight="bold")
    InputFont = Font(family="Consolas", slant="italic", size=12)
    AccFont = Font(family="Consolas", slant="italic", size=11)

    entry_FName = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_FName.place(x=143.0, y=149.0, width=261.0, height=27.0)

    entry_User = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_User.place(x=546.0, y=149.0, width=261.0, height=27.0)

    entry_Pssw = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_Pssw.place(x=144.0, y=232.0, width=261.0, height=27.0)

    entry_CfPssw = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_CfPssw.place(x=546.0, y=232.0, width=261.0, height=27.0)

    entry_LName = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_LName.place(x=148.0, y=314.0, width=261.0, height=27.0)

    entry_Email = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_Email.place(x=546.0, y=314.0, width=261.0, height=27.0)

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

    return canvas
