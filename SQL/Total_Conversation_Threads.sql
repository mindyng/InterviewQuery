-- Total Conversation Threads
-- 3
-- Question
-- Solution
-- Let’s say you work for Meta. You are given the table messenger_sends. Find the total number of unique conversation threads.

-- Note: In some entries, the receiver_id and sender_id are switched from the initial message. These entries should be treated as part of the same thread.

-- Example:

-- Input:

-- messenger_sends table

-- Column  Type
-- id  INTEGER
-- receiver_id INTEGER
-- sender_id INTEGER
-- Output:

-- Column  Type
-- total_conv_threads  INTEGER

SELECT COUNT(DISTINCT 
    LEAST(sender_id, receiver_id),
    GREATEST(sender_id, receiver_id)
) AS total_conv_threads
FROM messenger_sends
