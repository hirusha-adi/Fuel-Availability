from flask import render_template
from flask import url_for
from flask import redirect
from flask import request

from database.mongo import Stations


def check_mobile(request):
    user_agent = request.headers.get('User-Agent').lower()
    if ("iphone" in user_agent) or ("android" in user_agent):
        return True
    else:
        return False


def map():
    return render_template("map.html")


def map_petrol():
    return render_template("map_petrol.html")


def map_diesel():
    return render_template("map_diesel.html")


def amounts_no_id():
    mobile = check_mobile(request=request)
    stations = Stations.getAllStations()
    if len(stations) <= 0:
        return render_template("amounts.html", data={}, mobile=mobile, empty=True)
    return redirect(url_for('map'))


def amounts(id):
    data = Stations.getByID(id=id)
    mobile = check_mobile(request=request)
    return render_template("amounts.html", data=data, mobile=mobile, empty=False)
