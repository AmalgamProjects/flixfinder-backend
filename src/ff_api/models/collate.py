"""

"""

import pprint

from ..data import movies, tv_shows
from .imdb import Title
from .mdb import MovieDbTitle
from .rapid import RapidTitle
from .tastedive import TasteTitle


def collate_title(query):
    tconst_string = ''

    if not isinstance(query, str):
        # noinspection PyBroadException
        try:
            tconst_string = query.tconst
            if not isinstance(tconst_string, str):
                return
        except Exception:
            return

    if isinstance(query, str):
        if query[:2] == 'tt':
            tconst_string = query
        else:
            instance = Title.objects.filter(primaryTitle=query).first()
            tconst_string = instance.tconst
            if not isinstance(tconst_string, str):
                return

    if isinstance(tconst_string, str) and tconst_string != '':
        rapid_instance = RapidTitle.populate_from_api(tconst_string)
        MovieDbTitle.populate_from_api(tconst_string)
        if rapid_instance is not None:
            TasteTitle.populate_from_api(rapid_instance.title)


def collate_top_rated_movies():
    data = RapidTitle.call_api('title/get-top-rated-movies', None)
    # pprint.pprint(data)
    for item in data:
        tconst_string = item['id'].split('/')[2]
        collate_title(tconst_string)


def collate_hard_coded():
    for tconst_string in tv_shows:
        collate_title(tconst_string)
    for tconst_string in movies:
        collate_title(tconst_string)
