"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..shallow import \
    ShallowFavouriteSerializer, \
    ShallowFavouriteGenreSerializer, \
    ShallowSeenSerializer, \
    ShallowWatchSerializer
from ...models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='user-detail',
    #     lookup_field='username'
    # )
    favourites = ShallowFavouriteSerializer(many=True, read_only=True)
    favouriteGenres = ShallowFavouriteGenreSerializer(many=True, read_only=True, source='favourite_genres')
    seen = ShallowSeenSerializer(many=True, read_only=True)
    watch = ShallowWatchSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'favourites',
            'favouriteGenres',
            'seen',
            'watch',
        ]
