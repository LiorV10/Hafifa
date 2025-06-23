SELECT
	FirstName || " " || LastName AS Customer,
	InvoiceId,
	Total - AVG(Total) OVER (PARTITION BY cstmr.CustomerID) AS Difference
FROM invoices invc
INNER JOIN customers cstmr
	ON invc.CustomerID = cstmr.CustomerID
;
