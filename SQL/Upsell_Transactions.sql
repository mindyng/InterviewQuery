-- Upsell Transactions
-- 29
-- Question
-- Solution
-- We’re given a table of product purchases. Each row in the table represents an individual user product purchase.

-- Write a query to get the number of customers that were upsold by purchasing additional products.

-- Note: If the customer purchased two things on the same day that does not count as an upsell as they were purchased within a similar timeframe.

-- Example:

-- Input:

-- transactions table

-- Column  Type
-- id  INTEGER
-- user_id INTEGER
-- created_at  DATETIME
-- product_id  INTEGER
-- quantity  INTEGER
-- Output:

-- Column  Type
-- num_of_upsold_customers INTEGER

--filter out same day/time tx
--get orders per user ordered by order date
--filter on orders after first order
--get count of distinct users

WITH duplicates AS (
    SELECT user_id
, created_at
, ROW_NUMBER() OVER (PARTITION BY user_id, created_at ORDER BY created_at) AS dups
FROM transactions 
ORDER BY user_id
, created_at
)

, user_orders AS (
    SELECT *
, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) order_num
FROM duplicates
WHERE dups = 1
)

SELECT COUNT(DISTINCT user_id) AS num_of_upsold_customers
FROM user_orders
WHERE order_num > 1
