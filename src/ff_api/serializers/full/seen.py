"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..shallow import ShallowUserSerializer, ShallowTitleSerializer
from ...models import Seen, User, Title
from ...fields import WritableNestedRelatedField


class SeenSerializer(serializers.HyperlinkedModelSerializer):
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

    class Meta:
        model = Seen
        fields = ['url', 'user', 'title']
