-- Employee Salaries
-- 91
-- Question
-- Solution
-- Given a employees and departments table, select the top 3 departments with at least ten employees and rank them according to the percentage of their employees making over 100K in salary.

-- Example:

-- Input:

-- employees table

-- Columns Type
-- id  INTEGER
-- first_name  VARCHAR
-- last_name VARCHAR
-- salary  INTEGER
-- department_id INTEGER
-- departments table

-- Columns Type
-- id  INTEGER
-- name  VARCHAR
-- Output:

-- Column  Type
-- percentage_over_100k  FLOAT
-- department_name VARCHAR
-- number_of_employees INTEGER

--get emp count per department (window fxn)
--join employees to department table
--get count of employees who make >100K in salary 
--divide by total num employees per dept
--rank according to percentage with highest on top
--filter on top 3
WITH eligible_dept AS ( --table at employee level
SELECT  department_id
, COUNT(id) OVER (PARTITION BY department_id) AS number_of_employees
, salary
)

, eligible_salary AS (
SELECT SUM(CASE WHEN salary > 100000 THEN 1 ELSE 0 END) * 1.0/number_of_employees AS percentage_over_100k
, name AS department_name
, number_of_employees
FROM eligible_dept AS ed 
JOIN departments AS d
ON ed.department_id = d.id
WHERE number_of_employees >= 10
GROUP BY 2
, 3
)

, salary_rank AS (
SELECT percentage_over_100k
, department_name
, number_of_employees
, RANK() OVER (PARTITION BY department_name ORDER BY percentage_over_100k DESC) AS rk
FROM eligible_salary
)

SELECT percentage_over_100k
, department_name
, number_of_employees
FROM salary_rank
WHERE rk <= 3
