"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from .user import \
    ShallowUserSerializer

from .favourites import \
    ShallowFavouriteSerializer, \
    ShallowFavouriteGenreSerializer

from .imdb import \
    ShallowTitleSerializer

from .seen import \
    ShallowSeenSerializer

from .watch import \
    ShallowWatchSerializer
