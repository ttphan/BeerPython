import pytest
from sqlalchemy import create_engine
import db
from model import model
from model.model import *
from db import Session, sessionScope
from sqlalchemy.exc import IntegrityError
import pdb

import inspect, os


@pytest.yield_fixture(scope="module")
def connection():
    # in-memory sqlite database
    engine = create_engine('sqlite://')

    # Create tables
    model.Base.metadata.create_all(engine)

    # Establish connection, reconfigure session to use the test db
    connection = engine.connect()
    db.Session.configure(bind = connection)
    model.Base.metadata.bind = engine

    yield connection

    # Teardown
    model.Base.metadata.drop_all()


@pytest.yield_fixture
def db_session(connection):
    transaction = connection.begin()
    with sessionScope() as session:
        yield session

        # Teardown
        transaction.rollback()
        session.close()

def test_db_sanity_check(db_session):
    db_session.add(Member(name = 'foobar'))

    assert db_session.query(Member).count() == 1


def test_db_sanity_check_rollback(db_session):
    assert db_session.query(Member).count() == 0

class TestTally:
    def test_add_tally(self, db_session):
        testList = List()
        testMember1, testMember2 = Member(name = 'foo'), Member(name = 'bar')

        db_session.add(testList)
        db_session.commit()

        # Add tally
        Tally(testMember1, db_session)

        assert len(testMember1.tallies) == 1 
        assert len(testMember2.tallies) == 0
        assert db_session.query(Tally).count() == 1
        assert db_session.query(Tally).get(1).listId == 1

        # Add some more
        Tally(testMember1, db_session)
        Tally(testMember2, db_session)

        assert len(testMember1.tallies) == 2
        assert len(testMember2.tallies) == 1
        assert db_session.query(Tally).count() == 3

class TestList:
    def test_tally_list_dependency_exception(self, db_session):
        db_session.add(Tally(Member(name = 'foo'), db_session))

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()

    def test_add_tally_to_list(self, db_session):
        testList = List()
        testMember = Member(name = 'foo')

        # Add list to active session, sanity check
        db_session.add(testList)
        db_session.commit()
        assert db_session.query(List).count() == 1

        # Add tallies to newest list
        Tally(testMember, db_session)
        Tally(testMember, db_session)

        assert len(db_session.query(List).get(1).tallies) == 2

        # Create new list, should add new tallies to new list
        newList = List()
        db_session.add(newList)
        db_session.commit()
        assert db_session.query(List).count() == 2

        Tally(testMember, db_session)        
        Tally(testMember, db_session)
        Tally(testMember, db_session)

        assert len(db_session.query(List).get(1).tallies) == 2
        assert len(db_session.query(List).get(2).tallies) == 3