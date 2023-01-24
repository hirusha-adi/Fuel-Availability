import os
from datetime import datetime

from flask import g
from flask import request 
from flask import render_template
from flask import url_for
from flask import send_file
from flask import redirect
from flask import jsonify

from generate import makeMap
from database.mongo import Pending
from database.mongo import Stations
from database.mongo import Users
from database.settings import adminkey
from database.settings import Admin

def isAdmin(user):
    # The in user's information matches with the info in the backend
    return ((user['email'] == Admin.username) or (user['email'] == Admin.email)) and (user['id'] == Admin.id) and (user['password'] == Admin.password)


def admin_home():
    return render_template("admin.html")


def admin_panel():
    # login to redirect page if not logged in
    if not g.user:
        return redirect(url_for('login'))
    
    # send the currently logged in user
    adminAccess = isAdmin(user=g.user)
    
    # Login with account with admin access if you have not
    if not(adminAccess):
        return redirect(url_for('login'))
            
    
    data = {}

    """
    modes:
        overview
        settings
    """
    data['wmode'] = "overview"

    # TODAY's LOG FILES
    # -------------------------------------

    # Get File Names
    now = datetime.now()
    data['file_name_all'] = os.path.join(
        "logs",
        now.strftime("all_%Y_%m_%d.log")
    )
    data['file_name_unique'] = os.path.join(
        "logs",
        now.strftime("unique_%Y_%m_%d.log")
    )

    # Open Files and Get Info
    with open(data['file_name_all'], "r", encoding="utf-8") as _latest_log_all:
        latest_log_last_lines = _latest_log_all.readlines()
        data['latest_log_last_length'] = len(latest_log_last_lines)
        data['latest_log_last_lines'] = latest_log_last_lines[-10:]

    with open(data['file_name_unique'], "r", encoding="utf-8") as _latest_log_unique:
        unique_log_last_lines = _latest_log_unique.readlines()
        data['unique_log_last_length'] = len(unique_log_last_lines)
        data['unique_log_last_lines'] = unique_log_last_lines[-10:]
    
    data['unique_requests_percentage'] = str((data['unique_log_last_length']/data['latest_log_last_length'])*100)[:4]

    return render_template("admin.panel.html", **data)

def admin_download_log_noargs():
    return redirect(url_for('admin_panel'))

def admin_download_log(logtype):
    # login to redirect page if not logged in
    if not g.user:
        return redirect(url_for('login'))
    
    # send the currently logged in user
    adminAccess = isAdmin(user=g.user)
    
    # Login with account with admin access if you have not
    if not(adminAccess):
        return redirect(url_for('login'))
    
    # Get File Names
    now = datetime.now()
    file_name_all = os.path.join(
        "logs",
        now.strftime("all_%Y_%m_%d.log")
    )
    file_name_unique = os.path.join(
        "logs",
        now.strftime("unique_%Y_%m_%d.log")
    )
    
    # Return Files
    if logtype in ("all", "a"): # All
        return send_file(file_name_all)
    
    elif logtype in ("unique", "u"): # Unique
        return send_file(file_name_unique)

    else: # Redirect to admin page if none
        return redirect(url_for('admin_panel'))

def admin_update():
    # login to redirect page if not logged in
    if not g.user:
        return redirect(url_for('login'))
    
    # send the currently logged in user
    adminAccess = isAdmin(user=g.user)
    
    # Login with account with admin access if you have not
    if not(adminAccess):
        return redirect(url_for('login'))
    
    # ReMake the map and redirect to /map
    makeMap()
    return redirect(url_for('map'))


def admin_approve():
    # login to redirect page if not logged in
    if not g.user:
        return redirect(url_for('login'))
    
    # send the currently logged in user
    adminAccess = isAdmin(user=g.user)
    
    # Login with account with admin access if you have not
    if not(adminAccess):
        return redirect(url_for('login'))
    
    # Proceed if Admin
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
