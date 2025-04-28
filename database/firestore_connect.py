
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
    """Initialize Firebase with credentials from environment variables."""
    required_fields = [
        'type', 'project_id', 'private_key_id', 'private_key',
        'client_email', 'client_id', 'auth_uri', 'token_uri',
        'auth_provider_x509_cert_url', 'client_x509_cert_url'
    ]
    
    try:
        # Get credentials from environment variables
        creds_dict = {}
        for field in required_fields:
            env_key = f'FIREBASE_{field.upper()}'
            value = os.environ.get(env_key)
            if not value:
                raise ValueError(f'Missing required environment variable: {env_key}')
            creds_dict[field] = value
            
        # Special handling for private_key - it needs newlines
        if '\n' not in creds_dict['private_key']:
            creds_dict['private_key'] = creds_dict['private_key'].replace('\\n', '\n')
        
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(creds_dict)
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

