from tkinter import Canvas, Label, Button, Entry, PhotoImage, messagebox
from tkinter.font import Font
from .base_page import BasePage
from utils.utils import authenticate_user, get_user_details_by_user_key
from pathlib import Path
import concurrent.futures

class LoginPage(BasePage):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#DAE6E4")
        self.images = []

        canvas = Canvas(self, bg="#DAE6E4", height=503, width=937, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Load and place images
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
            img_path = self.relative_to_assets(image_name)
            img = PhotoImage(file=img_path)
            if "LogIn.png" in image_name:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=self.login)
                button.image = img
                button.place(x=x, y=y, width=273.0, height=41.365234375)
            elif "SignUp.png" in image_name:
                button = Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: self.controller.show_page("SignupPage"))
                button.image = img
                button.place(x=x, y=y, width=71.0, height=19.0)
            else:
                canvas.create_image(x, y, image=img)
            self.images.append(img)

        TitluFont = Font(family="Consolas", slant="italic", size=26)
        TextFont = Font(family="Consolas", slant="italic", size=13)
        TextRFont = Font(family="Consolas", slant="italic", size=11)

        Label(self, text="Create your account!", font=TitluFont, bg="#DAE6E4").place(x=228, y=20)
        Label(self, text="Username", font=TextFont, bg="#FFFCF1").place(x=280, y=142)
        Label(self, text="Password", font=TextFont, bg="#FFFCF1").place(x=280, y=265)
        Label(self, text="Don't have an account?", font=TextRFont, bg="#FFFCF1", fg="#5E5858").place(x=335, y=455)

        self.entry_Username = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_Username.place(x=294.0, y=177.0, width=349.0, height=43.0)
        self.entry_Username.bind("<Return>", self.login)

        self.entry_Password = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
        self.entry_Password.place(x=294.0, y=300.0, width=349.0, height=43.0)
        self.entry_Password.bind("<Return>", self.login)

    def login(self, event=None):
        username = self.entry_Username.get()
        password = self.entry_Password.get()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(authenticate_user, username, password)
            user_key = future.result()

        if user_key:
            self.controller.show_page("AppPage1", user_key)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def relative_to_assets(self, path: str) -> str:
        full_path = Path(__file__).parent.parent / 'assets' / 'frame1' / path
        print(f"Loading image from: {full_path}")
        return str(full_path)
