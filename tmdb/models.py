from django.db import models
from django.contrib.auth.models import User as DjangoUserModel


class TmdbMovie(models.Model):

    class Meta:
        db_table = "tmdb_movies"

    adult = models.BooleanField(default=False)
    backdrop_path = models.CharField(max_length=150, null=True)
    movie_id = models.PositiveIntegerField(null=True, unique=True)
    media_type = models.CharField(max_length=15, null=True)
    original_language = models.CharField(max_length=5, null=True)
    original_title = models.CharField(max_length=150, null=True)
    overview = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    poster_path = models.CharField(max_length=150, null=True)
    release_date = models.DateField(null=True)
    title = models.CharField(max_length=150, null=True)
    video = models.BooleanField(default=False)
    vote_average = models.FloatField(null=True)
    vote_count = models.PositiveIntegerField(null=True)


class WatchList(models.Model):

    class Meta:
        db_table = "watch_list"
        constraints = [
            models.UniqueConstraint(fields=("user_id", "movie_id", ), name="user_movie_unique")
        ]

    user = models.ForeignKey(DjangoUserModel, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(TmdbMovie, on_delete=models.CASCADE, null=True)
    note = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now=True)
