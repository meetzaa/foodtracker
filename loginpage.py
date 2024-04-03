import tkinter as tk
from tkinter import messagebox
from main import FoodTrackingApp

def login():
    username = username_entry.get()
    password = password_entry.get()

    #autentificare dummy, trebuie implementat sql/docker
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome back, {}!".format(username))
        root.destroy()
        app = FoodTrackingApp()
        app.show_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

root = tk.Tk()
root.title("Food Tracking App Login")

root.geometry("600x400")
root.resizable(False, False)


logo_image = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=logo_image)
logo_label.place(relx=0.2, rely=0.5, anchor="center")

username_label = tk.Label(root, text="Username:", font=("Helvetica", 14))
username_label.place(relx=0.7, rely=0.3, anchor="center")
username_entry = tk.Entry(root, font=("Helvetica", 12), bd=0, highlightthickness=2, highlightbackground="#007BFF",
                          highlightcolor="#007BFF")
username_entry.place(relx=0.7, rely=0.35, anchor="center", width=200)

password_label = tk.Label(root, text="Password:", font=("Helvetica", 14))
password_label.place(relx=0.7, rely=0.45, anchor="center")
password_entry = tk.Entry(root, font=("Helvetica", 12), show="*", bd=0, highlightthickness=2, highlightbackground="#007BFF",
                          highlightcolor="#007BFF")
password_entry.place(relx=0.7, rely=0.5, anchor="center", width=200)

login_button = tk.Button(root, text="Login", font=("Helvetica", 12, "bold"), bg="#007BFF", fg="white", bd=0, padx=20, pady=5,
                         command=login)
login_button.place(relx=0.7, rely=0.6, anchor="center", width=100)

signup_button = tk.Button(root, text="Sign Up", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", bd=0, padx=20, pady=5)
signup_button.place(relx=0.7, rely=0.7, anchor="center", width=100)

root.mainloop()
