"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..shallow import ShallowRatingSerializer
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
    
    principals = serializers.SerializerMethodField()
    averageRating = serializers.SerializerMethodField()
    numVotes = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()
    
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
            'principals',
            'averageRating',
            'numVotes',
            'directors',
            'writers',
        ]
        
    def get_principals(self, instance):
        result = []
        for principal in instance.principals.all():
            serializer = PrincipalSerializer(principal, context=self.context)
            serializedPrincipalData = serializer.data
            name = principal.nconst
            serializer = NameSerializer(name, context=self.context)
            serializedData = serializer.data
            serializedData['job'] = serializedPrincipalData['job']
            serializedData['category'] = serializedPrincipalData['category']
            result.append(serializedData)
        return result
    
    def get_averageRating(self, instance):
        try:
            result = instance.rating.first().averageRating
        except:
            result = '' 
        return result
    
    def get_numVotes(self, instance):
        try:
            result = instance.rating.first().numVotes
        except:
            result = '' 
        return result
    
    def get_directors(self, instance):
        result = []
        for crew in instance.crew.all():
            for director in crew.directors.all():
                nameSerializer = NameSerializer(director, context=self.context)
                result.append(nameSerializer.data)
        return result
    
    def get_writers(self, instance):
        result = []
        for crew in instance.crew.all():
            for writer in crew.writers.all():
                nameSerializer = NameSerializer(writer, context=self.context)
                result.append(nameSerializer.data)
        return result
    

class NameSerializer(serializers.HyperlinkedModelSerializer):
    knownForTitles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='title-detail'
    )
    
    #principals = serializers.HyperlinkedRelatedField(
    #    many=True,
    #    read_only=True,
    #    view_name='principal-detail'
    #)
    
    class Meta:
        model = Name
        fields = ['primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles']
        
    
class CrewSerializer(serializers.HyperlinkedModelSerializer):
    tconst = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='crew-detail'
    )
    
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
        fields = ['tconst', 'directors', 'writers']


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
    tconst = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rating-detail'
    )
    
    class Meta:
        model = Rating
        fields = ['tconst', 'averageRating', 'numVotes']
        

