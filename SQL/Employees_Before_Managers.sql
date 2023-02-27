-- Employees Before Managers
-- 12
-- Question
-- Solution
-- You’re given two tables: employees and managers. Find the names of all employees who joined before their manager.

-- Example:

-- Input:

-- employees table

-- Column  Type
-- id  INTEGER
-- first_name  VARCHAR
-- last_name VARCHAR
-- manager_id  INTEGER
-- join_date DATETIME
-- managers table

-- Column  Type
-- id  INTEGER
-- name  VARCHAR
-- join_date DATETIME
-- Output:

-- Column  Type
-- employee_name VARCHAR

--join employees to managers
--filter table on employees join date < managers join date
--output concat first name and last name of employees
SELECT CONCAT(employees.first_name, ' ', employees.last_name) AS employee_name
FROM employees
JOIN managers
ON employees.manager_id = managers.id
WHERE employees.join_date < managers.join_date
