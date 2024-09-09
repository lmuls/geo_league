from sqlalchemy.orm import Session

from database import models, schemas
from database.models import Player, Score, Game
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
    game = models.Game(id=game.id, map_name=game.map_name, date=game.date)
    db.add(game)
    db.commit()
    db.refresh(game)
    return game

def create_score(db: Session, score: schemas.ScoreCreate):
    score = models.Score(game_id=score.game_id, player_id=score.player_id, score=score.score)
    db.add(score)
    db.commit()
    db.refresh(score)
    return score


def get_leaderboard(db: Session) -> Leaderboard:
    res: Leaderboard = Leaderboard(players=[])
    players: list[Player] = db.query(Player).all()

    # TODO Refactor
    for player in players:
        scores = db.query(Score).filter(Score.player_id == player.id).all()

        points = 0
        for score in scores:
            points += score.score
        games: list[Game] = db.query(Game).join(Score).filter(Score.player_id == player.id).all()

        game_results: list[GameResult] = []
        for game in games:
            scores: list[Score] = db.query(Score).filter(Score.game_id == game.id).filter(Score.player_id == player.id).all()
            game_points = 0
            for score in scores:
                game_points += score.score

            game_results.append(GameResult(id=game.id, map_name=game.map_name, points=game_points, date=game.date))
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
