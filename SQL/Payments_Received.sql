-- Payments Received
-- 5
-- Question
-- Solution
-- Submissions
-- You’re given two tables, payments and users. The payments table holds all payments between users with the payment_state column consisting of either "success" or "failed". 

-- How many customers that signed up in January 2020 had a combined (successful) sending and receiving volume greater than $100 in their first 30 days?

-- Note: The sender_id and recipient_id both represent the user_id.

-- payments table

-- Column  Type
-- payment_id  INTEGER
-- sender_id INTEGER
-- recipient_id  INTEGER
-- created_at  DATETIME
-- payment_state VARCHAR
-- amount_cents  INTEGER
-- users table

-- Column  Type
-- id  INTEGER
-- created_at  DATETIME
-- Output:

-- Column  Type
-- num_customers INTEGER

--customers created in jan 2020
--filter on transactions within 30 days of their sign up
--need to get sending and receiving with 'success' only and union these by user id
--filter on sum >= 100000
--get count distinct user ids

WITH jan_users AS (
SELECT *
FROM users
WHERE EXTRACT(YEAR FROM created_at) = 2020
AND EXTRACT(MONTH FROM created_at) = 1

)

, transactions AS (
SELECT jan_users.id
, amount_cents
FROM jan_users
JOIN payments
ON jan_users.id = payments.sender_id
WHERE payment_state = 'success'
AND payments.created_at <= jan_users.created_at + '30 day'

UNION

SELECT jan_users.id
, amount_cents
FROM jan_users
JOIN payments
ON jan_users.id = payments.recipient_id
WHERE payment_state = 'success'
AND payments.created_at <= jan_users.created_at + '30 day'
)

SELECT COUNT(DISTINCT id) AS num_customers
FROM transactions
GROUP BY id
HAVING SUM(amount_cents) >= 10000
