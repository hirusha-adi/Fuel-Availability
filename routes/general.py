from flask import redirect
from flask import render_template

from database.settings import contactEmail


def index():
    return render_template("index.html")


def contact_us():
    return redirect(f'mailto:{contactEmail}')
