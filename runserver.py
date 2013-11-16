from dynamicgamedb.backend import backend
from flask import Flask

app = Flask(__name__)

app.debug = True
app.secret_key = 'I like turtles'
app.register_blueprint(backend)
app.run()