"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import MovieDbTitle

class MovieDbTitleSerializer(serializers.HyperlinkedModelSerializer):
    tconst = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='moviedbtitle-detail'
    )

    class Meta:
        model = MovieDbTitle
        fields = [
            'id', 
            'created', 
            'updated', 
            'tconst', 
            'title',
            'overview',
            'vote_average',
            'vote_count',
            'backdrop_url',
            'poster_url'
        ]