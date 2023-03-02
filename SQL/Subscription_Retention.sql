-- Subscription Retention
-- 15
-- Question
-- Solution
-- Given a table of subscriptions, write a query to get the retention rate of each monthly cohort for each plan_id for the three months after sign-up.

-- Order your output by start_month, plan_id, then num_month.

-- If an end_date is in the same month as start_date we say the subscription was not retained in the first month.

-- If the end_date occurs in the month after the month of start_date, the subscription was not retained in the second month. And so on for the third.

-- The end_date field is NULL if the user has not canceled.

-- Example:

-- Input:

-- subscriptions table

-- Column  Type
-- user_id INTEGER
-- start_date  DATETIME
-- end_date  DATETIME
-- plan_id VARCHAR
-- Output:

-- Column  Type
-- start_month DATETIME
-- num_month INTEGER
-- plan_id VARCHAR
-- retained  FLOAT

--filter for three months after sign up
--retention rate of monthly cohort's plan id
--order by desired output: start_month, plan_id, num_month
WITH retention_one_month AS (
    SELECT
        TO_CHAR(start_date, 'yyyy-mm-01')::date start_month,
        1 AS num_month,
        plan_id
        , ROUND(AVG(COALESCE(CASE WHEN DATE(end_date) - DATE(start_date) < 30 THEN 0 ELSE 1 END, 1)), 2) AS retained
    FROM subscriptions
    GROUP BY 1, 3
)

, retention_two_month AS (
    SELECT
        TO_CHAR(start_date, 'yyyy-mm-01')::date start_month,
        2 AS num_month,
        plan_id
        , ROUND(AVG(COALESCE(CASE WHEN DATE(end_date) - DATE(start_date) < 60 THEN 0 ELSE 1 END, 1)), 2) AS retained
    FROM subscriptions
    GROUP BY 1, 3
)

, retention_three_month AS (
    SELECT
        TO_CHAR(start_date, 'yyyy-mm-01')::date start_month,
        3 AS num_month,
        plan_id
        , ROUND(AVG(COALESCE(CASE WHEN DATE(end_date) - DATE(start_date) < 90 THEN 0 ELSE 1 END, 1)), 2) AS retained
    FROM subscriptions
    GROUP BY 1, 3
)

SELECT * FROM retention_one_month
UNION
SELECT * FROM retention_two_month
UNION
SELECT * FROM retention_three_month
ORDER BY start_month, plan_id, num_month 
