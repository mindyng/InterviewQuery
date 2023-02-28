-- Second Longest Flight
-- 7
-- Question
-- Solution
-- Given a table of flights, extract the 2nd longest flight between each pair of cities. Order the flights by the flight id ascending.

-- Note: For any cities X and Y, (source_location=X, destination_location=Y) and (source_location=Y, destination_location=X) are counted as the same pair of cities.

-- Note: If there are fewer than two flights between two cities, there is no 2nd longest flight.

-- Example:

-- Input:

-- flights table

-- Column  Type
-- id  INTEGER
-- destination_location  VARCHAR
-- source_location VARCHAR
-- plane_id  INTEGER
-- flight_start  DATETIME
-- flight_end  DATETIME
-- Output:

-- Column  Type
-- id  INTEGER
-- destination_location  VARCHAR
-- source_location VARCHAR
-- flight_start  DATETIME
-- flight_end  DATETIME

--get cte that has x as both source/destination and vice versa for y to capture distinct x, y pairs)
--calculate time diff
--crucial fxn is window fxn partitioned by x, y and ordered in time diff DESC order
--grab second lengthiest flight duration
--order by flight id ASCENDING 

WITH cte_1 AS (
SELECT  id
, destination_location AS x
, source_location AS y
, flight_start
, flight_end
, EXTRACT(EPOCH FROM flight_end - flight_start) AS diff
, 1 AS helper
FROM flights
UNION ALL 
SELECT  id
, source_location AS x
, destination_location AS y
, flight_start
, flight_end
, EXTRACT(EPOCH FROM flight_end - flight_start) AS diff
, 2 AS helper 
FROM flights
) 

, cte_2 AS (
SELECT *
, ROW_NUMBER() OVER (PARTITION BY x, y ORDER BY diff DESC) AS ranking 
FROM cte_1 
) 

SELECT id,
 x AS destination_location
 , y AS source_location
 , flight_start
 , flight_end 
FROM cte_2 
WHERE ranking = 2 AND helper= 1
ORDER BY id ASC
