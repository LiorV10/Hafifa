SELECT AVG(quantity)
FROM (
	SELECT SUM(Quantity) AS quantity
	FROM invoice_items
	GROUP BY InvoiceId
)
;
