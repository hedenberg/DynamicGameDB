from flask import Blueprint, render_template, abort, g, session, flash, redirect
from jinja2 import TemplateNotFound
from functools import wraps
from dynamicgamedb.frontend.api_com import DynamicGameDB

CLIENT_ID = 1337
CLIENT_SECRET = "you no take candle"

dgdb = DynamicGameDB(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET)

frontend = Blueprint('frontend', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/dynamicgamedb/frontend/static')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print "frontend login_required"
        if not g.frontend_user:
            flash("You need to be logged in to perform that action", "warning")
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

@frontend.before_request
def set_user():
    g.frontend_user = None
    dgdb.token = None
    if "user_token" in session:
        dgdb.token = session["user_token"]
        try:
            g.frontend_user = dgdb.user()
        except :
            session.pop("user_token", None)
            flash("Login has expired, login again", "warning")

import dynamicgamedb.frontend.views