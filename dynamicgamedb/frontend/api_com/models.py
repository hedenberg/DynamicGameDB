
class DGDB_Error(Exception):
    def __init__(self, type, message):
        print "DBDB_error init"
        Exception.__init__(self, message)
        self.type = type

class User(object):
    def __init__(self, email):
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return User(email = data.get("user_email"))

class Game(object):
    def __init__(self, id, title, platform=None, platform_id=None, info=None, picture=None, release_date=None, developer=None, publisher=None, edited_by=None, relations=None):
        self.id = id
        self.title = title
        self.platform = platform
        self.platform_id = platform_id
        self.info = info
        self.picture = picture
        self.release_date = release_date
        self.developer = developer
        self.publisher = publisher
        self.edited_by = edited_by
        self.relations = relations

    @classmethod
    def from_dict(cls, data):
        return Game(id = int(data.get("game_id")),
                    title = data.get("game_title"),
                    platform = data.get("platform"),
                    platform_id = int(data.get("platform_id")),
                    info = data.get("info"),
                    picture = data.get("picture"),
                    release_date = str(data.get("release_date")),
                    developer = data.get("developer"),
                    publisher = data.get("publisher"),
                    edited_by = data.get("edited_by"),
                    relations = data.get("relations")) 

class Platform(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return Platform(id = int(data.get("platform_id")),
                        name = str(data.get("platform_name")))

class Relation(object):
    def __init__(self, g1_id, g2_id):
        self.g1_id = g1_id
        self.g2_id = g2_id

    @classmethod
    def from_dict(cls, data):
        return Relation(id = int(data.get("relation_id")),
                        g1_id = int(data.get("g1_id")),
                        g2_id = int(data.get("g2_id")))


class GameRelation(object):
    def __init__(self, id, title, platform=None, platform_id=None, info=None, picture=None, release_date=None, developer=None, publisher=None, edited_by=None, relation_count=None):
        self.id = id
        self.title = title
        self.platform = platform
        self.platform_id = platform_id
        self.info = info
        self.picture = picture
        self.release_date = release_date
        self.developer = developer
        self.publisher = publisher
        self.edited_by = edited_by
        self.relation_count = relation_count

    @classmethod
    def from_dict(cls, data):
        return GameRelation(id = int(data.get("game_id")),
                            title = data.get("game_title"),
                            platform = data.get("platform"),
                            platform_id = int(data.get("platform_id")),
                            info = data.get("info"),
                            picture = data.get("picture"),
                            release_date = str(data.get("release_date")),
                            developer = data.get("developer"),
                            publisher = data.get("publisher"),
                            edited_by = data.get("edited_by"),
                            relation_count = int(data.get("relation_count"))) 