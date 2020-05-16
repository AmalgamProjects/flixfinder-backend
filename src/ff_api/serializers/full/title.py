"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

import json

from codecs import encode, decode
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
    directors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()

    averageRating = serializers.FloatField(source="get_vote_average")
    numVotes = serializers.IntegerField(source="get_vote_count")

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

    def _no_fake_null(self, string):
        if string == '\\N':
            return None
        return string

    def _fixup_characters(self, string):
        list = self._no_fake_null(string)
        if list is not None:
            list = decode(encode(list, 'latin-1', 'backslashreplace'), 'unicode-escape')
            list = json.loads(list)
        return list

    def get_principals(self, instance):
        result = []
        for principal in instance.principals.all():
            principal_data = PrincipalSerializer(principal, context=self.context).data
            name_data = NameSerializer(principal.nconst, context=self.context).data
            name_data['job'] = self._no_fake_null(principal_data['job'])
            name_data['category'] = self._no_fake_null(principal_data['category'])
            name_data['characters'] = self._fixup_characters(principal_data['characters'])
            result.append(name_data)
        return result

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
