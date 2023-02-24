--fitler on 6,6,20 and action = like
--get distinct num users

SELECT COUNT(DISTINCT user_id) AS num_users_gave_like
FROM events
WHERE DATE(created_at) = '2020-06-06'
AND action = 'like'
