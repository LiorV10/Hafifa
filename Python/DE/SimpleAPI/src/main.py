from datetime import date
import random
from typing import List
from dotenv import load_dotenv

load_dotenv(override=True)

from auth import keycloak_config
from models.login_request import LoginRequest
from models import Game, Team
from fastapi import Depends, FastAPI, HTTPException, Request

import requests
import uvicorn
import json
import os

app = FastAPI()

from fastapi_keycloak_middleware import get_user, setup_keycloak_middleware

setup_keycloak_middleware(app, keycloak_config, exclude_patterns=['/login', '/docs'])

@app.get('/')
async def root(request: Request, auth = Depends(get_user)):
    return {
        'msg': 'authorized'
    }

@app.post('/login')
async def login(data: LoginRequest):
    token_url = os.getenv('KEYCLOAK_TOKEN_URL')
    client_id = keycloak_config.client_id
    client_secret = keycloak_config.client_secret

    payload = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': data.username,
        'password': data.password
    }

    response = requests.post(token_url, data=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail='Invalid username or password')

    return json.loads(response.content).get('access_token')

teams = [
    Team(id=1, name="Lions", city="New York", primary_color="Blue"),
    Team(id=2, name="Tigers", city="Chicago", primary_color="Orange"),
    Team(id=3, name="Bears", city="Los Angeles", primary_color="Brown"),
    Team(id=4, name="Wolves", city="Houston", primary_color="Grey"),
    Team(id=5, name="Eagles", city="San Francisco", primary_color="Green"),
]

@app.get('/teams', response_model=List[Team])
async def get_teams(request: Request, auth = Depends(get_user)):
    return teams

@app.get('/games', response_model=List[Game])
async def get_games(request: Request, auth = Depends(get_user)):
    try:
        today = (await request.json())['date']
    except:
        today = date.today()

    num_games = random.randint(1, 3)
    game_list = []
    team_ids = [team.id for team in teams]

    for _ in range(num_games):
        home, away = random.sample(team_ids, 2)

        game = Game(
            game_date=today,
            home_team_id=home,
            home_team_score=random.randint(10, 40),
            away_team_id=away,
            away_team_score=random.randint(10, 40),
        )
        game_list.append(game)
        
    return game_list

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)