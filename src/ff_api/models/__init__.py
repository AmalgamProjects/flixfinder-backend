"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

"""

from .collate import \
    collate_title, \
    collate_top_rated_movies, \
    collate_hard_coded

from .external import \
    ExternalResponse

# noinspection PyUnresolvedReferences
from django.contrib.auth.models import \
    User, \
    Group

from .favourites import \
    Favourite, \
    FavouriteGenre

from .imdb import \
    Name, \
    Crew, \
    Episode, \
    Principal, \
    Rating

from .mdb import \
    MovieDbTitle

from .rapid import \
    RapidTitle

from .recommend import \
    Recommendation

from .seen import \
    Seen

from .tastedive import \
    TasteTitle

from .title import \
    Title, \
    Genre

from .watch import \
    Watch
