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
    NameViewSet, \
    CrewViewSet, \
    EpisodeViewSet, \
    PrincipalViewSet, \
    RatingViewSet

from .mdb import \
    MovieDbTitleViewSet, \
    title_reviews

from .rapid import \
    RapidTitleViewSet

from .recommend import \
    RecommendationViewSet, \
    titles_like_this

from .seen import \
    SeenViewSet

from .tastedive import \
    TasteTitleViewSet

from .watch import \
    WatchViewSet
