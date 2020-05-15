"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

"""

from .collate import collate_title

# noinspection PyUnresolvedReferences
from django.contrib.auth.models import \
    User, \
    Group

from .favourites import \
    Favourite, \
    FavouriteGenre

from .imdb import \
    Title, \
    Name, \
    Crew, \
    Episode, \
    Principal, \
    Rating, \
    Genre

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

from .watch import \
    Watch
