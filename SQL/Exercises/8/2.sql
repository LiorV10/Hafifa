SELECT
	CustomerId,
	FirstName || " " || LastName AS Customer,
	State,
	COUNT (CustomerId) OVER (PARTITION BY State) AS CustomersInState
FROM customers
;

