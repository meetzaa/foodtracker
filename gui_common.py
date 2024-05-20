import uuid
import re
from pathlib import Path
import tkinter as tk
from tkinter import (
    Toplevel,font, Entry, Label, Button, Listbox, Scrollbar, END, Tk, Canvas, PhotoImage, messagebox, ttk
)
from tkinter.font import Font
import firebase_admin
from firebase_admin import credentials, firestore
import CaloriesCalc
from CaloriesCalc import daily_intake, calculate_calories
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://foodtracker-8fe6b-default-rtdb.europe-west1.firebasedatabase.app/'
})
db = firestore.client()
def generate_user_key():
    """
    Generate a unique key for a user.
    """
    return str(uuid.uuid4())

def save_user_details(master, weight, height, age, user_key):
    user_details_ref = db.collection("UserDetails").where("UserKey", "==", user_key)
    user_details = user_details_ref.get()

    for doc in user_details:
        user_details_data = doc.to_dict()
        user_details_data["Greutate"] = weight
        user_details_data["Înălțime"] = height
        user_details_data["Vârstă"] = age
        db.collection("UserDetails").document(doc.id).set(user_details_data)

        # Adăugați un print pentru a verifica dacă bucla este parcursă la fiecare iterație
        print("Date actualizate pentru documentul:", doc.id)

    messagebox.showinfo("Success", "Date actualizate cu succes!")
    show_login(master)

def login(master, username, password):
    # Interogare pentru a găsi utilizatorul cu numele specificat
    user_ref = db.collection("users").where(field_path="Utilizator", op_string="==", value=username).limit(1)

    user = user_ref.get()

    for doc in user:
        user_data = doc.to_dict()
        stored_password = user_data.get("Parola")

        if stored_password == password:
            messagebox.showinfo("Success", "Autentificare reușită!")
            show_app_page1(master)
            # Aici puteți adăuga logica suplimentară pentru acțiuni după autentificare
            return True
        else:
            messagebox.showerror("Eroare", "Nume de utilizator sau parolă incorecte.")
            return False

    messagebox.showerror("Eroare", "Nume de utilizator sau parolă incorecte.")
    return False

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
def relative_to_assets(path: str, frame_directory: str) -> Path:
    """Returnează calea completă a unui asset relativ la directorul de assets specificat."""
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / frame_directory
    return ASSETS_PATH / Path(path)

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
            messagebox.showerror("Eroare", "Parolele nu coincid")
            return
        if check_existing_user(username_value, email_value):
            messagebox.showerror("Eroare", "Un utilizator cu același nume  sau aceeași adresă de e-mail există deja!")
            return
        if not is_valid_email(email_value):
            messagebox.showerror("Eroare", "Adresa de e-mail nu este într-un format corect")
            return
        user_key = generate_user_key()
        user_data = {
            "Utilizator": username_value,
            "Nume": last_name_value,
            "Prenume": first_name_value,
            "Email": email_value,
            "Parola": password_value,
            "UserKey": user_key
        }
        db.collection("users").add(user_data)
        user_details_data = {
            "UserKey": user_key,
            "Greutate": None,
            "Înălțime": None,
            "Vârstă": None
        }
        db.collection("UserDetails").add(user_details_data)
        show_gravity_check_page(master,user_key)
    for image_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(image_name))
        if "Submit.png" == image_name:  # Modificați numele imaginii pentru butonul "Submit"
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            button.config(command=submit_button_pressed)  # Asociați funcția submit_button_pressed la butonul "Submit"
            button.place(x=x, y=y, width=296.0, height=43.0)
        elif "Log_in.png" == image_name:  # Modificați numele imaginii pentru butonul "Log in"
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img
            button.config(command=lambda m=master: show_login(m))
            button.place(x=12, y=440, width=62.0, height=20.0)
        else:
            canvas.create_image(x, y, image=img)
        master.images.append(img)

    # Fonturile pentru texte
    Titlu1Font = Font(family="Consolas", slant="italic", size=20)
    Titlu2Font = Font(family="Consolas", slant="italic", size=20, weight="bold")
    InputFont = Font(family="Consolas", slant="italic", size=12)
    AccFont = Font(family="Consolas", slant="italic", size=11)

    # Crearea și plasarea Entry-urilor
    first_name = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    first_name.place(x=143.0, y=149.0, width=261.0, height=27.0)

    username = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    username.place(x=546.0, y=149.0, width=261.0, height=27.0)

    last_name = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    last_name.place(x=144.0, y=232.0, width=261.0, height=27.0)

    mail = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    mail.place(x=144.0, y=314.0, width=261.0, height=27.0)  # Ajustarea poziției câmpului "mail"

    password = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,show="***")
    password.place(x=546.0, y=232.0, width=261.0, height=27.0)  # Ajustarea poziției câmpului "password"

    confirm_password = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,show="***")
    confirm_password.place(x=546.0, y=314.0, width=261.0, height=27.0)


    # Adăugarea textelor pe ecran
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
    Label(master, text="e-mail", font=InputFont, bg="#FFFCF1").place(x=137, y=283)

    Label(master, text="Already have an account?", font=AccFont, bg="#FFFCF1", fg="#5E5858").place(x=345, y=440)
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
def setup_gravity_check_page(master,user_key):
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
                button.config(command=lambda: show_login(master))
                button.place(x=x, y=y, width=100.0, height=20.0)
        elif "NextStep.png" in image_name:
                button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
                button.image = img
                if "NextStep.png" == image_name:
                    button.config(command=lambda: save_user_details(master, entry_kg.get(), entry_cm.get(), entry_age.get(),user_key))
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


