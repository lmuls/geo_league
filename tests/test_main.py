import json

import os
import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from database.database import Base
from database.models import Round, Score, Game

from database.service import *
from database import models

from database.parse_input import parse
from main import app, get_db

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


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_post_game(session):
    response = client.post(
        "/new-game/",
        json={"game_id": "LqzTy7nxHCCAMU5I", "date": "2022-9-16"},
    )
    assert response.status_code == 201
    res: Game = session.query(Game).first()
    assert res is not None
    assert res.map_name == "Norway"
    # assert data is not None


def test_get_leaderboard(session):
    populate_response = client.post(
        "/new-game/",
        json={"game_id": "LqzTy7nxHCCAMU5I", "date": "2022-9-16"},
    )

    assert populate_response.status_code == 201

    response = client.get("/leaderboard/")
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    assert len(data["players"]) == 5
