import os
from flask import Flask, render_template, g, session, request, redirect, url_for, jsonify
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
def index():
    return render_template("index.html")


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/about")
@app.route("/contact")
def contact_us():
    return render_template("index.html")


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


@app.route("/edit/user", methods=['GET', 'POST'])
def panel_edit_user():
    """
    fullname (disabled)
    email (disabled)
    npassword
    vpassword
    """
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        npassword = request.form.get('npassword')
        vpassword = request.form.get('vpassword')
        print(npassword, vpassword)
        try:
            if npassword == vpassword:
                Users.updateUser(
                    name=g.user['name'],
                    email=g.user['email'],
                    password=npassword
                )
                return jsonify({'status': 'done'})
            else:
                return jsonify({'status': 'nomatch'})
        except Exception as e:
            return jsonify({'status': f'ERROR: {e}'})
    else:
        return redirect(url_for('panel'))


@app.route("/edit/station", methods=['GET', 'POST'])
def add_new_station():
    """
    EASY ---->
        fsname -> Fillion Station's Name
        fsgoogleurl -> Google Maps URL
        petrolAvailability -> 1|2 -> Petrol
        dieselAvailability -> 1|2 -> Diesel
        bussinessRegistrationNumber -> Bussiness Registration Number
    """

    data = {}

    # always
    fsname = request.form.get('fsname')
    petrolAvailability = request.form.get('petrolAvailability')
    dieselAvailability = request.form.get('dieselAvailability')
    bussinessRegistrationNumber = request.form.get(
        'bussinessRegistrationNumber')

    status = {'status': []}
    if len(fsname) < 5:
        status['status'].append('Please enter a valid filling station name')

    if not((petrolAvailability in ['1', '2']) or (dieselAvailability in ['1', '2'])):
        status['status'].append('Invalid values for fuel availability given')

    if len(bussinessRegistrationNumber) < 4:
        status['status'].append(
            'Please enter a valid Bussiness Registration Number')

    if len(status['status']) >= 1:
        return jsonify(status)

    data['fsname'] = fsname
    data['petrolAvailability'] = petrolAvailability
    data['dieselAvailability'] = dieselAvailability
    data['bussinessRegistrationNumber'] = bussinessRegistrationNumber


if __name__ == "__main__":
    makeMap()
    app.run("0.0.0.0", port=8090, debug=True)
