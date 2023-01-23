import os
import random
import string
from datetime import datetime

from flask import Flask
from flask import jsonify, redirect, render_template, url_for, send_from_directory
from flask import g, request, session
from werkzeug.utils import secure_filename

from database.mongo import Pending, Stations, Users
from database.settings import adminkey, contactEmail, flaskSecret
from generate import GenerateMap

app = Flask(__name__)
app.secret_key = flaskSecret
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
if not (os.path.isdir(app.config['UPLOAD_FOLDER'])):
    os.makedirs(app.config['UPLOAD_FOLDER'])
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
uniqueVisitors = set()

if not (os.path.isdir(os.path.join(os.getcwd(), "logs"))):
    os.makedirs("logs")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def makeMap():
    obj = GenerateMap()
    obj.run(path=os.path.join(
        os.getcwd(), 'templates', 'map.html'
    ),
        petrol=True,
        diesel=True
    )
    obj.run(path=os.path.join(
        os.getcwd(), 'templates', 'map_petrol.html'
    ),
        petrol=True,
        diesel=False
    )
    obj.run(path=os.path.join(
        os.getcwd(), 'templates', 'map_diesel.html'
    ),
        petrol=False,
        diesel=True
    )


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = Users.getUserByID(id=session['user_id'])
        g.user = user


@app.before_request
def log_all_requests():
    now = datetime.now()
    with open(now.strftime("logs/all_%Y_%m_%d.log"), "a") as f:
        f.write("{} - {} - {} - {}\n".format(
            now,
            request.remote_addr,
            request.user_agent,
            request.path
        ))


@app.before_request
def log_unique_requests():
    now = datetime.now()
    ip = request.remote_addr
    if not (ip in uniqueVisitors):
        uniqueVisitors.add(ip)
        with open(now.strftime("logs/unique_%Y_%m_%d.log"), "a") as f:
            f.write("{} - {} - {} - {}\n".format(
                now,
                ip,
                request.user_agent,
                request.path
            ))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/map/petrol")
def map_petrol():
    return render_template("map_petrol.html")


@app.route("/map/diesel")
def map_diesel():
    return render_template("map_diesel.html")


@app.route("/amount/<id>")
def amounts(id):
    data = Stations.getByID(id=id)
    user_agent = request.headers.get('User-Agent').lower()
    if ("iphone" in user_agent) or ("android" in user_agent):
        mobile = True
    else:
        mobile = False
    return render_template("amounts.html", data=data, mobile=mobile)


@app.route("/contact")
def contact_us():
    return redirect(f'mailto:{contactEmail}')


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
        if g.user:
            return redirect(url_for('panel'))

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
                adiesel="0",
                apetrol="0",
                lastupdated=str(datetime.now()),
                capacity_diesle=data_pending['capacity']['diesel'],
                capacity_petrol=data_pending['capacity']['petrol']
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


@app.route("/dashboard")
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
        petrolamt = request.form.get('petrolamt')
        dieselamt = request.form.get('dieselamt')
        try:
            Stations.updateAvailability(
                id=int(fillingStationNameID),
                petrol=True if petrolAvailability == '1' else False,
                diesel=True if dieselAvailability == '1' else False
            )
            Stations.updateAmount(
                id=int(fillingStationNameID),
                petrol=str(petrolamt),
                diesel=str(dieselamt)
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

    petrolamtcap = request.form.get('petrolamtcap')
    dieselamtcap = request.form.get('dieselamtcap')

    try:
        petrolamtcap = int(petrolamtcap)
    except:
        petrolamtcap = 100

    try:
        dieselamtcap = int(dieselamtcap)
    except:
        dieselamtcap = 100

    status = {'status': []}
    if len(fsname) < 5:
        status['status'].append('Please enter a valid filling station name')

    if not ((petrolAvailability in ['1', '2']) or (dieselAvailability in ['1', '2'])):
        status['status'].append('Invalid values for fuel availability given')

    if len(fsphone) < 9:
        status['status'].append('Please enter a valid Phone Number')

    if len(bussinessRegistrationNumber) < 4:
        status['status'].append(
            'Please enter a valid Bussiness Registration Number')

    if not (('maps.google.com' in fsgoogleurl) or ('/maps')):
        status['status'].append(
            'Invalid Google Maps URL. make sure you have "maps.google.com" in the url')

    try:
        coordinates = fsgoogleurl.split('@')[1].split(',')[0:2]
        if len(coordinates) == 0:
            status['status'].append('Error processing the Google Maps URL')
    except IndexError:
        status['status'].append('Error processing the Google Maps URL')

    # if 'regProof' not in request.files:
    #     return status['status'].append('Please upload the proof of registration and try again!')
    # regProof = request.files['regProof']
    # path = os.path.join(app.config['UPLOAD_FOLDER'], regProof.filename)
    # regProof.save(path)

    if 'regProof' not in request.files:
        status['status'].append(
            'Please upload the proof of registration and try again!')
    regProof = request.files['regProof']
    if regProof.filename == '':
        status['status'].append(
            'Please select a proper file')
    if regProof and allowed_file(regProof.filename):
        filename = ''.join(
            random.choice(
                string.ascii_letters + string.digits
            ) for i in range(5)
        ) + str(
            secure_filename(
                regProof.filename
            )
        )
        savepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )
        regProof.save(savepath)

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
        image=filename,
        lastupdated=datetime.now(),
        capacity_petrol=petrolamtcap,
        capacity_diesle=dieselamtcap
    )

    return jsonify({'status': 'success'})


@app.route("/admin", methods=['GET'])
def admin_home():
    return render_template("admin.html")


@app.route("/admin/panel", methods=['GET'])
def admin_panel():
    return render_template("admin.panel.html")


@app.route("/admin/update", methods=['GET'])
def admin_update():
    makeMap()
    return redirect(url_for('map'))


@app.route("/admin/verify", methods=['POST'])
def admin_verify():
    secretKey = request.form.get('secretKey')
    if secretKey == adminkey:
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'no'})


if __name__ == "__main__":
    makeMap()
    app.run("0.0.0.0", port=7879, debug=True)
