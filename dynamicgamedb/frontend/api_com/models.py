

class Game(object):
    def __init__(self, id, title, platform=None, platform_id=None, developer=None):
        self.id = id
        self.title = title
        self.platform = platform
        self.platform_id = platform_id
        self.developer = developer

    @classmethod
    def from_dict(cls, data):
        return Game(id = int(data.get("game_id")),
                    title = data.get("game_title"),
                    platform = str(data.get("platform")),
                    platform_id = int(data.get("platform_id")),
                    developer = str(data.get("developer"))) 

class Platform(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return Platform(id = int(data.get("platform_id")),
                        name = str(data.get("platform_name")))