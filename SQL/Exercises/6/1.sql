SELECT cstmr.FirstName, SUM(invc_itm.Quantity)
FROM customers cstmr
INNER JOIN invoice_items invc_itm
	ON invc_itm.InvoiceId = invc.InvoiceId
INNER JOIN invoices invc
	ON cstmr.CustomerId = invc.CustomerId
WHERE cstmr.Company IS NOT NULL
GROUP BY cstmr.CustomerId
;
