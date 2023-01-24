import os
from datetime import datetime

from flask import Flask

from database.mongo import Users
from database.settings import flaskSecret
from database.settings import uploadPath
from database.settings import WebServer

from routes.general import *
from routes.stations import *
from routes.users import *
from routes.admin import *

# Initialize flask app
app = Flask(__name__)

# Set up flask app config
app.secret_key = flaskSecret
app.config['UPLOAD_FOLDER'] = uploadPath

# Keep track of number of unique visitiors
uniqueVisitors = set()


@app.before_request
def check_user():
    # handle and check if user is logged in
    g.user = None
    if 'user_id' in session:
        user = Users.getUserByID(id=session['user_id'])
        g.user = user


@app.before_request
def log_requests():
    """
    Both log every request made and log all unique visitors by IP

    Structure of log of all requests ->
        {time} - {ip} - {user agent} - {route}

    Structure of log of unique visitors ->
        {time} - {ip} - {user agent}
    """
    now = datetime.now()
    ip = request.remote_addr

    # Log - All
    with open(now.strftime("logs/all_%Y_%m_%d.log"), "a") as f:
        f.write("{} - {} - {} - {}\n".format(
            now,
            ip,
            request.user_agent,
            request.path
        ))

    # Log - Unique Visitors
    if not (ip in uniqueVisitors):
        # If IP is not in our set, then proceed
        uniqueVisitors.add(ip)
        with open(now.strftime("logs/unique_%Y_%m_%d.log"), "a") as f:
            f.write("{} - {} - {}\n".format(
                now,
                ip,
                request.user_agent
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
app.add_url_rule("/edit/user", 'panel_edit_user', panel_edit_user, methods=['GET', 'POST'])
app.add_url_rule("/edit/station", 'panel_edit_station', panel_edit_station, methods=['GET', 'POST'])
app.add_url_rule("/add/station", 'add_new_station', add_new_station, methods=['GET', 'POST'])

# Admin
app.add_url_rule("/admin", 'admin_home', admin_home, methods=['GET'])
app.add_url_rule("/admin/panel", 'admin_panel', admin_panel, methods=['GET'])
app.add_url_rule("/admin/update", 'admin_update', admin_update, methods=['GET'])
app.add_url_rule("/admin/verify", 'admin_verify', admin_verify, methods=['GET'])
app.add_url_rule("/admin/approve", 'admin_approve', admin_approve, methods=['GET', 'POST'])


def runApp():
    # create the logs folder if it doesnt exist
    if not (os.path.isdir(os.path.join(os.getcwd(), "logs"))):
        os.makedirs("logs")

    # generate the map inititally before starting web app
    makeMap()

    # display web server stats
    _host = f"{'localhost' if (WebServer.host == '0.0.0.0') or (WebServer.host == '127.0.0.1') else WebServer.host}:{WebServer.port}"
    print(f"[*] The server is running on:\n\t-> http://{_host}/")

    # start the flask app
    app.run(
        WebServer.host,
        port=WebServer.port,
        debug=WebServer.debug
    )


if __name__ == "__main__":
    runApp()
