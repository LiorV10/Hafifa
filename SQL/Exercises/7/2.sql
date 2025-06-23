SELECT FirstName || " " || LastName
FROM employees
UNION
SELECT FirstName || " " || LastName
FROM customers
;
