-- Paired Products
-- 39
-- Question
-- Solution
-- Let’s say we have two tables, transactions and products. Hypothetically the transactions table consists of over a billion rows of purchases bought by users.

-- We are trying to find paired products that are often purchased together by the same user, such as wine and bottle openers, chips and beer, etc..

-- Write a query to find the top five paired products and their names.

-- Notes: For the purposes of satisfying the test case, p2 should be the item that comes first in the alphabet. The qty column represents paired products count

-- Example:

-- Input:

-- transactions table

-- Column  Type
-- id  INTEGER
-- user_id INTEGER
-- created_at  DATETIME
-- product_id  INTEGER
-- quantity  INTEGER
-- products table

-- Column  Type
-- id  INTEGER
-- name  VARCHAR
-- price FLOAT
-- Output:

-- Column  Type
-- p1  VARCHAR
-- p2  VARCHAR
-- qty INTEGER

--join transactions to products to get product name
--get product pairings by joining userid and tx time together 
--as well as excluding items paired to themselves by creating join
--based on first product name being less than second product name
--ORDER BY quantity in DESC order first and then second prod name in ASC order
--grab top 5

WITH purchases AS (
SELECT user_id
, created_at
, name
FROM transactions AS t 
JOIN products AS p 
ON t.product_id = p.id
)

SELECT t1.name AS p1
, t2.name AS p2
, COUNT(*) AS qty
FROM purchases AS t1
JOIN purchases AS t2
ON t1.user_id = t2.user_id
AND t1.created_at = t2.created_at
AND t1.name < t2.name
GROUP BY 1
, 2
ORDER BY 3 DESC, 2 ASC
LIMIT 5
