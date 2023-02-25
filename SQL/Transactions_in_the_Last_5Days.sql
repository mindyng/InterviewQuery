--filter on Jan 2020
--get each transaction's date
--get all tx dates that are between '2020-01-01' AND '2020-01-05'
--given that they are 5 total days, get users who only have tx count of 5
--count these users with tx/day for 5 days
WITH transactions AS (
SELECT DISTINCT user_id
, DATE(created_at) AS created_at
FROM bank_transactions
WHERE created_at BETWEEN '2020-01-01' AND '2020-01-05'
ORDER BY user_id
, created_at
)

, daily_tx AS (SELECT user_id
, created_at
FROM transactions
WHERE created_at <= '2020-01-05'
GROUP BY 1
, 2
HAVING COUNT(created_at) = 5
)

SELECT COUNT(user_id) AS number_of_users
FROM daily_tx
