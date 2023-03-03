-- Search Ratings
-- 33
-- Question
-- Solution
-- You’re given a table that represents search results from searches on Facebook. The query column is the search term, the position column represents each position the search result came in, and the rating column represents the human rating of the search result from 1 to 5 where 5 is high relevance and 1 is low relevance.

-- Example:

-- Input:

-- search_results table

-- Column  Type
-- query VARCHAR
-- result_id INTEGER
-- position  INTEGER
-- rating  INTEGER
-- Write a query to compute a metric to measure the quality of the search results for each query. 

-- You want to be able to compute a metric that measures the precision of the ranking system based on position. For example, if the results for dog and cat are…

-- query result_id position  rating  notes
-- dog 1000  1 2 picture of hotdog
-- dog 998 2 4 dog walking
-- dog 342 3 1 zebra
-- cat 123 1 4 picture of cat
-- cat 435 2 2 cat memes
-- cat 545 3 1 pizza shops
-- …we would rank ‘cat’ as having a better search result ranking precision than ‘dog’ based on the correct sorting by rating.

-- Write a query to create a metric that can validate and rank the queries by their search result precision. Round the metric (avg_rating column) to 2 decimal places.

-- Output:

-- Column  Type
-- query VARCHAR
-- avg_rating  FLOAT

--get average rating per search query
--need to account for position of rank so multiply avg ranking by inverse of position
--for higher rankings (lower number positions) want rating to count the most. hence, the weight is inverse of position. higher the position (lower the rank) avg rating is counted less
SELECT query
, ROUND(AVG((1/position) * rating), 2) AS avg_rating
FROM search_results
GROUP BY 1
