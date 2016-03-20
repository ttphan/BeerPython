from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, desc
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from datetime import datetime
from sqlalchemy import func
import bcrypt
import pdb

class BaseMixin(object):
    "Mixin to cut down on boiler-plate code"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default = datetime.utcnow())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

Base = declarative_base(cls=BaseMixin)


tallyTypeList = Table('TallyTypeList', Base.metadata,
    Column('listId', Integer, ForeignKey('List.id')),
    Column('tallyTypeId', Integer, ForeignKey('TallyType.id'))
)

class Password(Base):
    password = Column(String)

    def __init__(self, plaintext):
        self.password = bcrypt.hashpw(plaintext.encode('utf-8'), bcrypt.gensalt())
    

class Room(Base):
    """
    Stores which rooms are occupied by which member. 
    Default is 18 rooms with 3 spots for externs.
    """

    # one-to-one
    member = relationship('Member',
        uselist = False,
        backref = 'room'
    )


class List(Base):
    """
    List which can be opened and closed in order to generate a report and
    to reset the tallies to 0.
    """

    # one-to-many
    tallies = relationship('Tally', backref = 'list')

    # many-to-many
    tallyTypes = relationship('TallyType', secondary = tallyTypeList)


class TallyType(Base):
    "Tally types to differentiate from the standard beer tallies"

    label = Column(String, nullable = False)

    # one-to-many
    tallies = relationship('Tally', backref = 'tallyType')


class Tally(Base):
    "The tallies, coupled to a List."

    memberId = Column(Integer, ForeignKey('Member.id'), nullable = False)
    listId = Column(Integer, ForeignKey('List.id'), nullable = False)
    tallyTypeId = Column(Integer, ForeignKey('TallyType.id'), nullable = False)

    def __init__(self, member, session, tallyType = None):
        # Temporarily disable auto flush, so we can get the latest list and tally type
        session.autoflush = False

        self.member = member
        self.list = session.query(List).order_by(desc(List.id)).first()
        if tallyType == None:
            tallyType = 'Beer'
            
        self.tallyType = session.query(TallyType).filter_by(label = tallyType).first()

        session.autoflush = True



class Member(Base):
    "Tally member, can either be a housemate or an extern person."

    name = Column(String, nullable = False)
    roomId = Column(Integer, ForeignKey('Room.id'))

    # one-to-many
    tallies = relationship('Tally', backref = 'member')

    def __init__(self, name):
        self.name = name

    def getTotalTallies(self, session, listId = None):
        if listId == None:
            listId = session.query(List).order_by(desc(List.id)).first().id

        return (
            session.query(Tally, Member, List)
            .join(Member)
            .join(List)
            .filter(Member.id == self.id)
            .filter(List.id == listId)
            .count()
        )

    def addTally(self, session, amount = 1, tallyType = None):
        for _ in range(amount):
            session.add(Tally(self, session, tallyType))