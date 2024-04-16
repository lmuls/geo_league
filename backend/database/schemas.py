import datetime

from pydantic import BaseModel


class GameBase(BaseModel):
    id: str
    map: str
    map_name: str
    round_count: int
    time_limit: int
    date: datetime.date


class GameCreate(GameBase):
    pass


class Game(GameBase):
    pass

    class Config:
        orm_mode = True

class ScoreBase(BaseModel):
    game_id: str
    player_id: int
    score: int
    meta: str


class ScoreCreate(ScoreBase):
    pass


class Score(ScoreBase):
    id: int
    game: Game

    # player: Player

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    scores: list[Score] = []
    games: list[Game] = []

    class Config:
        orm_mode = True


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
