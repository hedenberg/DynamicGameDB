from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

backend = Blueprint('backend', __name__,
                    template_folder='templates')

import dynamicgamedb.backend.views