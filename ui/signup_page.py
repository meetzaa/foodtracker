from tkinter import Label, Entry, Button, Canvas, PhotoImage, messagebox
from tkinter.font import Font
from ui.base_page import BasePage
from utils.utils import check_existing_user, is_valid_email, generate_user_key
from firebase_config import db
from pathlib import Path

# Define the paths for the assets
OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame2"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class SignupPage(BasePage):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.password_visible = False  # Initial state for password visibility
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#DAE6E4")

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.images = []

        image_details = [
            ("image_1.png", 469.0, 282.0),
            ("first_name.png", 273.5, 164.0),
            ("last_name.png", 676.5, 164.0),
            ("username.png", 274.0, 247.6),
            ("confirm_password.png", 676.5, 247.0),
            ("password.png", 275.0, 330),
            ("mail.png", 676.5, 330.0),
            ("Submit.png", 326.0, 392.0),
            ("Log_In.png", 565, 440)
        ]

        for image_name, x, y in image_details:
            img_path = relative_to_assets(image_name)
            try:
                img = PhotoImage(file=img_path)
                if "Submit.png" == image_name:
                    button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat")
                    button.image = img
                    button.config(command=self.submit_button_pressed)
                    button.place(x=x, y=y, width=296.0, height=43.0)
                elif "Log_In.png" == image_name:
                    button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=self.show_login)
                    button.image = img
                    button.place(x=x, y=y, width=62.0, height=20.0)
                else:
                    canvas.create_image(x, y, image=img)
                self.images.append(img)
            except Exception as e:
                print(f"Error loading image {image_name}: {e}")

        # Define fonts
        Titlu1Font = Font(family="Consolas", slant="italic", size=20)
        Titlu2Font = Font(family="Consolas", slant="italic", size=20, weight="bold")
        InputFont = Font(family="Consolas", slant="italic", size=12)
        AccFont = Font(family="Consolas", slant="italic", size=11)

        # Create and place entries
        self.first_name = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.first_name.place(x=143.0, y=149.0, width=261.0, height=27.0)
        self.first_name.bind("<Return>", self.submit_button_pressed)

        self.username = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.username.place(x=546.0, y=149.0, width=261.0, height=27.0)
        self.username.bind("<Return>", self.submit_button_pressed)

        self.last_name = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.last_name.place(x=144.0, y=232.0, width=261.0, height=27.0)
        self.last_name.bind("<Return>", self.submit_button_pressed)

        self.mail = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.mail.place(x=144.0, y=314.0, width=261.0, height=27.0)
        self.mail.bind("<Return>", self.submit_button_pressed)

        self.password = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
        self.password.place(x=546.0, y=232.0, width=261.0, height=27.0)
        self.password.bind("<Return>", self.submit_button_pressed)

        self.confirm_password = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
        self.confirm_password.place(x=546.0, y=314.0, width=261.0, height=27.0)
        self.confirm_password.bind("<Return>", self.submit_button_pressed)

        # Add "Show Password" button
        self.show_password_button = Button(self, text="Show", command=self.toggle_password_visibility)
        self.show_password_button.place(x=835, y=232, width=40, height=27)

        # Add labels
        Label(self, text="Bite-sized", font=Titlu1Font, bg="#DAE6E4").place(x=170, y=18)
        Label(self, text="sign-up", font=Titlu2Font, bg="#DAE6E4").place(x=330, y=18)
        Label(self, text="for your", font=Titlu1Font, bg="#DAE6E4").place(x=445, y=18)
        Label(self, text="mega appetite", font=Titlu2Font, bg="#DAE6E4").place(x=575, y=18)
        Label(self, text="!", font=Titlu1Font, bg="#DAE6E4").place(x=773, y=18)

        Label(self, text="First Name", font=InputFont, bg="#FFFCF1").place(x=137, y=117)
        Label(self, text="Username", font=InputFont, bg="#FFFCF1").place(x=539, y=117)
        Label(self, text="Password", font=InputFont, bg="#FFFCF1").place(x=539, y=200)
        Label(self, text="Confirm Password", font=InputFont, bg="#FFFCF1").place(x=539, y=283)
        Label(self, text="Last Name", font=InputFont, bg="#FFFCF1").place(x=137, y=200)
        Label(self, text="e-mail", font=InputFont, bg="#FFFCF1").place(x=137, y=283)

        Label(self, text="Already have an account?", font=AccFont, bg="#FFFCF1", fg="#5E5858").place(x=345, y=440)

    def submit_button_pressed(self, event=None):
        first_name_value = self.first_name.get()
        last_name_value = self.last_name.get()
        username_value = self.username.get()
        email_value = self.mail.get()
        password_value = self.password.get()
        confirm_password_value = self.confirm_password.get()

        if not self.all_fields_completed():
            messagebox.showerror("Eroare", "Toate câmpurile trebuie completate")
            return

        if confirm_password_value != password_value:
            messagebox.showerror("Eroare", "Parolele nu coincid")
            return

        if check_existing_user(username_value, email_value):
            messagebox.showerror("Eroare", "Un utilizator cu același nume sau aceeași adresă de e-mail există deja!")
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
            "UserKey": user_key,
            "details": {
                "Age": None,
                "Weight": None,
                "Height": None,
                "Goal": None
            }
        }
        db.collection("users").add(user_data)

        self.controller.show_page_with_user_key("GravityCheckPage", user_key)

    def all_fields_completed(self):
        return all([
            self.first_name.get(),
            self.last_name.get(),
            self.username.get(),
            self.mail.get(),
            self.password.get(),
            self.confirm_password.get()
        ])

    def toggle_password_visibility(self):
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password.config(show="")
            self.confirm_password.config(show="")
            self.show_password_button.config(text="Hide")
        else:
            self.password.config(show="*")
            self.confirm_password.config(show="*")
            self.show_password_button.config(text="Show")

    def relative_to_assets(self, path: str) -> str:
        full_path = Path(__file__).parent / 'assets' / 'frame2' / path
        print(f"Loading image from: {full_path}")
        return str(full_path)

    def show_login(self):
        self.controller.show_page("LoginPage")
