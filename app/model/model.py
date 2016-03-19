from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, desc
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from datetime import datetime
from sqlalchemy import func
import pdb

class BaseMixin(object):
    "Mixin to cut down on boiler-plate code"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default = datetime.utcnow())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

Base = declarative_base(cls=BaseMixin)

class Room(Base):
    """
    Stores which rooms are occupied by which member. 
    Default is 18 rooms with 3 spots for externs.
    """

    # one-to-one
    member = relationship('Member',
        uselist = 'False',
        backref = 'room'
    )


class List(Base):
    """
    List which can be opened and closed in order to generate a report and
    to reset the tallies to 0.
    """

    # one-to-many
    tallies = relationship('Tally', backref = 'list')


class Tally(Base):
    "The tallies, coupled to a List."

    memberId = Column(Integer, ForeignKey('Member.id'), nullable = False)
    listId = Column(Integer, ForeignKey('List.id'), nullable = False)

    def __init__(self, member, session):
        # Temporarily disable auto flush, so we can get the latest list
        session.autoflush = False

        self.member = member
        self.list = session.query(List).order_by(desc(List.id)).first()

        session.autoflush = True


class Member(Base):
    "Tally member, can either be a housemate or an extern person."

    name = Column(String, nullable = False)
    roomId = Column(Integer, ForeignKey('Room.id'))

    # one-to-many
    tallies = relationship('Tally', backref = 'member')

    def __init__(self, name):
        self.name = name