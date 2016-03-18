from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Room(Base):
    """
    Stores which rooms are occupied by which member. 
    Default is 18 rooms with 3 spots for externs.
    """

    __tablename__ = 'Room'
    roomNumber = Column(Integer, primary_key = True)

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

    __tablename__ = 'List'
    id = Column(Integer, primary_key = True)
    date = Column(DateTime, default = datetime.utcnow())

    # one-to-many
    tallies = relationship('Tally',
        cascade = 'all',
        backref = 'list'
    )


class Tally(Base):
    "The tallies, coupled to a List."

    __tablename__ = 'Tally'
    id = Column(Integer, primary_key = True)
    memberId = Column(Integer, ForeignKey('Member.id'), nullable = False)
    listId = Column(Integer, ForeignKey('List.id'), nullable = False)
    date = Column(DateTime, default = datetime.utcnow())


class Member(Base):
    "Tally member, can either be a housemate or an extern person."

    __tablename__ = 'Member'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    roomId = Column(Integer)
    date = Column(DateTime, default = datetime.utcnow())

    # one-to-many
    tallies = relationship('Tally', 
        cascade = 'all',
        backref = 'member'
    )