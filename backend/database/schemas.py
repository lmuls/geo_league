import datetime

from pydantic import BaseModel, ConfigDict


class GameBase(BaseModel):
    id: str
    map_name: str
    date: datetime.date


class GameCreate(GameBase):
    pass


class Game(GameBase):
    model_config = ConfigDict(from_attributes=True)

class ScoreBase(BaseModel):
    game_id: str
    player_id: int
    score: int


class ScoreCreate(ScoreBase):
    pass


class Score(ScoreBase):
    id: int
    game: Game
    model_config = ConfigDict(from_attributes=True)


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    scores: list[Score] = []
    games: list[Game] = []
    model_config = ConfigDict(from_attributes=True)


class GameInformation(BaseModel):
    game_id: str
    date: datetime.date


class GameResult(BaseModel):
    id: str
    map_name: str
    points: int
    date: datetime.date


class PlayerResult(BaseModel):
    name: str
    points: int
    games: list[GameResult]


class Leaderboard(BaseModel):
    players: list[PlayerResult]
