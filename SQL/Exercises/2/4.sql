SELECT strftime("%Y-%m", InvoiceDate) AS Date, COUNT(*) Invoices
FROM invoices
GROUP BY strftime("%Y-%m", InvoiceDate)
;
