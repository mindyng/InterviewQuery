-- Closest SAT Scores
-- 56
-- Question
-- Solution
-- Given a table of students and their SAT test scores, write a query to return the two students with the closest test scores with the score difference.

-- If there are multiple students with the same minimum score difference, select the student name combination that is higher in the alphabet. 

-- Example:

-- Input:

-- scores table

-- Column  Type
-- id  INTEGER
-- student VARCHAR
-- score INTEGER
-- Output:

-- Column  Type
-- one_student VARCHAR
-- other_student VARCHAR
-- score_diff  INTEGER

--get table with all pair combos (INNER JOIN ON t1.id != t2.id AND t1.id < t2.id)
--get score diff
--get min score diff
--output students and score diff
WITH cte AS (
select t1.student AS one_student
, t1.score
, t2.student AS other_student
, t2.score
, abs(t1.score-t2.score) as score_diff
, RANK() OVER (ORDER BY abs(t1.score-t2.score)) as score_diff_rank
from scores t1
JOIN scores t2
ON t1.id != t2.id
AND t1.id < t2.id
)

SELECT one_student
, other_student
, score_diff
FROM cte
WHERE score_diff_rank = 1
ORDER BY 1 DESC
