-- Empty Neighborhoods
-- 63
-- Question
-- Solution
-- We’re given two tables, a users table with demographic information and the neighborhood they live in and a neighborhoods table.

-- Write a query that returns all neighborhoods that have 0 users. 

-- Example:

-- Input:

-- users table

-- Columns Type
-- id  INTEGER
-- name  VARCHAR
-- neighborhood_id INTEGER
-- created_at  DATETIME
-- neighborhoods table

-- Columns Type
-- id  INTEGER
-- name  VARCHAR
-- city_id INTEGER
-- Output:

-- Columns Type
-- name  VARCHAR

--LEFT join neighborhoods to users
--get neighborhood names that have users.neighborhood_id IS NULL
SELECT neighborhoods.name
FROM neighborhoods
LEFT JOIN users
ON users.neighborhood_id = neighborhoods.id
WHERE users.neighborhood_id IS NULL
