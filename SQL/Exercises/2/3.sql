SELECT PlaylistID, COUNT(*) AS Tracks
FROM playlist_track
GROUP BY PlaylistId
;
