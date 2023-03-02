-- Cumulative Reset
-- 32
-- Question
-- Solution
-- Given a users table, write a query to get the cumulative number of new users added by the day, with the total reset every month. 

-- Example:

-- Input:

-- users table

-- Columns Type
-- id  INTEGER
-- name  VARCHAR
-- created_at  DATETIME
-- Output:

-- DATE  INTEGER
-- 2020-01-01  5
-- 2020-01-02  12
-- … …
-- 2020-02-01  8
-- 2020-02-02  17
-- 2020-02-03  23

--cumulative number users by day
--reset each month (partitioned by month)
WITH num_users AS (
SELECT DATE(created_at) AS date
, COUNT(id) AS num_users
FROM users
GROUP BY 1
ORDER BY 1
)

SELECT date
, SUM(num_users) OVER (PARTITION BY EXTRACT(YEAR FROM date),  EXTRACT(MONTH FROM date) ORDER BY date) AS monthly_cumulative
FROM num_users
ORDER BY 1
