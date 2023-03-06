-- Unique Work Days
-- 0
-- Question
-- Solution
-- You have a table containing information about the projects employees have worked on and the time period in which they worked on the project. Each project can be assigned to more than one employee, and an employee can be working on more than one project at a time.

-- Write a query to find how many unique days each employee worked. Order your query by the employee_id.

-- Example:

-- Input:

-- projects table

-- Columns Type
-- id  INTEGER
-- title VARCHAR
-- start_date  DATETIME
-- end_date  DATETIME
-- budget  INTEGER
-- employee_id INTEGER
-- Output:

-- Columns Type
-- employee_id INTEGER
-- days_worked DATETIME

-- get overlaps by getting previous end date when ordering user_id's start date in ascending order
-- define work days with overlaps and non-overlaps
-- for overlaps, count days worked as diff between prior end date and current end date 
-- with no overlaps, make usual diff between start and end dates
-- filter on work days >0 to discount prior end dates going over current end date
-- sum total work days per user
-- order result my employee id

--get overlapping projects by comparing project's end_date with next start_date
WITH overlapping AS (
SELECT *
, LAG(end_date, 1) OVER (PARTITION BY employee_id ORDER BY start_date ASC) AS previous_end_date
, CASE WHEN start_date < LAG(end_date, 1) OVER (PARTITION BY employee_id ORDER BY start_date ASC) THEN 1 ELSE 0 END AS overlap
FROM projects
-- ORDER BY employee_id
-- , start_date
)

--get working days of each project with appropriate start dates
, date_counts AS (
SELECT *
, CASE WHEN overlap = 1 THEN DATE(end_date) - DATE(previous_end_date) 
    ELSE DATE(end_date) - DATE(start_date) END AS working_days
FROM overlapping
)

SELECT employee_id
, SUM(working_days) AS days_worked
FROM date_counts
WHERE working_days > 0
GROUP BY 1
ORDER BY 1
