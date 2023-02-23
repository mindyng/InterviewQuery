-- User Experience Percentage
-- 6
-- Question
-- Solution
-- Editor
-- Details
-- Submissions
-- Given a table called user_experiences, write a query to determine the percentage of users that held the title of “Data Analyst” immediately before holding the title “Data Scientist”.

-- Immediate is defined as the user holding no other titles between the “Data Analyst” and “Data Scientist” roles.

-- Example:

-- Input:

-- user_experiences table

-- Column  Type
-- id  INTEGER
-- position_name VARCHAR
-- start_date  DATETIME
-- end_date  DATETIME
-- user_id INTEGER
-- Output:

-- Column  Type
-- percentage  FLOAT

WITH cte AS
  (SELECT * ,
          LAG(position_name, 1) OVER (PARTITION BY user_id
                                      ORDER BY start_date) AS prev_position
   FROM user_experiences
   ORDER BY user_id,
            start_date)
SELECT round(SUM(CASE WHEN prev_position = 'Data Analyst'
                 AND position_name = 'Data Scientist' THEN 1 ELSE 0 END) * 1.0/COUNT(DISTINCT user_id), 3) AS percentage
FROM cte
