import os
from datetime import datetime

from flask import g
from flask import request
from flask import render_template
from flask import url_for
from flask import send_file
from flask import redirect
from flask import jsonify
from flask_paginate import Pagination

from generate import makeMap
from database import settings
from database.mongo import Pending
from database.mongo import Stations
from database.mongo import Users


def isAdmin(user):
    return ((user['email'] == settings.Admin.username) or (user['email'] == settings.Admin.email)) and (user['id'] == settings.Admin.id) and (user['password'] == settings.Admin.password)


def admin_home():
    return redirect(url_for('admin_panel'))


def admin_panel():
    return redirect(url_for('admin_panel_catergory', category='overview'))


def admin_panel_catergory(category):
    """
    category:
        overview
        settings
        alllogs
        uniquelogs
        fileslogs
        users
        stations
        pending
    """

    if not g.user:
        return redirect(url_for('login'))
    adminAccess = isAdmin(user=g.user)
    if not (adminAccess):
        return redirect(url_for('login'))

    category = str(category)

    data = {}

    if category.lower() in ("overview", "settings", "alllogs", "uniquelogs", "fileslogs", "users", "stations", "pending"):
        data['wmode'] = category.lower()
    else:
        data['wmode'] = "overview"

    if data['wmode'] in ("overview", "alllogs", "uniquelogs", "fileslogs"):
        now = datetime.now()
        data['file_name_all'] = os.path.join(
            "logs",
            now.strftime("all_%Y_%m_%d.log")
        )
        data['file_name_unique'] = os.path.join(
            "logs",
            now.strftime("unique_%Y_%m_%d.log")
        )

        with open(data['file_name_all'], "r", encoding="utf-8") as _latest_log_all:
            latest_log_last_lines = _latest_log_all.readlines()
            data['latest_log_last_length'] = len(latest_log_last_lines)
            if data['wmode'] == "alllogs":
                try:
                    current_page = int(request.args.get("page"))
                except:
                    current_page = 1
                list_all = latest_log_last_lines[::-1]
                list_length = len(list_all)
                per_page = 25
                max_possible_page = (list_length // per_page)+1
                if current_page > max_possible_page:
                    current_page = max_possible_page
                data['pagination'] = Pagination(
                    per_page=per_page,
                    page=current_page,
                    total=list_length,
                    href=str(url_for('admin_panel_catergory',
                             category='fileslogs', page=1))[:-1] + "{0}"
                )
                min_index = (current_page*per_page) - \
                    per_page
                max_index = (min_index + per_page)
                data['latest_log_last_lines'] = list_all[min_index:max_index]

            else:
                data['latest_log_last_lines'] = latest_log_last_lines[-10:]

        with open(data['file_name_unique'], "r", encoding="utf-8") as _latest_log_unique:
            unique_log_last_lines = _latest_log_unique.readlines()
            data['unique_log_last_length'] = len(unique_log_last_lines)
            if data['wmode'] == "uniquelogs":
                try:
                    current_page = int(request.args.get("page"))
                except:
                    current_page = 1
                list_all = unique_log_last_lines[::-1]
                list_length = len(list_all)
                per_page = 25
                max_possible_page = (list_length // per_page)+1
                if current_page > max_possible_page:
                    current_page = max_possible_page
                data['pagination'] = Pagination(
                    per_page=per_page,
                    page=current_page,
                    total=list_length,
                    href=str(url_for('admin_panel_catergory',
                             category='fileslogs', page=1))[:-1] + "{0}"
                )
                min_index = (current_page*per_page) - \
                    per_page
                max_index = (min_index + per_page)
                data['unique_log_last_lines'] = list_all[min_index:max_index]

            else:
                data['unique_log_last_lines'] = unique_log_last_lines[-10:]

        if data['wmode'] == "fileslogs":
            try:
                current_page = int(request.args.get("page"))
            except:
                current_page = 1

            list_all = [filename for filename in os.listdir("logs") if filename not in (
                data['file_name_all'][5:], data['file_name_unique'][5:])]

            list_length = len(list_all)
            per_page = 10
            max_possible_page = (list_length // per_page)+1
            if current_page > max_possible_page:
                current_page = max_possible_page
            data['pagination'] = Pagination(
                per_page=per_page,
                page=current_page,
                total=list_length,
                href=str(url_for('admin_panel_catergory',
                         category='fileslogs', page=1))[:-1] + "{0}"
            )
            min_index = (current_page*per_page) - \
                per_page
            max_index = (min_index + per_page)
            data['all_log_file_list'] = list_all[min_index:max_index]

        if data['wmode'] == "overview":
            data['unique_requests_percentage'] = str(
                (data['unique_log_last_length']/data['latest_log_last_length'])*100)[:4]
            data['total_no_users'] = len(Users.getAllUsers())
            data["total_pending_stations"] = len(Pending.getAllStations())
            data["total_approved_stations"] = len(Stations.getAllStations())

    if data['wmode'] == "settings":
        data['settings_flasksecret'] = settings.flaskSecret
        data['settings_jawgtoken'] = settings.JawgToken
        data['settings_contactemail'] = settings.contactEmail
        data['settings_mongo_ip'] = settings.MongoDB.ip
        data['settings_mongo_username'] = settings.MongoDB.username
        data['settings_mongo_password'] = settings.MongoDB.password
        data['settings_web_host'] = settings.WebServer.host
        data['settings_web_port'] = settings.WebServer.port
        data['settings_web_debug'] = settings.WebServer.debug

    if data['wmode'] == "users":
        data['user_admin_id'] = settings.Admin.id

        try:
            current_page = int(request.args.get("page"))
        except:
            current_page = 1

        try:
            filter = request.args.get("filter")
        except:
            pass

        try:
            q = request.args.get("q")
        except:
            pass

        try:
            if (filter and q):
                if q:
                    if filter == "id":
                        temp = Users.getUserByID(id=int(q), all=True)

                    elif filter == "email":
                        temp = Users.getUserByEmail(email=q, all=True)
                    elif filter == "name":
                        temp = Users.getUserByEmail(email=q, all=True)
                    elif filter == "password":
                        temp = Users.getUserByPassword(password=q, all=True)
                    else:
                        temp = Users.getAllUsers()

                    if isinstance(temp, list):
                        list_all = temp
                    else:
                        list_all = [temp]
            else:
                list_all = Users.getAllUsers()
        except:
            list_all = Users.getAllUsers()

        try:
            list_length = len(list_all)
        except TypeError:
            list_all = Users.getAllUsers()
            list_length = len(list_all)

        per_page = 20
        max_possible_page = (list_length // per_page)+1
        if current_page > max_possible_page:
            current_page = max_possible_page
        data['pagination'] = Pagination(
            per_page=per_page,
            page=current_page,
            total=list_length,
            href=str(url_for('admin_panel_catergory',
                     category='users', page=1))[:-1] + "{0}"
        )
        min_index = (current_page*per_page) - \
            per_page
        max_index = (min_index + per_page)
        data['users_all'] = list_all[min_index:max_index]

    if data['wmode'] == "stations" or data['wmode'] == "pending":
        isstations = False
        if data['wmode'] == "stations":
            isstations = True
        data['isstations'] = isstations
        
        try:
            current_page = int(request.args.get("page"))
        except:
            current_page = 1

        try:
            filter = request.args.get("filter")
        except:
            pass

        try:
            q = request.args.get("q")
        except:
            pass

        try:
            if (filter and q):
                if q:
                    if filter == "id":
                        temp = Stations.getByID(id=q) if isstations else Pending.getByID(id=q)
                    elif filter == "name":
                        temp = Stations.getByName(name=q) if isstations else Pending.getByName(name=q)
                    elif filter == "email":
                        temp = Stations.getByEmail(email=q) if isstations else Pending.getByEmail(email=q)
                    elif filter == "city":
                        temp = Stations.getByCity(city=q) if isstations else Pending.getByCity(city=q)
                    elif filter == "phone":
                        temp = Stations.getByPhone(phone=q) if isstations else Pending.getByPhone(phone=q)
                    elif filter == "coordinates":
                        temp = Stations.getByCoordinates(coordinates=q) if isstations else Pending.getByCoordinates(coordinates=q)
                    elif filter == "registration":
                        temp = Stations.getByRegistration(registration=q) if isstations else Pending.getByRegistration(registration=q)
                    else:
                        temp = Stations.getAllStations()

                    if isinstance(temp, list):
                        list_all = temp
                    else:
                        list_all = [temp]
            else:
                list_all = Stations.getAllStations() if isstations else Pending.getAllStations()
        except:
            list_all = Stations.getAllStations() if isstations else Pending.getAllStations()

        try:
            list_length = len(list_all)
        except TypeError:
            list_all = Stations.getAllStations() if isstations else Pending.getAllStations()
            list_length = len(list_all)

        per_page = 20
        max_possible_page = (list_length // per_page)+1
        if current_page > max_possible_page:
            current_page = max_possible_page
        data['pagination'] = Pagination(
            per_page=per_page,
            page=current_page,
            total=list_length,
            href=str(url_for('admin_panel_catergory',
                     category='pending', page=1))[:-1] + "{0}"
        )
        min_index = (current_page*per_page) - \
            per_page
        max_index = (min_index + per_page)
        data['stations_all'] = list_all[min_index:max_index]

    return render_template("admin.panel.html", **data)


def admin_delete_user(uid):
    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
        return redirect(url_for('login'))

    try:
        Users.deleteByID(id=uid)
        return jsonify({"status": "Deleted"})

    except Exception as e:
        return jsonify({"status": f"[Backend Error]: {e}"})


def admin_download_log_noargs():
    return redirect(url_for('admin_panel'))


def admin_download_log(logtype):

    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
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
    if logtype in ("all", "a"):  # All
        return send_file(file_name_all)

    elif logtype in ("unique", "u"):  # Unique
        return send_file(file_name_unique)

    else:  # Redirect to admin page if none
        return redirect(url_for('admin_panel'))


def admin_update():

    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
        return redirect(url_for('login'))

    # ReMake the map and redirect to /map
    makeMap()
    return redirect(url_for('map'))


def admin_approve():

    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
        return redirect(url_for('login'))

    # Proceed if Admin
    if request.method == 'POST':
        itemid = request.json['itemid']
        itemdo = request.json['itemdo']
    
        # Admin approved the station
        try:
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
                return jsonify({'wstatus': 'success'})

            # Admin declined the station
            elif itemdo.lower() == 'remove':
                Pending.deleteByID(id=int(itemid))
                makeMap()
                return jsonify({'wstatus': 'success'})
            
        except Exception as e:
            return jsonify({'wstatus': f'{e}'})

    else:
        return redirect(url_for('admin_panel_catergory', category='pending'))


def admin_download_file_no_arg():
    return redirect(url_for('admin_panel'))


def admin_download_file(logfilename):

    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
        return redirect(url_for('login'))

    return send_file(os.path.join("logs", logfilename))


def admin_delete_file_no_arg():
    return redirect(url_for('admin_panel'))


def admin_delete_file(logfilename):

    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
        return redirect(url_for('login'))

    finalfname = os.path.join("logs", logfilename)

    try:
        os.remove(finalfname)
        return jsonify({"status": "Deleted"})
    except:
        return jsonify({"status": "Failed"})


def amdin_settings_change(what):

    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
        return redirect(url_for('login'))

    if request.is_json:
        newval = request.json['newval']

    try:
        if what == "s-i-jawg-token":
            settings.uJawgToken(new=newval)
        elif what == "s-i-contact-email":
            settings.ucontactEmail(new=newval)

        elif what == "s-i-mongo-ip":
            settings.MongoDB.uip(new=newval)
        elif what == "s-i-mongo-username":
            settings.MongoDB.uusername(new=newval)
        elif what == "s-i-mongo-password":
            settings.MongoDB.upassword(new=newval)

        elif what == "s-i-web-host":
            settings.WebServer.uhost(new=newval)
        elif what == "s-i-web-port":
            settings.WebServer.uport(new=newval)
        elif what == "s-i-web-debug":
            if newval == "on":
                settings.WebServer.udebug(new=True)
            else:
                settings.WebServer.udebug(new=False)

        elif what == "users":
            Users.updateUserNewEmail(
                name=str(request.json['newname']),
                email=str(request.json['oldemail']),
                newEmail=str(request.json['newemail']),
                password=str(request.json['newpassword'])
            )

        elif what == "stationsapproved":
            Stations.updateStation(
                id=int(request.json['sameid']),
                name=str(request.json['newname']),
                registration=str(request.json['newregistration']),
                phone=str(request.json['newphone']),
                email=str(request.json['newemail']),
                coordinates=str(request.json['newcoordinates']),
                city=str(request.json['newcity'])
            )

        return jsonify({"wstatus": "ok"})

    except Exception as e:
        return jsonify({"wstatus": f"[Backend Error] -> {e}"})


def admin_delete_station(sid):
    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
        return redirect(url_for('login'))

    try:
        Stations.deleteByID(id=sid)
        return jsonify({"status": "Deleted"})
    except Exception as e:
        return jsonify({"status": f"[Backend Error]: {e}"})


def admin_stations_pending_image_no_args():
    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
        return redirect(url_for('login'))
    
    return redirect(url_for('admin_panel_catergory', category='pending'))
    
    
def admin_stations_pending_image(image): 
    if not g.user:
        return redirect(url_for('login'))

    adminAccess = isAdmin(user=g.user)

    if not (adminAccess):
        return redirect(url_for('login'))

    station = Pending.getByImage(image=image)
    if len(station) == 0:
        return redirect(url_for('admin_panel_catergory', category='pending'))
    
    data = {}
    data['title'] = f"{image} | Pending Station"
    data['image'] = image
    data['station'] = station[0]
    
    return render_template('image.html', **data)
