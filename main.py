from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import models, service, schemas
from database.database import SessionLocal, engine

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
    return service.get_player(db=db, id=player_id)


@app.get("/players", response_model=list[schemas.Player])
def get_players(db: Session = Depends(get_db)):
    return service.get_players(db=db)
