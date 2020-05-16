"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from .user import \
    ShallowUserSerializer

from .favourites import \
    ShallowFavouriteSerializer, \
    ShallowFavouriteGenreSerializer

from .imdb import \
    VeryShallowTitleSerializer, \
    ShallowTitleSerializer, \
    ShallowRatingSerializer, \
    ShallowNameSerializer

from .recommend import \
    ShallowRecommendationSerializer

from .seen import \
    ShallowSeenSerializer

from .watch import \
    ShallowWatchSerializer
