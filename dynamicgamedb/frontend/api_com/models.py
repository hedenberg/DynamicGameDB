

class Game(object):
    def __init__(self, id, title, platform=None, developer=None):
        self.id = id
        self.title = title
        self.platform = platform
        self.developer = developer

    @classmethod
    def from_dict(cls, data):
        return Game(id = int(data.get("game_id")),
                    title = str(data.get("game_title")),
                    platform = str(data.get("platform")),
                    developer = str(data.get("developer"))) 