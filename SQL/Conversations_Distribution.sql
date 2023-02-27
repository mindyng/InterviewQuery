-- Conversations Distribution
-- 20
-- Question
-- Solution
-- We have a table that represents the total number of messages sent between two users by date on messenger.

-- What are some insights that could be derived from this table?

-- What do you think the distribution of the number of conversations created by each user per day looks like?

-- Write a query to get the distribution of the number of conversations created by each user by day in the year 2020.

-- Example:

-- Input:

-- messages table

-- Column  Type
-- id  INTEGER
-- date  DATETIME
-- user1 INTEGER
-- user2 INTEGER
-- msg_count INTEGER

-- 1. Top-level insights that can be derived from this table are the total number of messages being sent per day, number of conversations being started, and the average number of messages per conversation.

-- If we think about business-facing metrics, we can start analyzing them by including time series.

-- How many more conversations are being started over the past year compared to now? Do more conversations between two users indicate a closer friendship versus the depth of the conversation in total messages? 

-- 2. The distribution would be likely skewed to the right or bimodal. If we think about the probability for a user to have a conversation with more than one additional person per day, would that likely be going up or down?

-- The peak is probably around one to five new conversations a day. After that, we would see a large decrease with a potential bump of very active users that may be using messenger tools for work.

-- 3. Given we just want to count the number of conversations, we can ignore the message count and focus on getting our key metric of a number of new conversations created by day in a single query.

-- To get this metric, we have to group by the date field and then group by the distinct number of users messaged. Afterward, we can then group by the frequency value and get the total count of that as our distribution.

--get year 2020
--by user1, get count of convos by aggregating on user2
--get freq by aggregating on convos count

WITH convos AS (
SELECT user1
, DATE(date)
, COUNT(DISTINCT user2) AS num_coversations
FROM messages
WHERE EXTRACT(YEAR FROM date) = 2020
GROUP BY 1
, 2
ORDER BY 3 DESC
) 

SELECT num_coversations
, COUNT(*) AS frequency
FROM convos
GROUP BY 1
