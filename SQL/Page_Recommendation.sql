-- Page Recommendations
-- 0
-- Question
-- Solution
-- Submissions
-- Write a query to get the percentage of recommendations for each page by users in the same postal code as the page. 

-- Note: A page can sponsor multiple postal codes.

-- Example:

-- Input:

-- page_sponsorships table

-- Column  Type
-- page_id INTEGER
-- postal_code VARCHAR
-- price FLOAT
-- recommendations table 

-- Column  Type
-- user_id INTEGER
-- page_id INTEGER
-- users table

-- Column  Type
-- id  INTEGER
-- postal_code VARCHAR
-- Output:

-- Column  Type
-- page  INTEGER
-- postal_code VARCHAR
-- percentage  FLOAT

-- join all tables together; recommendations acts as hinge table to get user_id
-- get count of all users' from recommendations
-- build business logic using case statement to say if postal code same between user and sponsored page then provide id from users
-- aggregate the portion value and the denominator value
-- get percentage by dividing the last 2


SELECT s.page_id AS page
, s.postal_code
, COUNT(CASE WHEN s.postal_code = u.postal_code THEN u.id END) * 1.0/COUNT(r.user_id) AS percentage
FROM page_sponsorships s
JOIN recommendations r
ON s.page_id = r.page_id
JOIN users u
ON u.id = r.user_id
GROUP BY 1
, 2
ORDER BY 1
, 2
