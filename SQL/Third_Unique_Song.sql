--left join users to song plays
--get earliest time this each song was played (correcting for window fxn on NULLs!)
--get third song
--final output should only have non-null from 3rd played song
--get max on case when to have one row per user name
WITH song_play AS (
SELECT name
, song_name
, date_played
, CASE WHEN song_name IS NULL THEN 1 ELSE ROW_NUMBER() OVER (PARTITION BY user_id, song_name ORDER BY date_played) END AS song_play_num
FROM users
LEFT JOIN song_plays ON song_plays.user_id = users.id
-- ORDER BY 1
-- , 2
-- , 3
)

, song_play_order AS (
SELECT name
, song_name
, date_played
, song_play_num
, RANK() OVER (PARTITION BY name ORDER BY date_played) AS song_play_order
FROM song_play
WHERE song_play_num = 1
-- ORDER BY 1
-- , 3
)

SELECT name
, MAX(CASE WHEN song_play_order = 3 THEN date_played 
ELSE NULL END) AS date_played
, MAX(CASE WHEN song_play_order = 3 THEN song_name 
ELSE NULL END) AS  song_name
FROM song_play_order
GROUP BY 1
