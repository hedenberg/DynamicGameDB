from dynamicgamedb.backend import backend
from dynamicgamedb.backend.database import db_session

@backend.teardown_app_request
def shutdown_session(exception=None):
    db_session.remove()

@backend.route('/', methods=['GET'])
def home():
    print "Katten"
    return "Hello there"
