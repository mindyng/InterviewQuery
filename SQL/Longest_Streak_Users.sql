-- Longest Streak Users
-- 29
-- Question
-- Solution
-- Given a table with event logs, find the top five users with the longest continuous streak of visiting the platform in 2020.

-- Note: A continuous streak counts if the user visits the platform at least once per day on consecutive days.

-- Example:

-- Input:

-- events table

-- Column  Type
-- user_id INTEGER
-- created_at  DATETIME
-- url VARCHAR
-- Output:

-- Column  Type
-- user_id INTEGER
-- streak_length INTEGER

WITH cte1 AS (
    SELECT user_id
        , DATE(created_at) AS created_at
        , DENSE_RANK() OVER (PARTITION BY user_id ORDER BY created_at) AS rnk
    FROM events
)
, cte2 AS (
    SELECT user_id
    , MAX(rnk) - MIN(rnk) + 1 AS streak_length
    FROM cte1
    GROUP BY user_id
        , created_at - INTERVAL '1 DAY' * rnk
)

SELECT user_id
        , MAX(streak_length) AS streak_length
    FROM cte2
    GROUP BY user_id
    ORDER BY MAX(streak_length) DESC
    LIMIT 5
