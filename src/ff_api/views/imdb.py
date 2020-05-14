from ff_api.models import Genre, Title, Crew, Episode, Principal, Rating
from rest_framework import viewsets
from rest_framework import permissions

from ..serializers import GenreSerializer, TitleSerializer, CrewSerializer, EpisodeSerializer, PrincipalSerializer, RatingSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'
    filter_fields = ('name')
    ordering_fields = ('name')
    ordering = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Title.objects.all().order_by('primaryTitle')
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'primaryTitle'
    filter_fields = ('titleType', 'primaryTitle', 'genres')
    ordering_fields = ('primaryTitle')
    ordering = ('primaryTitle',)
    

class CrewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class EpisodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class PrincipalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
