"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from .imdb import PrincipalSerializer, NameSerializer
from ...models import Title


# noinspection PyBroadException,PyPep8Naming,PyMethodMayBeStatic
class TitleSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #    view_name='title-detail',
    #    lookup_field='tconst'
    # )

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

    image_url = serializers.URLField(source="get_image_url")
    backdrop_url = serializers.URLField(source="get_backdrop_url")
    poster_url = serializers.URLField(source="get_poster_url")
    wikipedia_url = serializers.URLField(source="get_wikipedia_url")
    youtube_url = serializers.URLField(source="get_youtube_url")
    summary = serializers.CharField(source='get_summary')

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
            'image_url',
            'backdrop_url',
            'poster_url',
            'wikipedia_url',
            'youtube_url',
            'summary',
            # 'tastedb',
            # 'moviedb',
            # 'rapid',
        ]

    def get_principals(self, instance):
        result = []
        for principal in instance.principals.all():
            principal_data = PrincipalSerializer(principal, context=self.context).data
            name_data = NameSerializer(principal.nconst, context=self.context).data
            name_data['job'] = principal_data['job']
            name_data['category'] = principal_data['category']
            result.append(name_data)
        return result

    def get_averageRating(self, instance):
        try:
            return instance.rating.first().averageRating
        except Exception:
            return 0.0

    def get_numVotes(self, instance):
        try:
            return instance.rating.first().numVotes
        except Exception:
            return 0

    def get_directors(self, instance):
        result = []
        for crew in instance.crew.all():
            for director in crew.directors.all():
                result.append(NameSerializer(director, context=self.context).data)
        return result

    def get_writers(self, instance):
        result = []
        for crew in instance.crew.all():
            for writer in crew.writers.all():
                result.append(NameSerializer(writer, context=self.context).data)
        return result