# Definrea paginii de Sign Up

def show_login(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_login_page(master)


def show_signup(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_signup_page(master)


# Definirea paginii pentru inputurile BMI-ului


def show_gravity_check_page(master,user_key):
    for widget in master.winfo_children():
        widget.destroy()
    setup_gravity_check_page(master,user_key)


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



####PAGINA PRINCIPALA A APLICATIEI
def setup_app_page1(master):
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
        ("Profile.png", 25.0, 25.0, 43.0, 45.0, lambda: show_profile_page(master)),
        ("LogFood.png", 125.0, 102.0, 185.0, 160.0, lambda: show_LogFood_page(master)),
        ("TodayActivity.png", 381.0, 102.0, 198.0, 154.0, lambda: show_TodayActivity_page(master)),
        ("Goals.png", 640.0, 102.0, 198.0, 154.0, lambda: show_SetGoal_page(master)),
        ("SeeMore.png", 759.0, 369.0, 206.0, 69.0, lambda: show_SeeMore_page(master)),
        ("Calories.png", 531.0, 341.0, 100.0, 33.0, lambda: show_LogFood_page(master)),
        ("BMI.png", 531.0, 382.0, 100.0, 33.0, lambda: show_LogFood_page(master)),
        ("Macros.png", 531.0, 423.0, 100.0, 33.0, lambda: show_LogFood_page(master)),
        ("image_1.png", 313.0, 396.0, None, None, None)
    ]

    for details in image_details:
        image_name, x, y, width, height, command = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame6"))

        if command is not None:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img)

    master.images.append(img)

    font_large = Font(family="Consolas", slant="italic", size=20)
    font_medium = Font(family="Consolas", slant="italic", size=14)

    Label(master, text="Welcome, ", font=font_large, bg="#DAE6E4").place(x=80, y=33)
    Label(master, text="Log Food", font=font_medium, bg="#DAE6E4").place(x=171, y=255)
    Label(master, text="Today's Activity", font=font_medium, bg="#DAE6E4").place(x=398, y=255)
    Label(master, text="Goals", font=font_medium, bg="#DAE6E4").place(x=715, y=255)
    return Canvas


