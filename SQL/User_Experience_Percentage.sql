WITH cte AS
  (SELECT * ,
          LAG(position_name, 1) OVER (PARTITION BY user_id
                                      ORDER BY start_date) AS prev_position
   FROM user_experiences
   ORDER BY user_id,
            start_date)
SELECT round(SUM(CASE WHEN prev_position = 'Data Analyst'
                 AND position_name = 'Data Scientist' THEN 1 ELSE 0 END) * 1.0/COUNT(DISTINCT user_id), 3) AS percentage
FROM cte
