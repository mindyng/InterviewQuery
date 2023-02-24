-- Like Tracker
-- 19
-- Question
-- Solution
-- The events table tracks every time a user performs a certain action (like, post_enter, etc.) on a platform. An example of this table would look like this:

-- user_id created_at  action  platform
-- 1 2021-01-01 12:00:00 email_opened  Android
-- 2 2021-01-01 12:05:00 like  Outlook
-- 3 2021-01-01 12:10:00 post_enter  Gmail
-- 4 2021-01-01 12:15:00 post_cancel Outlook
-- 5 2021-01-01 12:20:00 like  Gmail
-- What query would you write to determine how many different users gave a like on June 6, 2020?

-- Example:

-- Input:

-- events table

-- Column  Type
-- user_id INTEGER
-- created_at  DATETIME
-- action  VARCHAR
-- platform  VARCHAR
-- Output

-- Column  Type
-- num_users_gave_like INTEGER

--fitler on 6,6,20 and action = like
--get distinct num users

SELECT COUNT(DISTINCT user_id) AS num_users_gave_like
FROM events
WHERE DATE(created_at) = '2020-06-06'
AND action = 'like'