def show_app_page1(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_app_page1(master)



###URMATOAREA PAGINA PRINCIPALA
def setup_SeeMore_page(master):
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
        ("Back.png", -50.0, 369.0, 203.0, 67.0, lambda: show_app_page1(master)),
        ("AddWater.png", 509.0, 174.0, 50.0, 40.0, lambda: placeholder_function("AddWater")),
        ("RemoveWater.png", 318.0, 180.0, 50.0, 30.0, lambda: placeholder_function("RemoveWater")),
        ("MyProfile.png", 700.0, 68.0, 160.0, 131.0, lambda: show_profile_page(master)),
        ("Settings.png", 700.0, 268.0, 160.0, 131.0, lambda: show_settings_page(master)),
        ("image_1.png", 240.0, 115.0, None, None, None),
        ("image_2.png", 405.0, 139.0, None, None, None),
        ("image_3.png", 295.0, 315.0, None, None, None),
        ("entry_Water.png", 403.0, 236.5, 47.0, 30.0, None)
    ]

    for details in image_details:
        image_name, x, y, width, height, command = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame7"))
        master.images.append(img)

        if width is None or height is None:
            width, height = 100, 100

        if command:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')

    def placeholder_function(button_name):
        print(f"{button_name} button pressed. Functionality under construction.")

    font_medium = Font(family="Consolas", slant="italic", size=15)

    Label(master, text="My Profile", font=font_medium, bg="#DAE6E4").place(x=725, y=193)
    Label(master, text="Settings", font=font_medium, bg="#DAE6E4").place(x=735, y=393)
    Label(master, text="Streak", font=font_medium, bg="#DAE6E4").place(x=92, y=21)
    Label(master, text="days", font=font_medium, bg="#DAE6E4").place(x=101, y=96)
    Label(master, text="Liters", font=font_medium, bg="#FFFCF1").place(x=492, y=244)

    entry_Water = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_Water.place(x=420.0, y=245.0, width=53.0, height=22.5)

    return canvas


def show_SeeMore_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_SeeMore_page(master)
#def search_action():
    #query = search_entry.get()
   #print(f"Searching for: {query}")




###LOG FOOD PAGE
def setup_LogFood_page(master, relative_to_assets, selected_foods=None, selected_meal=None):
    master.configure(bg="#DAE6E4")

    def add_food_to_menu(food_data, meal_type):
        if meal_type == "Breakfast" and 'breakfast_listbox' in globals():
            breakfast_listbox.insert(END, food_data)
        elif meal_type == "Lunch" and 'lunch_listbox' in globals():
            lunch_listbox.insert(END, food_data)
        elif meal_type == "Dinner" and 'dinner_listbox' in globals():
            dinner_listbox.insert(END, food_data)
        elif meal_type == "Snack" and 'snack_listbox' in globals():
            snack_listbox.insert(END, food_data)

    canvas = tk.Canvas(
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
        ("image_1.png", 30.0, 70.0, None, None, None),
        ("image_2.png", 321.0, 70.0, None, None, None),
        ("image_3.png", 612.0, 70.0, None, None, None),
        ("image_4.png", 184.0, 329.0, None, None, None),
        ("AddF_Breakfast.png", 79.0, 145.0, 110.0, 23.0, lambda: show_Add_Food(master, "Breakfast")),
        ("AddF_Lunch.png", 372.0, 145.0, 110.0, 23.0, lambda: show_Add_Food(master, "Lunch")),
        ("AddF_Dinner.png", 663.0, 145.0, 110.0, 23.0, lambda: show_Add_Food(master, "Dinner")),
        ("Back.png", 14.0, 18.0, 59.0, 35.0, lambda: show_app_page1(master)),
        ("Add_Snack.png", 280.0, 380.0, 118.0, 15.0, lambda: show_Add_Food(master, "Snack"))
    ]

    for details in image_details:
        image_name, x, y, width, height, command = details
        img = tk.PhotoImage(file=relative_to_assets(image_name, "assets/frame8"))
        master.images.append(img)

        if width is None or height is None:
            width, height = 100, 100

        if command:
            button = tk.Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command, bg="#FFFCF1")
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')

    # Stil pentru listbox-uri
    listbox_bg = "#FFFCF1"
    listbox_fg = "#000000"
    listbox_font = ("Consolas", 12)

    # Creăm listbox-uri pentru fiecare masă, încadrate în casetele lor
    global breakfast_listbox, lunch_listbox, dinner_listbox, snack_listbox
    breakfast_listbox = tk.Listbox(master, width=23, height=5, bg=listbox_bg, fg=listbox_fg, font=listbox_font, bd=0, highlightthickness=0, relief="flat")
    breakfast_listbox.place(x=79, y=170)

    lunch_listbox = tk.Listbox(master, width=23, height=5, bg=listbox_bg, fg=listbox_fg, font=listbox_font, bd=0, highlightthickness=0, relief="flat")
    lunch_listbox.place(x=372, y=170)

    dinner_listbox = tk.Listbox(master, width=23, height=5, bg=listbox_bg, fg=listbox_fg, font=listbox_font, bd=0, highlightthickness=0, relief="flat")
    dinner_listbox.place(x=663, y=170)

    snack_listbox = tk.Listbox(master, width=23, height=5, bg=listbox_bg, fg=listbox_fg, font=listbox_font, bd=0, highlightthickness=0, relief="flat")
    snack_listbox.place(x=280, y=380)

    if selected_foods and selected_meal:
        for food_data in selected_foods:
            add_food_to_menu(food_data, selected_meal)

    return canvas


