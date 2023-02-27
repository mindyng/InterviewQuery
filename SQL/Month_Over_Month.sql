-- Month Over Month
-- 23
-- Question
-- Solution
-- Given a table of transactions and products, write a function to get the month_over_month change in revenue for the year 2019. Make sure to round month_over_month to 2 decimal places.

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
-- month INTEGER
-- month_over_month  FLOAT

--get 2019 tx
--join tx to products to get price
--get current months rev
--get last months rev
--prev - current/prev by month
WITH cte AS (
SELECT EXTRACT(MONTH FROM created_at) AS month
, SUM(quantity * price) AS revenue
FROM transactions
JOIN products
ON transactions.product_id = products.id
GROUP BY 1
)

SELECT month
, ROUND((revenue - LAG(revenue, 1) OVER (ORDER BY month))/LAG(revenue, 1) OVER (ORDER BY month)), 2) AS month_over_month
FROM cte
ORDER BY 1
