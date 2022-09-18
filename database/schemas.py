import datetime

from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    map: str
    map_name: str
    round_count: int
    round_limit: int
    time_limit: int
    date: datetime.date


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int

    class Config:
        orm_mode = True


class RoundBase(BaseModel):
    map: str
    game_id: int
    lat: float
    lng: float


class RoundCreate(RoundBase):
    pass


class Round(RoundBase):
    id: int
    game: Game

    class Config:
        orm_mode = True


class ScoreBase(BaseModel):
    round_id: int
    player_id: int
    lat: float
    lng: float
    timed_out: bool
    timed_out_with_guess: bool
    round_score_points: int
    round_score_percentage: float
    distance_meters: float
    time: int


class ScoreCreate(ScoreBase):
    pass


class Score(ScoreBase):
    id: int
    round: Round
    player: Player

    class Config:
        orm_mode = True
