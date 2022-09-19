import os
import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import schemas
from database.database import Base

from database.models import Game, Player, Round, Score
from database.parse_input import parse
from database.service import create_player, get_players, create_game, get_games, create_round, create_score, get_leaderboard
from tests.test_parse_input import get_local_test_data

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
    player = schemas.PlayerCreate(name="Testplayer 1")
    create_player(db=session, player=player)
    assert len(get_players(session)) == 1


def test_create_player_duplicate_names(session):
    player = schemas.PlayerCreate(name="Testplayer 1")
    create_player(db=session, player=player)

    player2 = schemas.PlayerCreate(name="Testplayer 1")
    with pytest.raises(Exception):
        create_player(db=session, player=player2)
    assert len(get_players(session)) == 1


def test_create_games(session):
    game = schemas.GameCreate(id="1x2", map="Norway", map_name="Norway", round_count=5, time_limit=100, date=datetime.date(2022, 9, 17))
    # game2 = GameCreate(map="Europe", map_name="Europe", round_count=2, time_limit=100, date=datetime.date(2022, 9, 16))
    create_game(session, game)
    # create_game(session, game2)

    res = get_games(session)
    assert len(res) == 1
    assert res[0].map == "Norway"
    assert str(res[0].date) == str(datetime.date(2022, 9, 17))


def test_create_rounds(session):
    game = schemas.GameCreate(id="1x2", map="Norway", map_name="Norway", round_count=5, time_limit=100, date=datetime.date(2022, 9, 17))
    game = create_game(session, game)

    create_round(session, schemas.RoundCreate(game_id=game.id, round_number=1, lat=71.11270904541016, lng=31.09112548828125))
    res = session.query(Game).filter(Game.id == game.id).first()
    assert len(res.rounds) == 1
    assert res.rounds[0].lat == 71.11270904541016


def test_create_score(session):
    player = schemas.PlayerCreate(name="Testplayer 1")
    player = create_player(db=session, player=player)
    game = schemas.GameCreate(id="1x2", map="Norway", map_name="Norway", round_count=5, time_limit=100, date=datetime.date(2022, 9, 17))
    game = create_game(session, game)

    round = create_round(session, schemas.RoundCreate(game_id=game.id, round_number=1, lat=71.11270904541016, lng=31.09112548828125))

    score = create_score(session, schemas.ScoreCreate(round_id=round.id, player_id=player.id, lat=71.4520904541016, lng=31.03112548828125, timed_out=False, timed_out_with_guess=False,
                                                      round_score_points=2543, round_score_percentage=0.51, distance_meters=11932, time=100))

    res = session.query(Score).filter(Score.id == score.id).first()

    assert res.round is not None
    assert res.round.lat == 71.11270904541016
    assert res.round.game is not None
    assert res.round.game.map_name == "Norway"
    assert res.player.name == "Testplayer 1"
    assert res.lat == 71.4520904541016


data, game_information = get_local_test_data()


def test_get_leaderboard(session):
    parse(data, game_information, session)

    res = get_leaderboard(session)
    assert res is not None
    assert len(res.players) == 5
    assert res.players[0].games is not None