def show_LogFood_page(master, selected_foods=None, selected_meal=None):
    for widget in master.winfo_children():
        widget.destroy()
    setup_LogFood_page(master, relative_to_assets, selected_foods, selected_meal)
def add_food_to_menu(food_data, meal_type):
    if meal_type == "Breakfast":
        breakfast_listbox.insert(END, food_data)
    elif meal_type == "Lunch":
        lunch_listbox.insert(END, food_data)
    elif meal_type == "Dinner":
        dinner_listbox.insert(END, food_data)
    elif meal_type == "Snack":
        snack_listbox.insert(END, food_data)

def setup_Add_Food(master, show_LogFood_page, relative_to_assets, selected_meal):
    master.configure(bg="#DAE6E4")

    canvas = tk.Canvas(
        master,
        bg="#DAE6E4",
        height=503,
        width=937,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    customFont = font.Font(family="Consolas", size=15)

    # Listbox pentru alimentele selectate
    selected_foods_listbox = tk.Listbox(master, width=50, height=10, bg="#FFFCF1", fg="#000000", font=customFont, bd=0,
                                        highlightthickness=0, relief="flat")
    selected_foods_listbox.place(x=230, y=50)

    # Entry pentru căutare
    search_entry = tk.Entry(master, bd=4, relief="sunken", font=customFont, width=35)
    search_entry.place(x=230, y=230)

    # Listbox pentru sugestii
    suggestion_listbox = tk.Listbox(master, width=50, height=10, bg="#FFFCF1", fg="#000000", font=customFont, bd=0,
                                    highlightthickness=0, relief="flat")
    suggestion_listbox.place(x=230, y=270)

    def update_suggestions(event):
        search_text = search_entry.get().lower()
        suggestion_listbox.delete(0, END)
        suggestions = daily_intake.find_food_suggestions(search_text)
        for suggestion in suggestions:
            suggestion_listbox.insert(END, suggestion.description)

    search_entry.bind("<KeyRelease>", update_suggestions)

    def add_food_to_list(event):
        selected_food_index = suggestion_listbox.curselection()
        if selected_food_index:
            selected_food_name = suggestion_listbox.get(selected_food_index)
            selected_food = daily_intake.find_food(selected_food_name)
            if selected_food:
                # Extragem numele mâncării până la prima virgulă, dacă există
                display_name = selected_food_name.split(',')[0]
                selected_foods_listbox.insert(END, display_name)

    suggestion_listbox.bind("<<ListboxSelect>>", add_food_to_list)

    def search_action():
        food_name = search_entry.get().lower().strip()
        found_food = daily_intake.find_food(food_name)
        if found_food:
            messagebox.showinfo("Găsit", f"Alimentul '{food_name}' a fost găsit.")
        else:
            messagebox.showerror("Negăsit", f"Alimentul '{food_name}' nu a fost găsit.")

    add_button = tk.Button(master, text="Search", command=search_action)
    add_button.place(x=500, y=230)

    # Buton de "Back" cu imagine
    back_img = tk.PhotoImage(file=relative_to_assets("back.png", "assets/frame15"))
    master.images.append(back_img)
    back_button = tk.Button(master, image=back_img, borderwidth=0, highlightthickness=0, relief="flat",
                            command=lambda: show_LogFood_page(master, selected_foods_listbox.get(0, END),
                                                              selected_meal))
    back_button.place(x=22, y=17, width=42, height=36)
    back_button.image = back_img

    return canvas
def show_Add_Food(master, selected_meal):
    for widget in master.winfo_children():
        widget.destroy()
    setup_Add_Food(master, show_LogFood_page, relative_to_assets, selected_meal)
def add_food_to_menu(food_data, meal_type):
    if meal_type == "Breakfast":
        breakfast_listbox.insert(END, food_data)
    elif meal_type == "Lunch":
        lunch_listbox.insert(END, food_data)
    elif meal_type == "Dinner":
        dinner_listbox.insert(END, food_data)
    elif meal_type == "Snack":
        snack_listbox.insert(END, food_data)

def relative_to_assets(path, asset_dir):
    return f"{asset_dir}/{path}"






###TODAY'S ACTIVITY PAGE
def setup_TodayActivity_page(master):
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
        ("Back.png", 14.0, 18.0, 59.0, 38.0, lambda: show_app_page1(master)),
        ("image_1.png", 464.0, 257.0, None, None, None),
        ("image_2.png", 468.0, 176.99999999999994, None, None, None),
        ("image_3.png", 468.0, 244.99999999999994, None, None, None),
        ("image_4.png", 467.0, 312.9999999999999, None, None, None),
        ("image_5.png", 468.0, 380.9999999999999, None, None, None)
    ]

    for details in image_details:
        image_name, x, y, width, height, command = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame9"))
        master.images.append(img)
        if command is not None:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            if width is not None and height is not None:
                canvas.create_image(x, y, image=img, anchor='nw')
            else:
                canvas.create_image(x, y, image=img)

    font_large = Font(family="Consolas", slant="italic", size=20, underline=1)
    font_medium = Font(family="Consolas", slant="italic", size=16)

    Label(master, text="Today's Activity", font=font_large, bg="#FFFCF1").place(x=360, y=73)
    Label(master, text="Breakfast Meal:", font=font_medium, bg="#FFFCF1").place(x=324, y=146)
    Label(master, text="Lunch Meal:", font=font_medium, bg="#FFFCF1").place(x=324, y=214)
    Label(master, text="Dinner Meal:", font=font_medium, bg="#FFFCF1").place(x=324, y=282)
    Label(master, text="Water:", font=font_medium, bg="#FFFCF1").place(x=324, y=350)

    return canvas


