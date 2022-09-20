import json

import os
import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base
from database.models import Round, Score

from database.service import *
from database import models

from database.parse_input import parse

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


def get_local_test_data():
    with open("../database/test_data.json", "rb") as f:
        data = json.load(f)
        game_information = {
            "date": datetime.date(2022, 9, 17),
            "game_id": "LqzTy7nxHCCAMU5I"
        }
        return data, game_information


data, game_information = get_local_test_data()


def test_parse_handles_empty_input(session):
    data = []
    game_information = {}
    with pytest.raises(Exception):
        parse(data, game_information, session)

    new_data = [{}, {}]
    game_information = {}
    with pytest.raises(Exception):
        parse(new_data, game_information, session)


def test_parse_creates_players(session):
    parse(data, game_information, session)

    res: list[Player] = session.query(Player).all()
    assert len(res) == 5
    assert len([x for x in res if x.name == "Lmulsnes" or x.name == "Magnus Kongshem"]) == 2
    res.sort(key=(lambda x: x.name))
    assert res[0].name == "Kim Sverre Hilton"


def test_parse_creates_players_handles_duplicates(session):
    parse(data, game_information, session)
    parse(data, game_information, session)

    res: list[Player] = session.query(Player).all()
    assert len(res) == 5
    assert len([x for x in res if x.name == "Lmulsnes" or x.name == "Magnus Kongshem"]) == 2
    res.sort(key=(lambda x: x.name))
    assert res[0].name == "Kim Sverre Hilton"


def test_parse_creates_game_handles_duplicates(session):
    parse(data, game_information, session)
    parse(data, game_information, session)

    res: list[Game] = session.query(models.Game).all()

    assert len(res) == 1
    assert res[0] is not None
    assert res[0].id == "LqzTy7nxHCCAMU5I"
    assert res[0].map_name == "Norway"
    assert str(res[0].date) == str(datetime.date(2022, 9, 17))


def test_parse_creates_round_handles_duplicates(session):
    parse(data, game_information, session)
    parse(data, game_information, session)

    res: list[Round] = session.query(models.Round).all()

    assert res is not None
    res.sort(key=lambda x: x.round_number)
    assert len(res) == 5
    assert res[0].round_number is 1
    assert res[4].round_number is 5
    assert res[0].game_id == "LqzTy7nxHCCAMU5I"


def test_parse_creates_scores_handles_duplicates(session):
    parse(data, game_information, session)
    parse(data, game_information, session)

    res: list[Score] = session.query(models.Score).join(models.Round).join(models.Game).join(models.Player).filter(models.Game.id == "LqzTy7nxHCCAMU5I").filter(models.Player.name == "Lmulsnes").all()

    assert res is not None
    res.sort(key=lambda x: x.round.round_number)
    assert len(res) == 5
    assert res[0].round.round_number is 1
    assert res[4].round.round_number is 5
    assert res[0].round.game.id == "LqzTy7nxHCCAMU5I"
    assert res[0].round_score_points == 4994
    assert res[4].round_score_points == 4999
