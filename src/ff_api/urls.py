"""flixfinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/

"""

from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'favourites', views.FavouriteViewSet)
router.register(r'favouritegenres', views.FavouriteGenreViewSet)
router.register(r'name', views.NameViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'title', views.TitleViewSet)
router.register(r'crew', views.CrewViewSet)
router.register(r'episode', views.EpisodeViewSet)
router.register(r'principal', views.PrincipalViewSet)
router.register(r'rating', views.RatingViewSet)
router.register(r'seen', views.SeenViewSet)
router.register(r'watch', views.WatchViewSet)
router.register(r'moviedbtitle', views.MovieDbTitleViewSet)
router.register(r'rapidtitle', views.RapidTitleViewSet)
router.register(r'tastetitle', views.TasteTitleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('x/reviews/<str:tconst>/', views.title_reviews),
    path('x/news/<str:tconst>/', views.title_reviews),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
