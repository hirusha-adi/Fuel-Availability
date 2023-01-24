from flask import request
from flask import url_for
from flask import redirect
from flask import session
from flask import g
from flask import render_template
from flask import jsonify
import random
import string
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from database.mongo import Pending, Stations, Users
from database.settings import ALLOWED_EXTENSIONS, uploadPath


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


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
    if regProof and _allowed_file(regProof.filename):
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
            uploadPath,
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
