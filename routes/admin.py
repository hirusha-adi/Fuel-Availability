from flask import render_template
from flask import url_for
from flask import redirect
from flask import jsonify, request
from database.mongo import Pending, Stations
from datetime import datetime
from generate import makeMap
from database.settings import adminkey


def admin_home():
    return render_template("admin.html")


def admin_panel():
    return render_template("admin.panel.html")


def admin_update():
    makeMap()
    return redirect(url_for('map'))


def admin_verify():
    secretKey = request.form.get('secretKey')
    if secretKey == adminkey:
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'no'})


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
