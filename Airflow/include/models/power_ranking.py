from sqlalchemy import Column, Integer, String
from include.models.db import Base

class PowerRanking(Base):
    __tablename__ = 'power_ranking'

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    points = Column(Integer)
    score_differential = Column(Integer)
    rank = Column(Integer)