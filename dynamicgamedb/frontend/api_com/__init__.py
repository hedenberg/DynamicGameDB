import urllib
import httplib2
import json

from dynamicgamedb.frontend.api_com.models import Game

class DynamicGameDB(object):

    #def __init__(self):
        #

    def games(self):
        response, content = self.request("/games")
        if not response.status == 200:
            pass
            #Should probably handle error
        return [Game.from_dict(game) for game in json.loads(content).get("games")]

    def game(self, id):
        response, content = self.request("/game/%d"%id)
        if not response.status == 200:
            print "/game/id/ error"
            pass
        return Game.from_dict(json.loads(content))

    def request(self, endpoint):
        http = httplib2.Http()
        response, content = http.request("http://127.0.0.1:8000/api"+endpoint,
                                         method="GET",
                                         headers=dict(),
                                         body=None)
        return response, content