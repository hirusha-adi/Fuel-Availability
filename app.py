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

from routes.general import *
from routes.stations import *
from routes.users import *
from routes.admin import *

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


# General
app.add_url_rule("/", 'index', index, methods=['GET'])
app.add_url_rule("/contact", 'contact_us', contact_us, methods=['GET'])

# Stations
app.add_url_rule("/map", 'map', map, methods=['GET'])
app.add_url_rule("/map/petrol", 'map_petrol', map_petrol, methods=['GET'])
app.add_url_rule("/map/diesel", 'map_diesel', map_diesel, methods=['GET'])
app.add_url_rule("/amount", 'amounts_no_id', amounts_no_id, methods=['GET'])
app.add_url_rule("/amount/<id>", 'amounts', amounts, methods=['GET'])


# Users
app.add_url_rule("/login", 'login', login, methods=['GET', 'POST'])
app.add_url_rule("/signup", 'signup', signup, methods=['GET', 'POST'])
app.add_url_rule("/logout", 'logout', logout, methods=['GET'])
app.add_url_rule("/dashboard", 'panel', panel, methods=['GET'])
app.add_url_rule("/edit/user", 'panel_edit_user',
                 panel_edit_user, methods=['GET', 'POST'])
app.add_url_rule("/edit/station", 'panel_edit_station',
                 panel_edit_station, methods=['GET', 'POST'])
app.add_url_rule("/add/station", 'add_new_station',
                 add_new_station, methods=['GET', 'POST'])

# Admin
app.add_url_rule("/admin", 'admin_home', admin_home, methods=['GET'])
app.add_url_rule("/admin/panel", 'admin_panel', admin_panel, methods=['GET'])
app.add_url_rule("/admin/update", 'admin_update',
                 admin_update, methods=['GET'])
app.add_url_rule("/admin/verify", 'admin_verify',
                 admin_verify, methods=['GET'])
app.add_url_rule("/admin/approve", 'admin_approve',
                 admin_approve, methods=['GET', 'POST'])


if __name__ == "__main__":
    makeMap()
    app.run("0.0.0.0", port=7879, debug=True)
