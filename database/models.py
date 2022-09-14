from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, index=True)
    map = Column(String)
    map_name = Column(String)
    round_count = Column(Integer)
    time_limit = Column(Integer)

    # description = Column(String, index=True)
    # owner_id = Column(Integer, ForeignKey("users.id"))
    #
    # owner = relationship("User", back_populates="items")


class Coordinate:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y
