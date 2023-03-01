-- Total Time in Flight
-- 6
-- Question
-- Solution
-- Let’s say you work in air traffic control. You are given the table below containing information on flights between two cities.

-- Write a query to find out how much time, in minutes (rounded down), each plane spent in the air each day.

-- Note: Both cities are in the same time zone, so you do not need to worry about converting time zones.

-- flights table

-- Example:

-- Input:

-- Columns Type
-- id  INTEGER
-- destination_location  VARCHAR
-- source_location VARCHAR
-- plane_id  INTEGER
-- flight_start  DATETIME
-- flight_end  DATETIME
-- Output:

-- Columns Type
-- plane_id  INTEGER
-- calendar_day  VARCHAR
-- time_in_min INTEGER
-- Please give calendar_day in the format YYYY-MM-DD

--need to union 3 cte's
--first cte: sum of time diff of start and end times on same day
--second and third cte's: start and end times on diff days:
--second cte: start to midnight
--third cte: midnight to end
--filter on time diff > 0 and sum the time diff column by plane id

WITH cte AS (

SELECT
    DATE(flight_start) AS calendar_day,
    plane_id,
    SUM(EXTRACT(EPOCH FROM (flight_end - flight_start))/60) AS time
FROM flights
WHERE DATE(flight_start) = DATE(flight_end)
GROUP BY 1,2

UNION ALL

SELECT
    DATE(flight_start) AS calendar_day,
    plane_id,
    SUM(EXTRACT(EPOCH FROM (DATE(flight_end) - flight_start))/60) AS time
FROM flights
WHERE DATE(flight_start) < DATE(flight_end)
GROUP BY 1,2

UNION ALL

SELECT
    DATE(flight_end) AS calendar_day,
    plane_id,
    SUM(EXTRACT(EPOCH FROM (flight_end - DATE(flight_end)))/60) AS time
FROM flights
WHERE DATE(flight_start) < DATE(flight_end)
GROUP BY 1,2
    )
    
SELECT
    plane_id,
    calendar_day,
    SUM(time) AS time_in_min
FROM cte
GROUP BY 1,2
HAVING SUM(time) > 0
ORDER BY 1,2
