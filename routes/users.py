
import random
import string
import os

from datetime import datetime

from flask import g
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import render_template
from flask import jsonify
from werkzeug.utils import secure_filename

from database.mongo import Pending
from database.mongo import Stations
from database.mongo import Users
from database.settings import ALLOWED_EXTENSIONS
from database.settings import uploadPath


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login():
    if request.method == 'POST':
        # remove `user_id` from sessions to remove any conflicts in the future
        session.pop('user_id', None)

        # Get info from form
        email = request.form.get('email')
        password = request.form.get('password')

        # get user from db
        user = Users.getUserByEmail(email=email)

        try:
            if user and user['password'] == password:
                # password matched
                session['user_id'] = user['id']
                return redirect(url_for('panel'))
            else:
                # password incorrect
                return redirect(url_for('login'))
        except:
            return redirect(url_for('login'))

    else:  # GET
        # If already logged in
        if g.user:
            return redirect(url_for('panel'))

        # Return to login page if not
        return render_template("login.html")


def signup():
    if request.method == 'POST':
        # remove `user_id` from sessions to remove any conflicts in the future
        session.pop('user_id', None)

        # Get info from form
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Add user to db
        Users.addUser(
            password=password,
            name=name,
            email=email
        )

        # Get new user from db again and store to session
        user = Users.getUserByEmail(email=email)
        session['user_id'] = user['id']

        return redirect(url_for('panel'))

    else:  # GET
        return render_template("signup.html")


def logout():
    # Remove `user_id` from session
    session.pop('user_id', None)
    return redirect(url_for('index'))


def panel():
    if not g.user:
        # login to redirect page if not logged in
        return redirect(url_for('login'))

    # Get all required user info to display in the user dashboard
    data = {}
    data['user'] = Users.getUserByEmail(email=g.user['email'])
    data['pending'] = Pending.getByEmail(email=g.user['email'])
    data['pending_length'] = len(data['pending'])
    data['stations'] = Stations.getByEmail(email=g.user['email'])
    data['stations_length'] = len(data['stations'])
    return render_template("panel.html", **data)


def panel_edit_user():
    """
    fullname (disabled) - cannot be changed
    email (disabled) - cannot be changed
    npassword - New Password
    vpassword - Re-entered New Password to check for errors and typos
    """
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # get details from form
        npassword = request.form.get('npassword')
        vpassword = request.form.get('vpassword')
        try:
            if npassword == vpassword:
                # update db is new password == verify password (the re-enter thing)
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
    else:  # GET
        return redirect(url_for('panel'))


def panel_edit_station():
    if not g.user:
        # login to redirect page if not logged in
        return redirect(url_for('login'))

    if request.method == 'POST':
        # get info from request
        fillingStationNameID = request.form.get('fillingStationNameID')
        petrolAvailability = request.form.get('petrolAvailability')
        dieselAvailability = request.form.get('dieselAvailability')
        petrolamt = request.form.get('petrolamt')
        dieselamt = request.form.get('dieselamt')
        try:  # update db
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

        This will create a request for the Admins to approve,
        once approved, you can manage it and update it and
        it will be shown on the map.
    """

    if not g.user:
        # login to redirect page if not logged in
        return redirect(url_for('login'))

    # Main Information - Required
    fsname = request.form.get('fsname')
    fscity = request.form.get('fscity')
    fsgoogleurl = request.form.get('fsgoogleurl')
    fsphone = request.form.get('fsphone')
    petrolAvailability = request.form.get('petrolAvailability')
    dieselAvailability = request.form.get('dieselAvailability')
    bussinessRegistrationNumber = request.form.get(
        'bussinessRegistrationNumber')

    # Capacity - How much can they store? In litres
    petrolamtcap = request.form.get('petrolamtcap')
    dieselamtcap = request.form.get('dieselamtcap')

    # Default to 100 if any issue occurs
    try:
        petrolamtcap = int(petrolamtcap)
    except:
        petrolamtcap = 100

    try:
        dieselamtcap = int(dieselamtcap)
    except:
        dieselamtcap = 100

    # Check for errors and send to the front end
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

    # get coordinated from the google maps url
    try:
        coordinates = fsgoogleurl.split('@')[1].split(',')[0:2]
        if len(coordinates) == 0:
            status['status'].append('Error processing the Google Maps URL')
    except IndexError:
        status['status'].append('Error processing the Google Maps URL')

    # I have no idea whats going on in here
    # if 'regProof' not in request.files:
    #     return status['status'].append('Please upload the proof of registration and try again!')
    # regProof = request.files['regProof']
    # path = os.path.join(app.config['UPLOAD_FOLDER'], regProof.filename)
    # regProof.save(path)

    # Check for bussiness registration proof files
    if 'regProof' not in request.files:
        status['status'].append(
            'Please upload the proof of registration and try again!')

    regProof = request.files['regProof']

    if regProof.filename == '':
        status['status'].append(
            'Please select a proper file')

    # Save it in the upload path by sanitizing the name
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

    # If any errors, return them to the front end, dont add to pending list
    if len(status['status']) != 0:
        return jsonify(status)

    # Add everything to the Pending list for the admins to approve
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
