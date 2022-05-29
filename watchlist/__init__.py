import os
import requests
import json

from django.conf import settings
from utils.utils import get_tmdb_configuration_url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchlist.settings')

def fetch_tmdb_configuration():
    resp = requests.get(get_tmdb_configuration_url())
    configuration = json.loads(resp.text)
    settings.TMDB_API_CONFIGURATION = configuration


fetch_tmdb_configuration()
