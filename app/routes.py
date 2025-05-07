from flask import request, jsonify
from app.models.user_model import create_user
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

