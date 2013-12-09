from flask import Blueprint, render_template, abort, g, session, flash, redirect, request
from jinja2 import TemplateNotFound
from functools import wraps
from dynamicgamedb.frontend.api_com import DynamicGameDB

CLIENT_ID = 1337
CLIENT_SECRET = "you no take candle"

dgdb = DynamicGameDB(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET)

class FrontendBlueprint(Blueprint):
    def login_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print "frontend login_required"
            if not g.frontend_user:
                flash("You need to be logged in to perform that action", "warning")
                return redirect("/")
            return f(*args, **kwargs)
        return decorated_function

frontend = FrontendBlueprint('frontend', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/dynamicgamedb/frontend/static')

@frontend.before_request
def set_user():
    if request.endpoint != 'frontend.static':
        g.frontend_user = None
        g.frontend_token = None
        if "user_token" in session:
            g.frontend_token = session["user_token"]
            try:
                g.frontend_user = dgdb.user()
            except :
                session.pop("user_token", None)
                flash("Login has expired, login again", "warning")

import dynamicgamedb.frontend.views