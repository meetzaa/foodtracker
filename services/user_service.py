# services/user_service.py
from models.user import User
from services.firebase_service import firebase_service
from utils.utils import generate_user_key

class UserService:
    def __init__(self):
        self.db = firebase_service.get_firestore_client()

    def get_user_by_username(self, username):
        user_ref = self.db.collection("users").where('username', '==', username).limit(1)
        users = user_ref.get()
        for doc in users:
            user_data = doc.to_dict()
            return User(doc.id, user_data['username'], user_data['password'], user_data['user_key'])
        return None

    def authenticate_user(self, username, password):
        user = self.get_user_by_username(username)
        if user and user.password == password:
            return user
        return None

    def create_user(self, first_name, last_name, username, email, password):
        user_ref = self.db.collection("users").where('username', '==', username).limit(1)
        user = user_ref.get()
        if user:
            return None, "Username already exists"

        user_key = generate_user_key()
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password": password,
            "user_key": user_key
        }

        user_ref = self.db.collection("users").add(user_data)
        user_key = user_ref[1].id
        return user_key, None

user_service = UserService()
