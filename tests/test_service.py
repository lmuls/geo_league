import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base

from database.schemas import *
from database.service import *

engine = create_engine(os.environ.get("TEST_DB_URL"))
Session = sessionmaker()


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    Base.metadata.create_all(bind=engine)
    yield connection
    Base.metadata.drop_all(bind=engine)
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()


def test_create_player(session):
    player = PlayerCreate(name="Testplayer 1")
    create_player(db=session, player=player)
    assert len(get_players(session)) == 1


def test_create_player_duplicate_names(session):
    player = PlayerCreate(name="Testplayer 1")
    create_player(db=session, player=player)

    player2 = PlayerCreate(name="Testplayer 1")
    with pytest.raises(Exception):
        create_player(db=session, player=player2)
    assert len(get_players(session)) == 1
