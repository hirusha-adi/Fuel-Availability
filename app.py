import os
from flask import Flask, render_template
from generate import GenerateMap

app = Flask(__name__)


def makeMap():
    obj = GenerateMap()
    obj.run(path=os.path.join(os.getcwd(), 'templates', 'map.html'))


@app.route("/")
@app.route("/map")
def index():
    return render_template("map.html")


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    makeMap()
    app.run("0.0.0.0", port=8090, debug=True)
