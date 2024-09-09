from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    scores = relationship("Score", back_populates="player")

class Game(Base):
    __tablename__ = "game"
    id = Column(String, primary_key=True)
    map_name = Column(String)
    date = Column(Date)
    scores = relationship("Score", back_populates="game", cascade="all, delete-orphan")

class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True)
    game_id = Column(String, ForeignKey("game.id"))
    game = relationship("Game", back_populates="scores")
    player_id = Column(Integer, ForeignKey("player.id"))
    player = relationship("Player", back_populates="scores")
    score = Column(Integer)
