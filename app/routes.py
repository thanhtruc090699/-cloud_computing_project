from flask import request, jsonify
from app.models.user_model import create_user
from app.models.user_model import create_note

from app import app

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = create_user(email, password)
    return jsonify({
        "message": "User created",
        "user": {
            "email": user.get("email")
        }
    }), 201

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

