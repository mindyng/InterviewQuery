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
