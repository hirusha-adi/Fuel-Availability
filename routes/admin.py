from datetime import datetime

from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import jsonify

from generate import makeMap
from database.mongo import Pending
from database.mongo import Stations
from database.settings import adminkey


def admin_home():
    return render_template("admin.html")


def admin_panel():
    return render_template("admin.panel.html")


def admin_update():
    # Update map and redirect to the /map
    makeMap()
    return redirect(url_for('map'))


def admin_verify():
    """Verify the admin login key from `prompt()` in javascript with the backend"""
    secretKey = request.form.get('secretKey')
    if secretKey == adminkey:
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'no'})


def admin_approve():
    if request.method == 'POST':
        itemid = request.form.get('itemid')
        itemdo = request.form.get('itemdo')

        # Admin approved the station
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

        # Admin declined the station
        elif itemdo.lower() == 'remove':
            Pending.deleteByID(id=int(itemid))
            makeMap()
            return jsonify({'status': 'success'})

    else:
        # if GET
        data = {}
        data['pending'] = Pending.getAllStations()
        data['pending_length'] = len(data['pending'])
        return render_template('accept.html', **data)
