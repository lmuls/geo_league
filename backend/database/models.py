from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
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
    map = Column(String)
    map_name = Column(String)
    round_count = Column(Integer)
    time_limit = Column(Integer)
    date = Column(Date)
    rounds = relationship("Round", back_populates="game")


class Round(Base):
    __tablename__ = "round"
    id = Column(Integer, primary_key=True)
    round_number = Column(Integer)
    game_id = Column(String, ForeignKey("game.id"))
    game = relationship("Game", back_populates="rounds")
    lat = Column(Float)
    lng = Column(Float)
    scores = relationship("Score", back_populates="round")


class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True)
    round_id = Column(Integer, ForeignKey("round.id"))
    round = relationship("Round", back_populates="scores")
    player_id = Column(Integer, ForeignKey("player.id"))
    player = relationship("Player", back_populates="scores")
    lat = Column(Float)
    lng = Column(Float)
    timed_out = Column(Boolean)
    timed_out_with_guess = Column(Boolean)
    round_score_points = Column(Integer)
    round_score_percentage = Column(Float)
    distance_meters = Column(Float)
    time = Column(Integer)
