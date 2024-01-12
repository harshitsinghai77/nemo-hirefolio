import os
from datetime import datetime, timedelta

import bcrypt
import jwt

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

def hash_password(password):
    # Function to hash a password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')  # Decode back to string for storage

# Function to authenticate a user based on username or email
def authenticate_user(user, user_entered_password):
    if user and bcrypt.checkpw(user_entered_password.encode('utf-8'), user['password'].encode('utf-8')):
        return True  # Password is correct
    
def create_access_token(data: dict):
    """Create new access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=365)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token):
    """Get the curren user based on token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        return payload
    except jwt.PyJWTError:
        return None
    