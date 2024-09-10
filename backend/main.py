import datetime
import json

import uvicorn
from fastapi import FastAPI, Depends, Form, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from typing import Annotated


from database import models, schemas
from service import service
from batch.parse_html import parse

from database.database import SessionLocal, engine
from database.schemas import Game, GameInformation, Leaderboard, Player

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db()


@app.get("/players", response_model=list[schemas.Player])
def get_players(db: Session = Depends(get_db)):
    return service.get_players(db=db)


@app.get("/players/{player_id}", response_model=schemas.Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player: Player = service.get_player(db=db, id=player_id)
    return player


@app.get("/leaderboard/", response_model=Leaderboard)
def get_leaderboard(db: Session = Depends(get_db)):
    return service.get_leaderboard(db)


@app.get("/delete-game/{game_id}", status_code=status.HTTP_200_OK)
def delete_game(game_id: str, db: Session = Depends(get_db)):
    return service.delete_game(db, game_id)


@app.post("/new-game/")
async def new_game(file: UploadFile = File(), date: datetime.date = Form(), db: Session = Depends(get_db)):    
    parsed = parse(file.file.read())
    game_id = parsed[0]
    map_name = parsed[1]
    results = parsed[2]
    
    game = db.query(models.Game).filter(models.Game.id == game_id).first()

    if game is None:
        create_game = schemas.GameCreate(id=game_id, map_name=map_name, date=date)
        game = service.create_game(db, create_game)
        
    for result in results:
        player_name = result[0]
        player = db.query(models.Player).filter(models.Player.name == player_name).first()
        if player is None:
            player = service.create_player(db, schemas.PlayerCreate(name=player_name))

        score = db.query(models.Score).filter(models.Score.game_id == game.id).filter( models.Score.player_id == player.id).first()
        if score is None:
            service.create_score(db, schemas.ScoreCreate(game_id=game_id, player_id=player.id, score=result[1]))
        else:
            score.score = result[1]
    
    db.commit()
    
    # with open(file.file.read, "r") as f:
    #     print(f.readlines())
    # print(file.file.)
    return {"filename": file.filename}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
