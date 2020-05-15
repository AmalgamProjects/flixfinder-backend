"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from ..models import \
    Genre, \
    Title, \
    Name, \
    Crew, \
    Episode, \
    Principal, \
    Rating
from ..serializers import \
    GenreSerializer, \
    TitleSerializer, \
    NameSerializer, \
    CrewSerializer, \
    EpisodeSerializer, \
    PrincipalSerializer, \
    RatingSerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'
    filter_fields = ('name')
    ordering_fields = ('name')
    ordering = ('name',)


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all().order_by('primaryTitle')
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'tconst'
    filter_fields = ('titleType', 'primaryTitle', 'genres')
    ordering_fields = ('primaryTitle')
    ordering = ('primaryTitle',)
    search_fields = ['primaryTitle', 'titleType']
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ['titleType']


class NameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Name.objects.all()
    serializer_class = NameSerializer
    permission_classes = [permissions.IsAuthenticated]


class CrewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [permissions.IsAuthenticated]


class EpisodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrincipalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer
    permission_classes = [permissions.IsAuthenticated]


class RatingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
