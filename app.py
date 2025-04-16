from flask import Flask, render_template, request, redirect, session, url_for, abort, flash
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

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

        game = {
            "title": title,
            "platform": platform,
            "description": description
        }

        session["games"].append(game)
        session.modified = True

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