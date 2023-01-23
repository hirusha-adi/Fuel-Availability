from flask import render_template
from flask import url_for
from flask import request

from database.mongo import Stations


def map():
    return render_template("map.html")


def map_petrol():
    return render_template("map_petrol.html")


def map_diesel():
    return render_template("map_diesel.html")


def amounts_no_id():
    "return no stations if none"
    "return the first station if no val and have stations"
    return url_for('amounts', id='1')


def amounts(id):
    data = Stations.getByID(id=id)
    user_agent = request.headers.get('User-Agent').lower()
    if ("iphone" in user_agent) or ("android" in user_agent):
        mobile = True
    else:
        mobile = False
    return render_template("amounts.html", data=data, mobile=mobile)
