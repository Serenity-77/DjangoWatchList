SELECT
	auth_user.username,
	FLOOR(AVG(a.total)) AS average
FROM
(
	SELECT
		COUNT(*) AS total,
		watch_list.user_id
	FROM watch_list
	GROUP BY watch_list.user_id, DATE(watch_list.date_added)
)a JOIN auth_user
ON a.user_id = auth_user.id
GROUP BY a.user_id;
