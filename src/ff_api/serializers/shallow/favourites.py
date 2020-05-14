"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import Favourite, FavouriteGenre


class ShallowFavouriteSerializer(serializers.HyperlinkedModelSerializer):
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
        model = Favourite
        fields = ['url', 'user', 'title']


class ShallowFavouriteGenreSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
    )
    genre = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=FavouriteGenre.objects.all()
    )

    class Meta:
        model = FavouriteGenre
        fields = ['url', 'user', 'genre']
