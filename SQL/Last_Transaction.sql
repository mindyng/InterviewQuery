-- Last Transaction
-- 38
-- Question
-- Solution
-- Given a table of bank transactions with columns id, transaction_value, and created_at representing the date and time for each transaction, write a query to get the last transaction for each day.

-- The output should include the id of the transaction, datetime of the transaction, and the transaction amount. Order the transactions by datetime.

-- Example:

-- Input:

-- bank_transactions table

-- Column  Type
-- id  INTEGER
-- created_at  DATETIME
-- transaction_value FLOAT
-- Output:

-- Column  Type
-- created_at  DATETIME
-- transaction_value FLOAT
-- id  INTEGER

--get subq with max(created_at) group by date(created_at)
--filter original table's dates to these values
SELECT created_at
, transaction_value
, id
FROM bank_transactions
WHERE created_at IN
(SELECT MAX(created_at)
FROM bank_transactions
GROUP BY DATE(created_at))
ORDER BY created_at
