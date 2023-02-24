-- Monthly Customer Report
-- 13
-- Question
-- Solution
-- Write a query to show the number of users, number of transactions placed, and total order amount per month in the year 2020. Assume that we are only interested in the monthly reports for a single year (January-December).

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
-- users table

-- Column  Type
-- id  INTEGER
-- name  VARCHAR
-- sex VARCHAR
-- Output:

-- Column  Type
-- month INTEGER
-- num_customers INTEGER
-- num_orders  INTEGER
-- order_amt INTEGER

--get transactions in 2020
--get month for each transaction
--aggregate num users, num tx, total order amt
--order by month
select EXTRACT(MONTH FROM created_at) AS month
, COUNT(DISTINCT user_id) AS num_customers
, COUNT(transactions.id) AS num_orders
, SUM(quantity * price) AS order_amt
from users
LEFT JOIN transactions
ON users.id = transactions.user_id
JOIN products
ON transactions.product_id = products.id
GROUP BY 1
ORDER BY 1
