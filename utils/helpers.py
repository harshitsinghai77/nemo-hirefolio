import os
from datetime import datetime, timedelta

import bcrypt
import jwt

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def hash_password(password):
    # Function to hash a password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")  # Decode back to string for storage


# Function to authenticate a user based on username or email
def authenticate_user(user, user_entered_password):
    if user and bcrypt.checkpw(
        user_entered_password.encode("utf-8"), user["password"].encode("utf-8")
    ):
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


def get_dummy_data(email_address):
    if not email_address:
        return []
    
    dummy_data = [
        {
            "company_name": "S.H.I.E.L.D. Headquarters",
            "job_title": "Quinjet Mechanic",
            "link": "https://shieldjobs.gov/avengers-initiative",
            "status": "Pending (Thor insists on using a hammer)",
            "applied": "Yes",
            "application_method": "Hawkeye's arrow delivery",
            "application_date": "2024-01-11",
            "contact_person": "Nick Fury",
            "cold_email_sent": "No (Loki intercepted it)",
            "notes": "Must be comfortable working with Norse gods",
            "next_steps": "Practice assembling under 5 minutes",
        },
        {
            "company_name": "Central Perk Coffeehouse",
            "job_title": "Head Bean Counter",
            "link": "https://centralperk.com/jobs/smelly-cat-approved",
            "status": "Interviewing (Could I BE any more excited?)",
            "applied": "Yes",
            "application_method": "Pivot! (In person)",
            "application_date": "2024-01-12",
            "contact_person": "Gunther",
            "cold_email_sent": "Yes (Sent from Chandler's work computer)",
            "notes": "Bring extra sarcasm",
            "next_steps": "Master the art of the Unagi",
        },
        {
            "company_name": "Weasleys' Wizard Wheezes",
            "job_title": "Prank Product Tester",
            "link": "https://wheezes.com/careers/mischief-managed",
            "status": "Offer Received (Pending Ministry of Magic approval)",
            "applied": "Yes",
            "application_method": "Owl Post",
            "application_date": "2024-01-13",
            "contact_person": "Fred and George Weasley",
            "cold-email_sent": "No (Hedwig was busy delivering Hogwarts letters)",
            "notes": "Practice dodging Skiving Snackboxes",
            "next_steps": "Stock up on Ton-Tongue Toffees",
        },
        {
            "company_name": "Daily Prophet",
            "job_title": "Quidditch Correspondent",
            "link": "https://dailyprophet.com/jobs/quills-at-the-ready",
            "status": "Applied",
            "applied": "Yes",
            "application_method": "Flying Ford Anglia",
            "application_date": "2024-01-14",
            "contact_person": "Rita Skeeter",
            "cold_email_sent": "No (Sent via Howler)",
            "notes": "Bring Sneakoscope",
            "next_steps": "Brush up on Quidditch rules",
        },
        {
            "company_name": "Avengers Tower",
            "job_title": "Suit Up Intern",
            "link": "https://starkindustries.com/careers/iron-willed",
            "status": "Interested",
            "applied": "No",
            "application_method": "Waiting for Captain America's approval",
            "application_date": "",
            "contact_person": "Tony Stark",
            "cold_email_sent": "No (Jarvis is still under maintenance)",
            "notes": "Must be able to lift Mjolnir",
            "next_steps": "Practice assembling with Hulk-proof tools",
        },
    ]

    for obj in dummy_data:
        obj["user_email"] = email_address
    return dummy_data