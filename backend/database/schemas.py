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


class RoundBase(BaseModel):
    game_id: str
    round_number: int
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


class RoundResult(BaseModel):
    scores = list[Score]


class GameResult(BaseModel):
    id: str
    rounds: list[Score]
    map_name: str
    points: int
    date: datetime.date


class PlayerResult(BaseModel):
    name: str
    points: int
    games: list[GameResult]


class Leaderboard(BaseModel):
    players: list[PlayerResult]
