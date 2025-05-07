from flask import current_app as app

def create_user(email, password):
    user_data = {
        "email": email,
        "password": password 
    }
    app.db["users"].insert_one(user_data)
    return user_data
