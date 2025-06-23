SELECT trck.Name, gnr.Name
FROM tracks trck
INNER JOIN genres gnr
	ON trck.GenreID = gnr.GenreID
;
