import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# Path to the downloaded service account key
firebase_key_path = os.getenv("FIREBASE_KEY_PATH", "./firebase-key.json")

if not os.path.exists(firebase_key_path):
    raise FileNotFoundError(f"Firebase key file not found at {firebase_key_path}")

cred = credentials.Certificate(firebase_key_path)

# Initialize Firebase app (singleton check to avoid reinit)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()