def show_TodayActivity_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_TodayActivity_page(master)


current_goal = ""


def set_goal_and_show_info(goal, master):
    global current_goal
    current_goal = goal
    show_GoalInfo_page(master)



###PRIMA PAGINA PT GOALS
def setup_SetGoal_page(master):
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
        ("Weight_Loss.png", 289.0, 193.0, 350.0, 81.0, lambda: set_goal_and_show_info("Weight Loss", master)),
        ("Muscle_Build.png", 289.0, 283.0, 350.0, 81.0, lambda: set_goal_and_show_info("Muscle Build", master)),
        ("Maintenance.png", 289.0, 373.0, 350.0, 81.0, lambda: set_goal_and_show_info("Maintenance", master))
    ]

    for details in image_details:
        image_name, x, y, width, height, command = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame10"))
        master.images.append(img)
        button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
        button.place(x=x, y=y, width=width, height=height)
        button.image = img  # Atribuie imaginea la obiectul buton pentru a preveni garbage collection

    font_large = Font(family="Consolas", slant="italic", size=26, weight="bold")
    font_medium = Font(family="Consolas", slant="italic", size=20)

    Label(master, text="Let’s set your goals!", font=font_large, bg="#DAE6E4", fg="#000000").place(x=267, y=49)
    Label(master, text="First thing first, what do you want to achieve?", font=font_medium, bg="#DAE6E4",
          fg="#000000").place(x=147, y=108)

    master.mainloop()
    return canvas


def show_SetGoal_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_SetGoal_page(master)


goal_info_texts = {
}




###INFO GOALS
def setup_GoalInfo_page(master):
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
        ("SeeMore.png", 760.0, 433.0, 165.0, 39.0, lambda: show_GoalFinal_page(master)),
        ("image_1.png", 150.0, 154.0, None, None, None),
        ("image_2.png", 150.0, 190.0, None, None, None),
        ("image_3.png", 150.0, 226.0, None, None, None),
        ("image_4.png", 150.0, 262.0, None, None, None),
        ("image_5.png", 170.0, 305.0, None, None, None)
    ]

    for details in image_details:
        image_name, x, y, width, height, command = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame11"))
        master.images.append(img)

        if width and height:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')

    font_large = Font(family="Consolas", slant="italic", size=19)

    Label(master, text="Based on your choice, you should eat aproximatively(per day): ", font=font_large,
          bg="#DAE6E4").place(x=59, y=80)
    selected_texts = goal_info_texts.get(current_goal, {
        "kcal": "Configure your plan",
        "fats": "",
        "protein": "",
        "carbs": "",
        "reminder": ""
    })

    canvas.create_text(190.0, 147.0, anchor="nw", text=selected_texts["kcal"], fill="#000000",
                       font=("Consolas Italic", 18))
    canvas.create_text(190.0, 183.0, anchor="nw", text=selected_texts["fats"], fill="#000000",
                       font=("Consolas Italic", 18))
    canvas.create_text(190.0, 219.0, anchor="nw", text=selected_texts["protein"], fill="#000000",
                       font=("Consolas Italic", 18))
    canvas.create_text(190.0, 255.0, anchor="nw", text=selected_texts["carbs"], fill="#000000",
                       font=("Consolas Italic", 18))
    canvas.create_text(220.0, 362.0, anchor="nw", text=selected_texts["reminder"], fill="#515151",
                       font=("Consolas Italic", 16))

    return canvas


