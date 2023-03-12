-- Attribution Rules
-- 5
-- Question
-- Solution
-- Submissions
-- Write a query that creates an attribution rule for each user. If the user visited Facebook or Google at least once then the attribution is labeled as “paid.” Otherwise, the attribution is labeled as “organic.”

-- Example:

-- Input:

-- user_sessions table

-- Column  Type
-- created_at  DATETIME
-- session_id  INTEGER
-- user_id INTEGER
-- attribution table 

-- Column  Type
-- session_id  INTEGER
-- channel VARCHAR
-- Output:

-- Column  Type
-- user_id INTEGER
-- attribute VARCHAR

-- join user_sessions to attribution
-- CASE WHEN to build categories from paid vs organic
-- to get one row for each user, use max() on case st to grab paid if it exists otherwise output organic
SELECT user_id
, MAX(CASE WHEN lower(channel) IN ('facebook', 'google') THEN 'paid' ELSE 'organic' END) AS attribute
FROM user_sessions
JOIN attribution
ON user_sessions.session_id = attribution.session_id
GROUP BY 1
ORDER BY 1
