
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
    """Initialize Firebase with credentials from environment variables or JSON file."""
    try:
        # First try environment variables
        if os.environ.get('FIREBASE_TYPE'):
            creds_dict = {
                'type': os.environ.get('FIREBASE_TYPE'),
                'project_id': os.environ.get('FIREBASE_PROJECT_ID'),
                'private_key_id': os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
                'private_key': os.environ.get('FIREBASE_PRIVATE_KEY'),
                'client_email': os.environ.get('FIREBASE_CLIENT_EMAIL'),
                'client_id': os.environ.get('FIREBASE_CLIENT_ID'),
                'auth_uri': os.environ.get('FIREBASE_AUTH_URI'),
                'token_uri': os.environ.get('FIREBASE_TOKEN_URI'),
                'auth_provider_x509_cert_url': os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
                'client_x509_cert_url': os.environ.get('FIREBASE_CLIENT_X509_CERT_URL')
            }
            # Initialize Firebase with dictionary
            if not firebase_admin._apps:
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
        else:
            # Fallback to JSON file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            cred_path = os.path.join(base_dir, 'database-table-badc5-firebase-adminsdk-fbsvc-fee7cfa592.json')
            if not firebase_admin._apps:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
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

