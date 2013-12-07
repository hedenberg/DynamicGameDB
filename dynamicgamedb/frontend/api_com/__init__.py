import urllib
import httplib2
import json

from dynamicgamedb.frontend.api_com.models import Game, Platform, Relation, GameRelation

#API_URL = "http://dynamicgamedb.herokuapp.com"
API_URL = "http://localhost:8000"

CLIENT_ID = 1337
CLIENT_SECRET = "you no take candle"

class DynamicGameDB(object):

    # -- Game --

    def games(self,search_term):
        games_dict = dict(search_term=search_term)
        response, content = self.request("/games",  
                                         method="POST",
                                         body=games_dict)
        if not response.status == 200:
            pass
            #Should probably handle error
        print content
        return [Game.from_dict(game) for game in json.loads(content).get("games")]

    def get_games(self):
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

    def edit_game(self, id, title, platform_id, info, picture, release_date, developer, publisher):
        # platform title developer publisher description release_date
        game_dict = dict(title=title, 
                         platform_id=platform_id, 
                         info=info, 
                         picture=picture,
                         release_date=release_date, 
                         developer=developer,
                         publisher=publisher)
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

    
    def game_relations(self,id):
        print "game relation api_com"
        response, content = self.request("/game/%d/relation"%id)
        if not response.status == 200:
            print "/game/id/relation GET error"
            pass
        print content
        return [GameRelation.from_dict(game_relation) for game_relation in json.loads(content).get("relatedgames")]

    def game_relation(self,s_id,t_id):     #s_id = sourceId t_id = targetId
        response,content = self.request("/game/%d/relation/%d"%(s_id,t_id))
        if not response.status == 200:
            print "/game/sId/relation/tId GET error"
            pass
        return GameRelation.from_dict(json.loads(content))

    def add_game_relation(self,s_id,t_id):
        relation_dict = dict(g_id=t_id)
        response, content = self.request("/game/%d/relation"%s_id, method="POST", body=relation_dict)
        if not response.status == 200:
            print "/game/id/relation POST error"
            pass
        return GameRelation.from_dict(json.loads(content))

    # -- Authentication --

    def api_login_url(self):
        return API_URL + "/api/login/" + "?client_id=%s" % CLIENT_ID

    def auth_token(self, one_time_token):
        auth_dict = dict(client_id=str(CLIENT_ID), client_secret=CLIENT_SECRET, one_time_token=str(one_time_token))
        response, content = self.request("/token/", method="POST", body=auth_dict)
        if not response.status == 200:
            print "/token/ POST error"
            pass
        return content

    def user(self, token):
        auth_dict = dict(client_id=str(CLIENT_ID), client_secret=CLIENT_SECRET, one_time_token=str(token))
        response, content = self.request("/user/", method="POST", body=auth_dict)
        if not response.status == 200:
            print "/token/ POST error"
            pass
        return User.from_dict(json.loads(content))

    # -- General --

    def request(self, endpoint, method="GET", headers=dict(), body=None):
        http = httplib2.Http()
        if body:
            body=urllib.urlencode(dict([k, v.encode('utf-8')] for k, v in body.items()))
        headers.update({"Content-Type":"application/x-www-form-urlencoded"})
        response, content = http.request(API_URL+"/api"+endpoint,
                                         method=method,
                                         headers=headers,
                                         body=body)
        return response, content
