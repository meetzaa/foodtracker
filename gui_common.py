from tkinter import *
from tkinter.font import Font
from pathlib import Path

<<<<<<< Updated upstream
def setup_login_page(master):
=======
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import re
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://foodtracker-8fe6b-default-rtdb.europe-west1.firebasedatabase.app/'
})
db = firestore.client()


<<<<<<< Updated upstream
def save_user_details(master, weight, height, age, username):
    # Actualizarea datelor utilizatorului cu greutatea, înălțimea și vârsta
    user_ref = db.collection("users").where("Utilizator", "==", username)
    user = user_ref.get()
    for doc in user:
        user_data = doc.to_dict()
        user_data["Greutate"] = weight
        user_data["Inaltime"] = height
        user_data["Varsta"] = age
        db.collection("users").document(doc.id).set(user_data)
    messagebox.showinfo("Success", "Date actualizate cu succes!")
    show_login(master)
def login(username, password, master):
    # Access the 'users' collection in Firestore
    users_ref = db.collection('users')

    # Query the database for the provided username and password
    query = users_ref.where('Utilizator', '==', username).where('Parola', '==', password).stream()

    # Check if the query result is not empty
    query_results = list(query)

    if query_results:
        # Retrieve the first document from the query results
        for user_doc in query_results:
            # Convert the document to a dictionary
            user_data = user_doc.to_dict()

            # Check if any of the fields (greutate/inaltime/varsta) is None
            if (user_data.get('Greutate') is None or
                user_data.get('Inaltime') is None or
                user_data.get('Varsta') is None):
                messagebox.showinfo("Informație", "Completarea detaliilor este necesară!")
                test_user = users_ref.where('utilizator', '==', username).limit(1).get()
                show_gravity_check_page(master)
            else:
                # All details are present, redirect to the main page
                show_app_page1(master)
    else:
        # No user found with the provided credentials
        messagebox.showerror("Error", "Invalid username or password")

=======
def login(master, username, password):
    # Interogare pentru a găsi utilizatorul cu numele specificat
    user_ref = db.collection("users").where("Utilizator", "==", username).limit(1)
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


def save_user_details(master, weight, height, age, user_key):
>>>>>>> Stashed changes

    # Actualizarea datelor utilizatorului cu greutatea, înălțimea și vârsta
    user_details_ref = db.collection("UserDetails").where("UserKey", "==", user_key)
    user_details = user_details_ref.get()
    for doc in user_details:
        user_details_data = doc.to_dict()
        user_details_data["Greutate"] = weight
        user_details_data["Înălțime"] = height
        user_details_data["Vârstă"] = age
        db.collection("UserDetails").document(doc.id).set(user_details_data)
        print("Date actualizate pentru documentul:", doc.id)
    show_login(master)
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
>>>>>>> Stashed changes
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets/frame1"

    def relative_to_assets(path: str) -> str:
        """Returnează calea completă a unui asset relativ la directorul de assets."""
        return str(ASSETS_PATH / path)

    master.configure(bg="#DAE6E4")

<<<<<<< Updated upstream
=======

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
            messagebox.showerror("Eroare", "Un utilizator cu același nume sau aceeași adresă de e-mail există deja!")
            return
        if not is_valid_email(email_value):
            messagebox.showerror("Eroare", "Adresa de e-mail nu este într-un format corect")
            return
        user_data = {
            "Utilizator": username_value,
            "Nume": last_name_value,
            "Prenume": first_name_value,
            "Email": email_value,
            "Parola": password_value,
            "Greutate": None,  # Adăugați aici și alte câmpuri pentru varsta, inaltime, etc.
            "Inaltime": None,
            "Varsta": None
        }
        assert isinstance(db, object)
        db.collection("users").add(user_data)
        messagebox.showinfo("Titlu", "Inregistrare cu succes!")
<<<<<<< Updated upstream
        show_gravity_check_page(master,username_value)
=======
        show_gravity_check_page(master,user_key)
>>>>>>> Stashed changes
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

>>>>>>> Stashed changes
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

    # Păstrarea imaginilor într-o listă de referințe
    master.images = []

    # Încărcarea și plasarea imaginilor specifice
    image_details = [
        ("image_1.png", 467.0, 283.0),
        ("entry_1.png", 468.5, 199.0),  # Fundal pentru primul Entry
        ("entry_2.png", 468.5, 323.0),  # Fundal pentru al doilea Entry
        ("button_1.png", 337.0, 410.6),
        ("button_2.png", 540.0, 458.0),
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

<<<<<<< Updated upstream
    for img_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(img_name))
        if "button" in img_name:
            if img_name == "button_2.png":
                button = Button(master, image=img, borderwidth=0, highlightthickness=0,
                                command=lambda: show_signup(master),
                                relief="flat")
            else:
                button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.place(x=x, y=y, width=273.0 if "button_1" in img_name else 71.0,
                         height=41.365234375 if "button_1" in img_name else 19.0)
            button.image = img  # Keep a reference to prevent garbage collection
