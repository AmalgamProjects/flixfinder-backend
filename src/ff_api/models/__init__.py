"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

"""

from .favourites import \
    Favourite

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
