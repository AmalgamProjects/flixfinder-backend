"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from .favourites import \
    FavouriteSerializer, \
    FavouriteGenreSerializer

from .group import \
    GroupSerializer

from .imdb import \
    GenreSerializer, \
    TitleSerializer, \
    NameSerializer, \
    CrewSerializer, \
    EpisodeSerializer, \
    PrincipalSerializer, \
    RatingSerializer

from .seen import \
    SeenSerializer

from .user import \
    UserSerializer

from .watch import \
    WatchSerializer
