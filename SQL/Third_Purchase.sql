-- Third Purchase
-- 28
-- Question
-- Solution
-- Submissions
-- Given the transactions table below, write a query that finds the third purchase of every user.

-- Note: Sort the results by the user_id in ascending order. If a user purchases two products at the same time, the lower id field is used to determine which is the first purchase.

-- Example:

-- Input:

-- transactions table

-- Columns Type
-- id  INTEGER
-- user_id INTEGER
-- created_at  DATETIME
-- product_id  INTEGER
-- quantity  INTEGER
-- Output:

-- Columns Type
-- user_id INTEGER
-- created_at  DATETIME
-- product_id  INTEGER
-- quantity  INTEGER

-- get window function to get third tx from each user
-- get min tx id for ties
-- order by user_id in ASC order
WITH tx AS (
SELECT id
, user_id
, created_at
, product_id
, quantity
, RANK() OVER (PARTITION BY user_id ORDER BY created_at) AS tx_order
FROM transactions
)

,  target_tx AS (
SELECT MIN(id)
, user_id
, created_at
, product_id
, quantity
FROM tx
WHERE tx_order = 3
GROUP BY 2
, 3
, 4
, 5
)

SELECT user_id
, created_at
, product_id
, quantity
FROM target_tx
ORDER BY 1
