import os
from flask import Flask, render_template, g, session, request, redirect, url_for
from generate import GenerateMap
from database.mongo import Users

app = Flask(__name__)
app.secret_key = 'the random string'


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


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.getUserByEmail(email=email)
        try:
            if user and user['password'] == password:
                session['user_id'] = user['id']
                return redirect(url_for('panel'))
            else:
                return redirect(url_for('login'))
        except:
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        session.pop('user_id', None)
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        Users.addUser(
            password=password,
            name=name,
            email=email
        )
        user = Users.getUserByEmail(email=email)
        session['user_id'] = user['id']
        return redirect(url_for('panel'))
    else:
        return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route("/panel")
def panel():
    if not g.user:
        return redirect(url_for('login'))
    user = Users.getUserByEmail(email=g.user['email'])
    return render_template("panel.html", user=user)


@app.route("/panel/edit/user", methods=['GET', 'POST'])
def panel_edit_user():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        pass
    else:
        return redirect(url_for('panel'))


if __name__ == "__main__":
    makeMap()
    app.run("0.0.0.0", port=8090, debug=True)
