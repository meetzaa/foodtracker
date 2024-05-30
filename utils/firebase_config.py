# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("path/to/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

def get_firestore_client():
    initialize_firebase()
    return firestore.client()
