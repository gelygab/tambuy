
import firebase_admin
from firebase_admin import credentials, firestore

# firebaseConfig = {
#     'apiKey': "AIzaSyCCKm5R6f2BmfsRHd1381um73_9qOXjMdM",
#     'authDomain': "database-table-badc5.firebaseapp.com",
#     'databaseURL': "https://database-table-badc5-default-rtdb.firebaseio.com",
#     'projectId': "database-table-badc5",
#     'storageBucket': "database-table-badc5.appspot.com",
#     'messagingSenderId': "932634652261",
#     'appId': "1:932634652261:web:17c3f0bcd439576097e08c",
#     'measurementId': "G-GPMTBCPVQG"
# }

# 1. Connect to Firebase
import os

# Get the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the credentials file
cred_path = os.path.join(base_dir, 'database-table-badc5-firebase-adminsdk-fbsvc-fee7cfa592.json')
cred = credentials.Certificate(cred_path)  # <-- your JSON file here
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Initialize Firestore (or use Realtime Database if needed)
db = firestore.client()  # Firestore
# db = firebase_admin.db  # Uncomment if you're using Realtime Database

# firebase = pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()

# Function to store user data in Firestore
def add_user_to_firestore(user):
    user_id = user['localId']
    user_data = {
        'email': user['email'],
        'created_at': firestore.SERVER_TIMESTAMP
    }
    # Storing user data in Firestore under "users" collection
    db.collection('users').document(user_id).set(user_data)

