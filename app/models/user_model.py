from flask import current_app

def create_user(email, password):
    user_data = {
        "email": email,
        "password": password 
    }
    current_app.db["users"].insert_one(user_data)
    return user_data
