from sqlalchemy import Column
from sqlalchemy import Column, Integer, String
from include.models.db import Base

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    primary_color = Column(String)