def show_GoalInfo_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_GoalInfo_page(master)


goal_details = {
    "Weight Loss": {"kcal": "1500 kcal", "fats": "50g", "protein": "60g", "carbs": "100g"},
    "Muscle Build": {"kcal": "3000 kcal", "fats": "80g", "protein": "150g", "carbs": "350g"},
    "Maintenance": {"kcal": "2500 kcal", "fats": "70g", "protein": "120g", "carbs": "200g"}
}




###GOAL-UL FINAL
def setup_GoalFinal_page(master):
    global current_goal
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
        ("Back.png", 14.0, 18.0, 58.0, 36.0, lambda: show_app_page1(master)),
        ("image_1.png", 70.0, 70.0, None, None, None),
        ("image_2.png", 70.0, 280.0, None, None, None),
        ("image_3.png", 500.0, 280.0, None, None, None),
        ("image_4.png", 500.0, 70.0, None, None, None)
    ]

    for details in image_details:
        image_name, x, y, width, height, command = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame12"))
        master.images.append(img)

        if width and height:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')

    details = goal_details[current_goal]

    canvas.create_text(200.0, 115.0, anchor="nw", text=details["kcal"], fill="#000000", font=("Consolas Italic", 22))
    canvas.create_text(630.0, 115.0, anchor="nw", text=details["fats"] + " of fat", fill="#000000",
                       font=("Consolas Italic", 22))
    canvas.create_text(170.0, 329.0, anchor="nw", text=details["carbs"] + " of carbs", fill="#000000",
                       font=("Consolas Italic", 22))
    canvas.create_text(593.0, 329.0, anchor="nw", text=details["protein"] + " of protein", fill="#000000",
                       font=("Consolas Italic", 22))

    font_m = Font(family="Consolas", slant="italic", size=18)

    Label(master, text="You aet " "      / " + details["kcal"], font=font_m, bg="#FFFCF1", fg="#515151").place(x=115,
                                                                                                               y=156)
    Label(master, text="You aet " + "      / " + details["fats"], font=font_m, bg="#FFFCF1", fg="#515151").place(x=580,
                                                                                                                 y=156)
    Label(master, text="You aet " + "      / " + details["carbs"], font=font_m, bg="#FFFCF1", fg="#515151").place(x=140,
                                                                                                                  y=369)
    Label(master, text="You aet " + "      / " + details["protein"], font=font_m, bg="#FFFCF1", fg="#515151").place(
        x=580, y=369)
    return canvas


def show_GoalFinal_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_GoalFinal_page(master)




