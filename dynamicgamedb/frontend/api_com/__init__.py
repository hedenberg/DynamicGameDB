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

    def add_game(self, title, platform_id):
        game_dict = dict(title=title, platform_id=str(platform_id))
        response, content = self.request("/game/add", method="POST", body=game_dict)
        if not response.status == 200:
            print "/game/add/ error"
            pass
        return Game.from_dict(json.loads(content))


    def request(self, endpoint, method="GET", headers=dict(), body=None):
        http = httplib2.Http()
        if body:
            body=urllib.urlencode(dict([k, v.encode('utf-8')] for k, v in body.items()))
        headers.update({"Content-Type":"application/x-www-form-urlencoded"})
        response, content = http.request("http://http://fierce-wave-8853.herokuapp.com/api"+endpoint,
                                         method=method,
                                         headers=headers,
                                         body=body)
        return response, content