SELECT
	operations.operation_name,
	COALESCE(a.active_count, 0) AS active_count
FROM
(
	SELECT
		COUNT(*) AS active_count,
		operation_detail.operation_id
	FROM operations JOIN operation_detail
	ON operations.id = operation_detail.operation_id
	WHERE DATE(operation_detail.operation_date) = DATE(NOW())
	GROUP BY operation_detail.operation_id
)a
RIGHT JOIN operations
ON a.operation_id = operations.id;
