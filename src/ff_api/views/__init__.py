"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

from .auth import \
    UserViewSet, \
    GroupViewSet

from .favourites import \
    FavouriteViewSet, \
    FavouriteGenreViewSet

from .imdb import \
    GenreViewSet, \
    TitleViewSet, \
    CrewViewSet, \
    EpisodeViewSet, \
    PrincipalViewSet, \
    RatingViewSet

from .seen import \
    SeenViewSet

from .watch import \
    WatchViewSet
