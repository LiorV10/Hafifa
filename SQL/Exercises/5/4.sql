SELECT AVG(ctmrs)
FROM (
	SELECT COUNT(*) AS ctmrs
	FROM customers
	GROUP BY City
)
;
