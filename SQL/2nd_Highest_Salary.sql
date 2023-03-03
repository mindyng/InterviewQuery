-- 2nd Highest Salary
-- 98
-- Question
-- Solution
-- Write a SQL query to select the 2nd highest salary in the engineering department.

-- Note: If more than one person shares the highest salary, the query should select the next highest salary.

-- Example:

-- Input:

-- employees table

-- Column  Type
-- id  INTEGER
-- first_name  VARCHAR
-- last_name VARCHAR
-- salary  INTEGER
-- department_id INTEGER
-- departments table

-- Column  Type
-- id  INTEGER
-- name  VARCHAR
-- Output:

-- Column  Type
-- salary  INTEGER

--join employees to departments
--filter for engineering
--get dense rank of salary
--this fulfills criteria if more than 1 person ties for 1st place. dense rank continues with 2 after ties of 1st place is done
--filter for second rank
WITH cte_1 AS (SELECT salary
, DENSE_RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees
JOIN departments
ON employees.department_id = departments.id
where name = 'engineering'
)

SELECT salary
FROM cte_1
WHERE salary_rank = 2
