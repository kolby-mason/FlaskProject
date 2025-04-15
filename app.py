from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/games")
def view_games():
    return render_template("games.html")

if __name__ == "__main__":
    app.run(debug=True)