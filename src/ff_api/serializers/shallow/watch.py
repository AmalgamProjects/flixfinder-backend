"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import Watch


class ShallowWatchSerializer(serializers.HyperlinkedModelSerializer):
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

    class Meta:
        model = Watch
        fields = ['url', 'user', 'title']