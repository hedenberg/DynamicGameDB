from sqlalchemy import Column, Integer, String
from dynamicgamedb.database import Base

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True)

    def __init__(self, title=None):
        self.title = title

    def __repr__(self):
        return '<Game %r>' % (self.title)