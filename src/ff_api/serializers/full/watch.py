"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..shallow import ShallowUserSerializer, ShallowTitleSerializer
from ...models import Watch, User, Title
from ...fields import WritableNestedRelatedField


class WatchSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    user = WritableNestedRelatedField(
        many=False,
        serializer=ShallowUserSerializer,
        slug_field='username',
        model=User,
    )
    title = WritableNestedRelatedField(
        many=False,
        serializer=ShallowTitleSerializer,
        slug_field='tconst',
        model=Title,
    )

    primaryTitle = serializers.CharField(source="get_primary_title", read_only=True)
    backdrop_url = serializers.URLField(source="get_backdrop_url", read_only=True)
    poster_url = serializers.URLField(source="get_poster_url", read_only=True)

    class Meta:
        model = Watch
        fields = ['id', 'user', 'title', 'primaryTitle', 'backdrop_url', 'poster_url']
