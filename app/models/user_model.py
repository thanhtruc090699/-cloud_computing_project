from flask import current_app
from datetime import datetime


def create_user(email, password):
    user_data = {
        "email": email,
        "password": password 
    }
    current_app.db["users"].insert_one(user_data)
    return user_data

def create_note(email, notes, tags, create_date=None):
    note_data = {
        "notes": notes,
        "email": email,
        "tag": tags,
        "created_date": create_date or datetime.utcnow().isoformat()
    }
    current_app.db["notes"].insert_one(note_data)
    return note_data