###PAGINA PROFILULUI
def setup_profile_page(master):
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
        ("Back.png", 14.0, 18.0, 55.0, 36.0, lambda: show_SeeMore_page(master)),
        ("next.png", 738.0, 268.0, 32.0, 39.0, lambda: show_profile2_page(master)),
        ("image_1.png", 80.0, 20.0),

        ("image_2.png", -10.0, 66.0),
        ("image_3.png", 161.0, 470.0),
        ("image_4.png", 581.0, 22.0),
        ("image_5.png", 935.0, 354.0),
        ("image_6.png", 870.0, 265.0),
        ("image_7.png", 790.0, -15.0),
        ("image_8.png", 152.0, 45.0),
        ("image_9.png", 12.0, 404.0),
        ("image_10.png", 548.0, 491.0),
        ("image_11.png", 42.0, 227.0),
        ("image_12.png", 333.0, -70.0),
        ("image_13.png", 818.0, 429.0),
        ("image_14.png", 890.0, 85.0),

        ("image_15.png", 420.0, 35.0),
        ("image_16.png", 420.0, 35.0),
        ("image_17.png", 254.0, 242.51307678222656),
        ("image_18.png", 507.0, 242.51307678222656),
        ("image_19.png", 254.0, 311.5130615234375),
        ("image_20.png", 507.0, 311.5130615234375),
        ("image_21.png", 254.0, 380.5130615234375),
        ("image_22.png", 507.0, 380.5130615234375)
    ]

    for details in image_details:
        image_name, x, y, *args = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame13"))
        master.images.append(img)

        if len(args) == 3:
            width, height, command = args
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief='flat', command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')
    font_large = Font(family="Consolas", slant="italic", size=20)
    font_medium = Font(family="Consolas", slant="italic", size=16)

    Label(master, text="Last Name", font=font_medium, bg="#FFFCF1").place(x=262.03289794921875, y=193)
    Label(master, text="First Name", font=font_medium, bg="#FFFCF1").place(x=262.0657958984375, y=262)
    Label(master, text="My Profile", font=font_large, bg="#FFFCF1").place(x=260, y=95)
    Label(master, text="Age", font=font_medium, bg="#FFFCF1").place(x=515.0657958984375, y=331)
    Label(master, text="Password", font=font_medium, bg="#FFFCF1").place(x=515.0328979492188, y=193)
    Label(master, text="Email", font=font_medium, bg="#FFFCF1").place(x=262.0657958984375, y=331)
    Label(master, text="Username", font=font_medium, bg="#FFFCF1").place(x=515.0657958984375, y=262)

    return canvas
def show_profile_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_profile_page(master)
def setup_profile2_page(master):
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
        ("Back.png", 14.0, 18.0, 55.0, 36.0, lambda: show_SeeMore_page(master)),
        ("back_page.png", 182.94596222486825, 255.9999878536811, 32.0, 38.0, lambda: show_profile_page(master)),
        ("image_1.png", 80.0, 20.0),
        ("image_2.png", -10.0, 66.0),
        ("image_3.png", 161.0, 470.0),
        ("image_4.png", 581.0, 22.0),
        ("image_5.png", 935.0, 354.0),
        ("image_6.png", 870.0, 265.0),
        ("image_7.png", 790.0, -15.0),
        ("image_8.png", 152.0, 45.0),
        ("image_9.png", 12.0, 404.0),
        ("image_10.png", 548.0, 491.0),
        ("image_11.png", 42.0, 227.0),
        ("image_12.png", 333.0, -70.0),
        ("image_13.png", 818.0, 429.0),
        ("image_14.png", 890.0, 85.0),
        ("image_15.png", 420.0, 35.0),
        ("image_16.png", 420.0, 35.0),
        ("image_17.png", 254.0, 242.51307678222656),
        ("image_18.png", 507.0, 242.51307678222656),
        ("image_19.png", 254.03289794921875, 311.5130615234375),
        ("image_20.png", 507.0328979492188, 311.5130615234375)
    ]

    for details in image_details:
        image_name, x, y, *args = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame131"))
        master.images.append(img)

        if len(args) == 3:
            width, height, command = args
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief='flat', command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')
    font_large = Font(family="Consolas", slant="italic", size=20)
    font_medium = Font(family="Consolas", slant="italic", size=16)

    Label(master, text="My Profile", font=font_large, bg="#FFFCF1").place(x=260, y=95)
    Label(master, text="Weight", font=font_medium, bg="#FFFCF1").place(x=262.0657958984375, y=193)
    Label(master, text="Height", font=font_medium, bg="#FFFCF1").place(x=515.032958984375, y=193)
    Label(master, text="BMI", font=font_medium, bg="#FFFCF1").place(x=262.0657958984375, y=262)
    Label(master, text="Goal", font=font_medium, bg="#FFFCF1").place(x=515.0657958984375, y=262)

    return canvas
def show_profile2_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_profile2_page(master)

