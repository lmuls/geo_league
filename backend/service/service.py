from sqlalchemy.orm import Session

from database import models, schemas
from database.models import Player, Score, Round, Game
from database.schemas import Leaderboard, PlayerResult, GameResult


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
        scores = db.query(Score).filter(Score.player_id == player.id).all()

        points = 0
        for score in scores:
            points += score.round_score_points
        games: list[Game] = db.query(Game).join(Round).join(Score).filter(Score.player_id == player.id).all()

        game_results: list[GameResult] = []
        for game in games:
            scores: list[Score] = db.query(Score).join(Round).filter(Round.game_id == game.id).filter(Score.player_id == player.id).all()
            rounds = []
            game_points = 0
            for score in scores:
                rounds.append(score)
                game_points += score.round_score_points

            game_results.append(GameResult(id=game.id, rounds=rounds, map_name=game.map_name, points=game_points, date=game.date))
        game_results.sort(key=lambda x: x.points, reverse=True)
        res.players.append(PlayerResult(name=player.name, points=points, games=game_results))
    res.players.sort(key=lambda x: x.points, reverse=True)
    return res


def delete_game(db: Session, game_id: str):
    game_to_delete = db.query(Game).filter(Game.id == game_id).first()
    db.delete(game_to_delete)
    db.commit()

    players: list[Player] = db.query(Player).all()
    for player in players:
        if len(player.scores) == 0:
            db.delete(player)
    db.commit()
