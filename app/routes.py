from flask import request, jsonify
from app.models.user_model import view_note
from app.models.user_model import create_note

from app import app

@app.route("/view", methods=["POST"])
def view_note_route():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    notes = view_note(email)
    return jsonify({
        "message": "Here your note",
        "user": {
            "note" : notes
        }
    }), 200

@app.route("/create_note",methods=["POST"])
def create_note_route():
    data = request.get_json()

    email = data.get("email")
    notes = data.get("notes")
    tags = data.get("tags")
    create_date = data.get("create_date")
    note = create_note(email, notes, tags, create_date=None)
    return jsonify({
        "message": "Note is successfully created",
        "Note": {
            "email": note.get("email"),
            "note": note.get("notes"),
            "tags": note.get("tag"),
            "created_date": note.get("created_date")

        }
    }), 201

