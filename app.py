from flask import Flask, render_template, request, redirect, session, url_for, abort, flash
from flask_session import Session
import os
import uuid

app = Flask(__name__)
#app.secret_key = "super_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

allowed_types = [".png", ".jpg", ".jpeg", ".gif"]
file_save_location = "static/images"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/games")
def view_games():
    return render_template("games.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_game():
    if request.method == "GET":
        return render_template("upload.html")

    elif request.method == "POST":
        if "games" not in session:
            session["games"] = []

        title = request.form["title"]
        platform = request.form["platform"]
        description = request.form["description"]

        uploaded_file = request.files.get("image")
        image_filename = None

        if uploaded_file and uploaded_file.filename != "":
            extension = os.path.splitext(uploaded_file.filename)[1].lower()
            if extension in allowed_types:
                unique_name = f"{uuid.uuid4().hex}{extension}"
                filename = os.path.join(file_save_location, unique_name)
                uploaded_file.save(filename)
                image_filename = unique_name
            else:
                flash("Invalid image type. Only PNG, JPG, JPEG, or GIF are allowed.", "error")
                return redirect(url_for("upload_game"))

        game = {
            "title": title,
            "platform": platform,
            "description": description,
            "image": image_filename
        }

        session["games"].append(game)
        session.modified = True

        flash(f'"{title}" added successfully!', "success")
        return redirect(url_for("view_games"))

@app.route("/delete/<int:index>", methods=["POST"])
def delete_game(index):
    if "games" not in session:
        abort(400)

    games = session["games"]

    if 0 <= index < len(games):
        game_title = games[index]["title"]
        del games[index]
        session["games"] = games
        session.modified = True
        flash(f'{game_title} deleted successfully.', "message")
    else:
        flash("Invalid game index.", "error")

    return redirect(url_for("view_games"))

if __name__ == "__main__":
    app.run(debug=True)