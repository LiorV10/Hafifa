SELECT AVG(length) AS AvgLength
FROM (
	SELECT (SUM(Milliseconds) / (1000 * 60)) AS length
	FROM tracks
	GROUP BY AlbumId
)
;
