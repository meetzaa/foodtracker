# controllers/login_controller.py
from tkinter import messagebox

class LoginController:
    def __init__(self, user_service, page_controller):
        self.user_service = user_service
        self.page_controller = page_controller

    def login(self, master, username, password):
        user = self.user_service.authenticate_user(username, password)
        if user:
            messagebox.showinfo("Success", "Autentificare reușită!")
            self.page_controller.set_user_key(user.user_id)
            self.page_controller.show_page("main")
            return True
        else:
            messagebox.showerror("Eroare", "Nume de utilizator sau parolă incorecte.")
            return False
