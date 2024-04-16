import json

import os
import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base

from geo_league_vars import BASE_DIR

from service.service import *
from database import models

from test_data.provider import get_local_test_data, get_local_test_data_2, get_html_test_data
from batch.parse_html import parse

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


data, game_information = get_local_test_data()
data2, game_information2 = get_local_test_data_2()



def test_parse_html(session):
    parse(get_html_test_data())
    assert 1 < 0


# def test_parse_handles_empty_input(session):
#     data = []
#     game_information = {}
#     with pytest.raises(Exception):
#         parse(data, game_information, session)

#     new_data = [{}, {}]
#     game_information = {}
#     with pytest.raises(Exception):
#         parse(new_data, game_information, session)


# def test_parse_creates_players(session):
#     parse(data, game_information, session)

#     res: list[Player] = session.query(Player).all()
#     assert len(res) == 5
#     assert len([x for x in res if x.name == "Lmulsnes" or x.name == "Magnus Kongshem"]) == 2
#     res.sort(key=(lambda x: x.name))
#     assert res[0].name == "Kim Sverre Hilton"


# def test_parse_creates_players_handles_duplicates(session):
#     parse(data, game_information, session)
#     parse(data, game_information, session)

#     res: list[Player] = session.query(Player).all()
#     assert len(res) == 5
#     assert len([x for x in res if x.name == "Lmulsnes" or x.name == "Magnus Kongshem"]) == 2
#     res.sort(key=(lambda x: x.name))
#     assert res[0].name == "Kim Sverre Hilton"


# def test_parse_creates_game_handles_duplicates(session):
#     parse(data, game_information, session)
#     parse(data, game_information, session)

#     res: list[Game] = session.query(models.Game).all()

#     assert len(res) == 1
#     assert res[0] is not None
#     assert res[0].id == "LqzTy7nxHCCAMU5I"
#     assert res[0].map_name == "Norway"
#     assert str(res[0].date) == str(datetime.date(2022, 9, 17))


# def test_parse_creates_round_handles_duplicates(session):
#     parse(data, game_information, session)
#     parse(data, game_information, session)

#     res: list[Round] = session.query(models.Round).all()

#     assert res is not None
#     res.sort(key=lambda x: x.round_number)
#     assert len(res) == 5
#     assert res[0].round_number is 1
#     assert res[4].round_number is 5
#     assert res[0].game_id == "LqzTy7nxHCCAMU5I"


# def test_parse_multiple_games(session):
#     parse(data, game_information, session)
#     session.flush()

#     parse(data2, game_information2, session)
#     session.flush()

#     player: Player = session.query(models.Player).first()
#     res: list[Score] = session.query(models.Score).join(models.Round).join(models.Player).filter(models.Player.id == player.id).all()
#     res.sort(key=lambda x: x.round.game_id)

#     assert res is not None
#     assert len(res) == 10
#     assert res[0].round.game.id == "LqzTy7nxHCCAMU5I"
#     assert res[-1].round.game.id == "wmaH8zFegtFblYHJ"


# def test_random_name(session):
#     parse(data, game_information, session)
#     parse(data, game_information, session)

#     my_res: list[Score] = session.query(models.Score).join(models.Round).join(models.Game).join(models.Player).filter(models.Game.id == "LqzTy7nxHCCAMU5I").filter(
#         models.Player.name == "Lmulsnes").all()

#     assert my_res is not None
#     my_res.sort(key=lambda x: x.round.round_number)
#     assert len(my_res) == 5
#     assert my_res[0].round.round_number is 1
#     assert my_res[4].round.round_number is 5
#     assert my_res[0].round.game.id == "LqzTy7nxHCCAMU5I"
#     assert my_res[0].round_score_points == 4994
#     assert my_res[4].round_score_points == 4999
