SELECT
	auth_user.username,
	c.average
FROM
(
	SELECT
		b.user_id,
		FLOOR(AVG(b.total)) AS average
	FROM
	(
		SELECT
			COUNT(*) AS total,
			a.user_id
		FROM
		(
			SELECT
				watch_list.user_id,
				watch_list.date_added
			FROM watch_list
		)a
		GROUP BY a.user_id, DATE(a.date_added)
	)b
	GROUP BY b.user_id
)c JOIN auth_user
ON c.user_id = auth_user.id;
