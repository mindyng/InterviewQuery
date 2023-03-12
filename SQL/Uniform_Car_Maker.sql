-- Uniform Car Maker
-- 2
-- Question
-- Solution
-- Submissions
-- Editor
-- Details
-- Stats
-- Given a table of cars with columns id and make, write a query that outputs a random manufacturer’s name with an equal probability of selecting any name.

-- Input:

-- cars table

-- id  make
-- 1 Ford
-- 2 Toyota
-- 3 Toyota
-- 4 Honda
-- 5 Honda
-- 6 Honda
-- Output:

-- Column  Type
-- make  Text

--THIS IS IN MYSQL - not Postgres

--select unique car makers
--randomize them
--output 1 of them

SELECT 
    make
FROM
    cars
GROUP BY
    make
ORDER BY
    RAND()
LIMIT 1;
