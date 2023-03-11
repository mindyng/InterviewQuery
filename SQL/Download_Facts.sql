-- Download Facts
-- 19
-- Question
-- Solution
-- Submissions
-- Given two tables: accounts, and downloads, find the average number of downloads for free vs paying accounts, broken down by day.

-- Note: You only need to consider accounts that have had at least one download before when calculating the average.

-- Note: round average_downloads to 2 decimal places.

-- Example:

-- Input:

-- accounts table

-- Column  Type
-- account_id  INTEGER
-- paying_customer BOOLEAN
-- downloads table

-- column  type
-- account_id  INTEGER
-- download_date DATETIME
-- downloads INTEGER
-- Output:

-- Column  Type
-- download_date DATETIME
-- paying_customer BOOLEAN
-- average_downloads FLOAT

-- join accounts to downloads by accuont_id
-- get average downloads broken down by day per customer type
SELECT download_date
, paying_customer
, ROUND(AVG(downloads)::DECIMAL, 2) AS average_downloads
FROM accounts
JOIN downloads
ON accounts.account_id = downloads.account_id
GROUP BY 1
, 2
HAVING SUM(downloads) >= 1
