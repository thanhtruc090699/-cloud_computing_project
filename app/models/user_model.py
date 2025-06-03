from flask import current_app
from datetime import datetime


def view_note(email):
    notes = list(current_app.db["notes"].find({"email":email},{"_id":0}))
    return notes

def create_note(email, notes, tags):
    note_data = {
        "notes": notes,
        "email": email,
        "tag": tags,
        "created_date": datetime.utcnow().isoformat()
    }
    current_app.db["notes"].insert_one(note_data)
    return note_data

def find_note_by_tags(tags):
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")] 
    elif tags is None:
        tags = []
    notes = list(current_app.db["notes"].find({"tag":{"$in":tags}},{"_id":0}))
    return notes