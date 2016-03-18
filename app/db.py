from model.model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os

Session = scoped_session(sessionmaker())

def initialize():
    basepath = os.path.dirname(__file__)
    f = os.path.abspath(os.path.join(basepath, os.pardir, "data/db.sqlite"))
    engine = create_engine('sqlite:///' + f)

    Base.metadata.create_all(engine)

    Session.configure(bind = engine)

@contextmanager
def sessionScope():
    """
    Session scope
    How to use:
    Class Object1:
        def doSomething(self, session):
            session.query(something).update(somethingelse)
    with sessionScope() as session:
        Object1.doSomething(session)
    """

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()