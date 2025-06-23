SELECT 	DISTINCT
	cstmr.FirstName || " " || cstmr.LastName AS Customer,
	mtyp.Name AS MediaType
FROM invoice_items invc_itm
INNER JOIN invoices invc
	ON invc_itm.InvoiceId = invc.InvoiceId
INNER JOIN customers cstmr
	ON invc.CustomerId = cstmr.CustomerId
INNER JOIN tracks trck
	ON invc_itm.TrackId = trck.TrackId
INNER JOIN media_types mtyp
	ON trck.MediaTypeId = mtyp.MediaTypeId
;
