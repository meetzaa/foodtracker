# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore

# Check if the Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

# Get the Firestore client
db = firestore.client()
