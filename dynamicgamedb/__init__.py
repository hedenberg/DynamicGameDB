from dynamicgamedb.backend import backend
from dynamicgamedb.frontend import frontend
from flask import Flask
from werkzeug.debug import DebuggedApplication
import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')

app = Flask(__name__, static_folder=ASSETS_DIR)

app.debug = True
app.secret_key = 'I like turtles'
app.register_blueprint(backend)
app.register_blueprint(frontend)

app.wsgi_app = DebuggedApplication(app.wsgi_app)

import frontend
import backend