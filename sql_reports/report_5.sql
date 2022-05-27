SELECT
	tmdb_movies.title,
	COUNT(*) AS rank
FROM watch_list JOIN tmdb_movies
ON watch_list.movie_id = tmdb_movies.id
WHERE MONTH(watch_list.date_added) = %s
AND YEAR(watch_list.date_added) = %s
GROUP BY watch_list.movie_id;
