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

    primaryTitle = serializers.CharField(source="get_primary_title", read_only=True)
    backdrop_url = serializers.URLField(source="get_backdrop_url", read_only=True)
    poster_url = serializers.URLField(source="get_poster_url", read_only=True)

    class Meta:
        model = Favourite
        fields = ['id', 'user', 'title', 'primaryTitle', 'backdrop_url', 'poster_url']


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
        fields = ['id', 'user', 'genre']
