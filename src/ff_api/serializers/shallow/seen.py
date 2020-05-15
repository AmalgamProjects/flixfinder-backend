"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import Seen


class ShallowSeenSerializer(serializers.HyperlinkedModelSerializer):
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
        model = Seen
        fields = ['id', 'user', 'title', 'liked', 'disliked', 'primaryTitle', 'backdrop_url', 'poster_url']
