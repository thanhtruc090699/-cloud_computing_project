from app import app

@app.route('/')
def home():
    return "Public Notes Platform is running!"
