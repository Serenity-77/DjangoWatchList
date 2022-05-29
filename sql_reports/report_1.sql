SELECT
	COUNT(*) AS count
FROM auth_user
WHERE TO_CHAR(auth_user.date_joined, 'MM-YYYY') = %s
AND auth_user.is_superuser='0';
