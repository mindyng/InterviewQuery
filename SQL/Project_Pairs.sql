-- Project Pairs
-- 13
-- Question
-- Solution
-- Write a query to return pairs of projects where the end date of one project matches the start date of another project. 

-- Example:

-- Input:

-- projects table

-- Columns Type
-- id  INTEGER
-- title VARCHAR
-- start_date  DATETIME
-- end_date  DATETIME
-- budget  FLOAT
-- Output

-- Columns Type
-- project_title_end VARCHAR
-- project_title_start VARCHAR
-- date  DATETIME

--self join projects on diff projects and start date same as end date
--output first project title, second project time and overlapping date
SELECT t1.title AS project_title_end
, t2.title AS project_title_start
, t1.end_date AS date
FROM projects t1
JOIN projects t2
ON t1.id != t2.id
AND t1.end_date = t2.start_date
