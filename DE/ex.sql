-- 1
WITH team_stats AS (
    SELECT
        team.id AS team_id,
        team.name AS team_name,
		team.primary_color AS primary_color,
        COUNT(
			CASE 
				WHEN (g.home_team_id = team.id AND g.home_team_score > g.away_team_score)
                	OR (g.away_team_id = team.id AND g.away_team_score > g.home_team_score)
                THEN 1 
			END
		) AS wins
    FROM teams AS team
    JOIN games AS g ON team.id IN (g.home_team_id, g.away_team_id)
    GROUP BY team.id
)

SELECT primary_color, AVG(wins)
FROM team_stats
GROUP BY primary_color
;

-- 2
SELECT *
FROM games
ORDER BY (home_team_score + away_team_score) DESC
LIMIT 1
;

-- 3
WITH team_stats AS (
    SELECT
        team.id AS team_id,
        team.name AS team_name,
		team.primary_color AS primary_color,
        COUNT(
			CASE 
				WHEN g.home_team_score > g.away_team_score
                THEN 1
			END
		) AS wins
    FROM teams AS team
    JOIN games AS g ON team.id = g.home_team_id
    GROUP BY team.id
)

SELECT team_id
FROM team_stats
ORDER BY wins DESC
LIMIT 1
;

-- 4
SELECT
	team.id AS team_id,
	team.name AS team_name,
	team.primary_color AS primary_color,
	SUM(
		CASE 
			WHEN g.home_team_id = team.id THEN g.home_team_score
			WHEN g.away_team_id = team.id THEN g.away_team_score
		END
	) AS score
FROM teams AS team
JOIN games AS g ON team.id IN (g.home_team_id, g.away_team_id)
GROUP BY team.id
;

-- 5
WITH team_stats AS (
    SELECT
        team.id AS team_id,
        team.name AS team_name,
		date_part('year', g.game_date) AS year,
		team.primary_color AS primary_color,
        COUNT(
			CASE 
				WHEN (g.home_team_id = team.id AND g.home_team_score > g.away_team_score)
                	OR (g.away_team_id = team.id AND g.away_team_score > g.home_team_score)
                THEN 1 
			END
		) AS wins
    FROM teams AS team
    JOIN games AS g ON team.id IN (g.home_team_id, g.away_team_id)
    GROUP BY team.id, date_part('year', g.game_date)
),
team_wins_diff AS (
	SELECT *,
		wins - LAG(wins, 1, 0) OVER (
			PARTITION BY team_id
			ORDER BY year
		) AS diff
	FROM team_stats
)

SELECT *
FROM team_wins_diff
ORDER BY diff DESC
LIMIT 1
;

-- 6
SELECT *
FROM games
ORDER BY ABS(home_team_score - away_team_score) DESC
LIMIT 1
;

-- 7
SELECT
	team.id AS team_id,
	team.name AS team_name,
	team.primary_color AS primary_color,
	COUNT(
		CASE 
			WHEN g.home_team_id = team.id AND g.home_team_score > g.away_team_score
			THEN 1
		END
	) AS home_wins
FROM teams AS team
JOIN games AS g ON team.id = g.home_team_id
GROUP BY team.id
ORDER BY home_wins DESC
LIMIT 1
;

-- 8
WITH team_stats AS (
    SELECT
        team.id AS team_id,
        team.name AS team_name,
		team.primary_color AS primary_color,
        COUNT(
			CASE 
				WHEN (g.home_team_id = team.id AND g.home_team_score > g.away_team_score)
                	OR (g.away_team_id = team.id AND g.away_team_score > g.home_team_score)
                THEN 1 
			END
		) AS wins,
		COUNT(*) AS games
    FROM teams AS team
    JOIN games AS g ON team.id IN (g.home_team_id, g.away_team_id)
    GROUP BY team.id
)

SELECT *, (100 * wins / games) AS "wins %"
FROM team_stats
;

-- 9
WITH team_stats AS (
    SELECT
        team.id AS team_id,
        team.name AS team_name,
		team.primary_color AS primary_color,
        COUNT(
			CASE 
				WHEN g.home_team_score > g.away_team_score
                THEN 1
			END
		) AS losses
    FROM teams AS team
    JOIN games AS g ON team.id = g.away_team_id
    GROUP BY team.id
)

SELECT team_id
FROM team_stats
ORDER BY losses DESC
LIMIT 1
;

-- 10
SELECT
	team.id AS team_id,
	team.name AS team_name,
	team.primary_color AS primary_color,
	COUNT(
		CASE 
			WHEN g.home_team_id = team.id AND g.home_team_score > g.away_team_score
			THEN 1
		END
	) AS home_wins,
	COUNT(
		CASE 
			WHEN g.away_team_id = team.id AND g.home_team_score < g.away_team_score
			THEN 1
		END
	) AS away_wins
FROM teams AS team
JOIN games AS g ON team.id IN (g.home_team_id, g.away_team_id)
GROUP BY team.id
;