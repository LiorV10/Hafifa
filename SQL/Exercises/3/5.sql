SELECT *
FROM invoice_items invc_itm
INNER JOIN tracks trck
	ON invc_itm.TrackID = trck.TrackID
GROUP BY invc_itm.InvoiceID
HAVING COUNT(*) = SUM(
	CASE 
		WHEN trck.Milliseconds BETWEEN 2000 * 60 AND 5000 * 60 THEN 1
		ELSE 0
	END) 
;
