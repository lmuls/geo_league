from service import service
import database.schemas as schemas
from database.models import Game, Round, Score, Player
from database.database import SessionLocal


def parse(data: list[dict], game_information: dict, db: SessionLocal):
    if len(data) == 0:
        raise Exception("Empty input data array")
    if len(game_information) == 0:
        raise Exception("Empty game data")

    game = db.query(Game).filter(Game.id == game_information.get("game_id")).first()

    if game is None:
        create_game = schemas.GameCreate(id=game_information.get("game_id"), map=data[1]['game']['map'], map_name=data[1]['game']['mapName'], round_count=data[1]['game']['roundCount'],
                                         time_limit=data[1]['game']['timeLimit'],
                                         date=game_information.get("date"))
        game = service.create_game(db, create_game)

    for result in data:
        if len(result) == 0:
            # TODO implement logging
            continue

        player_name = result.get("playerName")
        existing_player = db.query(Player).filter(Player.name == player_name).first()
        if existing_player is None:
            player = service.create_player(db, schemas.PlayerCreate(name=player_name))
        else:
            player = existing_player

        round_number = 1
        for round in result["game"]["rounds"]:
            existing_round = db.query(Round).filter(Round.game_id == game.id).filter(Round.round_number == round_number).first()
            if existing_round is None:
                service.create_round(db, schemas.RoundCreate(game_id=game.id, round_number=round_number, lat=round.get("lat"), lng=round.get("lng")))
            round_number += 1

        guess_number = 1
        for guess in result["game"]["player"]["guesses"]:
            existing_guess = db.query(Score).join(Round).filter(Score.player_id == player.id).filter(Round.game_id == game.id).filter(Round.round_number == guess_number).first()
            equivalent_round = db.query(Round).filter(Round.game_id == game.id).filter(Round.round_number == guess_number).first()
            if existing_guess is None:
                service.create_score(db, schemas.ScoreCreate(round_id=equivalent_round.id, player_id=player.id, lat=guess["lat"], lng=guess["lng"], timed_out=guess["timedOut"],
                                                             timed_out_with_guess=guess["timedOutWithGuess"], round_score_points=guess["roundScoreInPoints"],
                                                             round_score_percentage=guess["roundScoreInPercentage"], distance_meters=guess["distanceInMeters"], time=guess["time"]))
            guess_number += 1
