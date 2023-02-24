-- Let’s say you have a table called events that keeps track of every user’s actions. A small example of the events table would look like this:

-- user_id created_at  action  platform
-- 1 2021-01-01 12:00:00 email_opened  Android
-- 2 2021-01-01 12:05:00 like  Outlook
-- 3 2021-01-01 12:10:00 post_enter  Gmail
-- 4 2021-01-01 12:15:00 post_cancel Outlook
-- 5 2021-01-01 12:20:00 like  Gmail
-- Using this information, you wish to find out how many users have opened an email.

-- What query would you use to find out?

-- Example:

-- Input:

-- events table

-- Column  Type
-- user_id INTEGER
-- created_at  DATETIME
-- action  VARCHAR
-- platform  VARCHAR
-- Output:

-- Column  Type
-- num_users_open_email  INTEGER

SELECT COUNT(DISTINCT user_id) AS num_users_open_email
FROM events
WHERE action = 'email_opened'
