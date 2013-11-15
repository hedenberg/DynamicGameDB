from dynamicgamedb import app
from dynamicgamedb.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/', methods=['GET'])
def home():
    print "Katten"
    return "Hello there"
