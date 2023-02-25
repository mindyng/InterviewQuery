-- Duplicate Rows
-- 17
-- Question
-- Solution
-- Given a users table, write a query to return only its duplicate rows.

-- Example:

-- Input:

-- users table

-- Column  Type
-- id  INTEGER
-- name  VARCHAR
-- created_at  DATETIME

WITH cte AS (
    SELECT *
    , ROW_NUMBER() OVER (PARTITION BY id, name, created_at) AS dup
FROM users
)

SELECT id
, name
, created_at
FROM cte
WHERE dup = 2
