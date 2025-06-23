SELECT
	cstmr.FirstName || " " || cstmr.LastName AS Customer,
	trck.Name AS Track,
	invc.InvoiceDate AS Date,
	invc.BillingCity AS City
FROM customers cstmr
INNER JOIN invoices invc
	ON cstmr.CustomerID = invc.CustomerID
INNER JOIN invoice_items invc_itm
	ON invc.InvoiceID = invc_itm.InvoiceID
INNER JOIN tracks trck
	ON invc_itm.TrackID = trck.TrackID
;
