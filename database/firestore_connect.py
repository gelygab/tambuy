
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

# Initialize Firebase with credentials from environment variable
try:
    # Get credentials from environment
    firebase_creds = os.environ.get('FIREBASE_CREDENTIALS')
    if not firebase_creds:
        raise ValueError('FIREBASE_CREDENTIALS environment variable is not set')

    # Parse JSON credentials
    creds_dict = json.loads(firebase_creds)

    # Initialize Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(cred)
except json.JSONDecodeError:
    raise ValueError('Invalid JSON in FIREBASE_CREDENTIALS environment variable')
except Exception as e:
    raise Exception(f'Failed to initialize Firebase: {str(e)}')

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

