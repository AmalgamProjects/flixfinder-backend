"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import Recommendation


class ShallowRecommendationSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
    )
    title = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='tconst',
    )

    primaryTitle = serializers.CharField(source="get_primary_title", read_only=True)
    backdrop_url = serializers.URLField(source="get_backdrop_url", read_only=True)
    poster_url = serializers.URLField(source="get_poster_url", read_only=True)

    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'priority', 'title', 'primaryTitle', 'backdrop_url', 'poster_url']
        read_only_fields = ['id', 'user', 'priority', 'title', 'primaryTitle', 'backdrop_url', 'poster_url']
