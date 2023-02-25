-- Comments Histogram
-- 96
-- Question
-- Solution
-- Write a SQL query to create a histogram of the number of comments per user in the month of January 2020.

-- Note: Assume bin buckets class intervals of one.

-- Note: Comments by users that were not created in January 2020 should be counted in a “0” bucket

-- Example:

-- Input:

-- users table

-- Columns Type
-- id  INTEGER
-- name  VARCHAR
-- created_at  DATETIME
-- neighborhood_id INTEGER
-- mail  VARCHAR
-- comments table

-- Columns Type
-- user_id INTEGER
-- body  VARCHAR
-- created_at  DATETIME
-- Output:

-- Column  Type
-- comment_count INTEGER
-- frequency INTEGER

--left join users to comments
--filter on Jan 2020 comments
--get comments/user for this time interval
--get num_comments freq

WITH hist AS (
SELECT users.id
, COUNT(comments.user_id) AS num_comments
FROM users
LEFT JOIN comments
ON users.id = comments.user_id
WHERE comments.created_at BETWEEN '2020-01-01' AND '2020-01-31'
GROUP BY 1
)

SELECT num_comments
, COUNT(*) AS frequency
FROM hist
GROUP BY 1
