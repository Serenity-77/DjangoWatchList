SELECT
	tmdb_movies.title,
	a.rank
FROM
(
	SELECT
		watch_list.movie_id,
		COUNT(*) AS rank
	FROM watch_list
	WHERE TO_CHAR(watch_list.date_added, 'MM-YYYY') = %s
	GROUP BY watch_list.movie_id
)a JOIN tmdb_movies
ON a.movie_id = tmdb_movies.id
