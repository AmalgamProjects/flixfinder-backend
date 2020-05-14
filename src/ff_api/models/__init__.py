"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

"""

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

from .seen import \
    Seen

from .watch import \
    Watch
