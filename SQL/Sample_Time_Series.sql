-- Sample Time Series
-- 10
-- Question
-- Solution
-- Given a transactions table with date timestamps, sample every 4th row ordered by the date.

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
-- created_at  DATETIME
-- product_id  INTEGER

--get row number for each row ordered by created_at
--filter by rows divisible by 4 (mod with remainder = 0)
WITH cte AS (
SELECT created_at
, product_id
, ROW_NUMBER() OVER (ORDER BY created_at) AS row_num 
FROM transactions
)

SELECT created_at
, product_id
FROM cte
WHERE row_num % 4 = 0
ORDER BY 1
, 2
