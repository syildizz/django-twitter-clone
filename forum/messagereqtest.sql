-- Traverse through all parent messages and aggregate them recursively
WITH RECURSIVE replies_to(id) AS (
    SELECT forum_message.reply_to_id FROM forum_message WHERE forum_message.id = %s
    UNION
        SELECT forum_message.reply_to_id
        FROM forum_message, replies_to
        WHERE forum_message.id = replies_to.id
)
SELECT *
FROM forum_message
WHERE forum_message.id IN replies_to

-- Traverse through specified number of parent messages and aggregate them recursively
WITH RECURSIVE replies_to(id) AS (
    SELECT forum_message.reply_to_id FROM forum_message WHERE forum_message.id = %s
    UNION
        SELECT forum_message.reply_to_id
        FROM forum_message, replies_to
        WHERE forum_message.id = replies_to.id
        LIMIT %s
)
SELECT *
FROM forum_message
WHERE forum_message.id IN replies_to

msg = Message.objects.raw('WITH RECURSIVE replies_to(id) AS ( SELECT forum_message.reply_to_id FROM forum_message WHERE forum_message.id = %s UNION SELECT forum_message.reply_to_id FROM forum_message, replies_to WHERE forum_message.id = replies_to.id) SELECT * FROM forum_message WHERE forum_message.id IN replies_to', [2])
from django.db import connection, reset_queries