=======
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
                button.config(command=lambda: login(master,entry_Username.get(), entry_Password.get()))
                button.place(x=x, y=y, width=273.0, height=41.365234375)
>>>>>>> Stashed changes
        else:
            canvas.create_image(x, y, image=img)
        master.images.append(img)
    # Crearea și plasarea Entry-urilor
    entry_1 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_1.place(x=294.0, y=177.0, width=349.0, height=43.0)

    entry_2 = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_2.place(x=294.0, y=300.0, width=349.0, height=43.0)

    # Fonturile pentru texte
    TitluFont = Font(family="Consolas", slant="italic", size=26)
    TextFont = Font(family="Consolas", slant="italic", size=13)
    TextRFont = Font(family="Consolas", slant="italic", size=11)

    # Adăugarea textelor pe ecran
    Label(master, text="Welcome back, gourmet guru!", font=TitluFont, bg="#DAE6E4").place(x=228, y=20)
    Label(master, text="Username", font=TextFont, bg="#FFFCF1").place(x=280, y=142)
    Label(master, text="Password", font=TextFont, bg="#FFFCF1").place(x=280, y=265)
    Label(master, text="Don't have an account?", font=TextRFont, bg="#FFFCF1", fg="#5E5858").place(x=335, y=455)


def setup_signup_page(master):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets/frame2"

    def relative_to_assets(path: str) -> str:
        return str(ASSETS_PATH / path)

    master.configure(bg="#DAE6E4")

    # Crearea unui canvas pentru plasarea imaginilor
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

    # Păstrarea imaginilor într-o listă de referințe
    master.images = []

    # Încărcarea și plasarea imaginilor
    image_details = [
        ("image_1.png", 469.0, 282.0),
        ("entry_1.png", 273.5, 164.0),  # Fundal pentru primul Entry
        ("entry_2.png", 676.5, 164.0),  # Fundal pentru al doilea Entry
        ("entry_3.png", 274.0, 247.6),
        ("entry_4.png", 676.5, 247.0),
        ("entry_5.png", 275.0, 330),
        ("entry_6.png", 676.5, 330.0),
        ("button_1.png", 326.0, 392.0),  # Locația butonului 1
        ("button_2.png", 545.0, 441.0)  # Locația butonului 2
    ]

    for image_name, x, y in image_details:
        img = PhotoImage(file=relative_to_assets(image_name))
        if "button" in image_name:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat")
            button.image = img  # Keep a reference to prevent garbage collection
            if "button_1.png" == image_name:
                button.config(command=lambda: print("button_1 clicked"))
                button.place(x=x, y=y, width=296.0, height=43.0)
            elif "button_2.png" == image_name:
                button.config(command=lambda m=master: show_login(m))  # Correctly capturing master
                button.place(x=x, y=y, width=62.0, height=20.0)
        else:
            canvas.create_image(x, y, image=img)
        master.images.append(img)

    # Fonturile pentru texte
    Titlu1Font = Font(family="Consolas", slant="italic", size=20)
    Titlu2Font = Font(family="Consolas", slant="italic", size=20, weight="bold")
    InputFont = Font(family="Consolas", slant="italic", size=12)
    AccFont = Font(family="Consolas", slant="italic", size=11)

    # Crearea și plasarea Entry-urilor
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
<<<<<<< Updated upstream
=======


# Definirea paginii pentru inputurile BMI-ului
def setup_gravity_check_page(master,username_value):
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
                button.config(command=lambda: save_user_details(master, entry_kg.get(), entry_cm.get(), entry_age.get(),
                                                                username_value))
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


