from sqlalchemy.orm import Session

from . import models, schemas
from .models import Player, Score, Round, Game
from .schemas import Leaderboard, PlayerResult


def get_player(db: Session, id: int):
    return db.query(models.Player).filter(models.Player.id == id).first()


def get_players(db: Session):
    return db.query(models.Player).all()


def get_game(db: Session, id: int):
    return db.query(models.Game).filter(models.Game.id == id).first()


def get_games(db: Session):
    return db.query(models.Game).all()


def create_player(db: Session, player: schemas.PlayerCreate):
    player = models.Player(name=player.name)
    if db.query(Player).filter(Player.name == player.name).first() is None:
        db.add(player)
        db.commit()
        db.refresh(player)
        return player
    else:
        raise Exception()


def create_game(db: Session, game: schemas.GameCreate):
    game = models.Game(id=game.id, map=game.map, map_name=game.map_name, round_count=game.round_count, time_limit=game.time_limit, date=game.date)
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


def create_round(db: Session, round: schemas.RoundCreate):
    round = models.Round(game_id=str(round.game_id), round_number=round.round_number, lat=round.lat, lng=round.lng)
    db.add(round)
    db.commit()
    db.refresh(round)
    return round


def create_score(db: Session, score: schemas.ScoreCreate):
    score = models.Score(round_id=score.round_id, player_id=score.player_id, lat=score.lat, lng=score.lng, timed_out=score.timed_out, timed_out_with_guess=score.timed_out_with_guess,
                         round_score_points=score.round_score_points, round_score_percentage=score.round_score_percentage, distance_meters=score.distance_meters, time=score.time)
    db.add(score)
    db.commit()
    db.refresh(score)
    return score


def get_leaderboard(db: Session) -> Leaderboard:
    res: Leaderboard = Leaderboard(players=[])
    players: list[Player] = db.query(Player).all()

    for player in players:
        scores = db.query(Score).filter(Score.player_id == player.id)

        points = 0
        for score in scores:
            points += score.round_score_points
        games: list[Game] = db.query(Game).join(Round).join(Score).filter(Score.player_id == player.id).all()

        res.players.append(PlayerResult(name=player.name, points=points, games=games))

    return res
