SELECT CustomerID, AVG(DaysBetween)
FROM (
	SELECT
	    CustomerID,
	    InvoiceDate,
	    CASE 
		WHEN NextInvoiceDate IS NOT NULL THEN CAST(JULIANDAY(NextInvoiceDate) - JULIANDAY(InvoiceDate) AS INTEGER)
		ELSE NULL
	    END AS DaysBetween
	FROM (
	    SELECT
		CustomerID,
		InvoiceDate,
		LEAD(InvoiceID) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS NextInvoiceID,
		LEAD(InvoiceDate) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS NextInvoiceDate
	    FROM Invoices
))
GROUP BY CustomerID;


