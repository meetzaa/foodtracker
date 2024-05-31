from tkinter import messagebox
from services.user_service import user_service
from ui.app_page1 import AppPage1
from firebase_config import db
def login(master, username, password, controller):
    user_ref = db.collection("users").where('username', '==', username).limit(1)
    user = user_ref.get()

    for doc in user:
        user_data = doc.to_dict()
        stored_password = user_data.get("password")

        if stored_password == password:
            messagebox.showinfo("Success", "Autentificare reușită!")
            user_key = doc.id  # Retrieve the user_key
            controller.add_page("AppPage1", AppPage1, user_key)
            controller.show_page("AppPage1", user_key)  # Pass the user_key to the AppPage1
            return True
        else:
            messagebox.showerror("Eroare", "Nume de utilizator sau parolă incorecte.")
            return False

    messagebox.showerror("Eroare", "Nume de utilizator sau parolă incorecte.")
    return False

def signup(master, first_name, last_name, username, email, password, confirm_password, controller):
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return False, None

    user_key, error = user_service.create_user(first_name, last_name, username, email, password)
    if error:
        messagebox.showerror("Error", error)
        return False, None

    messagebox.showinfo("Success", f"User created successfully! UserKey: {user_key}")
    controller.show_page("LoginPage")
    return True, user_key