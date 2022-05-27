from django.test import TestCase, Client
from django.contrib.auth.models import User as DjangoUserModel
from django.contrib.auth import SESSION_KEY

from .models import TmdbMovie, WatchList

class BaseWatchListTest(TestCase):

    def setUp(self):
        self.client = Client()

        DjangoUserModel.objects.create_user(
            username="harianja",
            password="123456")

    def _do_test_validation(self, url, parameters, expected_messages, method="POST", expected_status=422, login=True):
        if login:
            self.client.post("/", {'username': "harianja", 'password': "123456"})

        response = getattr(self.client, method.lower())(url, parameters)

        self.assertEquals(expected_status, response.status_code)
        self.assertEquals(expected_messages, response.content.decode())
        self.assertEquals("text/plain", response.headers['Content-Type'])



class WatchListAddTest(BaseWatchListTest):

    def test_incomplete_parameters(self):
        self._do_test_validation('/watchlist/', {}, "Incomplete Parameters")

    def test_movie_does_not_exist(self):
        self._do_test_validation(
            '/watchlist/',
            {'movie_id': '55'},
            "Movie Does Not Exist",
            expected_status=404)

    def test_add_success(self):
        movie = TmdbMovie(title="Some Movie")
        movie.save()

        self.client.post("/", {'username': "harianja", 'password': "123456"})

        response = self.client.post("/watchlist/", {'movie_id': movie.id})

        watch_list = WatchList.objects.raw("SELECT * FROM watch_list WHERE user_id=%d AND movie_id=%s" % (
            int(self.client.session[SESSION_KEY]), movie.id
        ))

        self.assertEquals(b"", response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals(movie.id, watch_list[0].movie_id)

    def test_add_already_exist(self):
        movie = TmdbMovie(title="Some Movie")
        movie.save()

        self.client.post("/", {'username': "harianja", 'password': "123456"})

        self.client.post("/watchlist/", {'movie_id': movie.id})

        self._do_test_validation(
            '/watchlist/',
            {'movie_id': movie.id},
            "Watch List Already Exist",
            expected_status=409, login=False)


class WatchListEditTest(BaseWatchListTest):

    def test_edit_watch_list_does_not_exist(self):
        self._do_test_validation(
            '/watchlist/55',
            {'movie_id': '44'},
            "Watch List Does Not Exist",
            expected_status=404)

    def test_edit_watch_list_already_exist(self):
        titles = ["Some Movie 1", "Some Movie 2"]
        movies = []

        for title in titles:
            movie = TmdbMovie(title=title)
            movie.save()
            movies.append(movie)

        self.client.post("/", {'username': "harianja", 'password': "123456"})
        user = DjangoUserModel.objects.get(pk=int(self.client.session[SESSION_KEY]))

        watch_lists = []
        for movie in movies:
            w = WatchList(user=user, movie=movie)
            w.save()
            watch_lists.append(w)

        self._do_test_validation(
            '/watchlist/' + str(watch_lists[0].id),
            {'movie_id': movies[1].id},
            "Watch List Already Exist",
            expected_status=409,
            login=False)

    def test_edit_watch_list_movie_does_not_exist(self):
        movie = TmdbMovie(title="Some Movie")
        movie.save()

        self.client.post("/", {'username': "harianja", 'password': "123456"})
        user = DjangoUserModel.objects.get(pk=int(self.client.session[SESSION_KEY]))

        watch_list = WatchList(user=user, movie=movie)
        watch_list.save()

        self._do_test_validation(
            '/watchlist/' + str(watch_list.id),
            {'movie_id': 77},
            "Movie Does Not Exist",
            expected_status=404,
            login=False)


    def test_edit_success(self):
        titles = ["Some Movie 1", "Some Movie 2"]
        movies = []

        for title in titles:
            movie = TmdbMovie(title=title)
            movie.save()
            movies.append(movie)

        self.client.post("/", {'username': "harianja", 'password': "123456"})
        user = DjangoUserModel.objects.get(pk=int(self.client.session[SESSION_KEY]))

        watch_list = WatchList(user=user, movie=movies[0])
        watch_list.save()

        response = self.client.post("/watchlist/" + str(watch_list.id), {'movie_id': movies[1].id})

        watch_list = WatchList.objects.raw("SELECT * FROM watch_list WHERE user_id=%d AND movie_id=%s" % (
            user.id, movie.id
        ))

        self.assertEquals(b"", response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals(movies[1].id, watch_list[0].movie_id)


class WatchListDeleteTest(BaseWatchListTest):

    def test_incomplete_parameters(self):
        self._do_test_validation('/watchlist/', {}, "Incomplete Parameters", method="delete")

    def test_watch_list_does_not_exist(self):
        self._do_test_validation(
            '/watchlist/55',
            {},
            "Watch List Does Not Exist",
            method="delete",
            expected_status=404)

    def test_delete_success(self):
        movie = TmdbMovie(title="Some Movie")
        movie.save()

        self.client.post("/", {'username': "harianja", 'password': "123456"})
        user = DjangoUserModel.objects.get(pk=int(self.client.session[SESSION_KEY]))

        watch_list = WatchList(user=user, movie=movie)
        watch_list.save()

        response = self.client.delete("/watchlist/" + str(watch_list.id), {'movie_id': movie.id})

        count = WatchList.objects.count()

        self.assertEquals(b"", response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, count)
