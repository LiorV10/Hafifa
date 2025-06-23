SELECT
	cstmr.FirstName || " " || cstmr.LastName AS Customer,
	gnr.Name AS Genre,
	COUNT(*) AS Tracks
FROM invoice_items invc_itm
INNER JOIN invoices invc
	ON invc_itm.InvoiceId = invc.InvoiceId
INNER JOIN customers cstmr
	ON invc.CustomerId = cstmr.CustomerId
RIGHT JOIN tracks trck
	ON invc_itm.TrackId = trck.TrackId
RIGHT JOIN genres gnr
	ON trck.GenreId = gnr.GenreId
GROUP BY cstmr.CustomerID, gnr.GenreId
;
