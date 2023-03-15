-- Time Difference
-- 11
-- Question
-- Solution
-- Submissions
-- You work at a ride-sharing company and are given a table containing information about the rides of users.

-- Write a query to get the duration (in minutes) of each ride longer than two hours. Sort the results by duration in descending order.

-- rides table:

-- Columns Type
-- id  INTEGER
-- passenger_user_id INTEGER
-- start_dt  DATETIME
-- end_dt  DATETIME
-- distance  FLOAT
-- ride_region VARCHAR
-- is_completed  INTEGER
-- Output:

-- Column  Type
-- duration_minutes  INTEGER

-- get ride duraration in hours/minutes using EXTRACT(EPOCH from ride duration)
-- convert seconds to minutes
-- filter by lasting longer than 120 minutes aka 2 hrs
-- get rid of decimals with floor() fxn
-- order by duration in desc order

SELECT FLOOR(EXTRACT(EPOCH FROM end_dt-start_dt)/60) AS duration_minutes
FROM rides
WHERE FLOOR(EXTRACT(EPOCH FROM end_dt-start_dt)/60) > 120
ORDER BY 1 DESC
