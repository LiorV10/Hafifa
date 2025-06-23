SELECT *
FROM tracks
WHERE Milliseconds BETWEEN 2000 * 60 AND 3000 * 60
ORDER BY Milliseconds ASC
;
