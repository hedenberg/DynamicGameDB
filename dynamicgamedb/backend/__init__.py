from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask.ext.openid import OpenID
from functools import wraps

oid = OpenID( '../openid')

class BackendBlueprint(Blueprint):
    def require_client(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.api_client:
                return """{"error":"No valid client"}"""
            return f(*args, **kwargs)
        return decorated_function

    def require_user(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user:
                return """{"error":"Not logged in"}"""
            return f(*args, **kwargs)
        return decorated_function


backend = BackendBlueprint('backend', __name__,
                    template_folder='templates')

from dynamicgamedb.backend.database import init_db
init_db()
import dynamicgamedb.backend.views