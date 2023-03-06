-- Closed Accounts
-- 9
-- Question
-- Solution
-- Editor
-- Details
-- Submissions
-- Given a table of account statuses, write a query to get the percentage of accounts that were active on December 31st, 2019, and closed on January 1st, 2020, over the total number of accounts that were active on December 31st. Each account has only one daily record indicating its status at the end of the day.

-- Note: Round the result to 2 decimal places.

-- Example:

-- Input:

-- account_status table

-- Column  Type
-- account_id  INTEGER
-- date  DATETIME
-- status  VARCHAR
-- account_id  date  status
-- 1 2020-01-01  closed
-- 1 2019-12-31  open
-- 2 2020-01-01  closed
-- Output:

-- Column  Type
-- percentage_closed FLOAT

--get total active accounts on Dec 31, 2019
--of those accounts, get those that have status closed on Jan 1, 2020
--have closed accounts/active accounts
--round result to 2 decimal places
WITH open_accounts AS (
SELECT *
FROM account_status 
WHERE date = '2019-12-31'
AND status = 'open'
)

, closed_accounts AS (
SELECT *
FROM account_status
WHERE date = '2020-01-01'
AND status = 'closed'
)

SELECT ROUND(SUM(CASE WHEN closed_accounts.account_id IS NOT NULL THEN 1 ELSE 0 END) * 1.0/COUNT(*), 2) AS percentage_closed
FROM open_accounts
LEFT JOIN closed_accounts
ON open_accounts.account_id = closed_accounts.account_id
