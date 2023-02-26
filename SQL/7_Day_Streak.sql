-- 7 Day Streak
-- 20
-- Question
-- Solution
-- Given a table with event logs, find the percentage of users that had at least one seven-day streak of visiting the same URL.

-- Note: Round the results to 2 decimal places. For example, if the result is 35.67% return 0.35.

-- Example:

-- Input:

-- events table

-- Column  Type
-- user_id INTEGER
-- created_at  DATETIME
-- url VARCHAR
-- Output

-- Column  Type
-- output  FLOAT

WITH unique_visits AS (
    SELECT DISTINCT user_id
      , url
      , DATE(created_at) AS date_created
    FROM events
    ORDER BY user_id
      , url
      , date_created
)

, date_groups AS (
    SELECT user_id
        , url
        , date_created
        , RANK() OVER (PARTITION BY url,user_id ORDER BY date_created) AS row_num
    FROM unique_visits
)

, date_groups_2 AS (
    SELECT user_id
        , url
        , date_created
        , row_num
        , date_created - INTERVAL '1 DAY' * row_num AS date_group
    FROM date_groups
)

, user_streaks AS (
    SELECT user_id
        , url
        , date_group
        , COUNT(*) AS day_streaks
    FROM date_groups_2
    GROUP BY user_id
    , url
    , date_group
)
    
SELECT   
    ROUND(
    (SELECT COUNT(DISTINCT user_id)   
     FROM (SELECT user_id
           FROM user_streaks 
           GROUP BY user_id 
           HAVING MAX(day_streaks) >= 7) AS active_users
           ) * 1.0
     / COUNT(DISTINCT user_id)
     , 2) AS precent_of_users
FROM user_streaks
