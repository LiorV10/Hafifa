from sqlalchemy import Column
from sqlalchemy import Column, Integer, Date
from include.models.db import Base

class Game(Base):
    __tablename__ = 'games'

    game_date = Column(Date, primary_key=True)
    home_team_id = Column(Integer, primary_key=True)
    away_team_id = Column(Integer, primary_key=True)
    home_team_score = Column(Integer)
    away_team_score = Column(Integer)
