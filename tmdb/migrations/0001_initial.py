# Generated by Django 3.2.13 on 2022-05-26 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TmdbMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult', models.BooleanField(default=False)),
                ('backdrop_path', models.CharField(max_length=150, null=True)),
                ('movie_id', models.PositiveIntegerField(null=True)),
                ('media_type', models.CharField(max_length=15, null=True)),
                ('original_language', models.CharField(max_length=5, null=True)),
                ('original_title', models.CharField(max_length=150, null=True)),
                ('overview', models.TextField(null=True)),
                ('popularity', models.FloatField(null=True)),
                ('poster_path', models.CharField(max_length=150, null=True)),
                ('release_date', models.DateField(null=True)),
                ('title', models.CharField(max_length=150, null=True)),
                ('video', models.BooleanField(default=False)),
                ('vote_average', models.FloatField(null=True)),
                ('vote_count', models.PositiveIntegerField(null=True)),
            ],
            options={
                'db_table': 'tmdb_movies',
            },
        ),
    ]