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
    NameSerializer, \
    CrewSerializer, \
    EpisodeSerializer, \
    PrincipalSerializer, \
    RatingSerializer

from .mdb import \
    MovieDbTitleSerializer

from .rapid import \
    RapidTitleSerializer

from .recommend import \
    RecommendationSerializer

from .seen import \
    SeenSerializer

from .title import \
    TitleSerializer

from .tastedive import \
    TasteTitleSerializer

from .user import \
    UserSerializer

from .watch import \
    WatchSerializer
