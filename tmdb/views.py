from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from django.shortcuts import render

from .forms import MoviesForm, WatchListForm
from .models import TmdbMovie, WatchList as WatchListModel
from operation.views import OperationMixin
# from operation.models import Operation


class UserWatchList(LoginRequiredMixin, View, OperationMixin):

    # operation = Operation.READ

    def get(self, request):
        results = WatchListModel.objects.select_related(
            "user", "movie"
        ).filter(user__id=request.user.id)

        if len(results) == 0:
            movies = []
        else:
            movies = [[result.id, result.note, result.movie] for result in results]

        response = render(request, "watchlist.html", {'movies': movies})

        self.save_operation(request)

        return response



class WatchList(LoginRequiredMixin, View, OperationMixin):

    # operation = Operation.ADD

    def get(self, request):
        form = MoviesForm(request.GET)

        if not form.is_valid():
            return HttpResponse("Incomplete Parameters", status=422, content_type="text/plain")

        cleaned_data = form.cleaned_data
        results = TmdbMovie.objects.raw("SELECT * FROM tmdb_movies OFFSET %d LIMIT %d" % (cleaned_data['start'], cleaned_data['length']))
        recordsTotal = TmdbMovie.objects.count()

        resp = []

        for result in results:
            d = [
                result.title,
                result.overview,
                "Yes" if result.adult else "No",
                result.popularity,
                result.release_date,
                result.vote_count,
                result.id
            ]

            resp.append(d)

        recordsFiltered = len(resp)

        return JsonResponse({
            'draw': int(request.GET['draw']),
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsTotal,
            'data': resp
        })

    def post(self, request, **kwargs):
        form = WatchListForm(request.POST)

        if not form.is_valid():
            return HttpResponse("Incomplete Parameters", status=422, content_type="text/plain")

        cleaned_data = form.cleaned_data
        response = None

        if 'wlid' in kwargs:
            self.operation = Operation.EDIT

            watch_list_id = kwargs['wlid']
            try:
                watch_list = WatchListModel.objects.get(pk=watch_list_id)
            except WatchListModel.DoesNotExist:
                return HttpResponse("Watch List Does Not Exist", status=404, content_type="text/plain")

            try:
                movie_id = cleaned_data['movie_id']
            except KeyError:
                movie_id = None

            try:
                note = cleaned_data['note']
            except KeyError:
                note = None

            if movie_id:
                try:
                    movie = TmdbMovie.objects.get(pk=movie_id)
                except TmdbMovie.DoesNotExist:
                    return HttpResponse("Movie Does Not Exist", status=404, content_type="text/plain")

                watch_list.movie = movie

            watch_list.note = note

            try:
                watch_list.save()
            except IntegrityError as e:
                if hasattr(e, "args") and e.args[0] == 1062:
                    return HttpResponse("Watch List Already Exist", status=409, content_type="text/plain")

            response = HttpResponse(content_type="text/plain")

        else:
            try:
                movie_id = cleaned_data['movie_id']
            except KeyError:
                movie_id = None

            if not movie_id:
                return HttpResponse("Incomplete Parameters", status=422, content_type="text/plain")

            try:
                movie = TmdbMovie.objects.get(pk=movie_id)
            except TmdbMovie.DoesNotExist:
                return HttpResponse("Movie Does Not Exist", status=404, content_type="text/plain")

            cleaned_data = form.cleaned_data
            cleaned_data['user_id'] = request.user.id

            watch_list = WatchListModel(**cleaned_data)

            try:
                watch_list.save()
            except IntegrityError as e:
                if hasattr(e, "args") and e.args[0] == 1062:
                    return HttpResponse("Watch List Already Exist", status=409, content_type="text/plain")

            response = HttpResponse(content_type="text/plain")

        self.save_operation(request)

        return response

    def delete(self, request, **kwargs):
        self.operation = Operation.DELETE

        try:
            wlid = kwargs['wlid']
        except KeyError:
            return HttpResponse(
                "Incomplete Parameters", status=422, content_type="text/plain")

        try:
            watch_list = WatchListModel.objects.get(pk=wlid)
        except WatchListModel.DoesNotExist:
            return HttpResponse(
                "Watch List Does Not Exist", status=404, content_type="text/plain")

        watch_list.delete()

        response = HttpResponse(content_type="text/plain")

        self.save_operation(request)

        return response
