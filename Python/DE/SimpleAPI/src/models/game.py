from datetime import date
from pydantic import BaseModel

class Game(BaseModel):
    game_date: date
    home_team_id: int
    home_team_score: int
    away_team_id: int
    away_team_score: int