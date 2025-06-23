SELECT
	cstmr.FirstName || " " || cstmr.LastName AS Customer,
	invc.InvoiceId
FROM customers cstmr
LEFT JOIN invoices invc
	ON cstmr.CustomerId = invc.InvoiceId
WHERE invc.InvoiceId IS NULL
;