def show_profile_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_profile_page(master)
def setup_EditProfile_page(master):
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
        ("Save.png", 701.0, 410.0, 89.0, 33.0, lambda: save(master)),
        ("Back.png", 14.0, 18.0, 59.0, 37.0, lambda: show_settings_page(master)),
        ("edit_firstn.png", 405.0, 211.0, 27.0, 23.0, lambda: enter_firstn(master)),
        ("edit_email.png", 713.0, 211.0, 27.0, 23.0, lambda: enter_email(master)),
        ("edit_lastn.png", 405.0, 262.0, 27.0, 23.0, lambda: enter_lastn(master)),
        ("edit_age.png", 713.0, 262.0, 27.0, 23.0, lambda: enter_age(master)),
        ("edit_username.png", 405.0, 313.0, 27.0, 23.0, lambda: enter_username(master)),
        ("edit_weight.png", 713.0, 313.0, 27.0, 23.0, lambda: enter_weight(master)),
        ("edit_password.png", 405.0, 364.0, 27.0, 23.0, lambda: enter_password(master)),
        ("edit_height.png", 713.0, 364.0, 27.0, 23.0, lambda: enter_height(master)),
        ("image_1.png", 406.0, 73.0),
        ("image_2.png", 100.0, 115.0),
        ("image_3.png", 568.0, 10.0),

    ]

    for details in image_details:
        if len(details) == 6:
            image_name, x, y, width, height, command = details
            img = PhotoImage(file=relative_to_assets(image_name, "assets/frame16"))
            master.images.append(img)
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img  # This keeps a reference to avoid garbage collection
        else:
            image_name, x, y = details
            img = PhotoImage(file=relative_to_assets(image_name, "assets/frame16"))
            master.images.append(img)
            canvas.create_image(x, y, image=img, anchor='nw')

    font_large = Font(family="Consolas", slant="italic", size=24)

    canvas.create_text(475, 55, text="Edit Profile", font=font_large, fill="black")
    return canvas

def show_EditProfile_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_EditProfile_page(master)


###SETTINGS
def setup_settings_page(master):
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
        ("Back.png", 14.0, 18.0, 59.0, 37.0, lambda: show_SeeMore_page(master)),
        ("Edit_profile.png", 333.0, 161.0, 284.0, 47.0, lambda: show_EditProfile_page(master)),
        ("Change_goal.png", 342.0, 223.0, 275.0, 40.0, lambda: show_SetGoal_page(master)),
        ("Info_goal.png", 299.0, 274.0, 359.0, 34.0, lambda: show_GoalInfo_page(master)),
        ("App_details.png", 338.0, 328.0, 285.0, 43.0, lambda: show_AppDetail_page(master)),
        ("SignOut.png", 340.0, 381.0, 277.0, 43.0, lambda: show_main_page(master)),
        ("image_1.png", 225.0, 120.0),
        ("image_2.png", 350.0, 43.0),

        ("image_3.png", 918.0, 78.0),
        ("image_4.png", 773.0, 210.0),
        ("image_5.png", 872.0, 354.0),
        ("image_6.png", 795.0, 60.0),
        ("image_7.png", 726.0, 436.0),
        ("image_8.png", 630.0, 125.0),
        ("image_9.png", 215.0, -15.0),
        ("image_10.png", 388.0, 503.0),
        ("image_11.png", -20.0, 100.0),
        ("image_12.png", 239.0, 105.0),
        ("image_13.png", 100.0, 240.0),
        ("image_14.png", 81.0, 429.0)
    ]

    for details in image_details:
        image_name, x, y, *args = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame14"))
        master.images.append(img)

        if len(args) == 3:
            width, height, command = args
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief='flat', command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')

    font_large = Font(family="Consolas", slant="italic", size=32)

    Label(master, text="Settings", font=font_large, bg="#DAE6E4").place(x=413, y=42)


def show_settings_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_settings_page(master)
def setup_AppDetails_page(master):
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
        ("Back.png", 14.0, 18.0, 58.0, 36.0, lambda: show_settings_page(master)),
        ("image_1.png", 70.0, 80.0, None, None, None),
        ("image_2.png", 880.0, 10.0, None, None, None),
        ("image_3.png", 911.0, 225.0, None, None, None),
        ("image_4.png", 864.0, 366.0, None, None, None),
        ("image_5.png", 760.0, 83.0, None, None, None),
        ("image_6.png", 718.0, 448.0, None, None, None),
        ("image_7.png", 586.0, 27.0, None, None, None),
        ("image_8.png", 421.0, 55.0, None, None, None),
        ("image_9.png", 372.0, 470.0, None, None, None),
        ("image_10.png", 8.0, 134.0, None, None, None),
        ("image_11.png", 182.0, 23.0, None, None, None),
        ("image_12.png", 52.0, 385.0, None, None, None)
    ]

    for details in image_details:
        if len(details) == 6:
            image_name, x, y, width, height, command = details
        else:
            image_name, x, y = details
            width, height, command = None, None, None

        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame17"))
        master.images.append(img)

        if command:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command)
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')

    return canvas
