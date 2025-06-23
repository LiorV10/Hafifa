SELECT
	FirstName || " " || LastName AS FullName,
	DENSE_RANK() OVER (ORDER BY length(FirstName||LastName) DESC) [Index]
FROM customers
;
