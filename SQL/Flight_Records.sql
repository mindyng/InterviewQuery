-- Flight Records
-- 35
-- Question
-- Solution
-- Write a query to create a new table, named flight routes, that displays unique pairs of two locations.

-- Example:

-- Note: Duplicate pairs from the flights table, such as Dallas to Seattle and Seattle to Dallas, should have one entry in the flight routes table.

-- flights table

-- Column  Type
-- id  INTEGER
-- source_location VARCHAR
-- destination_location  VARCHAR
-- Output:

-- Column  Type
-- destination_one VARCHAR
-- destination_two VARCHAR

--union all on flipped source and destination
--filter out dup's by getting alphabetical order of pairs
--get distinct pairs
WITH cte AS (SELECT source_location 
, destination_location 
FROM flights
 
UNION ALL

SELECT destination_location 
, source_location 

FROM flights)

SELECT DISTINCT source_location AS destination_one
, destination_location AS destination_two 
FROM cte
--WHERE source_location < destination_location
