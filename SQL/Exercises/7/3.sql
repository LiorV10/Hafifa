SELECT Address
FROM (
	SELECT Address
	FROM employees
	UNION ALL
	SELECT Address
	FROM customers
)
GROUP BY Address
HAVING COUNT(*) > 1
;
