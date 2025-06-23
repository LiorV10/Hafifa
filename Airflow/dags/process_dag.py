from airflow import DAG
from airflow.sdk import task
from sqlalchemy.orm import Session
from sqlalchemy import text
from include.models import Base, engine
from include.models import Game
from dataset import dataset

with DAG(
    dag_id='process_dag',
    schedule=[dataset]
) as dag:
    @task
    def rank():
        with Session(engine) as session:
            session.execute(text(
                '''
DELETE FROM power_ranking;

BEGIN;

WITH team_stats AS (
    SELECT
        team.id AS team_id,
        team.name AS team_name,
        COUNT(CASE WHEN (g.home_team_id = team.id AND g.home_team_score > g.away_team_score)
                    OR (g.away_team_id = team.id AND g.away_team_score > g.home_team_score)
                    THEN 1 END) AS wins,
        COUNT(CASE WHEN (g.home_team_id = team.id AND g.home_team_score < g.away_team_score)
                    OR (g.away_team_id = team.id AND g.away_team_score < g.home_team_score)
                    THEN 1 END) AS losses,
        SUM(
            CASE
                WHEN g.home_team_id = team.id THEN g.home_team_score - g.away_team_score
                WHEN g.away_team_id = team.id THEN g.away_team_score - g.home_team_score
                ELSE 0
            END
        ) AS score_differential
    FROM teams AS team
    JOIN games AS g ON team.id IN (g.home_team_id, g.away_team_id)
    GROUP BY team.id
),
final_ranking AS (
    SELECT
        team_id,
        team_name,
        wins,
        losses,
        (wins * 2 + losses) AS points,
        score_differential,
        RANK() OVER (
            ORDER BY (wins * 2 + losses) DESC, score_differential DESC, team_id
        ) AS rank
    FROM team_stats
)

INSERT INTO power_ranking (rank, team_id, team_name, wins, losses, points, score_differential)
SELECT rank, team_id, team_name, wins, losses, points, score_differential
FROM final_ranking
ORDER BY rank;

COMMIT;
'''
            ))

    rank()