-- Rolling Bank Transactions
-- 44
-- Question
-- Solution
-- We’re given a table of bank transactions with three columns, user_id, a deposit or withdrawal value (determined if the value is positive or negative), and created_at time for each transaction.

-- Write a query to get the total three-day rolling average for deposits by day.

-- Note: Please use the format '%Y-%m-%d' for the date in the outout

-- Example:

-- Input:

-- bank_transactions table

-- Column  Type
-- user_id INTEGER
-- created_at  DATETIME
-- transaction_value FLOAT
-- Output:

-- Column  Type
-- dt  VARCHAR
-- rolling_three_day FLOAT

--filter for deposits
--first aggregate transaction_value by date
--get window function to do average on current row and previous two transaction deposit values

WITH bank AS (
SELECT DATE(created_at) AS dt
, SUM(transaction_value) AS total 
FROM bank_transactions 
WHERE transaction_value > 0 
GROUP BY 1)

SELECT dt
, AVG(total) OVER (ORDER BY dt ASC ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_three_day 
FROM bank
