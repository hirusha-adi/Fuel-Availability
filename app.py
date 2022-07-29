from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/map")
def index():
    return render_template("map.html")
