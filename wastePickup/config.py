import firebase_admin
from firebase_admin import credentials

# Initialize Firebase only if it hasn't been initialized yet
if not firebase_admin._apps:
    cred = credentials.Certificate("wastePickup/key.json")
    firebase_admin.initialize_app(cred)