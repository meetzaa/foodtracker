import uuid
import re
from firebase_config import db

import os
from tkinter import messagebox
def check_existing_user(username, email):
    users_ref = db.collection('users')
    query_username = users_ref.where('Utilizator', '==', username).get()
    query_email = users_ref.where('Email', '==', email).get()

    if query_username or query_email:
        return True
    return False
def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, ""
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    return False


def check_existing_user(username, email):
    query_username = db.collection("users").where("Utilizator", "==", username).limit(1).get()
    query_email = db.collection("users").where("Email", "==", email).limit(1).get()
    return bool(query_username) or bool(query_email)

def is_valid_email(email):
    """
    Validate the format of an email address using a regular expression.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None
def is_username_available(username):
    query_username = db.collection("users").where("Utilizator", "==", username).limit(1).get()
    return not bool(query_username)
def generate_user_key():
    """
    Generate a unique key for a user.
    """
    return str(uuid.uuid4())
def save_user_details(controller, user_key, weight, height, age):
    try:
        weight = float(weight)
        height = float(height)
        age = int(age)
    except ValueError:
        raise ValueError("Please enter valid numbers for weight, height, and age")

    user_ref = db.collection("users").where("UserKey", "==", user_key).get()

    if not user_ref:
        raise Exception(f"User with key {user_key} not found")

    for user in user_ref:
        user_id = user.id
        user_ref = db.collection("users").document(user_id)
        user_details_data = {
            "details": {
                "Weight": weight,
                "Height": height,
                "Age": age
            }
        }
        user_ref.update(user_details_data)
        print("Date actualizate pentru utilizator:", user_id)
        messagebox.showinfo("Success", "Date actualizate cu succes!")
        controller.show_page("LoginPage")
        return

    raise Exception(f"User with key {user_key} not found")
def verify_login_credentials(username, password):
    query = db.collection("users").where("Utilizator", "==", username).limit(1).get()
    if not query:
        return None
    for doc in query:
        user_data = doc.to_dict()
        if user_data["Parola"] == password:
            return user_data["UserKey"]
    return None
def get_username_by_user_key(user_key):
    users_ref = db.collection("users")
    query = users_ref.where("UserKey", "==", user_key).limit(1).get()
    if query:
        user_data = query[0].to_dict()
        return user_data.get("Utilizator", "Unknown")
    return "Unknown"


def get_user_details_by_user_key(user_key):
    try:
        user_ref = db.collection("users").where("UserKey", "==", user_key).limit(1).get()
        if user_ref:
            user_doc = user_ref[0]
            return user_doc.to_dict()
        else:
            return None
    except Exception as e:
        print(f"Error getting user details: {e}")
        return None
def authenticate_user(username, password):
    try:
        user_ref = db.collection("users").where("Utilizator", "==", username).where("Parola", "==", password).limit(1).get()
        if user_ref:
            user_doc = user_ref[0]
            user_data = user_doc.to_dict()
            return user_data.get("UserKey")
        else:
            return None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None

def get_user_physical_details_by_user_key(user_key):
    user_details = get_user_details_by_user_key(user_key)
    if user_details and 'details' in user_details:
        return user_details['details']
    return None

def get_user_document_by_key(user_key):
    try:
        user_ref = db.collection("users").where('UserKey', '==', user_key).limit(1)
        users = user_ref.get()
        for doc in users:
            return doc.id, doc.to_dict()
    except Exception as e:
        print(f"Error finding user document by key: {e}")
    return None, None
