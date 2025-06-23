SELECT CustomerID, COUNT(*) AS Invoices
FROM invoices
GROUP BY CustomerID
;
