import requests
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.utils import IntegrityError

from tmdb.models import TmdbMovie


class Command(BaseCommand):
    help = 'Fetch TMDB Movie List'

    def handle(self, *args, **kwargs):
        counter = 1
        while self._do_fetch(counter) > 0:
            counter += 1


    def _do_fetch(self, counter):
        url = "%s/%d?api_key=%s" % (settings.TMDB_API_LIST_URL.rstrip("/"), counter, settings.TMDB_API_KEY)

        resp = requests.get(url)
        movie_list = json.loads(resp.text)

        for info in movie_list['results']:
            info['movie_id'] = info['id']
            del info['id']
            try:
                del info['genre_ids']
            except:
                pass

            model = TmdbMovie(**info)

            try:
                model.save()
            except Exception as e:
                self.stderr.write("Failed to add %s, error: %s\n" % (info['title'], e))
            else:
                self.stdout.write("Adding %s\n" % (info['title']))

        return movie_list['total_results']
