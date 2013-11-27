from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from dynamicgamedb.frontend.api_com import DynamicGameDB

dgdb = DynamicGameDB()

frontend = Blueprint('frontend', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/dynamicgamedb/frontend/static')

import dynamicgamedb.frontend.views