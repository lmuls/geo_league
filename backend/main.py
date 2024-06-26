import json

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from typing import Annotated


from database import models, schemas
from service import service
from batch.batch import import_data
from database.database import SessionLocal, engine
from database.schemas import Player, GameInformation, Leaderboard

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://deplo-loadb-50h0hx1kbfw1-4c9f648e705d62b7.elb.us-east-1.amazonaws.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


@app.post("/new-game/", status_code=status.HTTP_201_CREATED)
def post_game(game_information: GameInformation, db: Session = Depends(get_db)):
    try:
        import_data(game_information, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=json.dumps(str(e)))


@app.get("/leaderboard/", response_model=Leaderboard)
def get_leaderboard(db: Session = Depends(get_db)):
    return service.get_leaderboard(db)


@app.get("/delete-game/{game_id}", status_code=status.HTTP_200_OK)
def delete_game(game_id: str, db: Session = Depends(get_db)):
    return service.delete_game(db, game_id)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print(file.file.read())
    # with open(file.file.read, "r") as f:
    #     print(f.readlines())
    # print(file.file.)
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
