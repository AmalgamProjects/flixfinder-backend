"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import Genre, Title, Name, Crew, Episode, Principal, Rating


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class TitleSerializer(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(
    #    view_name='title-detail',
    #    lookup_field='tconst'
    #)

    id = serializers.SlugField(source='tconst')

    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    
    actors = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='name-detail',
    )

    class Meta:
        model = Title
        fields = [
            'id', 
            'titleType', 
            'primaryTitle', 
            'startYear', 
            'endYear', 
            'runtimeMinutes', 
            'genres',
            'actors'
        ]

class NameSerializer(serializers.HyperlinkedModelSerializer):
    knownForTitles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='title-detail'
    )
    
    class Meta:
        model = Name
        fields = ['primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles']
        
    
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
        view_name='principal-view'
    )

    class Meta:
        model = Principal
        fields = ['ordering', 'nconst', 'category', 'job', 'characters']


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ['averageRating', 'numVotes']
