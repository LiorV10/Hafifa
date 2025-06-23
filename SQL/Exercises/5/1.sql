SELECT AVG(tracks)
FROM (
	SELECT COUNT(*) AS tracks
	FROM playlist_track
	GROUP BY PlaylistId
)
;
