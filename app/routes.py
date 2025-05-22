from flask import request, jsonify
from app.models.user_model import view_note
from app.models.user_model import create_note
from app.models.user_model import find_note_by_tags


from app import app

@app.route("/view", methods=["POST"])
def view_note_route():
    data = request.get_json()
    email = data.get("email")

    notes = view_note(email)
    return jsonify({

        "note" : notes

    }), 200

@app.route("/search", methods=["POST"])
def find_note_by_tag_route():
    data = request.get_json()
    tag = data.get("tag")
    
    notes = find_note_by_tags(tag)
    return jsonify({
        
            "note" : notes
        
    }), 200

@app.route("/create_note",methods=["POST"])
def create_note_route():
    data = request.get_json()

    email = data.get("email")
    notes = data.get("notes")
    tags = data.get("tag")
    create_date = data.get("create_date")

    if not email or not notes: 
        return jsonify({
            "message": "email and notes are required"
        }), 400
    
    note = create_note(email, notes, tags)
    return jsonify({
        "message": "Note is successfully created",
        "Note": {
            "email": note.get("email"),
            "note": note.get("notes"),
            "tags": note.get("tag"),
            "created_date": note.get("created_date")

        }
    }), 201

