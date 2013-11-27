from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

engine = create_engine('sqlite:///dynamicgame.db', convert_unicode=True)
#engine = create_engine('postgres://jmcqxvdgcsvsyl:BlvratbaAe05GQYS6HQIjX_ZIX@ec2-184-73-254-144.compute-1.amazonaws.com:5432/d10k9sruavbqno', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import dynamicgamedb.backend.model
    Base.metadata.create_all(bind=engine)