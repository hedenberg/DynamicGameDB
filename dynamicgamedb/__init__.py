from dynamicgamedb.backend import backend, oid
from dynamicgamedb.frontend import frontend
from flask import Flask
from werkzeug.debug import DebuggedApplication
import os
#from dynamicgamedb.frontend.views.user import create_app


#ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')

#app = Flask(__name__, static_folder=ASSETS_DIR)
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')
app = Flask(__name__, static_folder=ASSETS_DIR)
oid.init_app(app)

#app= create_app()

app.debug = True
app.secret_key = 'I like turtles'
app.register_blueprint(backend)
app.register_blueprint(frontend)

app.wsgi_app = DebuggedApplication(app.wsgi_app)

#import frontend
#import backend