-- Top 3 Users
-- 18
-- Question
-- Solution
-- Submissions
-- Let’s say you work at a file-hosting website. You have information on user’s daily downloads in the download_facts table

-- Use the window function RANK to display the top three users by downloads each day. Order your data by date, and then by daily_rank

-- Example:

-- Input:

-- download_facts table

-- Column  Type
-- user_id INTEGER
-- date  DATE
-- downloads INTEGER
-- Output:

-- Column  Type
-- daily_rank  INTEGER
-- user_id INTEGER
-- date  DATE
-- downloads INTEGER

-- aggregate downloads per user
-- rank downloads in desc order
-- get top 3 users by downloads each day

WITH total_downloads AS (
SELECT user_id
, date
, SUM(downloads) AS downloads
FROM download_facts
GROUP BY 1
, 2
)

, download_rk AS(
SELECT user_id
, date
, downloads
, RANK() OVER (PARTITION BY date ORDER BY downloads DESC) AS daily_rank
FROM total_downloads
ORDER BY date
, user_id
)

SELECT daily_rank
, user_id
, date
, downloads
FROM download_rk
WHERE daily_rank <= 3
ORDER BY 3
, 1
