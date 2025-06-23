SELECT
	cstmr.FirstName || " " || cstmr.LastName AS Customer,
	trck.Name AS Track,
	gnr.Name AS Genre,
	plist.PlaylistID || "-" || plist.Name AS Playlist
FROM customers cstmr
INNER JOIN invoices invc
	ON cstmr.CustomerID = invc.CustomerID
INNER JOIN invoice_items invc_itm
	ON invc.InvoiceID = invc_itm.InvoiceID
INNER JOIN tracks trck
	ON invc_itm.TrackID = trck.TrackID
INNER JOIN genres gnr
	ON trck.GenreID = gnr.GenreID
INNER JOIN playlist_track plist_trck
	ON trck.TrackID = plist_trck.TrackID
INNER JOIN playlists plist
	ON plist_trck.PlaylistID = plist.PlaylistID
;
