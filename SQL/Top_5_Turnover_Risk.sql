-- Top 5 turnover risk
-- 1
-- Question
-- Solution
-- Let’s say you’re working in HR at a major tech company, and they ask you to find employees with a high probability of leaving the company. They tell you these employees perform well but have the lowest pay.

-- Given two tables, employees and projects, find the five lowest-paid employees who have completed at least three projects.

-- Note: We consider projects to be completed when they have an end date, which is the same as saying their End_dt is not NULL.

-- Example:

-- Input:

-- employees table

-- id  salary
-- INTEGER FLOAT
-- projects table

-- employee_id project_id  Start_dt  End_dt
-- INTEGER INTEGER DATETIME  DATETIME
-- Output:

-- employee_id
-- INTEGER

-- get the lowest paid employees
-- get their project counts
SELECT employee_id
FROM employees 
JOIN projects
ON employees.id = projects.employee_id
GROUP BY 1
HAVING COUNT(project_id) >= 3
ORDER BY salary 
LIMIT 5
