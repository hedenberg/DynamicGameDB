import urllib
import httplib2
import json

from dynamicgamedb.frontend.api_com.models import Game, Platform, Relation

#API_URL = "http://dynamicgamedb.herokuapp.com"
API_URL = "http://localhost:8000"

class DynamicGameDB(object):

    # -- Game --

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
        response, content = self.request("/game/add", 
                                         method="POST", 
                                         body=game_dict)
        if not response.status == 200:
            print "/game/add/ error"
            pass
        return Game.from_dict(json.loads(content))

    def edit_game(self, id, title, platform_id, info, release_date, developer):
        # platform title developer publisher description release_date
        game_dict = dict(title=title, 
                         platform_id=platform_id, 
                         info=info, 
                         release_date=release_date, 
                         developer=developer)
        response, content = self.request("/game/%d/edit"%id, 
                                         method="POST",
                                         body=game_dict)
        if not response.status == 200:
            pass
        return Game.from_dict(json.loads(content))


    # -- Platform --

    def platforms(self):
        response, content = self.request("/platforms")
        if not response.status == 200:
            pass
            #Should probably handle error
        return [Platform.from_dict(platform) for platform in json.loads(content).get("platforms")]

    def platform(self, id):
        response, content = self.request("/platform/%d"%id)
        if not response.status == 200:
            print "/game/id/ error"
            pass
        return Platform.from_dict(json.loads(content))

    def add_platform(self, name):
        platform_dict = dict(name=title)
        response, content = self.request("/platform/add", method="POST", body=platform_dict)
        if not response.status == 200:
            print "/game/add/ error"
            pass
        return Platform.from_dict(json.loads(content))

    # -- Relation --

    

    # -- General --

    def request(self, endpoint, method="GET", headers=dict(), body=None):
        http = httplib2.Http()
        if body:
            body=urllib.urlencode(dict([k, v.encode('utf-8')] for k, v in body.items()))
        headers.update({"Content-Type":"application/x-www-form-urlencoded"})
        #response, content = http.request("http://fierce-wave-8853.herokuapp.com/api"+endpoint,
        response, content = http.request(API_URL+"/api"+endpoint,
                                         method=method,
                                         headers=headers,
                                         body=body)
        return response, content
