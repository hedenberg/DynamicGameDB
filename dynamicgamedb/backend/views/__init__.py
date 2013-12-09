from dynamicgamedb.backend.database import db_session
from dynamicgamedb.backend import backend

@backend.teardown_app_request
def shutdown_session(exception=None):
    db_session.remove()

from dynamicgamedb.backend.views import misc, platform, game, relation, user