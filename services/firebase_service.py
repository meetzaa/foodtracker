import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseService:
    def __init__(self):
        if not firebase_admin._apps:
            self.cred = credentials.Certificate('serviceAccountKey.json')  # Ensure the correct path to your service account key
            firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def get_firestore_client(self):
        return self.db

# Singleton instance
firebase_service = FirebaseService()
