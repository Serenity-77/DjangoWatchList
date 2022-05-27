SELECT
	COUNT(*) AS count
FROM auth_user
WHERE MONTH(auth_user.date_joined) = %s
AND YEAR(auth_user.date_joined) = %s;
