from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

frontend = Blueprint('frontend', __name__,
                    template_folder='templates',
                    static_folder='/dynamicgamedb/frontend/static')

import dynamicgamedb.frontend.views