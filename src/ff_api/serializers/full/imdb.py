"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import Genre, Name, Crew, Episode, Principal, Rating


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class NameSerializer(serializers.HyperlinkedModelSerializer):
    knownForTitles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='title-detail'
    )

    # principals = serializers.HyperlinkedRelatedField(
    #    many=True,
    #    read_only=True,
    #    view_name='principal-detail'
    # )

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
