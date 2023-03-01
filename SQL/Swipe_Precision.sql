-- Swipe Precision
-- 9
-- Question
-- Solution
-- There are two tables. One table is called swipes that holds a row for every Tinder swipe and contains a boolean column that determines if the swipe was a right or left swipe called is_right_swipe. The second is a table named variants that determines which user has which variant of an AB test.

-- Write a SQL query to output the average number of right swipes for two different variants of a feed ranking algorithm by comparing users that have swiped the first 10, 50, and 100 swipes on their feed.

-- Note: Users have to have swiped at least 10 times to be included in the subset of users to analyze the mean number of right swipes.

-- Example:

-- Input:

-- variants table

-- Columns Type
-- id  INTEGER
-- experiment  VARCHAR
-- variant VARCHAR
-- user_id INTEGER
-- swipes table

-- Columns Type
-- id  INTEGER
-- user_id INTEGER
-- swiped_user_id  INTEGER
-- created_at  DATETIME
-- is_right_swipe  BOOLEAN
-- Output:

-- Columns Type
-- varient VARCHAR
-- mean_right_swipes FLOAT
-- swipe_threshold INTEGER
-- num_users INTEGER

--get qualified users with at least 10 swipes
--join swipes to variants
--get swipe thresholds for 10, 50 and 100
--get aggregations

WITH qualified_users AS (
SELECT user_id
, SUM(is_right_swipe) AS num_right_swipes
, COUNT(DISTINCT id) AS num_swipes
FROM swipes
GROUP BY 1
HAVING COUNT(DISTINCT id) >= 10
)
 
 SELECT variant
 , AVG(num_right_swipes) AS mean_right_swipes
 , CASE WHEN num_swipes >= 100 THEN 100 WHEN num_swipes >= 50 THEN 50 ELSE 10 END AS swipe_threshold
 , COUNT(DISTINCT qu.user_id) AS num_users
 FROM qualified_users AS qu
 JOIN variants AS v
 ON qu.user_id = v.user_id
GROUP BY 1
, 3
