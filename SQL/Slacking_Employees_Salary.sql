-- Slacking employees salaries
-- 0
-- Question
-- Solution
-- Suppose your company needs to cut costs due to an economic downturn. During a coffee break, you hear a rumor that a lot of money goes to employees who don’t do their work, and you decide to find out if the rumor is true.

-- Given two tables: employees and projects, find the sum of the salaries of all the employees who didn’t complete any of their projects.

-- Clarification:

-- We will consider a project unfinished if it has no end date (its End_dt is NULL).

-- Given this, we’ll say an employee didn’t finish any of their projects when:

-- They were assigned at least one project.
-- None of their projects have an End_dt.
-- Example:

-- Input:

-- employees table

-- id  salary
-- INTEGER FLOAT
-- projects table

-- employee_id project_id  Start_dt  End_dt
-- INTEGER INTEGER DATETIME  DATETIME
-- Output:

-- total_slack_salary
-- INTEGER

--inner join employees to projects
--create flag for non-null End_dt
--COUNT non-null per employee
--filter on employees who have 0 total sum for flag
--count distinct these employees
WITH cte AS (
SELECT employee_id
, salary
, SUM(CASE WHEN End_dt IS NOT NULL THEN 1 ELSE 0 END) AS completed_projects
FROM employees
JOIN projects 
ON employees.id = projects.employee_id
GROUP BY 1
, 2
)

SELECT SUM(salary) AS total_slack_salary
FROM cte
WHERE completed_projects = 0
