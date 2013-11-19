from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

backend = Blueprint('backend', __name__,
                    template_folder='templates')

from dynamicgamedb.backend.database import init_db
init_db()
import dynamicgamedb.backend.views