def show_gravity_check_page(master,username_value):
    for widget in master.winfo_children():
        widget.destroy()
    setup_gravity_check_page(master,username_value)


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
        ("Profile.png", 870.0, 25.0, 43.0, 45.0, lambda: show_profile_page(master)),
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

    Label(master, text="Welcome, ", font=font_large, bg="#DAE6E4").place(x=661, y=33)
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
        ("AddWater.png", 589.0, 74.0, 50.0, 40.0, lambda: placeholder_function("AddWater")),
        ("RemoveWater.png", 398.0, 80.0, 50.0, 30.0, lambda: placeholder_function("RemoveWater")),
        ("MyProfile.png", 223.0, 298.0, 160.0, 131.0, lambda: show_profile_page(master)),
        ("MyMeals.png", 432.0, 298.0, 160.0, 131.0, lambda: show_MyMeals(master)),
        ("Settings.png", 642.0, 298.0, 160.0, 131.0, lambda: show_settings_page(master)),
        ("image_1.png", 320.0, 10.0, None, None, None),
        ("image_2.png", 485.0, 39.0, None, None, None),
        ("image_3.png", 380.0, 215.0, None, None, None),
        ("entry_Water.png", 483.0, 136.5, 47.0, 30.0, None)
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

    Label(master, text="My Profile", font=font_medium, bg="#DAE6E4").place(x=250, y=428)
    Label(master, text="My Meals", font=font_medium, bg="#DAE6E4").place(x=473, y=428)
    Label(master, text="Settings", font=font_medium, bg="#DAE6E4").place(x=681, y=428)
    Label(master, text="Streak", font=font_medium, bg="#DAE6E4").place(x=92, y=21)
    Label(master, text="days", font=font_medium, bg="#DAE6E4").place(x=101, y=96)
    Label(master, text="Liters", font=font_medium, bg="#FFFCF1").place(x=572, y=144)

    entry_Water = Entry(master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    entry_Water.place(x=500.0, y=145.0, width=53.0, height=22.5)

    return canvas


def show_SeeMore_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_SeeMore_page(master)




###LOG FOOD PAGE
def setup_LogFood_page(master):
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
        ("image_1.png", 30.0, 70.0, None, None, None),
        ("image_2.png", 321.0, 70.0, None, None, None),
        ("image_3.png", 612.0, 70.0, None, None, None),
        ("image_4.png", 184.0, 329.0, None, None, None),
        ("AddF_Breakfast.png", 79.0, 145.0, 110.0, 23.0, lambda: Add_Breakfast(master)),
        ("AddF_Lunch.png", 372.0, 145.0, 110.0, 23.0, lambda: Add_Lunch(master)),
        ("AddF_Dinner.png", 663.0, 145.0, 110.0, 23.0, lambda: Add_Dinner(master)),
        ("Back.png", 14.0, 18.0, 59.0, 35.0, lambda: show_app_page1(master)),
        ("Add_Snack.png", 280.0, 380.0, 118.0, 15.0, lambda: Add_Snack(master))

    ]

    for details in image_details:
        image_name, x, y, width, height, command = details
        img = PhotoImage(file=relative_to_assets(image_name, "assets/frame8"))
        master.images.append(img)

        if width is None or height is None:
            width, height = 100, 100

        if command:
            button = Button(master, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=command,
                            bg="#FFFCF1")
            button.place(x=x, y=y, width=width, height=height)
            button.image = img
        else:
            canvas.create_image(x, y, image=img, anchor='nw')

    return canvas


def show_LogFood_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_LogFood_page(master)




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
        ("button_1.png", 657.0, 225.0, 30.0, 31.0, lambda: show_nextpage(master)),
        ("button_2.png", 14.0, 18.0, 59.0, 38.0, lambda: show_app_page1(master)),
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
    "Weight Loss": {
        "kcal": "1200 to 1500 kcal",
        "fats": "~0.3 to 0.5 grams per kg of fats",
        "protein": "1.0/1.2 grams of protein per kg of body weight",
        "carbs": "50 to 100 grams of carbohydrates",
        "reminder": "Increase your water intake to aid in fat loss!"
    },
    "Muscle Build": {
        "kcal": "2500 to 3000 kcal",
        "fats": "0.8 to 1 grams per kg of fats",
        "protein": "2.0/2.5 grams of protein per kg of body weight",
        "carbs": "300 to 350 grams of carbohydrates",
        "reminder": "Protein is crucial for muscle repair and growth!"
    },
    "Maintenance": {
        "kcal": "2000 to 2500 kcal",
        "fats": "0.6 to 0.8 grams per kg of fats",
        "protein": "1.5/2.0 grams of protein per kg of body weight",
        "carbs": "150 to 200 grams of carbohydrates",
        "reminder": "Maintaining balance is key to long-term health!"
    }
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
        ("PlanReady.png", 646.0, 433.0, 265.0, 39.0, lambda: show_GoalFinal_page(master)),
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
        ("Back.png", 14.0, 18.0, 63.0, 41.0, lambda: show_app_page1(master)),
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
        ("Back.png", 14.0, 18.0, 55.0, 35.0, lambda: show_SeeMore_page(master)),
        ("next.png", 744.0, 268.0, 32.0, 39.0, lambda: show_next_page(master)),
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
        ("image_17.png", 270.0, 230.0),
        ("image_18.png", 523.0, 230.0),
        ("image_19.png", 270.0, 299.0),
        ("image_20.png", 523.0, 299.0),
        ("image_21.png", 270.0, 368.0),
        ("image_22.png", 523.0, 368.0)
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

    font_large = Font(family="Consolas", slant="italic", size=15)
    font_medium = Font(family="Consolas", slant="italic", size=12)

    Label(master, text="My Profile", font=font_large, bg="#FFFCF1").place(x=310, y=110)
    Label(master, text="First Name", font=font_medium, bg="#FFFCF1").place(x=274, y=183)
    Label(master, text="Password", font=font_medium, bg="#FFFCF1").place(x=527, y=183)
    Label(master, text="Last Name", font=font_medium, bg="#FFFCF1").place(x=274, y=252)
    Label(master, text="Username", font=font_medium, bg="#FFFCF1").place(x=527, y=252)
    Label(master, text="Email", font=font_medium, bg="#FFFCF1").place(x=274, y=321)
    Label(master, text="Age", font=font_medium, bg="#FFFCF1").place(x=527, y=321)
    return canvas


def show_profile_page(master):
    for widget in master.winfo_children():
        widget.destroy()
    setup_profile_page(master)




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
>>>>>>> Stashed changes
