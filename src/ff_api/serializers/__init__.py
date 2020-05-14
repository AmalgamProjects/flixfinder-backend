"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from .auth import \
    UserSerializer, \
    GroupSerializer

from .favourites import \
    FavouriteSerializer

from .imdb import \
    GenreSerializer, \
    TitleSerializer, \
    CrewSerializer, \
    EpisodeSerializer, \
    PrincipalSerializer, \
    RatingSerializer

from .seen import \
    SeenSerializer

from .watch import \
    WatchSerializer
