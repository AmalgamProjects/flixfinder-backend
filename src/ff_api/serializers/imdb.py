"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

import hashlib

from ff_api.models import Genre, Title, Crew, Episode, Principal, Rating
from rest_framework import serializers


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']
        

class TitleSerializer(serializers.HyperlinkedModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    
    class Meta:
        model = Title
        fields = ['titleType', 'primaryTitle', 'startYear', 'endYear', 'runtimeMinutes', 'genres']
        

class CrewSerializer(serializers.HyperlinkedModelSerializer):
    directors = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='name-detail'
    )
    
    writers = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='name-detail'
    )
    
    class Meta:
        model = Crew
        fields = ['directors', 'writers']
        
class EpisodeSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Episode
        fields = ['seasonNumber', 'episodeNumber']
        
        
class PrincipalSerializer(serializers.HyperlinkedModelSerializer):
    nconst = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='name-detail'
    )
        
    class Meta:
        model = Principal
        fields = ['ordering', 'nconst', 'category', 'job', 'characters']
        
        
class RatingSerializer(serializers.HyperlinkedModelSerializer):
        
    class Meta:
        model = Rating
        fields = ['averageRating', 'numVotes']
        
        