SELECT mtyp.Name AS MediaType,  COUNT(*) AS Tracks 
FROM tracks trck
RIGHT JOIN media_types mtyp
	ON trck.MediaTypeId = mtyp.MediaTypeId
GROUP BY mtyp.MediaTypeId
;
