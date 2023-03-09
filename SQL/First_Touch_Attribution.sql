-- First Touch Attribution
-- 68
-- Question
-- Solution
-- Submissions
-- The schema below is for a retail online shopping company consisting of two tables, attribution and user_sessions.

-- The attribution table logs a session visit for each row.

-- If conversion is true, then the user converted to buying on that session.

-- The channel column represents which advertising platform the user was attributed to for that specific session.

-- Lastly the user_sessions table maps many to one session visits back to one user.

-- First touch attribution is defined as the channel with which the converted user was associated when they first discovered the website.

-- Calculate the first touch attribution for each user_id that converted. 

-- Example:

-- Input:

-- attribution table

-- Column  Type
-- session_id  INTEGER
-- channel VARCHAR
-- conversion  BOOLEAN
-- user_sessions table

-- column  type
-- session_id  INTEGER
-- created_at  DATETIME
-- user_id INTEGER
-- Example output:

-- user_id channel
-- 123 facebook
-- 145 google
-- 153 facebook
-- 172 organic
-- 173 email

--get converted users
--for those users, get all its sessions
--get first session

WITH converted AS (
SELECT session_id
, channel
FROM attribution 
WHERE conversion = 1
)

, user_sess AS (
SELECT user_sessions.user_id
, channel
, ROW_NUMBER() OVER (PARTITION BY user_sessions.user_id ORDER BY created_at) AS channel_order
FROM user_sessions
JOIN converted
ON user_sessions.session_id = converted.session_id
)

SELECT user_id
, channel
FROM user_sess
WHERE channel_order = 1
