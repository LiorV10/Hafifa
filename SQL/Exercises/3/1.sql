SELECT Title, Name
FROM albums albm
INNER JOIN artists art
	ON albm.ArtistID = art.ArtistID
;
