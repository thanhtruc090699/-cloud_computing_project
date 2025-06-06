from flask import request, jsonify
from app.models.user_model import view_note
from app.models.user_model import create_note
from app.models.user_model import find_note_by_tags
from datetime import datetime
from flask import render_template




from app import app
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/create", methods=["GET"])
def create_note_page():
    return render_template("create_note.html")


@app.route("/view", methods=["POST"])
def view_note_route():
    query = request.form.get("query")

    if not query: 
        return render_template("home.html", message="email or tag is required.")
    if "@" in query and "." in query:
        notes = view_note(query)
        return render_template("home.html", notes=notes, email=query)

    else:
        notes = find_note_by_tags(query) 
        return render_template("home.html",notes=notes)

@app.route("/search", methods=["POST"])
def find_note_by_tag_route():
    tag = request.form.get("tag")
    
    notes = find_note_by_tags(tag)
    return render_template("search.html",notes=notes, searched=tag)


@app.route("/create_note",methods=["POST"])
def create_note_route():

    email = request.form.get("email")
    notes = request.form.get("notes")
    tags = request.form.get("tag")
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("FORM DATA:", email, notes, tags)

    if not email or not notes: 
        return render_template("create_note.html", message="Email and note are required.")
    
    note = create_note(email, notes, tags)
    return render_template("create_note.html", note=note)




