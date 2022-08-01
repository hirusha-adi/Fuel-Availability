from datetime import datetime
from database.mongo import Users, Pending, Stations
from generate import GenerateMap
from flask import Flask, render_template, g, session, request, redirect, url_for, jsonify
import os
from database.settings import adminkey, flaskSecret

app = Flask(__name__)
app.secret_key = flaskSecret


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


@app.route("/admin/approve", methods=['GET', 'POST'])
def admin_approve():
    if request.method == 'POST':
        itemid = request.form.get('itemid')
        itemdo = request.form.get('itemdo')

        if itemdo.lower() == 'add':
            data_pending = Pending.getByID(id=int(itemid))
            Stations.addStation(
                name=data_pending['name'],
                registration=data_pending['registration'],
                phone=data_pending['phone'],
                email=data_pending['email'],
                coordinates=data_pending['coordinates'],
                city=data_pending['city'],
                petrol=data_pending['availablitiy']['petrol'],
                diesel=data_pending['availablitiy']['diesel'],
                lastupdated=str(datetime.now())
            )
            Pending.deleteByID(id=int(data_pending['id']))
            del data_pending
            makeMap()
            return jsonify({'status': 'success'})

        elif itemdo.lower() == 'remove':
            Pending.deleteByID(id=int(itemid))
            makeMap()
            return jsonify({'status': 'success'})

    else:
        data = {}
        data['pending'] = Pending.getAllStations()
        data['pending_length'] = len(data['pending'])
        return render_template('accept.html', **data)


@app.route("/panel")
def panel():
    if not g.user:
        return redirect(url_for('login'))

    data = {}
    data['user'] = Users.getUserByEmail(email=g.user['email'])
    data['pending'] = Pending.getByEmail(email=g.user['email'])
    data['pending_length'] = len(data['pending'])
    data['stations'] = Stations.getByEmail(email=g.user['email'])
    data['stations_length'] = len(data['stations'])
    return render_template("panel.html", **data)


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
def panel_edit_station():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        fillingStationNameID = request.form.get('fillingStationNameID')
        petrolAvailability = request.form.get('petrolAvailability')
        dieselAvailability = request.form.get('dieselAvailability')
        try:
            Stations.updateAvailability(
                id=int(fillingStationNameID),
                petrol=True if petrolAvailability == '1' else False,
                diesel=True if dieselAvailability == '1' else False
            )
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': f'ERROR: {e}'})
    else:
        return jsonify({'status': ''})


@app.route("/add/station", methods=['GET', 'POST'])
def add_new_station():
    """
        fsname -> Fillion Station's Name
        fscity -> City name
        fsgoogleurl -> Google Maps URL
        fsphone -> Phone Number
        petrolAvailability -> 1|2 -> Petrol
        dieselAvailability -> 1|2 -> Diesel
        bussinessRegistrationNumber -> Bussiness Registration Number
    """

    if not g.user:
        return redirect(url_for('login'))

    # always
    fsname = request.form.get('fsname')
    fscity = request.form.get('fscity')
    fsgoogleurl = request.form.get('fsgoogleurl')
    fsphone = request.form.get('fsphone')
    petrolAvailability = request.form.get('petrolAvailability')
    dieselAvailability = request.form.get('dieselAvailability')
    bussinessRegistrationNumber = request.form.get(
        'bussinessRegistrationNumber')

    status = {'status': []}
    if len(fsname) < 5:
        status['status'].append('Please enter a valid filling station name')

    if not((petrolAvailability in ['1', '2']) or (dieselAvailability in ['1', '2'])):
        status['status'].append('Invalid values for fuel availability given')

    if len(fsphone) < 9:
        status['status'].append('Please enter a valid Phone Number')

    if len(bussinessRegistrationNumber) < 4:
        status['status'].append(
            'Please enter a valid Bussiness Registration Number')

    if not(('maps.google.com' in fsgoogleurl) or ('/maps')):
        status['status'].append(
            'Invalid Google Maps URL. make sure you have "maps.google.com" in the url')

    try:
        coordinates = fsgoogleurl.split('@')[1].split(',')[0:2]
        if len(coordinates) == 0:
            status['status'].append('Error processing the Google Maps URL')
    except IndexError:
        status['status'].append('Error processing the Google Maps URL')

    if len(status['status']) != 0:
        return jsonify(status)

    Pending.addStation(
        name=fsname,
        registration=bussinessRegistrationNumber,
        phone=fsphone,
        email=g.user['email'],
        coordinates=coordinates,
        city=fscity,
        petrol=True if petrolAvailability == '1' else False,
        diesel=True if dieselAvailability == '1' else False,
        lastupdated=datetime.now()
    )

    return jsonify({'status': 'success'})


@app.route("/admin", methods=['GET'])
def admin_home():
    return render_template("admin.html")


@app.route("/admin/verify", methods=['POST'])
def admin_verify():
    secretKey = request.form.get('secretKey')
    if secretKey == adminkey:
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'no'})


if __name__ == "__main__":
    makeMap()
    app.run("0.0.0.0", port=8090, debug=True)
