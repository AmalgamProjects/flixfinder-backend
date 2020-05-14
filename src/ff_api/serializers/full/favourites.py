"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..shallow import ShallowUserSerializer, ShallowTitleSerializer
from ...fields import WritableNestedRelatedField
from ...models import Favourite, FavouriteGenre, User, Title


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


class FavouriteGenreSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    user = WritableNestedRelatedField(
        many=False,
        serializer=ShallowUserSerializer,
        slug_field='username',
        model=User,
    )
    genre = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=FavouriteGenre.objects.all()
    )

    class Meta:
        model = FavouriteGenre
        fields = ['url', 'user', 'genre']
