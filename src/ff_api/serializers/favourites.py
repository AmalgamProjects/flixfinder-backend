"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from .auth import ShallowUserSerializer
from .imdb import ShallowTitleSerializer
from ..models import Favourite, User, Title
from ..fields import WritableNestedRelatedField


class FavouriteSerializer(serializers.HyperlinkedModelSerializer):
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
        model = Favourite
        fields = ['url', 'user', 'title']
