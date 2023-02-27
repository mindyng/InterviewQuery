-- Monthly Product Sales
-- 3
-- Question
-- Solution
-- Given a table containing data for monthly sales, write a query to find the total amount of each product sold for each month with each product as its own column in the output table.

-- Example:

-- Input:

-- monthly_sales table

-- month product_id  amount_sold
-- 2021-01-01  1 100
-- 2021-01-01  2 300
-- 2021-02-01  3 200
-- 2021-03-01  4 250
-- Output:

-- month 1 2 3 4
-- 2021-01-01  100 0 300 0
-- 2021-02-01  0 200 0 0
-- 2021-03-01  0 0 0 250

--CASE WHEN product_id = 1, etc THEN 1 ELSE 0 END AS product_id
--SUM BY month
SELECT month
, SUM(CASE WHEN product_id = 1 THEN amount_sold ELSE 0 END) AS '1'
, SUM(CASE WHEN product_id = 2 THEN amount_sold ELSE 0 END) AS '2'
, SUM(CASE WHEN product_id = 3 THEN amount_sold ELSE 0 END) AS '3'
, SUM(CASE WHEN product_id = 4 THEN amount_sold ELSE 0 END) AS '4'
FROM monthly_sales_table
GROUP BY 1
