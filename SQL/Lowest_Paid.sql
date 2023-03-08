-- Lowest Paid
-- 12
-- Question
-- Solution
-- Submissions
-- Given tables employees, employee_projects, and projects, find the 3 lowest-paid employees that have completed at least 2 projects.

-- Note: incomplete projects will have an end date of NULL in the projects table.

-- Example:

-- Input:

-- employees table

-- Column  Type
-- id  INTEGER
-- first_name  VARCHAR
-- last_name VARCHAR
-- salary  INTEGER
-- department_id INTEGER
-- employee_projects table

-- Column  Type
-- employee_id INTEGER
-- project_id  INTEGER
-- projects table

-- Column  Type
-- id  INTEGER
-- title VARCHAR
-- start_date  DATE
-- end_date  DATE
-- budget  INTEGER
-- Output:

-- Column  Type
-- employee_id INTEGER
-- salary  INTEGER
-- completed_projects  INTEGER

--join employees to employee projects and this to projects to get desired output columns
--employees who completed minimum of 2 projects by getting project count
--filter on min 2 projects
--rank salary in ASC order
--get rank <= 3 (there may be ties)

WITH project_num AS (
SELECT employee_id
, salary
, COUNT(project_id) AS completed_projects
FROM employees
JOIN employee_projects
ON employees.id = employee_projects.employee_id
JOIN projects 
ON employee_projects.project_id = projects.id
GROUP BY 1
, 2
)

, salary_rank AS (
SELECT DISTINCT employee_id
, salary
, completed_projects
, DENSE_RANK() OVER (ORDER BY salary) AS salary_rk
FROM project_num
WHERE completed_projects >=2
)

SELECT employee_id
, salary
, completed_projects
FROM salary_rank
WHERE salary_rk <=3
