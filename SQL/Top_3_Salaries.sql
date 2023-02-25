-- Top Three Salaries
-- 39
-- Question
-- Solution
-- Given the employees and departments table, write a query to get the top 3 highest employee salaries by department. If the department contains less that 3 employees, the top 2 or the top 1 highest salaries should be listed (assume that each department has at least 1 employee). 

-- Note: The output should include the full name of the employee in one column, the department name, and the salary. The output should be sorted by department name in ascending order and salary in descending order. 

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
-- employee_name VARCHAR
-- department_name VARCHAR
-- salary  INTEGER

--join employees to departments
--get salaries by department ranking with highest first
--output as desired with top 3 (including departments with less than 3 employees)
WITH salary_rank AS (
SELECT CONCAT(first_name, ' ', last_name) AS employee_name
, name AS department_name
, salary
, DENSE_RANK() OVER (PARTITION BY name ORDER BY salary DESC) AS dept_salary_rank
FROM employees e 
JOIN departments d 
ON e.department_id = d.id
)

SELECT employee_name
, department_name
, salary
FROM salary_rank
WHERE dept_salary_rank <=3
ORDER BY 2
, 3 DESC
