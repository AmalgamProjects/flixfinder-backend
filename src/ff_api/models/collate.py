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
