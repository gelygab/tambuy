
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

def initialize_firebase():
    """Initialize Firebase with credentials from JSON file."""
    try:
        # Get project root directory (2 levels up from this file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        # Construct path to JSON file
        cred_path = os.path.join(
            project_root,
            'database',
            'database-table-badc5-firebase-adminsdk-fbsvc-fee7cfa592.json'
        )
        
        # Print debug info
        print(f'Looking for Firebase credentials at: {cred_path}')
        print(f'Current directory: {current_dir}')
        print(f'Project root: {project_root}')
        print(f'File exists: {os.path.exists(cred_path)}')
        
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print(f'Successfully initialized Firebase with credentials from: {cred_path}')
    except Exception as e:
        print(f'Firebase initialization error: {str(e)}')
        raise

# Initialize Firebase
initialize_firebase()

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

