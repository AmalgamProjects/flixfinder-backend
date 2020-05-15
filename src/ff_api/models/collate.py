"""

"""

import pprint

from .imdb import Title
from .mdb import MovieDbTitle
from .rapid import RapidTitle
from .tastedive import TasteTitle


def collate_title(query):
    instance = query
    if isinstance(instance, str):
        instance = Title.objects.filter(tconst=instance).first()
        if instance is None:
            instance = Title.objects.filter(primaryTitle=instance).first()
    if instance is not None:
        RapidTitle.populate_from_api(instance.tconst)
        MovieDbTitle.populate_from_api(instance.primaryTitle)
        TasteTitle.populate_from_api(instance.primaryTitle)
    else:
        pprint.pprint("Title not found in our database: %s" % query)
        # if isinstance(query, str):
        #     MovieDbTitle.populate_from_api(query)
        #     TasteTitle.populate_from_api(query)


def collate_top_rated_movies():
    data = RapidTitle.call_api('title/get-top-rated-movies', None)
    # pprint.pprint(data)
    for item in data:
        tconst_string = item['id'].split('/')[2]
        if not Title.objects.filter(tconst=tconst_string).exists():
            RapidTitle.create_title_from_rapid(tconst_string)
    for item in data:
        tconst_string = item['id'].split('/')[2]
        collate_title(tconst_string)
