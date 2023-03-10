-- ATM Robbery
-- 17
-- Question
-- Solution
-- Submissions
-- There was a robbery from the ATM at the bank where you work. Some unauthorized withdrawals were made, and you need to help your bank find out more about those withdrawals.

-- However, the only information you have is that there was more than 1 withdrawal, they were all performed in 10-second gaps, and no legitimate transactions were performed in between two fraudulent withdrawals.

-- We’re given a table of bank transactions with three columns, user_id, a deposit or withdrawal value transaction_value, and created_at time for each transaction.

-- Write a query to retrieve all user IDs in ascending order whose transactions have exactly a 10-second gap from one another.

-- Note: Assume that there are only withdrawals from the ATM, which are denoted with a positive transaction_value

-- Example: 

-- Input:

-- bank_transactions table

-- Column  Type
-- user_id INTEGER
-- created_at  DATETIME
-- transaction_value FLOAT
-- For given table bank_transactions:

-- user_id created_at  transaction_value
-- 1 2017-01-01 10:10:15 10
-- 2 2017-01-01 11:11:11 20
-- 3 2017-01-01 12:12:12 10
-- 4 2017-01-01 10:10:20 30
-- 5 2017-01-01 10:10:34 40
-- 6 2017-01-01 11:11:21 50
-- Output:

-- user_id
-- 2
-- 6

-- get previous tx
-- get subsequent tx
-- get timediff in seconds between current and prev and current and next tx times
-- filter on any instance of 10 sec gap between tx with OR
WITH times AS (
SELECT user_id
, created_at
, transaction_value
, LAG(created_at, 1) OVER (ORDER BY created_at) AS previous_tx
, LEAD(created_at, 1) OVER (ORDER BY created_at) AS next_tx
FROM bank_transactions
ORDER BY user_id
)

, timediff AS (
SELECT user_id
, created_at
, transaction_value
, EXTRACT(SECONDS FROM created_at - previous_tx) AS prev_diff
, EXTRACT(SECONDS FROM next_tx - created_at) AS next_diff
FROM times
)

SELECT DISTINCT user_id
FROM timediff
WHERE prev_diff = 10
OR next_diff = 10
ORDER BY 1
