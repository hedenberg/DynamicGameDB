from flask import Blueprint, render_template, abort, g, request, Response, jsonify
from jinja2 import TemplateNotFound
from flask.ext.openid import OpenID
from functools import wraps
import json

oid = OpenID( '../openid')

class BackendBlueprint(Blueprint):
    def client_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print "Check if client"
            if not g.backend_client:
                print "No client!"
                response = Response(
                    json.dumps({"error": { "type": "DGDB_API_Exception", "message": "The client was invalid. Contact your code monkey." }}),
                    mimetype="application/json",
                    status=404
                )
                return response
            return f(*args, **kwargs)
        return decorated_function

    def user_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print "Check if backend user"
            if not g.backend_user:
                print "No backend user!"
                return """{"error":"Not logged in"}"""
            return f(*args, **kwargs)
        return decorated_function

    def get_error_response(self, message, type="DGDB_API_Exception", status_code=404):
        response = Response(
            json.dumps({"error": { "type": type, "message": message }}),
            mimetype="application/json",
            status=status_code
        )
        return response


backend = BackendBlueprint('backend', __name__,
                    template_folder='templates')

from dynamicgamedb.backend.database import init_db
init_db()
from dynamicgamedb.backend.database import db_session
import dynamicgamedb.backend.views
from dynamicgamedb.backend.model import User, Client

@backend.before_request
def user_client_auth():
    g.backend_client = None
    g.backend_user = None

    client_id = request.headers.get('client_id', None) or request.args.get('client_id', None)
    client_secret = request.headers.get('client_secret', None) or request.args.get('client_secret', None)

    if client_id and client_secret:
        client = db_session.query(Client).get(client_id)
        if client:
            if client.c_secret == client_secret:
                print "client found"
                g.backend_client = client
            else:
                print "secret didn't match... eh"
                g.backend_client = client
        else:
            print "client not in db"
    else:
        print "client id and secret not in header or else"

    token = request.headers.get('token', None) or request.args.get('token', None)
    if token:
        user = db_session.query(User).filter(User.token.like(token)).first()
        if user:
            g.backend_user = user