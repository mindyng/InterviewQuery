-- Distance Traveled
-- 31
-- Question
-- Solution
-- Given the tables users and rides, write a query to report the distance traveled by each user in descending order.

-- Example:

-- Input:

-- users table

-- Column  Type
-- id  INTEGER
-- name  INTEGER
-- rides table

-- Column  Type
-- id  INTEGER
-- passenger_user_id INTEGER
-- distance  FLOAT
-- Output:

-- Column  Type
-- name  VARCHAR
-- distance_traveled FLOAT

SELECT name
, COALESCE(SUM(distance), 0) AS distance_traveled
FROM users
LEFT JOIN rides
ON users.id = passenger_user_id
GROUP BY 1
ORDER BY 2 DESC
