-- Session Difference
-- 27
-- Question
-- Solution
-- Submissions
-- Given a table of user sessions, write a query to get the number of days between each user’s first session and last session for the year 2020. 

-- Example:

-- Input:

-- user_sessions table

-- Column  Type
-- session_id  INTEGER
-- created_at  DATETIME
-- user_id INTEGER
-- Output:

-- Column  Type
-- user_id INTEGER
-- no_of_days  INTEGER

-- get data from 2020 only 
-- get window function to order by users' session
-- filter on min and max per user
-- get time difference in days
-- simpler solution since dont need to compare aggregate to all values in table:
-- min and max created_at per user_id
-- get dates of each created_at and get days diff


-- WITH sess_order AS (
-- SELECT user_id
-- , created_at
-- , ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS session_order
-- FROM user_sessions
-- WHERE EXTRACT(YEAR FROM created_at) = 2020
-- )

-- , first_sess AS (
-- SELECT user_id
-- , created_at AS first_sess_time
-- FROM sess_order
-- WHERE session_order = 1
-- ORDER BY 1
-- , 2
-- )

-- , last_sess AS (
-- SELECT user_id
-- , created_at AS last_sess_time
-- FROM (SELECT user_id
-- , created_at
-- , session_order
-- , MAX(session_order) OVER (PARTITION BY user_id) AS last_sess
-- FROM sess_order
-- ORDER BY 1
-- , 2
-- ) AS subq
-- WHERE session_order = last_sess
-- )

-- SELECT first_sess.user_id
-- , DATE(last_sess_time) - DATE( first_sess_time) AS no_of_days
-- FROM first_sess
-- JOIN last_sess
-- ON first_sess.user_id = last_sess.user_id

SELECT user_id
, MAX(DATE(created_at)) - MIN(DATE(created_at)) AS no_of_days
FROM user_sessions
WHERE EXTRACT(YEAR FROM created_at) = 2020
GROUP BY 1
ORDER BY 1
