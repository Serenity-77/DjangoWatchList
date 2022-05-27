import requests
import json

from django.conf import settings
from utils.utils import get_tmdb_configuration_url

def fetch_tmdb_configuration():
    resp = requests.get(get_tmdb_configuration_url())
    configuration = json.loads(resp.text)
    settings.TMDB_API_CONFIGURATION = configuration


fetch_tmdb_configuration()
