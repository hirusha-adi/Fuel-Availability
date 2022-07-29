import os
from flask import Flask, render_template, g, session
from generate import GenerateMap
from database.mongo import Users

app = Flask(__name__)


def makeMap():
    obj = GenerateMap()
    obj.run(path=os.path.join(os.getcwd(), 'templates', 'map.html'))


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = Users.getUserByID(id=session['user_id'])
        g.user = user


@app.route("/")
@app.route("/map")
def index():
    return render_template("map.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/panel")
def panel():
    return render_template("panel.html")


if __name__ == "__main__":
    makeMap()
    app.run("0.0.0.0", port=8090, debug=True)
