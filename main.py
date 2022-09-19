from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import models, service, schemas
from database.batch import import_data
from database.database import SessionLocal, engine
from database.schemas import Player, GameInformation, Leaderboard

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/players/{player_id}", response_model=schemas.Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player: Player = service.get_player(db=db, id=player_id)
    return player


@app.get("/players", response_model=list[schemas.Player])
def get_players(db: Session = Depends(get_db)):
    return service.get_players(db=db)


@app.post("/new-game/", status_code=status.HTTP_201_CREATED)
def post_game(game_information: GameInformation, db: Session = Depends(get_db)):
    try:
        import_data(game_information, db)
    except:
        raise HTTPException(status_code=500, detail="Some server error, not good...")


@app.get("/leaderboard/", response_model=Leaderboard)
def get_leaderboard(db: Session = Depends(get_db)):
    return service.get_leaderboard(db)
