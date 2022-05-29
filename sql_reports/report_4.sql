SELECT
	auth_user.username,
	COUNT(*) AS total
FROM watch_list JOIN auth_user
ON watch_list.user_id = auth_user.id
GROUP BY auth_user.username;
